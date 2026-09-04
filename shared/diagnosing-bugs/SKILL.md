---
name: diagnosing-bugs
description: Diagnose bugs, regressions, flaky failures, and performance problems using reproducible or captured evidence. Use when the cause is unknown or the user asks to diagnose, debug, investigate, or fix something broken, failing, throwing, flaky, or slow. Continue to implementation only when a fix is requested. Do not use for a ticket with an established cause or for pure code review.
---

# Diagnosing Bugs

Establish evidence before changing behavior. Prefer reproduction, but accept captured evidence or conclusive static proof when local reproduction is impractical.

## 0. Orient

Run one batch before framing the symptom, so the first hypothesis rests on observed state:

```sh
git rev-parse --abbrev-ref HEAD; git status --short; git log --oneline -10
git stash list
```

A dirty tree and a forgotten stash are ordinary causes of "it worked yesterday". When the symptom is a regression, get the last known good ref from the user or the tracker and run `git log --oneline <good>..HEAD` before reading code; that bounds the search instead of opening it.

## 1. Frame the symptom

Establish expected behavior, actual behavior, environment, frequency, and the narrowest affected path. Read only the repository guidance and implementation needed to understand that path.

Separate observed facts from assumptions. Do not convert a nearby error or suspicious code into the reported bug without evidence connecting them.

## 2. Build an evidence loop

Prefer the cheapest reliable signal that can go red on the reported symptom:

1. focused failing test,
2. local command, request, or script,
3. replayed request, event, fixture, or captured payload,
4. differential run between known-good and failing states,
5. small disposable harness when no existing seam reaches the behavior.

When local reproduction is unavailable or disproportionately costly, use verifiable logs, traces, metrics, request/response captures, database evidence, dumps, or staging observations tied to the exact symptom. State the limitation.

Do not run stress, fuzz, repeated-trigger, load, or destructive diagnostics against shared environments, production-like data, queues, or third-party services without explicit approval.

If evidence remains insufficient, continue only with clearly labeled hypotheses and the next evidence needed. Do not implement a speculative fix.

## 3. Isolate the cause

Minimize the failing path by removing inputs, callers, configuration, and dependencies while preserving the symptom.

Form falsifiable hypotheses. Rank multiple hypotheses only when the evidence is ambiguous. Test one prediction or variable at a time with focused instrumentation, tests, a debugger, profiling, query plans, or bisection as appropriate.

For a regression with a known good ref, bisect instead of reading forward from the diff. Write a predicate that exits non-zero only on the reported symptom, then let git find the commit:

```sh
git bisect start HEAD <last-good-ref>
git bisect run <predicate>
git bisect reset
```

To locate when one behavior changed, `git log -S'<symbol>' --oneline` reports the commits that added or removed it, and `git log -L :<function>:<file>` reports that function's history alone.

Measure performance problems before optimizing. Tag temporary instrumentation so it can be found and removed.

## 4. Respect the requested outcome

For a diagnosis-only request, stop after reporting the demonstrated cause, evidence, confidence, and remaining uncertainty. Do not modify code.

When the user requested a fix, implement the smallest change supported by the evidence. Preserve existing contracts, retry and transaction behavior, idempotency, and ownership boundaries unless the confirmed cause requires changing them.

## 5. Prove the result

When a reliable seam exists:

1. convert the minimized symptom into regression coverage and observe it fail when practical,
2. apply the fix and observe it pass,
3. rerun the original evidence loop.

If no honest regression seam exists, explain the limitation instead of adding artificial coverage.

Remove temporary instrumentation and disposable artifacts created for the diagnosis. Report the cause, change if authorized, validation actually executed, and unresolved risks. Do not commit, push, update tickets, or publish external findings unless explicitly requested.
