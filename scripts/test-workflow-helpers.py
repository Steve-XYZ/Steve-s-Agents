import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load(filename):
    spec = importlib.util.spec_from_file_location(filename, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


review = load("review-package.py")
validator = load("validate-skills.py")
pr_state = load("pr-state.py")


class ReviewPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="review-fixture-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        (self.repo / "value").write_text("old\n")
        self.git("add", "value")
        self.git("commit", "-qm", "base")
        self.base = self.git("rev-parse", "HEAD")
        (self.repo / "value").write_text("new with spaces  \n")
        self.git("commit", "-qam", "head")
        self.head = self.git("rev-parse", "HEAD")

    def git(self, *args):
        return review.git(self.repo, *args)

    def test_exact_diff_and_immutable_refs(self):
        destination = review.package(self.repo, self.base, self.head, self.root / "review")
        manifest = json.loads((destination / "review.json").read_text())
        self.assertEqual(manifest["base_sha"], self.base)
        self.assertEqual(manifest["head_sha"], self.head)
        self.assertEqual(manifest["validation"], [])
        expected = review.git(self.repo, "diff", "--no-ext-diff", "--no-textconv", "--no-color", "--binary", "--full-index", self.base, self.head, "--", raw=True)
        self.assertEqual((destination / "diff.patch").read_text(), expected)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.head)
        self.assertEqual(self.git("status", "--porcelain"), "")
        with self.assertRaises(FileExistsError):
            review.package(self.repo, self.base, self.head, destination)

    def test_dirty_checkout_is_not_misrepresented(self):
        (self.repo / "value").write_text("uncommitted")
        with self.assertRaisesRegex(ValueError, "tracked edits"):
            review.package(self.repo, self.base, self.head, self.root / "review")
        self.assertFalse((self.root / "review").exists())

    def test_invalid_ref_and_in_tree_destination_leave_no_package(self):
        with self.assertRaises(subprocess.CalledProcessError):
            review.package(self.repo, "missing-ref", self.head, self.root / "review")
        with self.assertRaisesRegex(ValueError, "outside"):
            review.package(self.repo, self.base, self.head, self.repo / "review")
        self.assertFalse((self.root / "review").exists())
        self.assertFalse((self.repo / "review").exists())

    def evidence(self, **changes):
        artifact = self.root / "test.log"
        artifact.write_text("assertion passed\n")
        record = {"claim": "The changed value is observable", "command": "test-command",
                  "environment": "disposable fixture", "observed": "assertion passed",
                  "exit_code": 0, "tree_sha": self.git("rev-parse", self.head + "^{tree}"),
                  "head_sha": self.head, "artifact": "test.log", **changes}
        path = self.root / "evidence.json"
        path.write_text(json.dumps([record]))
        return path

    def test_evidence_freezes_output_and_preserves_failure(self):
        path = self.evidence(exit_code=1, observed="assertion failed")
        destination = review.package(self.repo, self.base, self.head, self.root / "review", path)
        record = json.loads((destination / "review.json").read_text())["validation"][0]
        (self.root / "test.log").write_text("overwritten")
        self.assertEqual(record["exit_code"], 1)
        self.assertEqual((destination / record["artifact"]).read_text(), "assertion passed\n")
        self.assertEqual(record["artifact_sha256"], review.hashlib.sha256(b"assertion passed\n").hexdigest())

    def test_evidence_rejects_wrong_state_and_missing_output(self):
        for change in ({"tree_sha": self.git("rev-parse", self.base + "^{tree}")},
                       {"head_sha": self.base}, {"head_sha": self.git("rev-parse", self.head + "^{tree}")}, {"head_sha": "HEAD"},
                       {"artifact": "missing.log"}, {"exit_code": True}, {"claim": ""}):
            with self.subTest(change=change):
                with self.assertRaises((ValueError, FileNotFoundError)):
                    review.package(self.repo, self.base, self.head, self.root / "review", self.evidence(**change))
                self.assertFalse((self.root / "review").exists())

    def test_untracked_work_is_excluded_explicitly(self):
        (self.repo / "untracked").write_text("not in this review")
        destination = review.package(self.repo, self.base, self.head, self.root / "review")
        self.assertNotIn("not in this review", (destination / "diff.patch").read_text())
        self.assertIn("untracked files excluded", (destination / "review.json").read_text())
        self.assertEqual((self.repo / "untracked").read_text(), "not in this review")


