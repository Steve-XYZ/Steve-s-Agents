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
  server-rendered host. This is the only route to genuine offline operation,
  and it still needs a PWA service worker to cache the runtime and assets plus
  a decision about how data syncs when the connection returns.

Mix modes only when the split is clear, and name the reason. Be deliberate
about prerendering, streaming rendering, and enhanced navigation: each changes
when component code runs, and code that assumed a single pass breaks quietly.

## DbContext in components

A server-side Blazor component's scope outlives a request. Inject
`IDbContextFactory<TContext>` and create a short-lived context per operation
rather than injecting a scoped `DbContext`, which produces concurrency
exceptions and stale tracked entities under interactive server rendering. The
same applies to background services and any other non-request-scoped execution.

This is a server-side rule, covering static SSR and interactive server. A
WebAssembly component runs in the browser and reaches data through a server
API, never a `DbContext`.

Keep data access and business rules in injected services, pass data through
parameters rather than hidden global state, and keep long-running work off the
UI event path.

## Trust boundary

Client-side code and browser state are not trusted, and authorization-aware UI
is a convenience layer only. Enforce every rule on the server as well. Keep
secrets and privileged operations server-side. Treat JS interop as an edge
mechanism for browser APIs, not as the application model.
