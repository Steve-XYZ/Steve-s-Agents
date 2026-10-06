# Choosing proof

Choose the observation that distinguishes required behavior from a plausible wrong implementation. Start before the production edit, then verify the integrated result.

## See the failure first, by type of work

Decide from what the work is, not from how important it feels:

- **Fix.** Reproduce the failure before changing code, with a test, a command, or captured evidence of the symptom. When a test in the project already calls the failing code (search the tests for its module or symbol), the reproduction is a test seen failing.
- **New or changed behavior.** Each acceptance criterion that an existing test can reach gets a test seen failing without the change.
- **Refactor.** Pin current behavior before any structure moves: a characterization test, a recorded output, or an equivalence script. The pin passes before and after. A type check or lint run is not a pin.
- **Exploration.** Nothing has to fail first. State what the experiment cannot prove.

A test is seen failing when it ran against code without the change and failed on its assertion, either before the edit or against the base commit in a separate worktree. An import error, an unrelated build failure, or a test that cannot reach the changed branch does not count. Never revert or stash work in the user's checkout to show a failure. Where no test can reach the behavior, use a characterization, trace, or disposable experiment and state its limits instead of adding artificial coverage.

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

Mark missing material proof `UNPROVEN`. Label inspection and static reasoning `inspected`, never `tested` or `observed`. Do not claim a workflow improvement from catalog validation or a single happy-path run.
