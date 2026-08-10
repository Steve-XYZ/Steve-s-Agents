# AGENTS.md

## Workspace

The BOS workspace is `/home/stive/src/BOS` on the WSL Linux filesystem and contains three adjacent codebases:

- `player-manager`: Admin, API, Core services, Worker, EF Core/MySQL, reports, and exports.
- `lotto-propagator`: draw propagation, schedules, API/Admin, workers, and EF Core/MySQL.
- `lotto-app-v2`: player-facing Next.js frontend consuming PlayerManager and Lotto APIs.

Linear is the source of truth for BOS ticket intent. Confirm the target repository, current branch, and expected base before editing. When working from this workspace root, read the target repository's `AGENTS.md`; its instructions govern that repository.

## Ubuntu/WSL Setup

Keep builds and repositories under the Linux filesystem rather than `/mnt/c`.

For .NET repositories, use the user-local SDK selected by each repository's `global.json`:

```bash
export DOTNET_ROOT="$HOME/.dotnet"
export PATH="$DOTNET_ROOT:$PATH"
dotnet --version
```

The current BOS repositories require SDK `10.0.201`. Before a restore that needs the private GitHub package feed, run `source "$HOME/.config/bos/env"`; never print that file or its credential values.

For frontend work, load NVM in non-interactive shells when needed, then inspect lockfiles and existing package scripts before choosing a package-manager command:

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"
```

Use the WSL `docker` CLI and configured Docker context for local containers; do not use macOS Docker paths or commands.

## Cross-repo Invariants

- Keep report filters, cached/live projections, exports, API payloads, and UI labels semantically aligned.
- Treat shared contracts, money flows, authentication, background jobs, and database migrations as high-risk changes.
- Check affected consumers when changing frontend-visible payloads or shared lotto behavior.
- Preserve timezone semantics: draw operations follow draw/schedule timezone; Admin display and reporting follow configured Admin timezone.
- Surface partial external-provider failures rather than presenting incomplete data as complete success.
- PR descriptions should link the Linear ticket when a PR is requested.
- When explicitly asked to publish BOS review feedback, write concise English comments ordered by severity.
