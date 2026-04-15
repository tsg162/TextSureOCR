#!/usr/bin/env python3
"""
Batch debug script for analyzing TextSureOCR test failures.

Run all failing test cases with debug=True and collect detailed results
to understand why specific errors are missed or false positives occur.

Usage:
    python scripts/analyze_failures.py --test-file tests/test_ocr_tp_structural.py
    python scripts/analyze_failures.py --test-ids hard_misc_1,hard_misc_6
    python scripts/analyze_failures.py --all
    python scripts/analyze_failures.py --continuation  # Analyze continuation tests

Outputs:
    - failures_debug.jsonl      # One JSON object per test case
    - failures_summary.md       # Human-readable summary report
"""

import argparse
import importlib.util
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import requests

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def _load_textsureocr_config() -> tuple[str, str]:
    """Load URL and token from ~/.textsureocr/servers.yaml if available."""
    config_path = Path.home() / ".textsureocr" / "servers.yaml"
    if not config_path.exists():
        return "", ""
    try:
        import yaml
        with open(config_path) as f:
            cfg = yaml.safe_load(f) or {}
        default_name = cfg.get("defaults", {}).get("server", "")
        servers = cfg.get("servers", {})
        if default_name and default_name in servers:
            srv = servers[default_name]
            return srv.get("url", ""), srv.get("token", "")
        elif servers:
            # Use first server if no default
            srv = next(iter(servers.values()))
            return srv.get("url", ""), srv.get("token", "")
    except Exception:
        pass
    return "", ""

_cfg_url, _cfg_token = _load_textsureocr_config()
BASE_URL = os.getenv("TEXTSURE_URL") or _cfg_url or "http://localhost:5002"
AUTH_TOKEN = os.getenv("TEXTSURE_AUTH_TOKEN") or _cfg_token or ""


@dataclass
class TestCase:
    """A single OCR test case."""
    test_id: str
    text: str
    error_word: str
    expected_correction: str
    category: str = ""


@dataclass
class ContinuationTestCase:
    """A single continuation test case."""
    test_id: str
    first: str
    second: str
    expected_result: str  # "likely_continuation" or "unlikely_continuation"
    category: str = ""


@dataclass
class FailureAnalysis:
    """Analysis of why a test case failed."""
    test_id: str
    category: str
    input_text: str
    expected_error_word: str
    expected_correction: str

    # Result from API
    api_result: str  # "ok" or "issue_detected"
    api_score: float
    spans: list[dict] = field(default_factory=list)
    debug_info: dict | None = None

    # Analysis
    word_found: bool = False
    word_flagged: bool = False
    reason: str = ""
    original_score: float = 0.0
    correction_score: float = 0.0
    log_prob_improvement: float = 0.0
    tokenization_original: list[str] = field(default_factory=list)
    tokenization_correction: list[str] = field(default_factory=list)


@dataclass
class ContinuationFailureAnalysis:
    """Analysis of why a continuation test case failed."""
    test_id: str
    category: str
    first: str
    second: str
    expected_result: str

    # Result from API
    api_result: str
    api_score: float
    debug_info: dict | None = None

    # Analysis
    reason: str = ""


def load_test_cases_from_file(filepath: str) -> list[TestCase]:
    """Load test cases from a Python test file."""
    test_cases = []

    # Load the module
    spec = importlib.util.spec_from_file_location("test_module", filepath)
    module = importlib.util.module_from_spec(spec)

    # Read the file content to extract test case data
    with open(filepath, "r") as f:
        content = f.read()

    # Find all test case lists (e.g., CHAR_RN_M_CASES = [...])
    pattern = r'(\w+_CASES)\s*=\s*\[(.*?)\]'
    matches = re.findall(pattern, content, re.DOTALL)

    for list_name, list_content in matches:
        # Parse individual tuples
        tuple_pattern = r'\(\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)"\s*\)'
        tuples = re.findall(tuple_pattern, list_content)

        category = list_name.replace("_CASES", "").lower()
        for text, error_word, correction, test_id in tuples:
            test_cases.append(TestCase(
                test_id=test_id,
                text=text,
                error_word=error_word,
                expected_correction=correction,
                category=category,
            ))

    return test_cases


