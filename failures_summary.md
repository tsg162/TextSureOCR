# Failure Analysis Report

## Summary
- Total failures: 12
- Word not analyzed: 12
- Original wins scoring: 0
- Low log-prob improvement: 0
- No candidates generated: 0
- Filtered by similarity: 0
- Other: 0

## By Category
- char_cl_d: 5 failures
- char_rn_m: 6 failures
- char_vv_w: 1 failures

## Failure Categories

### 1. Word Not Analyzed
Words that should have been flagged but weren't even analyzed.

| Test ID | Word | Correction | Category |
|---------|------|------------|----------|
| rn_m_manner_1 | rnanner | manner | char_rn_m |
| rn_m_moment_1 | rnoment | moment | char_rn_m |
| rn_m_animal_1 | anirnai | animal | char_rn_m |
| rn_m_mental_1 | rnental | mental | char_rn_m |
| rn_m_material_1 | rnaterial | material | char_rn_m |
| rn_m_mineral_1 | rnineral | mineral | char_rn_m |
| cl_d_disclose_1 | disdose | disclose | char_cl_d |
| cl_d_enclose_1 | endose | enclose | char_cl_d |
| cl_d_acclaim_1 | adaim | acclaim | char_cl_d |
| cl_d_incline_1 | indine | incline | char_cl_d |
| cl_d_oracle_1 | orade | oracle | char_cl_d |
| vv_w_wisdom_1 | vvisdom | wisdom | char_vv_w |