class PRStateTests(unittest.TestCase):
    HEAD = "a" * 40

    def view(self, **changes):
        return {"number": 7, "url": "https://github.com/example/repo/pull/7",
                "headRefOid": self.HEAD, "baseRefOid": "b" * 40,
                "headRefName": "feature", "baseRefName": "main", "isDraft": False,
                "state": "OPEN", "reviewDecision": "APPROVED", "mergeStateStatus": "CLEAN",
                "statusCheckRollup": [{"name": "tests"}], **changes}

    def check(self, bucket):
        return {"name": "tests", "state": "COMPLETED", "bucket": bucket,
                "link": "https://example.invalid/check", "workflow": "ci"}

    def test_ci_and_human_gates_are_separate(self):
        view = self.view(isDraft=True, reviewDecision="REVIEW_REQUIRED", mergeStateStatus="BLOCKED")
        result = pr_state.classify(view, [self.check("pass")], view, self.HEAD)
        self.assertEqual(set(result["conditions"]), {"DRAFT", "REVIEW_REQUIRED", "MERGE_BLOCKED", "OBSERVED_CHECKS_PASSED"})
        self.assertEqual(result["readiness"], "NOT_ASSESSED")
        for bucket, label in (("fail", "CHECKS_FAILED"), ("pending", "CHECKS_PENDING"),
                              ("cancel", "CHECKS_CANCELLED"), ("skipping", "CHECKS_SKIPPED")):
            with self.subTest(bucket=bucket):
                view = self.view(reviewDecision="CHANGES_REQUESTED")
                result = pr_state.classify(view, [self.check(bucket)], view, self.HEAD)
                self.assertIn(label, result["conditions"])
                self.assertIn("CHANGES_REQUESTED", result["conditions"])
                self.assertNotIn("OBSERVED_CHECKS_PASSED", result["conditions"])

    def test_stale_head_base_or_target_discards_checks(self):
        for change in ({"headRefOid": "c" * 40}, {"baseRefOid": "c" * 40},
                       {"baseRefName": "release"}, {"url": "https://example.invalid/other"}):
            with self.subTest(change=change):
                result = pr_state.classify(self.view(), [self.check("pass")], self.view(**change), self.HEAD)
                self.assertEqual(result["conditions"], ["STALE"])
                self.assertEqual(result["checks"], [])
        result = pr_state.classify(self.view(), [], self.view(), "d" * 40)
        self.assertEqual(result["conditions"], ["STALE"])

    def test_missing_or_unknown_state_never_passes(self):
        for checks in (None, {}, [{"name": "tests", "bucket": "new-status"}]):
            with self.subTest(checks=checks), self.assertRaises(ValueError):
                pr_state.classify(self.view(), checks, self.view(), self.HEAD)
        with self.assertRaises(ValueError):
            pr_state.classify({}, [], self.view(), self.HEAD)
        view = self.view(reviewDecision="")
        result = pr_state.classify(view, [], view, self.HEAD)
        self.assertEqual(set(result["conditions"]), {"REVIEW_REQUIREMENTS_UNKNOWN", "NO_CHECKS"})

    def test_collect_uses_explicit_repo_and_rechecks_identity(self):
        responses = [self.view(), [self.check("pass")], self.view(headRefOid="c" * 40)]
        with patch.object(pr_state, "read_gh", side_effect=responses) as read:
            result = pr_state.collect("example/repo", 7, self.HEAD)
        self.assertEqual(result["conditions"], ["STALE"])
        self.assertEqual(read.call_count, 3)
        for call in read.call_args_list:
            arguments = call.args[0]
            self.assertEqual(arguments[:1], ["pr"])
            self.assertIn(arguments[1], ("view", "checks"))
            self.assertEqual(arguments[arguments.index("--repo") + 1], "example/repo")

    def test_no_checks_and_checks_appearing_during_read(self):
        before = self.view(statusCheckRollup=[])
        with patch.object(pr_state, "read_gh", side_effect=[before, before]):
            self.assertIn("NO_CHECKS", pr_state.collect("example/repo", 7, self.HEAD)["conditions"])
        with patch.object(pr_state, "read_gh", side_effect=[before, self.view()]):
            with self.assertRaisesRegex(ValueError, "Checks changed"):
                pr_state.collect("example/repo", 7, self.HEAD)

    def test_cli_json_exit_codes_and_invalid_output(self):
        for code in (0, 1, 8):
            response = subprocess.CompletedProcess([], code, json.dumps([self.check("pending")]), "")
            with patch.object(pr_state.subprocess, "run", return_value=response):
                self.assertEqual(pr_state.read_gh(["pr", "checks"], allowed=(0, 1, 8))[0]["bucket"], "pending")
        for code, output in ((1, "network failed"), (4, "[]"), (0, "not-json")):
            response = subprocess.CompletedProcess([], code, output, "not displayed")
            with patch.object(pr_state.subprocess, "run", return_value=response), self.assertRaises(ValueError):
                pr_state.read_gh(["pr", "view"])


