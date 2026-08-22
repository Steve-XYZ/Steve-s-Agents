---
name: deliver-ticket
description: Deliver well-defined engineering work end to end. Use when the user asks to implement, fix, complete, or deliver behavior already defined in a tracker, an accepted feature brief, or the user request itself. Do not use for unclear product requirements, unknown-cause diagnosis, planning-only requests, or pure code review.
---

# Deliver Ticket

Use the ticket, accepted feature brief, or explicit user requirements as the source of truth for intended behavior. User corrections, repository instructions, and verified repository facts still apply. Do not rewrite clear requirements into another specification.

Breadth in discovery. Depth in judgment. Discipline in execution. Independence
in review. Evidence against the claim.

## 1. Discover

Read the ticket and relevant linked context. Inspect only enough of the repository to identify:

- acceptance criteria and affected behavior,
- the existing analogous implementation,
- relevant tests and validation seams,
- public, shared, data, or cross-system contracts involved.

Then enumerate the change surface. For each symbol, setting, table, message, or
endpoint the change touches, list what already exists around it:

- readers and writers,
- callers, and sibling paths that solve the same problem,
- persistence and migrations,
- configuration layers and per-environment overrides,
- deployment scopes and tenants,
- asynchronous consumers and external contracts,
- reachable failure paths.

The scan enumerates; it does not judge. Record concrete locations rather than
categories: `Api/appsettings.Development.json:16` is checkable, `configuration:
reviewed` is not. Leave a category out when it genuinely has no members instead
of asserting that you checked it. A missing entry is a discovery gap someone
else can find; an unfalsifiable claim is not. Judgment happens in step 2, and
this scan produces no findings of its own.

Record what you could not reach, next to what you found. A surface that exists
but cannot be inspected from here is not the same as a surface that does not
exist, and silence collapses the two into false confidence. Naming the limit is
still enumeration.

Read [change-surface.md](references/change-surface.md) for the enumeration
recipe when the surface is unfamiliar or the change is material.

When the change affects money, migrations, tenants, shared contracts, or more
than one system, a Scout produces this scan in a fresh context. Its inputs are
the ticket, the linked context the ticket depends on, the repository
instructions, and the repository. It does not receive a brief, an approach, or
any part of the intended solution: an enumeration made with nothing to defend
is more complete. Its output is the list and the limits of the list, and nothing
else. For ordinary changes, produce the scan inline.

Emit the scan verbatim rather than summarising it, so the run preserves it. When
the change is published, carry it into the pull request or the ticket. An escaped
defect can only be attributed to a stage if what discovery actually contained is
still recoverable.

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

Run a surface delta as you go. When the implementation ends up touching a
setting, symbol, table, event, or contract the scan does not list, stop and
enumerate that one entity's immediate surface before continuing: its readers and
writers, its configuration layers, its consumers. Add it to the scan. A design
that grows past its own enumeration is the ordinary way a complete scan goes
stale, and the entities added late are the ones nobody has looked around.

## 4. Verify

Validate the requirement, not the implementation. State the claim the ticket
makes, then prefer evidence that could falsify it. Evidence that only proves the
edit exists does not establish that the requirement holds: that a setting
carries the intended value is evidence about the edit, while the claim is that
every supported environment resolves it and behaves correctly.

Run the cheapest reliable checks first:

1. directly affected tests or checks,
2. affected project or module,
3. relevant build,
4. broader suites only when risk or repository CI justifies them.

Never claim success from inspection alone. State exactly what ran, which claim
it settles, and what remains unverified.

## 5. Fresh Critic

A material or risky change is reviewed by a critic in a fresh context, not by
the agent that built it. Treat security, money, authorization, durable state,
concurrency, shared contracts, migrations, tenants, cross-system behavior, and
partial success as material. A trivial, low-risk change is reviewed against the
ticket and the diff directly.

The critic receives the ticket, the scan, the brief, the diff, the record of the
validation that was run and what it showed, and the repository instructions and
conventions. It does not receive the reasoning that produced the change.

The scan and the brief are handed over as claims to
falsify, not as established fact: the point of the fresh context is that nothing
in it inherits the builder's confidence.

Its brief is [fresh-critic.md](references/fresh-critic.md). This review is not
`code-review`, which is for a change you do not own.

## 6. Fix and revalidate

The critic returns coverage gaps and findings, and they are handled differently.

A coverage gap corrects the scan: add the surface, and enumerate it as the delta
step already requires. It is not a defect and it does not become work by itself.
Extra breadth that turns into extra tasks is how a wider map becomes noise.

A finding is addressed only when the critic demonstrated it. For each remaining
finding, either fix it or state why it is not a defect; do not leave it
unanswered and do not accept it because a reviewer raised it. Revalidate the
claims the fix touches rather than rerunning everything, and do not let review
commentary expand the scope of the ticket.

Return to the critic when a fix materially changes the design, the surface, a
contract or an invariant, or introduces behavior beyond the demonstrated repair.
A local fix with targeted validation does not need another pass.

This is not `triage-review`, which handles findings that arrive from outside
on a change already open for review.

## 7. Report

Report:

- what changed,
- validation actually executed, and which claim each check settles,
- findings raised and how each was resolved,
- coverage gaps found, and the scan corrected to include them,
- remaining risks or unresolved items.

Carry the scan into the pull request or the ticket when the change is published.

Do not create extra documentation, commit, push, open a PR, publish comments, or send external messages unless explicitly requested or required by an established repository workflow.

When commit, push, or PR creation is authorized, review the final diff and validation first. Confirm the intended repository, remote branch state, and PR base immediately before publishing, then verify the resulting remote head and PR base/head.
