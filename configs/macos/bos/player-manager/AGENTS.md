# AGENTS.md

## Project

Player Manager contains the Admin UI, PlayerManager API, Core domain/services, Worker jobs, EF Core/MySQL migrations, lotto integrations, and report/export flows. Preserve Admin/API/Core/Worker ownership boundaries.

Linear is the source of truth for ticket intent. For Winning Palace work, use `wp/develop` and `wp/feature/BOS-XXXX` unless the ticket or PR specifies otherwise; verify the remote base before branching.

## Build and Test

Load the BOS SDK switcher before .NET commands. The branch's `global.json` is authoritative; branches without one use the legacy .NET 8 fallback:

```bash
source /Users/stive/Documents/Code/BOS/.dotnetrc.zsh
dotnet --version
```

After changing branches in a non-interactive or compound shell command, source the switcher again before running `dotnet`.

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
- Cashier and other money flows: the invariant lives in a Core service. Endpoints orchestrate; they do not own balances, stamps, or transitions.
- Distinguish capability (`canCancel`, eligibility, entitlement) from performing the provider or ledger side effect. They are not the same type and not the same call.
- Every setting a service reads must exist in that service's deploy configuration (`deploy/compose.tenant.yml` or equivalent). Admin, API, and Worker are separate.
- A catalogue, seed, or allow-list guard is only a guard if a test goes red on the case it claims to catch.
- Do not leave unused confirmation, cancellation, actor, or stamp fields on a new money path.

## Review Rules

- Check cross-repo consumers for shared lotto flows, payloads, reports, jobs, or deploy configuration.
- When explicitly asked to publish review feedback, use concise English comments ordered by severity.
