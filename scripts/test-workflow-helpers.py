import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(filename):
    spec = importlib.util.spec_from_file_location(filename, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


review = load("review-package.py")
validator = load("validate-skills.py")


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


class CatalogTests(unittest.TestCase):
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
