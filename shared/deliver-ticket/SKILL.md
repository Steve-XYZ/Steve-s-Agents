---
name: deliver-ticket
description: Deliver well-defined engineering work end to end. Use when the user asks to implement, fix, complete, or deliver behavior already defined in a tracker, an accepted feature brief, or the user request itself. Do not use for unclear product requirements, unknown-cause diagnosis, planning-only requests, or pure code review.
---

# Deliver Ticket

Use the ticket, accepted feature brief, or explicit user requirements as the source of truth for intended behavior. User corrections, repository instructions, and verified repository facts still apply. Do not rewrite clear requirements into another specification.

The same loop runs on Codex or Claude Code. Do not hand the ticket to a second harness mid-delivery.

## 1. Understand

Read the ticket and relevant linked context. Inspect only enough of the repository to identify:

- acceptance criteria and affected behavior,
- the existing analogous implementation,
- relevant tests and validation seams,
- public, shared, data, or cross-system contracts involved.

Investigate discoverable facts. Ask only about unresolved decisions that materially change the implementation. If a reported bug has no established cause, use `diagnosing-bugs` as the primary workflow.

When the user supplies a repository, base, or branch, verify those live refs before editing. Do not silently continue from an unexpected branch, stale base, or conflicting remote branch.

## 2. Grill and brief

After the initial repository inspection and before settling an implementation
approach or execution plan, read [grill](../grill/SKILL.md) and follow it.
That pass loads [engineering-judgment](../engineering-judgment/SKILL.md).
Let the result shape the brief; do not treat an earlier draft plan as
fixed. Do not turn this pass into a separate plan or artifact.

If grill stops on an unresolved product or architectural decision, stop here.
Do not implement around the gap.

When the brief identified material surfaces beyond a single file — money,
durable state, provider calls, deploy configuration, shared contracts, or
cross-repo consumers — read [blast-radius](../blast-radius/SKILL.md) and
keep implementation inside that list.

Skip grill, blast-radius, and the brief for trivial, single-file, low-risk
changes when the judgment pass confirms no material risk.

## 3. Implement

Implement the smallest coherent vertical change that satisfies the ticket. Follow repository patterns and preserve existing contracts unless the ticket explicitly changes them.

When the brief named an invariant, write or extend the test that can go red
on that invariant before (or with) the production change. Cover the failure
class — stamp conflict, duplicate retry, illegal transition, guard negative
case — not only the observed happy path. Do not add a field, flag, or
setting that nothing writes or reads.

Do not expand scope or perform unrelated cleanup. Add or update tests when behavior changes or a regression could recur. For a bug with an established cause, reproduce the failure first when practical and safe.

## 4. Prove

Read [prove-it-works](../prove-it-works/SKILL.md) and follow it. Run the cheapest reliable checks first:

1. directly affected tests or checks, including the invariant and its negative case,
2. affected project or module,
3. a throwaway host and a real request when the change is an API, money path, or contract the tests cannot reach,
4. relevant build,
5. broader suites only when risk or repository CI justifies them.

Never claim success from inspection alone. A green build is not proof. State exactly what ran and what remains unverified.

## 5. Self-review

Review the resulting diff against the ticket, correctness, repository
conventions, tests, failure behavior, and unrelated changes. When the brief
identified material invariants, states, writers, or partial-failure boundaries,
challenge the implementation and tests against that same model rather than
only confirming the intended path.

When those concerns applied, confirm each item that is in scope:

1. The invariant lives in the owning Core (or equivalent) component, not in an endpoint, UI, or worker.
2. Illegal state combinations are difficult to persist.
3. Mid-operation death, retry, and stamp conflict have defined behavior, or the gap is stated.
4. Capability (`canX`) is not the same call as the provider or ledger side effect.
5. Each new setting exists in the deploy configuration of the service that reads it.
6. Frontend, Admin/PAM, export, and cache stay aligned with the payload or label.
7. A catalogue or seed guard has a test that goes red on the case it claims to catch.
8. Permissions and nav gating match the new path.
9. No unused confirmation, cancellation, actor, or stamp fields.
10. Diff contains no unrequested cleanup.

Treat money, authorization, concurrency, migration, compatibility, and
cross-system contracts as high risk. Surface the need for an independent
review; do not create a subagent or invoke `code-review` automatically.

## 6. Finish

When writing a pull request description, review comment, or report longer
than a short status line, read [unslop](../unslop/SKILL.md).

Report:

- what changed,
- validation actually executed,
- remaining risks or unresolved items.

Do not create extra documentation, commit, push, open a PR, publish comments, or send external messages unless explicitly requested or required by an established repository workflow.

When commit, push, or PR creation is authorized, review the final diff and validation first. Confirm the intended repository, remote branch state, and PR base immediately before publishing, then verify the resulting remote head and PR base/head. If this session cannot finish, write a handoff in the conversation for the same harness; do not switch Codex and Claude Code mid-ticket.
