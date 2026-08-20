# Steve-s-Agents

Personal agent guidance shared across development machines.

## Contents

- `shared/global-guidance/`: global engineering defaults for Codex and Claude.
- `shared/global-guidance/WRITING.md`: prose substitutions, read on demand for anything longer than a short report.
- `shared/`: reusable workflow skills.
- `dotnet/`: .NET and ASP.NET Core domain skills.
- `configs/macos/`: reference copies of the local macOS configuration, including BOS project guidance.
- `configs/macos/bos/dotnetrc.zsh`: branch- and worktree-aware BOS SDK selection.
- `configs/wsl/`: reference copies adapted for Ubuntu on WSL, including BOS project guidance.
- `scripts/install-agent-links.sh`: creates or repairs this machine's guidance and skill symlinks.
- `scripts/link-worktree-guidance.sh`: links ignored project guidance into new Git worktrees.

## Canonical Installation

The same shape applies on every machine; only the clone path, the reference
configuration directory, and the Codex skills directory differ.

- `~/.codex/AGENTS.md` and `~/.claude/CLAUDE.md` are symlinks to `shared/global-guidance/ENGINEERING.md`.
- `~/.codex/WRITING.md` and `~/.claude/WRITING.md` are symlinks to `shared/global-guidance/WRITING.md`, placed beside each entry point so that entry point's relative reference resolves whichever way the agent resolves it.
- Every directory holding a `SKILL.md` under `shared/` and `dotnet/` is symlinked into each installed CLI's skills directory.
- BOS repository `AGENTS.md` and `CLAUDE.md` files mirror this machine's `configs/<machine>/bos/` copies and stay untracked through `.git/info/exclude`.
- Selected settings from `configs/<machine>/codex/config.toml.example` are merged into the existing `~/.codex/config.toml`, which is never replaced wholesale.

Run `scripts/install-agent-links.sh` from the clone to create or repair every
symlink above. It is idempotent, links only into CLIs that are installed,
discovers skills by scanning for `SKILL.md`, and moves anything already
occupying a target path into `~/.agent-links-backup/<timestamp>/` rather than
deleting it. Use `--dry-run` first to see what it would do.

### Per-machine paths

| | macOS | Ubuntu on WSL |
| --- | --- | --- |
| Clone | `~/agent-skills` | `~/src/stive/Steve-s-Agents` |
| Reference configs | `configs/macos/` | `configs/wsl/` |
| Codex skills | `~/.agents/skills/` | `~/.codex/skills/` |
| BOS workspace | `/Users/stive/Documents/Code/BOS` | `/home/stive/src/BOS` |

The Codex skills directory follows the installed Codex version rather than the
operating system: Codex 0.147.0 scans `~/.codex/skills/`. The installer links
into whichever variants exist, so both are safe to leave in place.

T3 Code has no skills directory of its own. It launches the Claude Code and
Codex CLIs, so linking the directories above is what makes skills reachable
from T3.

macOS additionally mirrors `configs/macos/bos/dotnetrc.zsh` to
`/Users/stive/Documents/Code/BOS/.dotnetrc.zsh`, sourced from `~/.zshrc`. WSL
has no equivalent: it resolves the SDK through each repository's `global.json`
against `~/.dotnet`.

Machine-generated trust state, plugin caches, marketplace metadata, runtime hooks, accumulated tool permissions, and credentials are intentionally not canonicalized here.

### Verifying an installation

```sh
scripts/install-agent-links.sh --dry-run   # expect kept=N backed-up=0
readlink ~/.claude/CLAUDE.md               # expect .../shared/global-guidance/ENGINEERING.md
ls -l ~/.claude/skills ~/.codex/skills     # expect symlinks into the clone
```

Skills are read at CLI start-up, so restart Claude Code or Codex after linking.
A skill whose `agents/openai.yaml` sets `allow_implicit_invocation: false`
(currently `engineering-judgment`) will not appear in Codex's skill list; it is
still reachable when named explicitly.

## Worktree Guidance

Install a local `post-checkout` hook in each clone that should inherit its main checkout's ignored `AGENTS.md` and `CLAUDE.md`, pointing at this machine's clone path:

```sh
#!/bin/sh
"$HOME/src/stive/Steve-s-Agents/scripts/link-worktree-guidance.sh" || true
```

`configs/wsl/bos/post-checkout` holds the WSL variant verbatim; adjust the clone path on other machines.

Git stores this hook in the clone's common Git directory, so it applies to worktrees created by Git, T3 Code, or another orchestrator. The helper only acts in linked worktrees and never replaces an existing file or link.

## Adapting To Another Machine

Clone this repository in the target environment and ask the local agent to inspect the closest configuration under `configs/`, plus `shared/` and `dotnet/`. Treat machine-specific files as reference material: adapt paths, shell commands, SDK setup, repository locations, and local excludes before installing them elsewhere.

Do not replace an existing `~/.codex/config.toml` wholesale. Merge only the safe settings needed by the target environment, and never commit credentials, tokens, secrets, trust state, or machine-generated configuration.
