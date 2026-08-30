# Grill

Pressure-test the mapped behavior before choosing the implementation. Apply the compact pass from [engineering-judgment](../../engineering-judgment/SKILL.md), then answer only the questions that can change the design:

- What must remain true, and which component owns that rule?
- Which callers read, write, transport, or independently reconstruct the same fact?
- Which states and transitions exist, and which combinations must remain impossible?
- What happens to existing data, defaults, and in-flight work?
- What remains after failure, retry, duplicate delivery, concurrency, or partial success?
- Which effects are primary and which are ancillary? For each reachable failure, is it transient, permanent, an idempotent conflict, or still unknown; is retry safe; and should the primary effect commit, roll back, retry, or remain visibly partial?
- Which deploy process, tenant, environment, external provider, or consumer can observe the change?
- Which target, negative, and preserved cases can prove the result?
- Does every proposed field, setting, branch, or abstraction have a demonstrated caller or contract?

Use repository evidence to answer these questions. Do not ask the user for discoverable facts or present an exhaustive interview.

When a genuine product or architectural decision remains, ask only the smallest question needed to proceed. Include:

- **Question:** the unresolved choice;
- **Recommendation:** the best option when evidence supports one;
- **Evidence:** the repository fact or trade-off behind it;
- **Alternative consequence:** what materially changes if another option is chosen.

Say when the evidence does not support a recommendation. Do not invent a preference to complete the format.

Feed the answers into the execution brief. Do not create a second plan or start implementation from this reference.
