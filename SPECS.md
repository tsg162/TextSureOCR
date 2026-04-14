## TextSureOCR

**Mission statement:**
Build a compact text-forensics service that helps OCR and document pipelines decide whether extracted text is plausible, whether local spans are likely corrupted, and whether adjacent text fragments naturally belong together. The system should be optimized for short, structured judgments rather than open-ended generation, using language-model scoring and reranking to produce simple, auditable decisions.

The product’s goal is to make scanned text more trustworthy and document reconstruction more reliable. It should detect probable OCR errors, suggest likely corrections, and evaluate boundary continuity between lines or columns with a minimal, stable API that is easy to batch, easy to reason about, and suitable for production pipelines.


Two endpoints, same top-level structure.

### `POST /v1/ocr/check`

Request:

```json
{
  "text": "The quick br0wn fox jumps over the lazy dog"
}
```

Response:

```json
{
  "result": "issue_detected",
  "score": 0.96,
  "spans": [
    {
      "start": 10,
      "end": 15,
      "text": "br0wn",
      "kind": "probable_ocr_error",
      "suggestions": [
        { "text": "brown", "score": 0.997 },
        { "text": "crown", "score": 0.021 }
      ]
    }
  ]
}
```

Clean case:

```json
{
  "result": "ok",
  "score": 0.97,
  "spans": []
}
```

Interpretation:

* `result` is the discrete decision
* `score` is just the model’s strength for that decision
* `spans` exists only for localized findings

### `POST /v1/text/check-continuation`

Request:

```json
{
  "first": "The quick brown",
  "second": "fox jumps over the lazy dog"
}
```

Response:

```json
{
  "result": "likely_continuation",
  "score": 0.985
}
```

Bad join:

```json
{
  "result": "unlikely_continuation",
  "score": 0.08
}
```
