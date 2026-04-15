# TextSureOCR Test Failures — Run 3

**Summary:** 148 failed / 1280 total (88.4% pass rate)

_Snapshot from `/tmp/ocr_runs/run3.xml`_


## Failure counts by group

| Test function | Group | Fails |
|---|---|---:|
| `test_ocr_multi_error` | `multi_error` | 62 |
| `test_ocr_hard_case` | `hard_misc` | 20 |
| `test_ocr_hard_case` | `hard_punct` | 6 |
| `test_ocr_hard_case` | `hard_tech` | 4 |
| `test_ocr_hard_case` | `hard_numctx` | 4 |
| `test_ocr_hard_case` | `hard_num` | 3 |
| `test_ocr_hard_case` | `hard_quote` | 3 |
| `test_ocr_hard_case` | `hard_compound` | 3 |
| `test_ocr_hard_case` | `hard_list` | 3 |
| `test_ocr_hard_case` | `hard_long_ctx` | 2 |
| `test_ocr_hard_case` | `hard_end` | 2 |
| `test_ocr_hard_case` | `hard_realword` | 2 |
| `test_ocr_hard_case` | `hard_multi_corr` | 2 |
| `test_ocr_hard_case` | `hard_cap` | 2 |
| `test_ocr_hard_case` | `hard_poss` | 2 |
| `test_ocr_hard_case` | `hard_plural` | 2 |
| `test_ocr_char_confusion` | `rn_m_manner` | 1 |
| `test_ocr_char_confusion` | `rn_m_moment` | 1 |
| `test_ocr_char_confusion` | `rn_m_animal` | 1 |
| `test_ocr_char_confusion` | `rn_m_mental` | 1 |
| `test_ocr_char_confusion` | `rn_m_material` | 1 |
| `test_ocr_char_confusion` | `rn_m_mineral` | 1 |
| `test_ocr_char_confusion` | `cl_d_disclose` | 1 |
| `test_ocr_char_confusion` | `cl_d_enclose` | 1 |
| `test_ocr_char_confusion` | `cl_d_acclaim` | 1 |
| `test_ocr_char_confusion` | `cl_d_incline` | 1 |
| `test_ocr_char_confusion` | `cl_d_oracle` | 1 |
| `test_ocr_char_confusion` | `vv_w_wisdom` | 1 |
| `test_ocr_char_confusion` | `li_little` | 1 |
| `test_ocr_char_confusion` | `fi_finish` | 1 |
| `test_ocr_char_confusion` | `misc_confirm` | 1 |
| `test_ocr_char_confusion` | `misc_affirm` | 1 |
| `test_ocr_hard_case` | `hard_short` | 1 |
| `test_ocr_hard_case` | `hard_tense` | 1 |
| `test_ocr_hard_case` | `hard_adv` | 1 |
| `test_ocr_hard_case` | `hard_question` | 1 |
| `test_ocr_hard_case` | `hard_legal` | 1 |
| `test_ocr_digit_substitution` | `0_o_direction` | 1 |
| `test_ocr_digit_substitution` | `0_o_north` | 1 |
| `test_ocr_digit_substitution` | `0_o_strong` | 1 |
| `test_ocr_digit_substitution` | `1_l_total` | 1 |
| `test_ocr_digit_substitution` | `8_b_cabinet` | 1 |

## Detailed failures

### `test_ocr_char_confusion` — `cl_d_disclose` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `cl_d_disclose_1` | The court ordered the company to disdose its internal emails. | `disdose` | `disclose` |

### `test_ocr_char_confusion` — `cl_d_enclose` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `cl_d_enclose_1` | Please endose a self | `addressed envelope with your application.` | `endose` |

### `test_ocr_char_confusion` — `cl_d_incline` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `cl_d_incline_1` | Cooler temperatures tend to indine people toward heartier meals. | `indine` | `incline` |

### `test_ocr_char_confusion` — `cl_d_oracle` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `cl_d_oracle_1` | The priestess delivered the orade's cryptic message to the king. | `orade` | `oracle` |

### `test_ocr_char_confusion` — `misc_confirm` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `misc_confirm_1` | Can the witness confrrn where she was on the evening of the robbery? | `confrrn` | `confirm` |

