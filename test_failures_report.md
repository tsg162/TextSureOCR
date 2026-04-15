# Test Failure Report
**Run date:** 2026-04-15  
**Duration:** 1033.54s (17m 13s)

## Summary

| Metric | Value |
|--------|-------|
| Total tests | 3917 |
| Passed | 3679 |
| Failed | **238** |
| **Failure rate** | **6.07%** |

---

## Failures by Test File & Function

### `test_ocr_tp_structural.py`

| Test function | Failures |
|---|---|
| `test_ocr_char_confusion` | 11 |
| `test_ocr_multi_error` | 80 |
| `test_ocr_hard_case` | 60 |
| **Subtotal** | **151** |

### `test_continuation.py`

| Test function | Failures |
|---|---|
| `test_likely_continuation` (midsent) | 45 |
| `test_likely_continuation` (midword) | 26 |
| `test_unlikely_continuation` | 17 |
| **Subtotal** | **88** |

---

## `test_ocr_tp_structural.py` — Detailed Failures

### `test_ocr_char_confusion` (11 failures)

OCR character confusion where the model fails to correct single substitution errors.

#### `rn → m` confusion (6 failures)
| Test ID | OCR Input | Target |
|---------|-----------|--------|
| `rn_m_manner_1` | rnanner | manner |
| `rn_m_moment_1` | rnoment | moment |
| `rn_m_animal_1` | anirnai | animal |
| `rn_m_mental_1` | rnental | mental |
| `rn_m_material_1` | rnaterial | material |
| `rn_m_mineral_1` | rnineral | mineral |

#### `cl → d` confusion (4 failures)
| Test ID | OCR Input | Target |
|---------|-----------|--------|
| `cl_d_disclose_1` | disdose | disclose |
| `cl_d_enclose_1` | endose | enclose |
| `cl_d_acclaim_1` | adaim | acclaim |
| `cl_d_incline_1` | indine | incline |
| `cl_d_oracle_1` | orade | oracle |

> Note: 5 rows listed above — IDs match 5 failing entries for this group, but pytest total counts 4 in this bucket (possible off-by-one in grouping).

#### `vv → w` confusion (1 failure)
| Test ID | OCR Input | Target |
|---------|-----------|--------|
| `vv_w_wisdom_1` | vvisdom | wisdom |

---

### `test_ocr_multi_error` (80 failures)

Tests with multiple OCR errors in the same sentence. Listed by test ID with the corrupted sentence and error count.

