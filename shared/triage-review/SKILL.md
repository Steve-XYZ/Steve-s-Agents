---
name: triage-review
description: Validate and address incoming review findings, bot findings, or reviewer threads on a change you own. Use when your pull request has been reviewed and you must classify each current finding, implement owned fixes, validate them, and optionally push or respond when explicitly authorized. Do not use to review another author's change or to deliver a ticket with no incoming review.
---

# Triage Review

Treat findings as claims, not facts. Validate each current finding against the requirement, live PR state, and repository evidence before acting. Account for every current finding.

For material delivery work, begin triage in a fresh session of the same harness used for delivery. Reconstruct the behavior from the ticket, current diff, and repository before reading the author's implementation rationale as evidence.

## 1. Establish authority and state

Read the ticket or specification and inspect the live pull request: repository, base, head branch, current head SHA, commits, changed files, and existing review state. Record the initial head SHA.

If the user supplied an expected head SHA and the live head differs, stop and report the mismatch unless the user explicitly authorized working from the latest head.

Before editing, confirm the local checkout corresponds to the PR head and inspect its working-tree state. Do not overwrite unrelated or unknown changes.

Inventory unresolved or current findings from review summaries, inline threads, PR comments, bots, and check annotations. Deduplicate repeated findings and exclude resolved or demonstrably outdated comments. On a later round, include findings raised since the last triaged head plus earlier findings still unresolved.

Maintain a review ledger: fixed, deferred, rejected, still open, outdated, and new. For repeated rounds or a session handoff, read [review evidence](../code-review/references/review-evidence.md). Tie the ledger to the previously reviewed and current head SHAs. Review the fix diff and expand for named risks; the ledger does not replace inspecting code.

## 2. Validate each finding

Judge each finding on evidence, not reviewer seniority or bot confidence. Check:

- **Currentness** — does it still apply to the live head?
- **Requirement and ownership** — is it required by the ticket, introduced, worsened, or newly exposed by this change?
- **Reachability and evidence** — can the described state reach the path through a real caller or supported configuration?
- **Baseline differential** — how does the behavior compare with the base branch?

Reproduce the failure or prove it statically when practical. A preexisting defect is scope evidence, not an automatic dismissal. A claim that remains plausible but unproven needs evidence; it is not automatically accepted or rejected.

## 3. Classify

- **Valid and owned** — fix it here.
- **Valid but unrelated** — defer it only after establishing that this change did not introduce, worsen, or expose it; record the follow-up path.
- **Needs evidence or decision** — state what would settle it instead of guessing at a fix.
- **Incorrect, resolved, or outdated** — reject or acknowledge it with concrete evidence.

Do not implement a change believed to be wrong merely to close a thread.

## 4. Fix what is valid

Apply the smallest coherent change that satisfies each valid, owned finding. Add regression coverage when behavior changed and a reliable test seam exists. Otherwise run the narrowest build, migration, static, or manual check that proves the correction.

When a finding describes a failure class such as starvation, lost progress, duplication, ordering, or idempotency, cover the class rather than only the observed instance. State any boundary not covered.

Do not fix unrelated defects discovered during triage. Review the resulting diff against the ticket and every accepted finding, then run targeted validation.

## 5. Publish safely

Do not push or publish responses unless explicitly authorized.

Immediately before any authorized push or response, refresh the PR and confirm its remote head still matches the expected head or the last head produced by this triage. If someone else changed it, stop and reassess instead of overwriting or responding against stale code. Never force-push or rewrite history without separate authorization.

After an authorized push, confirm the new remote head. Reply to every current finding in its original thread with the classification and evidence: name the fix and validation for accepted findings, or the reason and follow-up path for deferred, evidence-dependent, or rejected findings. Follow repository language and formatting rules.

Do not resolve threads, request re-review, approve, merge, or publish unrelated comments unless explicitly authorized.

Do not describe the pull request as ready while a current `CHANGES_REQUESTED` review or unresolved material thread remains, or before an independent reviewer has approved the current head when repository policy requires it. Author fixes, comments, and validation do not count as independent reapproval.

## 6. Finish

Report per finding: classification, evidence, change if any, and validation executed. State the resulting local and remote head when publication occurred, then list unresolved evidence, deferred follow-ups, and validation not run.