def load_continuation_test_cases(filepath: str) -> list[ContinuationTestCase]:
    """Load continuation test cases from a Python test file.

    Handles both static lists and dynamically generated test cases by
    actually importing the module.
    """
    test_cases = []
    filepath = Path(filepath)

    # Add test directory to path for imports (helpers.py etc)
    test_dir = filepath.parent
    if str(test_dir) not in sys.path:
        sys.path.insert(0, str(test_dir))

    try:
        # Import the module to get generated test cases
        spec = importlib.util.spec_from_file_location("cont_test", str(filepath))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Try LIKELY_CASES / UNLIKELY_CASES (4-tuples: first, second, score, test_id)
        if hasattr(module, "LIKELY_CASES"):
            for item in module.LIKELY_CASES:
                first, second, score, test_id = item
                test_cases.append(ContinuationTestCase(
                    test_id=test_id,
                    first=first,
                    second=second,
                    expected_result="likely_continuation",
                    category="likely",
                ))

        if hasattr(module, "UNLIKELY_CASES"):
            for item in module.UNLIKELY_CASES:
                first, second, score, test_id = item
                test_cases.append(ContinuationTestCase(
                    test_id=test_id,
                    first=first,
                    second=second,
                    expected_result="unlikely_continuation",
                    category="unlikely",
                ))

        # Fallback: POSITIVE_CASES / NEGATIVE_CASES (3-tuples)
        if not test_cases:
            if hasattr(module, "POSITIVE_CASES"):
                for item in module.POSITIVE_CASES:
                    first, second, test_id = item
                    test_cases.append(ContinuationTestCase(
                        test_id=test_id,
                        first=first,
                        second=second,
                        expected_result="likely_continuation",
                        category="positive",
                    ))

            if hasattr(module, "NEGATIVE_CASES"):
                for item in module.NEGATIVE_CASES:
                    first, second, test_id = item
                    test_cases.append(ContinuationTestCase(
                        test_id=test_id,
                        first=first,
                        second=second,
                        expected_result="unlikely_continuation",
                        category="negative",
                    ))

    except Exception as e:
        print(f"Warning: Could not import {filepath}: {e}")

    return test_cases


def _headers() -> dict:
    """Build request headers with auth if configured."""
    h = {"Content-Type": "application/json"}
    if AUTH_TOKEN:
        h["Authorization"] = f"Bearer {AUTH_TOKEN}"
    return h


def run_ocr_check(text: str, debug: bool = False) -> dict:
    """Call the OCR check endpoint."""
    r = requests.post(
        f"{BASE_URL}/v1/ocr/check",
        json={"text": text, "debug": debug},
        headers=_headers(),
        timeout=120,
    )
    r.raise_for_status()
    return r.json()


def run_continuation_check(first: str, second: str, debug: bool = False) -> dict:
    """Call the continuation check endpoint."""
    r = requests.post(
        f"{BASE_URL}/v1/text/check-continuation",
        json={"first": first, "second": second, "debug": debug},
        headers=_headers(),
        timeout=120,
    )
    r.raise_for_status()
    return r.json()


