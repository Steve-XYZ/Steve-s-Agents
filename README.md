# Steve-s-Agents

Personal agent guidance shared across development machines and agents, including Codex, Claude Code, OpenCode, Antigravity, Cursor, and Grok Build. They use the same AGENTS.md and skills standards; symlinks keep a single source of guidance. The installer maintains the Codex and Claude paths used on this machine.

## Contents

- `shared/global-guidance/ENGINEERING.md`: global defaults, symlinked to `~/.codex/AGENTS.md` and `~/.claude/CLAUDE.md`.
- `shared/`: workflow skills — `deliver-ticket`, `code-review`, `triage-review`, `diagnosing-bugs`, `shape-feature`, `unslop`.
- `dotnet/aspnet-core/`: the ASP.NET Core facts a model gets wrong from memory — target-framework and breaking changes, middleware order, Blazor render modes. Not a documentation summary.
- `configs/macos/`, `configs/wsl/`: reference copies of each machine's local configuration, including the untracked BOS project guidance.
- `scripts/install-agent-links.sh`: creates or repairs this machine's skill and guidance symlinks.
- `scripts/link-worktree-guidance.sh`: links ignored project guidance into new Git worktrees.

## Delivery loop

Keep five entry points: `deliver-ticket`, `shape-feature`, `diagnosing-bugs`, `code-review`, and `triage-review`. They select a reasoning mode, not a mandatory sequence of ceremonies.

Delivery follows one observable behavior and its proof at a time. Inspect its owner and affected paths, choose evidence before the production edit, implement, verify, remove code made obsolete, and reassess the next slice. Later planned work remains provisional. Several authorized behavioral clusters call for a safe sequence, not an automatic stop.

Use shaping for unresolved decisions in existing systems as well as new projects. Keep a short durable work note only when continuity or handoff needs it. Retain one implementer across coupled slices. Separate planning contexts, workers, or worktrees only when isolation or handoff earns their cost.

Self-review checks the integrated change. Fresh independent review is required for material money, authorization, durable concurrency, irreversible migration, or hard-to-undo external-effect changes. Use one reviewer first. Triage tests findings against evidence before fixing them. A missing reviewer or material proof blocks a readiness claim, not an authorized diagnostic draft.

See [the foundation decisions](docs/workflow-foundation.md) for evidence, rejected defaults, and the boundary between this repository and project-owned tools. The WSL audit used a machine-local Claude `user-invocable-only` override; the installer preserves local routing settings.

Writing guidance lives in `unslop`, separate from the engineering defaults. Workflow skills load it when preparing a PR body, findings, or final report; requested prose writing and rewriting can also invoke it directly. Reuse it while it remains in context. Routine progress updates do not trigger a new load, and no startup hook or per-response reread is needed.

## When a reference earns its place

Progressive disclosure only pays when the deeper file holds facts the model cannot derive and would otherwise get wrong. Measure before adding one, and measure again before keeping it.

- A reference must carry version-gated behavior, an exact command, a repository
  invariant, or a procedure with a failure mode. Well-organized restatements of
  public documentation do not qualify; the model already has them.
- Keep the chain two levels deep. A router whose targets are rarely opened costs
  a read and returns nothing.
- Prefer a command that reports state over prose describing what to look for.
- Check reads against real sessions, not intent. Grep the harness rollouts for
  the filename inside actual tool calls and exclude sessions spent editing this
  repository, or every file looks used.

- Count opens against the sessions that met the reference's own trigger, not
  against every transcript. A conditional reference looks unused when the
  denominator includes the sessions it was never meant to open in.

## Workflow change evaluation

Before adopting a material workflow rule broadly, replay a fixed set of historical cases through the same model and harness: a clean control, a known escape, an oversized or multi-cluster change, and a representative pre-change control. Score required behavior, invariant preservation, invalid findings, escaped defects, human intervention/rework, elapsed time, and model/tool cost. Skill loads and checklist completion are diagnostic signals, not success metrics. Keep outcome expectations independent of the implementation and use holdout cases. Prefer the smallest rule that improves the target cases without adding noise to the clean control.

Run repository checks before spending model tokens:

```sh
python3 scripts/validate-skills.py
python3 scripts/test-install-agent-links.py
python3 scripts/test-workflow-helpers.py
```

The [evaluation cases](evals/README.md) distinguish structural checks from live routing and behavior. Passing the local validator does not prove skill selection.

For repeated reviews, `scripts/review-package.py --repo <project> --base <sha>` captures an exact committed diff in a new temporary directory without changing the project. The [review procedure](shared/code-review/references/review-evidence.md) defines evidence reuse, optional output import with `--evidence`, fix-round scope, and approval requirements. `scripts/pr-state.py` reads a head-bound PR/check snapshot without waiting, posting, or deciding merge readiness.

