# TextSureOCR Test Report

- **Endpoint:** `https://ts1-textsure.gpuharbor.xyz`
- **Model:** `Qwen/Qwen2.5-7B-Instruct` on `cuda` (loaded: True)
- **Run at:** 2026-04-14T19:58:56
- **Wall time:** 10.6s

## Summary

| Suite | Passed | Total | Accuracy |
|---|---|---|---|
| OCR check | 16 | 16 | 100.0% |
| Continuation check | 10 | 10 | 100.0% |
| **Overall** | **26** | **26** | **100.0%** |

## Timing

- OCR: mean 0.53s · p50 0.54s · p95 0.65s · min 0.29s · max 0.99s · sum 8.5s
- Continuation: mean 0.21s · p50 0.21s · p95 0.22s · min 0.20s · max 0.26s · sum 2.1s
- All: mean 0.41s · p50 0.42s · p95 0.63s · min 0.20s · max 0.99s · sum 10.6s

## Misses (0)

_None — all tests passed._
## Full Results

### OCR Check

| Test | Result | Time (s) | Detail |
|---|---|---|---|
| single digit sub (br0wn) | ✅ PASS | 0.42 | result=issue_detected score=0.99 spans=1 |
| multiple digit subs (heavy leet) | ✅ PASS | 0.99 | result=issue_detected score=0.982 spans=3 |
| single error in clean context (p0lice) | ✅ PASS | 0.55 | result=issue_detected score=0.99 spans=2 |
| rn→m confusion (governrnent) | ✅ PASS | 0.63 | result=issue_detected score=0.99 spans=1 |
| zero for O (c0mputer) | ✅ PASS | 0.65 | result=issue_detected score=0.99 spans=1 |
| one for l (1etter) | ✅ PASS | 0.59 | result=issue_detected score=0.99 spans=1 |
| five for S (5chool) | ✅ PASS | 0.54 | result=issue_detected score=0.99 spans=1 |
| garbled word (teh → the) | ✅ PASS | 0.48 | result=issue_detected score=0.99 spans=1 |
| clean prose | ✅ PASS | 0.30 | result=ok score=0.85 spans=0 |
| legitimate numbers only | ✅ PASS | 0.40 | result=ok score=0.85 spans=0 |
| technical with numbers | ✅ PASS | 0.48 | result=ok score=0.85 spans=0 |
| acronyms and abbreviations | ✅ PASS | 0.56 | result=ok score=0.85 spans=0 |
| date and time | ✅ PASS | 0.29 | result=ok score=0.85 spans=0 |
| proper nouns | ✅ PASS | 0.63 | result=ok score=0.85 spans=0 |
| all caps heading | ✅ PASS | 0.44 | result=ok score=0.85 spans=0 |
| currency and measurements | ✅ PASS | 0.53 | result=ok score=0.85 spans=0 |

### Continuation Check

| Test | Result | Time (s) | Detail |
|---|---|---|---|
| natural sentence split | ✅ PASS | 0.20 | result=likely_continuation score=0.999 |
| sentence boundary | ✅ PASS | 0.21 | result=likely_continuation score=0.947 |
| paragraph continuation | ✅ PASS | 0.26 | result=likely_continuation score=0.945 |
| mid-word line break (hypothet-ical) | ✅ PASS | 0.20 | result=likely_continuation score=0.972 |
| enumeration continuation | ✅ PASS | 0.21 | result=likely_continuation score=0.995 |
| random gibberish | ✅ PASS | 0.22 | result=unlikely_continuation score=0.003 |
| cross-column discontinuity | ✅ PASS | 0.20 | result=unlikely_continuation score=0.05 |
| language switch | ✅ PASS | 0.20 | result=unlikely_continuation score=0.012 |
| topic whiplash | ✅ PASS | 0.20 | result=unlikely_continuation score=0.286 |
| reversed text | ✅ PASS | 0.21 | result=unlikely_continuation score=0.034 |