def analyze_ocr_failure(test_case: TestCase, result: dict) -> FailureAnalysis:
    """Analyze why an OCR test case failed using beam search debug info."""
    debug_info = result.get("debug", {})
    beam_search = debug_info.get("beam_search", {}) if debug_info else {}

    analysis = FailureAnalysis(
        test_id=test_case.test_id,
        category=test_case.category,
        input_text=test_case.text,
        expected_error_word=test_case.error_word,
        expected_correction=test_case.expected_correction,
        api_result=result.get("result", "ok"),
        api_score=result.get("score", 0.0),
        spans=result.get("spans", []),
        debug_info=debug_info,
    )

    if not beam_search:
        analysis.word_found = False
        analysis.reason = "no_beam_search_debug"
        return analysis

    # Check if any patterns were found that could lead to our expected correction
    patterns = beam_search.get("patterns_found", [])
    error_word_patterns = []
    for p in patterns:
        # Check if pattern is within the error word's position in the text
        pat_text = test_case.text[p.get("start", 0):p.get("end", 0)]
        if test_case.error_word.lower().find(p.get("pattern_key", "").lower()) >= 0:
            error_word_patterns.append(p)

    if not patterns:
        analysis.word_found = False
        analysis.reason = "no_patterns_found"
        return analysis

    analysis.word_found = True  # Patterns were found and analyzed

    # Check final beams for our expected correction
    final_beams = beam_search.get("final_beam_states", [])
    original_log_prob = beam_search.get("original_log_prob", 0.0)
    analysis.original_score = original_log_prob

    # Look for a beam that produces the expected correction
    best_beam = final_beams[0] if final_beams else None
    expected_beam = None

    for beam in final_beams:
        corrections = beam.get("corrections", [])
        # Check if any correction produces the expected result
        for start, end, orig, repl in corrections:
            if orig.lower() == test_case.error_word.lower() or \
               (test_case.error_word.lower() in test_case.text[start:end].lower()):
                if repl.lower() == test_case.expected_correction.lower():
                    expected_beam = beam
                    break
        if expected_beam:
            break

    # Also check corrected_text for the expected correction
    if not expected_beam:
        for beam in final_beams:
            corrected = beam.get("corrected_text", "")
            if test_case.expected_correction.lower() in corrected.lower() and \
               test_case.error_word.lower() not in corrected.lower():
                expected_beam = beam
                break

    if expected_beam:
        analysis.correction_score = expected_beam.get("log_prob", 0.0)
        analysis.log_prob_improvement = analysis.correction_score - original_log_prob

        # Check if it was the best beam
        if best_beam and best_beam.get("beam_id") == expected_beam.get("beam_id"):
            analysis.word_flagged = True
            analysis.reason = "flagged_correctly"
        else:
            # Expected correction exists but wasn't chosen
            best_lp = best_beam.get("log_prob", 0.0) if best_beam else 0.0
            expected_lp = expected_beam.get("log_prob", 0.0)
            if best_beam and best_beam.get("is_original"):
                analysis.reason = f"original_beat_correction (orig={original_log_prob:.2f}, corr={expected_lp:.2f})"
            else:
                analysis.reason = f"wrong_correction_chosen (best={best_lp:.2f}, expected={expected_lp:.2f})"
    else:
        # Expected correction wasn't in any beam
        # Check if pattern was even found
        found_relevant_pattern = False
        for p in patterns:
            key = p.get("pattern_key", "")
            # Check common OCR patterns that could produce this correction
            if key in test_case.error_word.lower():
                found_relevant_pattern = True
                break

        if not found_relevant_pattern:
            analysis.reason = f"pattern_not_detected (error_word='{test_case.error_word}')"
        else:
            # Pattern found but correction not generated
            analysis.reason = f"correction_not_in_beams (patterns={len(patterns)}, beams={len(final_beams)})"

    return analysis


def analyze_continuation_failure(test_case: ContinuationTestCase, result: dict) -> ContinuationFailureAnalysis:
    """Analyze why a continuation test case failed."""
    debug_info = result.get("debug", {})

    analysis = ContinuationFailureAnalysis(
        test_id=test_case.test_id,
        category=test_case.category,
        first=test_case.first,
        second=test_case.second,
        expected_result=test_case.expected_result,
        api_result=result.get("result", ""),
        api_score=result.get("score", 0.0),
        debug_info=debug_info,
    )

    # Determine failure reason
    if test_case.expected_result == "likely_continuation" and result.get("result") == "unlikely_continuation":
        if debug_info:
            pmi = debug_info.get("pmi", 0)
            abs_score = debug_info.get("abs_score", 0)
            if pmi < 0.2:
                analysis.reason = f"low_pmi ({pmi:.3f})"
            elif abs_score < 0.5:
                analysis.reason = f"low_abs_score ({abs_score:.3f})"
            else:
                analysis.reason = f"combined_score_low (pmi={pmi:.3f}, abs={abs_score:.3f})"
    elif test_case.expected_result == "unlikely_continuation" and result.get("result") == "likely_continuation":
        if debug_info:
            pmi = debug_info.get("pmi", 0)
            abs_score = debug_info.get("abs_score", 0)
            analysis.reason = f"false_positive (pmi={pmi:.3f}, abs={abs_score:.3f})"

    return analysis


