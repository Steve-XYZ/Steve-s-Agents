# Data Systems

## Use when

Use this lens when correctness spans a database, cache, queue, worker, external provider, multiple services, asynchronous execution, or schema/contract evolution. It also applies to state where retries or partial failures can violate an invariant.

## Decision questions

- Which component is authoritative for each fact, and which copies are derived or cached?
- What guarantee does the requirement need: atomic visibility, eventual convergence, ordering, uniqueness, durability, or freshness?
- What happens if execution stops after each side effect or boundary crossing?
- Can a request, command, message, webhook, or job be duplicated, delayed, reordered, or replayed?
- What stable identity makes repeated work recognizable, and where is that identity enforced durably?
- Which producers and consumers coexist during deployment, rollback, or schema evolution?
- How are partial failure, staleness, and degraded results made observable to callers and operators?
- Are performance assumptions measured?

## Preferred defaults

- State the required guarantee and implement no stronger mechanism than the invariant needs.
- Assume retried external calls and at-least-once asynchronous delivery are possible unless the actual contract proves otherwise.
- Enforce idempotency and uniqueness at the durable boundary that owns the state, not only in process memory.
- Keep one source of truth; make derived state rebuildable or reconcilable where practical.
- Place atomic updates inside one transaction when they protect one invariant. Across boundaries, define retry, compensation, reconciliation, and visible partial-failure behavior.
- Evolve schemas and messages compatibly with the real producer/consumer deployment order.
- Bound retries and timeouts, and expose stalled or poisoned work.

## Evidence required

Trace the state transitions and failure timeline, including transaction boundaries and externally visible results. Inspect uniqueness constraints, concurrency controls, message identity, retry configuration, producer/consumer versions, and reconciliation paths. Use focused concurrency tests, replay tests, migration checks, query plans, or load measurements when they are necessary to support the claim. Distinguish a reachable failure from a merely imaginable one.

## Do not overapply

Do not introduce queues, distributed transactions, event sourcing, CQRS, outboxes, or new stores by default. Eventual consistency is not an excuse for unspecified stale behavior, and strong consistency is not automatically worth its coordination cost. Do not report a theoretical partition, race, or replay as a review defect without a plausible execution path and material impact. Existing platform guarantees and repository contracts outrank generic distributed-systems advice; verify them before designing around assumptions.
