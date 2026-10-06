#!/usr/bin/env python3
"""Create a disposable task and guidance copy without expected outcomes."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def create(case, output, skill=None):
    fixtures = json.loads((ROOT / "evals/task-fixtures.json").read_text())
    fixture = fixtures[case]
    skill = skill or fixture["skill"]
    if not (ROOT / "shared" / skill / "SKILL.md").is_file():
        raise ValueError(f"No shared skill named {skill}")
    output = Path(output).resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError("Create trial work outside the guidance repository")
    for name in fixture["files"]:
        if not (output / "repo" / name).resolve().is_relative_to(output / "repo"):
            raise ValueError("Fixture file escapes its repository")
    output.mkdir(parents=True, exist_ok=False)
    repo = output / "repo"
    repo.mkdir()
    for name, content in fixture["files"].items():
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    for area in ("shared", "dotnet"):
        shutil.copytree(ROOT / area, output / "guidance" / area)
    for args in (["init", "-q"], ["config", "user.name", "Fixture"],
                 ["config", "user.email", "fixture@example.invalid"],
                 ["add", "."], ["commit", "-qm", "fixture baseline"]):
        subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)
    skill_path = output / "guidance/shared" / skill / "SKILL.md"
    prompt = f"Use ${skill} at {skill_path}. Work in {repo}. {fixture['prompt']} Read guidance only from this supplied catalog."
    (output / "prompt.txt").write_text(prompt + "\n")
    return output / "prompt.txt"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=sorted(json.loads((ROOT / "evals/task-fixtures.json").read_text())))
    parser.add_argument("--output", required=True)
    parser.add_argument("--skill", help="entry skill to name instead of the task's default")
    args = parser.parse_args()
    try:
        print(create(args.case, args.output, args.skill))
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"make-task-fixture: {error}\n")
