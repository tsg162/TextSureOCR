# TextSureOCR — BERT + T5 Parallel Experiment Spec

An **experimental track** running in parallel to the current Qwen3-8B
pipeline. Goal: discover whether smaller, purpose-trained models
(BERT for sentence-continuity, T5 for OCR detect+correct) can match or
beat the Qwen-based `app.py` on quality — and, if it's close, let the
cheaper option win.

This is **not** a rewrite plan. Current `app.py` stays in production
untouched throughout. Experimental models are built and measured
side-by-side; promotion decisions come after evaluation, not before.

---

## 1. Goals & decision rule

### 1.1 What we're testing

Two independent experiments, each a drop-in candidate for one existing
endpoint:

| Endpoint | Current (prod) | Experimental candidate |
|---|---|---|
| `/v1/text/check-continuation` | Qwen3-8B PMI + absolute log-prob (`app.py:16-18`) | Fine-tuned BERT sentence-pair classifier |
| `/v1/ocr/check` | Qwen3-8B softmax + regex heuristics + LP re-rank | Fine-tuned T5 (detect + correct in one pass), optionally with a BERT assist |

Each experiment is evaluated independently. They can ship independently.

### 1.2 Decision rule (per endpoint)

1. **Quality first.** Experimental model must be at least **non-worse**
   than prod on the held-out validation set across agreed metrics (§6).
2. **Tie-breaker: cost.** If quality is within noise (see §6.4 for
   "within noise" definition), the cheaper-to-run model wins.
   In practice that means BERT / T5 beat Qwen at a tie, since both are
   dramatically smaller and cheaper to serve.
3. **Stay-in-place bias.** If the experimental model is *worse* on any
   critical metric (esp. clean-prose false-positive rate), prod stays.

No partial replacement: each endpoint either flips entirely to the
experimental model or stays on Qwen. We keep one code path per endpoint
in production.

---

## 2. Experiment A — BERT for `/v1/text/check-continuation`

### 2.1 Task

Given two text chunks (`first`, `second`), decide whether they are a
natural continuation of the same source document, or whether they come
from different provenance (e.g. concatenated from unrelated pages,
OCR-split across document boundaries, stitched incorrectly).

This is exactly the task BERT's next-sentence-prediction (NSP) objective
was designed for — a sentence-pair classifier is the canonical fit.

### 2.2 Model

- **Primary:** `deberta-v3-base` fine-tuned as a binary sentence-pair
  classifier with `[CLS] first [SEP] second [SEP]` input.
- **Alternative:** `roberta-base` if DeBERTa training is unstable on our
  data sizes.
- **Multilingual option:** `xlm-roberta-base` if the input distribution
  isn't English-only.

### 2.3 Output mapping

The current endpoint returns `{result, score}` where `score` blends PMI
and absolute conditional probability. BERT output maps cleanly:

- `score = P(continuation | first, second)` from the classifier head.
- `result` from a threshold (tune on validation; start at 0.5).

Schema (`ContinuationResponse` in `app.py:122`) unchanged.

### 2.4 Data

Training data, descending priority:

1. **Positives from in-house validated OCR docs** — consecutive
   sentence/paragraph pairs within a document.
2. **Hard negatives** — pairs from *different* documents, ideally
   same-topic and same-domain (so the model learns provenance, not
   topic). Mined by sampling pairs that share ≥ 50% vocabulary but are
   from different sources.
3. **Easy negatives** — random cross-document pairs (keep a minority;
   too many and the model learns topic, not continuity).
4. **Synthetic negatives** — split a real document mid-sentence, then
   replace the second half with a sentence from elsewhere. Limits
   trivial length/style cues.

Target ratio roughly 1 pos : 1 hard-neg : 0.3 easy-neg : 0.3 synth-neg.

Format (JSONL):

```json
{"first": "…", "second": "…", "label": 1, "source": "doc_4421", "provenance": "same_doc"}
{"first": "…", "second": "…", "label": 0, "source": "doc_mix_17a", "provenance": "hard_neg_same_topic"}
```

