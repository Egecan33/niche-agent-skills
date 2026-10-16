"""Original tests for package integrity and meaningful negative controls."""

import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


validator = module("validate_package")
checker = module("check_fixture")


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "package"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns("__pycache__", ".git", "eval-runs"))
        self.skill = self.root / "skills/agent-trajectory-regression/SKILL.md"

    def tearDown(self):
        self.temp.cleanup()

    def errors(self):
        return validator.validate(self.root)[0]

    def change_skill(self, old, new):
        self.skill.write_text(self.skill.read_text().replace(old, new), encoding="utf-8")

    def test_reviewed_package_passes(self):
        self.assertEqual(self.errors(), [])

    def test_name_directory_mismatch(self):
        self.change_skill("name: agent-trajectory-regression", "name: another-name")
        self.assertTrue(any("parent directory" in e for e in self.errors()))

    def test_invalid_name(self):
        self.change_skill("name: agent-trajectory-regression", "name: Invalid--Name")
        self.assertTrue(any("lowercase" in e for e in self.errors()))

    def test_duplicate_frontmatter(self):
        self.change_skill("name: agent-trajectory-regression", "name: agent-trajectory-regression\nname: agent-trajectory-regression")
        self.assertTrue(any("duplicate" in e for e in self.errors()))

    def test_permission_field_rejected(self):
        self.change_skill("name: agent-trajectory-regression", "name: agent-trajectory-regression\nallowed-tools: Bash(*)")
        self.assertTrue(any("frontmatter" in e for e in self.errors()))

    def test_broken_reference(self):
        self.change_skill("references/example.md", "references/missing.md")
        self.assertTrue(any("missing relative link" in e for e in self.errors()))

    def test_reference_cannot_leave_installed_skill(self):
        self.change_skill("references/example.md", "../../README.md")
        self.assertTrue(any("boundary" in e for e in self.errors()))

    def test_symlink_not_followed(self):
        (self.root / "outside").symlink_to(self.root.parent, target_is_directory=True)
        self.assertTrue(any("symlink" in e for e in self.errors()))

    def test_secret_report_withholds_value(self):
        secret = "gh" + "p_" + "A" * 36
        (self.root / "docs/leak.txt").write_text(secret)
        report = "\n".join(self.errors())
        self.assertIn("credential", report)
        self.assertNotIn(secret, report)

    def test_private_path_rejected(self):
        (self.root / "docs/local.txt").write_text("/" + "Users/fictional-person/private.txt")
        self.assertTrue(any("home path" in e for e in self.errors()))

    def test_email_rejected(self):
        (self.root / "docs/contact.txt").write_text("private" + "@" + "example.invalid")
        self.assertTrue(any("email address" in e for e in self.errors()))

    def test_unpinned_source_rejected(self):
        path = self.root / "sources.lock.json"
        data = json.loads(path.read_text())
        data["sources"][0]["commit"] = "main"
        path.write_text(json.dumps(data))
        self.assertTrue(any("immutable" in e for e in self.errors()))

    def test_missing_license_notice_rejected(self):
        (self.root / "docs/upstream-licenses/pgtap.txt").unlink()
        self.assertTrue(any("license snapshot" in e for e in self.errors()))

    def test_missing_negative_trigger_rejected(self):
        path = self.root / "evals/cases.json"
        data = json.loads(path.read_text())
        data["cases"] = [c for c in data["cases"] if c["id"] != "agent-trajectory-regression-routing-4"]
        path.write_text(json.dumps(data))
        self.assertTrue(any("two negative" in e for e in self.errors()))

    def test_trigger_expectation_must_be_boolean(self):
        path = self.root / "evals/cases.json"
        data = json.loads(path.read_text())
        data["cases"][0]["should_trigger"] = "true"
        path.write_text(json.dumps(data))
        self.assertTrue(any("must be boolean" in e for e in self.errors()))

    def test_validation_cli_nonzero_on_bad_input(self):
        self.change_skill("name: agent-trajectory-regression", "name: Invalid")
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate_package.py"), str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["status"], "failed")

    def test_inventory_does_not_modify_content(self):
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate_package.py"), str(self.root), "--inventory"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout)
        data = json.loads(result.stdout)
        self.assertEqual(data["skills"], 7)
        self.assertEqual(len(data["inventory"]), data["files_checked"])
        after = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)


class FixtureTests(unittest.TestCase):
    def fixture(self, skill):
        return json.loads((ROOT / "skills" / skill / "assets/case.json").read_text())

    def test_all_33_synthetic_controls(self):
        paths = sorted(ROOT.glob("skills/*/assets/case.json"))
        self.assertEqual(len(paths), 7)
        results = [r for path in paths for r in checker.run_fixture(path)]
        self.assertEqual(len(results), 33)
        self.assertTrue(all(r["passed"] for r in results), results)

    def test_trajectory_argument_mutation_fails(self):
        f = self.fixture("agent-trajectory-regression")
        value = copy.deepcopy(f["cases"][0]["input"])
        value["calls"][1]["arguments"]["record_id"] = 8
        self.assertIn("significant-argument", checker.trajectory(value, f))

    def test_duplicate_rows_are_not_collapsed(self):
        data = {"effective_role": "authenticated", "positive_control": True,
                "expected_rows": ["a"], "actual_rows": ["a", "a"]}
        self.assertIn("row-set-mismatch", checker.rls(data, {}))

    def test_api_missing_required_field(self):
        f = self.fixture("openapi-contract-probes")
        data = {"status": 200, "content_type": "application/json", "body": {}}
        self.assertIn("response-required-field", checker.openapi(data, f))

    def test_boolean_is_not_json_integer(self):
        f = self.fixture("openapi-contract-probes")
        data = {"status": 200, "content_type": "application/json", "body": {"quantity": True}}
        self.assertIn("response-type", checker.openapi(data, f))

    def test_union_handles_nested_disjoint_and_touching(self):
        self.assertEqual(checker.interval_union([(0, 5), (1, 3), (5, 7), (10, 12)]), 9)

    def test_negative_span_time_rejected(self):
        f = self.fixture("trace-failure-diagnosis")
        f["spans"][1]["end_ms"] = -1
        self.assertEqual(checker.trace(f["cases"][0]["input"], f), {"invalid-timing"})

    def test_session_requires_sanitization(self):
        f = self.fixture("masked-session-to-sop")
        data = copy.deepcopy(f["cases"][0]["input"])
        data["sanitized"] = False
        self.assertIn("sanitization-required", checker.session(data, f))

    def test_dataset_unknown_source_rejected(self):
        f = self.fixture("grounded-synthetic-datasets")
        data = copy.deepcopy(f["cases"][0]["input"])
        data["rows"][0]["source_id"] = "unlisted"
        self.assertIn("missing-provenance", checker.dataset(data, f))

    def test_pdf_raw_evidence_must_match(self):
        f = self.fixture("pdf-table-evidence")
        data = copy.deepcopy(f["cases"][0]["input"])
        data["ledger"][0]["raw_text"] = "1,500"
        self.assertIn("raw-text-mismatch", checker.pdf(data, f))

    def test_changed_oracle_causes_fixture_cli_failure(self):
        f = self.fixture("agent-trajectory-regression")
        f["cases"][1]["issues"] = []
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "case.json"
            path.write_text(json.dumps(f))
            result = subprocess.run([sys.executable, str(ROOT / "scripts/check_fixture.py"), str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["status"], "failed")


if __name__ == "__main__":
    unittest.main()
