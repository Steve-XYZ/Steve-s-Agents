# Reuse evidence and scope fix rounds

For a handoff or repeated review, retain one local review record outside the worktree. Record the requirement pointer, base SHA, reviewed head SHA, findings with status and evidence pointers, and validation actually executed. Do not copy the entire conversation or generate a second implementation plan.

The repository's `scripts/review-package.py` freezes a committed comparison:

```sh
python3 /path/to/Steve-s-Agents/scripts/review-package.py --repo /path/to/project --base <base-sha> --head <head-sha>
```

Use the PR merge base for its initial diff, or the previous reviewed head for a fix round. The command prints a new temporary directory containing `review.json`, `diff.patch`, and `stat.txt`. It refuses tracked dirty state and excludes untracked files. It does not fetch refs, run tests, or prove correctness. Add requirement and finding pointers to the record. Keep private diffs local; review before any authorized upload.

Do not commit merely to satisfy this helper when commits are not authorized. Use a reviewed local snapshot or another supported read-only comparison and state exactly which files it includes. Never describe a commit-only package as covering uncommitted work.

Append validation records only for commands actually run: command/filter, commit or exact working-tree state, relevant environment/fixture, exit status, observed behavior, and an output-file pointer. If the tested state is unclear, the record does not establish coverage of the current head.

To freeze existing output with the package, pass `--evidence /path/to/evidence.json`. The file is a JSON list with `claim`, `command`, `environment`, `observed`, `artifact`, `tree_sha` as nonempty strings and `exit_code` as an integer. Resolve `tree_sha` from the exact tested commit with `git rev-parse '<tested-sha>^{tree}'`. An optional `head_sha` must be a full commit SHA with that tree. Artifact paths are relative to the evidence file or absolute.

The helper rejects mismatched trees and missing outputs, copies output bytes, and records their SHA-256 hashes. It preserves failing exit codes. It verifies identity and packaging, not whether the command ran, the environment was correct, or the assertion proves the claim. Older valid evidence for unaffected behavior can remain separately referenced with its scope; do not relabel it as current-tree evidence.

Read existing evidence before rerunning it. Reuse it when the tested state and environment cover the current code and behavior. A fix invalidates affected evidence; rerun those checks. A missing output is an evidence gap to resolve, not proof that the check failed. Run another focused check when a concrete doubt remains. Repository-required gates still apply.

On a fix round, verdict every unresolved finding and inspect the fix diff for new breakage. Expand to callers or unchanged code when a changed contract, invariant, or other named risk requires it. Without a usable prior review, perform an initial review. A user-requested full review or required final merge review still covers the whole change. Never downgrade a material risk merely because it sits outside the fix diff; record its relation to this change and the necessary follow-up.

Stop when owned findings are addressed and the fix introduces no material defect. Unchanged findings get evidence or a decision, not another identical review loop. This record does not replace independent current-head approval.

For a live PR, `scripts/pr-state.py --repo <owner/repo> --pr <number> --expected-head <sha>` uses read-only GitHub CLI calls. It checks PR identity before and after collecting check results. `STALE` discards the check list; `UNAVAILABLE` means the snapshot could not be established. Both exit 2. Exit 0 means observed, not passed.

Conditions can coexist: draft, requested changes or review, failed/pending/cancelled/skipped checks, no checks, or observed checks passed. The helper inspects all reported checks, not the complete required-check policy. It does not certify current-head approval, thread resolution, or merge readiness. Do not poll a human gate as if it were running CI. Missing checks and skipped checks are not a demonstrated pass. Recheck current identity before any authorized external action.
