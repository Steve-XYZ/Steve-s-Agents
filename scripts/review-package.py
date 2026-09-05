#!/usr/bin/env python3
"""Freeze a committed diff for review without changing the reviewed checkout."""

import argparse
import json
from pathlib import Path
import subprocess
import tempfile


def git(repo, *args, raw=False):
    output = subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True, stderr=subprocess.PIPE,
    )
    return output if raw else output.strip()


def package(repo, base, head, output=None):
    repo = Path(git(repo, "rev-parse", "--show-toplevel"))
    base = git(repo, "rev-parse", "--verify", "--end-of-options", base + "^{commit}")
    head = git(repo, "rev-parse", "--verify", "--end-of-options", head + "^{commit}")
    if git(repo, "status", "--porcelain", "--untracked-files=no"):
        raise ValueError("Commit or isolate tracked edits first; this package covers commits only.")
    destination = Path(output).resolve() if output else Path(tempfile.mkdtemp(prefix="agent-review-"))
    if destination == repo or repo in destination.parents:
        raise ValueError("Keep review packages outside the reviewed worktree.")
    if output:
        destination.mkdir(parents=True, exist_ok=False)
    diff = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--no-color", "--binary", "--full-index", base, head, "--", raw=True)
    stat = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--stat", base, head, "--")
    (destination / "diff.patch").write_text(diff)
    (destination / "stat.txt").write_text(stat + "\n")
    (destination / "review.json").write_text(json.dumps({
        "base_sha": base,
        "head_sha": head,
        "head_tree": git(repo, "rev-parse", head + "^{tree}"),
        "diff": "diff.patch",
        "scope": "exact base-to-head committed tree difference; untracked files excluded",
        "validation": [],
    }, indent=2) + "\n")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--base", required=True, help="Use the PR merge base for initial review; prior reviewed head for a fix round.")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--output", help="New directory outside the reviewed worktree; defaults to a temporary directory.")
    args = parser.parse_args()
    try:
        print(package(args.repo, args.base, args.head, args.output))
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"review-package: {error}\n")


if __name__ == "__main__":
    main()
