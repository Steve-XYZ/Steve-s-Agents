#!/usr/bin/env python3
"""Create a disposable task and guidance copy without expected outcomes."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def create(case, output):
    fixtures = json.loads((ROOT / "evals/task-fixtures.json").read_text())
    fixture = fixtures[case]
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
    skill = output / "guidance/shared" / fixture["skill"] / "SKILL.md"
    prompt = f"Use ${fixture['skill']} at {skill}. Work in {repo}. {fixture['prompt']} Read guidance only from this supplied catalog."
    (output / "prompt.txt").write_text(prompt + "\n")
    return output / "prompt.txt"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("simple", "slices", "shape", "feedback"))
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        print(create(args.case, args.output))
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"make-task-fixture: {error}\n")
