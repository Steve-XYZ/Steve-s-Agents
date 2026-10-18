# Explicit Merge Danger ratings

The requested change is an explicit qualitative evaluation in the existing Merge Danger section: Low, Medium, or High, with a separate “Do not merge” hold for a known Blocker or unmet required merge gate. The user selected these labels instead of a score out of ten. The existing comment policy, review verdicts and severities, phase skills, and publication boundaries remain in force.

## Baseline and smallest change

The baseline is main at `abad57af71d398f34f732b3b48a873579bb1593a`. Its `engineering-writing` skill required consequences and recovery information but said “do not invent a risk rating or guarantee.” It had no required rating slot or rubric. Five fresh baseline contexts produced 50 complete PR-description/review-summary footers with consequences and recovery narratives, but none supplied an explicit rating. These outputs followed the old guidance; they demonstrate the missing requested behavior rather than a failure to follow it.

The change stays in the existing writing skill. It now requires an evidence-backed label and reason, with `Risk: Unassessed` when missing impact or recovery evidence prevents a supported rating. High does not automatically block a merge; Low does not waive a required gate. The writing step preserves the calling workflow's verdict and classifications. Individual inline comments and replies retain their existing severity and disposition without a separate rating or footer.

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

CodeRabbit later noted that the combined delivery-with-PR and review-with-GitHub-draft routing expectations still checked only footer placement. Both now also require the evidence-backed rating and conditional merge hold. This aligns their manual acceptance criteria with the writing skill; the combined routes remain unassessed in a live host.

## Delivery follow-up on the Unassessed rate

The comparison above supplied curated records that already stated impact and recovery. A reviewer asked whether real delivery work gives the writing step enough evidence, or whether it produces frequent `Risk: Unassessed` footers or invented recovery facts instead.

Nine fresh contexts each ran one existing `deliver-ticket` fixture with guidance pinned at `7339e3b2e62037b5bca8e4b80e22142d6dcd8b09`. That snapshot includes the rating-selection rewording but predates the reply clarification in `4a38f77`, which does not touch PR descriptions. Each task was prepared with `run-task.py --prepare-only`, and one sentence was appended to the generated prompt: "Also draft the GitHub PR description for this change in <task>/PR.md. Do not publish it." Nothing else in the prompt mentioned Merge Danger, ratings, or expected outcomes.

| Fixture | Runs | Change | Rating | Do not merge |
| --- | --- | --- | --- | --- |
| `simple` | 3 | One CLI help string | Low, 3/3 | 0/3 |
| `parcel` | 3 | Tier comparison `<` to `<=`; lowers boundary prices and accepts 5000 g parcels | Medium, 3/3 | 0/3 |
| `workspace` | 3 | Withdrawal state across three repositories with legacy stored flags | High, 3/3 | 3/3, pending independent review and contract decisions |

No draft used `Risk: Unassessed`. The assessor checked each recovery statement against the fixture contract and the agent's own diff and found no invented rollback test, flag, backup, or deployment fact. All three `workspace` drafts identified a recovery limit that `CONTRACT.md` does not state: once rows carry `withdrawal_state`, reverted code ignores it and re-opens withdrawal for review or disabled rows whose legacy flag is still true. The one loose inference is a `workspace` draft calling the repositories "separately deployed services"; the fixture says "independent repositories."

In delivery, the writer made the change itself, so impact is known, and for code-only changes "reverting restores it" follows from the diff. This run therefore shows that the rule adds no Unassessed noise to ordinary delivery. It does not show how the rule behaves when a change depends on deployment, migration, or provider state the agent cannot see.

Two observations bear on the rubric rather than this rule's form:

- All three `parcel` drafts rated a customer price change Medium without discussing the High row's "money." Medium is defensible because prices fall to the published rate card at boundary weights and a revert works, but the rubric text and the agents' reading differ.
- All three `parcel` drafts state in the body that no independent review has happened, and two agents' reports say the change should not merge without one. None adds `Do not merge`, because each was unsure whether `deliver-ticket`'s money-movement review rule covers price calculation. That is consistent with "unmet required merge gate"; the ambiguity sits in `deliver-ticket`.

