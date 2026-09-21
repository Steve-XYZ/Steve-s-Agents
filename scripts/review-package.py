#!/usr/bin/env python3
"""Freeze a committed diff for review without changing the reviewed checkout."""

import argparse
import hashlib
import json
import re
from pathlib import Path
import subprocess
import tempfile


def git(repo, *args, raw=False):
    output = subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True, stderr=subprocess.PIPE,
    )
    return output if raw else output.strip()


def read_evidence(path, repo, tree):
    if path is None:
        return []
    path = Path(path).resolve()
    records = json.loads(path.read_text())
    if not isinstance(records, list):
        raise ValueError("Evidence must be a JSON list")
    validated = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Each evidence record must be an object")
        for field in ("claim", "command", "environment", "observed", "artifact", "tree_sha"):
            if not isinstance(record.get(field), str) or not record[field].strip():
                raise ValueError(f"Evidence requires nonempty {field}")
        if type(record.get("exit_code")) is not int:
            raise ValueError("Evidence requires an integer exit_code")
        if record["tree_sha"] != tree:
            raise ValueError("Evidence tree differs from the reviewed tree")
        if "head_sha" in record:
            tested = record["head_sha"]
            if not isinstance(tested, str) or not re.fullmatch(r"[0-9a-f]{40}", tested):
                raise ValueError("Evidence requires a full commit SHA")
            try:
                commit = git(repo, "rev-parse", "--verify", "--end-of-options", tested + "^{commit}")
            except subprocess.CalledProcessError:
                raise ValueError("Evidence head is not a commit") from None
            if tested != commit or git(repo, "rev-parse", commit + "^{tree}") != tree:
                raise ValueError("Evidence commit differs from the reviewed tree")
        artifact = path.parent / record["artifact"]
        data = artifact.read_bytes()
        validated.append((record, data))
    return validated


def package(repo, base, head, output=None, evidence=None):
    repo = Path(git(repo, "rev-parse", "--show-toplevel"))
    base = git(repo, "rev-parse", "--verify", "--end-of-options", base + "^{commit}")
    head = git(repo, "rev-parse", "--verify", "--end-of-options", head + "^{commit}")
    if git(repo, "status", "--porcelain", "--untracked-files=no"):
        raise ValueError("Commit or isolate tracked edits first; this package covers commits only.")
    tree = git(repo, "rev-parse", head + "^{tree}")
    records = read_evidence(evidence, repo, tree)
    destination = Path(output).resolve() if output else Path(tempfile.mkdtemp(prefix="agent-review-"))
    if destination == repo or repo in destination.parents:
        raise ValueError("Keep review packages outside the reviewed worktree.")
    if output:
        destination.mkdir(parents=True, exist_ok=False)
    diff = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--no-color", "--binary", "--full-index", base, head, "--", raw=True)
    stat = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--stat", base, head, "--")
    (destination / "diff.patch").write_text(diff)
    (destination / "stat.txt").write_text(stat + "\n")
    validation = []
    for index, (record, data) in enumerate(records):
        name = f"evidence-{index}.log"
        (destination / name).write_bytes(data)
        validation.append({**record, "artifact": name, "artifact_sha256": hashlib.sha256(data).hexdigest()})
    (destination / "review.json").write_text(json.dumps({
        "base_sha": base,
        "head_sha": head,
        "head_tree": tree,
        "diff": "diff.patch",
        "scope": "exact base-to-head committed tree difference; untracked files excluded",
        "validation": validation,
    }, indent=2) + "\n")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--base", required=True, help="Use the PR merge base for initial review; prior reviewed head for a fix round.")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--output", help="New directory outside the reviewed worktree; defaults to a temporary directory.")
    parser.add_argument("--evidence", help="JSON records for this exact tree; copies observed output into the package.")
    args = parser.parse_args()
    try:
        print(package(args.repo, args.base, args.head, args.output, args.evidence))
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"review-package: {error}\n")


if __name__ == "__main__":
    main()
