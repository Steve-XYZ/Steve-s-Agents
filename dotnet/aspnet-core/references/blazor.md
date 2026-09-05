# Blazor

## Render mode

A Blazor Web App can mix static SSR, interactive server, and interactive
WebAssembly per component. Choosing wrongly is not a compile error.

- Static SSR when the page is mostly read-only and first paint matters.
- Interactive server for rich interactivity without shipping the .NET runtime.
- Interactive WebAssembly when browser-local compute or client-side latency is
  the actual requirement. It does not make the app work offline — the host page
  still comes from the server.
- Standalone WebAssembly when the app must run from static files with no
  server-rendered host. Offline operation still needs a PWA service worker
  to cache the runtime and assets plus
  a decision about how data syncs when the connection returns.

Mix modes only when the split is clear, and name the reason. Be deliberate
about prerendering, streaming rendering, and enhanced navigation: each changes
when component code runs, and code that assumed a single pass breaks quietly.

## DbContext in components

A component using interactive server rendering shares a circuit scope that
outlives a request. Prefer
`IDbContextFactory<TContext>` and create a short-lived context per operation
rather than sharing a scoped `DbContext` across components, which risks concurrent
use and stale tracked entities. Background services also need deliberate context
lifetimes, using a factory or an explicit service scope per unit of work.

Static SSR runs in an HTTP request scope; the circuit-lifetime concern does not
apply. Preserve an established request-scoped context unless the operation needs
a different lifetime. Browser components use a server API for server-owned data.

See Microsoft's [Blazor EF Core guidance](https://learn.microsoft.com/aspnet/core/blazor/blazor-ef-core?view=aspnetcore-10.0), which applies to interactive server rendering.

Keep data access and business rules in injected services, pass data through
parameters rather than hidden global state, and keep long-running work off the
UI event path.

## Trust boundary

Client-side code and browser state are not trusted, and authorization-aware UI
is a convenience layer only. Enforce every rule on the server as well. Keep
secrets and privileged operations server-side. Treat JS interop as an edge
mechanism for browser APIs, not as the application model.
