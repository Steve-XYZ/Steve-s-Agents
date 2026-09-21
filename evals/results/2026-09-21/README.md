# Explicit-invocation task trials, 21 September 2026

Three fresh subagent contexts received a raw task, a disposable Python repository, and a copy of the changed skill catalog. They did not receive expected outcomes or the parent review conclusions. All three used explicit skill invocation. The task definitions are in [task-fixtures.json](../../task-fixtures.json).

The trial catalog's SHA-256 is `2b591c39717a5568e0d4237d78438ce2c918df2aa6acee36879039e59ded1b6b`. Compute it by sorting the files under `shared`, then hashing each relative path, a NUL byte, its bytes, and another NUL byte. This identifies the guidance tested without implying a comparison against the old workflow.

| Task | Observed final outcome | Evidence |
| --- | --- | --- |
| Simple typo | Only the help string changed. No plan, reviewer, or production expansion. CLI help, empty invocation, and unknown-argument checks were reported; help was independently rerun. | [Patch](simple.patch), [CLI output](simple.log) |
| Authorized slices and invalidated plan | Completed the export change and integer negative/zero cases. Fresh review found an escaped case: -0.5 becomes zero before validation. Reused the existing CSV writer and removed the orphaned serializer; the quantity criterion is not fully met. | [Patch](slices.patch), [9 passing tests](slices.log) |
| Existing-system shaping and continuation | Used the documented JSON-array contract, implemented empty results, and added a regression without requesting another phase approval. | [Patch](shape.patch), [2 passing tests](shape.log) |

The parent reran final checks and independently checked negative-quantity rejection without mutation, zero quantities, CSV escaping, export sorting, unchanged input order, and preserved report order. Those selected checks passed, but were incomplete. A fresh reviewer reconstructed the patches and demonstrated that `set_quantity({"quantity": 2}, -0.5)` mutates the quantity to zero instead of rejecting it. The raw slices patch is preserved as a failed edge case, not relabeled as a complete success. The slice and shaping agents reported observing relevant failures before their fixes. The retained artifacts establish final patches and executed outcomes; they do not preserve the full RED/GREEN tool trajectory.

No agent committed or published fixture changes. The generated Python bytecode was disposable runtime output, not a deliverable. The fixture builder was also run separately and its baseline tests passed.

These are single trials, not an old-versus-new comparison or a productivity benchmark. Harness/model version and attributable token cost were not captured, so no cross-model or cost conclusion is supported. Actual automatic routing, production .NET/provider behavior, the high-risk fresh-review path, and the remaining pressure cases are unassessed here.
