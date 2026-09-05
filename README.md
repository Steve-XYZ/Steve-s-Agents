# Steve-s-Agents

Personal agent guidance shared across development machines. Codex and Claude Code
read the same guidance through symlinks; the installer handles their different paths.

## Contents

- `shared/global-guidance/ENGINEERING.md`: global defaults, symlinked to `~/.codex/AGENTS.md` and `~/.claude/CLAUDE.md`.
- `shared/`: workflow skills — `deliver-ticket`, `code-review`, `triage-review`, `diagnosing-bugs`, `shape-feature`, `unslop`.
- `dotnet/aspnet-core/`: the ASP.NET Core facts a model gets wrong from memory — target-framework and breaking changes, middleware order, Blazor render modes. Not a documentation summary.
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
author and implementer. The WSL audit used a machine-local Claude
`user-invocable-only` override; the installer preserves local routing settings.

Writing guidance lives in `ENGINEERING.md`. Each installed harness loads it
through its global instruction file: `~/.claude/CLAUDE.md` or
`${CODEX_HOME:-$HOME/.codex}/AGENTS.md`. It was a
skill for one release and the measurement killed that: an instruction telling
the model to invoke `unslop` fired in 1 of 16 real sessions, so 15 of 16
responses were written without the rules. A symlinked file fires in all of
them. The `unslop` skill is now only a shim for rewriting prose the user
pastes. Nothing re-reads a guidance file per response.

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

Run repository checks before spending model tokens:

```sh
python3 scripts/validate-skills.py
python3 scripts/test-install-agent-links.py
python3 scripts/test-workflow-helpers.py
```

The [evaluation cases](evals/README.md) distinguish structural checks from live
routing and behavior. Passing the local validator does not prove skill selection.

For repeated reviews, `scripts/review-package.py --repo <project> --base <sha>`
captures an exact committed diff in a new temporary directory without changing
the project. The [review procedure](shared/code-review/references/review-evidence.md)
defines evidence reuse, fix-round scope, and the remaining approval requirements.

### Practices adapted for this workflow

These are focused adaptations, not installed frameworks:

- [Peter Steinberger](https://github.com/steipete/agent-scripts): managed skill links, portable helpers, and fixture validation.
- [Matt Pocock](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md): observable test seams and independent expected results.
- [Addy Osmani](https://github.com/addyosmani/agent-skills/blob/main/evals/README.md): separate structural, routing, and behavioral checks.
- [Superpowers](https://github.com/obra/superpowers/blob/main/skills/subagent-driven-development/re-review-prompt.md): scoped fix rounds and traceable evidence reuse.
- [pstack](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md): runnable project verification and structural prevention of recurring mistakes.
- [T3 Code](https://github.com/pingdotgg/t3code/blob/main/AGENTS.md): targeted checks and project-owned operational traps.
- [Armin Ronacher](https://github.com/mitsuhiko/agent-stuff/blob/main/skills/librarian/SKILL.md): reuse local reference checkouts and record their revisions. No cache manager is installed here.

For personal learning after a difficult ticket, explain the invariant owner,
partial-failure outcome, and falsifying test before asking the agent for feedback.
Keep a lesson only if it changes a future decision. This is optional reflection,
not a new delivery gate or automatic teaching pass.

## Canonical installation

The same shape applies on every machine; only the clone path and the reference
configuration directory differ.

- `${CODEX_HOME:-$HOME/.codex}/AGENTS.md` and `~/.claude/CLAUDE.md` are symlinks to `shared/global-guidance/ENGINEERING.md`.
- Every directory holding a `SKILL.md` under `shared/` and `dotnet/` is symlinked into each installed CLI's skills directory.
- `~/.claude/settings.json` keeps its existing configuration while the installer ensures `permissions.additionalDirectories` includes this clone, so Claude can resolve skill reference files through the symlinks.
- BOS repository `AGENTS.md` and `CLAUDE.md` files mirror this machine's `configs/<machine>/bos/` copies and stay untracked through `.git/info/exclude`. Each `CLAUDE.md` is a two-line `@AGENTS.md` include, so the guidance has one source.
- Machine-specific Codex examples remain reference material; merge selected settings into `~/.codex/config.toml` without replacing it wholesale.

```sh
scripts/install-agent-links.sh --dry-run   # see what it would do
scripts/install-agent-links.sh
```

The installer is idempotent, detects installed CLIs by their configuration
directories, discovers skills by scanning for `SKILL.md`, and moves anything already occupying a target
path into `~/.agent-links-backup/<timestamp>/` rather than deleting it. When
Claude is installed it uses Python 3 to merge the one required directory into
existing user settings, backing that file up first. Invalid or unexpected JSON
fails without modifying the settings file; other links may already have been updated.

Upgrades back up the obsolete `engineering-judgment` links in the selected skill
roots and the old `~/.agent-guidance` link only when their literal targets match
this clone. Unrelated links and real files at those retired names stay in place.
Links in an abandoned skill root or pointing at another clone require inspection;
the installer does not guess their ownership. Existing settings entries are preserved.

Skills are read at CLI start-up. Restart Claude Code or Codex after linking.

### Codex skills root

Current [Codex documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)
places user skills in `~/.agents/skills`, which is the installer default.
`CODEX_HOME` selects configuration and `AGENTS.md`; it does not establish the
user skill root. The presence of `.system/` or an old skills directory does not
prove discovery.

The WSL 0.149.1 audit observed `$CODEX_HOME/skills`. For a harness that still uses
that location, pass an explicit override on installation and every dry run:

```sh
scripts/install-agent-links.sh --codex-skills-root="${CODEX_HOME:-$HOME/.codex}/skills"
```

Verify discovery in the actual harness after installation or an upgrade, using
its skill listing or the skill-roots table in a fresh session rollout. The
CLI and desktop app may run different builds. `codex doctor` reports the config
home; that alone does not verify the skills directory.

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
