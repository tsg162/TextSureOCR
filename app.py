"""
TextSureOCR — text forensics via token-level language-model scoring.

Endpoints:
  POST /v1/ocr/check              → detect OCR errors via per-token softmax analysis
  POST /v1/text/check-continuation → evaluate boundary continuity via conditional log-probs

Detection strategy (OCR check):
  1. Single forward pass → softmax probabilities at every token position
  2. For each token i, compare P(actual_i | prefix) against the model's top predictions
  3. Tokens with very low probability (< floor) are suspicious
  4. Aggregate suspicious tokens to word level
  5. Build correction candidates from the model's top-k predictions at suspicious positions
  6. Score [original, corrections] by full-text log-probability to filter false positives

Continuation strategy:
  PMI = avg_log_prob(second | first) − avg_log_prob(second)
  Combined with absolute conditional probability so gibberish never scores high.
"""

import os
import re
import math
import asyncio
import logging
from contextlib import asynccontextmanager
from difflib import SequenceMatcher

import torch
import torch.nn.functional as F
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
from transformers import AutoTokenizer, AutoModelForCausalLM

# ── Configuration ──────────────────────────────────────────────────────

AUTH_TOKEN       = os.getenv("TEXTSURE_AUTH_TOKEN", "")
VAST_INSTANCE_ID = os.getenv("TEXTSURE_VAST_INSTANCE_ID", "")
MODEL_ID         = os.getenv("TEXTSURE_MODEL", "Qwen/Qwen3-8B-Base")
DEVICE           = "cuda" if torch.cuda.is_available() else "cpu"
# Qwen3 is trained in bf16; using fp16 on bf16 checkpoints can produce NaNs
# in softmax tails, which matters for low-probability tokens (the exact regime
# this app inspects). Stay in bf16 on CUDA.
DTYPE            = torch.bfloat16 if DEVICE == "cuda" else torch.float32

TOKEN_PROB_FLOOR = float(os.getenv("TEXTSURE_TOKEN_PROB_FLOOR", "0.05"))
MIN_LP_GAIN      = float(os.getenv("TEXTSURE_MIN_LP_GAIN", "4.0"))
SIMILARITY_FLOOR = float(os.getenv("TEXTSURE_SIMILARITY_FLOOR", "0.5"))
TOP_K            = 5
MIN_WORD_LEN     = 2
MAX_HEURISTIC_CANDIDATES = 14

# Debug mode: set via env var or query param for detailed diagnostics
DEBUG_MODE       = os.getenv("TEXTSURE_DEBUG", "").lower() in ("1", "true", "yes")

# Branch-and-explore: proactively try OCR corrections on all words
BRANCH_EXPLORE   = os.getenv("TEXTSURE_BRANCH_EXPLORE", "").lower() in ("1", "true", "yes")

# OCR character confusion map: glyphs often misread as each other.
# Keys are sequences we find in suspect words; values are plausible true readings.
CONFUSIONS: dict[str, list[str]] = {
    "0":  ["o", "O"],
    "1":  ["l", "i", "I"],
    "5":  ["s", "S"],
    "8":  ["B"],
    "6":  ["b", "G"],
    "2":  ["Z"],
    "rn": ["m"],
    "vv": ["w"],
    # "cl" and "d" are mutually-confusable: print "cl" can scan as "d"
    # (include→indude) and vice-versa. We want candidates in both
    # directions, so list both keys; _heuristic_candidates takes the
    # union of matches.
    "cl": ["d"],
    "d":  ["cl"],
    "|":  ["l", "I"],
    # ── rrn: doubled-r artifact when m→rn occurs after an existing r ──
    # Words ending in -rm (alarm, form, storm, warm, etc.): the "m" is
    # OCR'd as "rn", and the preceding "r" gives "r"+"rn" = "rrn".
    # Fix: "rrn" → "rm"  (alarrn→alarm, storrn→storm, forrn→form).
    "rrn": ["rm"],
    # ── fi-ligature garble: fi scans as ft or fm ──
    # (ftre→fire, fmd→find, ftnal→final). Some cases need length-
    # changing substitutions (fmd→find: 3→4 chars, "m" → "in").
    "ft": ["fi"],
    "fm": ["fi", "fin"],
}

# Corrections that require position-specific matching, kept separate
# from CONFUSIONS so we don't generate noisy candidates on every "d"
# in the document. Applied only when the containing word is
# structurally suspicious (non-dictionary shape near a morpheme).
_D_FOR_CL_MORPHEMES = (
    "de", "da", "du",   # prefix-ish: indude/declare/reduce
)

# Single-position (NOT replace-all) OCR substitutions. Each entry
# generates one candidate per occurrence, so a word with two 'd's
# yields two candidates per replacement, never a garbled replace-all.
# Used for broad char-confusions that would explode candidate counts
# under replace-all (d→c for cirdular→circular, d→l for vehicde→vehicle).
POSITIONAL_CONFUSIONS: dict[str, list[str]] = {
    "d": ["c", "l"],
    "c": ["d"],
    "l": ["d"],
}

log = logging.getLogger("textsure")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")


# ── Pydantic schemas ───────────────────────────────────────────────────

class Suggestion(BaseModel):
    text: str
    score: float

class Span(BaseModel):
    start: int
    end: int
    text: str
    kind: str
    suggestions: list[Suggestion] = []

class CheckRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10_000)
    debug: bool = False  # Enable detailed diagnostics in response

class TokenDebug(BaseModel):
    text: str                                          # The actual text at this position
    token_id: int = 0                                  # Model's token ID
    char_start: int
    char_end: int
    actual_prob: float                                 # P(actual | prefix)
    actual_log_prob: float = 0.0                       # log P
    top_predictions: list[tuple[str, float, int]] = [] # (text, prob, token_id)
    is_suspicious: bool = False                        # Below TOKEN_PROB_FLOOR
    word_context: str | None = None                    # Which word this token belongs to


