"""
Run the TextSureOCR test battery against a registered server and write a
markdown report with accuracy, per-test misses, and wall time.

Server URL + auth token are read from ~/.textsureocr/servers.yaml
(populated by `textsureocr deploy`). No env-var juggling required.

Usage:
    python run_report.py                        # default server
    python run_report.py --server ts1
    python run_report.py --server ts1 --out report.md
    python run_report.py --url https://... --token tso_tok_...
"""

import os
import sys
import time
import json
import argparse
import datetime as dt
import importlib.util
from pathlib import Path
import requests

# Load tests.py directly (the tests/ package shadows `import tests`)
_spec = importlib.util.spec_from_file_location(
    "tests_module", os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests.py"),
)
T = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(T)

CONFIG_PATH = Path.home() / ".textsureocr" / "servers.yaml"
DEFAULT_OUT = "test_report.md"


def load_server(name: str | None) -> tuple[str, str, str]:
    """Return (server_name, url, token) from ~/.textsureocr/servers.yaml."""
    if not CONFIG_PATH.exists():
        sys.exit(f"FATAL: {CONFIG_PATH} not found. Run `textsureocr deploy` first, "
                 f"or pass --url and --token.")
    try:
        import yaml
    except ImportError:
        sys.exit("FATAL: pyyaml not installed. `pip install pyyaml` or pass --url/--token.")
    cfg = yaml.safe_load(CONFIG_PATH.read_text()) or {}
    servers = cfg.get("servers") or {}
    if not servers:
        sys.exit(f"FATAL: no servers registered in {CONFIG_PATH}.")
    target = name or (cfg.get("defaults") or {}).get("server")
    if not target:
        sys.exit(f"FATAL: no --server given and no defaults.server in {CONFIG_PATH}.")
    if target not in servers:
        sys.exit(f"FATAL: server '{target}' not in {CONFIG_PATH}. "
                 f"Known: {', '.join(sorted(servers))}")
    s = servers[target]
    url, token = s.get("url"), s.get("token", "")
    if not url:
        sys.exit(f"FATAL: server '{target}' has no url in {CONFIG_PATH}.")
    return target, url, token


def run_case(kind: str, case: dict, base: str, headers: dict):
    """Run one case, returning (ok, detail, response_body, wall_seconds, http_status)."""
    t0 = time.time()
    try:
        if kind == "ocr":
            r = requests.post(
                f"{base}/v1/ocr/check",
                json={"text": case["text"]},
                headers=headers, timeout=180,
            )
        else:
            r = requests.post(
                f"{base}/v1/text/check-continuation",
                json={"first": case["first"], "second": case["second"]},
                headers=headers, timeout=180,
            )
    except Exception as e:
        return False, f"request error: {e}", None, time.time() - t0, -1

    dt_s = time.time() - t0
    if r.status_code != 200:
        return False, f"HTTP {r.status_code}: {r.text[:200]}", None, dt_s, r.status_code

    body = r.json()
    problems = []

    if kind == "ocr":
        if "expect_result" in case and body.get("result") != case["expect_result"]:
            problems.append(f'result: got "{body.get("result")}", want "{case["expect_result"]}"')
        if "expect_spans" in case:
            span_texts = {s["text"] for s in body.get("spans", [])}
            for exp in case["expect_spans"]:
                if exp["text"] not in span_texts:
                    problems.append(f'missing span: "{exp["text"]}"')
                elif "suggestion" in exp:
                    span = next(s for s in body["spans"] if s["text"] == exp["text"])
                    sugg_texts = {s["text"] for s in span.get("suggestions", [])}
                    if exp["suggestion"] not in sugg_texts:
                        problems.append(
                            f'"{exp["text"]}": missing suggestion "{exp["suggestion"]}" (got {sorted(sugg_texts)})'
                        )
        if "expect_min_spans" in case:
            actual = len(body.get("spans", []))
            if actual < case["expect_min_spans"]:
                problems.append(f"span count: got {actual}, want >= {case['expect_min_spans']}")
        if "expect_no_spans" in case:
            span_texts = {s["text"] for s in body.get("spans", [])}
            for bad in case["expect_no_spans"]:
                for st in span_texts:
                    if bad in st:
                        problems.append(f'false positive: "{bad}" should not be flagged')
    else:
        if "expect_result" in case and body.get("result") != case["expect_result"]:
            problems.append(f'result: got "{body.get("result")}", want "{case["expect_result"]}"')
        if "expect_score_above" in case and body.get("score", 0) < case["expect_score_above"]:
            problems.append(f'score {body.get("score")} < {case["expect_score_above"]}')
        if "expect_score_below" in case and body.get("score", 1) > case["expect_score_below"]:
            problems.append(f'score {body.get("score")} > {case["expect_score_below"]}')

    ok = not problems
    if ok:
        if kind == "ocr":
            detail = f'result={body["result"]} score={body["score"]} spans={len(body.get("spans", []))}'
        else:
            detail = f'result={body["result"]} score={body["score"]}'
    else:
        detail = "; ".join(problems)
    return ok, detail, body, dt_s, 200


