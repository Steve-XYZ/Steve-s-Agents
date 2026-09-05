#!/usr/bin/env python3
"""Exercise the installer in disposable homes; no model or live CLI required."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1]


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agent-links-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "clone with spaces"
        shutil.copytree(SOURCE, self.repo, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        self.user_dir = self.root / "user with spaces"
        self.user_dir.mkdir()
        self.env = {**os.environ, "HOME": str(self.user_dir)}
        self.env.pop("CODEX_HOME", None)
        self.guidance = self.repo / "shared/global-guidance/ENGINEERING.md"

    def run_install(self, *args, expected=0):
        result = subprocess.run(
            ["sh", str(self.repo / "scripts/install-agent-links.sh"), *args],
            env=self.env, cwd=self.root, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout

    def assert_link(self, target, source):
        self.assertTrue(target.is_symlink(), str(target))
        self.assertEqual(target.readlink(), source)

    def snapshot(self):
        return {
            str(p.relative_to(self.root)): (
                ("link", str(p.readlink())) if p.is_symlink()
                else ("dir",) if p.is_dir() else ("file", p.read_bytes())
            )
            for p in self.root.rglob("*")
        }

    def test_fresh_install_and_repeat(self):
        for cli in (".codex", ".claude"):
            (self.user_dir / cli).mkdir()
        self.run_install()
        for cli, filename in ((".codex", "AGENTS.md"), (".claude", "CLAUDE.md")):
            self.assert_link(self.user_dir / cli / filename, self.guidance)
            for skill in list((self.repo / "shared").glob("*/SKILL.md")) + list((self.repo / "dotnet").glob("*/SKILL.md")):
                self.assert_link(self.user_dir / cli / "skills" / skill.parent.name, skill.parent)
        before = self.snapshot()
        self.assertIn("linked=0", self.run_install())
        self.assertEqual(before, self.snapshot())

    def test_no_cli_is_a_noop(self):
        before = self.snapshot()
        self.assertIn("linked=0", self.run_install())
        self.assertEqual(before, self.snapshot())

    def test_custom_codex_home_and_explicit_skill_root(self):
        custom = self.root / "custom codex home"
        custom.mkdir()
        self.env["CODEX_HOME"] = str(custom)
        default = self.user_dir / ".codex"
        default.mkdir()
        (default / "AGENTS.md").write_text("unrelated guidance")
        self.run_install()
        self.assert_link(custom / "AGENTS.md", self.guidance)
        self.assert_link(custom / "skills/unslop", self.repo / "shared/unslop")
        explicit = self.root / "explicit skills"
        self.run_install(f"--codex-skills-root={explicit}")
        self.assert_link(explicit / "unslop", self.repo / "shared/unslop")
        self.assertEqual((default / "AGENTS.md").read_text(), "unrelated guidance")
        self.assertFalse((default / "skills").exists())

    def test_upgrade_retires_only_owned_links_and_dry_run_writes_nothing(self):
        for cli in (".codex", ".claude"):
            skills = self.user_dir / cli / "skills"
            skills.mkdir(parents=True)
            (skills / "engineering-judgment").symlink_to(self.repo / "shared/engineering-judgment")
            (skills / "unrelated").symlink_to(self.root / "missing-external-skill")
        neutral = self.user_dir / ".agent-guidance"
        neutral.symlink_to(self.repo / "shared/global-guidance")
        before = self.snapshot()
        self.assertIn("retired=3", self.run_install("--dry-run"))
        self.assertEqual(before, self.snapshot())
        self.assertIn("retired=3", self.run_install())
        self.assertFalse(neutral.is_symlink())
        for cli in (".codex", ".claude"):
            self.assertFalse((self.user_dir / cli / "skills/engineering-judgment").is_symlink())
            self.assertTrue((self.user_dir / cli / "skills/unrelated").is_symlink())
        backups = list((self.user_dir / ".agent-links-backup").glob("*/*"))
        self.assertEqual(len(backups), 3)
        self.assertTrue(all(p.is_symlink() for p in backups))
        before = self.snapshot()
        self.run_install()
        self.assertEqual(before, self.snapshot())

    def test_unknown_retired_names_are_preserved(self):
        codex = self.user_dir / ".codex/skills"
        claude = self.user_dir / ".claude/skills"
        codex.mkdir(parents=True)
        claude.mkdir(parents=True)
        (codex / "engineering-judgment").mkdir()
        (codex / "engineering-judgment/notes").write_text("keep")
        foreign = self.root / "other-clone/shared/engineering-judgment"
        (claude / "engineering-judgment").symlink_to(foreign)
        self.run_install()
        self.assertEqual((codex / "engineering-judgment/notes").read_text(), "keep")
        self.assert_link(claude / "engineering-judgment", foreign)

    def test_conflicts_are_backed_up_and_settings_are_merged(self):
        cli = self.user_dir / ".claude"
        (cli / "skills/unslop").mkdir(parents=True)
        (cli / "skills/unslop/custom.txt").write_text("custom skill")
        (cli / "CLAUDE.md").write_text("custom guidance")
        original = {"theme": "dark", "permissions": {"allow": ["Read"], "additionalDirectories": ["/existing"]}}
        settings = cli / "settings.json"
        settings.write_text(json.dumps(original))
        self.run_install()
        merged = json.loads(settings.read_text())
        self.assertEqual(merged["theme"], "dark")
        self.assertEqual(merged["permissions"]["allow"], ["Read"])
        self.assertEqual(merged["permissions"]["additionalDirectories"], ["/existing", str(self.repo)])
        backups = self.user_dir / ".agent-links-backup"
        self.assertEqual(next(backups.glob("*/.claude_CLAUDE.md")).read_text(), "custom guidance")
        self.assertEqual(next(backups.glob("*/.claude_skills_unslop/custom.txt")).read_text(), "custom skill")
        self.assertEqual(json.loads(next(backups.glob("*/.claude_settings.json")).read_text()), original)

    def test_invalid_settings_are_not_replaced(self):
        cli = self.user_dir / ".claude"
        cli.mkdir()
        settings = cli / "settings.json"
        settings.write_text("{broken")
        self.run_install(expected=1)
        self.assertEqual(settings.read_text(), "{broken")


if __name__ == "__main__":
    unittest.main()