class WordDebug(BaseModel):
    word: str
    start: int
    end: int
    # Tokenization info
    tokenization: list[str] = []                       # How this word tokenizes ["▁dis", "dose"]
    token_ids: list[int] = []                          # Corresponding token IDs
    token_probs: list[float] = []                      # Per-token probabilities
    word_surprisal: float = 0.0                        # Mean negative log-prob

    # Detection info
    suspicious_tokens: list[int] = []                  # Indices of low-prob tokens
    structural_match: bool = False
    structural_reasons: list[str] = []                 # ["d_in_word", "rn_pattern", etc.]
    branch_explore: bool = False                       # Included via BRANCH_EXPLORE mode

    # Candidate generation
    softmax_candidates: list[str] = []                 # From top-k at suspicious positions
    heuristic_candidates: list[str] = []               # From confusion map
    candidates_pre_filter: list[str] = []              # Before similarity/shape filter
    candidates_post_filter: list[str] = []             # After filtering

    # Scoring
    scores: dict[str, float] = {}                      # {candidate: softmax_score}
    raw_log_probs: dict[str, float] = {}               # {candidate: total_log_prob}
    improvement: float = 0.0                           # best_correction_lp - original_lp

    # Decision
    outcome: str = ""                                  # "flagged", "fp_original_wins", etc.
    outcome_reason: str = ""                           # Human-readable explanation

    # Legacy compatibility
    tokens: list[TokenDebug] = []
    candidates_generated: list[str] = []
    candidates_after_filter: list[str] = []


class BranchExploreResult(BaseModel):
    word: str
    start: int
    end: int
    original_tokenization: list[str] = []
    original_log_prob: float = 0.0
    corrections_tried: list[dict] = []                 # Each correction attempt


class DebugInfo(BaseModel):
    all_tokens: list[TokenDebug] = []
    words_analyzed: list[WordDebug] = []
    branch_explore_results: list[BranchExploreResult] = []

class CheckResponse(BaseModel):
    result: str
    score: float
    spans: list[Span] = []
    debug: DebugInfo | None = None

class ContinuationRequest(BaseModel):
    first: str  = Field(..., min_length=1, max_length=5_000)
    second: str = Field(..., min_length=1, max_length=5_000)
    debug: bool = False


class ContinuationDebug(BaseModel):
    # Tokenization
    first_tokens: list[str] = []
    second_tokens: list[str] = []
    joint_tokens: list[str] = []                       # first + " " + second
    boundary_token_idx: int = 0                        # Where second starts in joint

    # Conditional scoring
    conditional_token_probs: list[float] = []          # P(second_token_i | first + preceding)
    conditional_avg_log_prob: float = 0.0

    # Unconditional scoring
    unconditional_token_probs: list[float] = []        # P(second_token_i | preceding_only)
    unconditional_avg_log_prob: float = 0.0

    # PMI calculation
    pmi: float = 0.0                                   # conditional - unconditional
    pmi_score: float = 0.0                             # sigmoid((PMI - 0.5) * 3)
    abs_score: float = 0.0                             # sigmoid((cond_avg + 5) * 1.5)
    final_score: float = 0.0                           # pmi_score * abs_score

    # Decision
    threshold: float = 0.5
    verdict: str = ""                                  # "likely_continuation" or "unlikely"


class ContinuationResponse(BaseModel):
    result: str
    score: float
    debug: ContinuationDebug | None = None


# ── Model manager ──────────────────────────────────────────────────────

class LM:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self._lock = asyncio.Lock()

    async def load(self):
        if self.model is not None:
            return
        async with self._lock:
            if self.model is not None:
                return
            log.info("Loading %s → %s (%s) …", MODEL_ID, DEVICE, DTYPE)
            self.tokenizer = AutoTokenizer.from_pretrained(
                MODEL_ID, trust_remote_code=True,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                MODEL_ID,
                torch_dtype=DTYPE,
                device_map="auto",
                trust_remote_code=True,
            )
            self.model.eval()
            log.info("Model loaded. Ready for inference.")

    def unload(self):
        if self.model is None:
            return
        del self.model, self.tokenizer
        self.model = self.tokenizer = None
        if DEVICE == "cuda":
            torch.cuda.empty_cache()


lm = LM()
_gpu_sem = asyncio.Semaphore(1)


# ── Token-level analysis ──────────────────────────────────────────────

def _token_predictions(text: str) -> list[dict]:
    """
    Single forward pass.  For each token position i > 0, returns:
      - char_start, char_end  (character offsets in the original text)
      - actual_text           (the characters at that position)
      - actual_id             (token ID of the actual token)
      - actual_prob           (P(actual_token_i | tokens_0..i-1))
      - actual_log_prob       (log P(actual_token_i | tokens_0..i-1))
      - top_preds             (top-K alternative tokens as [(token_id, prob), ...])

    This is the core primitive: the model sees tokens 0..i-1 and tells us
    how likely the actual token i is, and what it would have predicted instead.
    """
    enc = lm.tokenizer(
        text, return_tensors="pt",
        return_offsets_mapping=True, add_special_tokens=False,
    )
    ids     = enc["input_ids"].to(DEVICE)
    offsets = enc["offset_mapping"][0]
    if ids.shape[1] < 2:
        return []
    with torch.no_grad():
        logits = lm.model(ids).logits[0]
    probs = F.softmax(logits, dim=-1)
    log_probs = F.log_softmax(logits, dim=-1)

    out: list[dict] = []
    for i in range(1, ids.shape[1]):
        actual_id   = ids[0, i].item()
        actual_prob = probs[i - 1, actual_id].item()
        actual_log_prob = log_probs[i - 1, actual_id].item()
        top_vals, top_ids = probs[i - 1].topk(TOP_K)
        cs = int(offsets[i][0].item())
        ce = int(offsets[i][1].item())
        out.append({
            "char_start":  cs,
            "char_end":    ce,
            "actual_text": text[cs:ce],
            "actual_id":   actual_id,
            "actual_prob": actual_prob,
            "actual_log_prob": actual_log_prob,
            "top_preds":   [(top_ids[j].item(), top_vals[j].item()) for j in range(TOP_K)],
        })
    return out


def _token_log_probs(text: str) -> list[tuple[int, int, float]]:
    """
    Forward-pass *text*, return per-token (char_start, char_end, log_prob).
    Skips the first token (no left context).
    Used by full-text scoring and continuation check.
    """
    enc = lm.tokenizer(
        text, return_tensors="pt",
        return_offsets_mapping=True, add_special_tokens=False,
    )
    ids     = enc["input_ids"].to(DEVICE)
    offsets = enc["offset_mapping"][0]
    if ids.shape[1] < 2:
        return []
    with torch.no_grad():
        logits = lm.model(ids).logits[0]
    lps = F.log_softmax(logits, dim=-1)
    out: list[tuple[int, int, float]] = []
    for i in range(1, ids.shape[1]):
        tid = ids[0, i].item()
        lp  = lps[i - 1, tid].item()
        cs, ce = int(offsets[i][0].item()), int(offsets[i][1].item())
        out.append((cs, ce, lp))
    return out


def _total_log_prob(text: str) -> float:
    """Sum of per-token log-probs for the full text (one forward pass)."""
    return sum(lp for _, _, lp in _token_log_probs(text))


