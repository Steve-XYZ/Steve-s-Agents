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

Partition the diff into behavioral clusters, then check whether the scope matches the requirement without missing behavior or unrelated expansion. Follow call paths and end-to-end wiring when the changed behavior depends on code outside the diff. If independent clusters make the review too broad to cover with confidence, identify the uncovered cluster and recommend a split rather than implying complete coverage.

## 3. Review in passes

### Requirement fidelity

Check acceptance criteria, partial or incorrect behavior, scope creep, and edge cases implied by the requirement.

### Engineering correctness

Check functional correctness, failure behavior, repository architecture, contracts, test quality, and unnecessary complexity.

### Conditional risk

Only when relevant, inspect authorization, sensitive data, money calculations, idempotency, concurrency, shared contracts, migrations and rollback, destructive data changes, external providers, and performance.

When the change touches money or durable state, a shared flag, status, predicate, or contract, migrations, provider effects, concurrency, retries, partial failure, or several behavioral clusters, read [adversarial review](references/adversarial-review.md) and apply only its relevant lanes.

## 4. Verify

For repeated rounds or a review handoff, read [review evidence](references/review-evidence.md). Reuse traceable validation that covers the code being reviewed; run new checks for changed behavior or a concrete unresolved doubt. A claimed result without accessible evidence is not a passed check.

Run the narrowest reliable build, test, lint, format, migration, or runtime checks that can prove or disprove material findings. Confirm that tests execute the changed branch and would fail for the behavior being challenged. Distinguish changed-code failures from unrelated environment or baseline failures with an exact head/base comparison when that distinction affects the verdict.

Never present unexecuted validation as completed evidence.

## 5. Report findings

Start with a one-line verdict: approve, comment, or request changes. Request changes when a blocker remains, comment when only should-fix findings remain, and approve when only nits or no findings remain unless repository rules require another disposition. List findings first, ordered by severity:

- Blocker: cannot merge because of a demonstrated build failure, required-behavior defect, security exposure, or data risk.
- Should fix: likely defect, incomplete behavior, unsafe assumption, or material missing validation.
- Nit/follow-up: optional cleanup or non-blocking improvement.

Write each finding compactly as `[category] file:line — mechanism; reachable trigger and wrong observable outcome; impact. Fix: correction or validation path.` Keep blocker and should-fix findings visible. Collapse optional nits in a disclosure block when the review surface supports it.

Report only evidence-backed defects, regressions, risks, broken requirements, or repository-rule violations. Distinguish proven defects from plausible risks needing validation. Do not report cosmetic preferences unless they violate an explicit local rule.

Do not repeat a full finding in both the review body and an inline comment. When publishing inline findings, use the body for the verdict, severity counts, validation, and residual risk.

On a repeated review, account for prior findings as fixed, withdrawn, still open, outdated, or newly introduced. Inspect the fix diff, not only the author's responses. Expand for named contract or behavior risks; perform a whole-change pass when requested, required by repository policy, or when the prior review is unavailable.

If no findings remain, say so directly and identify any validation gap or residual risk. End with validation performed and the final verdict.

When explicitly asked to publish a live PR review, confirm the head SHA has not changed immediately before posting and follow repository-specific language and formatting rules.
