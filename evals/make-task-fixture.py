#!/usr/bin/env python3
"""Create a disposable task and guidance copy without expected outcomes."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess

from task_support import file_hashes, git, new_output


ROOT = Path(__file__).resolve().parents[1]


def create(case, output, skill=None, guidance_root=None, control=False):
    fixtures = json.loads((ROOT / "evals/task-fixtures.json").read_text())
    fixture = fixtures[case]
    guidance_root = Path(guidance_root or ROOT).resolve()
    skill = skill or fixture["skill"]
    if not control and skill not in {path.parent.name for path in (guidance_root / "shared").glob("*/SKILL.md")}:
        raise ValueError(f"No shared skill named {skill}")
    output = new_output(output)
    if output == guidance_root or guidance_root in output.parents:
        raise ValueError("Create task work outside the guidance source")
    repositories = fixture.get("repositories", ["."])
    if any(not (output / "repo" / name).resolve().is_relative_to(output / "repo") for name in repositories):
        raise ValueError("Repository path escapes its workspace")
    for name in [*fixture["files"], *fixture.get("change", {}).get("files", {})]:
        if not (output / "repo" / name).resolve().is_relative_to(output / "repo"):
            raise ValueError("Fixture file escapes its repository")
    if not control:
        for area in ("shared", "dotnet"):
            file_hashes(guidance_root / area)
    output.mkdir(parents=True, exist_ok=False)
    repo = output / "repo"
    repo.mkdir()
    for name, content in fixture["files"].items():
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    (output / "guidance").mkdir()
    if not control:
        for area in ("shared", "dotnet"):
            shutil.copytree(guidance_root / area, output / "guidance" / area)
    for name in repositories:
        checkout = repo / name
        checkout.mkdir(parents=True, exist_ok=True)
        for args in (["init", "-q"], ["config", "user.name", "Dana Reyes"],
                     ["config", "user.email", "dana@example.invalid"],
                     ["add", "."], ["commit", "-qm", "Import project"]):
            git(checkout, *args)
    if "change" in fixture:
        for name, content in fixture["change"]["files"].items():
            path = repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        for name in repositories:
            for args in (["add", "."], ["commit", "-qm", fixture["change"]["message"]]):
                git(repo / name, *args)
    skill_path = output / "guidance/shared" / skill / "SKILL.md"
    entry = "" if control else f"Use ${skill} at {skill_path}. "
    prompt = f"{entry}Work in {repo}. {fixture['prompt']} Read guidance only from {output / 'guidance'}."
    (output / "prompt.txt").write_text(prompt + "\n")
    return output / "prompt.txt"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=sorted(json.loads((ROOT / "evals/task-fixtures.json").read_text())))
    parser.add_argument("--output", required=True)
    parser.add_argument("--skill", help="entry skill to name instead of the task's default")
    parser.add_argument("--guidance-root", help="Steve's Agents checkout supplying shared/ and dotnet/")
    parser.add_argument("--control", action="store_true", help="omit the optional skill catalog and entry")
    args = parser.parse_args()
    try:
        print(create(args.case, args.output, args.skill, args.guidance_root, args.control))
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"make-task-fixture: {error}\n")
