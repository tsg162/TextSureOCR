# TextSureOCR

Text forensics service for OCR and document pipelines. Detects probable OCR errors, suggests corrections, and evaluates text continuity between fragments using token-level language model scoring.

See [SPECS.md](SPECS.md) for the API specification.

## Architecture

**Model**: Qwen2.5-7B-Instruct (~14GB VRAM, FP16)

**OCR error detection** (`POST /v1/ocr/check`):
1. Forward-pass the text → per-token log-probabilities
2. Aggregate to word-level surprisal (negative log-prob)
3. Flag candidates from two sources:
   - **Heuristic**: digit↔letter mixtures (br0wn, H3llo, p0lice)
   - **Statistical**: words whose surprisal exceeds mean + 1.5σ (catches rn→m, garbled text)
4. Generate correction suggestions via instruct-mode greedy decoding
5. Score [original, corrections] by full-text log-probability (softmax-normalised)
6. False-positive filter: if original word scores highest, skip it

**Text continuation** (`POST /v1/text/check-continuation`):
1. Compute P(second | first) via conditional log-probs
2. Compute P(second) standalone
3. PMI = conditional − unconditional (does context help predict the next fragment?)
4. Combined score = sigmoid(PMI) × sigmoid(absolute conditional probability)
5. This prevents gibberish from scoring high even when PMI is weakly positive

## Deployment

Runs on Vast.ai GPU instances via [GPUHarbor](../GPUHarbor).

```bash
# Submit to a running GPU instance
bash submit.sh gpu1

# Follow logs
gpuharbor logs <job_id> --server gpu1 --follow
```

The service runs on port 5002.

## Configuration

Environment variables (set in job YAML or .env):

| Variable | Default | Description |
|----------|---------|-------------|
| `TEXTSURE_MODEL` | `Qwen/Qwen2.5-7B-Instruct` | HuggingFace model ID |
| `TEXTSURE_PORT` | `5002` | API listen port |
| `TEXTSURE_SURPRISAL_Z` | `1.5` | Z-score threshold for surprisal outliers |
| `TEXTSURE_SURPRISAL_FLOOR` | `8.0` | Minimum absolute surprisal threshold |

## Performance (RTX 3090)

- Model load: ~4s (cached weights)
- OCR check (clean text): ~40ms
- OCR check (with errors): ~200-700ms (depends on number of corrections to generate)
- Continuation check: ~60ms
- GPU memory: ~14GB

## Files

```
TextSureOCR/
├── app.py              # FastAPI service with LM inference
├── job-setup.yaml      # GPUHarbor job template
├── submit.sh           # Encode + submit to GPU instance
├── requirements.txt    # Python dependencies
├── SPECS.md            # API specification
└── README.md           # This file
```

## Known Limitations

- Character-level confusions (rn→m, cl→d) are detected via surprisal, not heuristics. Some instances may be missed if their surprisal falls below the adaptive threshold.
- Suggestion scores in heavily-corrupted text can be low because the model adapts to the corrupted style. The corrections are still correct — only the relative scores are affected.
- Single GPU, single-request throughput. For production batching, consider vLLM.