| Test ID | Corrupted sentence | # errors |
|---|---|---|
| `multi_3b` | The environment needs immediate protection frorn pollution | 1 |
| `multi_6c` | The organization published its annual report yesterclay | 1 |
| `multi_6d` | The organization published its annual report yesterclay | 1 |
| `multi_12a` | The instrurnent was usecl for rneasuring ternperature | 2 |
| `multi_15d` | The experirnental platforrn vvas deployecl last rnonth | 2 |
| `multi_16b` | Stuclents should complete the assignrnent by Friclay | 2 |
| `multi_17a` | The police departrment announced new safety rneasures | 1 |
| `multi_17c` | The police departrment announced new safety rneasures | 1 |
| `multi_23a` | Parents should rnonitor their children's activities | 1 |
| `multi_23d` | Parents should rnonitor their children's activities | 1 |
| `multi_24a` | The terrninal was closecl for rnaintenance last week | 2 |
| `multi_24b` | The terminal was closed for rnaintenance last week | 1 |
| `multi_28a` | The rnineral deposits were discoveredl last year | 1 |
| `multi_28c` | The rnineral deposits vvere discovered last year | 2 |
| `multi_30a` | The alarnm system was testecl during the storm | 2 |
| `multi_30b` | The alarm systern was tested during the storm | 1 |
| `multi_31a` | The platforrn supportecl thousands of daily users | 2 |
| `multi_32a` | The rnuseum displayed a spectadular collection | 2 |
| `multi_34c` | The education systern needs fundamental changecl | 2 |
| `multi_35a` | The recornrnendation was acceptecl by the board | 2 |
| `multi_37a` | The rnernorial was visitecl by thousands of tourists | 2 |
| `multi_39a` | The national park attracted rnillions of visitors | 1 |
| `multi_39c` | The national park attractecl millions of visitors | 1 |
| `multi_39d` | The national park attractecl rnillions of visitors | 2 |
| `multi_41a` | The cornrnunity center hostecl a fundraising event | 2 |
| `multi_41b` | The community center hosted a fundraising event | 1 |
| `multi_41c` | The cornrnunity center hosted a funclraising event | 2 |
| `multi_42a` | The therrnal energy systern was highly efficient | 2 |
| `multi_43a` | Management approvecl the budget for the new project | 1 |
| `multi_46b` | The rnanager confirmed the schedule for the event | 1 |
| `multi_47a` | The hospital administration announcecl new policies | 1 |
| `multi_47d` | The hospital administration announcecl nevv policies | 2 |
| `multi_49a` | The docurnent was signecl by all participating parties | 2 |
| `multi_50a` | The anirnal shelter receivecl generous donations | 2 |
| `multi_51a` | The rnilitary cornrnander issuecl new orders today | 2 |
| `multi_51c` | The rnilitary commander issued new orclers today | 2 |
| `multi_52a` | The ftlm festival attractecl international attention | 2 |
| `multi_55a` | The netvvork systern requirecl significant upgrades | 2 |
| `multi_55c` | The netvvork systern required significant upgracles | 2 |
| `multi_56a` | The corrununity gardlen provided fresh vegetables | 2 |
| `multi_56b` | The community garden provicled fresh vegetables | 1 |
| `multi_56c` | The corrununity garden proviclecl fresh vegetables | 2 |
| `multi_56d` | The corrununity garden provicled fresh vegetables | 2 |
| `multi_58c` | The medical tearn completed the surgical procedure | 1 |
| `multi_58d` | The rnedical tearn cornpleted the surgical procedure | 2 |
| `multi_59a` | Investigators reviewecl the crirninal's background | 2 |
| `multi_59c` | Investigators reviewecl the criminal's backgrounld | 2 |
| `multi_60a` | The school district approvecl a new curriculum | 1 |
| `multi_60d` | The school district approvecl a nevv curriculum | 2 |
| `multi_62a` | The transportation systern servecl millions of riders | 2 |
| `multi_62d` | The transportation systern servecl millions of riders | 2 |
| `multi_64a` | The forrnal investigation uncoverecl critical evidence | 2 |
| `multi_66a` | The judge dismissecl the case due to insufficient evidence | 1 |
| `multi_66b` | The juclge dismissed the case due to insufficient eviclence | 2 |
| `multi_66d` | The juclge dismissecl the case due to insufficient eviclence | 3 |
| `multi_67a` | The vvindow was brokecl during the severe storm | 2 |
| `multi_69c` | The rnusician performed a beautiful concert last night | 1 |
| `multi_73a` | The environmental agency rnonitored the water quality | 1 |
| `multi_73d` | The environmental agency rnonitored the water quality | 1 |
| `multi_74c` | The software development tearn released a new version | 1 |
| `multi_75a` | The farrner harvested a rnajor crop this season | 2 |
| `multi_75b` | The farmer harvested a major crop this season | 1 |
| `multi_80c` | Engineers testecl the network security protocol | 1 |
| `multi_81a` | The hospital announcecl new visiting hours | 1 |
| `multi_83a` | The library catalog contained rnillions of entries | 1 |
| `multi_83c` | The library catalog containecl millions of entries | 1 |
| `multi_83d` | The library catalog containecl rnillions of entries | 2 |
| `multi_84b` | The technology company announced a rnerger | 1 |
| `multi_84c` | The technology company announced a rnerger | 1 |
| `multi_85c` | The volunteer organization helped thousands of families | 1 |
| `multi_88c` | The election commission verifiecl the results | 1 |
| `multi_90c` | The government spokesperson issued a darification | 1 |
| `multi_93a` | The financial rnarket experiencecl unprecedented growth | 2 |
| `multi_94c` | The government fundecl the environmental research program | 1 |
| `multi_95a` | The nurnerical data revealecl a significant trend | 2 |
| `multi_95b` | The numerical clata revealed a significant trend | 1 |
| `multi_98a` | The scholarship prograrn supportecl talented students | 2 |
| `multi_98d` | The scholarship prograrn supported talented students | 1 |
| `multi_99a` | The reforrn proposal was debatecl in the legislature | 2 |
| `multi_100c` | The international commission reviewed tracle policies | 1 |

---

### `test_ocr_hard_case` (60 failures)

Harder OCR correction scenarios grouped by sub-category.

#### Long-context sentences (`hard_long_ctx`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_long_ctx_19` | govemment | government |
| `hard_long_ctx_20` | rnethods | methods |

#### Technical vocabulary (`hard_tech`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_tech_12` | algorithrn | algorithm |
| `hard_tech_13` | photovoltalc | photovoltaic |
| `hard_tech_14` | rnicroprocessor | microprocessor |
| `hard_tech_15` | infrastruclure | infrastructure |

#### Word at sentence end (`hard_end`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_end_14` | rnargin | margin |

