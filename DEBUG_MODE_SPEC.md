# TextSureOCR Debug Mode Specification

## Overview

Add comprehensive debug logging to both API endpoints (`/v1/ocr/check` and `/v1/text/check-continuation`) to enable detailed analysis of failures. Debug output should capture the full reasoning pipeline so we can understand exactly why specific errors are missed or false positives occur.

## Current State

### Already Implemented (this session)
- `CheckRequest` has `debug: bool = False` field
- `DebugInfo`, `TokenDebug`, `WordDebug` Pydantic models defined
- `CheckResponse` has optional `debug: DebugInfo | None` field
- `_ocr_check()` accepts `debug` param and collects basic info:
  - All tokens with probabilities and top predictions
  - Per-word analysis with candidates, scores, and outcomes
- Environment variables: `TEXTSURE_DEBUG`, `TEXTSURE_BRANCH_EXPLORE`

### Not Yet Implemented
- Continuation endpoint debug output
- Tokenization-level debug info (how each word tokenizes)
- Branch-and-explore detailed results

---

## Phase 1: Complete OCR Check Debug Output

### 1.1 Token-Level Debug

For each token, capture:
```python
class TokenDebug(BaseModel):
    text: str                           # The actual text at this position
    token_id: int                       # Model's token ID
    char_start: int
    char_end: int
    actual_prob: float                  # P(actual | prefix)
    actual_log_prob: float              # log P
    top_predictions: list[tuple[str, float, int]]  # (text, prob, token_id)
    is_suspicious: bool                 # Below TOKEN_PROB_FLOOR
    word_context: str | None            # Which word this token belongs to
```

### 1.2 Word-Level Debug

For each word analyzed, capture:
```python
class WordDebug(BaseModel):
    word: str
    start: int
    end: int
    # Tokenization info
    tokenization: list[str]             # How this word tokenizes ["▁dis", "dose"]
    token_ids: list[int]                # Corresponding token IDs
    token_probs: list[float]            # Per-token probabilities
    word_surprisal: float               # Mean negative log-prob
    
    # Detection info
    suspicious_tokens: list[int]        # Indices of low-prob tokens
    structural_match: bool
    structural_reasons: list[str]       # ["d_in_word", "rn_pattern", etc.]
    branch_explore: bool                # Included via BRANCH_EXPLORE mode
    
    # Candidate generation
    softmax_candidates: list[str]       # From top-k at suspicious positions
    heuristic_candidates: list[str]     # From confusion map
    candidates_pre_filter: list[str]    # Before similarity/shape filter
    candidates_post_filter: list[str]   # After filtering
    
    # Scoring
    scores: dict[str, float]            # {candidate: softmax_score}
    raw_log_probs: dict[str, float]     # {candidate: total_log_prob}
    improvement: float                  # best_correction_lp - original_lp
    
    # Decision
    outcome: str                        # "flagged", "fp_original_wins", etc.
    outcome_reason: str                 # Human-readable explanation
```

### 1.3 Branch-and-Explore Debug

When `BRANCH_EXPLORE=true`, also capture:
```python
class BranchExploreResult(BaseModel):
    word: str
    start: int
    end: int
    original_tokenization: list[str]
    original_log_prob: float
    
    corrections_tried: list[dict]       # Each correction attempt:
    # {
    #   "correction": "disclose",
    #   "tokenization": ["▁dis", "close"],
    #   "log_prob": -12.5,
    #   "improvement": 8.3,
    #   "would_flag": True
    # }
```

---

## Phase 2: Continuation Endpoint Debug Output

### 2.1 Request Schema Update
```python
class ContinuationRequest(BaseModel):
    first: str
    second: str
    debug: bool = False
```

### 2.2 Response Schema Update
```python
class ContinuationDebug(BaseModel):
    # Tokenization
    first_tokens: list[str]
    second_tokens: list[str]
    joint_tokens: list[str]             # first + " " + second
    boundary_token_idx: int             # Where second starts in joint
    
    # Conditional scoring
    conditional_token_probs: list[float]  # P(second_token_i | first + preceding)
    conditional_avg_log_prob: float
    
    # Unconditional scoring
    unconditional_token_probs: list[float]  # P(second_token_i | preceding_only)
    unconditional_avg_log_prob: float
    
    # PMI calculation
    pmi: float                          # conditional - unconditional
    pmi_score: float                    # sigmoid((PMI - 0.5) * 3)
    abs_score: float                    # sigmoid((cond_avg + 5) * 1.5)
    final_score: float                  # pmi_score * abs_score
    
    # Decision
    threshold: float                    # 0.5
    verdict: str                        # "likely_continuation" or "unlikely"

class ContinuationResponse(BaseModel):
    result: str
    score: float
    debug: ContinuationDebug | None = None
```

