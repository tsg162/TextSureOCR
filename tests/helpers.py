"""
Shared helper functions for TextSureOCR integration tests.

Debug mode: use pytest --debug or --debug-log=FILE
"""

import json
import os
import requests

BASE_URL = os.getenv("TEXTSURE_URL", "http://localhost:5002")

# Set by conftest.py based on --debug / --debug-log args
DEBUG_MODE = False
_debug_file = None


def _log(msg: str) -> None:
    """Print to stdout and optionally to debug log file."""
    print(msg)
    if _debug_file:
        _debug_file.write(msg + "\n")
        _debug_file.flush()


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


def print_beam_debug(result: dict, test_id: str = "", expected_word: str = "", expected_correction: str = "", input_text: str = "") -> None:
    """Print verbose beam search debug info to stdout and log file."""
    debug = result.get("debug", {})
    beam_search = debug.get("beam_search", {})

    if not beam_search:
        _log(f"\n[{test_id}] NO BEAM SEARCH DEBUG")
        return

    _log(f"\n{'='*70}")
    _log(f"TEST: {test_id}")
    if input_text:
        _log(f"TEXT: {input_text}")
    if expected_word:
        _log(f"ERROR_WORD: '{expected_word}'")
        _log(f"EXPECTED: '{expected_correction}'")
    _log(f"{'='*70}")

    orig_lp = beam_search.get("original_log_prob", 0.0)
    _log(f"\nORIGINAL LOG-PROB: {orig_lp:.2f}")

    patterns = beam_search.get("patterns_found", [])
    _log(f"\nPATTERNS FOUND: {len(patterns)}")
    for i, p in enumerate(patterns):
        _log(f"  [{i}] '{p.get('original_text', '')}' @ {p.get('start')}-{p.get('end')}")
        _log(f"      key='{p.get('pattern_key', '')}' → {p.get('replacements', [])}")

    final_beams = beam_search.get("final_beam_states", [])
    _log(f"\nFINAL BEAMS: {len(final_beams)} (top 10 shown)")
    for i, beam in enumerate(final_beams[:10]):
        is_orig = beam.get("is_original", False)
        lp = beam.get("log_prob", 0.0)
        diff = lp - orig_lp
        marker = "← ORIG" if is_orig else ""
        winner = "★" if i == 0 else " "

        corrections = beam.get("corrections", [])
        corr_str = ", ".join(f"'{o}'→'{r}'" for _, _, o, r in corrections) if corrections else "(none)"

        _log(f"  {winner}[{i}] Δ={diff:+.1f} | {corr_str} {marker}")

    improvement = beam_search.get("improvement_over_original", 0.0)
    _log(f"\nBEST IMPROVEMENT: {improvement:.2f} nats")

    # Check if expected correction is in beams
    if expected_correction:
        found = False
        for beam in final_beams:
            corrected = beam.get("corrected_text", "").lower()
            if expected_correction.lower() in corrected:
                found = True
                break
        _log(f"EXPECTED '{expected_correction}' IN BEAMS: {'YES' if found else 'NO'}")
    _log("")