def generate_summary_report(
    analyses: list[FailureAnalysis],
    output_path: str,
) -> None:
    """Generate a markdown summary report."""
    # Categorize failures
    not_detected = [a for a in analyses if not a.word_found]
    fp_original_wins = [a for a in analyses if a.reason == "fp_original_wins"]
    fp_low_gain = [a for a in analyses if "fp_low_gain" in a.reason]
    no_candidates = [a for a in analyses if a.reason == "no_candidates"]
    filtered_out = [a for a in analyses if a.reason == "filtered_no_similar"]
    other = [a for a in analyses if a not in not_detected + fp_original_wins + fp_low_gain + no_candidates + filtered_out]

    with open(output_path, "w") as f:
        f.write("# Failure Analysis Report\n\n")

        f.write("## Summary\n")
        f.write(f"- Total failures: {len(analyses)}\n")
        f.write(f"- Word not analyzed: {len(not_detected)}\n")
        f.write(f"- Original wins scoring: {len(fp_original_wins)}\n")
        f.write(f"- Low log-prob improvement: {len(fp_low_gain)}\n")
        f.write(f"- No candidates generated: {len(no_candidates)}\n")
        f.write(f"- Filtered by similarity: {len(filtered_out)}\n")
        f.write(f"- Other: {len(other)}\n\n")

        # Category breakdown
        by_category = defaultdict(list)
        for a in analyses:
            by_category[a.category].append(a)

        f.write("## By Category\n")
        for cat, items in sorted(by_category.items()):
            f.write(f"- {cat}: {len(items)} failures\n")
        f.write("\n")

        f.write("## Failure Categories\n\n")

        # 1. Word Not Detected
        if not_detected:
            f.write("### 1. Word Not Analyzed\n")
            f.write("Words that should have been flagged but weren't even analyzed.\n\n")
            f.write("| Test ID | Word | Correction | Category |\n")
            f.write("|---------|------|------------|----------|\n")
            for a in not_detected[:50]:
                f.write(f"| {a.test_id} | {a.expected_error_word} | {a.expected_correction} | {a.category} |\n")
            if len(not_detected) > 50:
                f.write(f"\n*...and {len(not_detected) - 50} more*\n")
            f.write("\n")

        # 2. Original Wins Scoring
        if fp_original_wins:
            f.write("### 2. Original Wins Scoring\n")
            f.write("Word detected but original wins the scoring competition.\n\n")
            f.write("| Test ID | Word | Original Score | Correction Score | Improvement |\n")
            f.write("|---------|------|----------------|------------------|-------------|\n")
            for a in fp_original_wins[:50]:
                f.write(f"| {a.test_id} | {a.expected_error_word} | {a.original_score:.3f} | {a.correction_score:.3f} | {a.log_prob_improvement:.1f} |\n")
            if len(fp_original_wins) > 50:
                f.write(f"\n*...and {len(fp_original_wins) - 50} more*\n")
            f.write("\n")

        # 3. Low Log-Prob Improvement
        if fp_low_gain:
            f.write("### 3. Low Log-Prob Improvement\n")
            f.write("Correction scored higher but improvement below threshold.\n\n")
            f.write("| Test ID | Word | Improvement | Tokenization |\n")
            f.write("|---------|------|-------------|---------------|\n")
            for a in fp_low_gain[:50]:
                tok = " ".join(a.tokenization_original) if a.tokenization_original else "N/A"
                f.write(f"| {a.test_id} | {a.expected_error_word} | {a.log_prob_improvement:.1f} | {tok} |\n")
            if len(fp_low_gain) > 50:
                f.write(f"\n*...and {len(fp_low_gain) - 50} more*\n")
            f.write("\n")

        # 4. No Candidates
        if no_candidates:
            f.write("### 4. No Candidates Generated\n")
            f.write("Word detected but no correction candidates could be generated.\n\n")
            f.write("| Test ID | Word | Expected Correction |\n")
            f.write("|---------|------|---------------------|\n")
            for a in no_candidates[:50]:
                f.write(f"| {a.test_id} | {a.expected_error_word} | {a.expected_correction} |\n")
            if len(no_candidates) > 50:
                f.write(f"\n*...and {len(no_candidates) - 50} more*\n")
            f.write("\n")

        # 5. Filtered Out
        if filtered_out:
            f.write("### 5. Filtered by Similarity/Shape\n")
            f.write("Candidates were generated but filtered out.\n\n")
            f.write("| Test ID | Word | Expected Correction |\n")
            f.write("|---------|------|---------------------|\n")
            for a in filtered_out[:50]:
                f.write(f"| {a.test_id} | {a.expected_error_word} | {a.expected_correction} |\n")
            if len(filtered_out) > 50:
                f.write(f"\n*...and {len(filtered_out) - 50} more*\n")
            f.write("\n")


