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
set_workspace = load("set-workspace.py")
related = load("related-work.py")


class SiblingRepos:
    """Two sibling checkouts whose origin line is a local remote-tracking ref."""

    def make(self):
        self.temp = tempfile.TemporaryDirectory(prefix="workspace-fixture-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / "BOS"
        self.workspace.mkdir()
        (self.workspace / "AGENTS.md").write_text("workspace rules\n")
        (self.workspace / "CONTRACTS.md").write_text("contract map\n")
        for name in ("alpha", "beta"):
            repo = self.workspace / name
            repo.mkdir()
            self.git(name, "init", "-q", "-b", "main")
            self.git(name, "config", "user.name", "Fixture")
            self.git(name, "config", "user.email", "fixture@example.invalid")
            (repo / "Formatter.cs").write_text("old\n")
            (repo / "Other.cs").write_text("other\n")
            self.git(name, "add", ".")
            self.git(name, "commit", "-qm", "base")
            self.git(name, "update-ref", "refs/remotes/origin/line", "HEAD")
            (repo / "AGENTS.md").write_text(f"{name} rules\n")
            (repo / ".git/info/exclude").write_text("AGENTS.md\nCLAUDE.md\n")

    def git(self, name, *args):
        return review.git(self.workspace / name, *args)

    def commit(self, name, path, text, message):
        (self.workspace / name / path).write_text(text)
        self.git(name, "add", path)
        self.git(name, "commit", "-qm", message)
        return self.git(name, "rev-parse", "HEAD")


class SetWorkspaceTests(SiblingRepos, unittest.TestCase):
    def setUp(self):
        self.make()
        self.sets = self.root / "BOS-sets"

    def test_detached_worktrees_at_each_line_with_linked_guidance(self):
        self.git("beta", "update-ref", "refs/remotes/origin/other", "HEAD")
        line = self.git("alpha", "rev-parse", "origin/line")
        self.commit("alpha", "Other.cs", "moved on\n", "unrelated local work")
        destination, commits = set_workspace.create(self.workspace, self.sets, "set-1", "line", ["alpha", "beta=other"])
        self.assertEqual(destination, self.sets.resolve() / "set-1")
        self.assertEqual(commits["alpha"], ("line", line))
        self.assertEqual(commits["beta"][0], "other")
        self.assertEqual((destination / "AGENTS.md").resolve(), (self.workspace / "AGENTS.md").resolve())
        self.assertEqual((destination / "CONTRACTS.md").read_text(), "contract map\n")
        self.assertFalse((destination / "CLAUDE.md").exists())
        self.assertEqual((destination / "alpha/AGENTS.md").read_text(), "alpha rules\n")
        self.assertEqual(review.git(destination / "alpha", "rev-parse", "HEAD"), line)
        self.assertEqual(review.git(destination / "alpha", "status", "--porcelain"), "")
        self.assertNotEqual(self.git("alpha", "rev-parse", "HEAD"), line)

    def test_missing_line_or_folder_inside_workspace_creates_nothing(self):
        with self.assertRaisesRegex(ValueError, "names a commit"):
            set_workspace.create(self.workspace, self.sets, "set-1", "missing")
        with self.assertRaisesRegex(ValueError, "pass --base"):
            set_workspace.create(self.workspace, self.sets, "set-1", None, ["alpha"])
        with self.assertRaisesRegex(ValueError, "not a Git checkout"):
            set_workspace.create(self.workspace, self.sets, "set-1", "line", ["gamma"])
        with self.assertRaisesRegex(ValueError, "outside"):
            set_workspace.create(self.workspace, self.workspace / "sets", "set-1", "line")
        self.assertFalse(self.sets.exists())
        self.assertFalse((self.workspace / "sets").exists())
        self.assertEqual(self.git("alpha", "worktree", "list").count("\n"), 0)

    def test_remove_refuses_changes_and_keeps_the_set_note(self):
        destination, _ = set_workspace.create(self.workspace, self.sets, "set-1", "line")
        (destination / "alpha/Formatter.cs").write_text("unfinished\n")
        with self.assertRaisesRegex(ValueError, "changes first"):
            set_workspace.remove(self.workspace, self.sets, "set-1")
        self.assertTrue((destination / "beta/Formatter.cs").exists())
        review.git(destination / "alpha", "checkout", "--", "Formatter.cs")
        (destination / "SET.md").write_text("decisions\n")
        self.assertEqual(set_workspace.remove(self.workspace, self.sets, "set-1"), ["SET.md"])
        self.assertEqual(sorted(p.name for p in destination.iterdir()), ["SET.md"])
        self.assertEqual(self.git("alpha", "worktree", "list").count("\n"), 0)
        (destination / "SET.md").unlink()
        destination.rmdir()
        set_workspace.create(self.workspace, self.sets, "set-2", "line")
        self.assertEqual(set_workspace.remove(self.workspace, self.sets, "set-2"), [])
        self.assertFalse((self.sets / "set-2").exists())

    def test_set_names_cannot_leave_the_sets_folder(self):
        (self.workspace / "sets").mkdir()
        for name in ("../BOS/sets", "nested/set", "..", ".", ""):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "one folder name"):
                set_workspace.create(self.workspace, self.sets, name, "line")
        with self.assertRaisesRegex(ValueError, "one folder name"):
            set_workspace.remove(self.workspace, self.sets, "../BOS/alpha")
        self.assertEqual(list((self.workspace / "sets").iterdir()), [])
        self.assertEqual(self.git("alpha", "worktree", "list").count("\n"), 0)

    def test_remove_keeps_detached_commits_reachable(self):
        destination, _ = set_workspace.create(self.workspace, self.sets, "set-1", "line")
        alpha = destination / "alpha"
        (alpha / "Formatter.cs").write_text("committed in the set\n")
        review.git(alpha, "commit", "-qam", "detached work")
        work = review.git(alpha, "rev-parse", "HEAD")
        with self.assertRaisesRegex(ValueError, "on no branch or tag"):
            set_workspace.remove(self.workspace, self.sets, "set-1")
        self.assertTrue(alpha.is_dir())
        self.assertTrue((destination / "beta").is_dir())
        review.git(alpha, "branch", "keep/set-work")
        self.assertEqual(set_workspace.remove(self.workspace, self.sets, "set-1"), [])
        self.assertEqual(self.git("alpha", "rev-parse", "keep/set-work"), work)

    def test_inherited_git_dir_cannot_redirect_removal_checks(self):
        destination, _ = set_workspace.create(self.workspace, self.sets, "set-1", "line")
        alpha = destination / "alpha"
        (alpha / "Formatter.cs").write_text("committed in the set\n")
        review.git(alpha, "commit", "-qam", "detached work")
        hook_env = {**set_workspace.GIT_ENV, "GIT_DIR": str(self.workspace / "alpha/.git"),
                    "GIT_WORK_TREE": str(self.workspace / "alpha")}
        with patch.dict(set_workspace.os.environ, hook_env, clear=True):
            env = set_workspace.clean_env()
        self.assertNotIn("GIT_DIR", env)
        self.assertNotIn("GIT_WORK_TREE", env)
        with patch.object(set_workspace, "GIT_ENV", env), self.assertRaisesRegex(ValueError, "on no branch or tag"):
            set_workspace.remove(self.workspace, self.sets, "set-1")
        self.assertTrue(alpha.is_dir())

    def test_remove_rejects_a_folder_that_is_not_a_worktree(self):
        stray = self.sets / "set-1" / "alpha"
        stray.mkdir(parents=True)
        with self.assertRaises((ValueError, subprocess.CalledProcessError)):
            set_workspace.remove(self.workspace, self.sets, "set-1")
        self.assertTrue(stray.exists())