class CatalogTests(unittest.TestCase):
    def test_reference_cannot_escape_by_parent_path_or_symlink(self):
        with tempfile.TemporaryDirectory(prefix="catalog-fixture-") as tmp:
            root = Path(tmp) / "catalog"
            for name in ("shared", "dotnet", "evals"):
                shutil.copytree(ROOT / name, root / name)
            outside = Path(tmp) / "outside.md"
            outside.write_text("Outside the distributable catalog")
            skill = root / "shared/unslop/SKILL.md"
            original = skill.read_text()
            (skill.parent / "escape.md").symlink_to(outside)
            for target in ("../../../outside.md", "%2E%2E/%2E%2E/%2E%2E/outside.md", "escape.md"):
                with self.subTest(target=target):
                    skill.write_text(original + f"\n[escape]({target})\n")
                    self.assertTrue(any("escapes repository" in x for x in validator.validate(root)))
            skill.write_text(original + "\n[inside](../global-guidance/ENGINEERING.md)\n")
            self.assertEqual(validator.validate(root), [])

    def test_routing_fields_require_lists(self):
        with tempfile.TemporaryDirectory(prefix="catalog-fixture-") as tmp:
            root = Path(tmp)
            for name in ("shared", "dotnet", "evals"):
                shutil.copytree(ROOT / name, root / name)
            fixture = root / "evals/routing.json"
            original = fixture.read_text()
            for field in ("expectations", "load", "avoid"):
                for value in ("malformed", "", {}, None):
                    with self.subTest(field=field, value=value):
                        cases = json.loads(original)
                        cases[0][field] = value
                        fixture.write_text(json.dumps(cases))
                        self.assertTrue(any("must be lists" in x for x in validator.validate(root)))

    def test_current_catalog_and_seeded_regressions(self):
        self.assertEqual(validator.validate(ROOT), [])
        with tempfile.TemporaryDirectory(prefix="catalog-fixture-") as tmp:
            root = Path(tmp)
            for name in ("shared", "dotnet", "evals"):
                shutil.copytree(ROOT / name, root / name)
            skill = root / "shared/unslop/SKILL.md"
            original = skill.read_text()
            skill.write_text(original + "\n[missing](references/missing.md)\n")
            self.assertTrue(any("missing reference" in x for x in validator.validate(root)))
            skill.write_text(original.replace("name: unslop", "name: code-review"))
            self.assertTrue(any("duplicate installed name" in x for x in validator.validate(root)))
            skill.write_text(original)
            cases = json.loads((root / "evals/routing.json").read_text())
            cases[0]["load"].append("deleted-skill")
            (root / "evals/routing.json").write_text(json.dumps(cases))
            self.assertTrue(any("unknown skill" in x for x in validator.validate(root)))


if __name__ == "__main__":
    unittest.main()
