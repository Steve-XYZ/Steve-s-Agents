---
name: deliver-ticket
description: Deliver well-defined engineering work end to end. Use when the user asks to implement, fix, complete, or deliver behavior already defined in a tracker, an accepted feature brief, or the user request itself. Do not use for unclear product requirements, unknown-cause diagnosis, planning-only requests, or pure code review.
---

# Deliver Ticket

Use the ticket, accepted feature brief, or explicit user requirements as the source of truth for intended behavior. User corrections, repository instructions, and verified repository facts still apply. Do not rewrite clear requirements into another specification.

## 1. Understand

Read the ticket and relevant linked context. Inspect only enough of the repository to identify:

- acceptance criteria and affected behavior,
- the existing analogous implementation,
- relevant tests and validation seams,
- public, shared, data, or cross-system contracts involved.

Investigate discoverable facts. Ask only about unresolved decisions that materially change the implementation. If a reported bug has no established cause, use `diagnosing-bugs` as the primary workflow.

When the user supplies a repository, base, or branch, verify those live refs before editing. Do not silently continue from an unexpected branch, stale base, or conflicting remote branch.

## 2. Judge and brief

After the initial repository inspection and before settling an implementation
approach or execution plan, read
[engineering-judgment](../engineering-judgment/SKILL.md) and apply its compact
pass. Let the result shape the brief; do not treat an earlier draft plan as
fixed. Do not turn this pass into a separate plan or artifact.

Before substantial work, establish a compact execution brief containing:

- goal and acceptance criteria,
- existing pattern and affected surface,
- validation approach,
- material risks or blockers.

When the change materially affects money, durable state, concurrency, shared
contracts, migrations, or partial success, also capture only what applies:

- the invariant and the component that owns it,
- relevant states, transitions, and writers,
- the transaction or partial-failure boundary,
- adversarial cases that must be verified.

Keep the brief in the conversation. Skip it for trivial, single-file, low-risk
changes when the judgment pass confirms no material risk.

## 3. Implement

Implement the smallest coherent vertical change that satisfies the ticket. Follow repository patterns and preserve existing contracts unless the ticket explicitly changes them.

Do not expand scope or perform unrelated cleanup. Add or update tests when behavior changes or a regression could recur. For a bug with an established cause, reproduce the failure first when practical and safe.

## 4. Verify

Run the cheapest reliable checks first:

1. directly affected tests or checks,
2. affected project or module,
3. relevant build,
4. broader suites only when risk or repository CI justifies them.

Never claim success from inspection alone. State exactly what ran and what remains unverified.

## 5. Self-review

Review the resulting diff against the ticket, correctness, repository
conventions, tests, failure behavior, and unrelated changes. When the brief
identified material invariants, states, writers, or partial-failure boundaries,
challenge the implementation and tests against that same model rather than
only confirming the intended path. Apply deeper security, money,
authorization, concurrency, migration, compatibility, performance, or
cross-system scrutiny only when relevant.

Treat those areas as high risk. Surface the need for an independent review; do not create a subagent or invoke `code-review` automatically.

## 6. Finish

Report:

- what changed,
- validation actually executed,
- remaining risks or unresolved items.

Do not create extra documentation, commit, push, open a PR, publish comments, or send external messages unless explicitly requested or required by an established repository workflow.

When commit, push, or PR creation is authorized, review the final diff and validation first. Confirm the intended repository, remote branch state, and PR base immediately before publishing, then verify the resulting remote head and PR base/head.
