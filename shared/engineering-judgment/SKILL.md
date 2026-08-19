---
name: engineering-judgment
description: Apply focused engineering judgment to a material decision about module or API design, safe legacy change, data or distributed-system semantics, or non-trivial code construction. Use when such a decision can materially affect correctness, change cost, or failure behavior. Do not use for routine edits or reviews with no substantive design decision.
---

# Engineering Judgment

Use this skill as a decision aid, not as a separate workflow or a source of requirements. The user request, ticket, repository evidence, and local conventions remain authoritative.

Identify the concrete decision before loading detail. If no material decision exists, continue without a reference. Read exactly one reference by default; read two only when the same decision genuinely crosses both concerns.

## Route

- Read [design-complexity.md](references/design-complexity.md) for public APIs, module boundaries, responsibility placement, information hiding, or abstractions that change how callers reason about the system.
- Read [legacy-change.md](references/legacy-change.md) when changing poorly understood, weakly tested, or tightly coupled behavior requires a safe seam or characterization strategy.
- Read [data-systems.md](references/data-systems.md) for ownership, consistency, transactions, retries, ordering, idempotency, schema evolution, caches, workers, events, or partial failures across boundaries.
- Read [construction.md](references/construction.md) for a non-trivial routine, state transition, algorithm, validation boundary, data representation, or error-handling design.

Apply only guidance that is supported by the task's evidence and proportional to its risk. Do not enlarge the diff to satisfy a principle, introduce speculative abstractions, or replace an established repository pattern without a concrete reason.

In code review, a principle may suggest what to investigate but is never a finding by itself. Report only a demonstrated defect, material risk, broken requirement, or explicit repository-rule violation, with concrete impact and evidence.
