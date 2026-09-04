# .NET Version Facts

Facts a model gets wrong from memory. Confirm on Microsoft Learn when currency
decides the answer, and never introduce an API without confirming it exists in
the repository's target framework.

## Target framework

Read the target framework from `<TargetFramework>` or `<TargetFrameworks>` in
the affected project, or in the `Directory.Build.props` it imports.
`global.json` pins the SDK and toolchain, not the target.

- An existing repository stays on its current target unless the task is
  explicitly an upgrade.
- New production work prefers the latest stable .NET. Read the SDK pin from the
  repository's own `global.json` and do not assume one version across
  repositories: pins here sit on different feature bands with different
  `rollForward` policies, and the newest SDK installed locally is not the pin.
- Do not introduce preview-only APIs or preview guidance unless the user asks
  for preview adoption or the repository already runs a preview SDK.

## Added in .NET 10 / ASP.NET Core 10

- Minimal APIs support built-in validation through `AddValidation()`. Use it
  instead of building parallel validation infrastructure.
- Identity exposes metrics for authentication traffic.

## Breaking changes worth checking before an upgrade

Moving to ASP.NET Core 10:

- known API endpoints no longer use cookie-login redirects by default; return
  API-appropriate unauthorized responses instead;
- `WithOpenApi` is deprecated;
- `WebHostBuilder`, `IWebHost`, and `WebHost` are obsolete;
- Razor runtime compilation is obsolete.

Moving to ASP.NET Core 9:

- `ValidateOnBuild` and `ValidateScopes` are enabled in development under
  `HostBuilder`, so a captive or mis-scoped dependency now fails at startup;
- middleware constructor expectations and DI validation changed.

Moving to ASP.NET Core 8:

- Minimal API `IFormFile` requires antiforgery;
- `AddRateLimiter()` and `AddHttpLogging()` are required when the matching
  middleware is used.

## Upgrade sequence

Read the "what's new" and breaking-changes pages for each version hop, compile
and resolve obsoletions deliberately, then re-run integration tests, auth
flows, and deployment-specific behavior such as proxies, cookies, and static
assets. Remove a compatibility shim only after tests confirm the behavior.
Keep one authoritative target framework per project unless multi-targeting is
deliberate.
