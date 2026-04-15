# ts1 — Tests 1-1000 (likely_continuation)

- **Source:** `/tmp/ts1_1_1000.xml`
- **Cases:** 1000  (957 pass · 43 fail · 0 error · 0 skip)
- **Accuracy:** 95.70% (executed: 1000)
- **Total test-time:** 165.1s
- **Throughput:** 6.06 tests/sec  ·  **mean** 165 ms/test
- **Latency:** p50 163 ms · p95 175 ms · p99 201 ms · max 413 ms

## Per-file breakdown

| File | Pass | Fail | Error | Skip | Accuracy | Mean (ms) | Sum (s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `tests` | 957 | 43 | 0 | 0 | 95.7% | 165 | 165.1 |

## Failures (43)

### `tests` (43)

| Test | Status | Time (ms) | Message |
|---|---|---:|---|
| `test_likely_continuation[midsent_004_p0]` | fail | 163 | AssertionError: [midsent_004_p0] Expected likely_continuation: 'The committee...' -> 'unanimously approved the proposed budget...' |
| `test_likely_continuation[midsent_011_p0]` | fail | 166 | AssertionError: [midsent_011_p0] Expected likely_continuation: 'Local farmers...' -> 'harvested their crops before the first f...' |
| `test_likely_continuation[midsent_020_p0]` | fail | 161 | AssertionError: [midsent_020_p0] Expected likely_continuation: 'The mayor...' -> 'announced plans to renovate the historic...' |
| `test_likely_continuation[midsent_020_p7]` | fail | 162 | AssertionError: [midsent_020_p7] Expected likely_continuation: 'The mayor announced plans to renovate th...' -> 'district soon...' |
| `test_likely_continuation[midsent_023_p0]` | fail | 164 | AssertionError: [midsent_023_p0] Expected likely_continuation: 'Gardeners planted...' -> 'colorful flowers along the pathway leadi...' |
| `test_likely_continuation[midsent_029_p7]` | fail | 167 | AssertionError: [midsent_029_p7] Expected likely_continuation: 'Construction workers completed the found...' -> 'ahead of schedule...' |
| `test_likely_continuation[midsent_032_p0]` | fail | 163 | AssertionError: [midsent_032_p0] Expected likely_continuation: 'The bakery...' -> 'produces fresh bread and pastries every ...' |
| `test_likely_continuation[midsent_032_p6]` | fail | 166 | AssertionError: [midsent_032_p6] Expected likely_continuation: 'The bakery produces fresh bread and past...' -> 'morning before dawn...' |
| `test_likely_continuation[midsent_032_p7]` | fail | 164 | AssertionError: [midsent_032_p7] Expected likely_continuation: 'The bakery produces fresh bread and past...' -> 'before dawn...' |
| `test_likely_continuation[midsent_041_p0]` | fail | 171 | AssertionError: [midsent_041_p0] Expected likely_continuation: 'Marine biologists...' -> 'studied the coral reef ecosystem in the ...' |
| `test_likely_continuation[midsent_041_p2]` | fail | 168 | AssertionError: [midsent_041_p2] Expected likely_continuation: 'Marine biologists studied the...' -> 'coral reef ecosystem in the tropical wat...' |
| `test_likely_continuation[midsent_043_p4]` | fail | 165 | AssertionError: [midsent_043_p4] Expected likely_continuation: 'Electricians installed new wiring throug...' -> 'renovated office building...' |
| `test_likely_continuation[midsent_046_p0]` | fail | 142 | AssertionError: [midsent_046_p0] Expected likely_continuation: 'The coach...' -> 'motivated the team with an encouraging s...' |
| `test_likely_continuation[midsent_049_p3]` | fail | 160 | AssertionError: [midsent_049_p3] Expected likely_continuation: 'Biologists tracked the population of...' -> 'endangered species in the national park...' |
| `test_likely_continuation[midsent_052_p7]` | fail | 162 | AssertionError: [midsent_052_p7] Expected likely_continuation: 'The accountant prepared the annual finan...' -> 'board review...' |
| `test_likely_continuation[midsent_056_p0]` | fail | 161 | AssertionError: [midsent_056_p0] Expected likely_continuation: 'The teacher...' -> 'explained the mathematical concept using...' |
| `test_likely_continuation[midsent_056_p2]` | fail | 151 | AssertionError: [midsent_056_p2] Expected likely_continuation: 'The teacher explained the...' -> 'mathematical concept using practical exa...' |
| `test_likely_continuation[midsent_056_p5]` | fail | 163 | AssertionError: [midsent_056_p5] Expected likely_continuation: 'The teacher explained the mathematical c...' -> 'practical examples...' |
| `test_likely_continuation[midsent_065_p6]` | fail | 155 | AssertionError: [midsent_065_p6] Expected likely_continuation: 'Historians discovered new documents shed...' -> 'ancient civilization...' |
| `test_likely_continuation[midsent_068_p0]` | fail | 155 | AssertionError: [midsent_068_p0] Expected likely_continuation: 'The carpenter...' -> 'crafted beautiful furniture using tradit...' |
| `test_likely_continuation[midsent_070_p0]` | fail | 188 | AssertionError: [midsent_070_p0] Expected likely_continuation: 'The editor...' -> 'reviewed the manuscript and suggested se...' |
| `test_likely_continuation[midsent_076_p0]` | fail | 171 | AssertionError: [midsent_076_p0] Expected likely_continuation: 'The bus...' -> 'driver followed the detour after the mai...' |
| `test_likely_continuation[midsent_076_p1]` | fail | 170 | AssertionError: [midsent_076_p1] Expected likely_continuation: 'The bus driver...' -> 'followed the detour after the main road ...' |
| `test_likely_continuation[midsent_079_p1]` | fail | 168 | AssertionError: [midsent_079_p1] Expected likely_continuation: 'Engineers tested the...' -> 'prototype extensively before beginning m...' |
| `test_likely_continuation[midsent_081_p3]` | fail | 165 | AssertionError: [midsent_081_p3] Expected likely_continuation: 'Ornithologists recorded the songs of...' -> 'migratory birds in the wetland habitat...' |
| `test_likely_continuation[midsent_082_p0]` | fail | 171 | AssertionError: [midsent_082_p0] Expected likely_continuation: 'The contractor...' -> 'estimated the cost of the home renovatio...' |
| `test_likely_continuation[midsent_083_p5]` | fail | 170 | AssertionError: [midsent_083_p5] Expected likely_continuation: 'Dancers performed a breathtaking routine...' -> 'cultural festival downtown...' |
| `test_likely_continuation[midsent_088_p0]` | fail | 169 | AssertionError: [midsent_088_p0] Expected likely_continuation: 'The locksmith...' -> 'replaced all the locks in the apartment ...' |
| `test_likely_continuation[midsent_088_p3]` | fail | 160 | AssertionError: [midsent_088_p3] Expected likely_continuation: 'The locksmith replaced all the...' -> 'locks in the apartment building for secu...' |
| `test_likely_continuation[midsent_088_p6]` | fail | 166 | AssertionError: [midsent_088_p6] Expected likely_continuation: 'The locksmith replaced all the locks in ...' -> 'apartment building for security...' |
| `test_likely_continuation[midsent_088_p7]` | fail | 167 | AssertionError: [midsent_088_p7] Expected likely_continuation: 'The locksmith replaced all the locks in ...' -> 'building for security...' |
| `test_likely_continuation[midsent_090_p0]` | fail | 171 | AssertionError: [midsent_090_p0] Expected likely_continuation: 'The janitor...' -> 'maintained the building in excellent con...' |
| `test_likely_continuation[midsent_090_p6]` | fail | 186 | AssertionError: [midsent_090_p6] Expected likely_continuation: 'The janitor maintained the building in e...' -> 'throughout the year...' |
| `test_likely_continuation[midsent_094_p0]` | fail | 146 | AssertionError: [midsent_094_p0] Expected likely_continuation: 'The florist...' -> 'arranged beautiful bouquets for the rece...' |
| `test_likely_continuation[midsent_098_p0]` | fail | 393 | AssertionError: [midsent_098_p0] Expected likely_continuation: 'The dispatcher...' -> 'coordinated emergency response teams acr...' |
| `test_likely_continuation[midsent_104_p0]` | fail | 165 | AssertionError: [midsent_104_p0] Expected likely_continuation: 'The tax...' -> 'auditor reviewed the corporation's finan...' |
| `test_likely_continuation[midsent_106_p1]` | fail | 171 | AssertionError: [midsent_106_p1] Expected likely_continuation: 'The crane operator...' -> 'lifted the steel girder into position on...' |
| `test_likely_continuation[midsent_115_p6]` | fail | 163 | AssertionError: [midsent_115_p6] Expected likely_continuation: 'Construction crews poured the concrete f...' -> 'community sports center...' |
| `test_likely_continuation[midsent_120_p6]` | fail | 167 | AssertionError: [midsent_120_p6] Expected likely_continuation: 'The stonecutter shaped blocks of granite...' -> 'restoration of the cathedral...' |
| `test_likely_continuation[midsent_121_p0]` | fail | 164 | AssertionError: [midsent_121_p0] Expected likely_continuation: 'Rangers cleared...' -> 'fallen trees from the hiking trail after...' |
| `test_likely_continuation[midsent_124_p0]` | fail | 158 | AssertionError: [midsent_124_p0] Expected likely_continuation: 'The blacksmith...' -> 'forged iron tools using traditional meth...' |
| `test_likely_continuation[midsent_125_p6]` | fail | 167 | AssertionError: [midsent_125_p6] Expected likely_continuation: 'Conservationists released rehabilitated ...' -> 'warm ocean...' |
| `test_likely_continuation[midsent_128_p0]` | fail | 166 | AssertionError: [midsent_128_p0] Expected likely_continuation: 'The shepherd...' -> 'counted the flock carefully before leadi...' |

## Slowest 30 tests

| # | Time (ms) | Status | Test |
|---:|---:|---|---|
| 1 | 413 | pass | `tests.test_continuation::test_likely_continuation[midsent_081_p4]` |
| 2 | 407 | pass | `tests.test_continuation::test_likely_continuation[midsent_083_p1]` |
| 3 | 397 | pass | `tests.test_continuation::test_likely_continuation[midsent_071_p3]` |
| 4 | 397 | pass | `tests.test_continuation::test_likely_continuation[midsent_091_p1]` |
| 5 | 395 | pass | `tests.test_continuation::test_likely_continuation[midsent_130_p0]` |
| 6 | 393 | fail | `tests.test_continuation::test_likely_continuation[midsent_098_p0]` |
| 7 | 389 | pass | `tests.test_continuation::test_likely_continuation[midsent_097_p0]` |
| 8 | 378 | pass | `tests.test_continuation::test_likely_continuation[midsent_000_p0]` |
| 9 | 316 | pass | `tests.test_continuation::test_likely_continuation[midsent_132_p2]` |
| 10 | 252 | pass | `tests.test_continuation::test_likely_continuation[midsent_119_p5]` |
| 11 | 201 | pass | `tests.test_continuation::test_likely_continuation[midsent_107_p1]` |
| 12 | 197 | pass | `tests.test_continuation::test_likely_continuation[midsent_096_p5]` |
| 13 | 192 | pass | `tests.test_continuation::test_likely_continuation[midsent_075_p2]` |
| 14 | 188 | fail | `tests.test_continuation::test_likely_continuation[midsent_070_p0]` |
| 15 | 186 | fail | `tests.test_continuation::test_likely_continuation[midsent_090_p6]` |
| 16 | 183 | pass | `tests.test_continuation::test_likely_continuation[midsent_082_p5]` |
| 17 | 183 | pass | `tests.test_continuation::test_likely_continuation[midsent_091_p2]` |
| 18 | 183 | pass | `tests.test_continuation::test_likely_continuation[midsent_098_p1]` |
| 19 | 182 | pass | `tests.test_continuation::test_likely_continuation[midsent_067_p0]` |
| 20 | 181 | pass | `tests.test_continuation::test_likely_continuation[midsent_075_p1]` |
| 21 | 180 | pass | `tests.test_continuation::test_likely_continuation[midsent_039_p7]` |
| 22 | 180 | pass | `tests.test_continuation::test_likely_continuation[midsent_064_p4]` |
| 23 | 180 | pass | `tests.test_continuation::test_likely_continuation[midsent_075_p0]` |
| 24 | 180 | pass | `tests.test_continuation::test_likely_continuation[midsent_082_p4]` |
| 25 | 180 | pass | `tests.test_continuation::test_likely_continuation[midsent_098_p4]` |
| 26 | 179 | pass | `tests.test_continuation::test_likely_continuation[midsent_082_p6]` |
| 27 | 179 | pass | `tests.test_continuation::test_likely_continuation[midsent_098_p5]` |
| 28 | 178 | pass | `tests.test_continuation::test_likely_continuation[midsent_038_p6]` |
| 29 | 178 | pass | `tests.test_continuation::test_likely_continuation[midsent_059_p6]` |
| 30 | 178 | pass | `tests.test_continuation::test_likely_continuation[midsent_076_p6]` |