def generate_continuation_summary(
    analyses: list[ContinuationFailureAnalysis],
    output_path: str,
) -> None:
    """Generate a markdown summary report for continuation failures."""
    false_negatives = [a for a in analyses if a.expected_result == "likely_continuation"]
    false_positives = [a for a in analyses if a.expected_result == "unlikely_continuation"]

    with open(output_path, "w") as f:
        f.write("# Continuation Failure Analysis Report\n\n")

        f.write("## Summary\n")
        f.write(f"- Total failures: {len(analyses)}\n")
        f.write(f"- False negatives (should be likely, got unlikely): {len(false_negatives)}\n")
        f.write(f"- False positives (should be unlikely, got likely): {len(false_positives)}\n\n")

        if false_negatives:
            f.write("## False Negatives\n\n")
            f.write("| Test ID | Score | PMI | Abs Score | First | Second |\n")
            f.write("|---------|-------|-----|-----------|-------|--------|\n")
            for a in false_negatives[:50]:
                debug = a.debug_info or {}
                pmi = debug.get("pmi", 0)
                abs_s = debug.get("abs_score", 0)
                first_short = a.first[:30] + "..." if len(a.first) > 30 else a.first
                second_short = a.second[:30] + "..." if len(a.second) > 30 else a.second
                f.write(f"| {a.test_id} | {a.api_score:.3f} | {pmi:.3f} | {abs_s:.3f} | {first_short} | {second_short} |\n")
            f.write("\n")

        if false_positives:
            f.write("## False Positives\n\n")
            f.write("| Test ID | Score | PMI | Abs Score | First | Second |\n")
            f.write("|---------|-------|-----|-----------|-------|--------|\n")
            for a in false_positives[:50]:
                debug = a.debug_info or {}
                pmi = debug.get("pmi", 0)
                abs_s = debug.get("abs_score", 0)
                first_short = a.first[:30] + "..." if len(a.first) > 30 else a.first
                second_short = a.second[:30] + "..." if len(a.second) > 30 else a.second
                f.write(f"| {a.test_id} | {a.api_score:.3f} | {pmi:.3f} | {abs_s:.3f} | {first_short} | {second_short} |\n")
            f.write("\n")


def print_verbose_beam_debug(test_case: TestCase, result: dict) -> None:
    """Print verbose beam search debug info for a test case."""
    debug = result.get("debug", {})
    beam_search = debug.get("beam_search", {})

    print(f"\n{'='*70}")
    print(f"TEST: {test_case.test_id}")
    print(f"INPUT: {test_case.text}")
    print(f"EXPECTED: '{test_case.error_word}' → '{test_case.expected_correction}'")
    print(f"{'='*70}")

    if not beam_search:
        print("  [NO BEAM SEARCH DEBUG INFO]")
        return

    # Original text score
    orig_lp = beam_search.get("original_log_prob", 0.0)
    print(f"\nORIGINAL LOG-PROB: {orig_lp:.2f}")

    # Patterns found
    patterns = beam_search.get("patterns_found", [])
    print(f"\nPATTERNS FOUND: {len(patterns)}")
    for i, p in enumerate(patterns):
        print(f"  [{i}] '{p.get('original_text', '')}' @ {p.get('start')}-{p.get('end')}")
        print(f"      pattern_key: '{p.get('pattern_key', '')}'")
        print(f"      replacements: {p.get('replacements', [])}")

    # Prune events
    prune_events = beam_search.get("prune_events", [])
    if prune_events:
        print(f"\nPRUNE EVENTS: {len(prune_events)}")
        for pe in prune_events:
            print(f"  after pattern {pe.get('after_pattern_idx')}: '{pe.get('pattern_key')}'")
            print(f"    beams: {pe.get('beams_before')} → {pe.get('beams_after')}")

    # Final beams
    final_beams = beam_search.get("final_beam_states", [])
    print(f"\nFINAL BEAMS: {len(final_beams)} (sorted by log-prob)")
    for i, beam in enumerate(final_beams[:10]):  # Show top 10
        is_orig = beam.get("is_original", False)
        lp = beam.get("log_prob", 0.0)
        diff = lp - orig_lp
        marker = "← ORIGINAL" if is_orig else ""
        winner = "★ WINNER" if i == 0 else ""

        print(f"\n  [{i}] beam_id={beam.get('beam_id')} log_prob={lp:.2f} (Δ={diff:+.2f}) {winner} {marker}")

        corrections = beam.get("corrections", [])
        if corrections:
            print(f"      corrections:")
            for start, end, orig, repl in corrections:
                print(f"        @{start}-{end}: '{orig}' → '{repl}'")
        else:
            print(f"      (no corrections)")

        # Show snippet of corrected text
        corrected = beam.get("corrected_text", "")
        if corrected and not is_orig:
            print(f"      text: {corrected[:80]}{'...' if len(corrected) > 80 else ''}")

    # Best beam info
    print(f"\nBEST BEAM: {beam_search.get('best_beam_id')}")
    print(f"IMPROVEMENT: {beam_search.get('improvement_over_original', 0):.2f} nats")

    corrections_applied = beam_search.get("corrections_applied", [])
    if corrections_applied:
        print(f"CORRECTIONS APPLIED:")
        for start, end, orig, repl in corrections_applied:
            print(f"  @{start}-{end}: '{orig}' → '{repl}'")

    # Check if expected correction is in any beam
    print(f"\nEXPECTED CORRECTION '{test_case.expected_correction}' IN BEAMS?")
    found_in = []
    for beam in final_beams:
        corrected = beam.get("corrected_text", "").lower()
        if test_case.expected_correction.lower() in corrected:
            found_in.append(beam.get("beam_id"))
    if found_in:
        print(f"  YES, in beams: {found_in}")
    else:
        print(f"  NO - not found in any beam")

    print()


