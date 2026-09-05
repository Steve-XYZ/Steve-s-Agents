# Reuse evidence and scope fix rounds

For a handoff or repeated review, retain one local review record outside the
worktree. Record the requirement pointer, base SHA, reviewed head SHA, findings
with status and evidence pointers, and validation actually executed. Do not copy
the entire conversation or generate a second implementation plan.

The repository's `scripts/review-package.py` freezes a committed comparison:

```sh
python3 /path/to/Steve-s-Agents/scripts/review-package.py --repo /path/to/project --base <base-sha> --head <head-sha>
```

Use the PR merge base for its initial diff, or the previous reviewed head for a
fix round. The command prints a new temporary directory containing `review.json`,
`diff.patch`, and `stat.txt`. It does not fetch refs, run tests, include uncommitted
work, or prove correctness. Add requirement and finding pointers to the record.
Keep private diffs local; review before any authorized upload.

Append validation records only for commands actually run: command/filter, commit
or exact working-tree state, relevant environment/fixture, exit status, observed
behavior, and an output-file pointer. If the tested state is unclear, the record
does not establish coverage of the current head.

Read existing evidence before rerunning it. Reuse it when the tested state and
environment cover the current code and behavior. A fix invalidates affected
evidence; rerun those checks. A missing output is an evidence gap to resolve,
not proof that the check failed. Run another focused check when a concrete doubt
remains. Repository-required gates still apply.

On a fix round, verdict every unresolved finding and inspect the fix diff for new
breakage. Expand to callers or unchanged code when a changed contract, invariant,
or other named risk requires it. Without a usable prior review, perform an initial
review. A user-requested full review or required final merge review still covers
the whole change. Never downgrade a material risk merely because it sits outside
the fix diff; record its relation to this change and the necessary follow-up.

Stop when owned findings are addressed and the fix introduces no material defect.
Unchanged findings get evidence or a decision, not another identical review loop.
This record does not replace independent current-head approval.