def fmt_expectations(kind: str, case: dict) -> str:
    keys = ("expect_result", "expect_spans", "expect_min_spans",
            "expect_no_spans", "expect_score_above", "expect_score_below")
    parts = []
    for k in keys:
        if k in case:
            v = case[k]
            if k == "expect_spans":
                v = ", ".join(
                    f'{s["text"]}→{s.get("suggestion","*")}' for s in v
                )
            parts.append(f"`{k}`={v}")
    return "; ".join(parts)


def fmt_actual(kind: str, body) -> str:
    if body is None:
        return "_no response_"
    if kind == "ocr":
        spans = body.get("spans", [])
        span_str = ", ".join(
            f'{s["text"]}→[' + ", ".join(f'{x["text"]}({x["score"]})' for x in s.get("suggestions", [])) + "]"
            for s in spans
        )
        return f'result=`{body.get("result")}` score=`{body.get("score")}` spans=`{len(spans)}`' + (f" · {span_str}" if span_str else "")
    return f'result=`{body.get("result")}` score=`{body.get("score")}`'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--server", help="named server in ~/.textsureocr/servers.yaml")
    ap.add_argument("--url", help="override: server URL (bypasses config)")
    ap.add_argument("--token", help="override: auth token (bypasses config)")
    ap.add_argument("--out", default=DEFAULT_OUT, help=f"markdown report path (default: {DEFAULT_OUT})")
    args = ap.parse_args()

    if args.url:
        server_name, base, token = "(--url)", args.url, args.token or os.getenv("TEXTSURE_AUTH_TOKEN", "")
    else:
        server_name, base, token = load_server(args.server)
    out = args.out
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    print(f"Server: {server_name}  →  {base}")
    print(f"Auth:   {'Bearer ' + token[:14] + '…' if token else '(none)'}")
    print(f"Output: {out}\n")

    # Health
    try:
        h = requests.get(f"{base}/health", timeout=15).json()
    except Exception as e:
        print(f"FATAL: {base}/health unreachable — {e}")
        sys.exit(1)

    results = {"ocr": [], "cont": []}
    t_start = time.time()

    print(f"── OCR Check ({len(T.OCR_TESTS)} tests) ──")
    for case in T.OCR_TESTS:
        ok, detail, body, secs, status = run_case("ocr", case, base, headers)
        tag = "PASS" if ok else "FAIL"
        print(f"  [{tag}] {case['name']} ({secs:.1f}s) — {detail}")
        results["ocr"].append({"case": case, "ok": ok, "detail": detail, "body": body, "secs": secs, "status": status})

    print(f"\n── Continuation Check ({len(T.CONTINUATION_TESTS)} tests) ──")
    for case in T.CONTINUATION_TESTS:
        ok, detail, body, secs, status = run_case("cont", case, base, headers)
        tag = "PASS" if ok else "FAIL"
        print(f"  [{tag}] {case['name']} ({secs:.1f}s) — {detail}")
        results["cont"].append({"case": case, "ok": ok, "detail": detail, "body": body, "secs": secs, "status": status})

    total_wall = time.time() - t_start

    ocr_pass = sum(1 for r in results["ocr"] if r["ok"])
    cont_pass = sum(1 for r in results["cont"] if r["ok"])
    ocr_total = len(results["ocr"])
    cont_total = len(results["cont"])
    total_pass = ocr_pass + cont_pass
    total = ocr_total + cont_total
    acc = (total_pass / total * 100) if total else 0.0

    ocr_secs = [r["secs"] for r in results["ocr"]]
    cont_secs = [r["secs"] for r in results["cont"]]
    all_secs = ocr_secs + cont_secs

    def stats(xs):
        if not xs:
            return "—"
        xs_sorted = sorted(xs)
        mean = sum(xs) / len(xs)
        p50 = xs_sorted[len(xs)//2]
        p95 = xs_sorted[max(0, int(len(xs)*0.95) - 1)]
        return f"mean {mean:.2f}s · p50 {p50:.2f}s · p95 {p95:.2f}s · min {min(xs):.2f}s · max {max(xs):.2f}s · sum {sum(xs):.1f}s"

    misses = [r for r in results["ocr"] + results["cont"] if not r["ok"]]

    # ── Build markdown ────────────────────────────────────────────
    lines: list[str] = []
    lines.append(f"# TextSureOCR Test Report")
    lines.append("")
    lines.append(f"- **Endpoint:** `{base}`")
    lines.append(f"- **Model:** `{h.get('model','?')}` on `{h.get('device','?')}` (loaded: {h.get('model_loaded','?')})")
    lines.append(f"- **Run at:** {dt.datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"- **Wall time:** {total_wall:.1f}s")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Suite | Passed | Total | Accuracy |")
    lines.append("|---|---|---|---|")
    lines.append(f"| OCR check | {ocr_pass} | {ocr_total} | {(ocr_pass/ocr_total*100 if ocr_total else 0):.1f}% |")
    lines.append(f"| Continuation check | {cont_pass} | {cont_total} | {(cont_pass/cont_total*100 if cont_total else 0):.1f}% |")
    lines.append(f"| **Overall** | **{total_pass}** | **{total}** | **{acc:.1f}%** |")
    lines.append("")
    lines.append("## Timing")
    lines.append("")
    lines.append(f"- OCR: {stats(ocr_secs)}")
    lines.append(f"- Continuation: {stats(cont_secs)}")
    lines.append(f"- All: {stats(all_secs)}")
    lines.append("")
    lines.append(f"## Misses ({len(misses)})")
    lines.append("")
    if not misses:
        lines.append("_None — all tests passed._")
    else:
        for r in misses:
            c = r["case"]
            lines.append(f"### `{c['name']}`")
            lines.append("")
            if "text" in c:
                lines.append(f"- **Input:** `{c['text']}`")
            else:
                lines.append(f"- **First:** `{c['first']}`")
                lines.append(f"- **Second:** `{c['second']}`")
            lines.append(f"- **Expected:** {fmt_expectations('ocr' if 'text' in c else 'cont', c)}")
            lines.append(f"- **Actual:** {fmt_actual('ocr' if 'text' in c else 'cont', r['body'])}")
            lines.append(f"- **Why it failed:** {r['detail']}")
            lines.append(f"- **Time:** {r['secs']:.2f}s")
            lines.append("")

    lines.append("## Full Results")
    lines.append("")
    lines.append("### OCR Check")
    lines.append("")
    lines.append("| Test | Result | Time (s) | Detail |")
    lines.append("|---|---|---|---|")
    for r in results["ocr"]:
        status = "✅ PASS" if r["ok"] else "❌ FAIL"
        detail = r["detail"].replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {r['case']['name']} | {status} | {r['secs']:.2f} | {detail} |")
    lines.append("")
    lines.append("### Continuation Check")
    lines.append("")
    lines.append("| Test | Result | Time (s) | Detail |")
    lines.append("|---|---|---|---|")
    for r in results["cont"]:
        status = "✅ PASS" if r["ok"] else "❌ FAIL"
        detail = r["detail"].replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {r['case']['name']} | {status} | {r['secs']:.2f} | {detail} |")
    lines.append("")

    with open(out, "w") as f:
        f.write("\n".join(lines))

    print(f"\n{'='*70}")
    print(f"  {total_pass}/{total} passed ({acc:.1f}%)  wall={total_wall:.1f}s")
    print(f"  Report → {out}")
    print(f"{'='*70}")
    sys.exit(0 if total_pass == total else 1)


if __name__ == "__main__":
    main()
