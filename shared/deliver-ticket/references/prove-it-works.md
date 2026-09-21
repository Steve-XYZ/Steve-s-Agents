# Prove it works

Choose the observation that distinguishes required behavior from a plausible wrong implementation. Start before the production edit, then verify the integrated result.

For a feasible material regression or invariant, observe the relevant assertion fail before the fix and pass afterward. An import error, unrelated build failure, or test that cannot exercise the changed branch is not RED evidence. Characterization, captured traces, and disposable experiments are alternatives when they answer the question; state their limits instead of adding artificial coverage.

Derive expected values from requirements, a worked example, or an independent oracle. A test that repeats the implementation's calculation can repeat its mistake. Characterization records existing behavior; it does not establish correctness.

## Choose the affected boundary

Use the smallest reliable check, then broaden for a concrete remaining risk or a required gate:

- focused tests for pure behavior and preserved/negative cases;
- affected integration tests for wiring and contracts;
- a local host, request, browser interaction, or replay when lower seams cannot establish the outcome;
- build, lint, migration, or broader suites when relevant to the change.

Use real database semantics for transaction, query, locking, or migration claims. For money, retries, concurrency, or partial failure, select reachable failure schedules: competing requests, duplicate delivery, provider success followed by a lost response, or interruption between durable and external effects. A controlled provider substitute can exercise failure schedules; it cannot certify an undocumented provider contract.

For tenant configuration, prove the intended target and a non-target/default path. For APIs, observe the response or serialized artifact. Inspect other test projects and fixtures that seed changed shared state; a green unit project does not validate those assumptions.

## Make runtime evidence trustworthy

Verify the running build, configuration, and test identity. Startup alone does not prove an interaction succeeds. Observe the requested operation through completion. Wait for a specific state rather than fixed sleeps, and do not retry a state-changing operation merely to make the check pass.

Use isolated ports, databases, queues, and containers when necessary. Do not disturb the user's running stack or use shared, production, or paid systems outside existing authorization. Record unavailable environments as gaps.

When repeated setup blocks proof, improve the smallest project-owned command or test seam that resolves it within scope. Record its owner, setup, outputs/logs, limitations, and relevant version in project instructions. Do not put project-specific recipes in global skills or build a new MCP server without a demonstrated need.

Use repository-native complexity checks when already enforced. Read [local-complexity](local-complexity.md) only for a concrete risk in changed branching, nesting, state selection, retries, or failure coordination. Routine functions do not need a separate complexity pass.

## Retain honest evidence

Tie material results to the claim, exact tested commit or working-tree state, environment, command/filter/request, observed assertion, and output pointer. Retain evidence useful to the next step or reviewer. A newer edit invalidates affected evidence; recheck that behavior, not automatically every suite.

A successful restore, build, clean diff, or unrelated green test is insufficient for a behavioral claim. An observed failure is not waived because it may predate the change. Compare the same command at exact base and head if that distinction matters; record the delta and a specific owner/follow-up for a baseline failure.

Mark missing material proof `UNPROVEN`. Distinguish inspection and static reasoning from executed behavior. Do not claim a workflow improvement from catalog validation or a single happy-path run.