Target v1 scale: **≥ 50k pairs** (balanced).

### 2.5 Training

- Loss: binary cross-entropy.
- lr 2e-5, AdamW, warmup 6%, 3 epochs, early-stop on val AUC.
- batch 32, max_len 512 (split budget 256/256 between first and second).
- Truncate long inputs from the middle — keep context near the boundary
  where continuity signal lives.

### 2.6 Success criteria (vs Qwen prod)

On held-out in-house pairs:

- AUC ≥ Qwen prod's AUC.
- At the threshold matching Qwen's current production precision: recall
  must be within 2 points absolute.
- p95 latency ≤ 50ms (Qwen current ~200-500ms depending on chunk size).

If AUC matches and BERT is cheaper → promote BERT.
If AUC regresses → stay on Qwen.

---

## 3. Experiment B — T5 for `/v1/ocr/check`

### 3.1 Task

Given a text that may contain OCR errors, return:

- Whether the text has errors (`result`, `score`).
- Per-error spans with suggested corrections (`spans[]`).

T5's appeal: it can *both* detect and correct in a single pass. We frame
it as a tagged-rewrite task and derive spans from the diff between input
and output.

### 3.2 Core framing

**Input:**
```
fix ocr: The cornrnittee approved the fmal draft on 1anuary 5.
```

**Target (during training):**
```
The committee approved the final draft on January 5.
```

**Inference:** diff input vs output (character-level alignment) →
error spans + suggestions. A no-op output (input == output) means
"no errors detected."

This folds detection and correction into one model, one forward pass.
No separate detector needed — unless experiments show T5 alone has too
many false positives or negatives (§3.5).

### 3.3 Model

- **Primary:** `google/byt5-small` (300M, byte-level). Character-level
  tokens match character-level OCR errors; prior work (Maheshwari et al.
  2022, Rijhwani et al. 2020) shows ByT5 beats subword T5 on OCR
  post-correction.
- **Alternative:** `google/flan-t5-base` (250M). Instruction-tuned, may
  start stronger zero/few-shot but weaker on novel glyph confusions.
- **Bake-off:** train both on the pilot data; pick the winner on
  exact-match + CER + no-op rate.

### 3.4 Data

Validated (OCR → clean) sentence pairs from our corpus, plus:

1. **Public datasets** — ICDAR 2017/2019 Post-OCR Correction challenge,
   Impresso, Overproof.
2. **Synthetic augmentation** — apply the existing `CONFUSIONS` map
   (`app.py:57`) to clean text; also run Tesseract on rendered clean
   text to get realistic OCR noise. Cap at ≤ 30% of training mix.
3. **Negative examples (critical)** — clean sentences paired with
   themselves (input == target). These teach T5 to leave clean prose
   alone. Make up ≥ 30% of training pairs.

Format (JSONL):

```json
{"id": "doc_4421_p3_s17",
 "ocr": "The cornrnittee approved the fmal draft on 1anuary 5.",
 "clean": "The committee approved the final draft on January 5.",
 "source": "inhouse_validated"}
```

Target v1 scale: **≥ 100k pairs** training, **≥ 5k** held-out documents
for val and test each.

### 3.5 The BERT-assist question (open)

**Hypothesis to test, not commit to.** A T5-only approach may
hallucinate corrections on clean prose (false positives) or miss subtle
errors (false negatives). A BERT token-classifier could pre-filter:

- As a **pre-filter**: only call T5 on sentences BERT flags. Reduces
  FPs from T5 paraphrasing clean text; reduces inference cost.
- As a **post-filter**: only accept T5 edits when BERT confirms the
  flagged span looks error-like. Reduces FPs but adds latency.
- As a **feature**: concatenate BERT span-probability into T5's input
  (e.g. `fix ocr: The <p=0.9>cornrnittee</p> …`). Richer signal but
  complex to train.

