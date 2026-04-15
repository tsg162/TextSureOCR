# ts1 — Tests 2001-3000 (continuation)

- **Source:** `/tmp/ts1_2001_3000.xml`
- **Cases:** 1000  (960 pass · 40 fail · 0 error · 0 skip)
- **Accuracy:** 96.00% (executed: 1000)
- **Total test-time:** 160.1s
- **Throughput:** 6.25 tests/sec  ·  **mean** 160 ms/test
- **Latency:** p50 161 ms · p95 169 ms · p99 195 ms · max 399 ms

## Per-file breakdown

| File | Pass | Fail | Error | Skip | Accuracy | Mean (ms) | Sum (s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `tests` | 960 | 40 | 0 | 0 | 96.0% | 160 | 160.1 |

## Failures (40)

### `tests` (40)

| Test | Status | Time (ms) | Message |
|---|---|---:|---|
| `test_likely_continuation[same_topic_054]` | fail | 163 | AssertionError: [same_topic_054] Expected likely_continuation: 'The mine produced over two million tons ...' -> 'Safety improvements had reduced the acci...' |
| `test_likely_continuation[same_topic_065]` | fail | 164 | AssertionError: [same_topic_065] Expected likely_continuation: 'The power plant generated enough electri...' -> 'Maintenance shutdowns were carefully coo...' |
| `test_unlikely_continuation[topic_switch_014]` | fail | 150 | AssertionError: [topic_switch_014] Expected unlikely_continuation: 'The annual rainfall in the Amazon basin ...' -> 'The gardener planted rows of lavender al...' |
| `test_unlikely_continuation[topic_switch_016]` | fail | 147 | AssertionError: [topic_switch_016] Score 0.473 > max 0.4 |
| `test_unlikely_continuation[topic_switch_030]` | fail | 160 | AssertionError: [topic_switch_030] Score 0.43 > max 0.4 |
| `test_unlikely_continuation[topic_switch_034]` | fail | 167 | AssertionError: [topic_switch_034] Expected unlikely_continuation: 'The annual rainfall in the Amazon basin ...' -> 'The astronomy club set up telescopes for...' |
| `test_unlikely_continuation[topic_switch_062]` | fail | 161 | AssertionError: [topic_switch_062] Score 0.495 > max 0.4 |
| `test_unlikely_continuation[topic_switch_114]` | fail | 166 | AssertionError: [topic_switch_114] Score 0.414 > max 0.4 |
| `test_unlikely_continuation[topic_switch_154]` | fail | 163 | AssertionError: [topic_switch_154] Expected unlikely_continuation: 'Photosynthesis converts carbon dioxide a...' -> 'The astronomy club set up telescopes for...' |
| `test_unlikely_continuation[topic_switch_174]` | fail | 161 | AssertionError: [topic_switch_174] Expected unlikely_continuation: 'The migration patterns of arctic birds h...' -> 'The gardener planted rows of lavender al...' |
| `test_unlikely_continuation[topic_switch_187]` | fail | 163 | AssertionError: [topic_switch_187] Score 0.428 > max 0.4 |
| `test_unlikely_continuation[topic_switch_194]` | fail | 161 | AssertionError: [topic_switch_194] Expected unlikely_continuation: 'The migration patterns of arctic birds h...' -> 'The astronomy club set up telescopes for...' |
| `test_unlikely_continuation[topic_switch_214]` | fail | 164 | AssertionError: [topic_switch_214] Expected unlikely_continuation: 'The tectonic plates beneath the ocean fl...' -> 'The gardener planted rows of lavender al...' |
| `test_unlikely_continuation[topic_switch_234]` | fail | 164 | AssertionError: [topic_switch_234] Expected unlikely_continuation: 'The tectonic plates beneath the ocean fl...' -> 'The astronomy club set up telescopes for...' |
| `test_unlikely_continuation[topic_switch_254]` | fail | 194 | AssertionError: [topic_switch_254] Expected unlikely_continuation: 'The Hubble telescope has captured images...' -> 'The gardener planted rows of lavender al...' |
| `test_unlikely_continuation[topic_switch_266]` | fail | 165 | AssertionError: [topic_switch_266] Score 0.412 > max 0.4 |
| `test_unlikely_continuation[topic_switch_267]` | fail | 163 | AssertionError: [topic_switch_267] Score 0.417 > max 0.4 |
| `test_unlikely_continuation[topic_switch_274]` | fail | 159 | AssertionError: [topic_switch_274] Expected unlikely_continuation: 'The Hubble telescope has captured images...' -> 'The astronomy club set up telescopes for...' |
| `test_unlikely_continuation[topic_switch_314]` | fail | 160 | AssertionError: [topic_switch_314] Score 0.482 > max 0.4 |
| `test_unlikely_continuation[topic_switch_334]` | fail | 147 | AssertionError: [topic_switch_334] Expected unlikely_continuation: 'The melting of polar ice caps has accele...' -> 'The gardener planted rows of lavender al...' |
| `test_unlikely_continuation[topic_switch_354]` | fail | 157 | AssertionError: [topic_switch_354] Expected unlikely_continuation: 'The melting of polar ice caps has accele...' -> 'The astronomy club set up telescopes for...' |
| `test_unlikely_continuation[topic_switch_394]` | fail | 159 | AssertionError: [topic_switch_394] Expected unlikely_continuation: 'Volcanic eruptions can release enormous ...' -> 'The astronomy club set up telescopes for...' |
| `test_unlikely_continuation[topic_switch_434]` | fail | 150 | AssertionError: [topic_switch_434] Expected unlikely_continuation: 'The process of cellular respiration gene...' -> 'The astronomy club set up telescopes for...' |
| `test_unlikely_continuation[topic_switch_454]` | fail | 140 | AssertionError: [topic_switch_454] Expected unlikely_continuation: 'Coral reefs provide habitat for thousand...' -> 'The gardener planted rows of lavender al...' |
| `test_unlikely_continuation[topic_switch_462]` | fail | 163 | AssertionError: [topic_switch_462] Score 0.406 > max 0.4 |
| `test_unlikely_continuation[topic_switch_474]` | fail | 149 | AssertionError: [topic_switch_474] Expected unlikely_continuation: 'Coral reefs provide habitat for thousand...' -> 'The astronomy club set up telescopes for...' |
| `test_unlikely_continuation[topic_switch_534]` | fail | 163 | AssertionError: [topic_switch_534] Score 0.455 > max 0.4 |
| `test_unlikely_continuation[topic_switch_547]` | fail | 164 | AssertionError: [topic_switch_547] Score 0.445 > max 0.4 |
| `test_unlikely_continuation[topic_switch_554]` | fail | 160 | AssertionError: [topic_switch_554] Expected unlikely_continuation: 'Gravitational waves were first detected ...' -> 'The astronomy club set up telescopes for...' |
| `test_unlikely_continuation[topic_switch_594]` | fail | 163 | AssertionError: [topic_switch_594] Expected unlikely_continuation: 'The periodic table organizes elements by...' -> 'The astronomy club set up telescopes for...' |
| `test_unlikely_continuation[topic_switch_614]` | fail | 161 | AssertionError: [topic_switch_614] Score 0.409 > max 0.4 |
| `test_unlikely_continuation[topic_switch_634]` | fail | 168 | AssertionError: [topic_switch_634] Expected unlikely_continuation: 'Plate tectonics explains the movement of...' -> 'The astronomy club set up telescopes for...' |
| `test_unlikely_continuation[topic_switch_641]` | fail | 159 | AssertionError: [topic_switch_641] Score 0.448 > max 0.4 |
| `test_unlikely_continuation[topic_switch_654]` | fail | 162 | AssertionError: [topic_switch_654] Score 0.487 > max 0.4 |
| `test_unlikely_continuation[topic_switch_674]` | fail | 160 | AssertionError: [topic_switch_674] Expected unlikely_continuation: 'The water cycle involves evaporation con...' -> 'The astronomy club set up telescopes for...' |
| `test_unlikely_continuation[topic_switch_714]` | fail | 160 | AssertionError: [topic_switch_714] Expected unlikely_continuation: 'Black holes form when massive stars coll...' -> 'The astronomy club set up telescopes for...' |
| `test_unlikely_continuation[topic_switch_794]` | fail | 160 | AssertionError: [topic_switch_794] Expected unlikely_continuation: 'Nuclear fusion powers the sun by combini...' -> 'The astronomy club set up telescopes for...' |
| `test_unlikely_continuation[topic_switch_814]` | fail | 144 | AssertionError: [topic_switch_814] Expected unlikely_continuation: 'The ozone layer protects the earth from ...' -> 'The gardener planted rows of lavender al...' |
| `test_unlikely_continuation[topic_switch_827]` | fail | 143 | AssertionError: [topic_switch_827] Score 0.423 > max 0.4 |
| `test_unlikely_continuation[topic_switch_834]` | fail | 151 | AssertionError: [topic_switch_834] Expected unlikely_continuation: 'The ozone layer protects the earth from ...' -> 'The astronomy club set up telescopes for...' |

## Slowest 30 tests

| # | Time (ms) | Status | Test |
|---:|---:|---|---|
| 1 | 399 | pass | `tests.test_continuation::test_likely_continuation[tech_032]` |
| 2 | 293 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_881]` |
| 3 | 256 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_252]` |
| 4 | 207 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_256]` |
| 5 | 204 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_239]` |
| 6 | 199 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_261]` |
| 7 | 198 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_255]` |
| 8 | 198 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_264]` |
| 9 | 197 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_696]` |
| 10 | 195 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_233]` |
| 11 | 195 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_260]` |
| 12 | 194 | fail | `tests.test_continuation::test_unlikely_continuation[topic_switch_254]` |
| 13 | 194 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_609]` |
| 14 | 194 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_613]` |
| 15 | 193 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_610]` |
| 16 | 191 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_612]` |
| 17 | 189 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_401]` |
| 18 | 187 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_767]` |
| 19 | 184 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_411]` |
| 20 | 181 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_810]` |
| 21 | 179 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_410]` |
| 22 | 179 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_611]` |
| 23 | 178 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_488]` |
| 24 | 177 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_388]` |
| 25 | 177 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_824]` |
| 26 | 177 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_847]` |
| 27 | 176 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_620]` |
| 28 | 176 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_825]` |
| 29 | 176 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_833]` |
| 30 | 176 | pass | `tests.test_continuation::test_unlikely_continuation[topic_switch_861]` |
