# Steve-s-Agents

Personal agent guidance shared across development machines. Codex and Claude Code
read the same files through symlinks; nothing here is harness-specific.

## Contents

- `shared/global-guidance/ENGINEERING.md`: global defaults, symlinked to `~/.codex/AGENTS.md` and `~/.claude/CLAUDE.md`.
- `shared/`: workflow skills — `deliver-ticket`, `code-review`, `triage-review`, `diagnosing-bugs`, `shape-feature`, `unslop`.
- `dotnet/aspnet-core/`: .NET web domain skill.
- `configs/macos/`, `configs/wsl/`: reference copies of each machine's local configuration, including the untracked BOS project guidance.
- `scripts/install-agent-links.sh`: creates or repairs this machine's skill and guidance symlinks.
- `scripts/link-worktree-guidance.sh`: links ignored project guidance into new Git worktrees.

## Delivery loop

One harness runs investigation and implementation for a ticket. Do not split a
ticket across Codex and Claude Code. After external review, start
`triage-review` in a fresh session of the same harness so the review is not read
through an exhausted delivery context.

`deliver-ticket` is the entry:

1. run the orientation commands, so later steps reason from observed branch, worktree, and upstream state;
2. map concrete callers, data paths, configuration, consumers, and independent behavioral clusters before choosing a design;
3. split independently deliverable state machines or side-effect clusters, then grill shared-state provenance, invariants, failure classes, and unresolved decisions;
4. implement the smallest vertical change, with a test of the invariant when one exists;
5. prove the target behavior and any material behavior that must remain unchanged;
6. perform a cold self-review, compare the final diff with the original map, and keep the change draft while required evidence is materially `UNPROVEN`.

`diagnosing-bugs`, `code-review`, and `triage-review` are the entry points for
those jobs. `shape-feature` covers solo and greenfield work where you are both
author and implementer; it is set to `user-invocable-only` in Claude so it never
competes for selection on a specified ticket.

Writing guidance lives in the `unslop` skill. Load it once per session before
the first substantial response; it then applies to every later response.
`ENGINEERING.md` keeps only the three rules that must hold even when the skill
never loads. Nothing re-reads a guidance file per response.

## When a reference earns its place

Progressive disclosure only pays when the deeper file holds facts the model
cannot derive and would otherwise get wrong. Measure before adding one, and
measure again before keeping it.

- A reference must carry version-gated behavior, an exact command, a repository
  invariant, or a procedure with a failure mode. Well-organized restatements of
  public documentation do not qualify; the model already has them.
- Keep the chain two levels deep. A router whose targets are rarely opened costs
  a read and returns nothing.
- Prefer a command that reports state over prose describing what to look for.
- Check reads against real sessions, not intent. Grep the harness rollouts for
  the filename inside actual tool calls and exclude sessions spent editing this
  repository, or every file looks used.

## Workflow change evaluation

Before adopting a material workflow rule broadly, replay a fixed set of
historical cases through the same model and harness: a clean control, a known
escape, an oversized or multi-cluster change, and a representative pre-change
control. Score known-defect recall, invalid findings, elapsed time, and output
size. Prefer the smallest rule that improves the target cases without adding
noise to the clean control.

## Canonical installation

The same shape applies on every machine; only the clone path and the reference
configuration directory differ.

- `~/.codex/AGENTS.md` and `~/.claude/CLAUDE.md` are symlinks to `shared/global-guidance/ENGINEERING.md`.
- Every directory holding a `SKILL.md` under `shared/` and `dotnet/` is symlinked into each installed CLI's skills directory.
- `~/.claude/settings.json` keeps its existing configuration while the installer ensures `permissions.additionalDirectories` includes this clone, so Claude can resolve skill reference files through the symlinks.
- BOS repository `AGENTS.md` and `CLAUDE.md` files mirror this machine's `configs/<machine>/bos/` copies and stay untracked through `.git/info/exclude`. Each `CLAUDE.md` is a two-line `@AGENTS.md` include, so the guidance has one source.
- Machine-specific Codex examples remain reference material; merge selected settings into `~/.codex/config.toml` without replacing it wholesale.

```sh
scripts/install-agent-links.sh --dry-run   # see what it would do
scripts/install-agent-links.sh
```

The installer is idempotent, links only into CLIs that are installed, discovers
skills by scanning for `SKILL.md`, and moves anything already occupying a target
path into `~/.agent-links-backup/<timestamp>/` rather than deleting it. When
Claude is installed it uses Python 3 to merge the one required directory into
existing user settings, backing that file up first. Invalid or unexpected JSON
fails without modifying the file.

Skills are read at CLI start-up. Restart Claude Code or Codex after linking.

### Codex skills root

Codex reads personal skills from `$CODEX_HOME/skills`, normally
`~/.codex/skills`. The bundled skills live in `.system/` inside that same
directory, so its presence says nothing about where personal skills belong.

Do not predict the root from the Codex version. If a release moves it, confirm
the live value and pass it explicitly:

```sh
codex doctor                       # reports CODEX_HOME
scripts/install-agent-links.sh --codex-skills-root="$HOME/.codex/skills"
```

A skill left in an abandoned root is never read and Codex reports no error, so
verify after every Codex upgrade. The authoritative check is the skill-roots
table Codex emits into its own session rollout under `~/.codex/sessions/`.

### Per-machine paths

| | macOS | Ubuntu on WSL |
| --- | --- | --- |
| Clone | `~/agent-skills` | `~/src/stive/Steve-s-Agents` |
| Reference configs | `configs/macos/` | `configs/wsl/` |
| BOS workspace | `/Users/stive/Documents/Code/BOS` | `/home/stive/src/BOS` |

T3 Code has no skills directory of its own. It launches the Claude Code and
Codex CLIs, so linking the directories above is what makes skills reachable
from T3.

macOS additionally mirrors `configs/macos/bos/dotnetrc.zsh` to
`/Users/stive/Documents/Code/BOS/.dotnetrc.zsh`, sourced from `~/.zshrc`. WSL
resolves the SDK through each repository's `global.json` against `~/.dotnet`.

Machine-generated trust state, plugin caches, marketplace metadata, runtime
hooks, accumulated tool permissions, and credentials are intentionally not
canonicalized here.

### Verifying an installation

```sh
scripts/install-agent-links.sh --dry-run   # expect linked=0 backed-up=0 claude-settings=kept failed=0
readlink ~/.claude/CLAUDE.md ~/.codex/AGENTS.md
ls -l ~/.claude/skills ~/.codex/skills
```

## Worktree guidance

Install a local `post-checkout` hook in each clone that should inherit its main
checkout's ignored `AGENTS.md` and `CLAUDE.md`, pointing at this machine's clone
path:

```sh
#!/bin/sh
"$HOME/src/stive/Steve-s-Agents/scripts/link-worktree-guidance.sh" || true
```

`configs/wsl/bos/post-checkout` holds the WSL variant verbatim; adjust the clone
path on other machines. Git stores this hook in the clone's common Git
directory, so it applies to worktrees created by Git, T3 Code, or another
orchestrator. The helper only acts in linked worktrees and never replaces an
existing file or link.

## Adapting to another machine

Clone this repository in the target environment and ask the local agent to
inspect the closest configuration under `configs/`, plus `shared/` and
`dotnet/`. Treat machine-specific files as reference material: adapt paths,
shell commands, SDK setup, repository locations, and local excludes before
installing them elsewhere.

Do not replace an existing `~/.codex/config.toml` wholesale. Merge only the safe
settings the target environment needs, and never commit credentials, tokens,
secrets, trust state, or machine-generated configuration.
