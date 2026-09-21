# AGENTS.md

## Workspace

BOS contains four adjacent codebases:

- `player-manager`: Admin, API, Core services, Worker, EF Core/MySQL, reports, and exports.
- `lotto-propagator`: draw propagation, schedules, API/Admin, workers, and EF Core/MySQL.
- `lotto-app-v2`: player-facing Next.js frontend consuming PlayerManager and Lotto APIs.
- `PlayerManager.API`: legacy or adjacent PlayerManager API code and configuration.

Linear defines BOS outcomes and stated constraints. Treat suggested causes, files, and implementation paths as leads to verify. Confirm the target repository, current branch, and expected base before editing. When working from this workspace root, read the target repository's `AGENTS.md`; its instructions govern that repository.

## Shared Setup

Before .NET commands, load the BOS SDK switcher:

```bash
source /Users/stive/Documents/Code/BOS/.dotnetrc.zsh
```

The switcher uses the nearest valid `global.json` in Player Manager and Lotto Propagator worktrees; branches without one are legacy .NET 8. In interactive zsh, branch changes are reevaluated at the next prompt. In non-interactive shells, or after a branch change inside a compound command, source the switcher again before running `dotnet`. For frontend work, inspect lockfiles and existing package scripts before choosing a package-manager command.

## Cross-repo Invariants

- Keep report filters, cached/live projections, exports, API payloads, and UI labels semantically aligned.
- Treat shared contracts, money flows, authentication, background jobs, and database migrations as high-risk changes.
- Check affected consumers when changing frontend-visible payloads or shared lotto behavior.
- Preserve timezone semantics: draw operations follow draw/schedule timezone; Admin display and reporting follow configured Admin timezone.
- Surface partial external-provider failures rather than presenting incomplete data as complete success.
- Changes to deploy-time settings must cover every service that reads them, not only a sibling.
- Changes to shared settings or defaults must prove the target behavior and preserve non-target tenants and alternate callers.
- PR descriptions should link the Linear ticket when a PR is requested.
- When explicitly asked to publish BOS review feedback, write concise English comments ordered by severity.

## Project knowledge and proof

Read the target repository's root and applicable nested instructions before editing. Keep subsystem contracts beside their owner. Root guidance should identify commands, relevant test hosts, diagnostics, generated-code ownership, and links to specialized knowledge. Do not assume every harness loads nested files automatically.

Treat this machine configuration as a reference capture. Verify commands, dependency versions, and branch assumptions against the current checkout. Record the source/version when retaining dependency guidance. Improve repeated setup in the owning repository with the smallest executable helper; do not invent missing commands or copy project recipes into global skills.
