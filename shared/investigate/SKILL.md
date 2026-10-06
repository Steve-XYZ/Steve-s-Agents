---
name: investigate
description: Use when asked how something in a codebase or system works, why it was built that way, what a request or change would require, or whether a proposal, report, or assumption holds, when nothing is known to be broken and no edit was requested.
---

# Investigate

Answer the question with cited evidence. Change nothing.

1. Restate the question in one line and say what would answer it. Treat any theory in the request as one hypothesis among others.
2. Read the root and applicable nested instructions, then trace the real path: entry point, owner, data, side effects, configuration per environment or tenant, and consumers in other repositories.
3. Prefer an observation when it is cheap and read-only: run the test, call the read-only endpoint, query the local database, read the logs. Never write to shared systems or external services.
4. For history, use `git log -S`, `git log -G`, `git log -L`, and the commit and pull request messages. Report the reason only when a source states it; otherwise label it inferred.
5. Stop when the question is answered. Name what remains unknown and the cheapest observation that would settle it.

Label every claim with its evidence: a `file:line`, a command and its output, or `inferred`. A search that finds nothing counts as evidence when its query and scope are stated.

When the answer shows something broken, report it; use `diagnosing-bugs` only if the user asks to diagnose or fix it. When the answer leaves a product or design decision open, say so and point to `shape-feature`.

Answer first, then the evidence, then the unknowns. When preparing the final answer, reuse `unslop`, loading it only if absent.
