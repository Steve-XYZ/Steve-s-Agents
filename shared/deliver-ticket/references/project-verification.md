# Make repeated verification runnable

Use this only when a repeated launch, fixture, or interaction problem makes
verification expensive, and the task authorizes improving the project's tooling.
Prefer the existing harness. Otherwise add the smallest project-local helper and
procedure that another session can execute without rediscovery.

Read the repository to establish:

- Launch: the exact command, prerequisites, and readiness signal.
- Check: build identity, owned process/port, auth, tenant, and fixture state.
- Drive: one real user/API/CLI path with stable selectors or inputs.
- Observe: the action, visible result, and relevant durable or external effects.
- Clean up: only resources this run created; preserve evidence outside disposable state.

Use isolated test data. Do not infer permission to call shared or paid services.
Test the procedure end to end once before calling it usable, including cleanup
after a failed attempt. If the environment is unavailable, report the missing
prerequisite; do not publish an unexecuted recipe as verified.

Keep this knowledge in the project that owns it, and update it when its paths or
behavior change. Store exact version or commit references for external source
material; reuse an existing local reference checkout before downloading it again.
Refresh deliberately when currency matters. A cached reference is not evidence
that the installed version behaves identically.