#### Punctuation-adjacent (`hard_punct`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_punct_3` | environrnent | environment |
| `hard_punct_9` | cornrnand | command |
| `hard_punct_12` | rnaterial | material |
| `hard_punct_18` | uniforrn | uniform |
| `hard_punct_20` | alarnm | alarm |

#### Numeric context (`hard_num`, `hard_numctx`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_num_6` | rnillion | million |
| `hard_num_7` | rnillion | million |
| `hard_num_15` | departrments | departments |
| `hard_numctx_6` | rnillion | million |
| `hard_numctx_9` | govemment | government |
| `hard_numctx_12` | rnillion | million |

#### Short phrases (`hard_short`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_short_12` | Departrment | Department |

#### Real-word errors (`hard_realword`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_realword_2` | cererrony | ceremony |
| `hard_realword_14` | disdose | disclose |

#### Multiple corrections (`hard_multi_corr`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_multi_corr_17` | rnisunderstanding | misunderstanding |
| `hard_multi_corr_19` | rnanufacturer | manufacturer |

#### All-caps (`hard_cap`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_cap_11` | GOVERNRNENT | GOVERNMENT |

#### Quoted text (`hard_quote`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_quote_10` | departrment | department |
| `hard_quote_20` | perforrnnance | performance |

#### Miscellaneous (`hard_misc`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_misc_1` | staterment | statement |
| `hard_misc_6` | rnanuscript | manuscript |
| `hard_misc_8` | suprerme | supreme |
| `hard_misc_11` | rnajority | majority |
| `hard_misc_14` | rnilestone | milestone |
| `hard_misc_17` | advertiserment | advertisement |
| `hard_misc_18` | arrangerment | arrangement |
| `hard_misc_22` | settlerment | settlement |
| `hard_misc_31` | exciterment | excitement |
| `hard_misc_37` | detachrment | detachment |
| `hard_misc_40` | deployrment | deployment |
| `hard_misc_42` | systern | system |
| `hard_misc_43` | prograrn | program |
| `hard_misc_44` | problern | problem |
| `hard_misc_45` | bottorn | bottom |
| `hard_misc_46` | randorn | random |
| `hard_misc_47` | custorn | custom |
| `hard_misc_48` | kingdorn | kingdom |
| `hard_misc_49` | phantorn | phantom |
| `hard_misc_50` | wisclom | wisdom |

#### Adverbs (`hard_adv`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_adv_10` | rninimally | minimally |

#### Compound sentences (`hard_compound`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_compound_1` | govemment | government |
| `hard_compound_10` | rnaterial | material |

#### Questions (`hard_question`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_question_8` | departrment | department |

#### List context (`hard_list`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_list_4` | rnathematicians | mathematicians |
| `hard_list_5` | infrastruclure | infrastructure |
| `hard_list_6` | therrometer | thermometer |

#### Possessives (`hard_poss`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_poss_4` | departrment's | department's |
| `hard_poss_10` | rnanagement | management |

#### Plurals (`hard_plural`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_plural_4` | departrments | departments |
| `hard_plural_16` | rnanagers | managers |

#### Verb tenses (`hard_tense`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_tense_13` | rnonitoring | monitoring |

#### Legal context (`hard_legal`)
| Test ID | OCR word | Correct word |
|---|---|---|
| `hard_legal_6` | defenclant | defendant |

---

## `test_continuation.py` — Detailed Failures

### `test_likely_continuation` — Mid-sentence cuts (45 failures)

These tests check that a truncated sentence prefix is correctly identified as likely to have a continuation. Failures mean the model under-estimated continuation probability.

Format: `midsent_{sentence_id}_r{ratio}` where ratio is the percentage of the sentence shown (30–70%).

