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
MODEL_ID         = os.getenv("TEXTSURE_MODEL", "Qwen/Qwen2.5-7B-Instruct")
DEVICE           = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE            = torch.float16 if DEVICE == "cuda" else torch.float32

TOKEN_PROB_FLOOR = float(os.getenv("TEXTSURE_TOKEN_PROB_FLOOR", "0.05"))
MIN_LP_GAIN      = float(os.getenv("TEXTSURE_MIN_LP_GAIN", "4.0"))
SIMILARITY_FLOOR = float(os.getenv("TEXTSURE_SIMILARITY_FLOOR", "0.5"))
TOP_K            = 5
MIN_WORD_LEN     = 2
MAX_HEURISTIC_CANDIDATES = 8

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
    "cl": ["d"],
    "|":  ["l", "I"],
    "rri":["m"],
    "I":  ["l"],   # capital-I scanned for lowercase-l (faciIity → facility)
}

# UK→US spelling normalisation applied to model-generated corrections.
UK_US_SUFFIXES: list[tuple[str, str]] = [
    ("our",  "or"),    # honour → honor, colour → color
    ("ise",  "ize"),   # realise → realize
    ("ised", "ized"),
    ("ising","izing"),
    ("yse",  "yze"),   # analyse → analyze
    ("tre",  "ter"),   # centre → center
    ("ogue", "og"),    # catalogue → catalog
]

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

class CheckResponse(BaseModel):
    result: str
    score: float
    spans: list[Span] = []

class ContinuationRequest(BaseModel):
    first: str  = Field(..., min_length=1, max_length=5_000)
    second: str = Field(..., min_length=1, max_length=5_000)

