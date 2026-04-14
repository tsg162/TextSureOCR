"""
Shared pytest configuration and fixtures for TextSureOCR test suite.

Integration tests hit the live service (default http://localhost:5002).
Set TEXTSURE_URL to override.

Unit tests (test_unit*.py) run without a service and import app.py directly.
"""

import os
import sys

import pytest
import requests

# Ensure the tests/ directory is on sys.path so helpers.py is importable
sys.path.insert(0, os.path.dirname(__file__))

BASE_URL = os.getenv("TEXTSURE_URL", "http://localhost:5002")


# ── Session-scoped fixtures ───────────────────────────────────────────


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def api(base_url):
    """Requests session pointed at the live service.  Skips all
    integration tests if the service is unreachable."""
    s = requests.Session()
    s.base_url = base_url
    try:
        r = s.get(f"{base_url}/health", timeout=10)
        r.raise_for_status()
    except Exception as e:
        pytest.skip(f"TextSureOCR service not available at {base_url}: {e}")
    yield s
    s.close()


# ── Markers ───────────────────────────────────────────────────────────


def pytest_configure(config):
    config.addinivalue_line("markers", "integration: needs live TextSureOCR service")
    config.addinivalue_line("markers", "unit: pure logic, no model/service needed")
    config.addinivalue_line("markers", "ocr_positive: OCR error should be detected")
    config.addinivalue_line("markers", "ocr_negative: clean text, no errors expected")
    config.addinivalue_line("markers", "continuation: text continuation checks")
    config.addinivalue_line("markers", "slow: tests that take >5s each")
