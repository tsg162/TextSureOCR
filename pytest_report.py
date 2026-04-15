"""
Parse a pytest JUnit-XML file and write a markdown report covering:
  - per-file pass/fail/skip/error counts and accuracy
  - throughput (tests/sec, mean/p50/p95/max latency)
  - full failure list with assertion messages
  - slowest 30 tests

Usage:
    python pytest_report.py <junit.xml> [-o report.md] [--title "..."]
"""

import argparse
import statistics
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path


def percentile(xs, p):
    if not xs:
        return 0.0
    s = sorted(xs)
    i = max(0, int(len(s) * p) - 1)
    return s[i]


def parse(xml_path: Path):
    root = ET.parse(xml_path).getroot()
    suites = root.findall(".//testsuite") or [root]
    cases = []
    for suite in suites:
        for tc in suite.findall("testcase"):
            classname = tc.get("classname", "")
            name = tc.get("name", "")
            t = float(tc.get("time", "0"))
            file_attr = tc.get("file") or (classname.split(".")[0] if "." in classname else classname)
            status = "pass"
            message = ""
            for tag, label in (("failure", "fail"), ("error", "error"), ("skipped", "skip")):
                el = tc.find(tag)
                if el is not None:
                    status = label
                    message = (el.get("message") or el.text or "").strip().splitlines()[0][:300] if (el.get("message") or el.text) else ""
                    break
            cases.append({
                "file": file_attr,
                "classname": classname,
                "name": name,
                "id": f"{classname}::{name}" if classname else name,
                "time": t,
                "status": status,
                "message": message,
            })
    return cases


def render(cases, title: str, source: str) -> str:
    by_file = defaultdict(list)
    for c in cases:
        by_file[c["file"]].append(c)

    total = len(cases)
    n_pass = sum(1 for c in cases if c["status"] == "pass")
    n_fail = sum(1 for c in cases if c["status"] == "fail")
    n_err  = sum(1 for c in cases if c["status"] == "error")
    n_skip = sum(1 for c in cases if c["status"] == "skip")
    executed = total - n_skip
    acc = (n_pass / executed * 100) if executed else 0.0

    times = [c["time"] for c in cases if c["status"] != "skip"]
    sum_t = sum(times)
    mean_t = sum_t / len(times) if times else 0.0
    p50 = percentile(times, 0.50)
    p95 = percentile(times, 0.95)
    p99 = percentile(times, 0.99)
    mx = max(times) if times else 0.0
    throughput = (len(times) / sum_t) if sum_t > 0 else 0.0

    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"- **Source:** `{source}`")
    lines.append(f"- **Cases:** {total}  ({n_pass} pass · {n_fail} fail · {n_err} error · {n_skip} skip)")
    lines.append(f"- **Accuracy:** {acc:.2f}% (executed: {executed})")
    lines.append(f"- **Total test-time:** {sum_t:.1f}s")
    lines.append(f"- **Throughput:** {throughput:.2f} tests/sec  ·  **mean** {mean_t*1000:.0f} ms/test")
    lines.append(f"- **Latency:** p50 {p50*1000:.0f} ms · p95 {p95*1000:.0f} ms · p99 {p99*1000:.0f} ms · max {mx*1000:.0f} ms")
    lines.append("")

    lines.append("## Per-file breakdown")
    lines.append("")
    lines.append("| File | Pass | Fail | Error | Skip | Accuracy | Mean (ms) | Sum (s) |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for f in sorted(by_file):
        cs = by_file[f]
        p = sum(1 for c in cs if c["status"] == "pass")
        fl = sum(1 for c in cs if c["status"] == "fail")
        e = sum(1 for c in cs if c["status"] == "error")
        sk = sum(1 for c in cs if c["status"] == "skip")
        ex = len(cs) - sk
        a = (p / ex * 100) if ex else 0.0
        ts = [c["time"] for c in cs if c["status"] != "skip"]
        m = (sum(ts) / len(ts) * 1000) if ts else 0.0
        s_ = sum(ts)
        lines.append(f"| `{f}` | {p} | {fl} | {e} | {sk} | {a:.1f}% | {m:.0f} | {s_:.1f} |")
    lines.append("")

    fails = [c for c in cases if c["status"] in ("fail", "error")]
    lines.append(f"## Failures ({len(fails)})")
    lines.append("")
    if not fails:
        lines.append("_None._")
    else:
        # Group by file for readability
        fail_by_file = defaultdict(list)
        for c in fails:
            fail_by_file[c["file"]].append(c)
        for f in sorted(fail_by_file):
            lines.append(f"### `{f}` ({len(fail_by_file[f])})")
            lines.append("")
            lines.append("| Test | Status | Time (ms) | Message |")
            lines.append("|---|---|---:|---|")
            for c in fail_by_file[f]:
                msg = c["message"].replace("|", "\\|").replace("\n", " ")[:200] or "—"
                lines.append(f"| `{c['name']}` | {c['status']} | {c['time']*1000:.0f} | {msg} |")
            lines.append("")

    lines.append("## Slowest 30 tests")
    lines.append("")
    slowest = sorted([c for c in cases if c["status"] != "skip"], key=lambda c: c["time"], reverse=True)[:30]
    lines.append("| # | Time (ms) | Status | Test |")
    lines.append("|---:|---:|---|---|")
    for i, c in enumerate(slowest, 1):
        lines.append(f"| {i} | {c['time']*1000:.0f} | {c['status']} | `{c['id']}` |")
    lines.append("")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("xml", help="path to pytest junit-xml file")
    ap.add_argument("-o", "--out", default="pytest_report.md", help="markdown output path")
    ap.add_argument("--title", default="TextSureOCR Pytest Report", help="report title")
    args = ap.parse_args()

    xml_path = Path(args.xml)
    if not xml_path.exists():
        sys.exit(f"FATAL: {xml_path} not found")

    cases = parse(xml_path)
    md = render(cases, args.title, str(xml_path))
    Path(args.out).write_text(md)

    n_pass = sum(1 for c in cases if c["status"] == "pass")
    n_fail = sum(1 for c in cases if c["status"] in ("fail", "error"))
    n_skip = sum(1 for c in cases if c["status"] == "skip")
    print(f"Parsed {len(cases)} cases  →  {n_pass} pass · {n_fail} fail · {n_skip} skip")
    print(f"Report → {args.out}")


if __name__ == "__main__":
    main()
