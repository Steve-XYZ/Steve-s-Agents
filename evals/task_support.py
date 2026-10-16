"""Local fixture identity and output handling shared by the evaluation CLIs."""

import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def git(repo, *args):
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    return subprocess.check_output(
        ["git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "-C", str(repo), *args],
        env=env, text=True, stderr=subprocess.PIPE,
    ).strip()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def file_hashes(root):
    if Path(root).is_symlink():
        raise ValueError(f"Cannot snapshot a symlink: {root}")
    files = {}
    for directory, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(name for name in dirs if name not in (".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"))
        for name in [*dirs, *sorted(names)]:
            path = Path(directory) / name
            if path.is_symlink():
                raise ValueError(f"Cannot snapshot a symlink: {path}")
            if path.is_file() and name != ".git":
                files[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def state(task, repositories):
    root = Path(task) / "repo"
    return {
        "files": file_hashes(root),
        "heads": {name: git(root / name, "rev-parse", "HEAD") for name in repositories},
    }


def new_output(path):
    path = Path(path)
    if path.exists() or path.is_symlink():
        raise ValueError(f"Destination already exists: {path}")
    path = path.resolve()
    ancestor = path.parent
    while not ancestor.exists():
        ancestor = ancestor.parent
    try:
        git(ancestor, "rev-parse", "--show-toplevel")
    except subprocess.CalledProcessError:
        return path
    raise ValueError(f"Keep disposable output outside Git checkouts: {path}")


def write_json(path, value):
    path = Path(path)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, prefix=path.name, suffix=".tmp", delete=False) as temporary:
        temporary.write(json.dumps(value, indent=2) + "\n")
    os.replace(temporary.name, path)


def terminate(process):
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()
