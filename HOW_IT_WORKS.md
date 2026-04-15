# How TextSureOCR Works

TextSureOCR is a text forensics API that uses a base language model (Qwen3-8B-Base) as a statistical judge. Instead of pattern-matching against a dictionary, it asks: "how surprised is the model by this word in context?" and "does knowing fragment A help predict fragment B?" All decisions come from token-level log-probabilities computed in forward passes — no fine-tuning, no external lookup tables, no instruction tuning (which would distort the natural next-token distribution).

## Model

Qwen3-8B-Base loaded in BF16 on a single GPU (~16GB VRAM). Inference is pure logit inspection on a single forward pass — no sampling, no generation, no chat templates. The model is used in one mode: read the softmax distribution at each position and reason over it.

## OCR Error Detection (`POST /v1/ocr/check`)

The pipeline has two phases: **candidate identification** and **candidate verification**.

### Phase 1: Find candidate errors

Two independent detectors run in parallel over the input text:

**1a. Heuristic detector — digit/letter mixtures**

Catches the most common OCR failure mode: digits substituted for visually similar letters (0→o, 1→l, 3→e, 5→s, 7→t, 8→b). A word is flagged if it contains both letters and digits, with letters being the majority. This catches `br0wn`, `p0lice`, `H3llo`, `1etter`, `5chool`, etc. Pure numbers like `95` or `3` are not flagged because they have no letters.

**1b. Statistical detector — surprisal outliers**

A single forward pass through the model produces per-token log-probabilities. These are aggregated to word-level *surprisal* (average negative log-prob of the tokens comprising each word). A word is flagged if its surprisal exceeds an adaptive threshold:

```
threshold = max(mean + 1.5 * stddev, 8.0)
```

The threshold adapts to the text — technical or unusual writing raises the baseline, so only words that are surprising *relative to their context* get flagged. The absolute floor of 8.0 nats prevents flagging in uniformly high-surprisal text. This detector catches character-level confusions that don't involve digits, like `governrnent` (rn→m) and `teh` (transposition), because the model finds these sequences surprising.

### Phase 2: Verify and score corrections

For each candidate word, the system generates correction suggestions from two sources:

- **Softmax top-k correction**: at each suspicious token position, the forward-pass softmax distribution already has the model's preferred alternatives. Take the top-k token IDs, decode them, and splice them in at the suspicious position's character span (`_build_correction`). No generation, no prompting — just reading the distribution the model already produced.
- **Systematic correction** (pattern candidates): mechanically apply the OCR-confusion map (`rn` → `m`, `vv` → `w`, digit↔letter, etc.) to produce alternative spellings

Each unique correction is then scored against the original word using **full-text log-probability comparison**. For each candidate (original + corrections), the system:

1. Substitutes the candidate into the original text at the flagged position
2. Computes the total log-probability of the entire modified text (one forward pass each)
3. Applies softmax normalization across all candidates

This produces a probability distribution: e.g., `["br0wn": 0.00, "brown": 1.00]` or `["quick": 0.96, "swift": 0.04]`.

Using full-text comparison (rather than isolated token scoring) avoids a subtle bug where BPE tokenization boundaries shift when you replace a word, making isolated token-level scores incomparable.

### False-positive filtering

The filter strategy depends on how the candidate was identified:

- **Surprisal candidates**: strict — the original word must *lose* to at least one correction. If `"quick"` scores 0.96 and `"swift"` scores 0.04, the original wins and it's dropped as a false positive. This is the right behavior: the model is most surprised by `"quick"` in this sentence, but it's still the best word for the position.

- **Pattern candidates** (digit/letter mixtures): relaxed — any correction with >5% probability is enough to keep the candidate. This handles uniformly-corrupted text like `"H3llo w0rld, th1s is a t3st"`, where the model adapts to the corrupted style and may rate the corrupted form higher than the correction. The digit/letter pattern is strong enough prior evidence that we don't require the correction to win outright.

Suggestions with score < 1% are filtered out to avoid noise.

### Confidence score

When errors are found: `confidence = 0.80 + 0.19 * best_suggestion_score`. The best correction's score drives confidence — if the model is very sure about the fix (score near 1.0), confidence approaches 0.99.

