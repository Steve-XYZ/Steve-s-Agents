# Explicit Merge Danger ratings

The requested change is an explicit qualitative evaluation in the existing Merge Danger section: Low, Medium, or High, with a separate “Do not merge” hold for a known Blocker or unmet required merge gate. The user selected these labels instead of a score out of ten. The existing comment policy, review verdicts and severities, phase skills, and publication boundaries remain in force.

## Baseline and smallest change

The baseline is main at `abad57af71d398f34f732b3b48a873579bb1593a`. Its `engineering-writing` skill required consequences and recovery information but said “do not invent a risk rating or guarantee.” It had no required rating slot or rubric. Five fresh baseline contexts produced 50 complete PR-description/review-summary footers with consequences and recovery narratives, but none supplied an explicit rating. These outputs followed the old guidance; they demonstrate the missing requested behavior rather than a failure to follow it.

Only that skill's existing Merge Danger section changes. It now requires an evidence-backed label and reason, with `Risk: Unassessed` when missing impact or recovery evidence prevents a supported rating. High does not automatically block a merge; Low does not waive a required gate. The writing step preserves the calling workflow's verdict and classifications. Individual inline comments and replies retain their existing severity and disposition without a separate rating or footer.

There is no new skill, agent definition, phase, global instruction, model setting, or installation change. The skill description and triggers are unchanged. The evaluated body grows from 476 to 731 words, below the 1,200-word limit. Evaluation fixtures and manual-assessment support accompany the guidance change.

## Method and evidence

Five fresh contexts per variant drafted the same captured engineering records: one PR description and one full review summary for each of five cases, plus one inline Blocker and one reply. Expected labels, assessment code, and author conclusions were kept outside these contexts. The baseline ran before editing the guidance; the candidate used the frozen changed catalog. Two additional records were held out while writing the rule and run once against the candidate. One completed candidate context then wrote an internal operational handoff to check the artifact boundary.

| Record | Supplied facts that matter | Expected candidate behavior |
| --- | --- | --- |
| Help text | Only a CLI help string changes; exact-output check and required gates pass; simple revert | Low; no hold |
| Tenant preference | Two views consume a saved tenant setting; behavior and rollback checks pass; bounded effect | Medium; no hold |
| Audit retention | Authorized deletion of millions of rows across tenants; archive and full restore exercised; all required gates pass | High; no automatic hold; retain Approve |
| Approval month | Current-head reproduction writes approvals into the wrong month; correction unverified; green suite misses it | High; Do not merge; retain Request changes and all severity counts |
| Maintenance | Only file names and a successful compile; impact/recovery evidence missing; required assessment gate unmet | Unassessed; Do not merge; retain Comment and the Should fix classification |
| Documentation link, holdout | No runtime/data effect; changed link returns 404; required link check fails | Low; Do not merge; retain Comment |
| Duplicated sort policy, holdout | Bounded preference behavior correct; all gates pass; nonblocking Should fix remains | Medium; no hold merely for Should fix; retain Comment |

The parent inspected the resulting drafts against these records, including reasons, recovery limits, verdicts, counts, and inline/reply content. This semantic assessment was not blind to the variant. [Raw runs](merge-danger-rating/runs.json) retain prompts, all drafts, response text, agent-reported activity, preparation receipts, and source-preservation grades. The [inventory](merge-danger-rating/inventory.json) extracts footer labels, holds, and leading lines for inspection; it is not a correctness oracle. The [manifest](merge-danger-rating/manifest.json) pins both skill hashes and records measurement gaps.

These were explicit invocations in native collaboration contexts, using `fork_turns=none`, the inherited parent model, and no inner delegation or model overrides. Exact model identity, reasoning effort, host version, and attributable usage were not exposed. Activity files are agent reports, not independently exported tool transcripts. Preparation used the existing runner's `--prepare-only` path; receipts correctly remain `execution.status=prepared`. Native context completion is evidenced separately by the retained drafts and responses, not by a claimed Codex CLI completion. This does not test automatic host routing, an end-to-end delivery/review, or the applications described by the supplied records.

## Results and tradeoffs

