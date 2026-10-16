#!/usr/bin/env python3
"""Offline, read-only checks for this draft's deliberately narrow profile.

Original repository code. No dependencies, network, subprocesses, or writes.
This is not an official Agent Skills validator or a general Markdown/YAML parser.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


SKILLS = {
    "agent-trajectory-regression", "postgres-tenant-isolation", "openapi-contract-probes",
    "trace-failure-diagnosis", "masked-session-to-sop", "grounded-synthetic-datasets",
    "pdf-table-evidence",
}
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
IGNORED = {"__pycache__", ".git", ".venv", "eval-runs"}
PRIVATE = [
    ("private home path", re.compile(r"/(?:Users|home)/[A-Za-z0-9_.-]+/")),
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("GitHub credential", re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})")),
    ("AWS access key", re.compile(r"AKIA[A-Z0-9]{16}")),
    ("email address", re.compile(r"\b[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
]


def files_under(root: Path) -> tuple[list[Path], list[str]]:
    """Never follow symlinks, including links to directories outside the package."""
    files, errors = [], []
    for directory, dirs, names in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in list(dirs):
            path = base / name
            if path.is_symlink():
                errors.append(f"{path.relative_to(root)}: symlink is not publishable")
                dirs.remove(name)
            elif name in IGNORED:
                dirs.remove(name)
        for name in names:
            path = base / name
            if path.is_symlink():
                errors.append(f"{path.relative_to(root)}: symlink is not publishable")
            elif path.suffix not in {".pyc", ".pyo"} and name != ".DS_Store":
                files.append(path)
    return sorted(files), errors


def check_skill(path: Path) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return ["missing opening frontmatter delimiter"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return ["missing closing frontmatter delimiter"]
    fields = {}
    for line in lines[1:end]:
        match = re.fullmatch(r"(name|description): ([^\s].*)", line)
        if not match:
            errors.append("frontmatter must use only plain single-line name and description")
            continue
        key, value = match.groups()
        if key in fields:
            errors.append(f"duplicate frontmatter key: {key}")
        if value[0] in "\"'[{>|*&!%@`" or ": " in value or " #" in value:
            errors.append(f"{key}: unsupported YAML syntax in this profile")
        fields[key] = value
    name, description = fields.get("name", ""), fields.get("description", "")
    if not NAME.fullmatch(name) or len(name) > 64:
        errors.append("name must be 1-64 lowercase ASCII letters/digits with single hyphens")
    if name != path.parent.name:
        errors.append("name does not match parent directory")
    if not 1 <= len(description.strip()) <= 1024:
        errors.append("description must be 1-1024 characters")
    if not "\n".join(lines[end + 1:]).strip():
        errors.append("empty instruction body")
    if len(lines) >= 500:
        errors.append("draft convention requires SKILL.md below 500 lines")
    return errors


def check_links(path: Path, root: Path) -> list[str]:
    """Check inline destinations; anchors and external links are not fetched."""
    errors = []
    for raw in LINK.findall(path.read_text(encoding="utf-8")):
        target = raw.strip().strip("<>")
        parts = urlsplit(target)
        if parts.scheme in {"https", "http", "mailto"} or not parts.path:
            continue
        if parts.scheme or parts.netloc or parts.path.startswith("/"):
            errors.append("unsupported or absolute link destination")
            continue
        resolved = (path.parent / unquote(parts.path)).resolve()
        boundary = path.parent.resolve() if path.name == "SKILL.md" else root.resolve()
        if not resolved.is_relative_to(boundary):
            errors.append("local link escapes its permitted package boundary")
        elif not resolved.exists():
            errors.append(f"missing relative link: {parts.path}")
    return errors


def check_evals(root: Path) -> list[str]:
    errors = []
    try:
        data = json.loads((root / "evals/cases.json").read_text(encoding="utf-8"))
        if data.get("schema_version") != 1 or not isinstance(data.get("cases"), list):
            return ["invalid evaluation schema/version"]
        ids, routing, behavioral = set(), {}, set()
        for case in data["cases"]:
            cid = case.get("id")
            if not isinstance(cid, str) or not cid or cid in ids:
                errors.append("evaluation IDs must be unique nonempty strings")
            ids.add(cid if isinstance(cid, str) else repr(cid))
            skill, kind = case.get("skill"), case.get("kind")
            if skill not in SKILLS or kind not in {"routing", "behavior"}:
                errors.append(f"{cid}: unknown skill or case kind")
            if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
                errors.append(f"{cid}: missing prompt")
            if kind == "routing":
                expected = case.get("should_trigger")
                if type(expected) is not bool:
                    errors.append(f"{cid}: should_trigger must be boolean")
                else:
                    key = (skill, expected)
                    routing[key] = routing.get(key, 0) + 1
            else:
                assertions = case.get("assertions")
                if not isinstance(assertions, list) or not assertions or not all(
                    isinstance(item, str) and item.strip() for item in assertions
                ):
                    errors.append(f"{cid}: missing observable assertions")
                behavioral.add(skill)
                fixture = case.get("fixture", "")
                target = (root / fixture).resolve()
                if not fixture or not target.is_relative_to(root.resolve()) or not target.is_file():
                    errors.append(f"{cid}: missing or escaping fixture path")
        for skill in sorted(SKILLS):
            if not all(routing.get((skill, expected), 0) >= 2 for expected in (True, False)):
                errors.append(f"{skill}: need two positive and two negative routing cases")
            if skill not in behavioral:
                errors.append(f"{skill}: need a behavior case")
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        errors.append(f"cannot validate evals: {type(exc).__name__}")
    return errors


def check_sources(root: Path) -> list[str]:
    errors = []
    try:
        lock = json.loads((root / "sources.lock.json").read_text(encoding="utf-8"))
        if lock.get("schema_version") != 1 or len(lock.get("sources", [])) != 7:
            return ["source lock requires schema version 1 and seven sources"]
        covered, identities = set(), set()
        for source in lock["sources"]:
            repo, commit = source["repo"], source["commit"]
            if not re.fullmatch(r"[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+", repo) or not re.fullmatch(r"[0-9a-f]{40}", commit):
                errors.append("source must use repository identity and immutable 40-character commit")
                continue
            if source["id"] in identities:
                errors.append("duplicate source identity")
            identities.add(source["id"])
            covered.add(source["skill"])
            if source["license"] not in {"MIT", "Apache-2.0", "PostgreSQL"}:
                errors.append(f"{repo}: unreviewed source license")
            prefix = f"https://github.com/{repo}/blob/{commit}/"
            if not source["license_url"].startswith(prefix):
                errors.append(f"{repo}: license link is not pinned")
            snapshot = (root / source["license_snapshot"]).resolve()
            if not snapshot.is_relative_to(root.resolve()) or not snapshot.is_file():
                errors.append(f"{repo}: missing or escaping license snapshot")
            elif "Permission" not in snapshot.read_text() and "TERMS AND CONDITIONS" not in snapshot.read_text():
                errors.append(f"{repo}: incomplete license snapshot")
            if not source["reviewed_files"]:
                errors.append(f"{repo}: no file-level review")
            for item in source["reviewed_files"]:
                if not item["url"].startswith(prefix) or not re.fullmatch(r"[0-9a-f]{40}", item["blob_sha"]):
                    errors.append(f"{repo}: unpinned file review")
                if not item["license_scope"] or item["header_override_seen"] is not False:
                    errors.append(f"{repo}: license scope needs review")
        if covered != SKILLS:
            errors.append("source lock must cover exactly the seven published skills")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"cannot validate sources: {type(exc).__name__}")
    return errors


def validate(root: Path) -> tuple[list[str], list[Path]]:
    if not root.is_dir() or root.is_symlink():
        return ["package root must be an existing real directory"], []
    files, errors = files_under(root)
    for required in {"README.md", "LICENSE", "THIRD_PARTY_NOTICES.md", "docs/VALIDATION.md",
                     "docs/EVALUATION.md", "docs/INSTALLATION.md", "docs/KULLANIM-TR.md"}:
        if not (root / required).is_file():
            errors.append(f"missing required document: {required}")
    skills_root = root / "skills"
    actual = {p.parent.name for p in files if p.name == "SKILL.md" and p.parent.parent == skills_root}
    if actual != SKILLS:
        errors.append(f"skill set mismatch: missing={sorted(SKILLS - actual)}, extra={sorted(actual - SKILLS)}")
    for path in files:
        rel = str(path.relative_to(root))
        if path.relative_to(root).parts[0] not in {"skills", "docs", "scripts", "tests", "evals",
                "README.md", "LICENSE", "THIRD_PARTY_NOTICES.md", "CONTRIBUTING.md", "sources.lock.json", ".gitignore"}:
            errors.append(f"{rel}: outside reviewed publishable layout")
        if path.name.startswith(".env") or path.suffix in {".pem", ".key"}:
            errors.append(f"{rel}: potentially sensitive file name")
        if any(part in {".aws", ".ssh", ".codex", ".claude", ".agents"} for part in path.relative_to(root).parts):
            errors.append(f"{rel}: host/private configuration is not part of this draft")
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            errors.append(f"{rel}: unreadable or binary file requires review")
            continue
        for label, pattern in PRIVATE:
            if pattern.search(content):
                errors.append(f"{rel}: possible {label}; value withheld")
        if path.name == "SKILL.md":
            errors.extend(f"{rel}: {e}" for e in check_skill(path))
            if "!`" in content or "${CLAUDE_" in content:
                errors.append(f"{rel}: host-specific execution syntax is outside the portable profile")
        if path.suffix == ".md":
            errors.extend(f"{rel}: {e}" for e in check_links(path, root))
    errors.extend(check_evals(root))
    errors.extend(check_sources(root))
    return errors, files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--inventory", action="store_true", help="print relative file names and SHA-256 after validation")
    args = parser.parse_args()
    errors, files = validate(args.root.absolute())
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, indent=2))
        return 1
    result = {"status": "passed", "skills": len(SKILLS), "files_checked": len(files),
              "behavioral_evaluations": "not run", "host_smoke_tests": "not run"}
    if args.inventory:
        result["inventory"] = [{"path": str(p.relative_to(args.root.absolute())),
                                "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
