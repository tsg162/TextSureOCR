"""
TextSureOCR test battery.

Runs against a live service (default: http://localhost:5002).
Each test is a dict with input, expected result, and a human-readable name.
Exit code = number of failures.

Usage:
    python tests.py                        # against localhost:5002
    python tests.py https://some.host:5002 # against a remote URL
"""

import sys
import os
import json
import time
import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5002"
AUTH_TOKEN = os.getenv("TEXTSURE_AUTH_TOKEN", "")
HEADERS = {"Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else {}

# ── Test definitions ───────────────────────────────────────────────────

OCR_TESTS = [
    # ── True positives: should detect errors ──
    {
        "name": "single digit sub (br0wn)",
        "text": "The quick br0wn fox jumps over the lazy dog",
        "expect_result": "issue_detected",
        "expect_spans": [{"text": "br0wn", "suggestion": "brown"}],
    },
    {
        "name": "multiple digit subs (heavy leet)",
        "text": "H3llo w0rld, th1s is a t3st of 0CR detect1on",
        "expect_result": "issue_detected",
        "expect_min_spans": 3,  # model-only: per-word scoring limited in uniformly corrupted text
    },
    {
        "name": "single error in clean context (p0lice)",
        "text": "The p0lice stopped 3 cars on Interstate 95",
        "expect_result": "issue_detected",
        "expect_spans": [{"text": "p0lice", "suggestion": "police"}],
        "expect_no_spans": ["3", "95", "Interstate"],
    },
    {
        "name": "rn→m confusion (governrnent)",
        "text": "The governrnent announced new policies for the nation",
        "expect_result": "issue_detected",
        "expect_spans": [{"text": "governrnent", "suggestion": "government"}],
    },
    {
        "name": "zero for O (c0mputer)",
        "text": "The c0mputer crashed during the presentation yesterday",
        "expect_result": "issue_detected",
        "expect_spans": [{"text": "c0mputer", "suggestion": "computer"}],
    },
    {
        "name": "one for l (1etter)",
        "text": "Please send the 1etter to the main office today",
        "expect_result": "issue_detected",
        "expect_spans": [{"text": "1etter", "suggestion": "letter"}],
    },
    {
        "name": "five for S (5chool)",
        "text": "The children walked to 5chool every morning",
        "expect_result": "issue_detected",
        "expect_spans": [{"text": "5chool", "suggestion": "school"}],
    },
    {
        "name": "garbled word (teh → the)",
        "text": "She opened teh door and walked inside quietly",
        "expect_result": "issue_detected",
        "expect_spans": [{"text": "teh", "suggestion": "the"}],
    },

    # ── True negatives: should NOT detect errors ──
    {
        "name": "clean prose",
        "text": "The quick brown fox jumps over the lazy dog",
        "expect_result": "ok",
    },
    {
        "name": "legitimate numbers only",
        "text": "I bought 3 apples and 2 oranges at the store",
        "expect_result": "ok",
    },
    {
        "name": "technical with numbers",
        "text": "The server runs on port 8080 with 4 CPU cores",
        "expect_result": "ok",
    },
    {
        "name": "acronyms and abbreviations",
        "text": "The CEO of IBM met with the FBI in Washington DC",
        "expect_result": "ok",
    },
    {
        "name": "date and time",
        "text": "The meeting is scheduled for March 15 at 3 PM",
        "expect_result": "ok",
    },
    {
        "name": "proper nouns",
        "text": "John Smith visited the Eiffel Tower in Paris last summer",
        "expect_result": "ok",
    },
    {
        "name": "all caps heading",
        "text": "ANNUAL REPORT FOR THE FISCAL YEAR ENDING DECEMBER",
        "expect_result": "ok",
    },
    {
        "name": "currency and measurements",
        "text": "The total cost was $500 for 10 kg of premium material",
        "expect_result": "ok",
    },
]

CONTINUATION_TESTS = [
    # ── Likely continuations ──
    {
        "name": "natural sentence split",
        "first": "The quick brown fox jumps",
        "second": "over the lazy dog",
        "expect_result": "likely_continuation",
        "expect_score_above": 0.8,
    },
    {
        "name": "sentence boundary",
        "first": "Please send the report to",
        "second": "my email address today.",
        "expect_result": "likely_continuation",
        "expect_score_above": 0.7,
    },
    {
        "name": "paragraph continuation",
        "first": "The rain had been falling for three days straight.",
        "second": "Rivers overflowed their banks and roads became impassable.",
        "expect_result": "likely_continuation",
        "expect_score_above": 0.5,
    },
    {
        "name": "mid-word line break (hypothet-ical)",
        "first": "The committee discussed the hypothet",
        "second": "ical scenario at length during the session.",
        "expect_result": "likely_continuation",
        "expect_score_above": 0.5,
    },
    {
        "name": "enumeration continuation",
        "first": "The ingredients include flour, sugar,",
        "second": "butter, eggs, and vanilla extract.",
        "expect_result": "likely_continuation",
        "expect_score_above": 0.5,
    },

    # ── Unlikely continuations ──
    {
        "name": "random gibberish",
        "first": "The quick brown fox",
        "second": "banana elephant purple mathematics",
        "expect_result": "unlikely_continuation",
        "expect_score_below": 0.2,
    },
    {
        "name": "cross-column discontinuity",
        "first": "The annual revenue exceeded",
        "second": "In other news the mayor",
        "expect_result": "unlikely_continuation",
        "expect_score_below": 0.3,
    },
    {
        "name": "language switch",
        "first": "The committee voted unanimously to",
        "second": "les enfants jouent dans le jardin",
        "expect_result": "unlikely_continuation",
        "expect_score_below": 0.3,
    },
    {
        "name": "topic whiplash",
        "first": "Photosynthesis converts carbon dioxide",
        "second": "The stock market closed at record highs today",
        "expect_result": "unlikely_continuation",
        "expect_score_below": 0.3,
    },
    {
        "name": "reversed text",
        "first": "The weather forecast predicted",
        "second": "predicted forecast weather The",
        "expect_result": "unlikely_continuation",
        "expect_score_below": 0.3,
    },
]

# ── Runner ─────────────────────────────────────────────────────────────

def check_ocr(test: dict) -> tuple[bool, str]:
    """Run one OCR test. Returns (passed, details)."""
    r = requests.post(
        f"{BASE}/v1/ocr/check",
        json={"text": test["text"]},
        headers=HEADERS,
        timeout=120,
    )
    if r.status_code != 200:
        return False, f"HTTP {r.status_code}: {r.text}"
    body = r.json()
    problems = []

    # Check result
    if "expect_result" in test and body["result"] != test["expect_result"]:
        problems.append(
            f'result: got "{body["result"]}", want "{test["expect_result"]}"'
        )

    # Check expected spans
    if "expect_spans" in test:
        span_texts = {s["text"] for s in body.get("spans", [])}
        for expect in test["expect_spans"]:
            if expect["text"] not in span_texts:
                problems.append(f'missing span: "{expect["text"]}"')
            elif "suggestion" in expect:
                span = next(s for s in body["spans"] if s["text"] == expect["text"])
                sugg_texts = {s["text"] for s in span.get("suggestions", [])}
                if expect["suggestion"] not in sugg_texts:
                    problems.append(
                        f'"{expect["text"]}": missing suggestion '
                        f'"{expect["suggestion"]}" (got {sugg_texts})'
                    )

    # Check minimum span count
    if "expect_min_spans" in test:
        actual = len(body.get("spans", []))
        if actual < test["expect_min_spans"]:
            problems.append(
                f"span count: got {actual}, want >= {test['expect_min_spans']}"
            )

    # Check words that should NOT be flagged
    if "expect_no_spans" in test:
        span_texts = {s["text"] for s in body.get("spans", [])}
        for bad in test["expect_no_spans"]:
            # Check if any span contains this word
            for st in span_texts:
                if bad in st:
                    problems.append(f'false positive: "{bad}" should not be flagged')

    if problems:
        return False, "; ".join(problems) + f"\n    Response: {json.dumps(body, indent=2)}"
    return True, f'result={body["result"]} score={body["score"]} spans={len(body.get("spans", []))}'


def check_continuation(test: dict) -> tuple[bool, str]:
    """Run one continuation test. Returns (passed, details)."""
    r = requests.post(
        f"{BASE}/v1/text/check-continuation",
        json={"first": test["first"], "second": test["second"]},
        headers=HEADERS,
        timeout=120,
    )
    if r.status_code != 200:
        return False, f"HTTP {r.status_code}: {r.text}"
    body = r.json()
    problems = []

    if "expect_result" in test and body["result"] != test["expect_result"]:
        problems.append(
            f'result: got "{body["result"]}", want "{test["expect_result"]}"'
        )
    if "expect_score_above" in test and body["score"] < test["expect_score_above"]:
        problems.append(
            f'score {body["score"]} < {test["expect_score_above"]}'
        )
    if "expect_score_below" in test and body["score"] > test["expect_score_below"]:
        problems.append(
            f'score {body["score"]} > {test["expect_score_below"]}'
        )

    if problems:
        return False, "; ".join(problems) + f"\n    Response: {json.dumps(body)}"
    return True, f'result={body["result"]} score={body["score"]}'


def main():
    print(f"TextSureOCR Test Battery — {BASE}")
    print(f"{'=' * 70}\n")

    # Health check
    try:
        h = requests.get(f"{BASE}/health", timeout=10)
        info = h.json()
        print(f"Service: {info.get('model', '?')} on {info.get('device', '?')}")
        print(f"Model loaded: {info.get('model_loaded', '?')}\n")
    except Exception as e:
        print(f"FATAL: Cannot reach {BASE}/health — {e}")
        sys.exit(1)

    passed = 0
    failed = 0
    failures = []
    t0 = time.time()

    # OCR tests
    print(f"── OCR Check ({len(OCR_TESTS)} tests) ──\n")
    for test in OCR_TESTS:
        t1 = time.time()
        ok, detail = check_ocr(test)
        dt = time.time() - t1
        tag = "PASS" if ok else "FAIL"
        icon = "  " if ok else "* "
        print(f"  {icon}[{tag}] {test['name']} ({dt:.1f}s)")
        if ok:
            print(f"         {detail}")
            passed += 1
        else:
            print(f"         {detail}")
            failed += 1
            failures.append(test["name"])
        print()

    # Continuation tests
    print(f"── Continuation Check ({len(CONTINUATION_TESTS)} tests) ──\n")
    for test in CONTINUATION_TESTS:
        t1 = time.time()
        ok, detail = check_continuation(test)
        dt = time.time() - t1
        tag = "PASS" if ok else "FAIL"
        icon = "  " if ok else "* "
        print(f"  {icon}[{tag}] {test['name']} ({dt:.1f}s)")
        if ok:
            print(f"         {detail}")
            passed += 1
        else:
            print(f"         {detail}")
            failed += 1
            failures.append(test["name"])
        print()

    # Summary
    total = passed + failed
    elapsed = time.time() - t0
    print("=" * 70)
    print(f"  {passed}/{total} passed, {failed} failed  ({elapsed:.1f}s total)")
    if failures:
        print(f"\n  Failures:")
        for f in failures:
            print(f"    - {f}")
    print("=" * 70)

    sys.exit(failed)


if __name__ == "__main__":
    main()
