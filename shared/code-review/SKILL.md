---
name: code-review
description: Ticket-grounded code review workflow. Use when reviewing pull requests, diffs, commits, review threads, or ticket implementations, especially when the user asks for a review, PR review, code review, regression check, or whether a change satisfies a Linear/GitHub ticket.
---

# Code Review

## Workflow

1. Understand the ticket first: read the ticket, expected behavior, QA evidence, linked PRs, and user context before judging code.
2. Map the PR scope: check branch, base, commits, changed files, and whether the diff matches the ticket without scope creep or missing pieces.
3. Read the code seriously: open surrounding files, follow call chains, and verify end-to-end wiring instead of relying only on the diff or PR title.
4. Verify objectively: run the narrowest relevant build/test/format checks when practical; explain exact commands and failures if validation cannot complete.
5. Classify by severity: lead with findings ordered by impact.
6. Write actionable review feedback: include file/line, why it matters, and a concrete fix or validation path.

## What to Check

- Correctness: ticket fit, edge cases, idempotency, concurrency, null/error paths, and end-to-end wiring.
- Security: authorization, input validation, secrets, provider errors, sensitive data in URLs/logs/responses, and rate limiting when relevant.
- Data: migrations, snapshots, indexes, destructive updates, cache behavior, report/export alignment, and provider-specific SQL behavior.
- Consistency: existing architecture, naming, ownership boundaries, API contracts, UI/backend payload alignment, and test coverage.
- Build health: merge breakage, SDK/runtime mismatch, failing focused tests, and unrelated failures that must be called out separately.

## Output Shape

Start with a one-line verdict: approve, comment, or request changes.

Then list findings first, ordered by severity:

- Blocker: cannot merge because it fails to build, breaks required behavior, creates a security issue, or corrupts data.
- Should fix: likely bug, incomplete implementation, risky assumption, or missing validation.
- Nit/follow-up: optional cleanup or non-blocking improvement.

For each finding, include:

- `file:line`
- Problem
- Impact
- Suggested fix

Call out what looks correct only when it reduces ambiguity or clearly separates reviewed, safe areas from the findings; do not produce routine positive summaries. End with validation performed, open questions, and final verdict.


## Review Boundaries

- Do not turn a review into a refactoring exercise.
- Report only evidence-backed defects, regressions, security risks, broken requirements, or repository-standard violations. A repository-standard violation counts only when backed by concrete, local evidence: surrounding code, repo documentation, configuration, tests, ADRs, conventions already applied in the codebase, or ticket requirements. Do not turn personal preferences, external patterns, or generic recommendations into blocking findings.
- Do not request architectural rewrites when the current implementation is correct and within the ticket scope.
- Put optional design improvements, cleanup opportunities, and broader architectural ideas under `Nit/follow-up` unless they create a concrete correctness, security, operability, or maintainability risk.
- Distinguish clearly between a proven issue, a plausible risk that needs validation, and a personal preference.


## Rule

Do not assume; verify. Read the ticket, follow the code, run what is practical, and report only evidence-backed findings.
