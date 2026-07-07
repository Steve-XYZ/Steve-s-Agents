---
name: diagnosing-bugs
description: Evidence-first diagnosis workflow for bugs, regressions, and intermittent failures. Use when the user says "diagnose" or "debug this", or reports something broken, throwing, failing, flaky, or slow — before changing any code.
---

# Diagnosing Bugs

A discipline for diagnosing before changing code. Follow the phases in order; skip a phase only with explicit justification.

**Core rule: do not propose or implement a fix until the local feedback loop or captured evidence demonstrates the reported symptom.** No speculative fixes, no large refactors, no architecture changes before sufficient evidence.

Read existing repository documentation relevant to the area—such as README, AGENTS.md, CLAUDE.md, ADRs, runbooks, deployment notes, or test documentation—when present. None of it is required to use this skill.

## Phase 1 — Build a feedback loop or evidence loop

If you have a tight pass/fail signal that goes red on *this* bug, the rest is mechanical. Spend disproportionate effort here.

### Prefer a local red-capable command

One command you have already run at least once, that:

- drives the actual bug code path and asserts the user's exact symptom — not "runs without erroring";
- gives the same verdict every run (for flaky bugs: a pinned, high reproduction rate);
- runs unattended.

Ways to construct one, in rough order:

1. Failing test at whatever seam reaches the bug — unit, integration, e2e.
2. Curl/HTTP script against a locally running service.
3. CLI or script invocation with a fixture input, diffed against a known-good output.
4. Replay a captured artifact (request, message payload, event log) through the code path in isolation.
5. Throwaway harness: one service with mocked dependencies exercising the bug path directly.
6. Bisection: if the bug appeared between two known states, automate "boot at state X, check, repeat".
7. Differential run: same input through old vs. new version (or two configs), diff outputs.
8. Human-in-the-loop script (`scripts/hitl-loop.template.sh`) as a last resort when a human must click or act behind a VPN — the loop stays structured and its output feeds back to you.

### Loop speed

Prefer fast feedback: seconds when practical. Reliable integration loops taking roughly one to two minutes are acceptable when they provide meaningful evidence — including Docker Compose, Testcontainers, `WebApplicationFactory`, database integration tests, or message-bus test harnesses (e.g. the MassTransit in-memory test harness).

### Captured evidence as a valid substitute

When a local loop is impossible, not reproducible, or disproportionately costly — the problem depends on staging, VPN, real data, queues, or external services — accept captured, verifiable evidence instead:

- structured logs tied together by correlation ID;
- distributed traces;
- MassTransit or queue message payloads;
- request/response captures;
- database data snapshots or queries;
- metrics;
- dumps;
- observations reproducible in staging.

The evidence must show the reported symptom, not a nearby failure. State explicitly that you are working from captured evidence and what a full loop would have required.

### Shared resources

Run stress loops, parallel reproduction, fuzzing, repeated triggers, or load-oriented diagnostics only against isolated local or dedicated test resources. Never run them against shared staging, shared databases, shared queues, production-like shared infrastructure, or third-party services without explicit approval and safeguards.

### Intermittent bugs

The goal is a higher reproduction rate, not necessarily a clean repro: loop the trigger, add stress, narrow timing windows — within the shared-resources rule above. A bug that reproduces half the time is debuggable; one-in-a-hundred is not.

### If neither a loop nor evidence is attainable

Stop and say so. List what you tried, then ask the user for environment access, a captured artifact, or permission to add temporary instrumentation. Do not proceed to hypotheses without a loop or evidence.

## Phase 2 — Reproduce and minimize

Run the loop (or examine the evidence) and confirm:

- it shows the failure mode the user described — wrong bug means wrong fix;
- it is repeatable, or reproduces at a rate high enough to debug against;
- you have captured the exact symptom (error message, wrong output, timing) so later phases can verify the fix.

Then minimize: cut inputs, callers, config, data, and steps one at a time, re-checking after each cut, until every remaining element is load-bearing. A minimal repro shrinks the hypothesis space and becomes the regression test later.

## Phase 3 — Form ranked falsifiable hypotheses

Generate 3–5 ranked hypotheses before testing any of them, unless the evidence already points conclusively to a single cause. Single-hypothesis thinking anchors on the first plausible idea.

Each hypothesis must state a falsifiable prediction:

> "If X is the cause, then changing Y will make the bug disappear / changing Z will make it worse."

If you cannot state the prediction, discard or sharpen the hypothesis. Show the ranked list to the user before testing — they often re-rank it instantly — but do not block on a reply.

## Phase 4 — Instrument one variable at a time

Each probe must test one concrete prediction from Phase 3. Change one variable at a time.

- Prefer a debugger or REPL when the environment supports it; otherwise targeted tests, distributed traces, and structured logs with correlation IDs at the boundaries that distinguish hypotheses.
- Do not "log everything and grep".
- Tag every piece of temporary instrumentation with a unique prefix (e.g. `[DEBUG-a4f2]`) so removal is a single grep.
- For performance regressions, measure first: establish a baseline (timing harness, profiler, `EXPLAIN ANALYZE`, query plan), then bisect. Logs are usually the wrong tool.

## Phase 5 — Fix and regression coverage

The fix must be minimal and specific to the confirmed hypothesis. Do not turn the diagnosis into an unrequested refactoring or redesign.

Add a regression test or equivalent coverage only when a correct, reliable seam exists — one where the test exercises the real bug pattern as it occurs at the call site. Do not write artificial tests that give false confidence; if no correct seam exists, that itself is a finding worth recording.

When a correct seam exists:

1. Turn the minimized repro into a failing test at that seam and watch it fail.
2. Apply the fix and watch it pass.
3. Re-run the original Phase 1 loop or re-verify against the original captured evidence.

### Durable messaging boundary

Preserve existing consumer boundaries, retry semantics, idempotency conventions, outbox behavior, transaction boundaries, and message contracts. Do not move durable queue-driven work into HTTP request handlers or in-process hosted services merely to simplify a local fix.

## Phase 6 — Cleanup and prevention follow-up

Before declaring done:

- [ ] The original repro no longer reproduces (loop re-run or evidence re-verified).
- [ ] Regression test passes, or the absence of a correct seam is documented.
- [ ] All tagged temporary instrumentation is removed (grep the prefix).
- [ ] Throwaway harnesses and prototypes are deleted.
- [ ] The confirmed hypothesis is stated in the commit or PR message so the next debugger learns.

Then ask what would have prevented this bug. Record any prevention opportunity as a concise non-blocking follow-up in the PR description, Linear ticket, bug report, or repository documentation when relevant.
