---
name: deliver-ticket
description: Use when the user asks to implement, fix, complete, or deliver a defined outcome from a ticket, accepted brief, or request. Do not use while a failure's cause is still unknown, for planning-only requests, for questions about how something works, or for pure code review.
---

# Deliver ticket

Treat the requested outcome, acceptance criteria, and stated constraints as authoritative. Treat cause analysis, named files, and suggested designs as leads that repository evidence can overturn. Record consequential contradictions; do not silently change the required behavior.

## Orient

Inspect each checkout the work touches before editing. From a workspace or set folder that is not itself a Git checkout, run these checks in every repository the work selects, for example with `git -C <repo>`:

```sh
git rev-parse --show-toplevel || exit 1
git rev-parse --abbrev-ref HEAD && git status --short && git log --oneline -5
git remote
git rev-parse --abbrev-ref '@{upstream}' 2>/dev/null || echo '<no upstream>'
```

Use remote names, not URLs that may contain credentials. Read root and applicable nested repository instructions, then locate the affected owner, analogous behavior, executable checks, and how the project runs. Do not assume the host loaded nested instructions.

Resolve a supplied base with `git rev-parse --verify '<ref>^{commit}'`; inspect divergence with `git merge-base --is-ancestor <base-ref> HEAD`. Exit 1 establishes non-ancestry, not its cause. Fetch when freshness matters. Resolve an unexpected branch safely before editing; preserve unrelated work and report any unresolved mismatch.

## Choose the route

- An unexplained failure goes to `diagnosing-bugs` first.
- An unresolved outcome or costly design choice that blocks a useful first slice goes to `shape-feature`. Continue here once it is settled when implementation is already authorized.
- Shared state, contracts, configuration, persistence, downstream consumers, several repositories or tickets, or uncertain impact: use `blast-radius` before the first slice. A ticket's named repositories and blast radius are leads, like its suggested cause.
- Several tickets that need edits in two or more repositories go to `orchestrate`.
- A demonstrably local, low-risk change needs only a short brief: owner, expected behavior, and focused check.

Keep the brief proportional: outcome and constraints, affected and preserved behavior, non-obvious design decision, next slice and proof, and material unknowns. Use the conversation for small work. When continuity or handoff needs a durable record, read [work context](references/work-context.md).

Several independent behavioral clusters call for a safe sequence, not an automatic stop. Continue through the authorized outcome. A slice may cross several layers; a PR or deployment may need a different boundary for migrations, mixed-version consumers, or rollout safety. Ask only when scope, business policy, authority, or a costly unresolved choice needs the user's decision.

## Implement through verified slices

Repeat until the authorized outcome is complete:

1. Choose the next observable behavior or uncertainty to resolve. Inspect its owner, callers, and material effects before choosing files.
2. Choose its proof with `verify-work` before the production edit. For a feasible material regression or invariant, see a relevant assertion fail first; an import failure or broken harness is not that failure. For exploration or impractical reproduction, use characterization, traces, or a bounded experiment and state what they cannot prove.
3. Implement only that behavior through the necessary layers. Prefer fewer concepts, less duplicated policy, fewer invalid states, and less coordination for the next change. Preserve contracts unless the requirement changes them.
4. Run the selected proof at the affected boundary and check material preserved behavior. Derive expected results independently of the implementation.
5. Remove code, flags, branches, tests, comments, or compatibility paths this slice has made obsolete. Keep a path only for a demonstrated caller or contract. Do not force an extraction or unrelated cleanup.
6. Reassess the next slice. Revise the brief when evidence changes the design. Delete invalid planned work instead of completing it for consistency. Ask when the new direction changes a consequential requirement or authority boundary.

Keep related implementation in one context within a repository. Do not create a new plan, agent, or checklist report for every iteration.

## Verify the integrated change

Inspect the complete diff against the outcome and the impact map; for a ticket set, inspect every repository's diff together against the set note. Passing slices do not prove their composition. Reopen any newly affected behavior. Check for obsolete code and duplicated policy. Apply the repository's comment rule; preserve invariant or external-contract information and remove stale rationale. Do not rewrite unrelated comments.

Before claiming the outcome works, use `verify-work`. Every acceptance criterion and material preserved behavior gets an evidence level, and behavior a user or another system sees is driven through its real entry point.

## Independent review

Self-review is not independent review. Require a fresh-context `code-review` for material changes to money movement, authorization boundaries, durable concurrent state, irreversible migrations, or external effects that are difficult to undo. For other changes, use independent review when requested, required locally, or needed for a concrete risk. Start with one reviewer.

Give the reviewer the requirement, exact diff, contracts, evidence table, and gaps without your reasoning history. A change across repositories goes to one reviewer as one package with the set note. Use [review evidence](../code-review/references/review-evidence.md) for a pinned handoff. If a fresh reviewer is unavailable, report that gap; do not relabel self-review as independent. Use `triage-review` to validate findings and fix accepted ones.

## Report and publish within authorization

Report changed behavior, the evidence table, and remaining risk. Do not claim readiness while required evidence or review is missing. A diagnostic draft or request for help can expose a gap when publication is authorized; it does not imply readiness. Never waive required repository gates.

When preparing the final report or PR body, reuse `unslop`, loading it only if absent.

Commit, push, or update a PR when already authorized; do not ask again merely because a phase changed. Otherwise keep external writes within the user's authorization. Immediately before publishing, confirm the remote head and intended base, then verify the resulting remote state. Never overwrite someone else's concurrent changes.
