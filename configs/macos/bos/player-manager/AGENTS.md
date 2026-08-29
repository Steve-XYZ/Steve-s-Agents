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

## CI and Merge

- Protect the exact `refs/heads/wp/develop` ref in the GitHub ruleset; a rule for `refs/heads/develop` does not cover it.
- Treat application tests as blocking. Do not use `continue-on-error` for them. When a failure may be preexisting, run the same command at the exact head and base and compare the reason.
- Fix recurring baseline failures or quarantine each one explicitly with an owner and follow-up. Do not use a blanket baseline exemption.
- Keep artifact retention within the repository maximum of 5 days. Make artifact upload non-blocking or separate so a quota failure does not hide the build or test result.
- Before marking a PR ready to merge, require at least one independent approval on the current head after the latest push and resolve all material threads. Author fixes or comments do not clear an earlier `CHANGES_REQUESTED` review.

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
- When adding or overriding a deploy-time setting, update every service that reads it (`deploy/compose.tenant.yml` or equivalent). Admin, API, and Worker are separate.
- Before changing a shared setting or default, inspect every reader and creation path, including direct-auth, guest, SSO, and legacy flows; prove both target and non-target tenant behavior.
- Before changing a shared flag, status, enum, or eligibility predicate, inspect every writer and action surface plus initial, null/default, legacy, migration, backfill, and test-fixture states. Keep guards, queues, commands, Admin actions, reports, and stored-data handling on one compatible predicate.
- Migration and backfill eligibility must match runtime eligibility and be tested against representative legacy rows.
- Treat provider templates, template IDs, and notification payloads as external contracts when changing tenant-specific content.
- For a bonus, notification, audit, provider, or projection effect attached to a money operation, separate the primary and ancillary effects. Classify permanent, transient, idempotent-conflict, and unknown failures and decide explicitly whether the primary operation commits, rolls back, retries, or remains visibly partial.

## Review Rules

- Check cross-repo consumers for shared lotto flows, payloads, reports, jobs, or deploy configuration.
- When explicitly asked to publish review feedback, use concise English comments ordered by severity.
