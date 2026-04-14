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
MODEL_ID         = os.getenv("TEXTSURE_MODEL", "Qwen/Qwen2.5-7B-Instruct")
DEVICE           = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE            = torch.float16 if DEVICE == "cuda" else torch.float32

TOKEN_PROB_FLOOR = float(os.getenv("TEXTSURE_TOKEN_PROB_FLOOR", "0.05"))
MIN_LP_GAIN      = float(os.getenv("TEXTSURE_MIN_LP_GAIN", "1.0"))
SIMILARITY_FLOOR = float(os.getenv("TEXTSURE_SIMILARITY_FLOOR", "0.5"))
TOP_K            = 5
MIN_WORD_LEN     = 2

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
    # A token is suspicious when P(actual | prefix) < floor — the model
    # thinks there's < 1% chance this token belongs here.
    word_candidates: list[tuple[str, int, int, list[dict], list[dict]]] = []

    for m in re.finditer(r"\S+", text):
        word, ws, we = m.group(), m.start(), m.end()
        if len(word) < MIN_WORD_LEN:
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
        if not suspicious:
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
        word_candidates.append((word, ws, we, word_tokens, suspicious))

    log.info(
        "OCR check: %d tokens, floor=%.3f, candidate words=%d (%s)",
        len(preds), TOKEN_PROB_FLOOR,
        len(word_candidates),
        ", ".join(w for w, _, _, _, _ in word_candidates),
    )

    if not word_candidates:
        min_prob = min(t["actual_prob"] for t in preds)
        margin = min(min_prob / TOKEN_PROB_FLOOR, 1.0) if TOKEN_PROB_FLOOR > 0 else 1.0
        conf = 0.80 + 0.19 * min(margin, 1.0)
        return CheckResponse(result="ok", score=round(conf, 3), spans=[])

    # ── Phase 2: build corrections, score, and filter ──
    spans: list[Span] = []
    for word, ws, we, word_tokens, suspicious in word_candidates:
        # Correction candidates from softmax top-k
        seen: set[str] = {word.lower()}
        cands: list[str] = []

        # Try top-1, top-2, top-3 substitutions
        for rank in range(3):
            c = _build_correction(word, ws, we, word_tokens, suspicious, rank=rank)
            cl = c.lower()
            if c and cl not in seen and cl != word.lower():
                cands.append(c)
                seen.add(cl)

        # Instruct-generated correction (backup)
        c_instruct = _ask_correction(text, word)
        if c_instruct and c_instruct not in seen:
            cands.append(c_instruct)
            seen.add(c_instruct)

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
        #   2. The log-prob improvement must be substantial (MIN_LP_GAIN nats)
        #      Real OCR fixes produce huge gains (10+), stylistic preferences
        #      produce small gains (1-3).
        best_corr = max(scores[1:], default=0)
        if scores and scores[0] >= best_corr:
            log.info("  → false positive (original wins)")
            continue
        if improvement < MIN_LP_GAIN:
            log.info("  → false positive (improvement %.1f < %.1f)", improvement, MIN_LP_GAIN)
            continue

        suggestions = sorted(
            [Suggestion(text=c, score=s)
             for c, s in zip(cands, scores[1:]) if s >= 0.01],
            key=lambda x: x.score, reverse=True,
        )
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
    joint     = first + " " + second
    joint_enc = lm.tokenizer(joint, return_tensors="pt", add_special_tokens=False)
    joint_ids = joint_enc["input_ids"].to(DEVICE)

    first_sp = lm.tokenizer(first + " ", return_tensors="pt", add_special_tokens=False)
    split    = first_sp["input_ids"].shape[1]

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
    # Bias of 0.5 means weakly-positive PMI (unrelated but both fluent) scores < 0.5
    pmi       = cond_avg - uncond_avg
    pmi_score = 1.0 / (1.0 + math.exp(-(pmi - 0.5) * 3.0))

    # Absolute score: is the conditional probability decent?
    # Good continuations: cond_avg ~ -1 to -4
    # Technical/unusual:   cond_avg ~ -4 to -6
    # Gibberish:           cond_avg ~ -7 to -10+
    # Midpoint at -5 so technical text isn't over-penalised
    abs_score = 1.0 / (1.0 + math.exp(-(cond_avg + 5.0) * 1.5))

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
    return {
        "status": "ok",
        "model": MODEL_ID,
        "device": DEVICE,
        "model_loaded": lm.model is not None,
    }

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
