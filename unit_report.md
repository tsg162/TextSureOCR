# TextSureOCR Unit Test Report

- **Source:** `/tmp/textsure_unit.xml`
- **Cases:** 2223  (2223 pass · 0 fail · 0 error · 0 skip)
- **Accuracy:** 100.00% (executed: 2223)
- **Total test-time:** 0.0s
- **Throughput:** 148200.00 tests/sec  ·  **mean** 0 ms/test
- **Latency:** p50 0 ms · p95 0 ms · p99 0 ms · max 3 ms

## Per-file breakdown

| File | Pass | Fail | Error | Skip | Accuracy | Mean (ms) | Sum (s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `tests` | 2223 | 0 | 0 | 0 | 100.0% | 0 | 0.0 |

## Failures (0)

_None._
## Slowest 30 tests

| # | Time (ms) | Status | Test |
|---:|---:|---|---|
| 1 | 3 | pass | `tests.test_unit.TestSigmoidProperties::test_abs_sigmoid_complement[-9.5]` |
| 2 | 2 | pass | `tests.test_unit.TestCombinedScore::test_combined_monotone_in_pmi[0.8]` |
| 3 | 1 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['hello'-'hello']` |
| 4 | 1 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['list'-'list']` |
| 5 | 1 | pass | `tests.test_unit.TestFirstWordMultipleWords::test_returns_first_word_only['X Y Z'-'x']` |
| 6 | 1 | pass | `tests.test_unit.TestSpanValid::test_valid_span[0-5-hello-ocr_error]` |
| 7 | 1 | pass | `tests.test_unit.TestBuildCorrectionBasic::test_single_suspicious_token[br0wn-4-9-6-7-100-o-brown]` |
| 8 | 1 | pass | `tests.test_unit.TestBuildCorrectionBasic::test_single_suspicious_token[t3st-0-4-1-2-300-e-test]` |
| 9 | 1 | pass | `tests.test_unit.TestBuildCorrectionBasic::test_single_suspicious_token[w0rld-0-5-1-2-400-o-world]` |
| 10 | 1 | pass | `tests.test_unit.TestBuildCorrectionWordOffset::test_offset_word[hello-10-15-11-12-100-E-hEllo]` |
| 11 | 1 | pass | `tests.test_unit.TestBuildCorrectionWordOffset::test_offset_word[world-20-25-20-21-200-W-World]` |
| 12 | 1 | pass | `tests.test_unit.TestBuildCorrectionWordOffset::test_offset_word[test-5-9-7-8-300-S-teSt]` |
| 13 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['World'-'world']` |
| 14 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['TESTING'-'testing']` |
| 15 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['Python'-'python']` |
| 16 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['a'-'a']` |
| 17 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['Z'-'z']` |
| 18 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['abc'-'abc']` |
| 19 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['XYZ'-'xyz']` |
| 20 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['MixedCase'-'mixedcase']` |
| 21 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['lowercase'-'lowercase']` |
| 22 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['UPPERCASE'-'uppercase']` |
| 23 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['tEsT'-'test']` |
| 24 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['AbCdEf'-'abcdef']` |
| 25 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['word'-'word']` |
| 26 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['text'-'text']` |
| 27 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['data'-'data']` |
| 28 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['code'-'code']` |
| 29 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['file'-'file']` |
| 30 | 0 | pass | `tests.test_unit.TestFirstWordBasic::test_basic_words['test'-'test']` |