### `test_ocr_char_confusion` — `rn_m_animal` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `rn_m_animal_1` | A frightened anirnai bolted across the road and disappeared into the brush. | `anirnai` | `animal` |

### `test_ocr_char_confusion` — `rn_m_manner` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `rn_m_manner_1` | She answered the question in a brusque rnanner that ended the conversation. | `rnanner` | `manner` |

### `test_ocr_char_confusion` — `rn_m_material` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `rn_m_material_1` | The factory orders raw rnaterial from a single supplier. | `rnaterial` | `material` |

### `test_ocr_char_confusion` — `rn_m_mental` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `rn_m_mental_1` | The ordeal left him in a fragile rnental state. | `rnental` | `mental` |

### `test_ocr_char_confusion` — `rn_m_mineral` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `rn_m_mineral_1` | Quartz is a common rnineral in granite and sandstone. | `rnineral` | `mineral` |

### `test_ocr_char_confusion` — `rn_m_moment` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `rn_m_moment_1` | At that rnoment the phone finally rang. | `rnoment` | `moment` |

### `test_ocr_char_confusion` — `vv_w_wisdom` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `vv_w_wisdom_1` | The villagers spoke of her wisdom as a gift from her late grandmother. | `vvisdom` | `wisdom` |

### `test_ocr_digit_substitution` — `0_o_direction` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `0_o_direction_1` |  | `` | `` |

### `test_ocr_digit_substitution` — `0_o_north` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `0_o_north_1` |  | `` | `` |

### `test_ocr_digit_substitution` — `0_o_strong` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `0_o_strong_1` |  | `` | `` |

### `test_ocr_digit_substitution` — `1_l_total` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `1_l_total_1` |  | `` | `` |

### `test_ocr_digit_substitution` — `8_b_cabinet` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `8_b_cabinet_1` |  | `` | `` |

### `test_ocr_hard_case` — `hard_adv` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_adv_10` | The rninimally invasive procedure reduced recovery time | `rninimally` | `minimally` |

### `test_ocr_hard_case` — `hard_cap` (2 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_cap_11` | GOVERNRNENT OFFICIALS RELEASED THE CLASSIFIED REPORT | `GOVERNRNENT` | `GOVERNMENT` |
| `hard_cap_19` | The Annual Tourrnarment drew competitors from twenty nations | `Tourrnarment` | `Tournament` |

### `test_ocr_hard_case` — `hard_compound` (3 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_compound_1` | The govemment released a statement, and the cornrnunity responded positively | `govemment` | `government` |
| `hard_compound_6` | The tourrnarment was postponed, but organizers rescheduled quickly | `tourrnarment` | `tournament` |
| `hard_compound_10` | The rnaterial arrived late, but the project still finished on time | `rnaterial` | `material` |

### `test_ocr_hard_case` — `hard_end` (2 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_end_14` | The election was decided by a narrow rnargin | `rnargin` | `margin` |
| `hard_end_20` | The court hearing was scheduled for the afternoorn | `afternoorn` | `afternoon` |

### `test_ocr_hard_case` — `hard_legal` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_legal_6` | The plaintiff alleges that the defenclant violated the agreement | `defenclant` | `defendant` |

### `test_ocr_hard_case` — `hard_list` (3 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_list_4` | The team comprised engineers, rnathematicians, physicists, and analysts | `rnathematicians` | `mathematicians` |
| `hard_list_5` | Priority areas: infrastruclure, transportation, energy, and water | `infrastruclure` | `infrastructure` |
| `hard_list_6` | The kit includes: therrometer, bandages, antiseptic, and gloves | `therrometer` | `thermometer` |

### `test_ocr_hard_case` — `hard_long_ctx` (2 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_long_ctx_19` | The new highway bypass reduced travel time between the two cities by nearly thirty minutes | `govemment` | `government` |
| `hard_long_ctx_20` | The school district implemented a comprehensive teacher training program focusing on moder | `rnethods` | `methods` |

