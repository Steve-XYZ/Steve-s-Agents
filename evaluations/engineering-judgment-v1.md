# Engineering Judgment V1 Evaluation

Evaluate the integrated skill against the parent commit using the same model, repository snapshot, user prompt, and available tools. Run each task once without the skill and once with it. Keep the outputs unlabeled during comparison and do not tell either run the expected conclusion.

## Representative tasks

1. **Module/API design:** Add a provider-neutral operation where two existing callers currently coordinate sequencing and validation. Compare boundary ownership, exposed concepts, compatibility, and unnecessary abstractions.
2. **Legacy change:** Change one report/export behavior in a weakly tested path with static dependencies. Compare the chosen safety seam, preserved behavior, validation strength, and diff scope.
3. **Data/distributed semantics:** Change a worker that can receive duplicate or reordered events and updates a durable projection. Compare stated guarantees, idempotency placement, partial-failure handling, and schema compatibility.
4. **Non-trivial construction:** Implement a state transition or parser with several invalid inputs and failure outcomes. Compare invariant clarity, control flow, error semantics, and focused tests.

## Comparison record

For each pair, record:

- material decisions that differ and which version is better supported by repository evidence;
- requirement fidelity and correctness under representative failure cases;
- new abstractions, dependencies, files, and lines changed;
- false or preference-only review findings;
- validation performed and important paths left unverified;
- skill/reference files loaded and their approximate token cost;
- reviewer preference with a concrete reason, not a numeric health score.

Retain the integration when it repeatedly improves a material decision or exposes a real risk without consistent growth in scope, abstraction, false findings, or context. Narrow its triggers or references when the benefit is domain-specific. Revert the integration if it mostly restates normal workflow behavior, produces theory-driven review comments, or adds process without changing decisions.
