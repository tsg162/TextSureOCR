"""
Shared pytest configuration and fixtures for TextSureOCR test suite.

Target resolution order (integration tests):
  1. --server NAME (pytest CLI)  or  TEXTSURE_SERVER env  →  look up in
     ~/.textsureocr/servers.yaml and use its url + token
  2. TEXTSURE_URL (+ optional TEXTSURE_AUTH_TOKEN) env vars
  3. default server in ~/.textsureocr/servers.yaml
  4. fallback: http://localhost:5002 (no token)

Unit tests (test_unit*.py) run without a service and import app.py directly.
"""

import os
import sys
from pathlib import Path

import pytest
import requests

sys.path.insert(0, os.path.dirname(__file__))

CONFIG_PATH = Path.home() / ".textsureocr" / "servers.yaml"


def _load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    try:
        import yaml
    except ImportError:
        return {}
    try:
        return yaml.safe_load(CONFIG_PATH.read_text()) or {}
    except Exception:
        return {}


def _resolve_target(server_name: str | None) -> tuple[str, str, str]:
    """Return (source, url, token)."""
    cfg = _load_config()
    servers = cfg.get("servers") or {}
    defaults = cfg.get("defaults") or {}

    name = server_name or os.getenv("TEXTSURE_SERVER")
    if name:
        if name not in servers:
            raise RuntimeError(
                f"server '{name}' not in {CONFIG_PATH}. "
                f"Known: {', '.join(sorted(servers)) or '(none)'}"
            )
        s = servers[name]
        return f"config:{name}", s["url"], s.get("token", "")

    env_url = os.getenv("TEXTSURE_URL")
    if env_url:
        return "env", env_url, os.getenv("TEXTSURE_AUTH_TOKEN", "")

    default_name = defaults.get("server")
    if default_name and default_name in servers:
        s = servers[default_name]
        return f"config:{default_name} (default)", s["url"], s.get("token", "")

    return "fallback", "http://localhost:5002", ""


def pytest_addoption(parser):
    parser.addoption(
        "--server", action="store", default=None,
        help="named server in ~/.textsureocr/servers.yaml (integration tests)",
    )


@pytest.fixture(scope="session")
def target(pytestconfig):
    source, url, token = _resolve_target(pytestconfig.getoption("--server"))
    return {"source": source, "url": url, "token": token}


@pytest.fixture(scope="session")
def base_url(target):
    return target["url"]


@pytest.fixture(scope="session")
def api(target):
    """Requests session pointed at the live service.  Skips all
    integration tests if the service is unreachable."""
    url, token = target["url"], target["token"]
    s = requests.Session()
    s.base_url = url
    if token:
        s.headers["Authorization"] = f"Bearer {token}"
    try:
        r = s.get(f"{url}/health", timeout=10)
        r.raise_for_status()
    except Exception as e:
        pytest.skip(f"TextSureOCR service not available at {url}: {e}")
    yield s
    s.close()


def pytest_report_header(config):
    source, url, token = _resolve_target(config.getoption("--server"))
    masked = f"{token[:14]}…" if token else "(none)"
    return f"textsureocr target: {url}  [{source}]  auth={masked}"


def pytest_configure(config):
    config.addinivalue_line("markers", "integration: needs live TextSureOCR service")
    config.addinivalue_line("markers", "unit: pure logic, no model/service needed")
    config.addinivalue_line("markers", "ocr_positive: OCR error should be detected")
    config.addinivalue_line("markers", "ocr_negative: clean text, no errors expected")
    config.addinivalue_line("markers", "continuation: text continuation checks")
    config.addinivalue_line("markers", "slow: tests that take >5s each")
