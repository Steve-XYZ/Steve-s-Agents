#!/usr/bin/env python3
"""Run one disposable explicit-invocation task and retain execution receipts."""

import argparse
from collections import Counter
import datetime
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time

from task_support import ROOT, digest, file_hashes, git, new_output, state, terminate, write_json


def load(filename):
    spec = importlib.util.spec_from_file_location(filename, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stream_metadata(path):
    turns = []
    items = Counter()
    malformed = 0
    for line in Path(path).read_text(errors="replace").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            malformed += 1
            continue
        if not isinstance(event, dict):
            malformed += 1
            continue
        if event.get("type") == "turn.completed":
            turns.append(event.get("usage"))
        if event.get("type") == "item.completed" and isinstance(event.get("item"), dict):
            kind = event["item"].get("type")
            if isinstance(kind, str):
                items[kind] += 1
    keys = ("input_tokens", "cached_input_tokens", "output_tokens")
    valid = turns and all(isinstance(turn, dict) and all(type(turn.get(key)) is int and turn[key] >= 0 for key in keys) for turn in turns)
    usage = {key: sum(turn[key] for turn in turns) for key in keys} if valid and not malformed else None
    return {"completed_turns": len(turns), "usage": usage, "completed_items_by_type": dict(items),
            "malformed_lines": malformed, "tool_calls": None, "cost_usd": None, "resolved_model": None}


def execute(record, prompt, model, effort, timeout, executable):
    started = time.monotonic()
    result = {"status": "blocked", "exit_code": None, "harness_version": None}
    process = None
    (record / "events.jsonl").touch()
    with (record / "stderr.txt").open("wb") as errors:
        try:
            with subprocess.Popen([executable, "--version"], stdout=subprocess.PIPE, stderr=errors, start_new_session=True) as probe:
                try:
                    version = probe.communicate(timeout=min(10, timeout))[0]
                finally:
                    terminate(probe)
            if probe.returncode:
                raise subprocess.CalledProcessError(probe.returncode, probe.args)
            result["harness_version"] = version.decode(errors="replace").strip()
            remaining = timeout - (time.monotonic() - started)
            if remaining <= 0:
                raise subprocess.TimeoutExpired([executable], timeout)
            command = [executable, "exec", "--ignore-user-config", "--ephemeral", "--json",
                       "--sandbox", "workspace-write", "-C", str(prompt.parent / "repo"),
                       "--model", model, "-c", 'model_reasoning_effort="' + effort + '"',
                       "--output-last-message", str(record / "response.txt"), "-"]
            if not (prompt.parent / "repo/.git").exists():
                command.insert(2, "--skip-git-repo-check")
            result["argv"] = command
            with (record / "events.jsonl").open("wb") as events:
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=events, stderr=errors, start_new_session=True)
                process.communicate(prompt.read_bytes(), timeout=remaining)
            result["exit_code"] = process.returncode
            metadata = stream_metadata(record / "events.jsonl")
            result["status"] = "completed" if process.returncode == 0 and metadata["completed_turns"] else "blocked"
        except subprocess.TimeoutExpired:
            result["status"] = "timed_out"
        except KeyboardInterrupt:
            result["status"] = "cancelled"
        except (OSError, subprocess.CalledProcessError) as error:
            result["reason"] = str(error)
        finally:
            if process is not None:
                terminate(process)
                result["exit_code"] = process.returncode
            result["elapsed_seconds"] = time.monotonic() - started
    result.update(stream_metadata(record / "events.jsonl"))
    return result


def run(case, task_dir, record_dir, model=None, effort=None, timeout=300, executable="codex",
        guidance_root=None, skill=None, control=False, prepare_only=False):
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be positive and finite")
    if not prepare_only and (not model or effort not in ("low", "medium", "high", "xhigh")):
        raise ValueError("Native runs require an explicit model and supported effort")
    task, record = new_output(task_dir), new_output(record_dir)
    if task == record or task in record.parents or record in task.parents:
        raise ValueError("Task and record directories must be separate, with neither inside the other")
    source = Path(guidance_root or ROOT).resolve()
    if record == source or source in record.parents:
        raise ValueError("Keep records outside the guidance source")
    fixtures = json.loads((ROOT / "evals/task-fixtures.json").read_text())
    fixture = fixtures[case]
    prompt = load("make-task-fixture.py").create(case, task, skill, source, control)
    prompt.write_text(prompt.read_text().rstrip() + " Work in this one context; do not delegate.\n")
    record.mkdir(parents=True)
    repositories = fixture.get("repositories", ["."])
    initial = state(task, repositories)
    try:
        commit = git(source, "rev-parse", "HEAD")
    except subprocess.CalledProcessError:
        commit = None
    receipt = {
        "version": 1, "case": case, "task_dir": str(task), "repositories": repositories,
        "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "fixture_sha256": digest(fixture), "initial_state": initial,
        "guidance": {"commit": commit, "snapshot_sha256": digest(file_hashes(task / "guidance")),
                     "mode": "no-guidance" if control else "explicit-skill", "entry": None if control else skill or fixture["skill"]},
        "prompt_sha256": hashlib.sha256(prompt.read_bytes()).hexdigest(),
        "host": {"platform": platform.platform(), "python": platform.python_version()},
        "requested": {"harness": "manual" if prepare_only else "codex", "model": model, "effort": effort,
                      "sandbox": "workspace-write", "delegation": "instructed_single_context"},
        "limits": {"wall_seconds": timeout, "tokens": None, "tool_calls": None},
        "execution": {"status": "prepared"},
    }
    write_json(record / "receipt.json", receipt)
    if not prepare_only:
        receipt["execution"] = execute(record, prompt, model, effort, timeout, executable)
        receipt["artifacts"] = {name: hashlib.sha256((record / name).read_bytes()).hexdigest()
                                for name in ("events.jsonl", "stderr.txt", "response.txt") if (record / name).is_file()}
        try:
            receipt["final_state"] = state(task, repositories)
        except (OSError, ValueError, subprocess.CalledProcessError) as error:
            receipt["snapshot_error"] = str(error)
        write_json(record / "receipt.json", receipt)
        if receipt["execution"]["status"] == "completed":
            load("grade-task.py").grade(record)
    return record / "receipt.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=sorted(json.loads((ROOT / "evals/task-fixtures.json").read_text())))
    parser.add_argument("--task-dir", required=True)
    parser.add_argument("--record-dir", required=True)
    parser.add_argument("--guidance-root")
    parser.add_argument("--skill")
    parser.add_argument("--control", action="store_true")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--effort", choices=("low", "medium", "high", "xhigh"))
    parser.add_argument("--timeout", type=float, default=300)
    parser.add_argument("--codex", default="codex", help="Codex CLI executable")
    args = parser.parse_args()
    def cancel(*_):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, cancel)
    try:
        receipt = run(args.case, args.task_dir, args.record_dir, args.model, args.effort, args.timeout,
                      args.codex, args.guidance_root, args.skill, args.control, args.prepare_only)
        print(receipt)
        status = json.loads(receipt.read_text())["execution"]["status"]
        return 0 if status in ("completed", "prepared") else 2
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(2, f"run-task: {error}\n")


if __name__ == "__main__":
    sys.exit(main())
