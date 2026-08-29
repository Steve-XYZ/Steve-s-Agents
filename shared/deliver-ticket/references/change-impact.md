# Change Impact

Map the change before design, then challenge that map against the final diff. The goal is not a list of nearby components. It is evidence that the affected and preserved behavior has been traced far enough to implement safely.

## Before implementation

Start from the requested behavioral change. Find its owner and analogous path, then trace concrete locations:

- direct callers, readers, writers, and state transitions;
- creation, update, default, migration, backfill, retry, and deletion paths for affected data;
- configuration read by each process, environment, or tenant involved;
- serialized payloads, wire formats, provider templates, generated artifacts, and external contracts;
- background jobs, caches, projections, reports, exports, user interfaces, and sibling repositories that consume the same fact.

Use symbol search, text search, repository structure, tests, and configuration. Follow behavior across names when a shared setting, database column, event, JSON field, or external identifier connects it. A search that finds no relevant dependency is evidence when its query and scope are clear.

Partition the map by behavioral cluster. A cluster has its own state machine, invariant owner, or durable or external side-effect boundary and can be delivered and proved independently. When more than one independent cluster is required, stop before editing and recommend separate tickets or pull requests. Keep the work together only when splitting would violate one acceptance criterion or invariant; record the coupling evidence.

For a changed shared flag, status, enum, predicate, or serialized fact, build a compact provenance map: owner, every writer, every reader or action surface, initial and null/default states, legacy rows, migration or backfill, and every test project or fixture that creates the state. Compare the predicates used by guards, queues, commands, user interfaces, and reports; matching names do not prove matching behavior.

Only when the map identifies material function-level complexity risk and the actual pre-edit source cannot be recovered later—typically because the function already has uncommitted changes—read [local-complexity](local-complexity.md) and retain that function's pre-edit source or diagnostic outside the target repository. Otherwise defer any complexity decision to Prove.

Record only:

- **Changes:** exact file, symbol, contract, or data path and the intended behavior.
- **Must remain unchanged:** concrete callers or consumers and their expected behavior.
- **Checked clear:** plausible locations inspected and the evidence that excluded them.
- **Scope:** one coherent cluster, or the invariant that requires multiple clusters to move together.

Do not add a location merely because it is adjacent. If the change is demonstrably local, has no shared state, configuration, contract, persistence, or downstream consumer, record `impact: local; no material fan-out` and continue.

## After implementation

Read the final diff as new evidence. List the symbols, contracts, settings, and persisted behavior it actually changes. Compare them with the original map. Any new location or behavior reopens the map before publication.

Identify the one or two facts the change's safety depends on. Examples include "only the target tenant receives the new default" or "retries cannot apply the credit twice." For each fact, obtain the cheapest honest evidence:

1. a concrete source location;
2. a step-by-step failure trace showing the bad path cannot reach;
3. a test or script executing the real code;
4. the behavior observed in a running local application when lower seams cannot prove it.

Prefer executable evidence. Mark a material fact `UNPROVEN` when it cannot be tested cheaply; never promote source inspection into runtime proof.
