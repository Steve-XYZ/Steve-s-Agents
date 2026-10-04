#!/usr/bin/env python3
"""Create or remove one folder of detached worktrees for work that spans sibling repositories.

The folder sits outside the workspace root, so a session started at the workspace root
never searches a second copy of the code. Workspace and repository guidance is linked,
not copied, and stays untracked through each clone's info/exclude.
"""

import argparse
import os
from pathlib import Path
import subprocess


GUIDANCE = ("AGENTS.md", "CLAUDE.md")
WORKSPACE_FILES = GUIDANCE + ("CONTRACTS.md",)


def git(repo, *args, raw=False):
    output = subprocess.check_output(["git", "-C", str(repo), *args], text=True, stderr=subprocess.PIPE)
    return output if raw else output.strip()


def checkouts(workspace):
    return sorted(path for path in workspace.iterdir() if path.is_dir() and (path / ".git").exists())


def resolve(repo, ref):
    for candidate in (f"refs/remotes/origin/{ref}", ref):
        try:
            return git(repo, "rev-parse", "--verify", "--end-of-options", candidate + "^{commit}")
        except subprocess.CalledProcessError:
            continue
    raise ValueError(f"{repo.name}: neither origin/{ref} nor {ref} names a commit; fetch it or pass {repo.name}=<ref>")


def link_missing(source_dir, target_dir, names):
    for name in names:
        source, target = source_dir / name, target_dir / name
        if source.is_file() and not target.exists() and not target.is_symlink():
            target.symlink_to(source)


def linked(source_dir, target_dir, names):
    return [name for name in names
            if (target_dir / name).is_symlink() and Path(os.readlink(target_dir / name)) == source_dir / name]


def plan(workspace, base, selections):
    available = {path.name: path for path in checkouts(workspace)}
    chosen = {}
    for selection in selections or available:
        name, _, ref = selection.partition("=")
        if name not in available:
            raise ValueError(f"{name}: not a Git checkout directly under {workspace}")
        if not (ref or base):
            raise ValueError(f"{name}: pass --base or {name}=<ref>")
        chosen[name] = (available[name], ref or base)
    if not chosen:
        raise ValueError(f"No Git checkouts directly under {workspace}")
    return chosen


def set_folder(workspace, sets_dir, name):
    if name in ("", ".", "..") or Path(name).name != name or "\\" in name:
        raise ValueError(f"{name!r}: a set name is one folder name, without path separators")
    destination = (Path(sets_dir) / name).resolve()
    if destination == workspace or workspace in destination.parents:
        raise ValueError("Keep set workspaces outside the workspace root.")
    return destination


def create(workspace, sets_dir, name, base=None, selections=(), fetch=False):
    workspace = Path(workspace).resolve()
    destination = set_folder(workspace, sets_dir, name)
    chosen = plan(workspace, base, selections)
    if fetch:
        for repo, ref in chosen.values():
            git(repo, "fetch", "--quiet", "origin", ref)
    commits = {repo_name: resolve(repo, ref) for repo_name, (repo, ref) in chosen.items()}
    destination.mkdir(parents=True, exist_ok=False)
    added = []
    try:
        link_missing(workspace, destination, WORKSPACE_FILES)
        for repo_name, (repo, ref) in chosen.items():
            target = destination / repo_name
            git(repo, "worktree", "add", "--quiet", "--detach", str(target), commits[repo_name])
            added.append((repo, target))
            link_missing(repo, target, GUIDANCE)
    except (OSError, subprocess.CalledProcessError):
        for repo, target in added:
            git(repo, "worktree", "remove", "--force", str(target))
        for entry in destination.iterdir():
            entry.unlink()
        destination.rmdir()
        raise
    return destination, {repo_name: (chosen[repo_name][1], commits[repo_name]) for repo_name in chosen}


def remove(workspace, sets_dir, name):
    workspace = Path(workspace).resolve()
    destination = set_folder(workspace, sets_dir, name)
    if not destination.is_dir():
        raise ValueError(f"{destination} does not exist")
    worktrees = {path.name: path for path in destination.iterdir() if path.is_dir() and not path.is_symlink()}
    for repo_name, path in worktrees.items():
        common = workspace / repo_name / ".git"
        if not common.is_dir() or Path(git(path, "rev-parse", "--path-format=absolute", "--git-common-dir")) != common.resolve():
            raise ValueError(f"{path}: not a worktree of {workspace / repo_name}")
    for repo_name, path in worktrees.items():
        links = {f"?? {name}" for name in linked(workspace / repo_name, path, GUIDANCE)}
        if set(git(path, "status", "--porcelain", "--untracked-files=normal", raw=True).splitlines()) - links:
            raise ValueError(f"{path}: commit, stash, or discard its changes first")
    for repo_name, path in worktrees.items():
        for name in linked(workspace / repo_name, path, GUIDANCE):
            (path / name).unlink()
        git(workspace / repo_name, "worktree", "remove", str(path))
    for entry in destination.iterdir():
        if entry.is_symlink():
            entry.unlink()
    kept = sorted(entry.name for entry in destination.iterdir())
    if not kept:
        destination.rmdir()
    return kept


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Set folder name, such as the line and ticket range.")
    parser.add_argument("repos", nargs="*", help="Checkout names, each optionally repo=<ref>. Defaults to every checkout.")
    parser.add_argument("--workspace", type=Path, default=Path.cwd(), help="Folder holding the sibling checkouts.")
    parser.add_argument("--sets-dir", type=Path, help="Defaults to <workspace>-sets beside the workspace.")
    parser.add_argument("--base", help="Line every selected repository starts from, such as develop.")
    parser.add_argument("--fetch", action="store_true", help="Fetch each base from origin first.")
    parser.add_argument("--remove", action="store_true", help="Remove a clean set and its worktrees.")
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    sets_dir = args.sets_dir or workspace.with_name(workspace.name + "-sets")
    try:
        if args.remove:
            kept = remove(workspace, sets_dir, args.name)
            folder = Path(sets_dir).resolve() / args.name
            print(f"kept {folder} for {', '.join(kept)}" if kept else f"removed {folder}")
            return
        destination, commits = create(workspace, sets_dir, args.name, args.base, args.repos, args.fetch)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        detail = getattr(error, "stderr", "") or error
        parser.exit(1, f"set-workspace: {str(detail).strip()}\n")
    print(destination)
    for repo_name, (ref, commit) in commits.items():
        print(f"{repo_name}\t{ref}\t{commit}")


if __name__ == "__main__":
    main()
