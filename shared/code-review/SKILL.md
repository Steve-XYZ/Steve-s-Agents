---
name: code-review
description: Review a pull request, diff, commit, review thread, or ticket implementation against its stated requirements and repository evidence. Use when the user asks for a PR review, code review, regression review, or confirmation that a change satisfies a ticket. Do not use as an automatic delivery self-review, to implement changes, or to diagnose an unknown failure.
---

# Code Review

Review the exact change the user placed in scope. Inspect and report; do not modify code, publish comments, approve, or request changes externally unless explicitly requested.

## 1. Establish authority

Read the ticket, specification, user context, linked evidence, and existing review threads before judging the implementation. If no formal requirement exists, state the behavior being used as the review baseline.

For a live PR, verify repository, base branch, head branch, head SHA, commits, and changed files. Review the latest head rather than relying on the title or an earlier snapshot.

If the user supplied an expected head SHA and the live head differs, stop and report the mismatch unless the user explicitly asked to review the latest head.

## 2. Map the change

Start with:

1. ticket or specification,
2. diff and commits,
3. changed tests,
4. surrounding implementation only as needed.

Check whether the scope matches the requirement without missing behavior or unrelated expansion. Follow call paths and end-to-end wiring when the changed behavior depends on code outside the diff.

## 3. Review in passes

### Requirement fidelity

Check acceptance criteria, partial or incorrect behavior, scope creep, and edge cases implied by the requirement.

### Engineering correctness

Check functional correctness, failure behavior, repository architecture, contracts, test quality, and unnecessary complexity.

### Conditional risk

Only when relevant, inspect authorization, sensitive data, money calculations, idempotency, concurrency, shared contracts, migrations and rollback, destructive data changes, external providers, and performance.

## 4. Verify

Run the narrowest reliable build, test, lint, format, migration, or runtime checks that can prove or disprove material findings. Distinguish changed-code failures from unrelated environment or baseline failures.

Never present unexecuted validation as completed evidence.

## 5. Report findings

Start with a one-line verdict: approve, comment, or request changes. List findings first, ordered by severity:

- Blocker: cannot merge because of a demonstrated build failure, required-behavior defect, security exposure, or data risk.
- Should fix: likely defect, incomplete behavior, unsafe assumption, or material missing validation.
- Nit/follow-up: optional cleanup or non-blocking improvement.

For every finding include:

- `file:line`,
- concrete evidence and problem,
- impact,
- recommended correction or validation path.

Report only evidence-backed defects, regressions, risks, broken requirements, or repository-rule violations. Distinguish proven defects from plausible risks needing validation. Do not report cosmetic preferences unless they violate an explicit local rule.

If no findings remain, say so directly and identify any validation gap or residual risk. End with validation performed and the final verdict.

When explicitly asked to publish a live PR review, confirm the head SHA has not changed immediately before posting and follow repository-specific language and formatting rules.