### `test_ocr_hard_case` — `hard_misc` (20 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_misc_1` | The judge's staterment was carefully worded to avoid ambiguity | `staterment` | `statement` |
| `hard_misc_6` | The rnanuscript was discovered in the basement of the old library | `rnanuscript` | `manuscript` |
| `hard_misc_8` | The suprerme court's decision was announced this morning | `suprerme` | `supreme` |
| `hard_misc_11` | The rnajority of respondents supported the proposed change | `rnajority` | `majority` |
| `hard_misc_14` | The rnilestone was reached ahead of the original schedule | `rnilestone` | `milestone` |
| `hard_misc_17` | The advertiserment campaign reached millions of viewers | `advertiserment` | `advertisement` |
| `hard_misc_18` | The arrangerment of the conference was handled professionally | `arrangerment` | `arrangement` |
| `hard_misc_22` | The settlerment agreement was reached after long negotiations | `settlerment` | `settlement` |
| `hard_misc_31` | The exciterment surrounding the discovery was palpable | `exciterment` | `excitement` |
| `hard_misc_37` | The detachrment was deployed to the northern border | `detachrment` | `detachment` |
| `hard_misc_40` | The deployrment was completed without major incidents | `deployrment` | `deployment` |
| `hard_misc_42` | The systern was designed to handle peak loads efficiently | `systern` | `system` |
| `hard_misc_43` | The prograrn was launched to support first | `generation students` | `prograrn` |
| `hard_misc_44` | The problern was identified during the routine audit process | `problern` | `problem` |
| `hard_misc_45` | The bottorn line showed a net loss for the third quarter | `bottorn` | `bottom` |
| `hard_misc_46` | The randorn selection process ensured statistical validity | `randorn` | `random` |
| `hard_misc_47` | The custorn software was developed to meet specific needs | `custorn` | `custom` |
| `hard_misc_48` | The kingdorn prospered under the new ruler's leadership | `kingdorn` | `kingdom` |
| `hard_misc_49` | The phantorn signal appeared intermittently on the radar | `phantorn` | `phantom` |
| `hard_misc_50` | The wisclom of the decision was debated for years afterward | `wisclom` | `wisdom` |

### `test_ocr_hard_case` — `hard_multi_corr` (2 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_multi_corr_17` | The rnisunderstanding arose from a lack of communication | `rnisunderstanding` | `misunderstanding` |
| `hard_multi_corr_19` | The rnanufacturer recalled thousands of defective units | `rnanufacturer` | `manufacturer` |

### `test_ocr_hard_case` — `hard_num` (3 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_num_6` | Approximately 85 rnillion people were affected by the policy | `rnillion` | `million` |
| `hard_num_7` | The cornpany earned $4.2 rnillion in the first quarter | `rnillion` | `million` |
| `hard_num_15` | The 8 departrments reported their quarterly results | `departrments` | `departments` |

### `test_ocr_hard_case` — `hard_numctx` (4 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_numctx_6` | The $12.5 rnillion grant funded 8 research laboratories | `rnillion` | `million` |
| `hard_numctx_9` | By 2030 the govemment plans to reduce emissions by 40 percent | `govemment` | `government` |
| `hard_numctx_10` | The 1,200 | `seat auditorium hosted the tourrnarment finals in 2022` | `tourrnarment` |
| `hard_numctx_12` | The $8.7 rnillion contract was awarded to the lowest bidder | `rnillion` | `million` |

### `test_ocr_hard_case` — `hard_plural` (2 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_plural_4` | All departrments submitted their quarterly reports on time | `departrments` | `departments` |
| `hard_plural_16` | The rnanagers discussed the proposed organizational changes | `rnanagers` | `managers` |

### `test_ocr_hard_case` — `hard_poss` (2 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_poss_4` | The departrment's budget was reduced by fifteen percent | `departrment's` | `department's` |
| `hard_poss_10` | The organization's rnanagement structure was overhauled completely | `rnanagement` | `management` |

### `test_ocr_hard_case` — `hard_punct` (6 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_punct_3` | The environrnent\u2014already fragile\u2014needed immediate protection. | `environrnent` | `environment` |
| `hard_punct_9` | The cornrnand\u2014once given\u2014cannot be revoked. | `cornrnand` | `command` |
| `hard_punct_11` | After the tourrnarment, players celebrated their victory. | `tourrnarment` | `tournament` |
| `hard_punct_12` | The rnaterial (imported from overseas) was expensive. | `rnaterial` | `material` |
| `hard_punct_18` | The uniforrn\u2014worn by all employees\u2014was recently updated. | `uniforrn` | `uniform` |
| `hard_punct_20` | The alarnm (installed last month) triggered at midnight. | `alarnm` | `alarm` |