**Experimental plan:** train T5 first. Measure its FPR on clean prose
and FNR on known errors. Then run a small ablation comparing:

- T5 alone
- BERT-detector → T5-corrector (pre-filter)
- T5 → BERT-verifier (post-filter)

Pick the configuration with best F1 at our FPR budget. If T5-alone is
within budget, prefer it — fewer moving parts.

### 3.6 Training (T5)

- lr 1e-4 (ByT5) / 3e-5 (Flan-T5), AdamW, linear warmup 3%.
- batch 16 (grad-accum to effective 64).
- Label-smoothed cross-entropy, smoothing 0.1.
- 3-8 epochs, early-stop on val CER.
- max input: 512 bytes (ByT5) / 256 tokens (Flan-T5). Long docs
  sentence-split before inference.
- Decoding: beam 5, length_penalty 0.6, `num_return_sequences=3` to feed
  the `Suggestion` list.

### 3.7 Output mapping

Current `CheckResponse` schema (`app.py:113`) preserved:

- Run T5 → corrected text.
- Char-level diff against input → error spans.
- Each span's top-3 beams become `Suggestion(text, score)`.
- Overall `score` = 1 − (fraction of chars changed), clipped to [0, 1].
- `result` = `"ok"` if no spans, else `"error"`.

### 3.8 Success criteria (vs Qwen prod)

On held-out in-house pairs:

- Span-level F1 ≥ Qwen prod F1.
- CER on corrected output ≤ Qwen prod CER.
- **No-op rate on clean prose ≥ 98%** — hard gate. This is the most
  common failure mode for seq2seq correctors and the metric users
  notice first.
- p95 latency ≤ 500ms on 10k-char input (Qwen current ~2-4s).

If quality matches prod and T5 is cheaper → promote T5.
If T5 regresses on clean-prose no-op rate → stay on Qwen (or re-run
with BERT assist per §3.5).

---

## 4. Data pipeline

Shared infrastructure across both experiments:

### 4.1 Corpus consolidation

Script `scripts/build_corpus.py`:
- Pulls validated OCR→clean pairs from in-house sources.
- Normalizes to JSONL (schema in §2.4 / §3.4).
- De-duplicates by hash of `clean`.
- Produces train / val / test splits held out by **document**, not by
  sentence, to prevent leakage.

### 4.2 Label derivation

Script `scripts/label_detector_data.py` (only needed if §3.5 BERT-assist
experiments happen):
- Character-level Needleman-Wunsch alignment of `ocr` ↔ `clean`.
- Projects edit spans onto tokenizer tokens.
- Manual review of 500 auto-labeled examples before each training run;
  fail the job if noise > 5%.

### 4.3 Storage

JSONL files under `data/` (gitignored). Each dataset version tagged
`v{YYYYMMDD}-{commit-sha}` for reproducibility.

---

## 5. Repo layout

Experimental code lives under `experiments/` so `app.py` is untouched
during the investigation.

```
experiments/
  README.md                    # points at this spec
  continuation_bert/
    train.py
    eval.py
    serve.py                   # FastAPI shim exposing the same contract
                               #   as /v1/text/check-continuation
  ocr_t5/
    train.py
    eval.py
    serve.py                   # same, for /v1/ocr/check
    bert_assist/               # only populated if §3.5 is explored
  shared/
    data.py                    # JSONL loading, splits
    align.py                   # char-level alignment for labels + eval
    metrics.py                 # AUC, F1, CER, WER, no-op rate
```

Each `serve.py` runs on a separate port and matches the existing
`app.py` request/response schemas so a shared evaluator can hit either.

---

## 6. Evaluation

### 6.1 Golden set

Curated from in-house validated data, held out from all training:
- **Clean set** — 1-2k sentences known to be OCR-clean. Drives no-op /
  FPR metrics.
- **Noisy set** — 1-2k sentences with known errors and ground-truth
  fixes. Drives detection / correction metrics.
