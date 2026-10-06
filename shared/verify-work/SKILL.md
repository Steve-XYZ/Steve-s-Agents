---
name: verify-work
description: Use before claiming that work is done, fixed, passing, safe, or ready; when asked to verify, validate, or prove a change, a fix, or claims and findings someone else produced; and when a change needs runtime proof but nobody has recorded how to run the project.
---

# Verify work

A claim is worth the evidence behind it. Run the check now, read what it printed, and state the claim at the level that output supports.

## Before any completion claim

1. Name the claim and the observation that would show it false.
2. Run that check now, against the current code and build.
3. Read the whole output and the exit code.
4. State the claim with its evidence level, or state the actual result.

An earlier run, a worker's report, a green build, or "should pass" is not a check run now.

## Evidence levels

Every material claim in a report carries one level, set by what actually ran:

| What ran | Level |
| --- | --- |
| The product's own entry point, invoked the way its user or consuming system invokes it, on the current build: the command a user types, the endpoint, the screen, the scheduled job, or a read-back of the value it stored | `observed` |
| A test runner, or a script that imports and calls the code; the check would fail if the behavior were wrong | `tested` |
| Nothing: source reading or a traced argument | `inspected` |
| No check, or the check could not run; name what is missing | `UNPROVEN` |

A test suite is `tested` even when it is started from a terminal.

A claim needs `observed` when it depends on wiring, configuration, startup, or runtime state that a lower check cannot tell apart, such as a flag reaching the code, a setting read per tenant, or a job picking up a record. Otherwise use the cheapest level that settles it. When an `observed` claim has no environment that can produce it, report the level reached and name the missing environment. [Choosing proof](references/choosing-proof.md) says when a failure must be seen first for each type of work, and covers the cheapest observation that settles a claim, runtime identity, and retained evidence. [Local complexity](references/local-complexity.md) measures a named control-flow risk in changed functions.

## Drive the real thing

For an `observed` claim, find how the project runs before improvising: a `Verify` section in its agent instructions, the README, package scripts, a Makefile, compose files, existing end-to-end tests or test hosts. When none exists or the recorded recipe fails, follow [driving the app](references/driving-the-app.md). It launches, checks readiness, drives, captures, cleans up, and records what worked so the next agent starts with a recipe.

## Claims someone else made

A worker's report, a review finding, an investigation's conclusions, and findings about to leave the team are claims to check, not evidence. For each claim:

1. State what observation would make it false.
2. Re-derive it from primary evidence: code at the exact commit, the request actually sent, the response actually received, stored rows, logs correlated by id and time, the contract text.
3. Look for an explanation on your own side before accepting it: the request, data, identifiers, environment, timing, or code you control.
4. Give a verdict: `confirmed` with its level, `wrong`, `overstated` (say which part holds), or `UNPROVEN` (say what would settle it). Name anything the claims missed.

Stay read-only unless the requester lists the allowed writes exactly. Never print or store secrets; delete temporary files that hold credentials.

To delegate verification, give a fresh context the claims verbatim, the requirement or contract they rest on, the exact state (repository, commit, environment, time range), what it may read, the allowed writes, and the report shape. Leave out the author's reasoning and the verdict you expect. Spend independent verification on the claims with the weakest evidence or the highest cost if wrong.

## Red flags

Stop and run the check when you notice any of these:

- "should", "probably", or "looks right" about behavior;
- "done", "fixed", or "all good" written before the output was read;
- a subagent, worker, or tool reported success;
- tests pass but nobody ran the entry point the user touches;
- the running instance started before the last edit;
- the check cannot fail for the bug it is meant to catch.

## Report

Give one row per material claim: the claim, its level, the command or observation, and where the output lives. A `tested` row for new or changed behavior also says when its test was seen failing, before the edit or against the base commit; a test never seen failing is not evidence for the change. A test that pins existing behavior passes before and after; label it a pin. For each claim below `observed`, say what would raise it. When this is the final report, reuse `unslop`, loading it only if absent.
