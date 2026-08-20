# Deepening Engineering Judgment

Load this file only after the compact pass and repository inspection have identified one or more specific unresolved risks with a material cost of being wrong. Do not use it to search broadly for improvements. Before continuing, state internally each material risk, its missing evidence, and the decision this deeper pass must support. Stop when those decisions are supported; concerns without a material connection to the change remain out of scope.

## Establish the change boundary

Trace one real path from caller or trigger to observable result. Identify the behavior required by the ticket, the invariants that protect it, the component that owns each invariant, and every externally visible or durable side effect. Distinguish intended behavior from behavior that merely exists today.

Compare candidate changes by what callers must know, where policy is duplicated, which invalid states they permit, how many coordinated edits future changes require, and how failures are exposed. Keep volatile knowledge with the owner that can enforce it. Introduce a new abstraction only when it removes current coordination or makes a required invariant enforceable; hypothetical reuse is insufficient.

For shared contracts, schemas, or messages, inspect actual producers and consumers, compatibility expectations, deployment order, rollback behavior, and any generated artifacts. Preserve existing contracts unless the requirement explicitly changes them.

## Create an honest feedback path

Use the narrowest existing test, public boundary, integration path, replay, fixture, or captured payload that can demonstrate the affected behavior. For a bug, observe the signal fail before the fix when practical and safe.

When weak tests or hard dependencies block reliable feedback, characterize the affected path through its real boundary. If no controllable boundary exists, introduce only the smallest seam needed to control the dependency or observe the result. Keep enabling edits behavior-preserving and separate from the intended behavior change when that materially improves reviewability. Avoid seams created only for a mocking tool, mocks that reproduce implementation details, and broad characterization unrelated to the ticket.

Characterization records current behavior; it does not prove that behavior is correct. Use the ticket and verified domain requirements to decide what must change.

## Walk the failure timeline

List durable and external side effects in execution order. Ask what remains visible if execution stops before or after each one, and what happens when the operation is retried, duplicated, delayed, reordered, or replayed. Use actual platform guarantees rather than assumed exactly-once behavior.

Keep updates in one transaction when they protect one invariant owned by one durable boundary. Across boundaries, define only the retry, idempotency, compensation, reconciliation, or partial-failure behavior needed for reachable failures. Put uniqueness and idempotency at the durable owner, not only in process memory. Make incomplete or degraded outcomes visible instead of presenting them as complete success.

Do not introduce queues, outboxes, distributed transactions, event sourcing, or new stores unless the demonstrated invariant requires them and the repository lacks an established mechanism.

## Shape and verify the implementation

Represent meaningful states and transitions explicitly enough that invalid combinations are difficult to create and failure semantics remain inspectable. Validate untrusted input at the boundary, preserve diagnostic context, keep the normal path visible, and order side effects deliberately. Prefer ordinary repository idioms over theoretically purer structures.

Verify representative normal, boundary, and failure cases. Review the final diff against the ticket, callers, contracts, invariants, and unrelated changes. State what remains unverified. Use only the techniques that resolve the named risk: do not broaden scope, add speculative generality, or turn this file into a checklist for generating code-review findings.
