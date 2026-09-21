---
name: code-review
description: Use for requested PR/code reviews or an independent review required by delivery risk or repository policy. Run independent delivery review in a fresh context. Do not use to implement changes or diagnose an unknown failure.
---

# Code Review

Review the exact change the user placed in scope. Inspect and report; do not modify code, publish comments, approve, or request changes externally unless explicitly requested.

For independent delivery review, start in a fresh context with the requirement, exact diff, applicable contracts, evidence, and gaps. Do not import the author's reasoning history. Use read-only tools where enforceable; a role prompt alone does not restrict permissions. If fresh context is unavailable, label the result self-review and report the unmet requirement.

## 1. Establish authority

Read the ticket, specification, user context, linked evidence, and existing review threads before judging the implementation. If no formal requirement exists, state the behavior being used as the review baseline.

For a live PR, verify repository, base branch, head branch, head SHA, commits, and changed files. Review the latest head rather than relying on the title or an earlier snapshot.

If the user supplied an expected head SHA and the live head differs, stop and report the mismatch unless the user explicitly asked to review the latest head.

## 2. Map the change

Before reading the diff, state in one line the observable outcome this change has to produce. Take it from the ticket or specification when one exists, otherwise from the review baseline you named in step 1. Do not take it from the diff's structure or the PR description. Then use repository evidence for actual behavior, constraints, ownership, and affected boundaries. The implementation is evidence about the route taken, not part of the requirement.

Treat the author's rationale as a claim after establishing expected behavior. Seek concrete counterexamples, not a target number of findings.

Start with:

1. ticket or specification,
2. diff and commits,
3. changed tests,
4. surrounding implementation as far as the changed behavior reaches.

Read every changed line. Partition the diff into behavioral clusters, then check whether the scope matches the requirement without missing behavior or unrelated expansion. Follow call paths and end-to-end wiring when the changed behavior depends on code outside the diff. Cover independent clusters in focused passes. If coverage remains incomplete, name the uncovered behavior and withhold a complete verdict; recommend a split when it would make review reliable.

## 3. Review in passes

### Requirement fidelity

Check acceptance criteria, partial or incorrect behavior, scope creep, and edge cases implied by the requirement.

### Engineering correctness

Check functional correctness, failure behavior, repository architecture, contracts, and test quality.

Then ask whether this is the simplest diff that satisfies the requirement, rather than whether the chosen structure is correctly implemented. Name what the change makes removable or leaves stale: code, paths, branches, flags, fields, helpers, abstractions, compatibility shims, duplicated policy, comments, tests, and state. The local comment rule counts here; report a comment that restates the code, narrates the ticket, or has gone stale.

### Conditional risk

Only when relevant, inspect authorization, sensitive data, money calculations, idempotency, concurrency, shared contracts, migrations and rollback, destructive data changes, external providers, and performance.

When the change touches money or durable state, a shared flag, status, predicate, or contract, migrations, provider effects, concurrency, retries, partial failure, or several behavioral clusters, read [adversarial review](references/adversarial-review.md) and apply only its relevant lanes.

## 4. Verify

For repeated rounds or a review handoff, read [review evidence](references/review-evidence.md). Reuse traceable validation that covers the code being reviewed; run new checks for changed behavior or a concrete unresolved doubt. A claimed result without accessible evidence is not a passed check.

Run the narrowest reliable build, test, lint, format, migration, or runtime checks that can prove or disprove material findings. Confirm that tests execute the changed branch and would fail for the behavior being challenged. Distinguish changed-code failures from unrelated environment or baseline failures with an exact head/base comparison when that distinction affects the verdict.

Never present unexecuted validation as completed evidence.

## 5. Report findings

When preparing a PR body, findings, or final report, load `unslop` if it is not already in context and apply it while drafting.

Start with a one-line verdict: approve, comment, or request changes. Request changes when a blocker remains, comment when only should-fix findings remain, and approve when only nits or no findings remain unless repository rules require another disposition. A correct change that leaves avoidable complexity behind is a should-fix, not an approve. List findings first, ordered by severity:

- Blocker: cannot merge because of a demonstrated build failure, required-behavior defect, security exposure, or data risk.
- Should fix: likely defect, incomplete behavior, unsafe assumption, material missing validation, or avoidable complexity the change leaves behind.
- Nit/follow-up: optional cleanup or non-blocking improvement.

Write each finding compactly as `[category] file:line — mechanism; reachable trigger and wrong observable outcome; impact. Fix: correction or validation path.` Keep blocker and should-fix findings visible. Collapse optional nits in a disclosure block when the review surface supports it.

Report only evidence-backed defects, regressions, risks, broken requirements, or repository-rule violations. Distinguish proven defects from plausible risks needing validation. Do not report cosmetic preferences unless they violate an explicit local rule.

Do not repeat a full finding in both the review body and an inline comment. When publishing inline findings, use the body for the verdict, severity counts, validation, and residual risk.

On a repeated review, account for prior findings as fixed, withdrawn, still open, outdated, or newly introduced. Inspect the fix diff, not only the author's responses. Expand for named contract or behavior risks; perform a whole-change pass when requested, required by repository policy, or when the prior review is unavailable.

If no findings remain, say so directly and identify any validation gap or residual risk. End with validation performed and the final verdict.

When explicitly asked to publish a live PR review, confirm the head SHA has not changed immediately before posting and follow repository-specific language and formatting rules.
