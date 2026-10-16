#!/usr/bin/env python3
"""Grade a recorded disposable task with independent checks, never skill keywords."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

from task_oracles import CHECKS
from task_support import ROOT, digest, file_hashes, new_output, state, terminate, write_json


MANUAL = {
    "discounts": ["Find shipping incorrectly included in the percentage base.",
                  "Identify self-referential expectations and the lookup-only test.", "Reject unsupported findings."],
    "discounts-clean": ["No actionable findings against the ticket; do not invent a rounding policy."],
    "claims": ["Support only the captured duplicate response mismatch; do not allege duplicate credit.",
               "Attribute 504 cents becoming 5.40 to the client.",
               "Reject the stale-provider allegation: the old GET preceded credit success."],
    "feedback": ["Adjudicate each supplied finding against current code, not reviewer confidence."],
}
READ_ONLY = ("discounts", "discounts-clean", "claims")
UNCHECKED = "No independent check exists for this case; judge its behavior against the fixture contract."


def remove_bytecode_caches(root):
    for directory, dirs, _ in os.walk(root):
        dirs[:] = [name for name in dirs if name != ".git"]
        for name in [name for name in dirs if name == "__pycache__"]:
            path = Path(directory) / name
            if path.is_symlink():
                path.unlink()
            else:
                shutil.rmtree(path)
            dirs.remove(name)


def check(command, directory, path, allow_empty=False, timeout=30):
    result = {"command": command, "cwd": str(directory), "output": path.name}
    with path.open("xb") as output:
        process = None
        try:
            process = subprocess.Popen(command, cwd=directory, stdout=output, stderr=subprocess.STDOUT, start_new_session=True)
            process.wait(timeout=timeout)
            result.update(exit_code=process.returncode, status="passed" if process.returncode == 0 else "failed")
        except (OSError, subprocess.TimeoutExpired) as error:
            result.update(status="blocked", reason=str(error))
        finally:
            if process is not None:
                terminate(process)
    if allow_empty and "Ran 0 tests" in path.read_text(errors="replace") and result.get("exit_code") in (0, 5):
        result["status"] = "not_applicable"
    return result


def grade(record, output=None):
    record = Path(record).resolve()
    destination = new_output(output or record / "grade.json")
    receipt = json.loads((record / "receipt.json").read_text())
    task = Path(receipt["task_dir"]).resolve()
    if task == destination or task in destination.parents:
        raise ValueError("Keep grades outside the candidate task directory")
    fixture = json.loads((ROOT / "evals/task-fixtures.json").read_text())[receipt["case"]]
    unchecked = receipt["case"] not in READ_ONLY and receipt["case"] not in CHECKS
    result = {"case": receipt["case"], "checks": [],
              "manual_review": MANUAL.get(receipt["case"], []) + ([UNCHECKED] if unchecked else []),
              "execution_status": receipt["execution"]["status"],
              "environment": {"python": platform.python_version(), "platform": platform.platform()},
              "grader_sha256": digest({name: hashlib.sha256((ROOT / "evals" / name).read_bytes()).hexdigest()
                                       for name in ("grade-task.py", "task_oracles.py", "task_support.py")})}
    try:
        current = state(task, receipt["repositories"])
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        result.update(status="blocked", reason=str(error))
        write_json(destination, result)
        return result
    result["state"] = current
    artifacts_match = all((record / name).is_file() and hashlib.sha256((record / name).read_bytes()).hexdigest() == value
                          for name, value in receipt.get("artifacts", {}).items())
    treatment_matches = (digest(file_hashes(task / "guidance")) == receipt["guidance"]["snapshot_sha256"] and
                         hashlib.sha256((task / "prompt.txt").read_bytes()).hexdigest() == receipt["prompt_sha256"])
    if not artifacts_match or not treatment_matches or digest(fixture) != receipt["fixture_sha256"] or ("final_state" in receipt and current != receipt["final_state"]):
        result["status"] = "stale"
    elif receipt["execution"]["status"] not in ("prepared", "completed") or "snapshot_error" in receipt:
        result["status"] = "blocked"
    else:
        repo = Path(receipt["task_dir"]) / "repo"
        prefix = destination.stem
        if receipt["case"] in READ_ONLY:
            result["checks"].append({"claim": "Read-only task left source and heads unchanged",
                                     "status": "passed" if current == receipt["initial_state"] else "failed"})
        # The snapshot excludes bytecode caches, so no check may load one.
        remove_bytecode_caches(repo)
        if receipt["case"] not in READ_ONLY and not unchecked:
            result["checks"].append(check([sys.executable, "-I", "-B", str(ROOT / "evals/task_oracles.py"), receipt["case"], str(repo)],
                                          repo, destination.with_name(prefix + "-oracle.txt")))
        for index, name in enumerate(receipt["repositories"]):
            result["checks"].append(check([sys.executable, "-B", "-m", "unittest", "discover", "-v"],
                                          repo / name, destination.with_name(f"{prefix}-suite-{index}.txt"), allow_empty=True))
        statuses = {row["status"] for row in result["checks"]}
        result["status"] = ("failed" if "failed" in statuses else "blocked" if "blocked" in statuses else
                            "manual_required" if result["manual_review"] else "passed")
        after = state(task, receipt["repositories"])
        if after != current:
            result.update(status="stale", post_check_state=after)
    write_json(destination, result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record-dir", required=True)
    parser.add_argument("--output", help="New JSON path for a later retained grade")
    args = parser.parse_args()
    try:
        result = grade(args.record_dir, args.output)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["status"] == "passed" else 1 if result["status"] == "failed" else 2)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        parser.exit(2, f"grade-task: {error}\n")