| Dimension | Baseline, five contexts | Candidate, five contexts |
| --- | --- | --- |
| Explicit risk evaluation in full artifacts | 0/50 rated; 50/50 retain consequence/recovery footers | 50/50 use the expected rating with evidence and recovery limits |
| Required holds | Blocker/gate information remains in the narratives; no standardized hold slot | 20/20 blocked artifacts say Do not merge and name the clearing condition |
| False holds | No newly imposed holds observed | 0/30 nonblocked artifacts, including 10 High/Approve artifacts |
| Review verdicts and counts | 25/25 preserved | 25/25 preserved, including Comment with a gate hold |
| Individual inline comments and replies | 10/10 retain their severity/disposition without a footer | 10/10 retain severity/disposition without a separate rating or footer |
| Source edits or corrective intervention | None | None |
| Median draft words per context, all 12 artifacts | 1,243 | 1,386 |

All four holdout drafts used the expected rating/hold combination and preserved their supplied verdicts. The internal continuation produced no Merge Danger section or formal rating slot. It did retain the missing assessment and the factual warning against merging before the required gate clears; preserving that safety information is appropriate in an internal handoff.

The observed cost is more guidance and longer drafts: the candidate median is about 11.5% more words. Output words are not tokens or a dollar-cost estimate. Active elapsed time, model/tool usage, and dollar cost are unavailable, so this record supports no efficiency claim. There were 11 fresh contexts and one planned continuation, with no repair prompts or manual edits to their drafts.

Retain the focused change: the baseline demonstrates the missing evaluation, and the candidate supplies it without the tested verdict changes, false holds, or artifact-boundary spillover. This small captured dataset does not establish general risk calibration. Arm order was not randomized, there was no separate no-guidance arm, the two holdout records ran only once, and the assessor knew the variant. Actual routing, production judgments, and cost remain unassessed.

## Reproduction and deterministic checks

Prepare the same task using either pinned guidance checkout, outside Git worktrees, then supply only its generated prompt to a fresh context:

```sh
python3 evals/run-task.py merge-danger \
  --guidance-root /path/to/pinned/catalog \
  --task-dir /tmp/release-drafts \
  --record-dir /tmp/writing-records/drafts --prepare-only
python3 evals/grade-task.py --record-dir /tmp/writing-records/drafts
```

Use separate fresh directories per run; substitute `merge-danger-controls` for the holdout records. Assess `drafts.json` manually against the engineering records and table above. The source grader returns `manual_required`, not a correctness pass based on rating words. The new harness test proves that even an unsupported “Low. All checks pass.” draft needs manual assessment and that editing supplied records fails the read-only check. Removing these fixtures from read-only handling made that test fail; adding the handling made it pass.

Local checks passed: skill validation, 8 installer tests, 31 workflow-helper tests, 31 evaluation-harness tests, and `git diff --check`. These checks cover catalog structure and harness behavior; the fresh-context drafts supply the writing-behavior evidence.

A [fresh-context independent review](merge-danger-rating/review.json) of `878dab25602163f604b7c9fad03f8721ca69fcc8` found no Blocker or Should fix findings. The reviewer inspected all 124 drafts and the internal continuation, checked evidence integrity, and independently ran the focused harness test and its failing negative control. Its single provenance nit was normalized afterward: the inventory now calls `release-notes-116` “holdout,” matching the raw runs. That correction and this review record do not change the evaluated guidance or drafts.

After evaluation, one sentence of the skill was reworded for clarity. "Choose the highest level supported by the workflow's evidence" could be read as requiring proof before rating High. It now says to base the rating on the evidence and to use the more severe level when factors disagree. The manifest's candidate hash and word count describe the evaluated text, not this rewording, and no drafts were rerun against it.

A subsequent GPT 6.1 Sol review with high reasoning at `7339e3b2e62037b5bca8e4b80e22142d6dcd8b09` found no Blocker or Should fix findings and one wording nit: keeping all “merge holds” out of replies could conflict with preserving a supplied blocking disposition. No captured draft demonstrated that suppression. The final sentence now prohibits adding a separate rating, hold, or footer while expressly preserving existing blocking conditions. Skill validation and `git diff --check` passed after this correction. This is an inspected clarification of the existing preservation contract; no drafts were rerun against it, and the original comparison does not establish its behavioral effect.
