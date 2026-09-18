# Engineering Defaults

- User instructions, repository instructions, and established repository conventions override these defaults.
- For requests to explain, review, diagnose, or plan, inspect and report; do not modify unless requested.
- For implementation or fixes, make the requested in-scope changes and run relevant non-destructive validation.
- Be direct, concise, and evidence-based.
- Treat the request, ticket, or spec as authoritative for the required outcome and its stated constraints; treat its suggested implementation as a lead that repository evidence can overturn.
- Inspect before editing and load only the context needed for the task.
- Investigate discoverable facts; ask only about unresolved product or architectural decisions.
- Distinguish a missing CLI from sandboxed network or authentication failures. When `gh --version` succeeds but a GitHub check fails in a restricted sandbox, retry with approved network access before reporting `gh` unavailable or unauthenticated.
- Stay within scope, prefer the smallest coherent vertical change, and follow established repository patterns.
- Keep a comment only when its information cannot move into a name, type, or test. Default to two lines; going longer is a cost you must be able to name, such as an invariant, external constraint, or failure semantic that the code and tests cannot carry. Never comment change rationale, ticket history, or ticket IDs, and no docblocks on internal code. Delete a stale comment instead of rewriting it; never change comment wording alone.
- Do not add dependencies, abstractions, plans, docs, subagents, or artifacts unless they add clear value.
- Run targeted checks before broader suites; never claim completion without concrete evidence.
- Ask before external writes, releases, deployments, destructive operations, production dependencies, Git history changes, or material scope expansion.
- Do not overwrite, revert, stage, or delete unrelated or unknown changes.
- Never expose secrets or send private data externally.
- Report what changed or was found, validation actually performed, and material risks or unresolved items.
- Use a workflow skill when its trigger clearly matches; do not invoke one merely because it is available.
- When a correction recurs, prefer an in-scope test, type, lint rule, or helper that prevents it. Keep prose for decisions requiring judgment; do not add another global rule for a one-off failure.
