# ts1 — 1k OCR true-positive sample (digits + structural)

- **Source:** `/tmp/ts1_ocr_tp_1k.xml`
- **Cases:** 1000  (552 pass · 448 fail · 0 error · 0 skip)
- **Accuracy:** 55.20% (executed: 1000)
- **Total test-time:** 338.4s
- **Throughput:** 2.96 tests/sec  ·  **mean** 338 ms/test
- **Latency:** p50 327 ms · p95 555 ms · p99 645 ms · max 813 ms

## Per-file breakdown

| File | Pass | Fail | Error | Skip | Accuracy | Mean (ms) | Sum (s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `tests` | 552 | 448 | 0 | 0 | 55.2% | 338 | 338.4 |

## Failures (448)

### `tests` (448)

| Test | Status | Time (ms) | Message |
|---|---|---:|---|
| `test_ocr_digit_substitution[3_for_e__b3tter__t4]` | fail | 257 | AssertionError: Expected issue_detected for 'b3tter' in: Researchers published a comprehensive study about the b3tter |
| `test_ocr_digit_substitution[3_for_e__b3tween__t1]` | fail | 189 | AssertionError: Expected issue_detected for 'b3tween' in: The b3tween was thoroughly discussed at the annual conference |
| `test_ocr_digit_substitution[3_for_e__b3tween__t8]` | fail | 189 | AssertionError: Expected issue_detected for 'b3tween' in: Experts recommended paying closer attention to the b3tween |
| `test_ocr_digit_substitution[3_for_e__b3fore__t5]` | fail | 388 | AssertionError: Expected issue_detected for 'b3fore' in: The organization focused its efforts on improving the b3fore |
| `test_ocr_digit_substitution[3_for_e__b3hind__t2]` | fail | 323 | AssertionError: Expected issue_detected for 'b3hind' in: Many people considered the b3hind to be extremely important |
| `test_ocr_digit_substitution[3_for_e__b3hind__t9]` | fail | 322 | AssertionError: Expected issue_detected for 'b3hind' in: The recent developments regarding the b3hind surprised everyone |
| `test_ocr_digit_substitution[3_for_e__b3nefit__t6]` | fail | 373 | AssertionError: Expected issue_detected for 'b3nefit' in: After the review, the b3nefit was modified to meet new standards |
| `test_ocr_digit_substitution[3_for_e__b3lieve__t3]` | fail | 258 | AssertionError: Expected issue_detected for 'b3lieve' in: The government announced changes to the b3lieve policy |
| `test_ocr_digit_substitution[3_for_e__b3lieve__t10]` | fail | 338 | AssertionError: Expected issue_detected for 'b3lieve' in: Students were required to understand the b3lieve before proceeding |
| `test_ocr_digit_substitution[3_for_e__b3yond__t7]` | fail | 334 | AssertionError: Expected issue_detected for 'b3yond' in: The b3yond significantly impacted the outcome of the project |
| `test_ocr_digit_substitution[3_for_e__car3er__t4]` | fail | 258 | AssertionError: Expected issue_detected for 'car3er' in: Researchers published a comprehensive study about the car3er |
| `test_ocr_digit_substitution[3_for_e__c3nter__t1]` | fail | 197 | AssertionError: Expected issue_detected for 'c3nter' in: The c3nter was thoroughly discussed at the annual conference |
| `test_ocr_digit_substitution[3_for_e__c3nter__t8]` | fail | 198 | AssertionError: Expected issue_detected for 'c3nter' in: Experts recommended paying closer attention to the c3nter |
| `test_ocr_digit_substitution[3_for_e__compl3te__t5]` | fail | 393 | AssertionError: Expected issue_detected for 'compl3te' in: The organization focused its efforts on improving the compl3te |
| `test_ocr_digit_substitution[3_for_e__cr3ate__t2]` | fail | 255 | AssertionError: Expected issue_detected for 'cr3ate' in: Many people considered the cr3ate to be extremely important |
| `test_ocr_digit_substitution[3_for_e__cr3ate__t9]` | fail | 257 | AssertionError: Expected issue_detected for 'cr3ate' in: The recent developments regarding the cr3ate surprised everyone |
| `test_ocr_digit_substitution[3_for_e__d3bate__t6]` | fail | 323 | AssertionError: Expected issue_detected for 'd3bate' in: After the review, the d3bate was modified to meet new standards |
| `test_ocr_digit_substitution[3_for_e__d3crease__t3]` | fail | 189 | AssertionError: Expected issue_detected for 'd3crease' in: The government announced changes to the d3crease policy |
| `test_ocr_digit_substitution[3_for_e__d3crease__t10]` | fail | 255 | AssertionError: Expected issue_detected for 'd3crease' in: Students were required to understand the d3crease before proceeding |
| `test_ocr_digit_substitution[3_for_e__d3fense__t7]` | fail | 336 | AssertionError: Expected issue_detected for 'd3fense' in: The d3fense significantly impacted the outcome of the project |
| `test_ocr_digit_substitution[3_for_e__d3gree__t4]` | fail | 256 | AssertionError: Expected issue_detected for 'd3gree' in: Researchers published a comprehensive study about the d3gree |
| `test_ocr_digit_substitution[3_for_e__d3liver__t1]` | fail | 256 | AssertionError: Expected issue_detected for 'd3liver' in: The d3liver was thoroughly discussed at the annual conference |
| `test_ocr_digit_substitution[3_for_e__d3liver__t8]` | fail | 261 | AssertionError: Expected issue_detected for 'd3liver' in: Experts recommended paying closer attention to the d3liver |
| `test_ocr_digit_substitution[3_for_e__d3mand__t5]` | fail | 393 | AssertionError: Expected issue_detected for 'd3mand' in: The organization focused its efforts on improving the d3mand |
| `test_ocr_digit_substitution[3_for_e__d3scribe__t2]` | fail | 333 | AssertionError: Expected issue_detected for 'd3scribe' in: Many people considered the d3scribe to be extremely important |
| `test_ocr_digit_substitution[3_for_e__d3scribe__t9]` | fail | 346 | AssertionError: Expected issue_detected for 'd3scribe' in: The recent developments regarding the d3scribe surprised everyone |
| `test_ocr_digit_substitution[3_for_e__d3sign__t6]` | fail | 407 | AssertionError: Expected issue_detected for 'd3sign' in: After the review, the d3sign was modified to meet new standards |
| `test_ocr_digit_substitution[3_for_e__d3sire__t3]` | fail | 258 | AssertionError: Expected issue_detected for 'd3sire' in: The government announced changes to the d3sire policy |
| `test_ocr_digit_substitution[3_for_e__d3sire__t10]` | fail | 325 | AssertionError: Expected issue_detected for 'd3sire' in: Students were required to understand the d3sire before proceeding |
| `test_ocr_digit_substitution[3_for_e__d3termine__t7]` | fail | 375 | AssertionError: Expected issue_detected for 'd3termine' in: The d3termine significantly impacted the outcome of the project |
| `test_ocr_digit_substitution[3_for_e__d3velop__t4]` | fail | 267 | AssertionError: Expected issue_detected for 'd3velop' in: Researchers published a comprehensive study about the d3velop |
| `test_ocr_digit_substitution[3_for_e__d3vice__t1]` | fail | 261 | AssertionError: Expected issue_detected for 'd3vice' in: The d3vice was thoroughly discussed at the annual conference |
| `test_ocr_digit_substitution[3_for_e__d3vice__t8]` | fail | 250 | AssertionError: Expected issue_detected for 'd3vice' in: Experts recommended paying closer attention to the d3vice |
| `test_ocr_digit_substitution[3_for_e__diff3rent__t5]` | fail | 458 | AssertionError: Expected issue_detected for 'diff3rent' in: The organization focused its efforts on improving the diff3rent |
| `test_ocr_digit_substitution[3_for_e__dir3ct__t2]` | fail | 365 | AssertionError: Missing suggestion 'direct' for 'dir3ct' |
| `test_ocr_digit_substitution[3_for_e__dir3ct__t9]` | fail | 320 | AssertionError: Expected issue_detected for 'dir3ct' in: The recent developments regarding the dir3ct surprised everyone |
| `test_ocr_digit_substitution[3_for_e__dis3ase__t6]` | fail | 374 | AssertionError: Expected issue_detected for 'dis3ase' in: After the review, the dis3ase was modified to meet new standards |
| `test_ocr_digit_substitution[3_for_e__dr3am__t3]` | fail | 188 | AssertionError: Expected issue_detected for 'dr3am' in: The government announced changes to the dr3am policy |
| `test_ocr_digit_substitution[3_for_e__dr3am__t10]` | fail | 255 | AssertionError: Expected issue_detected for 'dr3am' in: Students were required to understand the dr3am before proceeding |
| `test_ocr_digit_substitution[3_for_e__3conomy__t7]` | fail | 325 | AssertionError: Expected issue_detected for '3conomy' in: The 3conomy significantly impacted the outcome of the project |
| `test_ocr_digit_substitution[3_for_e__3ducation__t4]` | fail | 326 | AssertionError: Expected issue_detected for '3ducation' in: Researchers published a comprehensive study about the 3ducation |
| `test_ocr_digit_substitution[3_for_e__3ffect__t1]` | fail | 190 | AssertionError: Expected issue_detected for '3ffect' in: The 3ffect was thoroughly discussed at the annual conference |
| `test_ocr_digit_substitution[3_for_e__3ffect__t8]` | fail | 189 | AssertionError: Expected issue_detected for '3ffect' in: Experts recommended paying closer attention to the 3ffect |
| `test_ocr_digit_substitution[3_for_e__3ffort__t5]` | fail | 388 | AssertionError: Expected issue_detected for '3ffort' in: The organization focused its efforts on improving the 3ffort |
| `test_ocr_digit_substitution[3_for_e__3lection__t2]` | fail | 261 | AssertionError: Expected issue_detected for '3lection' in: Many people considered the 3lection to be extremely important |
| `test_ocr_digit_substitution[3_for_e__3lection__t9]` | fail | 320 | AssertionError: Expected issue_detected for '3lection' in: The recent developments regarding the 3lection surprised everyone |
| `test_ocr_digit_substitution[3_for_e__3lement__t6]` | fail | 330 | AssertionError: Expected issue_detected for '3lement' in: After the review, the 3lement was modified to meet new standards |
| `test_ocr_digit_substitution[3_for_e__3merge__t3]` | fail | 199 | AssertionError: Expected issue_detected for '3merge' in: The government announced changes to the 3merge policy |
| `test_ocr_digit_substitution[3_for_e__3merge__t10]` | fail | 265 | AssertionError: Expected issue_detected for '3merge' in: Students were required to understand the 3merge before proceeding |
| `test_ocr_digit_substitution[3_for_e__3nergy__t7]` | fail | 320 | AssertionError: Expected issue_detected for '3nergy' in: The 3nergy significantly impacted the outcome of the project |
| `test_ocr_digit_substitution[3_for_e__3ngine__t4]` | fail | 321 | AssertionError: Expected issue_detected for '3ngine' in: Researchers published a comprehensive study about the 3ngine |
| `test_ocr_digit_substitution[3_for_e__3ntire__t1]` | fail | 259 | AssertionError: Expected issue_detected for '3ntire' in: The 3ntire was thoroughly discussed at the annual conference |
| `test_ocr_digit_substitution[3_for_e__3ntire__t8]` | fail | 261 | AssertionError: Expected issue_detected for '3ntire' in: Experts recommended paying closer attention to the 3ntire |
| `test_ocr_digit_substitution[3_for_e__3nvironment__t5]` | fail | 485 | AssertionError: Expected issue_detected for '3nvironment' in: The organization focused its efforts on improving the 3nvironment |
| `test_ocr_digit_substitution[3_for_e__3pisode__t2]` | fail | 323 | AssertionError: Expected issue_detected for '3pisode' in: Many people considered the 3pisode to be extremely important |
| `test_ocr_digit_substitution[3_for_e__3pisode__t9]` | fail | 320 | AssertionError: Expected issue_detected for '3pisode' in: The recent developments regarding the 3pisode surprised everyone |
| `test_ocr_digit_substitution[3_for_e__3qual__t6]` | fail | 324 | AssertionError: Expected issue_detected for '3qual' in: After the review, the 3qual was modified to meet new standards |
| `test_ocr_digit_substitution[3_for_e__3scape__t3]` | fail | 189 | AssertionError: Expected issue_detected for '3scape' in: The government announced changes to the 3scape policy |
| `test_ocr_digit_substitution[3_for_e__3scape__t10]` | fail | 255 | AssertionError: Expected issue_detected for '3scape' in: Students were required to understand the 3scape before proceeding |
| `test_ocr_digit_substitution[3_for_e__3stablish__t7]` | fail | 395 | AssertionError: Expected issue_detected for '3stablish' in: The 3stablish significantly impacted the outcome of the project |
| `test_ocr_digit_substitution[3_for_e__3vent__t4]` | fail | 255 | AssertionError: Expected issue_detected for '3vent' in: Researchers published a comprehensive study about the 3vent |
| `test_ocr_digit_substitution[3_for_e__3very__t1]` | fail | 189 | AssertionError: Expected issue_detected for '3very' in: The 3very was thoroughly discussed at the annual conference |
| `test_ocr_digit_substitution[3_for_e__3very__t8]` | fail | 187 | AssertionError: Expected issue_detected for '3very' in: Experts recommended paying closer attention to the 3very |
| `test_ocr_digit_substitution[3_for_e__3vidence__t5]` | fail | 451 | AssertionError: Expected issue_detected for '3vidence' in: The organization focused its efforts on improving the 3vidence |
| `test_ocr_digit_substitution[3_for_e__3xample__t2]` | fail | 260 | AssertionError: Expected issue_detected for '3xample' in: Many people considered the 3xample to be extremely important |
| `test_ocr_digit_substitution[3_for_e__3xample__t9]` | fail | 260 | AssertionError: Expected issue_detected for '3xample' in: The recent developments regarding the 3xample surprised everyone |
| `test_ocr_digit_substitution[3_for_e__3xcellent__t6]` | fail | 328 | AssertionError: Expected issue_detected for '3xcellent' in: After the review, the 3xcellent was modified to meet new standards |
| `test_ocr_digit_substitution[3_for_e__3xercise__t3]` | fail | 263 | AssertionError: Expected issue_detected for '3xercise' in: The government announced changes to the 3xercise policy |
| `test_ocr_digit_substitution[3_for_e__3xercise__t10]` | fail | 318 | AssertionError: Expected issue_detected for '3xercise' in: Students were required to understand the 3xercise before proceeding |
| `test_ocr_digit_substitution[3_for_e__3xpect__t7]` | fail | 319 | AssertionError: Expected issue_detected for '3xpect' in: The 3xpect significantly impacted the outcome of the project |
| `test_ocr_digit_substitution[3_for_e__3xpense__t4]` | fail | 260 | AssertionError: Expected issue_detected for '3xpense' in: Researchers published a comprehensive study about the 3xpense |
| `test_ocr_digit_substitution[3_for_e__3xperience__t1]` | fail | 256 | AssertionError: Expected issue_detected for '3xperience' in: The 3xperience was thoroughly discussed at the annual conference |
| `test_ocr_digit_substitution[3_for_e__3xperience__t8]` | fail | 253 | AssertionError: Expected issue_detected for '3xperience' in: Experts recommended paying closer attention to the 3xperience |
| `test_ocr_digit_substitution[3_for_e__3xperiment__t5]` | fail | 450 | AssertionError: Expected issue_detected for '3xperiment' in: The organization focused its efforts on improving the 3xperiment |
| `test_ocr_digit_substitution[3_for_e__3xpert__t2]` | fail | 267 | AssertionError: Expected issue_detected for '3xpert' in: Many people considered the 3xpert to be extremely important |
| `test_ocr_digit_substitution[3_for_e__3xpert__t9]` | fail | 258 | AssertionError: Expected issue_detected for '3xpert' in: The recent developments regarding the 3xpert surprised everyone |
| `test_ocr_digit_substitution[3_for_e__3xpress__t6]` | fail | 334 | AssertionError: Expected issue_detected for '3xpress' in: After the review, the 3xpress was modified to meet new standards |
| `test_ocr_digit_substitution[3_for_e__3xtend__t3]` | fail | 258 | AssertionError: Expected issue_detected for '3xtend' in: The government announced changes to the 3xtend policy |
| `test_ocr_digit_substitution[3_for_e__3xtend__t10]` | fail | 274 | AssertionError: Expected issue_detected for '3xtend' in: Students were required to understand the 3xtend before proceeding |
| `test_ocr_digit_substitution[3_for_e__3xtreme__t7]` | fail | 479 | AssertionError: Expected issue_detected for '3xtreme' in: The 3xtreme significantly impacted the outcome of the project |
| `test_ocr_digit_substitution[3_for_e__f3deral__t4]` | fail | 259 | AssertionError: Expected issue_detected for 'f3deral' in: Researchers published a comprehensive study about the f3deral |
| `test_ocr_digit_substitution[3_for_e__financ3__t1]` | fail | 194 | AssertionError: Expected issue_detected for 'financ3' in: The financ3 was thoroughly discussed at the annual conference |
| `test_ocr_digit_substitution[3_for_e__financ3__t8]` | fail | 267 | AssertionError: Expected issue_detected for 'financ3' in: Experts recommended paying closer attention to the financ3 |
| `test_ocr_digit_substitution[3_for_e__fr3edom__t5]` | fail | 401 | AssertionError: Expected issue_detected for 'fr3edom' in: The organization focused its efforts on improving the fr3edom |
| `test_ocr_digit_substitution[3_for_e__fr3quent__t2]` | fail | 249 | AssertionError: Expected issue_detected for 'fr3quent' in: Many people considered the fr3quent to be extremely important |
| `test_ocr_digit_substitution[3_for_e__fr3quent__t9]` | fail | 272 | AssertionError: Expected issue_detected for 'fr3quent' in: The recent developments regarding the fr3quent surprised everyone |
| `test_ocr_digit_substitution[3_for_e__g3neral__t6]` | fail | 334 | AssertionError: Expected issue_detected for 'g3neral' in: After the review, the g3neral was modified to meet new standards |
| `test_ocr_digit_substitution[3_for_e__h3ritage__t3]` | fail | 271 | AssertionError: Expected issue_detected for 'h3ritage' in: The government announced changes to the h3ritage policy |
| `test_ocr_digit_substitution[3_for_e__h3ritage__t10]` | fail | 330 | AssertionError: Expected issue_detected for 'h3ritage' in: Students were required to understand the h3ritage before proceeding |
| `test_ocr_digit_substitution[3_for_e__incr3ase__t7]` | fail | 393 | AssertionError: Expected issue_detected for 'incr3ase' in: The incr3ase significantly impacted the outcome of the project |
| `test_ocr_digit_substitution[3_for_e__int3rest__t4]` | fail | 327 | AssertionError: Expected issue_detected for 'int3rest' in: Researchers published a comprehensive study about the int3rest |
| `test_ocr_digit_substitution[3_for_e__int3rnet__t1]` | fail | 360 | AssertionError: Expected issue_detected for 'int3rnet' in: The int3rnet was thoroughly discussed at the annual conference |
| `test_ocr_digit_substitution[3_for_e__int3rnet__t8]` | fail | 333 | AssertionError: Expected issue_detected for 'int3rnet' in: Experts recommended paying closer attention to the int3rnet |
| `test_ocr_digit_substitution[3_for_e__l3ader__t5]` | fail | 456 | AssertionError: Expected issue_detected for 'l3ader' in: The organization focused its efforts on improving the l3ader |
| `test_ocr_digit_substitution[3_for_e__m3asure__t2]` | fail | 267 | AssertionError: Expected issue_detected for 'm3asure' in: Many people considered the m3asure to be extremely important |
| `test_ocr_digit_substitution[3_for_e__m3asure__t9]` | fail | 266 | AssertionError: Expected issue_detected for 'm3asure' in: The recent developments regarding the m3asure surprised everyone |
| `test_ocr_digit_substitution[3_for_e__m3mber__t6]` | fail | 330 | AssertionError: Expected issue_detected for 'm3mber' in: After the review, the m3mber was modified to meet new standards |
| `test_ocr_digit_substitution[3_for_e__m3ssage__t3]` | fail | 186 | AssertionError: Expected issue_detected for 'm3ssage' in: The government announced changes to the m3ssage policy |
| `test_ocr_digit_substitution[3_for_e__m3ssage__t10]` | fail | 258 | AssertionError: Expected issue_detected for 'm3ssage' in: Students were required to understand the m3ssage before proceeding |
| `test_ocr_digit_substitution[3_for_e__m3thod__t7]` | fail | 325 | AssertionError: Expected issue_detected for 'm3thod' in: The m3thod significantly impacted the outcome of the project |
| `test_ocr_digit_substitution[3_for_e__n3twork__t4]` | fail | 245 | AssertionError: Expected issue_detected for 'n3twork' in: Researchers published a comprehensive study about the n3twork |
| `test_ocr_digit_substitution[3_for_e__n3ver__t1]` | fail | 177 | AssertionError: Expected issue_detected for 'n3ver' in: The n3ver was thoroughly discussed at the annual conference |
| `test_ocr_digit_substitution[3_for_e__n3ver__t8]` | fail | 188 | AssertionError: Expected issue_detected for 'n3ver' in: Experts recommended paying closer attention to the n3ver |
| `test_ocr_digit_substitution[3_for_e__p3rfect__t5]` | fail | 364 | AssertionError: Expected issue_detected for 'p3rfect' in: The organization focused its efforts on improving the p3rfect |
| `test_ocr_digit_substitution[3_for_e__p3rson__t2]` | fail | 257 | AssertionError: Expected issue_detected for 'p3rson' in: Many people considered the p3rson to be extremely important |
| `test_ocr_digit_substitution[3_for_e__p3rson__t9]` | fail | 257 | AssertionError: Expected issue_detected for 'p3rson' in: The recent developments regarding the p3rson surprised everyone |
| `test_ocr_digit_substitution[3_for_e__pr3serve__t6]` | fail | 320 | AssertionError: Expected issue_detected for 'pr3serve' in: After the review, the pr3serve was modified to meet new standards |
| `test_ocr_digit_substitution[3_for_e__pr3vent__t3]` | fail | 188 | AssertionError: Expected issue_detected for 'pr3vent' in: The government announced changes to the pr3vent policy |
| `test_ocr_digit_substitution[3_for_e__pr3vent__t10]` | fail | 238 | AssertionError: Expected issue_detected for 'pr3vent' in: Students were required to understand the pr3vent before proceeding |
| `test_ocr_digit_substitution[3_for_e__r3cent__t7]` | fail | 335 | AssertionError: Expected issue_detected for 'r3cent' in: The r3cent significantly impacted the outcome of the project |
| `test_ocr_digit_substitution[3_for_e__r3member__t4]` | fail | 253 | AssertionError: Expected issue_detected for 'r3member' in: Researchers published a comprehensive study about the r3member |
| `test_ocr_digit_substitution[3_for_e__r3search__t1]` | fail | 188 | AssertionError: Expected issue_detected for 'r3search' in: The r3search was thoroughly discussed at the annual conference |
| `test_ocr_digit_substitution[3_for_e__r3search__t8]` | fail | 189 | AssertionError: Expected issue_detected for 'r3search' in: Experts recommended paying closer attention to the r3search |
| `test_ocr_digit_substitution[3_for_e__r3source__t5]` | fail | 389 | AssertionError: Expected issue_detected for 'r3source' in: The organization focused its efforts on improving the r3source |
| `test_ocr_digit_substitution[7_for_t__7able__t2]` | fail | 185 | AssertionError: Expected issue_detected for '7able' in: Visitors were impressed by the remarkable 7able on display |
| `test_ocr_digit_substitution[7_for_t__7able__t9]` | fail | 189 | AssertionError: Expected issue_detected for '7able' in: The 7able played a pivotal role in shaping the community |
| `test_ocr_digit_substitution[7_for_t__7alent__t6]` | fail | 212 | AssertionError: Expected issue_detected for '7alent' in: Historians traced the origins of the 7alent to ancient times |
| `test_ocr_digit_substitution[7_for_t__7arget__t3]` | fail | 256 | AssertionError: Expected issue_detected for '7arget' in: The professor lectured extensively about the 7arget topic |
| `test_ocr_digit_substitution[7_for_t__7arget__t10]` | fail | 261 | AssertionError: Expected issue_detected for '7arget' in: Engineers redesigned the 7arget to improve overall efficiency |
| `test_ocr_digit_substitution[7_for_t__7aste__t7]` | fail | 119 | AssertionError: Expected issue_detected for '7aste' in: The documentary explored every aspect of the 7aste in depth |
| `test_ocr_digit_substitution[7_for_t__7eacher__t4]` | fail | 521 | AssertionError: Expected issue_detected for '7eacher' in: Local authorities invested heavily in modernizing the 7eacher |
| `test_ocr_digit_substitution[7_for_t__7echnology__t1]` | fail | 382 | AssertionError: Expected issue_detected for '7echnology' in: The 7echnology was established decades ago in the heart of the city |
| `test_ocr_digit_substitution[7_for_t__7echnology__t8]` | fail | 420 | AssertionError: Expected issue_detected for '7echnology' in: Funding for the 7echnology was approved by the legislative body |
| `test_ocr_digit_substitution[7_for_t__7emperature__t5]` | fail | 258 | AssertionError: Expected issue_detected for '7emperature' in: The 7emperature received an award for excellence this year |
| `test_ocr_digit_substitution[7_for_t__7emple__t2]` | fail | 254 | AssertionError: Expected issue_detected for '7emple' in: Visitors were impressed by the remarkable 7emple on display |
| `test_ocr_digit_substitution[7_for_t__7emple__t9]` | fail | 190 | AssertionError: Expected issue_detected for '7emple' in: The 7emple played a pivotal role in shaping the community |
| `test_ocr_digit_substitution[7_for_t__7erminal__t6]` | fail | 254 | AssertionError: Expected issue_detected for '7erminal' in: Historians traced the origins of the 7erminal to ancient times |
| `test_ocr_digit_substitution[7_for_t__7erritory__t3]` | fail | 349 | AssertionError: Missing suggestion 'territory' for '7erritory' |
| `test_ocr_digit_substitution[7_for_t__7erritory__t10]` | fail | 348 | AssertionError: Expected issue_detected for '7erritory' in: Engineers redesigned the 7erritory to improve overall efficiency |
| `test_ocr_digit_substitution[7_for_t__7est__t7]` | fail | 121 | AssertionError: Expected issue_detected for '7est' in: The documentary explored every aspect of the 7est in depth |
| `test_ocr_digit_substitution[7_for_t__7heater__t4]` | fail | 634 | AssertionError: Expected issue_detected for '7heater' in: Local authorities invested heavily in modernizing the 7heater |
| `test_ocr_digit_substitution[7_for_t__7heory__t1]` | fail | 261 | AssertionError: Expected issue_detected for '7heory' in: The 7heory was established decades ago in the heart of the city |
| `test_ocr_digit_substitution[7_for_t__7heory__t8]` | fail | 319 | AssertionError: Expected issue_detected for '7heory' in: Funding for the 7heory was approved by the legislative body |
| `test_ocr_digit_substitution[7_for_t__7herapy__t5]` | fail | 257 | AssertionError: Expected issue_detected for '7herapy' in: The 7herapy received an award for excellence this year |
| `test_ocr_digit_substitution[7_for_t__7hought__t2]` | fail | 260 | AssertionError: Expected issue_detected for '7hought' in: Visitors were impressed by the remarkable 7hought on display |
| `test_ocr_digit_substitution[7_for_t__7hought__t9]` | fail | 188 | AssertionError: Expected issue_detected for '7hought' in: The 7hought played a pivotal role in shaping the community |
| `test_ocr_digit_substitution[7_for_t__7itle__t6]` | fail | 254 | AssertionError: Expected issue_detected for '7itle' in: Historians traced the origins of the 7itle to ancient times |
| `test_ocr_digit_substitution[7_for_t__7ogether__t3]` | fail | 260 | AssertionError: Expected issue_detected for '7ogether' in: The professor lectured extensively about the 7ogether topic |
| `test_ocr_digit_substitution[7_for_t__7ogether__t10]` | fail | 238 | AssertionError: Expected issue_detected for '7ogether' in: Engineers redesigned the 7ogether to improve overall efficiency |
| `test_ocr_digit_substitution[7_for_t__7omorrow__t7]` | fail | 203 | AssertionError: Expected issue_detected for '7omorrow' in: The documentary explored every aspect of the 7omorrow in depth |
| `test_ocr_digit_substitution[7_for_t__7otal__t4]` | fail | 530 | AssertionError: Expected issue_detected for '7otal' in: Local authorities invested heavily in modernizing the 7otal |
| `test_ocr_digit_substitution[7_for_t__7ouch__t1]` | fail | 188 | AssertionError: Expected issue_detected for '7ouch' in: The 7ouch was established decades ago in the heart of the city |
| `test_ocr_digit_substitution[7_for_t__7ouch__t8]` | fail | 333 | AssertionError: Expected issue_detected for '7ouch' in: Funding for the 7ouch was approved by the legislative body |
| `test_ocr_digit_substitution[7_for_t__7ourist__t5]` | fail | 319 | AssertionError: Expected issue_detected for '7ourist' in: The 7ourist received an award for excellence this year |
| `test_ocr_digit_substitution[7_for_t__7ower__t2]` | fail | 254 | AssertionError: Expected issue_detected for '7ower' in: Visitors were impressed by the remarkable 7ower on display |
| `test_ocr_digit_substitution[7_for_t__7ower__t9]` | fail | 169 | AssertionError: Expected issue_detected for '7ower' in: The 7ower played a pivotal role in shaping the community |
| `test_ocr_digit_substitution[7_for_t__7radition__t6]` | fail | 381 | AssertionError: Expected issue_detected for '7radition' in: Historians traced the origins of the 7radition to ancient times |
| `test_ocr_digit_substitution[7_for_t__7raffic__t3]` | fail | 383 | AssertionError: Missing suggestion 'traffic' for '7raffic' |
| `test_ocr_digit_substitution[7_for_t__7raffic__t10]` | fail | 253 | AssertionError: Expected issue_detected for '7raffic' in: Engineers redesigned the 7raffic to improve overall efficiency |
| `test_ocr_digit_substitution[7_for_t__7raining__t7]` | fail | 254 | AssertionError: Expected issue_detected for '7raining' in: The documentary explored every aspect of the 7raining in depth |
| `test_ocr_digit_substitution[7_for_t__7ransfer__t4]` | fail | 515 | AssertionError: Expected issue_detected for '7ransfer' in: Local authorities invested heavily in modernizing the 7ransfer |
| `test_ocr_digit_substitution[7_for_t__7ransport__t1]` | fail | 190 | AssertionError: Expected issue_detected for '7ransport' in: The 7ransport was established decades ago in the heart of the city |
| `test_ocr_digit_substitution[7_for_t__7ransport__t8]` | fail | 327 | AssertionError: Expected issue_detected for '7ransport' in: Funding for the 7ransport was approved by the legislative body |
| `test_ocr_digit_substitution[7_for_t__7ravel__t5]` | fail | 267 | AssertionError: Expected issue_detected for '7ravel' in: The 7ravel received an award for excellence this year |
| `test_ocr_digit_substitution[7_for_t__7reatment__t2]` | fail | 187 | AssertionError: Expected issue_detected for '7reatment' in: Visitors were impressed by the remarkable 7reatment on display |
| `test_ocr_digit_substitution[7_for_t__7reatment__t9]` | fail | 252 | AssertionError: Expected issue_detected for '7reatment' in: The 7reatment played a pivotal role in shaping the community |
| `test_ocr_digit_substitution[7_for_t__7reaty__t6]` | fail | 188 | AssertionError: Expected issue_detected for '7reaty' in: Historians traced the origins of the 7reaty to ancient times |
| `test_ocr_digit_substitution[7_for_t__7rend__t3]` | fail | 255 | AssertionError: Expected issue_detected for '7rend' in: The professor lectured extensively about the 7rend topic |
| `test_ocr_digit_substitution[7_for_t__7rend__t10]` | fail | 254 | AssertionError: Expected issue_detected for '7rend' in: Engineers redesigned the 7rend to improve overall efficiency |
| `test_ocr_digit_substitution[7_for_t__7rial__t7]` | fail | 196 | AssertionError: Expected issue_detected for '7rial' in: The documentary explored every aspect of the 7rial in depth |
| `test_ocr_digit_substitution[7_for_t__7ribute__t4]` | fail | 595 | AssertionError: Expected issue_detected for '7ribute' in: Local authorities invested heavily in modernizing the 7ribute |
| `test_ocr_digit_substitution[7_for_t__7rouble__t1]` | fail | 193 | AssertionError: Expected issue_detected for '7rouble' in: The 7rouble was established decades ago in the heart of the city |
| `test_ocr_digit_substitution[7_for_t__7rouble__t8]` | fail | 321 | AssertionError: Expected issue_detected for '7rouble' in: Funding for the 7rouble was approved by the legislative body |
| `test_ocr_digit_substitution[7_for_t__7rust__t5]` | fail | 234 | AssertionError: Expected issue_detected for '7rust' in: The 7rust received an award for excellence this year |
| `test_ocr_digit_substitution[7_for_t__7ruth__t2]` | fail | 189 | AssertionError: Expected issue_detected for '7ruth' in: Visitors were impressed by the remarkable 7ruth on display |
| `test_ocr_digit_substitution[7_for_t__7ruth__t9]` | fail | 171 | AssertionError: Expected issue_detected for '7ruth' in: The 7ruth played a pivotal role in shaping the community |
| `test_ocr_digit_substitution[7_for_t__7unnel__t6]` | fail | 191 | AssertionError: Expected issue_detected for '7unnel' in: Historians traced the origins of the 7unnel to ancient times |
| `test_ocr_digit_substitution[7_for_t__ba7tle__t3]` | fail | 257 | AssertionError: Expected issue_detected for 'ba7tle' in: The professor lectured extensively about the ba7tle topic |
| `test_ocr_digit_substitution[7_for_t__ba7tle__t10]` | fail | 257 | AssertionError: Expected issue_detected for 'ba7tle' in: Engineers redesigned the ba7tle to improve overall efficiency |
| `test_ocr_digit_substitution[7_for_t__be7ter__t7]` | fail | 106 | AssertionError: Expected issue_detected for 'be7ter' in: The documentary explored every aspect of the be7ter in depth |
| `test_ocr_digit_substitution[7_for_t__bo7tom__t4]` | fail | 525 | AssertionError: Expected issue_detected for 'bo7tom' in: Local authorities invested heavily in modernizing the bo7tom |
| `test_ocr_digit_substitution[7_for_t__bu7ter__t1]` | fail | 205 | AssertionError: Expected issue_detected for 'bu7ter' in: The bu7ter was established decades ago in the heart of the city |
| `test_ocr_digit_substitution[7_for_t__bu7ter__t8]` | fail | 329 | AssertionError: Expected issue_detected for 'bu7ter' in: Funding for the bu7ter was approved by the legislative body |
| `test_ocr_digit_substitution[7_for_t__bu7ton__t5]` | fail | 251 | AssertionError: Expected issue_detected for 'bu7ton' in: The bu7ton received an award for excellence this year |
| `test_ocr_digit_substitution[7_for_t__cap7ain__t2]` | fail | 322 | AssertionError: Expected issue_detected for 'cap7ain' in: Visitors were impressed by the remarkable cap7ain on display |
| `test_ocr_digit_substitution[7_for_t__cap7ain__t9]` | fail | 322 | AssertionError: Expected issue_detected for 'cap7ain' in: The cap7ain played a pivotal role in shaping the community |
| `test_ocr_digit_substitution[7_for_t__car7oon__t6]` | fail | 195 | AssertionError: Expected issue_detected for 'car7oon' in: Historians traced the origins of the car7oon to ancient times |
| `test_ocr_digit_substitution[7_for_t__cas7le__t3]` | fail | 256 | AssertionError: Expected issue_detected for 'cas7le' in: The professor lectured extensively about the cas7le topic |
| `test_ocr_digit_substitution[7_for_t__cas7le__t10]` | fail | 252 | AssertionError: Expected issue_detected for 'cas7le' in: Engineers redesigned the cas7le to improve overall efficiency |
| `test_ocr_digit_substitution[7_for_t__ca7tle__t7]` | fail | 125 | AssertionError: Expected issue_detected for 'ca7tle' in: The documentary explored every aspect of the ca7tle in depth |
| `test_ocr_digit_substitution[7_for_t__cen7er__t4]` | fail | 498 | AssertionError: Expected issue_detected for 'cen7er' in: Local authorities invested heavily in modernizing the cen7er |
| `test_ocr_digit_substitution[7_for_t__chap7er__t1]` | fail | 190 | AssertionError: Expected issue_detected for 'chap7er' in: The chap7er was established decades ago in the heart of the city |
| `test_ocr_digit_substitution[7_for_t__chap7er__t8]` | fail | 321 | AssertionError: Expected issue_detected for 'chap7er' in: Funding for the chap7er was approved by the legislative body |
| `test_ocr_digit_substitution[7_for_t__con7ent__t5]` | fail | 269 | AssertionError: Expected issue_detected for 'con7ent' in: The con7ent received an award for excellence this year |
| `test_ocr_digit_substitution[7_for_t__con7ext__t2]` | fail | 196 | AssertionError: Expected issue_detected for 'con7ext' in: Visitors were impressed by the remarkable con7ext on display |
| `test_ocr_digit_substitution[7_for_t__con7ext__t9]` | fail | 280 | AssertionError: Expected issue_detected for 'con7ext' in: The con7ext played a pivotal role in shaping the community |
| `test_ocr_digit_substitution[7_for_t__con7rol__t6]` | fail | 186 | AssertionError: Expected issue_detected for 'con7rol' in: Historians traced the origins of the con7rol to ancient times |
| `test_ocr_digit_substitution[7_for_t__co7ton__t3]` | fail | 255 | AssertionError: Expected issue_detected for 'co7ton' in: The professor lectured extensively about the co7ton topic |
| `test_ocr_digit_substitution[7_for_t__co7ton__t10]` | fail | 395 | AssertionError: Expected issue_detected for 'co7ton' in: Engineers redesigned the co7ton to improve overall efficiency |
| `test_ocr_digit_substitution[7_for_t__coun7er__t7]` | fail | 179 | AssertionError: Missing suggestion 'counter' for 'coun7er' |
| `test_ocr_digit_substitution[7_for_t__coun7ry__t4]` | fail | 554 | AssertionError: Expected issue_detected for 'coun7ry' in: Local authorities invested heavily in modernizing the coun7ry |
| `test_ocr_digit_substitution[7_for_t__cus7om__t1]` | fail | 189 | AssertionError: Expected issue_detected for 'cus7om' in: The cus7om was established decades ago in the heart of the city |
| `test_ocr_digit_substitution[7_for_t__cus7om__t8]` | fail | 346 | AssertionError: Expected issue_detected for 'cus7om' in: Funding for the cus7om was approved by the legislative body |
| `test_ocr_digit_substitution[7_for_t__digi7al__t5]` | fail | 388 | AssertionError: Expected issue_detected for 'digi7al' in: The digi7al received an award for excellence this year |
| `test_ocr_digit_substitution[7_for_t__dis7ant__t2]` | fail | 335 | AssertionError: Expected issue_detected for 'dis7ant' in: Visitors were impressed by the remarkable dis7ant on display |
| `test_ocr_digit_substitution[7_for_t__dis7ant__t9]` | fail | 329 | AssertionError: Expected issue_detected for 'dis7ant' in: The dis7ant played a pivotal role in shaping the community |
| `test_ocr_digit_substitution[7_for_t__eas7ern__t6]` | fail | 254 | AssertionError: Missing suggestion 'eastern' for 'eas7ern' |
| `test_ocr_digit_substitution[7_for_t__fif7een__t3]` | fail | 331 | AssertionError: Expected issue_detected for 'fif7een' in: The professor lectured extensively about the fif7een topic |
| `test_ocr_digit_substitution[7_for_t__fif7een__t10]` | fail | 501 | AssertionError: Missing suggestion 'fifteen' for 'fif7een' |
| `test_ocr_digit_substitution[7_for_t__gen7le__t7]` | fail | 122 | AssertionError: Expected issue_detected for 'gen7le' in: The documentary explored every aspect of the gen7le in depth |
| `test_ocr_char_confusion[The changes to the rnanner affected thousands of residents-rnanner-manner-rn_m_manner_t3]` | fail | 190 | AssertionError: [rn_m_manner_t3] Should detect 'rnanner' |
| `test_ocr_char_confusion[The perrnanent issued a formal statement regarding the matter-perrnanent-permanent-rn_m_permanent_t1]` | fail | 271 | AssertionError: [rn_m_permanent_t1] Should detect 'perrnanent' |
| `test_ocr_char_confusion[The changes to the tournarment affected thousands of residents-tournarment-tournament-rn_m_tournament_t3]` | fail | 187 | AssertionError: [rn_m_tournament_t3] Should detect 'tournarment' |
| `test_ocr_char_confusion[The new policy regarding the environrnent takes effect immediately-environrnent-environment-rn_m_environment_t5]` | fail | 328 | AssertionError: [rn_m_environment_t5] Should detect 'environrnent' |
| `test_ocr_char_confusion[Citizens were asked to review the developrnent before the vote-developrnent-development-rn_m_development_t2]` | fail | 191 | AssertionError: [rn_m_development_t2] Should detect 'developrnent' |
| `test_ocr_char_confusion[A detailed analysis of the fundarmental was published last month-fundarmental-fundamental-rn_m_fundamental_t4]` | fail | 313 | AssertionError: [rn_m_fundamental_t4] Should detect 'fundarmental' |
| `test_ocr_char_confusion[The monurnent issued a formal statement regarding the matter-monurnent-monument-rn_m_monument_t1]` | fail | 256 | AssertionError: [rn_m_monument_t1] Should detect 'monurnent' |
| `test_ocr_char_confusion[The changes to the rnoment affected thousands of residents-rnoment-moment-rn_m_moment_t3]` | fail | 197 | AssertionError: [rn_m_moment_t3] Should detect 'rnoment' |
| `test_ocr_char_confusion[The new policy regarding the norrnal takes effect immediately-norrnal-normal-rn_m_normal_t5]` | fail | 367 | AssertionError: [rn_m_normal_t5] Should detect 'norrnal' |
| `test_ocr_char_confusion[Citizens were asked to review the crirninal before the vote-crirninal-criminal-rn_m_criminal_t2]` | fail | 301 | AssertionError: [rn_m_criminal_t2] Should detect 'crirninal' |
| `test_ocr_char_confusion[The forrnal issued a formal statement regarding the matter-forrnal-formal-rn_m_formal_t1]` | fail | 260 | AssertionError: [rn_m_formal_t1] Should detect 'forrnal' |
| `test_ocr_char_confusion[The changes to the rnental affected thousands of residents-rnental-mental-rn_m_mental_t3]` | fail | 174 | AssertionError: [rn_m_mental_t3] Should detect 'rnental' |
| `test_ocr_char_confusion[The new policy regarding the rernoval takes effect immediately-rernoval-removal-rn_m_removal_t5]` | fail | 254 | AssertionError: [rn_m_removal_t5] Should detect 'rernoval' |
| `test_ocr_char_confusion[Citizens were asked to review the rnineral before the vote-rnineral-mineral-rn_m_mineral_t2]` | fail | 254 | AssertionError: [rn_m_mineral_t2] Should detect 'rnineral' |
| `test_ocr_char_confusion[A detailed analysis of the therrnal was published last month-therrnal-thermal-rn_m_thermal_t4]` | fail | 233 | AssertionError: [rn_m_thermal_t4] Should detect 'therrnal' |
| `test_ocr_char_confusion[The nurnerical issued a formal statement regarding the matter-nurnerical-numerical-rn_m_numerical_t1]` | fail | 328 | AssertionError: [rn_m_numerical_t1] Should detect 'nurnerical' |
| `test_ocr_char_confusion[The changes to the experirnental affected thousands of residents-experirnental-experimental-rn_m_experimental_t3]` | fail | 261 | AssertionError: [rn_m_experimental_t3] Should detect 'experirnental' |
| `test_ocr_char_confusion[The new policy regarding the elernent takes effect immediately-elernent-element-rn_m_element_t5]` | fail | 382 | AssertionError: [rn_m_element_t5] Should detect 'elernent' |
| `test_ocr_char_confusion[They decided to dedare the findings from the public record-dedare-declare-cl_d_declare_t2]` | fail | 435 | AssertionError: [cl_d_declare_t2] Should detect 'dedare' |
| `test_ocr_char_confusion[Experts attempted to exdude the source of the discrepancy-exdude-exclude-cl_d_exclude_t4]` | fail | 190 | AssertionError: [cl_d_exclude_t4] Should detect 'exdude' |
| `test_ocr_char_confusion[The report was designed to redaim all relevant information-redaim-reclaim-cl_d_reclaim_t1]` | fail | 252 | AssertionError: [cl_d_reclaim_t1] Should detect 'redaim' |
| `test_ocr_char_confusion[The committee voted to dedine the new provisions-dedine-decline-cl_d_decline_t3]` | fail | 367 | AssertionError: [cl_d_decline_t3] Should detect 'dedine' |
| `test_ocr_char_confusion[The document was meant to disdose the complete set of rules-disdose-disclose-cl_d_disclose_t5]` | fail | 168 | AssertionError: [cl_d_disclose_t5] Should detect 'disdose' |
| `test_ocr_char_confusion[They decided to prodaim the findings from the public record-prodaim-proclaim-cl_d_proclaim_t2]` | fail | 470 | AssertionError: [cl_d_proclaim_t2] Should detect 'prodaim' |
| `test_ocr_char_confusion[Experts attempted to addaim the source of the discrepancy-addaim-acclaim-cl_d_acclaim_t4]` | fail | 253 | AssertionError: [cl_d_acclaim_t4] Should detect 'addaim' |
| `test_ocr_char_confusion[The report was designed to reduse all relevant information-reduse-recluse-cl_d_recluse_t1]` | fail | 169 | AssertionError: [cl_d_recluse_t1] Should detect 'reduse' |
| `test_ocr_char_confusion[The committee voted to nudear the new provisions-nudear-nuclear-cl_d_nuclear_t3]` | fail | 297 | AssertionError: [cl_d_nuclear_t3] Should detect 'nudear' |
| `test_ocr_char_confusion[The document was meant to cirdular the complete set of rules-cirdular-circular-cl_d_circular_t5]` | fail | 192 | AssertionError: [cl_d_circular_t5] Should detect 'cirdular' |
| `test_ocr_char_confusion[They decided to spectadular the findings from the public record-spectadular-spectacular-cl_d_spectacular_t2]` | fail | 386 | AssertionError: [cl_d_spectacular_t2] Should detect 'spectadular' |
| `test_ocr_char_confusion[Experts attempted to moledular the source of the discrepancy-moledular-molecular-cl_d_molecular_t4]` | fail | 170 | AssertionError: [cl_d_molecular_t4] Should detect 'moledular' |
| `test_ocr_char_confusion[The report was designed to sedular all relevant information-sedular-secular-cl_d_secular_t1]` | fail | 169 | AssertionError: [cl_d_secular_t1] Should detect 'sedular' |
| `test_ocr_char_confusion[The committee voted to artide the new provisions-artide-article-cl_d_article_t3]` | fail | 415 | AssertionError: [cl_d_article_t3] Should detect 'artide' |
| `test_ocr_char_confusion[The document was meant to vehicde the complete set of rules-vehicde-vehicle-cl_d_vehicle_t5]` | fail | 199 | AssertionError: [cl_d_vehicle_t5] Should detect 'vehicde' |
| `test_ocr_char_confusion[They decided to obstade the findings from the public record-obstade-obstacle-cl_d_obstacle_t2]` | fail | 382 | AssertionError: [cl_d_obstacle_t2] Should detect 'obstade' |
| `test_ocr_char_confusion[Experts attempted to chronide the source of the discrepancy-chronide-chronicle-cl_d_chronicle_t4]` | fail | 253 | AssertionError: [cl_d_chronicle_t4] Should detect 'chronide' |
| `test_ocr_char_confusion[The report was designed to orade all relevant information-orade-oracle-cl_d_oracle_t1]` | fail | 190 | AssertionError: [cl_d_oracle_t1] Should detect 'orade' |
| `test_ocr_char_confusion[The committee voted to spectade the new provisions-spectade-spectacle-cl_d_spectacle_t3]` | fail | 345 | AssertionError: [cl_d_spectacle_t3] Should detect 'spectade' |
| `test_ocr_char_confusion[The document was meant to partide the complete set of rules-partide-particle-cl_d_particle_t5]` | fail | 198 | AssertionError: [cl_d_particle_t5] Should detect 'partide' |
| `test_ocr_char_confusion[The new IittIe was added to the system database-IittIe-little-li_little_t1]` | fail | 235 | AssertionError: [li_little_t1] Missing correction 'little' |
| `test_ocr_char_confusion[The report failed to fmd any significant improvements-fmd-find-fi_find_t3]` | fail | 274 | AssertionError: [fi_find_t3] Should detect 'fmd' |
| `test_ocr_char_confusion[The committee planned to ftre the budget before year end-ftre-fire-fi_fire_t5]` | fail | 192 | AssertionError: [fi_fire_t5] Should detect 'ftre' |
| `test_ocr_char_confusion[Officials agreed to ftll the ongoing investigation-ftll-fill-fi_fill_t2]` | fail | 191 | AssertionError: [fi_fill_t2] Should detect 'ftll' |
| `test_ocr_char_confusion[Researchers hoped to ftlm new evidence in the study-ftlm-film-fi_film_t4]` | fail | 198 | AssertionError: [fi_film_t4] Should detect 'ftlm' |
| `test_ocr_char_confusion[The team managed to ftnance the correct answer quickly-ftnance-finance-fi_finance_t1]` | fail | 191 | AssertionError: [fi_finance_t1] Should detect 'ftnance' |
| `test_ocr_char_confusion[The report failed to ftnger any significant improvements-ftnger-finger-fi_finger_t3]` | fail | 387 | AssertionError: [fi_finger_t3] Should detect 'ftnger' |
| `test_ocr_char_confusion[The committee planned to ftmsh the budget before year end-ftmsh-finish-fi_finish_t5]` | fail | 188 | AssertionError: [fi_finish_t5] Should detect 'ftmsh' |
| `test_ocr_char_confusion[Officials agreed to ftrst the ongoing investigation-ftrst-first-fi_first_t2]` | fail | 322 | AssertionError: [fi_first_t2] Should detect 'ftrst' |
| `test_ocr_char_confusion[Researchers hoped to ftve new evidence in the study-ftve-five-fi_five_t4]` | fail | 189 | AssertionError: [fi_five_t4] Should detect 'ftve' |
| `test_ocr_char_confusion[The team managed to ftght the correct answer quickly-ftght-fight-fi_fight_t1]` | fail | 189 | AssertionError: [fi_fight_t1] Should detect 'ftght' |
| `test_ocr_char_confusion[The report failed to ftgure any significant improvements-ftgure-figure-fi_figure_t3]` | fail | 365 | AssertionError: [fi_figure_t3] Should detect 'ftgure' |
| `test_ocr_char_confusion[The committee planned to ftle the budget before year end-ftle-file-fi_file_t5]` | fail | 186 | AssertionError: [fi_file_t5] Should detect 'ftle' |
| `test_ocr_char_confusion[Officials agreed to ftne the ongoing investigation-ftne-fine-fi_fine_t2]` | fail | 326 | AssertionError: [fi_fine_t2] Should detect 'ftne' |
| `test_ocr_char_confusion[Researchers hoped to fttness new evidence in the study-fttness-fitness-fi_fitness_t4]` | fail | 190 | AssertionError: [fi_fitness_t4] Should detect 'fttness' |
| `test_ocr_char_confusion[The organization decided to hurnan its existing approach-hurnan-human-misc_human_t1]` | fail | 512 | AssertionError: [misc_human_t1] Should detect 'hurnan' |
| `test_ocr_char_confusion[Local authorities examined the burrn for regulatory compliance-burrn-burn-misc_burn_t3]` | fail | 329 | AssertionError: [misc_burn_t3] Should detect 'burrn' |
| `test_ocr_char_confusion[Stakeholders expressed confidence in the proposed warrn-warrn-warm-misc_warm_t5]` | fail | 266 | AssertionError: [misc_warm_t5] Should detect 'warrn' |
| `test_ocr_char_confusion[The alarrn was featured in the quarterly progress report-alarrn-alarm-misc_alarm_t2]` | fail | 122 | AssertionError: [misc_alarm_t2] Should detect 'alarrn' |
| `test_ocr_char_confusion[The charrn underwent extensive testing before deployment-charrn-charm-misc_charm_t4]` | fail | 275 | AssertionError: [misc_charm_t4] Should detect 'charrn' |
| `test_ocr_char_confusion[The organization decided to storrn its existing approach-storrn-storm-misc_storm_t1]` | fail | 546 | AssertionError: [misc_storm_t1] Should detect 'storrn' |
| `test_ocr_char_confusion[Local authorities examined the reforrn for regulatory compliance-reforrn-reform-misc_reform_t3]` | fail | 400 | AssertionError: [misc_reform_t3] Should detect 'reforrn' |
| `test_ocr_char_confusion[Stakeholders expressed confidence in the proposed platforrn-platforrn-platform-misc_platform_t5]` | fail | 252 | AssertionError: [misc_platform_t5] Should detect 'platforrn' |
| `test_ocr_char_confusion[The transforrn was featured in the quarterly progress report-transforrn-transform-misc_transform_t2]` | fail | 120 | AssertionError: [misc_transform_t2] Should detect 'transforrn' |
| `test_ocr_char_confusion[The perforrn underwent extensive testing before deployment-perforrn-perform-misc_perform_t4]` | fail | 290 | AssertionError: [misc_perform_t4] Should detect 'perforrn' |
| `test_ocr_char_confusion[The organization decided to confrrn its existing approach-confrrn-confirm-misc_confirm_t1]` | fail | 557 | AssertionError: [misc_confirm_t1] Should detect 'confrrn' |
| `test_ocr_char_confusion[Local authorities examined the affrrn for regulatory compliance-affrrn-affirm-misc_affirm_t3]` | fail | 347 | AssertionError: [misc_affirm_t3] Should detect 'affrrn' |
| `test_ocr_char_confusion[Stakeholders expressed confidence in the proposed worrn-worrn-worm-misc_worm_t5]` | fail | 264 | AssertionError: [misc_worm_t5] Should detect 'worrn' |
| `test_ocr_char_confusion[The forrn was featured in the quarterly progress report-forrn-form-misc_form_t2]` | fail | 129 | AssertionError: [misc_form_t2] Should detect 'forrn' |
| `test_ocr_char_confusion[The borrn underwent extensive testing before deployment-borrn-born-misc_born_t4]` | fail | 273 | AssertionError: [misc_born_t4] Should detect 'borrn' |
| `test_ocr_char_confusion[The organization decided to horrn its existing approach-horrn-horn-misc_horn_t1]` | fail | 541 | AssertionError: [misc_horn_t1] Should detect 'horrn' |
| `test_ocr_char_confusion[Local authorities examined the torrn for regulatory compliance-torrn-torn-misc_torn_t3]` | fail | 363 | AssertionError: [misc_torn_t3] Should detect 'torrn' |
| `test_ocr_char_confusion[Stakeholders expressed confidence in the proposed learrn-learrn-learn-misc_learn_t5]` | fail | 268 | AssertionError: [misc_learn_t5] Should detect 'learrn' |
| `test_ocr_char_confusion[The turrn was featured in the quarterly progress report-turrn-turn-misc_turn_t2]` | fail | 121 | AssertionError: [misc_turn_t2] Should detect 'turrn' |
| `test_ocr_char_confusion[The returrn underwent extensive testing before deployment-returrn-return-misc_return_t4]` | fail | 193 | AssertionError: [misc_return_t4] Should detect 'returrn' |
| `test_ocr_char_confusion[The organization decided to patterrn its existing approach-patterrn-pattern-misc_pattern_t1]` | fail | 489 | AssertionError: [misc_pattern_t1] Should detect 'patterrn' |
| `test_ocr_char_confusion[Local authorities examined the moderrn for regulatory compliance-moderrn-modern-misc_modern_t3]` | fail | 325 | AssertionError: [misc_modern_t3] Should detect 'moderrn' |
| `test_ocr_transposition[The committee found taht the evidence was compelling-taht-that-trans_that_t2]` | fail | 330 | AssertionError: [trans_that_t2] Should detect 'taht' |
| `test_ocr_transposition[The investigation revealed taht the original plan had flaws-taht-that-trans_that_t9]` | fail | 431 | AssertionError: [trans_that_t9] Should detect 'taht' |
| `test_ocr_transposition[It became clear tihs the project needed more resources-tihs-this-trans_this_t6]` | fail | 198 | AssertionError: [trans_this_t6] Should detect 'tihs' |
| `test_ocr_transposition[Everyone acknowledged wiht the results were significant-wiht-with-trans_with_t3]` | fail | 336 | AssertionError: [trans_with_t3] Should detect 'wiht' |
| `test_ocr_transposition[Experts concluded wiht the approach was fundamentally sound-wiht-with-trans_with_t10]` | fail | 227 | AssertionError: [trans_with_t10] Should detect 'wiht' |
| `test_ocr_transposition[The witness stated hvae the incident occurred at noon-hvae-have-trans_have_t7]` | fail | 327 | AssertionError: [trans_have_t7] Should detect 'hvae' |
| `test_ocr_transposition[Records show tehy the decision was made unanimously-tehy-they-trans_they_t4]` | fail | 331 | AssertionError: [trans_they_t4] Should detect 'tehy' |
| `test_ocr_transposition[Investigators confirmed bene the document was submitted to the review board-bene-been-trans_been_t1]` | fail | 391 | AssertionError: [trans_been_t1] Should detect 'bene' |
| `test_ocr_transposition[Officials determined bene the procedure was followed-bene-been-trans_been_t8]` | fail | 253 | AssertionError: [trans_been_t8] Should detect 'bene' |
| `test_ocr_transposition[The analysis confirmed thier the data supported the claim-thier-their-trans_their_t5]` | fail | 404 | AssertionError: [trans_their_t5] Should detect 'thier' |
| `test_ocr_transposition[The committee found abuot the evidence was compelling-abuot-about-trans_about_t2]` | fail | 330 | AssertionError: [trans_about_t2] Should detect 'abuot' |
| `test_ocr_transposition[The investigation revealed abuot the original plan had flaws-abuot-about-trans_about_t9]` | fail | 462 | AssertionError: [trans_about_t9] Should detect 'abuot' |
| `test_ocr_transposition[It became clear woudl the project needed more resources-woudl-would-trans_would_t6]` | fail | 122 | AssertionError: [trans_would_t6] Should detect 'woudl' |
| `test_ocr_transposition[Everyone acknowledged tehre the results were significant-tehre-there-trans_there_t3]` | fail | 259 | AssertionError: [trans_there_t3] Should detect 'tehre' |
| `test_ocr_transposition[Experts concluded tehre the approach was fundamentally sound-tehre-there-trans_there_t10]` | fail | 106 | AssertionError: [trans_there_t10] Should detect 'tehre' |
| `test_ocr_transposition[The witness stated whcih the incident occurred at noon-whcih-which-trans_which_t7]` | fail | 370 | AssertionError: [trans_which_t7] Should detect 'whcih' |
| `test_ocr_transposition[Records show coudl the decision was made unanimously-coudl-could-trans_could_t4]` | fail | 328 | AssertionError: [trans_could_t4] Should detect 'coudl' |
| `test_ocr_transposition[Investigators confirmed ohter the document was submitted to the review board-ohter-other-trans_other_t1]` | fail | 299 | AssertionError: [trans_other_t1] Should detect 'ohter' |
| `test_ocr_transposition[Officials determined ohter the procedure was followed-ohter-other-trans_other_t8]` | fail | 189 | AssertionError: [trans_other_t8] Should detect 'ohter' |
| `test_ocr_transposition[The analysis confirmed aftre the data supported the claim-aftre-after-trans_after_t5]` | fail | 331 | AssertionError: [trans_after_t5] Should detect 'aftre' |
| `test_ocr_transposition[The committee found thsoe the evidence was compelling-thsoe-those-trans_those_t2]` | fail | 319 | AssertionError: [trans_those_t2] Should detect 'thsoe' |
| `test_ocr_transposition[The investigation revealed thsoe the original plan had flaws-thsoe-those-trans_those_t9]` | fail | 380 | AssertionError: [trans_those_t9] Should detect 'thsoe' |
| `test_ocr_transposition[It became clear wehre the project needed more resources-wehre-where-trans_where_t6]` | fail | 119 | AssertionError: [trans_where_t6] Should detect 'wehre' |
| `test_ocr_transposition[Everyone acknowledged shoudl the results were significant-shoudl-should-trans_should_t3]` | fail | 265 | AssertionError: [trans_should_t3] Should detect 'shoudl' |
| `test_ocr_transposition[Experts concluded shoudl the approach was fundamentally sound-shoudl-should-trans_should_t10]` | fail | 123 | AssertionError: [trans_should_t10] Should detect 'shoudl' |
| `test_ocr_transposition[The witness stated mihgt the incident occurred at noon-mihgt-might-trans_might_t7]` | fail | 370 | AssertionError: [trans_might_t7] Should detect 'mihgt' |
| `test_ocr_transposition[Records show bieng the decision was made unanimously-bieng-being-trans_being_t4]` | fail | 383 | AssertionError: [trans_being_t4] Should detect 'bieng' |
| `test_ocr_transposition[Investigators confirmed nevre the document was submitted to the review board-nevre-never-trans_never_t1]` | fail | 318 | AssertionError: [trans_never_t1] Should detect 'nevre' |
| `test_ocr_transposition[Officials determined nevre the procedure was followed-nevre-never-trans_never_t8]` | fail | 189 | AssertionError: [trans_never_t8] Should detect 'nevre' |
| `test_ocr_transposition[The analysis confirmed eevry the data supported the claim-eevry-every-trans_every_t5]` | fail | 316 | AssertionError: [trans_every_t5] Should detect 'eevry' |
| `test_ocr_transposition[The committee found sicne the evidence was compelling-sicne-since-trans_since_t2]` | fail | 401 | AssertionError: [trans_since_t2] Should detect 'sicne' |
| `test_ocr_transposition[The investigation revealed sicne the original plan had flaws-sicne-since-trans_since_t9]` | fail | 461 | AssertionError: [trans_since_t9] Should detect 'sicne' |
| `test_ocr_transposition[It became clear thougth the project needed more resources-thougth-thought-trans_thought_t6]` | fail | 188 | AssertionError: [trans_thought_t6] Should detect 'thougth' |
| `test_ocr_transposition[Everyone acknowledged thoguh the results were significant-thoguh-though-trans_though_t3]` | fail | 255 | AssertionError: [trans_though_t3] Should detect 'thoguh' |
| `test_ocr_transposition[Experts concluded thoguh the approach was fundamentally sound-thoguh-though-trans_though_t10]` | fail | 122 | AssertionError: [trans_though_t10] Should detect 'thoguh' |
| `test_ocr_transposition[The witness stated betwene the incident occurred at noon-betwene-between-trans_between_t7]` | fail | 330 | AssertionError: [trans_between_t7] Should detect 'betwene' |
| `test_ocr_transposition[Records show agaisnt the decision was made unanimously-agaisnt-against-trans_against_t4]` | fail | 384 | AssertionError: [trans_against_t4] Should detect 'agaisnt' |
| `test_ocr_transposition[Investigators confirmed durign the document was submitted to the review board-durign-during-trans_during_t1]` | fail | 382 | AssertionError: [trans_during_t1] Should detect 'durign' |
| `test_ocr_transposition[Officials determined durign the procedure was followed-durign-during-trans_during_t8]` | fail | 252 | AssertionError: [trans_during_t8] Should detect 'durign' |
| `test_ocr_transposition[The analysis confirmed beofre the data supported the claim-beofre-before-trans_before_t5]` | fail | 347 | AssertionError: [trans_before_t5] Should detect 'beofre' |
| `test_ocr_transposition[The committee found wihtout the evidence was compelling-wihtout-without-trans_without_t2]` | fail | 395 | AssertionError: [trans_without_t2] Should detect 'wihtout' |
| `test_ocr_transposition[The investigation revealed wihtout the original plan had flaws-wihtout-without-trans_without_t9]` | fail | 450 | AssertionError: [trans_without_t9] Should detect 'wihtout' |
| `test_ocr_transposition[It became clear anohter the project needed more resources-anohter-another-trans_another_t6]` | fail | 123 | AssertionError: [trans_another_t6] Should detect 'anohter' |
| `test_ocr_transposition[Everyone acknowledged becuase the results were significant-becuase-because-trans_because_t3]` | fail | 262 | AssertionError: [trans_because_t3] Should detect 'becuase' |
| `test_ocr_transposition[Experts concluded becuase the approach was fundamentally sound-becuase-because-trans_because_t10]` | fail | 102 | AssertionError: [trans_because_t10] Should detect 'becuase' |
| `test_ocr_transposition[The witness stated aruond the incident occurred at noon-aruond-around-trans_around_t7]` | fail | 323 | AssertionError: [trans_around_t7] Should detect 'aruond' |
| `test_ocr_transposition[Records show togehter the decision was made unanimously-togehter-together-trans_together_t4]` | fail | 322 | AssertionError: [trans_together_t4] Should detect 'togehter' |
| `test_ocr_transposition[Investigators confirmed alraedy the document was submitted to the review board-alraedy-already-trans_already_t1]` | fail | 325 | AssertionError: [trans_already_t1] Should detect 'alraedy' |
| `test_ocr_transposition[Officials determined alraedy the procedure was followed-alraedy-already-trans_already_t8]` | fail | 186 | AssertionError: [trans_already_t8] Should detect 'alraedy' |
| `test_ocr_transposition[The analysis confirmed enoguh the data supported the claim-enoguh-enough-trans_enough_t5]` | fail | 303 | AssertionError: [trans_enough_t5] Should detect 'enoguh' |
| `test_ocr_transposition[The committee found beleive the evidence was compelling-beleive-believe-trans_believe_t2]` | fail | 386 | AssertionError: [trans_believe_t2] Should detect 'beleive' |
| `test_ocr_transposition[The investigation revealed beleive the original plan had flaws-beleive-believe-trans_believe_t9]` | fail | 446 | AssertionError: [trans_believe_t9] Should detect 'beleive' |
| `test_ocr_transposition[It became clear perhpas the project needed more resources-perhpas-perhaps-trans_perhaps_t6]` | fail | 123 | AssertionError: [trans_perhaps_t6] Should detect 'perhpas' |
| `test_ocr_transposition[Everyone acknowledged oftem the results were significant-oftem-often-trans_often_t3]` | fail | 260 | AssertionError: [trans_often_t3] Should detect 'oftem' |
| `test_ocr_transposition[Experts concluded oftem the approach was fundamentally sound-oftem-often-trans_often_t10]` | fail | 105 | AssertionError: [trans_often_t10] Should detect 'oftem' |
| `test_ocr_transposition[The witness stated abvoe the incident occurred at noon-abvoe-above-trans_above_t7]` | fail | 308 | AssertionError: [trans_above_t7] Should detect 'abvoe' |
| `test_ocr_transposition[Records show whlie the decision was made unanimously-whlie-while-trans_while_t4]` | fail | 369 | AssertionError: [trans_while_t4] Should detect 'whlie' |
| `test_ocr_transposition[Investigators confirmed amnog the document was submitted to the review board-amnog-among-trans_among_t1]` | fail | 305 | AssertionError: [trans_among_t1] Should detect 'amnog' |
| `test_ocr_transposition[Officials determined amnog the procedure was followed-amnog-among-trans_among_t8]` | fail | 184 | AssertionError: [trans_among_t8] Should detect 'amnog' |
| `test_ocr_transposition[The analysis confirmed untli the data supported the claim-untli-until-trans_until_t5]` | fail | 397 | AssertionError: [trans_until_t5] Should detect 'untli' |
| `test_ocr_transposition[The committee found sitll the evidence was compelling-sitll-still-trans_still_t2]` | fail | 381 | AssertionError: [trans_still_t2] Should detect 'sitll' |
| `test_ocr_transposition[The investigation revealed sitll the original plan had flaws-sitll-still-trans_still_t9]` | fail | 445 | AssertionError: [trans_still_t9] Should detect 'sitll' |
| `test_ocr_transposition[It became clear alawys the project needed more resources-alawys-always-trans_always_t6]` | fail | 101 | AssertionError: [trans_always_t6] Should detect 'alawys' |
| `test_ocr_transposition[Everyone acknowledged ealry the results were significant-ealry-early-trans_early_t3]` | fail | 258 | AssertionError: [trans_early_t3] Should detect 'ealry' |
| `test_ocr_transposition[Experts concluded ealry the approach was fundamentally sound-ealry-early-trans_early_t10]` | fail | 101 | AssertionError: [trans_early_t10] Should detect 'ealry' |
| `test_ocr_transposition[The witness stated rahter the incident occurred at noon-rahter-rather-trans_rather_t7]` | fail | 321 | AssertionError: [trans_rather_t7] Should detect 'rahter' |
| `test_ocr_transposition[Records show whsoe the decision was made unanimously-whsoe-whose-trans_whose_t4]` | fail | 320 | AssertionError: [trans_whose_t4] Should detect 'whsoe' |
| `test_ocr_transposition[Investigators confirmed qutie the document was submitted to the review board-qutie-quite-trans_quite_t1]` | fail | 387 | AssertionError: [trans_quite_t1] Should detect 'qutie' |
| `test_ocr_transposition[Officials determined qutie the procedure was followed-qutie-quite-trans_quite_t8]` | fail | 240 | AssertionError: [trans_quite_t8] Should detect 'qutie' |
| `test_ocr_transposition[The analysis confirmed ligth the data supported the claim-ligth-light-trans_light_t5]` | fail | 384 | AssertionError: [trans_light_t5] Should detect 'ligth' |
| `test_ocr_transposition[The committee found huamn the evidence was compelling-huamn-human-trans_human_t2]` | fail | 303 | AssertionError: [trans_human_t2] Should detect 'huamn' |
| `test_ocr_transposition[The investigation revealed huamn the original plan had flaws-huamn-human-trans_human_t9]` | fail | 381 | AssertionError: [trans_human_t9] Should detect 'huamn' |
| `test_ocr_transposition[It became clear womain the project needed more resources-womain-woman-trans_woman_t6]` | fail | 187 | AssertionError: [trans_woman_t6] Should detect 'womain' |
| `test_ocr_transposition[Everyone acknowledged watre the results were significant-watre-water-trans_water_t3]` | fail | 256 | AssertionError: [trans_water_t3] Should detect 'watre' |
| `test_ocr_transposition[Experts concluded watre the approach was fundamentally sound-watre-water-trans_water_t10]` | fail | 106 | AssertionError: [trans_water_t10] Should detect 'watre' |
| `test_ocr_transposition[The witness stated paepr the incident occurred at noon-paepr-paper-trans_paper_t7]` | fail | 316 | AssertionError: [trans_paper_t7] Should detect 'paepr' |
| `test_ocr_transposition[Records show maojr the decision was made unanimously-maojr-major-trans_major_t4]` | fail | 313 | AssertionError: [trans_major_t4] Should detect 'maojr' |
| `test_ocr_transposition[Investigators confirmed bagen the document was submitted to the review board-bagen-began-trans_began_t1]` | fail | 298 | AssertionError: [trans_began_t1] Should detect 'bagen' |
| `test_ocr_transposition[Officials determined bagen the procedure was followed-bagen-began-trans_began_t8]` | fail | 186 | AssertionError: [trans_began_t8] Should detect 'bagen' |
| `test_ocr_transposition[The analysis confirmed sceince the data supported the claim-sceince-science-trans_science_t5]` | fail | 401 | AssertionError: [trans_science_t5] Should detect 'sceince' |
| `test_ocr_transposition[The committee found poilcy the evidence was compelling-poilcy-policy-trans_policy_t2]` | fail | 417 | AssertionError: [trans_policy_t2] Should detect 'poilcy' |
| `test_ocr_transposition[The investigation revealed poilcy the original plan had flaws-poilcy-policy-trans_policy_t9]` | fail | 463 | AssertionError: [trans_policy_t9] Should detect 'poilcy' |
| `test_ocr_transposition[It became clear reprot the project needed more resources-reprot-report-trans_report_t6]` | fail | 120 | AssertionError: [trans_report_t6] Should detect 'reprot' |
| `test_ocr_transposition[Everyone acknowledged chagne the results were significant-chagne-change-trans_change_t3]` | fail | 264 | AssertionError: [trans_change_t3] Should detect 'chagne' |
| `test_ocr_transposition[Experts concluded chagne the approach was fundamentally sound-chagne-change-trans_change_t10]` | fail | 123 | AssertionError: [trans_change_t10] Should detect 'chagne' |
| `test_ocr_multi_error[Researchers condudecl taht the experirnent vvas a succ3ss-3-multi_7d]` | fail | 426 | AssertionError: [multi_7d] Expected >= 3 spans, got 1 |
| `test_ocr_multi_error[The tourrnarment attractecl thousands 0f spectators-2-multi_9c]` | fail | 105 | AssertionError: [multi_9c] Should detect multiple errors |
| `test_ocr_multi_error[Teh cornrnittee examinecl the proposed arnendment-2-multi_13a]` | fail | 463 | AssertionError: [multi_13a] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[Teh governrnent announcecl a fundarnental reforrn pIan-3-multi_14d]` | fail | 391 | AssertionError: [multi_14d] Expected >= 3 spans, got 2 |
| `test_ocr_multi_error[Students shoudl complete teh assignment by Friday-2-multi_16c]` | fail | 388 | AssertionError: [multi_16c] Should detect multiple errors |
| `test_ocr_multi_error[The articde described the spectadular transforrnnation-2-multi_20a]` | fail | 327 | AssertionError: [multi_20a] Should detect multiple errors |
| `test_ocr_multi_error[Teh crirninal vvas apprehendecl near the tovvn center-3-multi_21d]` | fail | 472 | AssertionError: [multi_21d] Expected >= 3 spans, got 2 |
| `test_ocr_multi_error[Parents shoudl monitor their chiIdren's activiti3s-2-multi_23c]` | fail | 645 | AssertionError: [multi_23c] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[Teh vehicle's permanent registrati0n was approved-2-multi_25b]` | fail | 459 | AssertionError: [multi_25b] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[Teh moledular structure was analyzecl in the Iab-2-multi_27a]` | fail | 192 | AssertionError: [multi_27a] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[The alarrn system vvas tested during the storrn-2-multi_30c]` | fail | 260 | AssertionError: [multi_30c] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[Teh museum dispIayed a spectacular collection-2-multi_32b]` | fail | 305 | AssertionError: [multi_32b] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[The educati0n systern needs fundarnental changes-2-multi_34a]` | fail | 280 | AssertionError: [multi_34a] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[Teh recornrnendation vvas acceptecl by teh board-3-multi_35d]` | fail | 600 | AssertionError: [multi_35d] Expected >= 3 spans, got 2 |
| `test_ocr_multi_error[The rnernorial was visited by thous4nds of tourists-2-multi_37c]` | fail | 590 | AssertionError: [multi_37c] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[Teh national park attracted miIIions of visitors-2-multi_39b]` | fail | 434 | AssertionError: [multi_39b] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[The cornrnunity center hostecl a fundraising event-2-multi_41a]` | fail | 503 | AssertionError: [multi_41a] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[Teh therrrnal energy systern vvas highIy efficient-3-multi_42d]` | fail | 366 | AssertionError: [multi_42d] Expected >= 3 spans, got 2 |
| `test_ocr_multi_error[Teh teacher explalined the experimental procedur3-2-multi_44c]` | fail | 364 | AssertionError: [multi_44c] Should detect multiple errors |
| `test_ocr_multi_error[The rnanager confirmed teh schedule for the ev3nt-2-multi_46b]` | fail | 272 | AssertionError: [multi_46b] Should detect multiple errors |
| `test_ocr_multi_error[Voters shoudl exarnine eachl candidate's platform-2-multi_48a]` | fail | 178 | AssertionError: [multi_48a] Should detect multiple errors |
| `test_ocr_multi_error[Teh docurnent vvas signecl by aII participating parti3s-3-multi_49d]` | fail | 587 | AssertionError: [multi_49d] Expected >= 3 spans, got 2 |
| `test_ocr_multi_error[The rnilitary commander issued new orclers today-2-multi_51c]` | fail | 325 | AssertionError: [multi_51c] Should detect multiple errors |
| `test_ocr_multi_error[The netvvork systern requirecl significant upgrades-2-multi_55a]` | fail | 431 | AssertionError: [multi_55a] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[Teh corrununity gardlen provicled fresh vegetabIes-3-multi_56d]` | fail | 370 | AssertionError: [multi_56d] Expected >= 3 spans, got 1 |
| `test_ocr_multi_error[Teh medical tearn completed the surgicaI procedure-2-multi_58c]` | fail | 326 | AssertionError: [multi_58c] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[Teh school district approved a nevv curriculum-2-multi_60b]` | fail | 392 | AssertionError: [multi_60b] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[The transportati0n systern servecl millions of riders-2-multi_62a]` | fail | 520 | AssertionError: [multi_62a] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[Teh construction cornpany cornpleted the tovver on tirne-3-multi_63d]` | fail | 333 | AssertionError: [multi_63d] Expected >= 3 spans, got 1 |
| `test_ocr_multi_error[Several ernployees complained abuot the nevv policy-2-multi_65c]` | fail | 327 | AssertionError: [multi_65c] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[Teh window vvas broken during the severe storrn-2-multi_67b]` | fail | 323 | AssertionError: [multi_67b] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[The rnusician perforrned a beautifuI concert last night-2-multi_69a]` | fail | 403 | AssertionError: [multi_69a] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[Teh archit3ct clesigned a spectadular buiIding-3-multi_70d]` | fail | 561 | AssertionError: [multi_70d] Expected >= 3 spans, got 1 |
| `test_ocr_multi_error[Teh university published its res3arch findings-2-multi_72c]` | fail | 324 | AssertionError: [multi_72c] Should detect multiple errors |
| `test_ocr_multi_error[The factory producecl thousands of uniforrns daily-2-multi_76a]` | fail | 237 | AssertionError: [multi_76a] Should detect multiple errors |
| `test_ocr_multi_error[Teh historian exarnined ancierit docurnents carefuIIy-3-multi_77d]` | fail | 662 | AssertionError: [multi_77d] Expected >= 3 spans, got 1 |
| `test_ocr_multi_error[The dernonstration attracted international rnedia attenti0n-2-multi_79c]` | fail | 604 | AssertionError: [multi_79c] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[The Iibrary catalogl contained rnillions of entries-2-multi_83a]` | fail | 460 | AssertionError: [multi_83a] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[Teh technol0gy cornpany announcecl a rnerg3r-3-multi_84d]` | fail | 326 | AssertionError: [multi_84d] Expected >= 3 spans, got 2 |
| `test_ocr_multi_error[The infrastrudure required significant investrnent-2-multi_86c]` | fail | 442 | AssertionError: [multi_86c] Should detect multiple errors |
| `test_ocr_multi_error[Teh election commission verified teh results-2-multi_88b]` | fail | 512 | AssertionError: [multi_88b] Should detect multiple errors |
| `test_ocr_multi_error[Teh governrnent spokesperson issuecl a clarification-2-multi_90a]` | fail | 538 | AssertionError: [multi_90a] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[Teh financiaI market experienced unprecedented growth-2-multi_93c]` | fail | 379 | AssertionError: [multi_93c] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[Teh numerical clata reveaIed a significant tr3nd-2-multi_95b]` | fail | 291 | AssertionError: [multi_95b] Expected >= 2 spans, got 1 |
| `test_ocr_multi_error[The dernonstrators rnarched through the tovvn peacefully-2-multi_97a]` | fail | 304 | AssertionError: [multi_97a] Expected >= 2 spans, got 1 |
| `test_ocr_hard_case[The hospital administration released a statement noting that patient satisfaction scores had improved significantly thanks to the dedication of the rnedical staff and support personnel-rnedical-medical-hard_long_ctx_6]` | fail | 710 | AssertionError: [hard_long_ctx_6] Should detect 'rnedical' |
| `test_ocr_hard_case[The transportation authority confirmed that the new subway extension would serve an estimated forty thousand daily commuters once the terrninal station was completed next year-terrninal-terminal-hard_long_ctx_13]` | fail | 555 | AssertionError: [hard_long_ctx_13] Should detect 'terrninal' |
| `test_ocr_hard_case[The school district implemented a comprehensive teacher training program focusing on modern pedagogy, digital literacy, and inclusive classroom rnethods that support all learners-rnethods-methods-hard_long_ctx_20]` | fail | 596 | AssertionError: [hard_long_ctx_20] Should detect 'rnethods' |
| `test_ocr_hard_case[The pharrnaceutical compound showed promising results in trials-pharrnaceutical-pharmaceutical-hard_tech_7]` | fail | 404 | AssertionError: [hard_tech_7] Should detect 'pharrnaceutical' |
| `test_ocr_hard_case[The rnicroprocessor executed billions of instructions per second-rnicroprocessor-microprocessor-hard_tech_14]` | fail | 327 | AssertionError: [hard_tech_14] Should detect 'rnicroprocessor' |
| `test_ocr_hard_case[Alraedy the results have exceeded initial expectations-Alraedy-Already-hard_start_15]` | fail | 260 | AssertionError: [hard_start_15] Should detect 'Alraedy' |
| `test_ocr_hard_case[The evidence led to a startling achievernent-achievernent-achievement-hard_end_9]` | fail | 336 | AssertionError: [hard_end_9] Should detect 'achievernent' |
| `test_ocr_hard_case[The environrnent\u2014already fragile\u2014needed immediate protection.-environrnent-environment-hard_punct_3]` | fail | 389 | AssertionError: [hard_punct_3] Should detect 'environrnent' |
| `test_ocr_hard_case["The instrurnent is precise," the technician confirmed.-instrurnent-instrument-hard_punct_10]` | fail | 480 | AssertionError: [hard_punct_10] Should detect 'instrurnent' |
| `test_ocr_hard_case["The reforrn is necessary," the senator argued.-reforrn-reform-hard_punct_17]` | fail | 121 | AssertionError: [hard_punct_17] Should detect 'reforrn' |
| `test_ocr_hard_case[They collected 3,500 sarnples from the river basin-sarnples-samples-hard_num_4]` | fail | 277 | AssertionError: [hard_num_4] Should detect 'sarnples' |
| `test_ocr_hard_case[Room 301 housed the experirnental equipment-experirnental-experimental-hard_num_18]` | fail | 200 | AssertionError: [hard_num_18] Should detect 'experirnental' |
| `test_ocr_hard_case[Review the docurnent carefully-docurnent-document-hard_short_5]` | fail | 117 | AssertionError: [hard_short_5] Should detect 'docurnent' |
| `test_ocr_hard_case[Departrment budget review-Departrment-Department-hard_short_12]` | fail | 186 | AssertionError: [hard_short_12] Should detect 'Departrment' |
| `test_ocr_hard_case[Shoudl be approved-Shoudl-Should-hard_short_19]` | fail | 110 | AssertionError: [hard_short_19] Should detect 'Shoudl' |
| `test_ocr_hard_case[The workers needed to reforrn the outdated procedures-reforrn-reform-hard_realword_6]` | fail | 125 | AssertionError: [hard_realword_6] Should detect 'reforrn' |
| `test_ocr_hard_case[Officials voted to exdude the contested provision-exdude-exclude-hard_realword_13]` | fail | 265 | AssertionError: [hard_realword_13] Should detect 'exdude' |
| `test_ocr_hard_case[The exarnination results will be posted tomorrow-exarnination-examination-hard_multi_corr_7]` | fail | 332 | AssertionError: [hard_multi_corr_7] Should detect 'exarnination' |
| `test_ocr_hard_case[The adrninistrative burden fell on the local office-adrninistrative-administrative-hard_multi_corr_14]` | fail | 332 | AssertionError: [hard_multi_corr_14] Should detect 'adrninistrative' |
| `test_ocr_hard_case[The United Nations Environrnent Programme released a new report-Environrnent-Environment-hard_cap_1]` | fail | 263 | AssertionError: [hard_cap_1] Should detect 'Environrnent' |
| `test_ocr_hard_case[The World Environrnent Day celebration was held in June-Environrnent-Environment-hard_cap_8]` | fail | 260 | AssertionError: [hard_cap_8] Should detect 'Environrnent' |
| `test_ocr_hard_case[She wrote in her letter: "The environrnent is our shared responsibility."-environrnent-environment-hard_quote_2]` | fail | 347 | AssertionError: [hard_quote_2] Should detect 'environrnent' |
| `test_ocr_hard_case[The judge declared: "The arnendment is unconstitutional."-arnendment-amendment-hard_quote_9]` | fail | 269 | AssertionError: [hard_quote_9] Should detect 'arnendment' |
| `test_ocr_hard_case[The advertisement claimed: "This is a fundarnental breakthrough."-fundarnental-fundamental-hard_quote_16]` | fail | 327 | AssertionError: [hard_quote_16] Should detect 'fundarnental' |
| `test_ocr_hard_case[The 1,200-seat auditorium hosted the tourrnarment finals in 2022-tourrnarment-tournament-hard_numctx_10]` | fail | 616 | AssertionError: [hard_numctx_10] Should detect 'tourrnarment' |
| `test_ocr_hard_case[The cornputer system crashed during the critical update process-cornputer-computer-hard_misc_7]` | fail | 323 | AssertionError: [hard_misc_7] Should detect 'cornputer' |
| `test_ocr_hard_case[The rnilestone was reached ahead of the original schedule-rnilestone-milestone-hard_misc_14]` | fail | 323 | AssertionError: [hard_misc_14] Should detect 'rnilestone' |
| `test_ocr_hard_case[The investrnent portfolio was diversified across sectors-investrnent-investment-hard_misc_21]` | fail | 388 | AssertionError: [hard_misc_21] Should detect 'investrnent' |
| `test_ocr_hard_case[The announcerrrent was made during the press conference-announcerrrent-announcement-hard_misc_28]` | fail | 190 | AssertionError: [hard_misc_28] Should detect 'announcerrrent' |
| `test_ocr_hard_case[The abandonrnent of the site raised environmental concerns-abandonrnent-abandonment-hard_misc_35]` | fail | 323 | AssertionError: [hard_misc_35] Should detect 'abandonrnent' |
| `test_ocr_hard_case[The multi-platforrn solution supported all major operating systems-multi-platforrn-multi-platform-hard_hyph_6]` | fail | 273 | AssertionError: [hard_hyph_6] Should detect 'multi-platforrn' |
| `test_ocr_hard_case[The instrurnents were calibrated before each measurement-instrurnents-instruments-hard_plural_3]` | fail | 262 | AssertionError: [hard_plural_3] Should detect 'instrurnents' |
| `test_ocr_hard_case[The requirernents for certification were recently updated-requirernents-requirements-hard_plural_10]` | fail | 321 | AssertionError: [hard_plural_10] Should detect 'requirernents' |
| `test_ocr_hard_case[The cornrnittee exarnined the evidence for three consecutive days-exarnined-examined-hard_tense_4]` | fail | 628 | AssertionError: [hard_tense_4] Missing span for 'exarnined' |
| `test_ocr_hard_case[The authorities were confirrning the identities of the passengers-confirrning-confirming-hard_tense_18]` | fail | 539 | AssertionError: [hard_tense_18] Should detect 'confirrning' |
| `test_ocr_hard_case[Since 1998 the environrnent has deteriorated measurably-environrnent-environment-hard_numctx_15]` | fail | 253 | AssertionError: [hard_numctx_15] Should detect 'environrnent' |
| `test_ocr_hard_case[The systern was designed to handle peak loads efficiently-systern-system-hard_misc_42]` | fail | 253 | AssertionError: [hard_misc_42] Should detect 'systern' |
| `test_ocr_hard_case[The phantorn signal appeared intermittently on the radar-phantorn-phantom-hard_misc_49]` | fail | 333 | AssertionError: [hard_misc_49] Should detect 'phantorn' |
| `test_ocr_hard_case[The fundarnentally flawed approach was abandoned after review-fundarnentally-fundamentally-hard_adv_6]` | fail | 196 | AssertionError: [hard_adv_6] Should detect 'fundarnentally' |
| `test_ocr_hard_case[Workers dernanded higher wages, so the cornpany began negotiations-dernanded-demanded-hard_compound_3]` | fail | 273 | AssertionError: [hard_compound_3] Should detect 'dernanded' |
| `test_ocr_hard_case[The rnaterial arrived late, but the project still finished on time-rnaterial-material-hard_compound_10]` | fail | 345 | AssertionError: [hard_compound_10] Should detect 'rnaterial' |
| `test_ocr_hard_case[The arnendment was ratified by the state legislature-arnendment-amendment-hard_passive_7]` | fail | 260 | AssertionError: [hard_passive_7] Should detect 'arnendment' |
| `test_ocr_hard_case[How many docurnents were reviewed during the audit?-docurnents-documents-hard_question_4]` | fail | 431 | AssertionError: [hard_question_4] Should detect 'docurnents' |

## Slowest 30 tests

| # | Time (ms) | Status | Test |
|---:|---:|---|---|
| 1 | 813 | pass | `tests.test_ocr_tp_structural::test_ocr_multi_error[The internationaI commission reviewed tracl3 policies-2-multi_100c]` |
| 2 | 724 | pass | `tests.test_ocr_tp_structural::test_ocr_multi_error[Citizens should exarnine teh officiaI report carefuIIy-2-multi_4b]` |
| 3 | 710 | fail | `tests.test_ocr_tp_structural::test_ocr_hard_case[The hospital administration released a statement noting that patient satisfaction scores had improved significantly thanks to the dedication of the rnedical staff and support personnel-rnedical-medical-hard_long_ctx_6]` |
| 4 | 708 | pass | `tests.test_ocr_tp_structural::test_ocr_multi_error[The 0rganization pubiished its annuaI rep0rt yesterday-2-multi_6a]` |
| 5 | 693 | pass | `tests.test_ocr_tp_structural::test_ocr_hard_case[The organization was cornrnitting resources to the new initiative-cornrnitting-committing-hard_tense_11]` |
| 6 | 677 | pass | `tests.test_ocr_tp_digits::test_ocr_digit_substitution[1_for_l__constitutiona1__t3]` |
| 7 | 666 | pass | `tests.test_ocr_tp_structural::test_ocr_multi_error[Teh schoiarship prograrrr supp0rted taIented stud3nts-3-multi_98d]` |
| 8 | 662 | pass | `tests.test_ocr_tp_digits::test_ocr_digit_substitution[1_for_l__1iteral__t3]` |
| 9 | 662 | fail | `tests.test_ocr_tp_structural::test_ocr_multi_error[Teh historian exarnined ancierit docurnents carefuIIy-3-multi_77d]` |
| 10 | 647 | pass | `tests.test_ocr_tp_digits::test_ocr_digit_substitution[1_for_l__surviva1__t3]` |
| 11 | 645 | fail | `tests.test_ocr_tp_structural::test_ocr_multi_error[Parents shoudl monitor their chiIdren's activiti3s-2-multi_23c]` |
| 12 | 644 | pass | `tests.test_ocr_tp_structural::test_ocr_multi_error[Teh rnineral dep0sits vvere discoveredl Iast year-3-multi_28d]` |
| 13 | 644 | pass | `tests.test_ocr_tp_structural::test_ocr_multi_error[Teh particuIar spectade drevv considerabIe att3ntion-3-multi_91d]` |
| 14 | 637 | pass | `tests.test_ocr_tp_structural::test_ocr_multi_error[Teh final rep0rt included several recornrnendations-2-multi_11b]` |
| 15 | 634 | fail | `tests.test_ocr_tp_digits::test_ocr_digit_substitution[7_for_t__7heater__t4]` |
| 16 | 633 | pass | `tests.test_ocr_tp_digits::test_ocr_digit_substitution[1_for_l__constitutiona1__t10]` |
| 17 | 628 | fail | `tests.test_ocr_tp_structural::test_ocr_hard_case[The cornrnittee exarnined the evidence for three consecutive days-exarnined-examined-hard_tense_4]` |
| 18 | 616 | fail | `tests.test_ocr_tp_structural::test_ocr_hard_case[The 1,200-seat auditorium hosted the tourrnarment finals in 2022-tourrnarment-tournament-hard_numctx_10]` |
| 19 | 615 | pass | `tests.test_ocr_tp_digits::test_ocr_digit_substitution[1_for_l__virtua1__t3]` |
| 20 | 605 | pass | `tests.test_ocr_tp_digits::test_ocr_digit_substitution[1_for_l__crysta1__t3]` |
| 21 | 604 | pass | `tests.test_ocr_tp_digits::test_ocr_digit_substitution[0_for_o__br0wn__t1]` |
| 22 | 604 | fail | `tests.test_ocr_tp_structural::test_ocr_multi_error[The dernonstration attracted international rnedia attenti0n-2-multi_79c]` |
| 23 | 603 | pass | `tests.test_ocr_tp_digits::test_ocr_digit_substitution[1_for_l__po1itical__t1]` |
| 24 | 600 | fail | `tests.test_ocr_tp_structural::test_ocr_multi_error[Teh recornrnendation vvas acceptecl by teh board-3-multi_35d]` |
| 25 | 596 | fail | `tests.test_ocr_tp_structural::test_ocr_hard_case[The school district implemented a comprehensive teacher training program focusing on modern pedagogy, digital literacy, and inclusive classroom rnethods that support all learners-rnethods-methods-hard_long_ctx_20]` |
| 26 | 595 | fail | `tests.test_ocr_tp_digits::test_ocr_digit_substitution[7_for_t__7ribute__t4]` |
| 27 | 592 | pass | `tests.test_ocr_tp_digits::test_ocr_digit_substitution[1_for_l__medica1__t1]` |
| 28 | 590 | fail | `tests.test_ocr_tp_structural::test_ocr_multi_error[The rnernorial was visited by thous4nds of tourists-2-multi_37c]` |
| 29 | 590 | pass | `tests.test_ocr_tp_structural::test_ocr_hard_case[In 2024 the cornrnission published its annual review-cornrnission-commission-hard_num_11]` |
| 30 | 588 | pass | `tests.test_ocr_tp_digits::test_ocr_digit_substitution[1_for_l__regiona1__t1]` |
