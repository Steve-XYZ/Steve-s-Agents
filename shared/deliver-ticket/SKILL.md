---
name: deliver-ticket
description: Deliver well-defined engineering work end to end. Use when the user asks to implement, fix, complete, or deliver behavior already defined in a tracker, an accepted feature brief, or the user request itself. Do not use for unclear product requirements, unknown-cause diagnosis, planning-only requests, or pure code review.
---

# Deliver Ticket

Use the ticket, accepted feature brief, or explicit user requirements as the source of truth for intended behavior. User corrections, repository instructions, and verified repository facts still apply. Do not rewrite clear requirements into another specification.

Keep the ticket in one Codex or Claude Code session. Do not hand it to another harness mid-delivery.

## 1. Understand

Read the ticket and relevant linked context. Inspect enough of the repository to identify:

- acceptance criteria and affected behavior,
- the existing analogous implementation,
- relevant tests and validation seams,
- public, shared, data, deploy, or cross-system contracts involved.

Investigate discoverable facts. Ask only about unresolved decisions that materially change the implementation. If a reported bug has no established cause, use `diagnosing-bugs` as the primary workflow.

When the user supplies a repository, base, or branch, verify those live refs before editing. Do not silently continue from an unexpected branch, stale base, or conflicting remote branch.

## 2. Map and brief

Before choosing an implementation, read [change-impact](references/change-impact.md) and perform its pre-change pass. Build the brief from concrete locations and evidence, not from repository categories or an assumed design.

Then read [grill](references/grill.md) and pressure-test the behavior found in the map. If a product or architectural decision remains unresolved, stop and ask with a recommendation when evidence supports one. Do not implement around the gap.

Keep one compact brief in the conversation containing only what applies:

- goal and acceptance criteria,
- existing pattern,
- locations that change and behavior that must remain unchanged,
- invariant, owner, states, writers, or partial-failure boundary,
- validation approach,
- material risks or blockers.

Do not create a separate planning artifact. A trivial, local, low-risk change may use the short form defined by `change-impact`.

## 3. Implement

Implement the smallest coherent vertical change that satisfies the ticket. Follow repository patterns and preserve existing contracts unless the ticket explicitly changes them.

When the brief names an invariant or expensive failure, write or extend the test that can go red on that behavior before or with the production change. Cover the relevant failure class, not only the intended path.

Do not expand scope or perform unrelated cleanup. Do not add fields, settings, abstractions, or compatibility paths without a demonstrated caller or contract.

## 4. Prove

Read [prove-it-works](references/prove-it-works.md) and follow it. Prove both the requested behavior and any nearby behavior the brief says must remain unchanged.

Never claim success from inspection alone. A green build is not proof. State exactly what ran and what remains unverified.

## 5. Cold self-review

Re-read the ticket, final diff, and test results without using the implementation rationale as proof. Derive what changed from the diff itself.

Run the post-change pass in [change-impact](references/change-impact.md). If the diff reveals a location or behavior absent from the original map, update the map and inspect that impact before continuing.

Confirm only what applies:

1. Every acceptance criterion has an observable implementation and proof.
2. The owning component enforces each invariant; callers do not duplicate or bypass it.
3. Existing callers, stored data, defaults, deploy configuration, and downstream consumers preserve the intended behavior.
4. Failure, retry, concurrency, and partial success have defined outcomes when relevant.
5. Tests can fail for the target behavior and at least one material preserved or negative case.
6. The diff contains no dead fields, speculative compatibility, or unrequested cleanup.

Mark material claims without executable evidence as `UNPROVEN`. Do not create a critic or invoke `code-review` automatically. Recommend independent review when risk remains material.

## 6. Finish

For a pull request description, review comment, design explanation, or other substantial prose, read [WRITING.md](../global-guidance/WRITING.md) before responding.

Report:

- what changed,
- validation actually executed,
- remaining risks or unresolved items.

Do not create extra documentation, commit, push, open a PR, publish comments, or send external messages unless explicitly requested or required by an established repository workflow.

When publication is authorized, review the final diff and validation first. Confirm the intended repository, remote branch state, and PR base immediately before publishing, then verify the resulting remote head and PR base/head.