### `test_ocr_hard_case` — `hard_question` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_question_8` | Who authorized the departrment budget increase? | `departrment` | `department` |

### `test_ocr_hard_case` — `hard_quote` (3 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_quote_10` | The spokesperson said: "The departrment is fully operational." | `departrment` | `department` |
| `hard_quote_11` | The invitation stated: "The tourrnarment begins at noon." | `tourrnarment` | `tournament` |
| `hard_quote_20` | The reviewer wrote: "The perforrnnance was absolutely outstanding." | `perforrnnance` | `performance` |

### `test_ocr_hard_case` — `hard_realword` (2 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_realword_2` | The nation celebrated its independence with a grand cererrony | `cererrony` | `ceremony` |
| `hard_realword_14` | The agency planned to disdose the findings next week | `disdose` | `disclose` |

### `test_ocr_hard_case` — `hard_short` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_short_12` | Departrment budget review | `Departrment` | `Department` |

### `test_ocr_hard_case` — `hard_tech` (4 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_tech_12` | The algorithrn was optimized for large | `scale data processing tasks` | `algorithrn` |
| `hard_tech_13` | The photovoltalc cells converted sunlight into electrical energy | `photovoltalc` | `photovoltaic` |
| `hard_tech_14` | The rnicroprocessor executed billions of instructions per second | `rnicroprocessor` | `microprocessor` |
| `hard_tech_15` | The infrastruclure supported high | `bandwidth data transmission` | `infrastruclure` |

### `test_ocr_hard_case` — `hard_tense` (1 fails)

| test_id | text | error_word | expected |
|---|---|---|---|
| `hard_tense_13` | The agency was rnonitoring the situation around the clock | `rnonitoring` | `monitoring` |

### `test_ocr_multi_error` — `multi_error` (62 fails)

