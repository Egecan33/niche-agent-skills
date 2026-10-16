#!/usr/bin/env python3
"""Original offline teaching-case checks, not upstream library integrations.

Checks explicit invariants over the bundled normalized synthetic fixtures.
Does not run models, SQL, HTTP requests, replay engines, OCR, or PDF parsers.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


def trajectory(data, fixture):
    calls, reference = data["calls"], fixture["reference"]["calls"]
    issues = set()
    if len(calls) != len(reference):
        issues.add("call-count")
    for actual, expected in zip(calls, reference):
        if actual["name"] != expected["name"]:
            issues.add("tool-order")
        elif actual["arguments"] != expected["arguments"]:
            issues.add("significant-argument")
    return issues


def rls(data, fixture):
    issues = set()
    if data["effective_role"] in {"postgres", "service_role", "owner", "superuser", "bypassrls"}:
        issues.add("bypass-role")
    if data["positive_control"] is not True:
        issues.add("missing-positive-control")
    if sorted(data["actual_rows"]) != sorted(data["expected_rows"]):
        issues.add("row-set-mismatch")
    return issues


def openapi(data, fixture):
    """Deliberately one integer-property contract, not a JSON Schema engine."""
    contract, issues = fixture["contract"], set()
    if data["status"] != contract["status"]:
        issues.add("response-status")
    if data["content_type"] != contract["content_type"]:
        issues.add("response-content-type")
    if contract["required"] not in data["body"]:
        issues.add("response-required-field")
    else:
        value = data["body"][contract["required"]]
        if type(value) is not int:  # Python bool must not pass the integer check.
            issues.add("response-type")
        elif value < contract["minimum"]:
            issues.add("response-range")
    return issues


def interval_union(intervals):
    """Length of overlapping immediate-child intervals, not critical-path time."""
    total, current_end = 0, None
    for start, end in sorted(intervals):
        if end < start:
            raise ValueError("negative span interval")
        if current_end is None or start > current_end:
            total += end - start
            current_end = end
        elif end > current_end:
            total += end - current_end
            current_end = end
    return total


def trace(data, fixture):
    spans, report, issues = fixture["spans"], data["report"], set()
    roots = [s for s in spans if s["parent"] is None]
    if len(roots) != 1 or len({s["id"] for s in spans}) != len(spans):
        return {"invalid-span-identity"}
    root = roots[0]
    if any(s["end_ms"] < s["start_ms"] for s in spans):
        return {"invalid-timing"}
    children = [s for s in spans if s["parent"] == root["id"]]
    if any(s["start_ms"] < root["start_ms"] or s["end_ms"] > root["end_ms"] for s in children):
        return {"invalid-timing"}
    wall = root["end_ms"] - root["start_ms"]
    covered = interval_union([(s["start_ms"], s["end_ms"]) for s in children])
    if report.get("wall_ms") != wall:
        issues.add("wall-time-mismatch")
    if report.get("covered_ms") != covered:
        issues.add("coverage-mismatch")
    if report.get("uncovered_ms") != wall - covered:
        issues.add("uncovered-mismatch")
    if sorted(report.get("error_span_ids", [])) != sorted(s["id"] for s in spans if s["status"] == "ERROR"):
        issues.add("error-evidence-mismatch")
    if "p95_ms" in report:
        issues.add("unsupported-population-statistic")
    return issues


def session(data, fixture):
    issues = set()
    if data["consent"] is not True:
        issues.add("consent-required")
    if data["sanitized"] is not True:
        issues.add("sanitization-required")
    ids = {e["id"] for e in data["events"]}
    for step in data["steps"]:
        if not step["evidence"] or not set(step["evidence"]) <= ids:
            issues.add("unknown-event-reference")
    if data["outcome"] == "saved" and not any(e["action"] == "confirmation" for e in data["events"]):
        issues.add("unobserved-success")
    if data["recovered_masked_value"] is not None:
        issues.add("unmasking-inference")
    return issues


def dataset(data, fixture):
    sources = {s["id"]: s for s in fixture["sources"]}
    seen_questions, seen_ids, issues = set(), set(), set()
    for row in data["rows"]:
        source = sources.get(row.get("source_id"))
        if not source or row.get("source_revision") != source["revision"] or not row.get("evidence"):
            issues.add("missing-provenance")
            continue
        if row["source_group"] != source["group"] or row["split"] != source["split"]:
            issues.add("source-split-leakage")
        question = " ".join(row["question"].lower().split())
        if question in seen_questions:
            issues.add("duplicate-question")
        if row["id"] in seen_ids:
            issues.add("duplicate-row-id")
        seen_questions.add(question)
        seen_ids.add(row["id"])
        # The tiny fixture has hand-authored answer oracles, not automated entailment.
        oracles = {" ".join(q.lower().split()): a for q, a in source["oracles"].items()}
        if question not in oracles:
            issues.add("unreviewed-question")
        elif row["answer"] != oracles[question] or row["answerable"] != (oracles[question] is not None):
            issues.add("unsupported-answer")
    return issues


def pdf(data, fixture):
    issues = set()
    cells = {c["id"]: c for c in fixture["table"]["cells"]}
    for evidence in data["ledger"]:
        cell = cells.get(evidence["cell_id"])
        if not cell:
            issues.add("unknown-cell")
            continue
        x0, top, x1, bottom = evidence["bbox"]
        page = fixture["page"]
        if not (0 <= x0 < x1 <= page["width"] and 0 <= top < bottom <= page["height"]):
            issues.add("bbox-out-of-page")
        if evidence["bbox"] != cell["bbox"]:
            issues.add("cell-coordinate-mismatch")
        if evidence["page"] != cell["page"] or evidence["coordinate_system"] != "x0-top-x1-bottom-pdf-points":
            issues.add("coordinate-provenance-mismatch")
        if evidence["raw_text"] != cell["raw_text"]:
            issues.add("raw-text-mismatch")
        if evidence["normalized_value"] != cell["normalized_value"]:
            issues.add("normalization-mismatch")
        if evidence["visual_review"] == "passed" and not fixture["render_available"]:
            issues.add("unverified-visual-claim")
    if len(data["ledger"]) != len(cells):
        issues.add("cell-coverage-mismatch")
    return issues


CHECKERS = {"trajectory": trajectory, "rls": rls, "openapi": openapi,
            "trace": trace, "session": session, "dataset": dataset, "pdf": pdf}


def run_fixture(path):
    fixture = json.loads(Path(path).read_text(encoding="utf-8"))
    if fixture.get("schema_version") != 1:
        raise ValueError("unknown fixture schema")
    results = []
    for case in fixture["cases"]:
        actual = sorted(CHECKERS[fixture["kind"]](case["input"], fixture))
        expected = sorted(case["issues"])
        results.append({"id": case["id"], "passed": actual == expected,
                        "expected_issues": expected, "observed_issues": actual})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", nargs="?", type=Path)
    args = parser.parse_args()
    paths = [args.fixture] if args.fixture else sorted(Path(__file__).resolve().parents[1].glob("skills/*/assets/case.json"))
    results, errors = {}, []
    for path in paths:
        try:
            results[path.parent.parent.name] = run_fixture(path)
        except (ValueError, TypeError, KeyError, OSError) as exc:
            errors.append({"fixture": path.name, "error": type(exc).__name__})
    passed = bool(results) and not errors and all(c["passed"] for cases in results.values() for c in cases)
    print(json.dumps({"status": "passed" if passed else "failed", "mode": "offline synthetic invariants",
                      "upstream_integrations": "not run", "results": results, "errors": errors}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
