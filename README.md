# Steve-s-Agents

Personal agent guidance shared across development machines.

## Contents

- `shared/global-guidance/`: global engineering defaults for Codex and Claude.
- `shared/`: reusable workflow skills.
- `dotnet/`: .NET and ASP.NET Core domain skills.
- `configs/macos/`: reference copies of the local macOS configuration, including BOS project guidance.
- `configs/macos/bos/dotnetrc.zsh`: branch- and worktree-aware BOS SDK selection.
- `configs/wsl/`: reference copies adapted for Ubuntu on WSL, including BOS project guidance.
- `scripts/link-worktree-guidance.sh`: links ignored project guidance into new Git worktrees.

## Canonical Installation

- `~/.codex/AGENTS.md` and `~/.claude/CLAUDE.md` link to `shared/global-guidance/ENGINEERING.md`.
- Codex skills under `~/.agents/skills/` and Claude skills under `~/.claude/skills/` link to the matching directories in this repository.
- `/Users/stive/Documents/Code/BOS/.dotnetrc.zsh` mirrors `configs/macos/bos/dotnetrc.zsh` and is sourced from `~/.zshrc`.
- BOS repository `AGENTS.md` and `CLAUDE.md` files mirror `configs/macos/bos/` and remain local through `.git/info/exclude`.

Machine-generated trust state, plugin caches, marketplace metadata, runtime hooks, accumulated tool permissions, and credentials are intentionally not canonicalized here.

## Worktree Guidance

Install a local `post-checkout` hook in each clone that should inherit its main checkout's ignored `AGENTS.md` and `CLAUDE.md`:

```sh
#!/bin/sh
"$HOME/agent-skills/scripts/link-worktree-guidance.sh" || true
```

Git stores this hook in the clone's common Git directory, so it applies to worktrees created by Git, T3 Code, or another orchestrator. The helper only acts in linked worktrees and never replaces an existing file or link.

## Adapting To Another Machine

Clone this repository in the target environment and ask the local agent to inspect the closest configuration under `configs/`, plus `shared/` and `dotnet/`. Treat machine-specific files as reference material: adapt paths, shell commands, SDK setup, repository locations, and local excludes before installing them elsewhere.

Do not replace an existing `~/.codex/config.toml` wholesale. Merge only the safe settings needed by the target environment, and never commit credentials, tokens, secrets, trust state, or machine-generated configuration.
