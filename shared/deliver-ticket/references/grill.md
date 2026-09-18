# Grill

Pressure-test the mapped behavior before choosing the implementation.

## Name the difficulty

Identify what makes this change hard: what callers must know, what behavior cannot be verified, where work can succeed partially, and which states or failures the code must distinguish. These overlap. Name the dominant difficulty, its evidence, and the cost of being wrong. Keep any independent material risk that could violate required behavior or corrupt durable or external state; do not discard it to force the change into one category.

Trace the real path, callers, observable behavior, ownership, side effects, and validation. Decide what must remain unchanged, where the invariant should live, and what evidence will prove the result. Prefer the smallest design that lets the owner enforce the rule, makes partial failure visible, and represents important distinctions directly.

## Answer only what changes the design

- What must remain true, and which component owns that rule?
- Which callers read, write, transport, or independently reconstruct the same fact?
- Which states and transitions exist, and which combinations must remain impossible?
- What happens to existing data, defaults, and in-flight work?
- What remains after failure, retry, duplicate delivery, concurrency, or partial success?
- Which effects are primary and which are ancillary? For each reachable failure, is it transient, permanent, an idempotent conflict, or still unknown; is retry safe; and should the primary effect commit, roll back, retry, or remain visibly partial?
- Which deploy process, tenant, environment, external provider, or consumer can observe the change?
- Which target, negative, and preserved cases can prove the result?
- Does every proposed field, setting, branch, or abstraction have a demonstrated caller or contract?

Use repository evidence to answer these. Do not ask the user for discoverable facts or present an exhaustive interview.

## Go deeper only on an unresolved risk

Read [judgment](judgment.md) when the cost of being wrong is material and one of these remains unresolved after the questions above:

- no honest validation seam reaches the affected behavior;
- failure can leave durable or external state partially updated;
- a shared contract, schema, migration, or ownership boundary changes;
- several callers coordinate the same knowledge or invariant;
- the implementation must distinguish states or failures that the current representation obscures.

Touching legacy code, a database, an API, or complex-looking code does not qualify by itself. When none of these remains open, continue without it.

Do not add abstractions, tests, error handling, or generality merely to satisfy this pass. Requirements, evidence, and local patterns outrank these heuristics, and a principle alone is never a code-review finding.

## Ask only what evidence cannot settle

When a genuine product or architectural decision remains, ask the smallest question needed to proceed. Include:

- **Question:** the unresolved choice;
- **Recommendation:** the best option when evidence supports one;
- **Evidence:** the repository fact or trade-off behind it;
- **Alternative consequence:** what materially changes if another option is chosen.

Say when the evidence does not support a recommendation. Do not invent a preference to complete the format.

Feed the answers into the execution brief. Do not create a second plan or start implementing from this reference.
