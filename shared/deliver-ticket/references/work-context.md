# Work context and continuity

Use this when work spans sessions, a handoff would otherwise lose decisions, or exploration has filled the context with discarded approaches. Small tickets need no work note.

## Preserve only what the next step needs

Keep one durable note in the repository's established task location, or a local location outside the worktree. Report its path before ending a session. Do not silently add a tracked plan or put private task details in a public repository.

Record the outcome and constraints separately from the tentative approach, completed slices and their commit/evidence pointers, important decisions and rejected hypotheses, current unknowns, and the next slice or experiment. Update at useful checkpoints, not after every tool call. Remove superseded pending work.

On resumption, inspect the current checkout and evidence before trusting the note. Preserve a verified checkpoint before interruptions or context resets; do not assume a transcript will survive.

## Separate contexts for a reason

Keep one implementer across coupled slices. Separate planning from implementation when exploration is large, abandoned approaches dominate the history, or another session will own implementation. Hand over decisions, alternatives, evidence, unknowns, and a detailed next slice. Later steps remain provisional.

A planning-only request grants no implementation authority. Use read-only tools where the host supports enforcement. Run a disposable experiment only within the request's authorization; a role prompt alone does not restrict tool permissions.

For independent review, use a fresh context with the raw requirement and exact code/evidence. Do not forward the author's reasoning history or tell the reviewer which findings to reach. Same-model fresh review reduces shared narrative bias, not every correlated mistake.

## Isolate only when needed

Delegate bounded independent questions or implementation units whose handoff is cheaper than shared context. Before concurrent writes, assign ownership and account for shared lockfiles, generated files, schemas, branches, ports, databases, queues, and caches.

A worktree isolates checked-out files, HEAD, and index. It does not isolate all Git refs or runtime resources. Use it for competing edits, historical reproduction, or experiments that could disturb active work. Do not require it for every ticket.

Have one integrator inspect and verify the combined change. Worker reports alone do not prove integration. Respect the host's delegation permissions; lack of subagents does not justify pretending contexts are independent.
