---
name: engineering-judgment
description: Apply a compact cross-cutting judgment pass to a material engineering decision. Loaded by deliver-ticket and conditionally by shape-feature; outside those workflows, use only when the user explicitly asks for engineering judgment. Do not auto-select for routine edits, diagnosis, code review, or review triage.
---

# Engineering Judgment

Before committing to an implementation or first slice, identify what makes this change difficult: what callers must know, what behavior cannot be verified, where work can succeed partially, and what states or failures the code must distinguish. These concerns overlap. Name the dominant difficulty, its evidence, and the cost of being wrong. Retain any independent material risk that could violate required behavior or corrupt durable or external state; do not discard it merely to force the change into one category.

Trace the real path, callers, observable behavior, ownership, side effects, and validation. Decide what must remain unchanged, where the invariant should live, and what evidence will prove the result. Prefer the smallest design that lets the owner enforce the rule, makes partial failure visible, and represents important distinctions directly.

After inspecting the repository, read [deepening.md](references/deepening.md) only when the cost of being wrong is material and evidence still leaves one or more concrete risks unresolved:

- no honest validation seam reaches the affected behavior;
- failure can leave durable or external state partially updated;
- a shared contract, schema, migration, or ownership boundary changes;
- several callers coordinate the same knowledge or invariant;
- the implementation must distinguish states or failures that the current representation obscures.

Touching legacy code, a database, an API, or complex-looking code does not qualify by itself. When none of these risks remains unresolved, continue without deepening. Do not create a separate plan, explanation, or artifact for this pass.

Do not add abstractions, tests, error handling, or generality merely to satisfy this pass. Requirements, evidence, and local patterns outrank these heuristics; a principle alone is never a code-review finding. If the pass only confirms the existing decision, do not change the code or enlarge the scope.