# ── Correction generation ─────────────────────────────────────────────

def _build_correction(word: str, word_start: int, word_end: int,
                      word_tokens: list[dict],
                      suspicious: list[dict],
                      rank: int = 0) -> str:
    """
    Build a corrected word by replacing suspicious tokens with the model's
    top prediction at those positions.

    rank=0 uses top-1, rank=1 uses top-2, etc.
    Returns the reconstructed word string.
    """
    result = word
    # Process replacements in reverse character order to preserve indices
    replacements = []
    for tok in sorted(suspicious, key=lambda t: t["char_start"], reverse=True):
        cs, ce = tok["char_start"], tok["char_end"]
        overlap_start = max(cs, word_start) - word_start
        overlap_end   = min(ce, word_end) - word_start
        if rank < len(tok["top_preds"]):
            top_id, top_prob = tok["top_preds"][rank]
            alt_text = lm.tokenizer.decode([top_id]).strip()
            if alt_text:
                replacements.append((overlap_start, overlap_end, alt_text))
    for start, end, alt in replacements:
        result = result[:start] + alt + result[end:]
    return result


def _first_word(text: str) -> str:
    hit = re.search(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", text)
    return hit.group().lower() if hit else ""


# ── Structural / character-confusion heuristics ────────────────────────

# A word is structurally suspicious if it:
#   (a) mixes alphabetic characters with digits (schoo1, c0mputer, 1etter)
#   (b) contains an "rn" inside a word and isn't a known -rn word
#       (governrnent, hurnan, rnedical — catches single and doubled rn)
#   (c) contains "vv" inside an alpha run (vvord → word)
#   (d) contains a pipe among letters (he|lo)
#   (e) word-initial "ft" or "fm" followed by alpha — fi-ligature garble
#   (f) "rrn" or "rrm" — doubled-r m-substitution artifact
#   (g) "d" between vowels inside a non-dictionary shape — cl→d OCR
_DIGIT_IN_ALPHA = re.compile(r"[A-Za-z][0-9]|[0-9][A-Za-z]")
_RN_IN_ALPHA    = re.compile(r"(?:^|[A-Za-z])rn(?:$|[A-Za-z])", re.IGNORECASE)
_VV_IN_ALPHA    = re.compile(r"[A-Za-z]vv|vv[A-Za-z]")
_PIPE_IN_ALPHA  = re.compile(r"[A-Za-z]\||\|[A-Za-z]")
_FI_GARBLE      = re.compile(r"^f[tm][a-z]|[a-z]f[tm][a-z]", re.IGNORECASE)
_RRN_DOUBLED    = re.compile(r"rr[nm]", re.IGNORECASE)
# Any "d" in word could be OCR'd "cl". We filter false positives via
# the safe-word list and let log-prob scoring do the final decision.
# Old approach required d between vowels - too restrictive (missed "disdose").
_D_IN_WORD = re.compile(r"[a-zA-Z]d|d[a-zA-Z]")
# Word that contains zero alphabetic characters — pure digits/punctuation
# like "16", "750", "--", "555-0140". Not OCR-checkable as a "word".
_NO_ALPHA       = re.compile(r"^[^A-Za-z]+$")
# Punctuation characters stripped from word-span boundaries so that
# span.text / offsets cover the word itself, not trailing commas, periods,
# quotes, parens, etc. Internal punctuation (hyphens/apostrophes in the
# middle of "mother-in-law", "don't") is untouched because str.strip only
# removes characters from the ends.
_WORD_PUNCT = ".,;:!?\"'`()[]{}<>“”‘’…—–-"

# Legitimate English words that contain "rn" — these should NOT trip
# the single-rn structural flag. Generous to avoid false positives;
# the downstream LP-gain filter will re-check anyway.
_RN_SAFE_WORDS = frozenset({
    # verbs / nouns with rn
    "corn", "born", "torn", "yarn", "worn", "horn", "barn", "earn",
    "earns", "earned", "earning", "earnings", "earnest",
    "learn", "learns", "learned", "learner", "learning",
    "turn", "turns", "turned", "turning", "return", "returns",
    "returned", "returning", "turnaround", "turnout", "turnover", "turnpike",
    "burn", "burns", "burned", "burning", "burnt", "burner", "sunburn",
    "concern", "concerns", "concerned", "concerning",
    "pattern", "patterns", "patterned",
    "modern", "modernity", "modernize",
    "morning", "mornings",
    "warning", "warnings",
    "kernel", "kernels",
    "journal", "journals", "journalist", "journalism",
    "journey", "journeys", "journeyed",
    "adorn", "adorns", "adorned", "adornment",
    "thorn", "thorns", "thorny",
    "scorn", "scorns", "scorned",
    "mourn", "mourns", "mourned", "mourning", "mourner",
    "stern", "sterns", "sternly",
    "intern", "interns", "internal", "international", "internet",
    "internally", "internally", "internship",
    "govern", "governs", "governed", "governing", "government",
    "governments", "governor", "governance",
    "alternate", "alternating", "alternative", "alternatives",
    "alternatively", "alternative",
    "eastern", "western", "northern", "southern", "southwestern",
    "northeastern", "northwestern", "southeastern",
    "hibernate", "hibernation",
    "subordinate", "coordinate", "coordination", "coordinator",
    "tavern", "taverns", "cavern", "caverns", "cavernous",
    "lantern", "lanterns",
    "cornea", "corneal", "corner", "corners", "cornering",
    "cornerstone", "cornerstones",
    "garner", "garnered", "garnering",
    "harness", "harnessed", "harnessing",
    "earnest", "earnestly", "earnestness",
    "tarnish", "tarnished", "tarnishing",
    "furnish", "furnished", "furniture",
    "girl", "girls",  # not rn but guard against false match (not needed)
    "ornament", "ornamental", "ornate",
    "supernova", "hornet", "hornets",
    "bourne", "fortnight",
    "discern", "discerning", "discerned",
    "yearn", "yearns", "yearned", "yearning",
    "spurn", "spurns", "spurned",
    "cornflake", "cornflakes", "cornfield",
    "marney", "barney", "journey",
})

# Common English words with "d" that should NOT trigger cl→d detection.
# This is a large list because we now flag ANY word with "d" adjacent to
# letters. The log-prob scoring does final filtering, but this list
# prevents expensive scoring passes on obviously-correct common words.
_D_SAFE_WORDS = frozenset({
    # -ade words
    "made", "fade", "wade", "blade", "glade", "grade", "trade", "shade",
    "spade", "upgrade", "degrade", "cascade", "decade", "arcade",
    "parade", "crusade", "invade", "evade", "pervade", "brigade",
    "handmade", "homemade", "lemonade", "promenade", "blockade",
    # -ide words
    "side", "ride", "hide", "tide", "wide", "bride", "pride", "slide",
    "glide", "stride", "provide", "divide", "beside", "decide", "guide",
    "outside", "inside", "upside", "aside", "reside", "subside",
    "collide", "abide", "preside", "override", "landslide", "worldwide",
    # -ode words
    "node", "code", "mode", "rode", "erode", "bode", "abode", "episode",
    "explode", "corrode", "anode", "diode", "methodology", "encode", "decode",
    # -ude words
    "dude", "rude", "crude", "etude", "nude", "allude", "elude",
    "exclude", "include", "preclude", "conclude", "delude", "extrude",
    "seclude", "intrude", "magnitude", "attitude", "altitude", "latitude",
    # Very common words with d
    "and", "said", "had", "would", "could", "should", "did", "good", "bad",
    "old", "new", "end", "find", "found", "hand", "hands", "kind", "mind",
    "need", "needed", "used", "called", "world", "word", "words", "made",
    "day", "days", "today", "yesterday", "red", "bed", "head", "read",
    "dead", "lead", "bread", "spread", "thread", "instead", "ahead",
    "add", "added", "odd", "sudden", "hidden", "forbidden", "middle",
    "children", "garden", "modern", "golden", "wooden", "sudden",
    "hundred", "considered", "indeed", "understand", "understood",
    "riend", "friend", "friends", "send", "spend", "depend", "extend",
    "defend", "offend", "suspend", "recommend", "trend", "blend",
    "second", "beyond", "around", "ground", "sound", "found", "round",
    "bound", "pound", "wound", "background", "underground",
    "standard", "understand", "demand", "command", "expand", "brand",
    "grand", "hand", "land", "band", "sand", "stand", "island",
    "wind", "kind", "mind", "find", "behind", "remind", "blind",
    "hold", "told", "cold", "gold", "bold", "sold", "fold", "old",
    "field", "build", "child", "wild", "mild", "guild", "yield",
    "board", "record", "toward", "forward", "reward", "word", "lord",
    "order", "ordered", "border", "disorder", "record", "accord",
    "food", "good", "mood", "wood", "hood", "flood", "blood", "stood",
    "road", "load", "broad", "abroad", "download", "upload",
    "head", "dead", "read", "lead", "bread", "spread", "thread",
    "instead", "ahead", "widespread",
    "bed", "red", "fed", "led", "shed", "sped", "wed", "fled", "bred",
    "speed", "need", "feed", "seed", "deed", "breed", "proceed", "exceed",
    "succeed", "indeed",
    "add", "odd", "added", "adding", "addition", "additional", "address",
    "middle", "muddle", "puddle", "riddle", "saddle", "paddle", "meddle",
    "sudden", "hidden", "forbidden", "ridden", "madden", "gladden",
    "garden", "burden", "warden", "harden", "pardon",
    "modern", "golden", "wooden", "olden", "embolden",
    "children", "brethren",
    "under", "wonder", "thunder", "blunder", "plunder", "asunder",
    "hundred", "kindred",
    "idea", "ideal", "ideas", "ideally", "identity", "identify",
    "identical", "ideology",
    "media", "medium", "audio", "radio", "video", "studio",
    "body", "nobody", "everybody", "somebody", "anybody",
    "lady", "study", "studied", "studies", "studying", "ready", "already",
    "steady", "unsteady", "heady", "shady", "windy", "cloudy", "muddy",
    "edit", "edits", "edited", "editing", "editor", "edition", "editorial",
    "credit", "credits", "audit", "reddit",
    "model", "models", "modem", "modest", "modify", "modified",
    "adopt", "adopted", "adoption", "adapt", "adapted", "adaptation",
    "adult", "adults", "adequate", "adequately", "inadequate",
    "advice", "advise", "advised", "advisor", "advocate", "advocacy",
    "advance", "advanced", "advancement", "advantage", "adventure",
    "advertise", "advertisement", "advertised",
    "education", "educational", "educator", "educate", "educated",
    "individual", "individuals", "individually",
    "industry", "industrial", "industries",
    "product", "products", "production", "produce", "produced", "producer",
    "period", "periods", "periodic", "periodically",
    "method", "methods", "methodology",
    "president", "presidential", "resident", "residential",
    "student", "students", "accident", "accidental", "incident",
    "evidence", "evident", "evidently", "provide", "provided", "provider",
    "decide", "decided", "decision", "dividend",
    "consider", "considered", "consideration",
    "understand", "understood", "understanding", "misunderstand",
    "during", "procedure", "procedures",
    "ود", "údržba",  # non-English but might appear
})


_STRIP_PUNCT = re.compile(r"^[^A-Za-z]+|[^A-Za-z]+$")


def _core_word(word: str) -> str:
    """Strip leading/trailing punctuation so 'commitment,' == 'commitment'."""
    return _STRIP_PUNCT.sub("", word).lower()


def _get_structural_reasons(word: str) -> list[str]:
    """Return list of all structural patterns matched by this word."""
    reasons = []
    w = _core_word(word)

    if _DIGIT_IN_ALPHA.search(word):
        reasons.append("digit_in_alpha")
    if _VV_IN_ALPHA.search(word):
        reasons.append("vv_pattern")
    if _PIPE_IN_ALPHA.search(word):
        reasons.append("pipe_in_alpha")
    if _RRN_DOUBLED.search(word):
        reasons.append("rrn_doubled")
    if _FI_GARBLE.search(word):
        reasons.append("fi_garble")
    if _RN_IN_ALPHA.search(word) and w not in _RN_SAFE_WORDS:
        reasons.append("rn_pattern")
    if _D_IN_WORD.search(word) and w not in _D_SAFE_WORDS:
        reasons.append("d_in_word")

    return reasons


def _is_structurally_suspicious(word: str) -> bool:
    return len(_get_structural_reasons(word)) > 0


def _occurrences(word: str, key: str) -> list[tuple[int, int]]:
    """Find (start, end) spans of every case-insensitive occurrence of *key*."""
    spans = []
    lower = word.lower()
    k = key.lower()
    i = 0
    while True:
        j = lower.find(k, i)
        if j < 0:
            break
        spans.append((j, j + len(k)))
        i = j + 1  # allow overlapping matches (e.g. "rnrn" has two at 0,1,2)
    return spans


def _heuristic_candidates(word: str) -> list[str]:
    """
    Generate correction candidates by applying OCR confusion substitutions.

    For each confusion key, enumerate both:
      * replace-all: every occurrence of the key → replacement (handles
        "cornrnitrnent" → "commitment" where every `rn` is really an `m`)
      * single-position: exactly one occurrence replaced (handles
        "governrnent" → "government" where only one of two `rn`s is an `m`)
    Candidates are capped to keep downstream scoring cheap.
    """
    seen: set[str] = set()
    out: list[str] = []

    def add(cand: str):
        cl = cand.lower()
        if cand and cand != word and cl not in seen:
            seen.add(cl)
            out.append(cand)

    for key, replacements in CONFUSIONS.items():
        spans = _occurrences(word, key)
        if not spans:
            continue
        for rep in replacements:
            # Replace-all variant.
            if key.isalpha():
                add(re.sub(re.escape(key), rep, word, flags=re.IGNORECASE))
            else:
                add(word.replace(key, rep))
            # Single-position variants (only matters when >1 occurrence).
            if len(spans) > 1:
                for s, e in spans:
                    add(word[:s] + rep + word[e:])

    # Combined all-key candidate for multi-confusion tokens like "c0rnrni".
    combined = word
    for key, replacements in CONFUSIONS.items():
        rep = replacements[0]
        if key.isalpha():
            combined = re.sub(re.escape(key), rep, combined, flags=re.IGNORECASE)
        else:
            combined = combined.replace(key, rep)
    add(combined)

    # Positional-only substitutions: one candidate per occurrence, never
    # replace-all. Handles cirdular→circular (d@3→c), vehicde→vehicle
    # (d@5→l) without polluting common words.
    for key, replacements in POSITIONAL_CONFUSIONS.items():
        spans = _occurrences(word, key)
        if not spans:
            continue
        for rep in replacements:
            for s, e in spans:
                add(word[:s] + rep + word[e:])

    return out[:MAX_HEURISTIC_CANDIDATES]


# Common-English allow-list used to suppress false positives on clean prose.
# If the "suspect" word is a plain dictionary-shaped lowercase alpha word,
# and the best correction differs only stylistically, skip flagging it.
_COMMON_WORD_SHAPE = re.compile(r"^[a-z]{2,}$")


def _looks_like_common_word(word: str) -> bool:
    """Cheap shape check: purely alphabetic lowercase form, 2+ chars."""
    return bool(_COMMON_WORD_SHAPE.match(word.lower()))


def _looks_like_code(word: str) -> bool:
    """
    Tracking numbers / SKUs / IDs: long mixed-alphanumeric strings with
    many letter/digit transitions and several digits. These trip the
    digit-in-alpha structural rule but are legitimate — the LM will
    happily hallucinate "corrections" that are just different digit strings.

    Must be distinguishable from single-digit-sub words like "c0mputer"
    (len 8, 2 transitions, 1 digit) which *are* OCR errors we want to flag.
    """
    if len(word) < 10:
        return False
    digit_count = sum(c.isdigit() for c in word)
    alpha_count = sum(c.isalpha() for c in word)
    if digit_count < 3 or alpha_count < 1:
        return False
    transitions, prev = 0, None
    for c in word:
        kind = "a" if c.isalpha() else "d" if c.isdigit() else None
        if kind is not None and prev is not None and kind != prev:
            transitions += 1
        if kind is not None:
            prev = kind
    return transitions >= 3


def _edit_distance(a: str, b: str) -> int:
    """Plain Levenshtein distance between two short strings."""
    a, b = a.lower(), b.lower()
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(
                prev[j] + 1,            # deletion
                cur[j - 1] + 1,         # insertion
                prev[j - 1] + (ca != cb),  # substitution
            )
        prev = cur
    return prev[-1]


# ── Candidate scoring (full-text log-prob comparison) ──────────────────

def _score_candidates(
    text: str, ws: int, we: int, candidates: list[str],
) -> tuple[list[float], list[float]]:
    """
    Score each candidate by substituting it into the text and computing
    the full-text log-probability.

    Returns (softmax_scores, raw_log_probs).  The raw log-probs let the
    caller compute the absolute improvement from a correction.
    """
    raw: list[float] = []
    for cand in candidates:
        full = text[:ws] + cand + text[we:]
        raw.append(_total_log_prob(full))
    if not raw:
        return [], []
    mx   = max(raw)
    exps = [math.exp(r - mx) for r in raw]
    s    = sum(exps)
    return [round(e / s, 3) for e in exps], raw


# ── Branch-and-explore: try OCR corrections proactively ───────────────

def _branch_explore_word(
    text: str, word: str, ws: int, we: int
) -> tuple[float, str | None, list[tuple[str, float]]]:
    """
    Try all OCR correction candidates for a word and score them.

    Returns:
        (improvement, best_candidate, all_scored)
        - improvement: log-prob gain of best correction over original (nats)
        - best_candidate: the correction with highest score, or None
        - all_scored: list of (candidate, raw_log_prob) for debugging
    """
    # Generate candidates from confusion map
    cands = _heuristic_candidates(word)
    if not cands:
        return 0.0, None, []

    # Filter by similarity - OCR corrections must resemble original
    cands = [
        c for c in cands
        if SequenceMatcher(None, word.lower(), c.lower()).ratio() > SIMILARITY_FLOOR
    ]
    if not cands:
        return 0.0, None, []

    # Score [original, *corrections]
    all_cands = [word] + cands
    scores, raw_lps = _score_candidates(text, ws, we, all_cands)

    if len(raw_lps) < 2:
        return 0.0, None, []

    # Find best correction
    orig_lp = raw_lps[0]
    best_idx = 1
    best_lp = raw_lps[1]
    for i in range(2, len(raw_lps)):
        if raw_lps[i] > best_lp:
            best_lp = raw_lps[i]
            best_idx = i

    improvement = best_lp - orig_lp
    best_cand = all_cands[best_idx] if improvement > 0 else None

    # Build debug info
    all_scored = list(zip(all_cands, raw_lps))

    return improvement, best_cand, all_scored


def _has_ocr_pattern(word: str) -> bool:
    """Check if word contains any OCR confusion pattern worth exploring."""
    w = word.lower()
    # Check main confusion map keys
    for key in CONFUSIONS:
        if key.lower() in w:
            return True
    # Check positional confusion keys
    for key in POSITIONAL_CONFUSIONS:
        if key.lower() in w:
            return True
    return False


# ── /v1/ocr/check ─────────────────────────────────────────────────────

def _ocr_check(text: str, debug: bool = False) -> CheckResponse:
    debug_info = DebugInfo() if (debug or DEBUG_MODE) else None
    preds = _token_predictions(text)
    if not preds:
        return CheckResponse(result="ok", score=0.95, spans=[], debug=debug_info)

    # Collect token debug info
    if debug_info is not None:
        for t in preds:
            top_preds = [
                (lm.tokenizer.decode([tid]).strip(), prob, tid)
                for tid, prob in t["top_preds"]
            ]
            debug_info.all_tokens.append(TokenDebug(
                text=t["actual_text"],
                token_id=t["actual_id"],
                char_start=t["char_start"],
                char_end=t["char_end"],
                actual_prob=t["actual_prob"],
                actual_log_prob=t["actual_log_prob"],
                top_predictions=top_preds,
                is_suspicious=t["actual_prob"] < TOKEN_PROB_FLOOR,
            ))

    # ── Phase 1: find words with suspicious tokens ──
    # A word enters Phase 2 if ANY of:
    #   (a) it contains a token with P(actual | prefix) < floor  (LM signal), OR
    #   (b) it matches a structural OCR-confusion pattern         (heuristic signal), OR
    #   (c) BRANCH_EXPLORE is enabled and word has an OCR pattern worth trying
    word_candidates: list[tuple[str, int, int, list[dict], list[dict], bool]] = []

    for m in re.finditer(r"\S+", text):
        raw, rs, re_ = m.group(), m.start(), m.end()
        # Strip leading/trailing punctuation so the span covers just the
        # word itself — not trailing commas, periods, quotes, parens, etc.
        lstrip = len(raw) - len(raw.lstrip(_WORD_PUNCT))
        rstrip = len(raw) - len(raw.rstrip(_WORD_PUNCT))
        ws = rs + lstrip
        we = re_ - rstrip
        if we <= ws:
            continue
        word = text[ws:we]
        if len(word) < MIN_WORD_LEN:
            continue

        # Pure digits/punctuation (e.g. "16", "750", "--", "$50") aren't
        # OCR-checkable as words — the only OCR-error case for them
        # (digit-in-alpha) is already covered by the structural pattern,
        # which requires alpha context. Skipping suppresses false positives
        # on legitimate numbers, currency, dates, and punctuation runs.
        if _NO_ALPHA.match(word):
            continue

        # Tokens overlapping this word
        word_tokens = [t for t in preds if t["char_start"] < we and t["char_end"] > ws]
        if not word_tokens:
            continue

        # Suspicious tokens: very low actual probability
        suspicious = [
            t for t in word_tokens
            if t["actual_prob"] < TOKEN_PROB_FLOOR
        ]

        # Long alphanumeric codes (tracking numbers, SKUs, IDs) look
        # structurally suspicious by the digit-in-alpha rule, but their
        # letter/digit intermixing is legitimate. Suppress both the
        # structural flag and any LM-based flagging for them.
        if _looks_like_code(word):
            continue

        structural = _is_structurally_suspicious(word)

        # LM veto for structural-only flags: if every token in the word
        # has high actual probability, the LM is confident the word fits
        # the context. Don't waste a candidate-scoring pass on it.
        # This lets us keep the regex rules generous without flooding
        # clean prose with false positives.
        if structural and not suspicious:
            min_prob = min(t["actual_prob"] for t in word_tokens)
            if min_prob > 0.5:
                structural = False

        # Branch-and-explore: also include words with OCR patterns even if
        # they passed surprisal/structural checks. Let scoring decide.
        branch_explore = False
        if BRANCH_EXPLORE and not suspicious and not structural:
            if _has_ocr_pattern(word):
                branch_explore = True
                log.info("  branch-explore: trying corrections on '%s'", word)

        if not suspicious and not structural and not branch_explore:
            continue

        # Log what we found
        for t in suspicious:
            top_id, top_prob = t["top_preds"][0]
            top_text = lm.tokenizer.decode([top_id]).strip()
            log.info(
                "  token [%s] P=%.4f — model prefers [%s] P=%.4f  (in word '%s')",
                t["actual_text"], t["actual_prob"],
                top_text, top_prob,
                word,
            )
        if structural and not suspicious:
            log.info("  structural match on '%s' (no LM signal)", word)
        # Include branch_explore flag (treated as structural for filtering purposes)
        is_structural = structural or branch_explore
        structural_reasons = _get_structural_reasons(word) if structural else []
        word_candidates.append((word, ws, we, word_tokens, suspicious, is_structural, branch_explore, structural_reasons))

    log.info(
        "OCR check: %d tokens, floor=%.3f, candidate words=%d (%s)",
        len(preds), TOKEN_PROB_FLOOR,
        len(word_candidates),
        ", ".join(w for w, _, _, _, _, _, _, _ in word_candidates),
    )

    if not word_candidates:
        min_prob = min(t["actual_prob"] for t in preds)
        margin = min(min_prob / TOKEN_PROB_FLOOR, 1.0) if TOKEN_PROB_FLOOR > 0 else 1.0
        conf = 0.80 + 0.19 * min(margin, 1.0)
        return CheckResponse(result="ok", score=round(conf, 3), spans=[], debug=debug_info)

    # ── Phase 2: build corrections, score, and filter ──
    spans: list[Span] = []
    for word, ws, we, word_tokens, suspicious, structural, branch_explore_flag, structural_reasons in word_candidates:
        # Initialize debug entry for this word
        word_debug = None
        if debug_info is not None:
            # Collect tokenization info for this word
            tokenization = [lm.tokenizer.decode([t["actual_id"]]) for t in word_tokens]
            token_ids = [t["actual_id"] for t in word_tokens]
            token_probs = [t["actual_prob"] for t in word_tokens]
            token_log_probs = [t["actual_log_prob"] for t in word_tokens]
            word_surprisal = -sum(token_log_probs) / len(token_log_probs) if token_log_probs else 0.0
            suspicious_indices = [i for i, t in enumerate(word_tokens) if t["actual_prob"] < TOKEN_PROB_FLOOR]

            word_debug = WordDebug(
                word=word, start=ws, end=we,
                tokenization=tokenization,
                token_ids=token_ids,
                token_probs=token_probs,
                word_surprisal=word_surprisal,
                suspicious_tokens=suspicious_indices,
                structural_match=structural,
                structural_reasons=structural_reasons,
                branch_explore=branch_explore_flag,
            )
            debug_info.words_analyzed.append(word_debug)

        # Correction candidates from softmax top-k
        seen: set[str] = {word.lower()}
        softmax_cands: list[str] = []
        heuristic_cands: list[str] = []

        # Softmax-based corrections (only when we have suspicious tokens)
        if suspicious:
            for rank in range(3):
                c = _build_correction(word, ws, we, word_tokens, suspicious, rank=rank)
                cl = c.lower()
                if c and cl not in seen and cl != word.lower():
                    softmax_cands.append(c)
                    seen.add(cl)

        # Heuristic corrections from the OCR confusion map.
        for c in _heuristic_candidates(word):
            cl = c.lower()
            if cl not in seen:
                heuristic_cands.append(c)
                seen.add(cl)

        cands = softmax_cands + heuristic_cands

        if word_debug is not None:
            word_debug.softmax_candidates = list(softmax_cands)
            word_debug.heuristic_candidates = list(heuristic_cands)
            word_debug.candidates_generated = list(cands)
            word_debug.candidates_pre_filter = list(cands)

        if not cands:
            if word_debug is not None:
                word_debug.outcome = "no_candidates"
                word_debug.outcome_reason = "No correction candidates could be generated for this word"
            continue

        # Similarity filter: OCR corrections must resemble the original.
        # "br0wn"→"brown" (0.8) passes; "material"→"coffee" (0.14) is filtered.
        cands = [
            c for c in cands
            if SequenceMatcher(None, word.lower(), c.lower()).ratio() > SIMILARITY_FLOOR
        ]
        # Shape filter — different rules for structural vs alpha-only words:
        #   * Structural (digit-in-alpha, rn-doubling, etc.): an OCR error
        #     shrinks "cornrnitrnent" (13) → "commitment" (10). Length and
        #     edit distance can be large, so we only keep the ratio filter
        #     above and add no further shape constraint here.
        #   * Alpha-only (no structural marker): real OCR errors in pure-alpha
        #     words overwhelmingly preserve length (1-char swap like teh↔the,
        #     glyph flips like hlelo↔hello). Require same length AND edit
        #     distance ≤ 2. This kills common-word paraphrases like
        #     "for"→"from", "washed"→"was", "community"→"city".
        if not structural:
            # Allow small length shifts (±2) so OCR-specific transforms
            # like d→cl (endose→enclose, disdose→disclose) survive when
            # the LM flags the word but no structural pattern matched.
            # Edit distance ≤ 2 still blocks wild paraphrases.
            cands = [
                c for c in cands
                if abs(len(c) - len(word)) <= 2 and _edit_distance(word, c) <= 2
            ]

        if word_debug is not None:
            word_debug.candidates_after_filter = list(cands)

        if not cands:
            log.info("  %s → no similar corrections, skipping", word)
            if word_debug is not None:
                word_debug.outcome = "filtered_no_similar"
                word_debug.outcome_reason = "All candidates filtered out by similarity/shape constraints"
            continue

        # Score [original, *corrections] by full-text log-prob
        all_cands = [word] + cands
        scores, raw_lps = _score_candidates(text, ws, we, all_cands)

        # Compute the log-prob improvement from the best correction
        improvement = max(raw_lps[1:]) - raw_lps[0] if len(raw_lps) > 1 else 0.0

        log.info(
            "  %s → candidates: %s  scores: %s  improvement: %.1f nats",
            word, all_cands, scores, improvement,
        )

        if word_debug is not None:
            word_debug.scores = dict(zip(all_cands, scores))
            word_debug.raw_log_probs = dict(zip(all_cands, raw_lps))
            word_debug.improvement = improvement

        # False-positive filter:
        #   1. Original must lose (correction scores higher)
        #   2. The log-prob improvement must be substantial (MIN_LP_GAIN nats).
        #      Real OCR fixes produce huge gains (10+); stylistic paraphrases
        #      produce small gains (1-3) and we want those filtered.
        #   3. Structural matches bypass the LP-gain floor — we already have
        #      strong prior evidence (digit-in-alpha, rn-doubling, etc.).
        best_corr = max(scores[1:], default=0)
        if scores and scores[0] >= best_corr:
            log.info("  → false positive (original wins)")
            if word_debug is not None:
                word_debug.outcome = "fp_original_wins"
                word_debug.outcome_reason = f"Original word scored {scores[0]:.3f} >= best correction {best_corr:.3f}"
            continue
        if not structural:
            # When the only signal is softmax probability and the surface form
            # is a plausible English word, require a much larger gain to flag.
            # The stronger base model (Qwen3) produces 6-10 nat gains on
            # natural paraphrase swaps, so we keep the bar high.
            gain_threshold = MIN_LP_GAIN
            if _looks_like_common_word(word):
                gain_threshold = max(gain_threshold, 10.0)
            if improvement < gain_threshold:
                log.info(
                    "  → false positive (improvement %.1f < %.1f)",
                    improvement, gain_threshold,
                )
                if word_debug is not None:
                    word_debug.outcome = f"fp_low_gain ({improvement:.1f} < {gain_threshold:.1f})"
                    word_debug.outcome_reason = f"Log-prob improvement {improvement:.1f} nats below threshold {gain_threshold:.1f}"
                continue

        # Build suggestions sorted by score. Always preserve the top-2
        # candidates regardless of score so that a heavily-diluted top
        # correction (e.g. "rebel" diluted across many sibling candidates
        # for "rebe1") still surfaces. Below top-2, drop very low scores.
        ranked = sorted(
            zip(cands, scores[1:]), key=lambda cs: cs[1], reverse=True,
        )
        suggestions = [
            Suggestion(text=c, score=s)
            for i, (c, s) in enumerate(ranked)
            if i < 2 or s >= 0.01
        ]
        if suggestions:
            spans.append(Span(
                start=ws, end=we, text=word,
                kind="probable_ocr_error",
                suggestions=suggestions,
            ))
            if word_debug is not None:
                best_suggestion = suggestions[0]
                word_debug.outcome = "flagged"
                word_debug.outcome_reason = f"OCR error detected, best suggestion '{best_suggestion.text}' with score {best_suggestion.score:.3f}"

    if not spans:
        return CheckResponse(result="ok", score=round(0.85, 3), spans=[], debug=debug_info)

    best_suggestion_score = max(
        s.score for span in spans for s in span.suggestions
    ) if spans else 0.5
    conf = 0.80 + 0.19 * min(best_suggestion_score, 1.0)
    return CheckResponse(
        result="issue_detected", score=round(conf, 3), spans=spans, debug=debug_info,
    )


# ── /v1/text/check-continuation ───────────────────────────────────────

def _continuation_check(first: str, second: str, debug: bool = False) -> ContinuationResponse:
    """
    Combined score:
      pmi_score = sigmoid((PMI − 0.5) * 3)      — does first help predict second?
      abs_score = sigmoid((cond_avg + 5) * 1.5)  — is second likely at all given first?
      score     = pmi_score * abs_score           — both must be high

    The PMI bias (0.5) ensures weakly-positive PMI from unrelated but fluent
    text doesn't push score above 0.5.  Absolute score prevents gibberish.
    """
    debug_info = ContinuationDebug() if (debug or DEBUG_MODE) else None

    # Tokenize first and second separately for debug
    if debug_info is not None:
        first_enc = lm.tokenizer(first, add_special_tokens=False)
        second_enc = lm.tokenizer(second, add_special_tokens=False)
        debug_info.first_tokens = [lm.tokenizer.decode([tid]) for tid in first_enc["input_ids"]]
        debug_info.second_tokens = [lm.tokenizer.decode([tid]) for tid in second_enc["input_ids"]]

    # Conditional: P(second | first)
    # Use offset_mapping to locate the boundary precisely. BPE tokenizers
    # merge the space into the first token of `second` (" dog"), so naively
    # tokenising `first + " "` and using its length as the split would skip
    # that high-signal first token of the continuation. Instead, the split is
    # the first token in the joint whose char_start lies at or past the
    # boundary between `first` and `second`.
    joint     = first + " " + second
    boundary  = len(first) + 1  # char index of second's first character
    joint_enc = lm.tokenizer(
        joint, return_tensors="pt",
        return_offsets_mapping=True, add_special_tokens=False,
    )
    joint_ids = joint_enc["input_ids"].to(DEVICE)
    j_offsets = joint_enc["offset_mapping"][0]

    if debug_info is not None:
        debug_info.joint_tokens = [lm.tokenizer.decode([tid.item()]) for tid in joint_ids[0]]

    split = joint_ids.shape[1]
    for i in range(joint_ids.shape[1]):
        cs = int(j_offsets[i][0].item())
        ce = int(j_offsets[i][1].item())
        # First token whose content actually reaches into `second`.
        if ce > boundary - 1 and cs >= boundary - 1:
            split = i
            break

    if debug_info is not None:
        debug_info.boundary_token_idx = split

    with torch.no_grad():
        j_logits = lm.model(joint_ids).logits[0]
    j_lps = F.log_softmax(j_logits, dim=-1)

    cond_probs: list[float] = []
    cond_sum, cond_n = 0.0, 0
    for i in range(split, joint_ids.shape[1]):
        if i > 0:
            lp = j_lps[i - 1, joint_ids[0, i].item()].item()
            cond_sum += lp
            cond_n   += 1
            cond_probs.append(lp)
    if cond_n == 0:
        return ContinuationResponse(result="unlikely_continuation", score=0.5, debug=debug_info)
    cond_avg = cond_sum / cond_n

    if debug_info is not None:
        debug_info.conditional_token_probs = cond_probs
        debug_info.conditional_avg_log_prob = cond_avg

    # Unconditional: P(second)
    sec_enc = lm.tokenizer(second, return_tensors="pt", add_special_tokens=False)
    sec_ids = sec_enc["input_ids"].to(DEVICE)
    with torch.no_grad():
        s_logits = lm.model(sec_ids).logits[0]
    s_lps = F.log_softmax(s_logits, dim=-1)

    uncond_probs: list[float] = []
    uncond_sum, uncond_n = 0.0, 0
    for i in range(1, sec_ids.shape[1]):
        lp = s_lps[i - 1, sec_ids[0, i].item()].item()
        uncond_sum += lp
        uncond_n   += 1
        uncond_probs.append(lp)
    uncond_avg = uncond_sum / max(uncond_n, 1)

    if debug_info is not None:
        debug_info.unconditional_token_probs = uncond_probs
        debug_info.unconditional_avg_log_prob = uncond_avg

    # PMI score: does context help?
    # Bias of 0.2: even weakly-positive PMI suggests genuine continuation,
    # since the abs_score below already filters gibberish. Earlier value of
    # 0.5 was too punishing — well-formed mid-sentence and mid-word splits
    # often have small but real PMI gains and should clear the 0.5 mark.
    pmi       = cond_avg - uncond_avg
    pmi_score = 1.0 / (1.0 + math.exp(-(pmi - 0.2) * 3.0))

    # Absolute score: is the conditional probability decent?
    # Good continuations: cond_avg ~ -1 to -4
    # Technical/unusual:   cond_avg ~ -4 to -6
    # Gibberish:           cond_avg ~ -7 to -10+
    # Midpoint at -5.5 (was -5.0) gives slightly more headroom for technical
    # and proper-noun-heavy continuations whose conditional sits around -5.
    abs_score = 1.0 / (1.0 + math.exp(-(cond_avg + 5.5) * 1.5))

    score = pmi_score * abs_score

    log.info(
        "Continuation: cond=%.3f uncond=%.3f pmi=%.3f "
        "pmi_score=%.3f abs_score=%.3f → %.3f",
        cond_avg, uncond_avg, pmi, pmi_score, abs_score, score,
    )

    result = "likely_continuation" if score >= 0.5 else "unlikely_continuation"

    if debug_info is not None:
        debug_info.pmi = pmi
        debug_info.pmi_score = pmi_score
        debug_info.abs_score = abs_score
        debug_info.final_score = score
        debug_info.verdict = result

    return ContinuationResponse(result=result, score=round(score, 3), debug=debug_info)


# ── FastAPI ────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    await lm.load()
    yield
    lm.unload()

app = FastAPI(
    title="TextSureOCR",
    description="Text forensics for OCR pipelines — token-level scoring",
    version="0.3.0",
    lifespan=lifespan,
)

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if AUTH_TOKEN and request.url.path.startswith("/v1/"):
        auth = request.headers.get("Authorization", "")
        if auth != f"Bearer {AUTH_TOKEN}":
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    return await call_next(request)

@app.get("/health")
async def health():
    body = {
        "status": "ok",
        "model": MODEL_ID,
        "device": DEVICE,
        "model_loaded": lm.model is not None,
    }
    if VAST_INSTANCE_ID:
        body["vast_instance_id"] = VAST_INSTANCE_ID
    return body

@app.post("/v1/ocr/check", response_model=CheckResponse)
async def ocr_check(req: CheckRequest):
    async with _gpu_sem:
        return await asyncio.to_thread(_ocr_check, req.text, req.debug)

@app.post("/v1/text/check-continuation", response_model=ContinuationResponse)
async def check_continuation(req: ContinuationRequest):
    async with _gpu_sem:
        return await asyncio.to_thread(_continuation_check, req.first, req.second, req.debug)


if __name__ == "__main__":
    port = int(os.getenv("TEXTSURE_PORT", "5002"))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
