# AGENTS.md

## Project

Player Manager contains the Admin UI, PlayerManager API, Core domain/services, Worker jobs, EF Core/MySQL migrations, lotto integrations, and report/export flows. Preserve Admin/API/Core/Worker ownership boundaries.

Linear is the source of truth for ticket intent. For Winning Palace work, use `wp/develop` and `wp/feature/BOS-XXXX` unless the ticket or PR specifies otherwise; verify the remote base before branching.

## Build and Test

Use the WSL user-local .NET SDK selected by `global.json`:

```bash
export DOTNET_ROOT="$HOME/.dotnet"
export PATH="$DOTNET_ROOT:$PATH"
dotnet --version
```

The expected SDK is `10.0.201`. Before a restore that needs the private GitHub package feed, run `source "$HOME/.config/bos/env"`; never print that file or its credential values.

- Restore: `dotnet restore`
- Core: `dotnet build src/PlayerManager.Core/PlayerManager.Core.csproj --no-restore`
- Admin: `dotnet build admin/PlayerManager.Admin.csproj --no-restore`
- Worker: `dotnet build src/PlayerManager.Worker/PlayerManager.Worker.csproj --no-restore`
- Focused tests: `dotnet test tests/PlayerManager.Tests/PlayerManager.Tests.csproj --no-restore --filter <Filter>`
- Diff hygiene: `git diff --check`

## Architecture and Data

- Keep domain and report logic in Core services rather than controllers, endpoints, Razor components, or workers.
- Preserve public API contracts unless the ticket changes them; check `lotto-app-v2` consumers for frontend-visible payload changes.
- Sanitize external-provider failures before client-visible ProblemDetails while preserving operator trace context.
- Keep live queries, cached projections, filters, exports, and Admin labels aligned.
- Treat ticket attachments and workbooks as primary evidence for report metric semantics.
- Avoid empty-cache windows unless existing behavior explicitly requires live fallback.
- Schema changes require migration `.cs`, `.Designer.cs`, and model snapshot alignment; verify migrations are discoverable.
- Do not edit generated migrations or snapshots manually unless intentionally resolving model drift; verify with EF commands afterward.
- Use relational tests for SQL-sensitive behavior and MySQL/MariaDB when provider behavior matters.
- Draw operations follow draw/schedule timezone; Admin reporting and display follow configured Admin timezone.

## Review Rules

- Check cross-repo consumers for shared lotto flows, payloads, reports, jobs, or deploy configuration.
- When explicitly asked to publish review feedback, use concise English comments ordered by severity.
