---
name: deliver-ticket
description: Deliver a well-defined engineering ticket end to end. Use when the user asks to implement, fix, complete, or deliver work whose intended behavior is already defined in Linear, GitHub, Jira, or another tracker. Do not use for unclear product requirements, unknown-cause diagnosis, planning-only requests, or pure code review.
---

# Deliver Ticket

Use the ticket as the source of truth for intended behavior. User corrections, repository instructions, and verified repository facts still apply. Do not rewrite the ticket into another specification.

## 1. Understand

Read the ticket and relevant linked context. Inspect only enough of the repository to identify:

- acceptance criteria and affected behavior,
- the existing analogous implementation,
- relevant tests and validation seams,
- public, shared, data, or cross-system contracts involved.

Investigate discoverable facts. Ask only about unresolved decisions that materially change the implementation. If a reported bug has no established cause, use `diagnosing-bugs` as the primary workflow.

When the user supplies a repository, base, or branch, verify those live refs before editing. Do not silently continue from an unexpected branch, stale base, or conflicting remote branch.

## 2. Brief

Before substantial work, establish a compact execution brief containing:

- goal and acceptance criteria,
- existing pattern and affected surface,
- validation approach,
- material risks or blockers.

Keep the brief in the conversation. Skip it for trivial, single-file, low-risk changes.

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

Review the resulting diff against the ticket, correctness, repository conventions, tests, failure behavior, and unrelated changes. Apply deeper security, money, authorization, concurrency, migration, compatibility, performance, or cross-system scrutiny only when relevant.

Treat those areas as high risk. Surface the need for an independent review; do not create a subagent or invoke `code-review` automatically.

## 6. Finish

Report:

- what changed,
- validation actually executed,
- remaining risks or unresolved items.

Do not create extra documentation, commit, push, open a PR, publish comments, or send external messages unless explicitly requested or required by an established repository workflow.

When commit, push, or PR creation is authorized, review the final diff and validation first. Confirm the intended repository, remote branch state, and PR base immediately before publishing, then verify the resulting remote head and PR base/head.
