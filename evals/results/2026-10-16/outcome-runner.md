# Outcome runner validation

The fixture generator previously supplied tasks and guidance, but no executable grader checked their outcomes. The new runner keeps execution receipts outside candidate context, and the grader checks behavior independently of the supplied tests. This record validates the tooling, not a workflow or model improvement.

## Executed controls

`python3 evals/test-task-evals.py` passed 23 tests on Linux with Python 3.12.14. The tests use real disposable repositories and subprocesses, with a fake Codex executable where provider output is needed. No paid model inference is used.

The controls establish these outcomes:

- A currency implementation can pass its existing suite and still fail the independent EUR-configured, no-flag USD-default check. Correcting that default passes the same oracle. Breaking the module entry point fails it again.
- Corrected empty-result, CSV/quantity, tier-limit, retry and three-repository implementations pass. The original defects and an implementation that updates only the named service fail.
- Negative fractional quantities must be rejected before mutation. A retry implementation that silently drops previously failed deliveries fails even when its supplied suite passes. Both negative controls exposed passing grades before the oracle corrections.
- The clean discount review remains `manual_required` even when its response says approval. Editing its source fails the read-only check. No keyword classifier assigns review correctness.
- A typo control passes through CLI behavior with empty unittest discovery recorded as `not_applicable`.
- Existing destinations, outputs under Git checkouts, dangling links, records inside candidate context and grades inside the task are refused.
- Prompt, catalog, raw-response and untracked-source changes invalidate the recorded state. Source changes during validation cannot retain a pass.
- Requested model/effort arguments reach the fake CLI. Valid usage counters and completed-item types are retained; absent, malformed or invalid usage remains null. Unreported resolved model identity, dollar cost and total tool calls remain null.
- Multi-repository execution permits Codex startup outside a Git checkout while retaining independent child checkouts. The fake CLI rejects that layout without the required flag; its regression failed before the adapter correction. Codex CLI 0.159.2 also accepted the corrected arguments without the previous trusted-directory rejection, then reached the three-second probe timeout with no model turn or usage. That probe used a placeholder model and does not establish provider access or model support.
- Provider failure retains stderr and events without a candidate correctness grade. Execution timeout and signal cancellation stop the process group, including its child, and retain the receipt. A validation timeout retains partial output.

The existing catalog validator, 8 installer tests, 31 workflow-helper tests and `git diff --check` also passed.

## Limits

The adapter was exercised through a fake CLI, not a successful native Codex model turn. The preceding investigation observed HTTP CONNECT 403 from this environment's proxy at the authenticated Codex model endpoint. No model catalog was available locally to confirm a native model choice. Native completion, provider-specific usage semantics, macOS, WSL, Claude Code and T3 routing remain unassessed for this change.

Before using these tools to claim a workflow improvement, complete a native pilot on a supported host, inspect its prompt, source state, raw events and grade, then run repeated matched cases and clean controls. The runner bounds CLI wall time; it does not enforce token/tool budgets or isolate ambient global guidance. Review findings and engineering-quality judgments still require an assessor.