Limits: one model, nine samples across three fixtures, explicit invocation rather than host routing, and an assessor who knew the expected ratings. No baseline arm ran, because the baseline guidance forbids a rating. The runs used the host's subagent facility; an attempt to launch separate CLI processes was blocked by the host's permission policy. Subagent context therefore included this catalog's root `AGENTS.md`, which mentions trials, and organization-level instructions. Transcripts show no reads of receipts, notes, or `evals/`. The `code-review` path, where the writer works from another author's evidence, remains untested and is the likelier source of Unassessed footers or invented facts.

[Delivery runs](merge-danger-rating/delivery-runs.json) retain each prompt, receipt hashes, full PR draft, extracted Merge Danger section, diff against the imported fixture, and host-reported subagent tokens, duration, and tool-use counts. Exact model identity and dollar cost were not exposed.

## Financial scope and approval-gate follow-up

The three parcel drafts support Medium for that bounded quote correction. Their diffs change a pure integer-returning function to match the published rate card, not a payment, refund, or balance mutation. Each draft also retains the limit that reverting quote code cannot undo charges an external consumer may already have made. The author decision is to narrow the High row's financial example to “money movement (payments, refunds, or balance mutations).” This makes the intended scope explicit; it does not make every price change Medium. Material effects on shared consumers, stored data, or difficult recovery still support High under the other criteria.

The opening now accurately states that this skill derives the Merge Danger risk rating from caller evidence. The caller retains facts, findings, finding severity, evidence, verdict, and required merge gates. This corrects the description of the skill's responsibility without giving it authority to invent facts or change a review verdict.

Before editing those two passages, five fresh contexts used the current catalog at `d3920e52045fac8b359abc85094e61be6b019605`. Five more used the clarified catalog. Each drafted a PR description and full review summary for four raw records in `merge-danger-boundaries`, with no expected ratings or assessor conclusions in context. Unlike the earlier delivery trial, these writing records explicitly state the required gate outcomes; they cannot settle which reviews real pricing work requires.

| Captured record | Before clarification, 10 artifacts | After clarification, 10 artifacts |
| --- | --- | --- |
| Bounded parcel quote correction; no payment, refund, or balance mutation in the inspected repository | Medium; no hold | Medium; no hold |
| Refund worker with lasting provider transactions and balance mutations; required gates complete | High; no hold | High; no hold |
| Documentation spelling correction; supplied Approve verdict; separate required owner sign-off missing | Low; Do not merge | Low; Do not merge |
| Same documentation impact; all required gates complete | Low; no hold | Low; no hold |

The parent inspected all 80 drafts, unblinded. Both variants preserve the external-consumer and recovery limits, all 20 supplied review verdicts and zero-finding counts per variant, and the named owner gate. All five owner-gated summaries in the existing-guidance arm already explain that code-review approval and the separate owner sign-off are different. The clarified catalog preserves that distinction in all five. No additional Approve/hold instruction was added: the control already behaved. An Approve verdict remains the review disposition; it does not clear an independently required sign-off.

There were no repair prompts, draft edits, or false holds in the 30 nonblocked artifacts per variant. All ten source-preservation checks passed, while semantic grades remain `manual_required`. [Boundary runs](merge-danger-rating/boundary-runs.json) retain the raw records, prompts, drafts, agent-reported activity, preparation receipts, grades, both skill hashes, and mechanical inventory. The catalog body grows from 750 to 772 words. Median output length is 1,015 words before and 993 after for eight drafts per context; words are not usage or cost. Native model identity, effort, active elapsed time, and attributable cost remain unreported. Receipts are prepare-only, not native CLI completion records. The arms ran in order with no separate no-guidance arm or blind assessor; these supplied-record tasks do not exercise application behavior or host routing.

The unchanged outputs support preserving the chosen interpretation, not a measured improvement in rating accuracy. The reasons to retain these edits are precise financial scope and an accurate ownership statement. Existing results moved under `2026-10-18` to follow the repository convention; current links move with them, while historical review records retain the paths and commits they originally reviewed.

### Open follow-up: pricing and independent review

`deliver-ticket`'s independent-review rule requires review for material money movement, but does not explicitly classify pricing calculations. This predates the Merge Danger rating rule. Keep that phase-policy decision outside this PR, as requested. A follow-up should decide when pure quotes and downstream billing calculations require review, then replay the parcel task with explicit required-review and optional-review policies, plus a payment/refund control. A known missing required review must produce a hold; an optional review must not be invented as a gate. Neither the Medium label nor this record settles that policy question.
