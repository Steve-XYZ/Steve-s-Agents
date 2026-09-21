---
name: deliver-ticket
description: Use when the user asks to implement, fix, complete, or deliver a defined outcome from a ticket, accepted brief, or request. Shape unresolved decisions when needed and resume delivery once settled. Use diagnosing-bugs first for an unknown cause. Do not use for planning-only requests or pure code review.
---

# Deliver ticket

Treat the requested outcome, acceptance criteria, and stated constraints as authoritative. Treat cause analysis, named files, and suggested designs as leads that repository evidence can overturn. Record consequential contradictions; do not silently change the required behavior.

## Orient and establish scope

Inspect the checkout before editing:

```sh
git rev-parse --show-toplevel || exit 1
git rev-parse --abbrev-ref HEAD && git status --short && git log --oneline -5
git remote
git rev-parse --abbrev-ref '@{upstream}' 2>/dev/null || echo '<no upstream>'
```

Use remote names, not URLs that may contain credentials. Read root and applicable nested repository instructions, then locate the affected owner, analogous behavior, and executable checks. Do not assume the host loaded nested instructions.

Resolve a supplied base with `git rev-parse --verify '<ref>^{commit}'`; inspect divergence with `git merge-base --is-ancestor <base-ref> HEAD`. Exit 1 establishes non-ancestry, not its cause. Fetch when freshness matters. Resolve an unexpected branch safely before editing; preserve unrelated work and report any unresolved mismatch.

Investigate discoverable facts. Use `diagnosing-bugs` for an unexplained failure. Use `shape-feature` when an unresolved outcome or costly design choice prevents selecting a useful next slice. Continue after those decisions are settled when implementation is already authorized.

## Map the outcome and choose the next slice

For a demonstrably local, low-risk change, identify the owner, expected behavior, and focused check in a short brief. For shared state, contracts, configuration, persistence, downstream consumers, or uncertain impact, read [change-impact](references/change-impact.md). Read [grill](references/grill.md) when invariants, ownership, or failure behavior need investigation. Read [judgment](references/judgment.md) only if a specific material risk remains unresolved.

Keep the brief proportional: outcome and constraints, concrete affected and preserved behavior, non-obvious design decision, next slice and proof, and material unknowns. Use one conversation brief for small work. When continuity or handoff requires a durable record, read [work context](references/work-context.md).

Several independent behavioral clusters call for a safe sequence, not an automatic stop. Continue through the authorized outcome. A slice may cross several layers; a PR or deployment may need a different boundary for migrations, mixed-version consumers, or rollout safety. Ask only when scope, business policy, authority, or a costly unresolved choice needs the user's decision.

## Implement through verified slices

Repeat until the authorized outcome is complete:

1. Choose the next observable behavior or uncertainty to resolve. Inspect its owner, callers, and material effects before choosing files.
2. Choose proof before the production edit. Use [prove-it-works](references/prove-it-works.md) for evidence selection. For a feasible material regression or invariant, observe a relevant failing assertion first. Import failures or a broken harness are not RED evidence. For exploration or impractical reproduction, use characterization, traces, or a bounded experiment and state what they cannot prove.
3. Implement only that behavior through the necessary layers. Prefer fewer concepts, less duplicated policy, fewer invalid states, and less coordination for the next change. Preserve contracts unless the requirement changes them.
4. Run the selected proof at the affected boundary and check material preserved behavior. Derive expected results independently of the implementation.
5. Remove code, flags, branches, tests, comments, or compatibility paths this slice has made obsolete. Keep a path only for a demonstrated caller or contract. Do not force an extraction or unrelated cleanup.
6. Reassess the next slice. Revise the impact map and brief when evidence changes the design. Delete invalid planned work instead of completing it for consistency. Continue within scope; ask when the new direction changes a consequential requirement or authority boundary.

Keep related implementation in one context. Use [work context](references/work-context.md) only when context isolation, interruption, handoff, or parallel work adds value. Do not create a new plan, agent, or checklist report for every iteration.

## Verify the integrated change and review it

Inspect the complete diff against the outcome and impact map. Confirm changed shared facts, primary and ancillary effects, and tests still agree after integration. Reopen any newly affected behavior. Passing slices do not prove their composition.

Check for obsolete code and duplicated policy. Apply the repository's comment rule; preserve useful invariant or external-contract information and remove stale rationale. Do not rewrite unrelated comments.

Self-review prepares the change; it is not independent review. Require `code-review` in a fresh context for material changes to money movement, authorization boundaries, durable concurrent state, irreversible migrations, or external effects that are difficult to undo. For other changes, use independent review when requested, required locally, or needed to resolve a concrete risk. Start with one reviewer. Inspect a risky invariant early if a wrong decision would be expensive, then review the integrated result.

Provide the requirement, exact diff, contracts, evidence, and gaps without the author's reasoning history. Use [review evidence](../code-review/references/review-evidence.md) for a pinned handoff. If a fresh reviewer is unavailable, report that gap; do not relabel self-review as independent. Use `triage-review` to validate findings and fix accepted ones.

## Report and publish within authorization

Report changed behavior, checks actually executed, and remaining risk. Mark material missing proof `UNPROVEN`. Do not claim readiness while required evidence or review is missing. A diagnostic draft or request for help can expose a gap when publication is authorized; it does not imply readiness. Never waive required repository gates.

When preparing the final report or PR body, reuse `unslop`, loading it only if absent.

Commit, push, or update a PR when already authorized; do not ask again merely because a phase changed. Otherwise keep external writes within the user's authorization. Immediately before publishing, confirm the remote head and intended base, then verify the resulting remote state. Never overwrite someone else's concurrent changes.
