# Failure Analysis Report

## Summary
- Total failures: 4
- Word not analyzed: 2
- Original wins scoring: 0
- Low log-prob improvement: 0
- No candidates generated: 0
- Filtered by similarity: 0
- Other: 2

## By Category
- char_cl_d: 2 failures
- char_rn_m: 1 failures
- char_vv_w: 1 failures

## Failure Categories

### 1. Word Not Analyzed
Words that should have been flagged but weren't even analyzed.

| Test ID | Word | Correction | Category |
|---------|------|------------|----------|
| cl_d_oracle_1 | orade | oracle | char_cl_d |
| vv_w_wisdom_1 | vvisdom | wisdom | char_vv_w |

