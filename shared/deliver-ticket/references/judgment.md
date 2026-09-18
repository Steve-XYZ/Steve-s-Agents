# Deep Judgment Pass

Load this only when a specific risk to this change is named, still unresolved after the caller's questions, and material if wrong. The gate lives at the call site ( [grill](grill.md) in `deliver-ticket`, the brief in `shape-feature` ) so arriving here means it is already satisfied. State the risk, its missing evidence, and the decision this pass must support, then stop once those decisions are supported. Concerns without a material connection to the change stay out of scope.

Do not use this file to search for improvements, generate review findings, or produce a separate plan or artifact.

## Establish the change boundary

Trace one real path from caller or trigger to observable result. Identify the behavior the ticket requires, the invariants that protect it, the component that owns each invariant, and every durable or externally visible side effect. Distinguish intended behavior from behavior that merely exists today.

Keep volatile knowledge with the owner that can enforce it. The design comparison and the abstraction test live in `deliver-ticket`; apply them here rather than restating them.

Name which component is authoritative for each fact and which copies are derived or cached. For shared contracts, schemas, or messages, inspect the actual producers and consumers, compatibility expectations, deployment order, rollback behavior, and generated artifacts. Preserve existing contracts unless the requirement changes them.

For a shared flag, status, enum, or eligibility predicate, work from the provenance map `change-impact` already built. A new write-side rule does not repair stored rows or a reader that independently reconstructs the old rule.

## Create an honest feedback path

Use the narrowest existing test, public boundary, integration path, replay, fixture, or captured payload that can demonstrate the affected behavior. For a bug, observe the signal fail before the fix when that is practical and safe.

When weak tests or hard dependencies block reliable feedback, characterize the affected path through its real boundary. If no controllable boundary exists, add only the smallest seam needed to control the dependency or observe the result, and keep that enabling edit behavior-preserving and separate from the behavior change when it materially improves reviewability. Avoid seams that exist only for a mocking tool, mocks that reproduce implementation details, and characterization unrelated to the ticket.

Characterization records current behavior; it does not prove that behavior is correct. The ticket and verified domain requirements decide what must change.

## Walk the failure timeline

State the guarantee the requirement actually needs — atomic visibility, eventual convergence, ordering, uniqueness, durability, or freshness — and implement no stronger mechanism than that invariant requires.

List durable and external side effects in execution order. For each, ask what remains visible if execution stops before or after it, and what happens when the operation is retried, duplicated, delayed, reordered, or replayed. Use the platform's actual guarantees; assume at-least-once delivery and retried external calls unless a contract proves otherwise. Separate primary from ancillary effects and decide, per failure class, whether the primary effect commits, rolls back, retries, or remains visibly partial. Do not retry a permanent ancillary failure forever by rolling back successful primary work.

Identify the stable identity that makes repeated work recognizable, and enforce uniqueness and idempotency at the durable owner rather than in process memory. Keep updates in one transaction when they protect one invariant owned by one durable boundary; across boundaries, define only the retry, compensation, or reconciliation behavior that reachable failures require. Bound retries and timeouts, expose stalled or poisoned work, and make degraded outcomes visible instead of presenting them as complete success.

## Shape and verify

Represent meaningful states and transitions explicitly enough that invalid combinations are hard to create and failure semantics stay inspectable. Prefer ordinary repository idioms over theoretically purer structures. State what remains unverified.

## Do not overapply

Do not introduce queues, outboxes, distributed transactions, event sourcing, CQRS, or new stores unless the demonstrated invariant requires them and the repository lacks an established mechanism. Eventual consistency is not an excuse for unspecified stale behavior, and strong consistency is not automatically worth its coordination cost.

A theoretical partition, race, or replay without a plausible execution path and material impact is not a defect. Platform guarantees and repository contracts outrank generic distributed-systems advice; verify them before designing around assumptions. If this pass only confirms the existing decision, change nothing and do not enlarge the scope.