When no errors are found: `confidence = 0.80 + 0.19 * margin`, where margin measures how far the worst word's surprisal is from the threshold. Text where every word is comfortably below threshold scores higher.

## Text Continuation Check (`POST /v1/text/check-continuation`)

Evaluates whether `second` is a natural continuation of `first`. The core idea: if knowing the first fragment helps predict the second, they probably belong together.

### Scoring

Two forward passes compute:

1. **Conditional probability**: P(second | first) — tokenize `first + " " + second` as one sequence, extract log-probs for only the second-fragment tokens
2. **Unconditional probability**: P(second) — tokenize `second` alone, extract log-probs

**Pointwise Mutual Information (PMI):**
```
PMI = avg_log_prob(second | first) - avg_log_prob(second)
```

If PMI is positive, the first fragment makes the second *more predictable* — evidence of continuity. If PMI is near zero or negative, the first fragment doesn't help (or hurts) prediction.

### Combined scoring

PMI alone has a failure mode: gibberish after gibberish can have weakly positive PMI (both are bad, but conditional is slightly less bad). To prevent this, the final score combines PMI with absolute conditional quality:

```
pmi_score = sigmoid((PMI - 0.5) * 3.0)
abs_score = sigmoid((cond_avg + 5.0) * 1.5)
score     = pmi_score * abs_score
```

- **pmi_score**: the sigmoid with a bias of 0.5 means weakly-positive PMI (common when two unrelated but grammatically fluent fragments are concatenated) maps to below 0.5. Only genuinely helpful context pushes the score high.
- **abs_score**: midpoint at `cond_avg = -5.0` nats. Good continuations sit around -1 to -4 (high score), technical text around -4 to -6 (moderate), gibberish below -7 (near zero). This prevents garbage from scoring high regardless of PMI.
- **Product**: both components must be high. A fluent continuation of relevant context scores near 1.0. Gibberish scores near 0 (abs_score kills it). Unrelated but fluent text scores below 0.5 (pmi_score kills it).

The threshold is 0.5: above → `likely_continuation`, below → `unlikely_continuation`.

### What it catches

| Scenario | PMI | abs_score | Final | Verdict |
|---|---|---|---|---|
| Natural sentence split ("fox jumps" → "over the lazy dog") | high (+4.5) | high (0.999) | 0.999 | likely |
| Paragraph continuation (related sentences) | moderate (+1.5) | high (0.995) | 0.946 | likely |
| Mid-word break ("hypothet" → "ical scenario...") | high (+2.8) | high (0.973) | 0.973 | likely |
| Topic whiplash (photosynthesis → stock market) | weak (+0.3) | moderate (0.77) | 0.287 | unlikely |
| Cross-column jump (revenue → "In other news") | near-zero (+0.1) | low (0.20) | 0.050 | unlikely |
| Language switch (English → French) | negative (-0.9) | moderate (0.71) | 0.012 | unlikely |
| Random gibberish | weak (+0.9) | very low (0.004) | 0.003 | unlikely |

## Runtime

- FastAPI + uvicorn, single worker
- `asyncio.Semaphore(1)` serializes GPU access — one inference at a time, but the event loop stays responsive for health checks
- `asyncio.to_thread()` moves blocking GPU work off the event loop
- Model loaded once at startup via FastAPI lifespan handler

## Performance (RTX 3090)

| Operation | Latency |
|---|---|
| Model load (cached weights) | ~4s |
| OCR check, clean text | ~40ms |
| OCR check, with errors | ~200-700ms (scales with number of corrections to generate) |
| Continuation check | ~60ms |
| GPU memory | ~14GB |

## Known Limitations

- **Character-level confusions** (rn→m, cl→d) rely on surprisal detection. If the model doesn't find the corrupted form surprising enough (surprisal below the adaptive threshold), the error is missed. The heuristic detector only covers digit/letter mixtures.
- **Uniformly corrupted text** makes the model adapt to the corrupted style. Correction scores may be lower than expected, though the corrections themselves are still correct.
- **Single-request throughput** — the semaphore serializes all GPU work. For production batching, a vLLM backend would allow concurrent inference.
