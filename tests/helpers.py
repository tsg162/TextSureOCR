"""
Shared helper functions for TextSureOCR integration tests.

These are plain functions (not fixtures) that test files import directly.

Debug mode: set TEXTSURE_DEBUG=1 to get verbose beam search output on failures.
"""

import json
import os
import requests

BASE_URL = os.getenv("TEXTSURE_URL", "http://localhost:5002")
DEBUG_MODE = os.getenv("TEXTSURE_DEBUG", "").lower() in ("1", "true", "yes")


def ocr_check(api, text: str, debug: bool = None) -> dict:
    """POST /v1/ocr/check and return parsed JSON."""
    use_debug = debug if debug is not None else DEBUG_MODE
    r = api.post(
        f"{api.base_url}/v1/ocr/check",
        json={"text": text, "debug": use_debug},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()


def continuation_check(api, first: str, second: str, debug: bool = None) -> dict:
    """POST /v1/text/check-continuation and return parsed JSON."""
    use_debug = debug if debug is not None else DEBUG_MODE
    r = api.post(
        f"{api.base_url}/v1/text/check-continuation",
        json={"first": first, "second": second, "debug": use_debug},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()


def print_beam_debug(result: dict, test_id: str = "", expected_word: str = "", expected_correction: str = "") -> None:
    """Print verbose beam search debug info."""
    debug = result.get("debug", {})
    beam_search = debug.get("beam_search", {})

    if not beam_search:
        print(f"\n[{test_id}] NO BEAM SEARCH DEBUG")
        return

    print(f"\n{'='*70}")
    print(f"TEST: {test_id}")
    if expected_word:
        print(f"EXPECTED: '{expected_word}' → '{expected_correction}'")
    print(f"{'='*70}")

    orig_lp = beam_search.get("original_log_prob", 0.0)
    print(f"\nORIGINAL LOG-PROB: {orig_lp:.2f}")

    patterns = beam_search.get("patterns_found", [])
    print(f"\nPATTERNS FOUND: {len(patterns)}")
    for i, p in enumerate(patterns):
        print(f"  [{i}] '{p.get('original_text', '')}' @ {p.get('start')}-{p.get('end')}")
        print(f"      key='{p.get('pattern_key', '')}' → {p.get('replacements', [])}")

    final_beams = beam_search.get("final_beam_states", [])
    print(f"\nFINAL BEAMS: {len(final_beams)} (top 10 shown)")
    for i, beam in enumerate(final_beams[:10]):
        is_orig = beam.get("is_original", False)
        lp = beam.get("log_prob", 0.0)
        diff = lp - orig_lp
        marker = "← ORIG" if is_orig else ""
        winner = "★" if i == 0 else " "

        corrections = beam.get("corrections", [])
        corr_str = ", ".join(f"'{o}'→'{r}'" for _, _, o, r in corrections) if corrections else "(none)"

        print(f"  {winner}[{i}] Δ={diff:+.1f} | {corr_str} {marker}")

    improvement = beam_search.get("improvement_over_original", 0.0)
    print(f"\nBEST IMPROVEMENT: {improvement:.2f} nats")

    # Check if expected correction is in beams
    if expected_correction:
        found = False
        for beam in final_beams:
            corrected = beam.get("corrected_text", "").lower()
            if expected_correction.lower() in corrected:
                found = True
                break
        print(f"EXPECTED '{expected_correction}' IN BEAMS: {'YES' if found else 'NO'}")
    print()
