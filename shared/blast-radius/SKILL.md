---
name: blast-radius
description: Use before the first slice of a change that touches shared state, contracts, configuration, persistence, or downstream consumers; when work spans several repositories or tickets or a ticket's named scope may be incomplete; and when asked what a change or diff could break.
---

# Blast radius

Find what a change affects beyond its diff and the one or two facts its safety depends on. A list of callers is not the result; a search produces that in seconds. The result is the breakage a symbol search misses, with evidence for the facts that matter.

## Map what the change touches

Start from the requested behavior. Find its owner and an analogous path, then trace concrete locations:

- direct callers, readers, writers, and state transitions;
- creation, update, default, migration, backfill, retry, and deletion paths for affected data;
- configuration read by each process, environment, or tenant involved;
- serialized payloads, wire formats, provider templates, generated artifacts, and external contracts;
- background jobs, caches, projections, reports, exports, user interfaces, and sibling repositories that consume the same fact.

Follow behavior across names when a setting, database column, event, JSON field, or external identifier connects it. A search that finds nothing is evidence when its query and scope are stated.

For a changed shared flag, status, enum, predicate, or serialized fact, build a provenance map: owner, every writer, every reader or action surface, initial and null/default states, legacy rows, migration or backfill, and every test project or fixture that creates the state. Compare the predicates used at each surface; matching names do not prove matching behavior.

When the work runs from a multi-repository workspace, names several tickets, or changes a fact another repository, process, or customer line reads, also follow [ticket scope](references/ticket-scope.md).

Partition the map by behavioral cluster. A cluster has its own state machine, invariant owner, or durable or external side-effect boundary and can be delivered and proved independently. Several required clusters call for a safe sequence of observable slices within the authorized outcome, not a stop. Record coupling and rollout constraints.

## Pressure-test what must stay true

Answer only the questions that change the design, from repository evidence:

- What must remain true, and which component owns that rule?
- Which callers read, write, transport, or independently rebuild the same fact?
- Which states and transitions exist, and which combinations must stay impossible?
- What happens to existing data, defaults, and in-flight work?
- What remains after failure, retry, duplicate delivery, concurrency, or partial success? Which effects are primary and which ancillary, and does the primary effect commit, roll back, retry, or stay visibly partial?
- Which deploy process, tenant, environment, provider, or consumer can observe the change?
- Does every proposed field, setting, branch, or abstraction have a demonstrated caller or contract?

Follow [judgment](references/judgment.md) when the cost of being wrong is material and one of these stays open: no honest validation seam reaches the behavior; failure can leave durable or external state partly updated; a shared contract, schema, migration, or ownership boundary changes; several callers coordinate one invariant; or the current representation hides states the change must distinguish. Touching legacy code, a database, or an API does not qualify by itself.

Ask the user only what evidence cannot settle. Give the question, a recommendation when evidence supports one, the evidence, and what changes if another option is chosen.

## Name the safety facts

Name the one or two facts the change is safe because of, such as "only the target tenant receives the new default" or "a retry cannot apply the credit twice". Take each as far as is cheap and say where it stopped: a cited source line, a failure path traced step by step, a test or script running the real code, or the behavior observed in the running app. Label each with a `verify-work` evidence level.

When the map names a function-level complexity risk in code that already has uncommitted changes, copy that function's pre-edit source outside the repository before editing, so the result can be compared later.

## Record

- **Changes.** Exact file, symbol, contract, or data path and the intended behavior.
- **Must remain unchanged.** Concrete callers or consumers and their expected behavior.
- **Checked clear.** Locations inspected and the evidence that excluded them.
- **Safety facts.** Each with its evidence level.
- **Scope.** The next slice, later provisional slices, and coupling or rollout constraints.

A demonstrably local change with no shared state, configuration, contract, persistence, or downstream consumer records `impact: local; no material fan-out` and stops here.

## After implementation

Read the integrated diff as new evidence. List the symbols, contracts, settings, and persisted behavior it actually changes and compare them with the map. A new location or behavior reopens the map before publication.