class RelatedWorkTests(SiblingRepos, unittest.TestCase):
    def setUp(self):
        self.make()

    def branch(self, name, branch, path, text):
        self.git(name, "checkout", "-q", "-b", branch, "origin/line")
        commit = self.commit(name, path, text, f"{branch} work")
        self.git(name, "checkout", "-q", "main")
        return commit

    def scan(self, name, **options):
        settings = {"patterns": ["*Formatter*"], "regexes": [], "since_days": 30, "exclude": [], **options}
        return related.scan(self.workspace / name, "line", settings["patterns"], settings["regexes"],
                            settings["since_days"], settings["exclude"])

    def test_reports_only_unmerged_branches_touching_the_paths(self):
        commit = self.branch("alpha", "feature/BOS-1", "Formatter.cs", "label v1\n")
        self.git("alpha", "update-ref", "refs/remotes/origin/feature/BOS-1", commit)
        self.branch("alpha", "feature/BOS-2", "Other.cs", "unrelated\n")
        self.git("alpha", "branch", "-q", "merged", "origin/line")
        result = self.scan("alpha")
        self.assertEqual([b["branch"] for b in result["branches"]], ["feature/BOS-1"])
        self.assertEqual(result["branches"][0]["files"], ["Formatter.cs"])
        self.assertEqual(self.scan("alpha", exclude=["*BOS-1"])["branches"], [])
        self.assertEqual(self.scan("beta")["branches"], [])

    def test_skips_the_current_branch_and_matches_code_by_regex(self):
        self.branch("alpha", "feature/BOS-3", "Other.cs", "FormatDrawName()\n")
        self.assertEqual(self.scan("alpha")["branches"], [])
        result = self.scan("alpha", patterns=[], regexes=["FormatDrawName"])
        self.assertEqual(result["branches"][0]["files"], ["Other.cs"])
        self.git("alpha", "checkout", "-q", "feature/BOS-3")
        self.assertEqual(self.scan("alpha", patterns=[], regexes=["FormatDrawName"])["branches"], [])

    def test_reports_uncommitted_work_in_other_worktrees(self):
        other = self.root / "thread-2"
        self.git("alpha", "worktree", "add", "-q", "-b", "feature/BOS-4", str(other), "origin/line")
        (other / "Formatter.cs").write_text("in progress\n")
        (self.workspace / "alpha/Formatter.cs").write_text("own edit\n")
        result = self.scan("alpha")
        self.assertEqual(result["worktrees"], [{"worktree": str(other.resolve()), "branch": "feature/BOS-4", "files": ["Formatter.cs"]}])

    def test_regex_alone_checks_uncommitted_work_in_other_worktrees(self):
        other = self.root / "thread-3"
        self.git("alpha", "worktree", "add", "-q", "-b", "feature/BOS-6", str(other), "origin/line")
        (other / "Other.cs").write_text("FormatDrawName()\n")
        (other / "New.cs").write_text("calls FormatDrawName\n")
        (other / "Unrelated.cs").write_text("nothing here\n")
        result = self.scan("alpha", patterns=[], regexes=["FormatDrawName"])
        self.assertEqual(result["worktrees"][0]["files"], ["New.cs", "Other.cs"])

    def test_quoted_paths_and_posix_classes_match_like_git(self):
        other = self.root / "thread-4"
        self.git("alpha", "worktree", "add", "-q", "-b", "feature/BOS-7", str(other), "origin/line")
        (other / "Other.cs").write_text("Format DrawName()\n")
        (other / "New File.cs").write_text("Format DrawName()\n")
        (other / "Quote\"d.cs").write_text("Format\tDrawName()\n")
        (other / "Plain.cs").write_text("FormatDrawName()\n")
        result = self.scan("alpha", patterns=[], regexes=["Format[[:space:]]+DrawName"])
        self.assertEqual(result["worktrees"][0]["files"], ["New File.cs", "Other.cs", "Quote\"d.cs"])
        result = self.scan("alpha", patterns=["New File.cs"], regexes=[])
        self.assertEqual(result["worktrees"][0]["files"], ["New File.cs"])

    def test_reports_recent_changes_on_the_line(self):
        commit = self.commit("beta", "Formatter.cs", "merged label\n", "BOS-5 merged")
        self.git("beta", "update-ref", "refs/remotes/origin/line", commit)
        result = self.scan("beta")
        self.assertEqual([(c["commit"], c["subject"]) for c in result["recent_on_base"]], [(commit, "BOS-5 merged")])
        self.assertEqual(self.scan("beta", since_days=-1)["recent_on_base"], [])


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

    def test_model_profile_examples_are_complete(self):
        import tomllib
        examples = [ROOT / f"configs/{machine}/agents/model-profiles.toml.example" for machine in ("wsl", "macos")]
        self.assertEqual(examples[0].read_text(), examples[1].read_text())
        profile = tomllib.loads(examples[0].read_text())
        self.assertGreater(profile["limits"]["max_concurrent_workers"], 0)
        entries = {"reviewer": profile["reviewer"], "verifier": profile["verifier"],
                   **{f"tiers.{k}": v for k, v in profile["tiers"].items()},
                   **{f"fallback.{k}": v for k, v in profile["fallback"].items()}}
        self.assertEqual(set(profile), {"limits", "tiers", "reviewer", "verifier", "fallback"})
        self.assertEqual(set(profile["tiers"]), {"low", "medium", "high"})
        self.assertEqual(set(profile["fallback"]), {"medium", "high"})
        for name, entry in entries.items():
            with self.subTest(entry=name):
                self.assertEqual(set(entry), {"provider", "model", "thinking"})

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

    def test_skill_authoring_rules(self):
        with tempfile.TemporaryDirectory(prefix="catalog-fixture-") as tmp:
            root = Path(tmp)
            for name in ("shared", "dotnet", "evals"):
                shutil.copytree(ROOT / name, root / name)
            skill = root / "shared/unslop/SKILL.md"
            original = skill.read_text()
            cases = {
                "must start with \"Use \"": original.replace("description: Use for", "description: Writes"),
                "description exceeds 1024": original.replace("description: Use for", "description: Use for " + "x" * 1024),
                "words; limit": original + ("word " * validator.MAX_SKILL_WORDS),
            }
            for message, text in cases.items():
                with self.subTest(message=message):
                    skill.write_text(text)
                    self.assertTrue(any(message in x for x in validator.validate(root)), validator.validate(root))
            skill.write_text(original)
            metadata = root / "shared/unslop/agents/openai.yaml"
            metadata.write_text(metadata.read_text().replace("$unslop", "$other"))
            self.assertTrue(any("must name $unslop" in x for x in validator.validate(root)))
            metadata.unlink()
            self.assertTrue(any("missing agents/openai.yaml" in x for x in validator.validate(root)))

    def test_skills_link_other_skills_only_through_handoff_contracts(self):
        with tempfile.TemporaryDirectory(prefix="catalog-fixture-") as tmp:
            root = Path(tmp)
            for name in ("shared", "dotnet", "evals"):
                shutil.copytree(ROOT / name, root / name)
            skill = root / "shared/shape-feature/SKILL.md"
            original = skill.read_text()
            skill.write_text(original + "\n[scope](../blast-radius/references/ticket-scope.md)\n")
            self.assertTrue(any("links into another skill" in x for x in validator.validate(root)))
            skill.write_text(original + "\n[handoff](../code-review/references/review-evidence.md)\n")
            self.assertEqual(validator.validate(root), [])


if __name__ == "__main__":
    unittest.main()
