---
name: shape-feature
description: Turn one of your own ideas into an implementable feature and first vertical slice. Use for solo or greenfield work where you are both author and implementer and the product, behavior, or architecture decisions are still open. Do not use when a tracker ticket or accepted brief already specifies the behavior, for unknown-cause bug diagnosis, or for pure code review.
---

# Shape Feature

Reduce uncertainty with the least process necessary. Stop at an implementation-ready brief unless the user also requested implementation and no material decisions remain.

## 1. Inspect

Understand the existing product and relevant implementation before asking questions. Load only the context needed to discover existing behavior, constraints, analogous features, and likely validation seams.

Do not ask the user for facts available in the repository, documentation, ticket history, or approved sources.

## 2. Resolve uncertainty

Separate uncertainty into:

- facts to investigate,
- product or architecture decisions to ask,
- non-blocking details to defer.

Ask only questions whose answers materially change behavior, contracts, data, architecture, or scope. Prefer a small grouped set of high-impact questions over exhaustive interviewing.

## 3. Research selectively

Use external, primary-source research only when correctness depends on current framework, protocol, regulatory, provider, or platform behavior. Retrieve only what is needed to resolve the decision.

Use a small prototype or experiment only when it is cheaper and more reliable than reasoning about the uncertainty. Do not turn exploration into production code accidentally.

When the brief requires a material decision about ownership, contracts, state, failure behavior, or an implementation boundary, read [judgment](../deliver-ticket/references/judgment.md) before finalizing the first slice. Do not use it to invent implementation detail prematurely.

## 4. Establish the brief

Once sufficiently clear, establish:

- problem and desired outcome,
- acceptance criteria,
- decisions made,
- out of scope,
- validation seam,
- first vertical slice,
- remaining risks or blockers.

Keep the brief proportional. Do not create a persistent document unless requested or the work must survive across sessions, agents, or future decisions.

## 5. Slice

Prefer independently verifiable vertical behavior. The first slice should be small enough to investigate, implement, validate, and review in one focused context.

If uncertainty still prevents a first slice, record only the destination, known decisions, blocking unknowns, and next experiment or research action. Resolve that blocker before planning the wider initiative.

Do not invoke `deliver-ticket` automatically. When shaping is complete, report the brief and the next executable slice.
