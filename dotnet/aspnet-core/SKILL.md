---
name: aspnet-core
description: Correct version-gated, pipeline-order, and Blazor render-mode decisions in ASP.NET Core work. Use when changing Program.cs or middleware order, choosing or changing a Blazor render mode, introducing a platform API that may not exist in the target framework, or upgrading across major versions. Do not use for ordinary feature work inside an established app model, where the repository's own conventions govern.
---

# ASP.NET Core

This skill holds the facts a model gets wrong from memory: what exists in which
framework version, what order the pipeline must run in, and which Blazor render
mode a component needs. Everything else about ASP.NET Core it already knows.
The repository's conventions, architecture, and dependencies outrank all of it.

## Orient

Run this first, in one batch, so later decisions rest on the repository's real
target rather than a default:

```sh
cat global.json 2>/dev/null; dotnet --version
grep -rhoE '<TargetFramework[s]?>[^<]+' --include='*.csproj' . | sort -u
grep -rlE '@rendermode|AddInteractiveServerComponents|AddInteractiveWebAssemblyComponents' --include='*.razor' --include='*.cs' . | head
```

Do not restate the output. If the target framework differs from what the task
assumes, say so before writing code.

## References

Open only the one the change touches:

- [version-facts.md](references/version-facts.md) — target framework rules, what .NET 10 added, and the breaking changes for each version hop. Read before introducing a platform API or starting an upgrade.
- [pipeline-order.md](references/pipeline-order.md) — middleware order and the ordering mistakes that compile, start, and fail in production. Read before adding, moving, or reviewing middleware.
- [blazor.md](references/blazor.md) — render-mode choice, `IDbContextFactory` in components, and the trust boundary.

For anything else — globalization, hosting details, a narrow API page — go
straight to Microsoft Learn. A summary of it here would only restate what the
model has.

## Defaults

- Prefer `WebApplicationBuilder` and `WebApplication`. Use `Startup` or
  `WebHost` patterns only where the codebase already does, or when migrating.
- Prefer built-in DI, options, logging, ProblemDetails, OpenAPI, health checks,
  rate limiting, output caching, and Identity before adding a third-party
  dependency — but do not replace an established repository dependency or
  infrastructure pattern merely because a built-in alternative exists.
- Respect the existing app model. Do not rewrite Razor Pages to MVC or
  controllers to Minimal APIs without a reason the ticket states.
- Reuse the repository's conventions for messaging, persistence, validation,
  caching, telemetry, authentication, and deployment.
- Keep domain and report logic in services rather than controllers, endpoints,
  components, or workers.
- Do not introduce template-driven folders, services, or abstractions unless
  the codebase has a clear place for them.

`LICENSE.txt` is the Apache 2.0 license of `dotnet/AspNetCore.Docs`, from which
these references were synthesized.