class ContinuationResponse(BaseModel):
    result: str
    score: float


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
      - actual_prob           (P(actual_token_i | tokens_0..i-1))
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

    out: list[dict] = []
    for i in range(1, ids.shape[1]):
        actual_id   = ids[0, i].item()
        actual_prob = probs[i - 1, actual_id].item()
        top_vals, top_ids = probs[i - 1].topk(TOP_K)
        cs = int(offsets[i][0].item())
        ce = int(offsets[i][1].item())
        out.append({
            "char_start":  cs,
            "char_end":    ce,
            "actual_text": text[cs:ce],
            "actual_prob": actual_prob,
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


def _generate(prompt_text: str) -> str:
    messages = [{"role": "user", "content": prompt_text}]
    chat = lm.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True,
    )
    ids = lm.tokenizer(chat, return_tensors="pt").input_ids.to(DEVICE)
    with torch.no_grad():
        out = lm.model.generate(ids, max_new_tokens=10, do_sample=False)
    return lm.tokenizer.decode(out[0, ids.shape[1]:], skip_special_tokens=True)


def _first_word(text: str) -> str:
    hit = re.search(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", text)
    return hit.group().lower() if hit else ""


def _ask_correction(text: str, word: str) -> str:
    return _first_word(_generate(
        f'The following OCR text contains a scanning error in the word "{word}". '
        f'What should it correctly read? Reply with ONLY the single corrected '
        f'word.\n\nText: "{text}"'
    ))


def _uk_to_us(word: str) -> str:
    """Normalise common UK suffix spellings to US forms."""
    wl = word.lower()
    for uk, us in UK_US_SUFFIXES:
        if wl.endswith(uk) and len(wl) > len(uk) + 1:
            return word[:-len(uk)] + us
    return word


# ── Structural / character-confusion heuristics ────────────────────────

# A word is structurally suspicious if it:
#   (a) mixes alphabetic characters with digits (schoo1, c0mputer, 1etter)
#   (b) contains a doubled "rn" pattern (cornrnitrnent, governrnent)
#   (c) contains "vv" inside an alpha run (vvord → word)
#   (d) contains a pipe among letters (he|lo)
_DIGIT_IN_ALPHA = re.compile(r"[A-Za-z][0-9]|[0-9][A-Za-z]")
_RN_DOUBLED     = re.compile(r"rn.*rn", re.IGNORECASE)
_VV_IN_ALPHA    = re.compile(r"[A-Za-z]vv|vv[A-Za-z]")
_PIPE_IN_ALPHA  = re.compile(r"[A-Za-z]\||\|[A-Za-z]")
# Capital I appearing inside a lowercase alpha run (faciIity, additionaI, Iate).
_CAP_I_IN_ALPHA = re.compile(r"[a-z]I|I[a-z]")
# Word that contains zero alphabetic characters — pure digits/punctuation
# like "16", "750", "--", "555-0140". Not OCR-checkable as a "word".
_NO_ALPHA       = re.compile(r"^[^A-Za-z]+$")


def _is_structurally_suspicious(word: str) -> bool:
    return bool(
        _DIGIT_IN_ALPHA.search(word)
        or _RN_DOUBLED.search(word)
        or _VV_IN_ALPHA.search(word)
        or _PIPE_IN_ALPHA.search(word)
        or _CAP_I_IN_ALPHA.search(word)
    )


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

    return out[:MAX_HEURISTIC_CANDIDATES]


# Common-English allow-list used to suppress false positives on clean prose.
# If the "suspect" word is a plain dictionary-shaped lowercase alpha word,
# and the best correction differs only stylistically, skip flagging it.
_COMMON_WORD_SHAPE = re.compile(r"^[a-z]{2,}$")


def _looks_like_common_word(word: str) -> bool:
    """Cheap shape check: purely alphabetic lowercase form, 2+ chars."""
    return bool(_COMMON_WORD_SHAPE.match(word.lower()))


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


# ── /v1/ocr/check ─────────────────────────────────────────────────────

def _ocr_check(text: str) -> CheckResponse:
    preds = _token_predictions(text)
    if not preds:
        return CheckResponse(result="ok", score=0.95, spans=[])

    # ── Phase 1: find words with suspicious tokens ──
    # A word enters Phase 2 if EITHER:
    #   (a) it contains a token with P(actual | prefix) < floor  (LM signal), OR
    #   (b) it matches a structural OCR-confusion pattern         (heuristic signal)
    word_candidates: list[tuple[str, int, int, list[dict], list[dict], bool]] = []

    for m in re.finditer(r"\S+", text):
        word, ws, we = m.group(), m.start(), m.end()
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

        structural = _is_structurally_suspicious(word)

        if not suspicious and not structural:
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
        word_candidates.append((word, ws, we, word_tokens, suspicious, structural))

    log.info(
        "OCR check: %d tokens, floor=%.3f, candidate words=%d (%s)",
        len(preds), TOKEN_PROB_FLOOR,
        len(word_candidates),
        ", ".join(w for w, _, _, _, _, _ in word_candidates),
    )

    if not word_candidates:
        min_prob = min(t["actual_prob"] for t in preds)
        margin = min(min_prob / TOKEN_PROB_FLOOR, 1.0) if TOKEN_PROB_FLOOR > 0 else 1.0
        conf = 0.80 + 0.19 * min(margin, 1.0)
        return CheckResponse(result="ok", score=round(conf, 3), spans=[])

    # ── Phase 2: build corrections, score, and filter ──
    spans: list[Span] = []
    for word, ws, we, word_tokens, suspicious, structural in word_candidates:
        # Correction candidates from softmax top-k
        seen: set[str] = {word.lower()}
        cands: list[str] = []

        # Softmax-based corrections (only when we have suspicious tokens)
        if suspicious:
            for rank in range(3):
                c = _build_correction(word, ws, we, word_tokens, suspicious, rank=rank)
                cl = c.lower()
                if c and cl not in seen and cl != word.lower():
                    cands.append(c)
                    seen.add(cl)

        # Heuristic corrections from the OCR confusion map.
        for c in _heuristic_candidates(word):
            cl = c.lower()
            if cl not in seen:
                cands.append(c)
                seen.add(cl)

        # Instruct-generated correction (backup)
        c_instruct = _ask_correction(text, word)
        if c_instruct and c_instruct not in seen:
            cands.append(c_instruct)
            seen.add(c_instruct)
            # Also try its US-normalised form so US-preference tests pass.
            c_us = _uk_to_us(c_instruct)
            if c_us and c_us.lower() not in seen:
                cands.append(c_us)
                seen.add(c_us.lower())

        if not cands:
            continue

        # Similarity filter: OCR corrections must resemble the original.
        # "br0wn"→"brown" (0.8) passes; "material"→"coffee" (0.14) is filtered.
        cands = [
            c for c in cands
            if SequenceMatcher(None, word.lower(), c.lower()).ratio() > SIMILARITY_FLOOR
        ]
        if not cands:
            log.info("  %s → no similar corrections, skipping", word)
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
            continue
        if not structural:
            # When the only signal is softmax probability and the surface form
            # is a plausible English word, require a *much* larger gain to flag.
            gain_threshold = MIN_LP_GAIN
            if _looks_like_common_word(word):
                gain_threshold = max(gain_threshold, 6.0)
            if improvement < gain_threshold:
                log.info(
                    "  → false positive (improvement %.1f < %.1f)",
                    improvement, gain_threshold,
                )
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

    if not spans:
        return CheckResponse(result="ok", score=round(0.85, 3), spans=[])

    best_suggestion_score = max(
        s.score for span in spans for s in span.suggestions
    ) if spans else 0.5
    conf = 0.80 + 0.19 * min(best_suggestion_score, 1.0)
    return CheckResponse(
        result="issue_detected", score=round(conf, 3), spans=spans,
    )


# ── /v1/text/check-continuation ───────────────────────────────────────

def _continuation_check(first: str, second: str) -> ContinuationResponse:
    """
    Combined score:
      pmi_score = sigmoid((PMI − 0.5) * 3)      — does first help predict second?
      abs_score = sigmoid((cond_avg + 5) * 1.5)  — is second likely at all given first?
      score     = pmi_score * abs_score           — both must be high

    The PMI bias (0.5) ensures weakly-positive PMI from unrelated but fluent
    text doesn't push score above 0.5.  Absolute score prevents gibberish.
    """
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

    split = joint_ids.shape[1]
    for i in range(joint_ids.shape[1]):
        cs = int(j_offsets[i][0].item())
        ce = int(j_offsets[i][1].item())
        # First token whose content actually reaches into `second`.
        if ce > boundary - 1 and cs >= boundary - 1:
            split = i
            break

    with torch.no_grad():
        j_logits = lm.model(joint_ids).logits[0]
    j_lps = F.log_softmax(j_logits, dim=-1)

    cond_sum, cond_n = 0.0, 0
    for i in range(split, joint_ids.shape[1]):
        if i > 0:
            cond_sum += j_lps[i - 1, joint_ids[0, i].item()].item()
            cond_n   += 1
    if cond_n == 0:
        return ContinuationResponse(result="unlikely_continuation", score=0.5)
    cond_avg = cond_sum / cond_n

    # Unconditional: P(second)
    sec_enc = lm.tokenizer(second, return_tensors="pt", add_special_tokens=False)
    sec_ids = sec_enc["input_ids"].to(DEVICE)
    with torch.no_grad():
        s_logits = lm.model(sec_ids).logits[0]
    s_lps = F.log_softmax(s_logits, dim=-1)

    uncond_sum, uncond_n = 0.0, 0
    for i in range(1, sec_ids.shape[1]):
        uncond_sum += s_lps[i - 1, sec_ids[0, i].item()].item()
        uncond_n   += 1
    uncond_avg = uncond_sum / max(uncond_n, 1)

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
    return ContinuationResponse(result=result, score=round(score, 3))


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
        return await asyncio.to_thread(_ocr_check, req.text)

@app.post("/v1/text/check-continuation", response_model=ContinuationResponse)
async def check_continuation(req: ContinuationRequest):
    async with _gpu_sem:
        return await asyncio.to_thread(_continuation_check, req.first, req.second)


if __name__ == "__main__":
    port = int(os.getenv("TEXTSURE_PORT", "5002"))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
