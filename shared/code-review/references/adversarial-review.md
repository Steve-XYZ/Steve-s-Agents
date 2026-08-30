# Adversarial Review

Use only the lanes implicated by the change. Stop when the named risks are resolved; do not turn the lanes into checklist output.

## Establish coverage

Partition the diff into behavioral clusters with their own invariant owner, state machine, or durable or external side-effect boundary. Name any cluster that was not covered deeply enough for the verdict. Recommend separate changes when independent clusters can be delivered and proved independently.

## Trace shared facts

For each changed shared flag, status, enum, predicate, contract field, or serialized fact, trace:

- every writer and reader or action surface;
- initial, null/default, legacy, migration, and backfill states;
- guards, queues, commands, user interfaces, reports, and external consumers; and
- every test project and fixture that creates the state.

Compare the actual predicates. Similar names do not establish equivalent eligibility or transition rules.

## Replay effects and failures

List durable and external effects in execution order. Separate the primary effect from ancillary effects such as bonuses, notifications, audit enrichment, provider callbacks, or projections.

For each reachable failure, classify it as transient, permanent, idempotent conflict, or unknown. Record retryability separately. Determine whether the primary effect commits, rolls back, retries, or remains visibly partial. Check duplicate delivery, concurrency, reordering, and replay when the platform can produce them.

## Make findings concrete

For each material finding, state a real trigger, the resulting state, the branch taken, and the wrong observable outcome. Verify that a supported caller, stored state, or configuration can reach it. A hypothetical branch without a reachable path is not a defect.

Tests are material evidence only when they execute the challenged branch and would fail under the wrong behavior. Inspect other test projects and fixtures for stale state assumptions. Exercise migrations against the real database provider when provider behavior is part of the risk.
