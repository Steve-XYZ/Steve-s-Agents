# Triaging an Escaped Finding

This file is for humans reviewing how the workflow performed. It is not agent
guidance and is not installed anywhere.

Its purpose is to turn "the agent missed something again" into a verdict about
one stage, so the fix lands on that stage instead of on the whole workflow.

## The metric that matters

Count **external escaped blockers per pull request**: real defects that the
internal pipeline declared ready and that a human reviewer found afterwards.
The goal is to move blockers from the human reviewer into the pipeline, not to
raise the total number of findings.

Track alongside it:

- internal true findings raised before the pull request,
- internal false positives,
- review rounds needed,
- wall-clock and token cost,
- defects found after merge.

A rise in internal findings with no fall in escaped blockers means the pipeline
got noisier, not better.

## Classifying one escaped finding

Ask the questions in order and stop at the first "no".

| Question | If no |
| --- | --- |
| Was the affected surface listed in the change-surface scan? | **Discovery failure** — enumeration missed it |
| Was the risk named during judgment? | **Judgment failure** — the surface was known, the risk was not drawn |
| Did the implementation address the named risk? | **Execution failure** |
| Would the executed validation have caught it? | **Evidence failure** — validated the implementation, not the claim |
| Did the critic reconstruct that surface? | **Review failure** — the critic's reconstruction did not reach it |
| Did the critic raise it and the fix dismiss it? | **Adjudication failure** — a demonstrated finding was argued away |

Each verdict points at one stage, which is the point of recording the scan as
an artifact: without it, discovery failures and judgment failures are
indistinguishable after the fact.

## What each verdict changes

- Discovery: extend the enumeration recipe, or move the scan to a fresh context for that class of change.
- Judgment: the gap is in `engineering-judgment`, not in discovery.
- Execution: usually scope or pattern adherence, not process.
- Evidence: the validation proved the edit rather than the requirement.
- Review: the critic's inputs or reconstruction scope, not its independence. Check whether it received the scan and the diff it needed.
- Adjudication: the builder overrode a demonstrated finding. The weakest link in the chain, because it converts a working review into a discarded one.