### Maintain the foundation

The [foundation decisions](docs/workflow-foundation.md) link the mechanisms to inspected practitioner sources. Keep versioned project facts beside their owner; use tests, types, and deterministic tools for enforceable rules. Do not accumulate global prose after every correction.

For a recurring or expensive failure, record the failure, smallest proposed prevention, evidence from a relevant task and a clean control, cost, and retain/revert decision. Prefer code or tests, then local knowledge, then a helper, and only then a workflow rule when judgment is the missing part. One-off corrections may need no durable change. Retire superseded rules.

## Canonical installation

The same shape applies on every machine; only the clone path and the reference configuration directory differ.

- `${CODEX_HOME:-$HOME/.codex}/AGENTS.md` and `~/.claude/CLAUDE.md` are symlinks to `shared/global-guidance/ENGINEERING.md`.
- Every directory holding a `SKILL.md` under `shared/` and `dotnet/` is symlinked into each installed CLI's skills directory.
- `~/.claude/settings.json` keeps its existing configuration while the installer ensures `permissions.additionalDirectories` includes this clone, so Claude can resolve skill reference files through the symlinks.
- BOS repository `AGENTS.md` and `CLAUDE.md` files mirror this machine's `configs/<machine>/bos/` copies and stay untracked through `.git/info/exclude`. Each `CLAUDE.md` is a two-line `@AGENTS.md` include, so the guidance has one source.
- Machine-specific Codex examples remain reference material; merge selected settings into `~/.codex/config.toml` without replacing it wholesale.

```sh
scripts/install-agent-links.sh --dry-run   # see what it would do
scripts/install-agent-links.sh
```

The installer is idempotent, detects installed CLIs by their configuration directories, discovers skills by scanning for `SKILL.md`, and moves anything already occupying a target path into `~/.agent-links-backup/<timestamp>/` rather than deleting it. When Claude is installed it uses Python 3 to merge the one required directory into existing user settings, backing that file up first. Invalid or unexpected JSON fails without modifying the settings file; other links may already have been updated.

Restart the harness after linking so it refreshes skill discovery. Skill bodies load when invoked.

### Codex skills root

Current [Codex documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)
places user skills in `~/.agents/skills`, which is the installer default.
`CODEX_HOME` selects configuration and `AGENTS.md`; it does not establish the user skill root. The presence of `.system/` or an old skills directory does not prove discovery.

For a harness that still uses the `$CODEX_HOME/skills` location, pass an explicit override on installation and every dry run:

```sh
scripts/install-agent-links.sh --codex-skills-root="${CODEX_HOME:-$HOME/.codex}/skills"
```

Verify discovery in the actual harness after installation or an upgrade, using its skill listing or the skill-roots table in a fresh session rollout. The CLI and desktop app may run different builds. `codex doctor` reports the config home; that alone does not verify the skills directory.

### Per-machine paths

| | macOS | Ubuntu on WSL |
| --- | --- | --- |
| Clone | `~/agent-skills` | `~/src/stive/Steve-s-Agents` |
| Reference configs | `configs/macos/` | `configs/wsl/` |
| BOS workspace | `/Users/stive/Documents/Code/BOS` | `/home/stive/src/BOS` |

T3 Code has no skills directory of its own. It launches the harness CLIs, so linking the directories above is what makes skills reachable
from T3.

macOS additionally mirrors `configs/macos/bos/dotnetrc.zsh` to
`/Users/stive/Documents/Code/BOS/.dotnetrc.zsh`, sourced from `~/.zshrc`. WSL
resolves the SDK through each repository's `global.json` against `~/.dotnet`.

Machine-generated trust state, plugin caches, marketplace metadata, runtime
hooks, accumulated tool permissions, and credentials are intentionally not
canonicalized here.

### Verifying an installation

```sh
scripts/install-agent-links.sh --dry-run   # expect linked=0 backed-up=0 retired=0 failed=0
# claude-settings is kept when Claude is installed, otherwise skipped.
for agent_dir in "$HOME/.claude" "${CODEX_HOME:-$HOME/.codex}"; do
  [ -d "$agent_dir" ] || continue
  if [ "$agent_dir" = "$HOME/.claude" ]; then
    ls -l "$agent_dir/skills"
  else
    ls -l "$HOME/.agents/skills"
  fi
  for guidance_file in "$agent_dir/CLAUDE.md" "$agent_dir/AGENTS.md"; do
    [ -L "$guidance_file" ] && readlink "$guidance_file"
  done
done
```

Pass the same `--codex-skills-root` override to the dry run if installation used
one, and inspect that directory instead of the default skills path.

Installer regression checks use disposable homes and do not run either CLI:

```sh
python3 scripts/test-install-agent-links.py
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
