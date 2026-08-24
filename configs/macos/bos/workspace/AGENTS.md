# AGENTS.md

## Workspace

BOS contains four adjacent codebases:

- `player-manager`: Admin, API, Core services, Worker, EF Core/MySQL, reports, and exports.
- `lotto-propagator`: draw propagation, schedules, API/Admin, workers, and EF Core/MySQL.
- `lotto-app-v2`: player-facing Next.js frontend consuming PlayerManager and Lotto APIs.
- `PlayerManager.API`: legacy or adjacent PlayerManager API code and configuration.

Linear is the source of truth for BOS ticket intent. Confirm the target repository, current branch, and expected base before editing. When working from this workspace root, read the target repository's `AGENTS.md`; its instructions govern that repository.

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
- Capability flags returned to a client are not the same as performing the provider or ledger action.
- Deploy configuration for a setting belongs on the service that reads it, not only on a sibling.
- PR descriptions should link the Linear ticket when a PR is requested.
- When explicitly asked to publish BOS review feedback, write concise English comments ordered by severity.