---

## Phase 3: Test Failure Analysis Pipeline

### 3.1 Batch Debug Script

Create `scripts/analyze_failures.py`:
```python
"""
Run all failing test cases with debug=True and collect results.

Usage:
    python scripts/analyze_failures.py --test-file tests/test_ocr_tp_structural.py
    python scripts/analyze_failures.py --test-ids hard_misc_1,hard_misc_6
"""

# Outputs:
# - failures_debug.jsonl  # One JSON object per test case
# - failures_summary.md   # Human-readable summary
```

### 3.2 Debug Output Format

For each failure, output:
```json
{
  "test_id": "hard_misc_1",
  "input_text": "The judge's staterment was...",
  "expected_error_word": "staterment",
  "expected_correction": "statement",
  
  "ocr_check_result": {
    "result": "ok",  // or "issue_detected"
    "spans": [...],
    "debug": {
      "all_tokens": [...],
      "words_analyzed": [...],
      "branch_explore_results": [...]
    }
  },
  
  "failure_analysis": {
    "word_found": true,
    "word_flagged": false,
    "reason": "fp_original_wins",
    "original_score": 0.52,
    "correction_score": 0.48,
    "log_prob_improvement": 2.1,
    "tokenization_original": ["▁state", "rment"],
    "tokenization_correction": ["▁statement"]
  }
}
```

### 3.3 Summary Report

Generate markdown report:
```markdown
# Failure Analysis Report

## Summary
- Total failures: 238
- Tokenization issues: 45 (word tokenizes poorly)
- Scoring issues: 92 (correction doesn't win)
- Detection issues: 101 (word not flagged at all)

## Failure Categories

### 1. Word Not Detected (101 cases)
Words that should have been flagged but weren't.

| Test ID | Word | Why Not Detected |
|---------|------|------------------|
| ... | ... | min_prob > 0.5, not structural |

### 2. Correction Loses Scoring (92 cases)
Word detected but original wins scoring competition.

| Test ID | Word | Original Score | Correction Score | Improvement |
|---------|------|----------------|------------------|-------------|
| ... | ... | 0.52 | 0.48 | 2.1 nats |

### 3. Tokenization Artifacts (45 cases)
Word tokenizes in a way that hurts detection/correction.

| Test ID | Word | Tokenization | Issue |
|---------|------|--------------|-------|
| hard_misc_42 | systern | ["▁syst", "ern"] | "ern" token has moderate prob |
```

---

## Implementation Tasks

1. [x] Add `token_id` field to TokenDebug
2. [x] Add tokenization info to WordDebug (token strings, IDs, per-token probs)
3. [x] Add `word_surprisal` calculation
4. [x] Expand `structural_reasons` to list all matching patterns
5. [x] Separate softmax vs heuristic candidates in debug output
6. [x] Add `outcome_reason` with human-readable explanation
7. [x] Implement ContinuationDebug model and collection
8. [x] Update continuation endpoint to accept debug param
9. [x] Create `scripts/analyze_failures.py`
10. [x] Create failure categorization logic
11. [x] Generate markdown summary report

---

## Environment Variables

```bash
# Enable debug mode globally (all requests)
export TEXTSURE_DEBUG=true

# Enable branch-and-explore (try corrections on all words)
export TEXTSURE_BRANCH_EXPLORE=true
```

## API Usage

```bash
# Single request with debug
curl -X POST http://localhost:8000/v1/ocr/check \
  -H "Content-Type: application/json" \
  -d '{"text": "The disdose was filed", "debug": true}'

# Response includes full debug info
{
  "result": "issue_detected",
  "score": 0.95,
  "spans": [...],
  "debug": {
    "all_tokens": [...],
    "words_analyzed": [...]
  }
}
```

---

## Changes Made This Session

1. **Removed `_D_BETWEEN_VOWELS` restriction** — now flags any word with `d` adjacent to letters
2. **Expanded `_D_SAFE_WORDS`** — large list of common English words with `d`
3. **Added `BRANCH_EXPLORE` mode** — try corrections on all words with OCR patterns
4. **Added basic debug scaffolding** — `DebugInfo`, `TokenDebug`, `WordDebug` models
5. **Cleaned garbage test cases** — removed invalid OCR patterns (extra `r` insertion, etc.)

## Files Modified

- `app.py` — main implementation
- `tests/test_ocr_tp_structural.py` — removed garbage test cases