def main():
    parser = argparse.ArgumentParser(description="Analyze TextSureOCR test failures")
    parser.add_argument("--test-file", nargs="+", help="Path(s) to test file(s) to analyze")
    parser.add_argument("--test-ids", help="Comma-separated list of test IDs to analyze")
    parser.add_argument("--all", action="store_true", help="Analyze all test files")
    parser.add_argument("--continuation", action="store_true", help="Analyze continuation tests")
    parser.add_argument("--output-dir", default=".", help="Output directory for reports")
    parser.add_argument("--limit", type=int, help="Limit number of tests to analyze")
    parser.add_argument("--quiet", "-q", action="store_true", help="Only show failures, not passes")
    parser.add_argument("--failures-only", action="store_true", help="Stop collecting debug on pass (faster)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print verbose beam search debug for each failure")
    args = parser.parse_args()

    # Determine test files to process
    test_files = []
    if args.test_file:
        test_files = args.test_file  # Already a list due to nargs="+"
    elif args.all:
        test_dir = Path(__file__).parent.parent / "tests"
        test_files = list(test_dir.glob("test_*.py"))
    elif args.continuation:
        test_dir = Path(__file__).parent.parent / "tests"
        test_files = [str(test_dir / "test_continuation.py")]
    else:
        # Default to structural tests
        test_dir = Path(__file__).parent.parent / "tests"
        test_files = [str(test_dir / "test_ocr_tp_structural.py")]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    if args.continuation:
        # Analyze continuation tests
        all_test_cases = []
        for test_file in test_files:
            if Path(test_file).exists():
                cases = load_continuation_test_cases(str(test_file))
                all_test_cases.extend(cases)
                print(f"Loaded {len(cases)} continuation test cases from {test_file}")

        if args.test_ids:
            filter_ids = set(args.test_ids.split(","))
            all_test_cases = [tc for tc in all_test_cases if tc.test_id in filter_ids]

        if args.limit:
            all_test_cases = all_test_cases[:args.limit]

        print(f"Analyzing {len(all_test_cases)} continuation test cases...")

        analyses = []
        jsonl_path = output_dir / "continuation_failures_debug.jsonl"

        passed = 0
        with open(jsonl_path, "w") as f:
            for i, tc in enumerate(all_test_cases, 1):
                if not args.quiet:
                    print(f"  [{i}/{len(all_test_cases)}] {tc.test_id}...", end=" ", flush=True)
                try:
                    # Fast path: check without debug first if --failures-only
                    if args.failures_only:
                        quick = run_continuation_check(tc.first, tc.second, debug=False)
                        if quick.get("result") == tc.expected_result:
                            passed += 1
                            if not args.quiet:
                                print("PASSED")
                            continue
                        # It's a failure - get debug info
                        result = run_continuation_check(tc.first, tc.second, debug=True)
                    else:
                        result = run_continuation_check(tc.first, tc.second, debug=True)

                    # Check if it's a failure
                    if result.get("result") != tc.expected_result:
                        analysis = analyze_continuation_failure(tc, result)
                        analyses.append(analysis)
                        if args.quiet:
                            print(f"  FAIL: {tc.test_id} ({analysis.reason})")
                        else:
                            print(f"FAILED ({analysis.reason})")

                        # Write to JSONL
                        record = {
                            "test_id": tc.test_id,
                            "first": tc.first,
                            "second": tc.second,
                            "expected_result": tc.expected_result,
                            "api_result": result,
                            "failure_analysis": {
                                "reason": analysis.reason,
                            }
                        }
                        f.write(json.dumps(record) + "\n")
                    else:
                        passed += 1
                        if not args.quiet:
                            print("PASSED")
                except Exception as e:
                    print(f"ERROR: {tc.test_id}: {e}")

        # Generate summary
        summary_path = output_dir / "continuation_failures_summary.md"
        generate_continuation_summary(analyses, str(summary_path))
        print(f"\n{passed} passed, {len(analyses)} failed")
        if analyses:
            print(f"Failures written to: {jsonl_path}")
            print(f"Summary report: {summary_path}")

    else:
        # Analyze OCR tests
        all_test_cases = []
        for test_file in test_files:
            if Path(test_file).exists():
                cases = load_test_cases_from_file(str(test_file))
                all_test_cases.extend(cases)
                print(f"Loaded {len(cases)} test cases from {test_file}")

        if args.test_ids:
            filter_ids = set(args.test_ids.split(","))
            all_test_cases = [tc for tc in all_test_cases if tc.test_id in filter_ids]

        if args.limit:
            all_test_cases = all_test_cases[:args.limit]

        print(f"Analyzing {len(all_test_cases)} test cases...")

        analyses = []
        jsonl_path = output_dir / "failures_debug.jsonl"

        passed = 0
        with open(jsonl_path, "w") as f:
            for i, tc in enumerate(all_test_cases, 1):
                if not args.quiet:
                    print(f"  [{i}/{len(all_test_cases)}] {tc.test_id}...", end=" ", flush=True)
                try:
                    # Helper to check if test passed
                    def check_pass(res: dict) -> bool:
                        for span in res.get("spans", []):
                            if span.get("text", "").lower() == tc.error_word.lower():
                                suggestions = [s["text"].lower() for s in span.get("suggestions", [])]
                                if tc.expected_correction.lower() in suggestions:
                                    return True
                        return False

                    # Fast path: check without debug first if --failures-only
                    if args.failures_only:
                        quick = run_ocr_check(tc.text, debug=False)
                        if check_pass(quick):
                            passed += 1
                            if not args.quiet:
                                print("PASSED")
                            continue
                        # It's a failure - get debug info
                        result = run_ocr_check(tc.text, debug=True)
                    else:
                        result = run_ocr_check(tc.text, debug=True)

                    if not check_pass(result):
                        analysis = analyze_ocr_failure(tc, result)
                        analyses.append(analysis)
                        if args.quiet:
                            print(f"  FAIL: {tc.test_id} ({analysis.reason})")
                        else:
                            print(f"FAILED ({analysis.reason})")

                        # Print verbose beam search debug if requested
                        if args.verbose:
                            print_verbose_beam_debug(tc, result)

                        # Write to JSONL
                        record = {
                            "test_id": tc.test_id,
                            "input_text": tc.text,
                            "expected_error_word": tc.error_word,
                            "expected_correction": tc.expected_correction,
                            "ocr_check_result": result,
                            "failure_analysis": {
                                "word_found": analysis.word_found,
                                "word_flagged": analysis.word_flagged,
                                "reason": analysis.reason,
                                "original_score": analysis.original_score,
                                "correction_score": analysis.correction_score,
                                "log_prob_improvement": analysis.log_prob_improvement,
                                "tokenization_original": analysis.tokenization_original,
                            }
                        }
                        f.write(json.dumps(record) + "\n")
                    else:
                        passed += 1
                        if not args.quiet:
                            print("PASSED")
                except Exception as e:
                    print(f"ERROR: {tc.test_id}: {e}")

        # Generate summary
        summary_path = output_dir / "failures_summary.md"
        generate_summary_report(analyses, str(summary_path))
        print(f"\n{passed} passed, {len(analyses)} failed")
        if analyses:
            print(f"Failures written to: {jsonl_path}")
            print(f"Summary report: {summary_path}")


if __name__ == "__main__":
    main()