- **Continuation set** — 1-2k labeled `(first, second, same_doc?)`
  triples. Drives `/continuation` metrics.

### 6.2 Offline bake-off

Script `experiments/shared/bakeoff.py`:
- Hits prod (Qwen) and each experimental endpoint with the golden set.
- Logs per-request outputs, latency, and GPU/CPU seconds.
- Emits a report with side-by-side metrics and per-example diffs.

Run after each training run. Check in the report (not the raw outputs)
under `experiments/reports/{date}-{exp}/`.

### 6.3 Metrics

Continuation:
- AUC, F1, precision, recall at operating threshold, calibration error.

OCR:
- Span-level F1 (exact + partial overlap).
- Character error rate (CER) on output.
- Word error rate (WER).
- No-op rate on clean inputs.
- False-positive rate on clean inputs (edits made where none needed).

Both:
- p50 / p95 latency.
- $ per 1k requests at target GPU class (rough serving cost estimate).

### 6.4 "Within noise" threshold

For the tie-breaker (§1.2), "within noise" means:
- Continuation AUC: Δ < 0.005.
- OCR span F1: Δ < 0.01.
- OCR CER: Δ < 0.002.

Tighter thresholds → conservative; prefer staying on Qwen when truly
ambiguous. Loosen only with a deliberate decision.

### 6.5 Shadow mode (optional, before promotion)

Once an experimental model passes offline eval, run it in shadow beside
prod for 1-2 weeks:
- Each production request dual-dispatched (prod result is returned;
  experimental result is logged).
- Diffs reviewed weekly. Promotion decision gated on shadow stability,
  not just offline numbers.

---

## 7. Cost & infra

### 7.1 Serving cost estimates (rough, for tie-breaker)

| Model | Params | Typical GPU | Req/s per GPU (est.) |
|---|---|---|---|
| Qwen3-8B-Base | 8B | A100 40GB | ~2-4 |
| DeBERTa-v3-base | 184M | T4 / L4 | ~50-100 |
| ByT5-small | 300M | T4 / L4 | ~10-30 |
| Flan-T5-base | 250M | T4 / L4 | ~20-40 |

If experimental models tie on quality, these numbers are the
tie-breaker rationale.

### 7.2 Training cost

Single A100 40GB, ~1 day per full training run per experiment.
Fits comfortably in experiment budget; no multi-node required.

---

## 8. Risks

- **False positives on clean prose** — top risk for T5. Hard gate at
  ≥ 98% no-op rate. If not met, explore BERT assist (§3.5) or stay on
  Qwen.
- **Topic leakage in BERT continuation** — model learns "same topic =
  same document." Mitigate with hard negatives (§2.4).
- **Label noise** from automatic alignment — 5% cap, manual spot-checks.
- **Domain drift** (medical / legal / historical) — track per-domain
  metrics; don't promote if any domain regresses materially.
- **Decision paralysis** — "within noise" thresholds (§6.4) are
  committed in advance so bake-off outcomes are unambiguous.

---

## 9. Open questions

1. English-only v1 or multilingual from the start? (Affects base model.)
2. Approximate size of the validated in-house corpus today? Does it
   clear the §2.4 / §3.4 targets or do we need more collection first?
3. Training hardware: access to A100s, or L4s and accept slower epochs?
4. Shadow-mode feasibility in prod — is there a proxy layer that can
   dual-dispatch, or do we rely solely on offline bake-off?
5. For Experiment B, do we commit to the BERT-assist ablation up-front
   or gate it on T5-only results?

---

## 10. Explicitly out of scope

- Modifying `app.py` during the experiment phase.
- Training any model from scratch — all are fine-tuned from public
  checkpoints.
- Layout-aware / image-conditioned correction (LayoutLM family).
- Active-learning loop for continuous retraining from production data.
- Partial / per-request model selection (no A/B mixing beyond shadow
  mode).
