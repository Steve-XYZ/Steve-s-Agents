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

## Delivery loop

For a defined ticket, one harness runs the ticket end to end. Codex is the
default; Claude Code is the same loop when that session is the one in use.
Do not split a ticket across both.

`deliver-ticket` is the entry:

1. map concrete callers, data paths, configuration, and consumers before choosing a design;
2. grill the mapped behavior, invariants, failure cases, and unresolved decisions;
3. implement the smallest vertical change, with a test of the invariant when one exists;
4. prove the target behavior and any material behavior that must remain unchanged;
5. perform a cold self-review, compare the final diff with the original map, and mark missing evidence `UNPROVEN`;
6. apply the shared writing guidance to substantial user-facing prose.

`diagnosing-bugs`, `shape-feature`, `code-review`, and `triage-review` stay
the entry points for those jobs. The map, grill, and proof procedures are
supporting references inside `deliver-ticket`, so they do not compete for
automatic skill selection. `engineering-judgment` is loaded by the grill.

After linking new skills, restart the CLI so it rereads `SKILL.md`.

## Canonical Installation

The same shape applies on every machine; only the clone path, the reference
configuration directory, and the Codex skills directory differ.

- `~/.codex/AGENTS.md` and `~/.claude/CLAUDE.md` are symlinks to `shared/global-guidance/ENGINEERING.md`.
- `~/.agent-guidance` is a symlink to `shared/global-guidance/`, providing a neutral readable path for guidance loaded on demand by either harness.
- `~/.claude/settings.json` preserves its existing configuration while the installer ensures `permissions.additionalDirectories` includes both the neutral guidance path and its resolved source directory.
- Every directory holding a `SKILL.md` under `shared/` and `dotnet/` is symlinked into each installed CLI's skills directory.
- BOS repository `AGENTS.md` and `CLAUDE.md` files mirror this machine's `configs/<machine>/bos/` copies and stay untracked through `.git/info/exclude`.
- Machine-specific Codex examples remain reference material; merge selected settings into `~/.codex/config.toml` without replacing it wholesale.

Run the installer from the clone with this machine's observed personal-skills
root:

```sh
# macOS with Codex 0.148.0
scripts/install-agent-links.sh --codex-skills-root="$HOME/.agents/skills"

# Ubuntu on WSL with Codex 0.147.0
scripts/install-agent-links.sh --codex-skills-root="$HOME/.codex/skills"
```

The installer is idempotent, links only into CLIs that are installed,
discovers skills by scanning for `SKILL.md`, and moves anything already
occupying a target path into `~/.agent-links-backup/<timestamp>/` rather than
deleting it. When Claude is installed, it uses Python 3 to merge the two
required directories into the existing user settings and backs that file up
before changing it. Invalid or unexpected JSON fails without modifying the
file. Use `--dry-run` first to see what it would do.

### Per-machine paths

These are the roots each machine was observed to use, not a rule derived from
its operating system.

| | macOS | Ubuntu on WSL |
| --- | --- | --- |
| Clone | `~/agent-skills` | `~/src/stive/Steve-s-Agents` |
| Reference configs | `configs/macos/` | `configs/wsl/` |
| BOS workspace | `/Users/stive/Documents/Code/BOS` | `/home/stive/src/BOS` |
| Codex version observed | 0.148.0 | 0.147.0 |
| Codex personal skills | `~/.agents/skills/` | `~/.codex/skills/` |

The Codex personal-skills root is a property of the installed Codex version,
not of the operating system. 0.147 reads `~/.codex/skills/`; 0.148 reads
`~/.agents/skills/` and keeps only bundled skills under
`~/.codex/skills/.system/`. The presence of `~/.codex/skills/` therefore does
not make it a personal root.

The installer treats the two as mutually exclusive and prefers
`~/.agents/skills/` when that directory exists, so personal skills are never
installed into both. This fallback cannot detect a newly changed root before
that directory exists, which is why the canonical commands pass it explicitly.
After upgrading Codex, verify its active personal-skills root and re-run the
installer with that value: skills left in the old root go unread with no error
to signal it.

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
# Use ~/.codex/skills instead on the observed WSL installation. Expect
# linked=0, backed-up=0, claude-settings=kept, and failed=0.
scripts/install-agent-links.sh --dry-run --codex-skills-root="$HOME/.agents/skills"
readlink ~/.claude/CLAUDE.md
readlink ~/.agent-guidance
ls -l ~/.claude/skills ~/.agents/skills
```

Skills are read at CLI start-up, so restart Claude Code or Codex after linking.
A skill whose `agents/openai.yaml` sets `allow_implicit_invocation: false`
(currently `engineering-judgment` and `unslop`) will not appear in Codex's
skill list. Claude also keeps `unslop` manual through
`disable-model-invocation: true` in its frontmatter.

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
