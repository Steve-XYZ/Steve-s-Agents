# AGENTS.md

## Project

Lotto Propagator contains draw propagation, schedule/draw administration, Propagator API/Admin, worker flows, EF Core/MySQL data access, and tests. Preserve Admin/API/Data/Worker ownership boundaries.

Linear is the source of truth for ticket intent. The current reference branch is `feature/dotnet10-upgrade`; this repository does not use `wp/develop`. Feature branches usually use `feature/BOS-XXXX` unless the ticket or PR specifies otherwise; verify the remote base before branching.

## Build and Test

Use the WSL user-local .NET SDK selected by `global.json`:

```bash
export DOTNET_ROOT="$HOME/.dotnet"
export PATH="$DOTNET_ROOT:$PATH"
dotnet --version
```

The expected SDK is `10.0.201`.

- Restore: `dotnet restore`
- Build: `dotnet build --no-restore`
- Focused tests: `dotnet test tests/Lotto.Propagator.Tests/Lotto.Propagator.Tests.csproj --no-restore --filter <Filter>`
- Broad tests: `dotnet test --no-build`
- Diff hygiene: `git diff --check`

## Architecture and Data

- Keep domain and workflow decisions in services rather than endpoints, controllers, or Razor components.
- Keep Admin behavior, report payloads, API contracts, and exports aligned.
- Preserve draw/schedule state-machine semantics for re-grade, cancellation, disablement, and Admin attribution.
- For Admin auth/session defects, trace the live minimal API and 2FA completion path before changing helper code.
- Schema changes require migration `.cs`, `.Designer.cs`, and model snapshot alignment.
- Do not edit generated migrations or snapshots manually unless intentionally resolving model drift; verify with EF commands afterward.
- Check concurrent updates, duplicate transitions, N+1 queries, unbounded queries, and indexes when relevant.
- Every setting a service reads must exist in that service's deploy configuration; Admin, API, and Worker are separate.
- Validate provider-specific behavior against local MariaDB when it materially affects the change: use the WSL `docker` CLI with container `mariadb-mysqldb` and database `lotto_propagator`.

## Review Rules

- Check cross-repo consumers for shared lotto flows, reports, Admin behavior, jobs, or deploy configuration.
- When explicitly asked to publish review feedback, use concise English comments ordered by severity.
