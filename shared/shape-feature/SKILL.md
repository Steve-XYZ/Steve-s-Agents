---
name: shape-feature
description: Use to resolve unclear product behavior, scope, or a costly architectural choice before implementation, in existing systems or new projects. Use even when a ticket exists if its decisions remain open. Do not use for a fully specified change with an established route, unknown-cause diagnosis, or pure code review.
---

# Shape a change

Resolve what prevents selecting a useful first slice. Preserve the requested outcome and constraints; investigate suggested causes and designs as leads.

## Inspect before asking

Read relevant repository instructions, existing behavior, analogous implementations, and validation seams. Separate unknown facts from decisions the user must make. Investigate facts available in code, documentation, tickets, or approved sources.

Ask only about choices that materially change behavior, contracts, data, architecture, scope, or authority. Give a recommendation when evidence supports it. Do not turn ordinary implementation choices into a product interview.

## Resolve the uncertainty

Use current primary sources when a framework, protocol, or provider fact determines correctness. Run a small authorized experiment when it is cheaper than continued speculation. Keep exploratory changes separate from production behavior and remove discarded experiments.

When a material question about ownership, contracts, state, failure behavior, or validation remains unresolved, read [judgment](../deliver-ticket/references/judgment.md). Stop the investigation once the next useful decision is supported.

## Establish a proportional brief

Record the outcome and constraints, acceptance criteria, decisions and evidence, scope exclusions, first behavior and proof, and material unknowns. Detail only the next slice. Keep later work provisional, including safe deployment order when one behavior spans several releases.

A slice may cross application layers. Prefer an observable behavior or a resolved uncertainty over completing a whole architectural layer.

Use a conversation brief for small work. For long exploration, interruptions, handoff, or a context reset, use [work context](../deliver-ticket/references/work-context.md). A separate planning session is conditional, not a prerequisite.

## Continue within the request

For planning-only requests, stop with the brief and next executable step. If implementation is already requested and no material decision blocks the first slice, continue through `deliver-ticket`. Do not stop just to ask permission to enter another workflow.

If no implementation slice can yet be chosen, identify the blocking unknown and the next evidence-producing experiment. Do not write a detailed plan around the gap.

When preparing a final brief or report, reuse `unslop`, loading it only if absent.