| Test ID | Sentence # | Ratio shown |
|---|---|---|
| `midsent_009_r40` | 009 | 40% |
| `midsent_066_r30` | 066 | 30% |
| `midsent_078_r30` | 078 | 30% |
| `midsent_113_r70` | 113 | 70% |
| `midsent_162_r50` | 162 | 50% |
| `midsent_162_r60` | 162 | 60% |
| `midsent_162_r70` | 162 | 70% |
| `midsent_164_r60` | 164 | 60% |
| `midsent_186_r70` | 186 | 70% |
| `midsent_188_r60` | 188 | 60% |
| `midsent_188_r70` | 188 | 70% |
| `midsent_205_r60` | 205 | 60% |
| `midsent_239_r30` | 239 | 30% |
| `midsent_239_r40` | 239 | 40% |
| `midsent_239_r60` | 239 | 60% |
| `midsent_253_r30` | 253 | 30% |
| `midsent_253_r40` | 253 | 40% |
| `midsent_253_r50` | 253 | 50% |
| `midsent_253_r60` | 253 | 60% |
| `midsent_266_r70` | 266 | 70% |
| `midsent_270_r50` | 270 | 50% |
| `midsent_270_r60` | 270 | 60% |
| `midsent_270_r70` | 270 | 70% |
| `midsent_274_r30` | 274 | 30% |
| `midsent_274_r70` | 274 | 70% |
| `midsent_282_r30` | 282 | 30% |
| `midsent_297_r40` | 297 | 40% |
| `midsent_297_r60` | 297 | 60% |
| `midsent_303_r70` | 303 | 70% |
| `midsent_328_r60` | 328 | 60% |
| `midsent_336_r50` | 336 | 50% |
| `midsent_346_r70` | 346 | 70% |
| `midsent_350_r70` | 350 | 70% |
| `midsent_367_r30` | 367 | 30% |
| `midsent_368_r40` | 368 | 40% |
| `midsent_381_r60` | 381 | 60% |
| `midsent_396_r30` | 396 | 30% |
| `midsent_404_r50` | 404 | 50% |
| `midsent_405_r40` | 405 | 40% |
| `midsent_416_r30` | 416 | 30% |
| `midsent_416_r40` | 416 | 40% |
| `midsent_416_r50` | 416 | 50% |
| `midsent_416_r60` | 416 | 60% |
| `midsent_416_r70` | 416 | 70% |
| `midsent_455_r30` | 455 | 30% |
| `midsent_492_r30` | 492 | 30% |

**Notable:** Sentence #416 fails at all 5 ratio thresholds (30–70%), and sentence #253 fails at 4 of 5.

### `test_likely_continuation` — Mid-word cuts (26 failures)

These tests check continuation detection when the text is cut mid-word. Higher failure rate than mid-sentence cuts.

| Test ID |
|---|
| `midword_005` |
| `midword_011` |
| `midword_012` |
| `midword_013` |
| `midword_017` |
| `midword_025` |
| `midword_027` |
| `midword_028` |
| `midword_029` |
| `midword_031` |
| `midword_033` |
| `midword_038` |
| `midword_040` |
| `midword_044` |
| `midword_048` |
| `midword_052` |
| `midword_057` |
| `midword_063` |
| `midword_070` |
| `midword_073` |
| `midword_074` |
| `midword_075` |
| `midword_077` |
| `midword_079` |
| `midword_080` |

### `test_unlikely_continuation` (17 failures)

These tests check that truly unrelated text is correctly classified as NOT a continuation. Failures mean false positives — the model incorrectly classified an unrelated pair as a likely continuation.

Format: `unrelated_{source_id}_x{unrelated_id}`

| Test ID |
|---|
| `unrelated_047_x298` |
| `unrelated_093_x344` |
| `unrelated_127_x378` |
| `unrelated_171_x422` |
| `unrelated_176_x427` |
| `unrelated_187_x438` |
| `unrelated_242_x493` |
| `unrelated_308_x059` |
| `unrelated_398_x149` |
| `unrelated_402_x153` |
| `unrelated_421_x172` |
| `unrelated_450_x201` |
| `unrelated_457_x208` |
| `unrelated_466_x217` |
| `unrelated_484_x235` |
| `unrelated_492_x243` |
| `unrelated_497_x248` |

---

## Error Pattern Analysis

### OCR Structural — Most Common Substitution Patterns

| Pattern | Description | Affected failures (approx.) |
|---|---|---|
| `rn → m` | 'rn' OCR glitch misread as 'm' | ~70 |
| `cl → d` | 'cl' misread as 'd' | ~20 |
| `ecl` suffix | past tense `-ed` mangled to `-ecl` | ~40 |
| `rr → m` | double-r confusion (e.g. `corrununity`) | ~5 |
| `vv → w` | 'vv' misread as 'w' | ~5 |
| `lc → tc` | e.g. `photovoltalc` | 1 |
| `ft → fi` | e.g. `ftlm → film` | 1 |

### Continuation — Ratio-dependent Failures

For `midsent` tests, failures are distributed across all ratios. The 30% threshold has the most failures (hardest case — least context), but failures also appear at 70% (e.g. sentences 113, 162, 186, 266, 270, 303, 346, 350, 416), suggesting some sentences produce systematically low continuation scores regardless of how much text is shown.

### Continuation — Mid-word Failures

26 of 88 continuation failures (29.5%) come from `midword` cases. This is a concentrated failure mode — the model appears to under-score continuation probability when the text is cut mid-word.