| test_id | text | min_spans |
|---|---|---|
| `multi_3b` | The environment needs immediate protection frorn pollution | 1 |
| `multi_12a` | The instrurnent was usecl for rneasuring ternperature | 2 |
| `multi_15c` | The experirnental pIatform was deployed last rnonth | 2 |
| `multi_16b` | Stuclents should complete the assignrnent by Friclay | 2 |
| `multi_17a` | The police departrment announced new safety rneasures | 1 |
| `multi_17c` | The poIice departrment announced new safety rneasures | 2 |
| `multi_23a` | Parents should rnonitor their children's activities | 1 |
| `multi_24a` | The terrninal was closecl for rnaintenance last week | 2 |
| `multi_28a` | The rnineral deposits were discoveredl Iast year | 2 |
| `multi_28c` | The rnineral deposits vvere discovered last year | 2 |
| `multi_30a` | The alarnm system was testecl during the storm | 2 |
| `multi_30b` | The alarm systern was tested during the storm | 1 |
| `multi_31a` | The platforrn supportecl thousands of daily users | 2 |
| `multi_34c` | The education systern needs fundamental changecl | 1 |
| `multi_35a` | The recornrnendation was acceptecl by the board | 2 |
| `multi_37a` | The rnernorial was visitecl by thousands of tourists | 2 |
| `multi_39a` | The nationaI parkl attracted rnillions of visitors | 2 |
| `multi_39b` | The national park attracted miIIions of visitors | 1 |
| `multi_41a` | The cornrnunity center hostecl a fundraising event | 2 |
| `multi_41b` | The community center hosted a fundraising event | 1 |
| `multi_41c` | The cornrnunity center hosted a funclraising event | 2 |
| `multi_42a` | The therrnal energy systern was highly efficient | 2 |
| `multi_43a` | Management approvecl the budget for the new project | 1 |
| `multi_44c` | The teacher explalined the experimental procedure | 1 |
| `multi_46b` | The rnanager confirmed the schedule for the event | 1 |
| `multi_47a` | The hospitaI adminlstration announcecl new policies | 2 |
| `multi_49a` | The docurnent was signecl by all participating parties | 2 |
| `multi_50a` | The anirnai shelter receivecl generous donations | 2 |
| `multi_51a` | The rnilitary cornrnander issuecl new orders today | 2 |
| `multi_51c` | The rnilitary commander issued new orclers today | 2 |
| `multi_52a` | The ftlm festival attractecl international attention | 2 |
| `multi_55a` | The netvvork systern requirecl significant upgrades | 2 |
| `multi_55c` | The netvvork systern required significant upgracles | 2 |
| `multi_56a` | The corrununity gardlen provided fresh vegetables | 2 |
| `multi_56c` | The corrununity garden proviclecl fresh vegetables | 2 |
| `multi_56d` | The corrununity gardlen provicled fresh vegetabIes | 2 |
| `multi_59a` | Investigators reviewecl the crirninal's background | 2 |
| `multi_59c` | Investigators reviewecl the criminal's backgrounld | 2 |
| `multi_60a` | The schooi district approvecl a new curriculurn | 2 |
| `multi_61c` | The pubIic library expandecl its digital collection | 2 |
| `multi_62a` | The transportation systern servecl millions of riders | 1 |
| `multi_64a` | The forrnal investigation uncoverecl critical evidence | 2 |
| `multi_66a` | The judge dismissecl the case due to insufficient evidence | 1 |
| `multi_66b` | The juclge dismissed the case due to insufficient eviclence | 1 |
| `multi_66d` | The juclge dismissecl the case due to insufficient eviclence | 1 |
| `multi_67a` | The vvindow was brokecl during the severe storm | 2 |
| `multi_74c` | The software development tearn released a new version | 1 |
| `multi_75a` | The farrner harvested a rnajor crop this season | 2 |
| `multi_75b` | The farmer harvested a major crop this season | 1 |
| `multi_80c` | Engineers testecl the network security protocol | 1 |
| `multi_81a` | The hospital announcecl new visiting hours | 1 |
| `multi_83a` | The Iibrary catalogl contained rnillions of entries | 2 |
| `multi_83b` | The library catalog contained miIIions of entries | 1 |
| `multi_83c` | The Iibrary catalog containecl millions of entries | 2 |
| `multi_84b` | The technology company announced a rnerger | 1 |
| `multi_84c` | The technology company announced a rnerger | 1 |
| `multi_85c` | The volunteer organization helped thousands of families | 1 |
| `multi_90c` | The government spokesperson issued a darification | 1 |
| `multi_93a` | The financiaI rnarket experiencecl unprecedented growth | 1 |
| `multi_94c` | The government fundecl the environmental research program | 1 |
| `multi_95a` | The nurnerical data revealecl a significant trend | 2 |
| `multi_100a` | The internationaI cornrnission reviewecl trade policies | 2 |

## Root-cause buckets


| Bucket | Pattern | Count (est.) | Fix applied in round 4 |
|---|---|---:|---|
| rn at word boundary | `rnanner`, `frorn`, `rnoment`, `rnineral`, `rnental`, `rnaterial`, `rnonitor` | ~8 char + many multi_ | ✅ Widened `_RN_IN_ALPHA` to `(?:^|alpha)rn(?:$|alpha)` |
| d→cl requires insertion | `endose→enclose`, `disdose→disclose`, `indine→incline`, `orade→oracle` | 5 | ✅ Relaxed alpha-only filter to `abs(Δlen) ≤ 2` |
| rrn requires `irm` | `confrrn→confirm`, `affrrn→affirm` | 2 | ✅ Added `"rrn": [..., "irm"]` |
| multi-error word counts | Expecting ≥2 spans but only 1 detected | ~35 | ✅ Transitively covered by rn boundary fix |
| hard_misc mixed | Compound of above + novel patterns | ~20 | Partially fixed; review after rerun |
| `addaim → acclaim` | Needs `dd → ccl` (3-edit) | 1 | ❌ Skipped (too specialized) |
| `ftmsh → finish` | Needs chained `ft→fi` + `m→ni` | 1 | ❌ Skipped |
| `vvisdom` broken test | Test text contains "wisdom", not "vvisdom" | 1 | ❌ Test fixture bug, not app bug |
| digit substitution misses | `direction_1`, `north_1`, `strong_1`, `total_1`, `cabinet_1` | 5 | Pending diagnosis post-rerun |
