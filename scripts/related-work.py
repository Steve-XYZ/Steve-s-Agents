#!/usr/bin/env python3
"""Report other work that touches the paths or code a change is about to touch.

Reads unmerged local and origin branches, uncommitted changes in every worktree, and
recent commits on the base line of each sibling repository. It reports overlap only.
It does not decide whether two changes conflict, and it cannot see work that exists
only in a ticket. A squash-merged branch still looks unmerged until it is deleted.
"""

import argparse
from fnmatch import fnmatch
import json
import re
from pathlib import Path
import subprocess
import time


def git(repo, *args, raw=False):
    output = subprocess.check_output(["git", "-C", str(repo), *args], text=True, stderr=subprocess.PIPE)
    return output if raw else output.strip()


def lines(text):
    return [line for line in text.splitlines() if line]


def checkouts(workspace):
    return sorted(path for path in workspace.iterdir() if path.is_dir() and (path / ".git").exists())


def resolve(repo, ref):
    for candidate in (f"refs/remotes/origin/{ref}", ref):
        try:
            return git(repo, "rev-parse", "--verify", "--end-of-options", candidate + "^{commit}")
        except subprocess.CalledProcessError:
            continue
    raise ValueError(f"{repo.name}: neither origin/{ref} nor {ref} names a commit")


def matches(path, patterns):
    return any(fnmatch(path, pattern) or fnmatch(Path(path).name, pattern) for pattern in patterns)


def touched(repo, base, tip, patterns, regexes):
    files = set()
    if patterns:
        files |= {path for path in lines(git(repo, "diff", "--name-only", f"{base}...{tip}", "--")) if matches(path, patterns)}
    for regex in regexes:
        files |= set(lines(git(repo, "log", "--format=", "--name-only", "-G", regex, f"{base}..{tip}", "--")))
    return sorted(files)


def branches(repo, since_days):
    refs = lines(git(repo, "for-each-ref", "--format=%(refname)\t%(objectname)\t%(committerdate:unix)\t%(contents:subject)",
                     "refs/heads", "refs/remotes/origin"))
    cutoff = time.time() - since_days * 86400
    seen = {}
    for ref in refs:
        name, commit, date, subject = (ref.split("\t") + [""])[:4]
        if name.endswith("/HEAD") or int(date) < cutoff:
            continue
        short = name.removeprefix("refs/heads/").removeprefix("refs/remotes/")
        key = short.removeprefix("origin/")
        if key in seen and seen[key]["commit"] == commit:
            continue
        seen[short] = {"branch": short, "commit": commit, "subject": subject}
    return list(seen.values())


def untracked_matches(path, regex):
    try:
        return re.search(regex, path.read_text(errors="ignore")) is not None
    except OSError:
        return False


def dirty_worktrees(repo, patterns, regexes):
    found = []
    for entry in git(repo, "worktree", "list", "--porcelain").split("\n\n"):
        fields = dict(line.split(" ", 1) for line in entry.splitlines() if " " in line)
        path = fields.get("worktree")
        if not path or not Path(path).is_dir() or Path(path).resolve() == repo.resolve():
            continue
        status = lines(git(path, "status", "--porcelain", "--untracked-files=all", raw=True))
        hits = {line[3:].split(" -> ")[-1] for line in status if matches(line[3:].split(" -> ")[-1], patterns)}
        untracked = [line[3:] for line in status if line.startswith("??")]
        for regex in regexes:
            hits |= set(lines(git(path, "diff", "HEAD", "--name-only", "-G", regex, "--")))
            hits |= {name for name in untracked if untracked_matches(Path(path) / name, regex)}
        hits = sorted(hits)
        if hits:
            found.append({"worktree": path, "branch": fields.get("branch", "detached").removeprefix("refs/heads/"), "files": hits})
    return found


def scan(repo, ref, patterns, regexes, since_days, exclude):
    base = resolve(repo, ref)
    current = subprocess.run(["git", "-C", str(repo), "symbolic-ref", "--quiet", "--short", "HEAD"],
                             capture_output=True, text=True).stdout.strip()
    report = {"repo": repo.name, "base": ref, "base_commit": base, "branches": [], "worktrees": [], "recent_on_base": []}
    for branch in branches(repo, since_days):
        if branch["branch"].removeprefix("origin/") in (ref, current) or any(fnmatch(branch["branch"], pattern) for pattern in exclude):
            continue
        if git(repo, "rev-list", "--count", f"{base}..{branch['commit']}") == "0":
            continue
        files = touched(repo, base, branch["commit"], patterns, regexes)
        if files:
            report["branches"].append({**branch, "files": files})
    report["worktrees"] = dirty_worktrees(repo, patterns, regexes)
    since = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(time.time() - since_days * 86400)) + "Z"
    for line in lines(git(repo, "log", f"--since={since}", "--format=%H\t%s", base)):
        commit, subject = line.split("\t", 1)
        files = touched(repo, commit + "^", commit, patterns, regexes) if git(repo, "rev-list", "--parents", "-n1", commit).count(" ") else []
        if files:
            report["recent_on_base"].append({"commit": commit, "subject": subject, "files": files})
    return report


def render(reports):
    out = []
    for report in reports:
        out.append(f"== {report['repo']} (base {report['base']} {report['base_commit'][:12]})")
        for title, key, label in (("unmerged branches", "branches", "branch"), ("uncommitted worktrees", "worktrees", "worktree"),
                                  ("recent on base", "recent_on_base", "commit")):
            items = report[key]
            out.append(f"  {title}: {len(items) or 'none'}")
            for item in items:
                name = item[label][:12] if label == "commit" else item[label]
                detail = item.get("subject") or item.get("branch", "")
                out.append(f"    {name}  {detail}")
                out.extend(f"      {path}" for path in item["files"])
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repos", nargs="*", help="Checkout names under --workspace, each optionally repo=<ref>. Defaults to every checkout.")
    parser.add_argument("--workspace", type=Path, default=Path.cwd(), help="Folder holding the sibling checkouts or set worktrees.")
    parser.add_argument("--base", help="Line to compare against, such as develop.")
    parser.add_argument("--path", action="append", default=[], help="Glob for a changed path or file name; repeatable.")
    parser.add_argument("--grep", action="append", default=[], help="Regex for added or removed lines, as git log -G; repeatable.")
    parser.add_argument("--since-days", type=int, default=30, help="Ignore branches and base commits older than this.")
    parser.add_argument("--exclude", action="append", default=[], help="Branch glob to skip, such as '*TICKET-12*'.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.path and not args.grep:
        parser.error("pass at least one --path or --grep")
    workspace = args.workspace.resolve()
    available = {path.name: path for path in checkouts(workspace)}
    try:
        reports = []
        for selection in args.repos or available:
            name, _, ref = selection.partition("=")
            if name not in available:
                raise ValueError(f"{name}: not a Git checkout directly under {workspace}")
            if not (ref or args.base):
                raise ValueError(f"{name}: pass --base or {name}=<ref>")
            reports.append(scan(available[name], ref or args.base, args.path, args.grep, args.since_days, args.exclude))
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        detail = getattr(error, "stderr", "") or error
        parser.exit(1, f"related-work: {str(detail).strip()}\n")
    print(json.dumps(reports, indent=2) if args.json else render(reports))


if __name__ == "__main__":
    main()
