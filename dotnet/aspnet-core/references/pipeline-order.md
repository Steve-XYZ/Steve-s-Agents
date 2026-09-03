# Pipeline Order

Middleware order is the most common cause of behavior that compiles, starts,
and is wrong. Read this before adding, moving, or reviewing middleware.

## Order

1. Forwarded headers, when behind a proxy or load balancer
2. Exception handling, and HSTS outside development
3. HTTPS redirection
4. Static files
5. Routing, when explicit routing middleware is needed
6. CORS, when endpoints require it
7. `UseAuthentication()`
8. `UseAuthorization()`
9. Endpoint-specific middleware such as rate limiting or session
10. Endpoint mapping: `MapRazorPages`, `MapControllers`, `MapGet`, `MapHub`, `MapGrpcService`

Adjust only with a concrete reason, and say what it is.

## The rules that break production

- `UseAuthentication()` must precede `UseAuthorization()`.
- Proxy header processing must precede authentication, redirects, and link
  generation. Nothing scheme-sensitive — a redirect URI, a generated absolute
  URL, an auth callback — may be evaluated before forwarded headers are read.
  This is the failure that only appears once the app is behind the proxy.
- Do not insert custom middleware between authentication and authorization
  without a reason.
- In a Minimal API app, an explicit `UseRouting()` is usually unnecessary and
  changes ordering when added.
- Persist data-protection keys outside ephemeral local storage whenever the app
  runs on more than one instance. Otherwise cookies, antiforgery tokens, and
  protected payloads stop validating across instances and after a restart.

## Verifying a change

Middleware order has no compile-time signal. Prove an ordering change by
exercising the affected path end to end — the redirect, the callback, the
unauthorized response, the generated link — behind the same proxy topology the
environment uses. A green build proves nothing here.
