"""
Shared helper functions for TextSureOCR integration tests.

These are plain functions (not fixtures) that test files import directly.
"""

import os
import requests

BASE_URL = os.getenv("TEXTSURE_URL", "http://localhost:5002")


def ocr_check(api, text: str) -> dict:
    """POST /v1/ocr/check and return parsed JSON."""
    r = api.post(f"{api.base_url}/v1/ocr/check", json={"text": text}, timeout=120)
    r.raise_for_status()
    return r.json()


def continuation_check(api, first: str, second: str) -> dict:
    """POST /v1/text/check-continuation and return parsed JSON."""
    r = api.post(
        f"{api.base_url}/v1/text/check-continuation",
        json={"first": first, "second": second},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()
