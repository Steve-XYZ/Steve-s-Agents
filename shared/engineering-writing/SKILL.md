---
name: engineering-writing
description: Use when drafting or revising GitHub PR descriptions, full review summaries, inline review comments, or review replies. Do not use for routine responses, progress updates, or internal reports.
---

# Engineering writing

Use `unslop` if it is not already in context; reuse it without rereading. It owns the language rules.

This skill controls presentation. The calling workflow owns the facts, findings, severity, evidence, and verdict. Preserve its classifications and required evidence fields. Never trade technical accuracy or material uncertainty for brevity. Drafting an artifact does not authorize publishing it.

## PR descriptions

Lead with the observable change and why it is needed. Include material design decisions and verification actually performed, including gaps. Scale detail to the change; use headings only when they help scanning.

Do not narrate implementation steps, duplicate the diff, or include agent activity logs. End with Merge Danger.

## Full review summaries

Lead with the verdict and finding counts by severity. Preserve `code-review`'s classifications and order. Include validation performed and material gaps. When inline comments contain the details, summarize their impact instead of repeating the findings verbatim.

End with Merge Danger using the review's independently assessed consequences, not the author's assurance.

## Inline review comments

State the problem, reachable trigger, and observable consequence, retaining the workflow's severity, location, and evidence. Give the correction when it is clear; leave implementation choices open when several fixes are valid. Distinguish demonstrated defects from suspected risks.

Default to one or two sentences; expand when needed to explain the failure. Use a lighter tone for optional suggestions while preserving their classification. Do not add a Merge Danger section.

Weak:

> Could we improve how the selected month is handled here?

Better:

> [Blocker] `admin/Approvals.tsx:84`: Switching months leaves the previous rows available, so approving one submits its amount against the newly selected month. Clear stale rows or bind approval to the row's original period.

## Review replies

Address the finding directly. For accepted findings, state what changed and how it was verified. For rejected findings, give the evidence or contract that disproves the concern. Retain deferred work or missing proof from the workflow's disposition.

Never reply with "Fixed", "Done", or "Addressed" alone. Do not add a Merge Danger section.

## Merge Danger

Place this section last in PR descriptions and full review summaries. Begin with `Risk: Low`, `Risk: Medium`, or `Risk: High`, using the rubric below. Follow the rating with its concrete reason, affected behavior or data, whether reverting restores the previous state, and any recovery requirement or unverified risk.

Base the rating on the workflow's evidence about plausible failure consequences, affected consumers, reversibility, recovery, and material verification gaps. When these point to different levels, use the more severe one. These are qualitative judgments, not probabilities or scores out of ten.

| Rating | Meaning |
| --- | --- |
| Low | Limited consequences and straightforward recovery, with evidence bounding the impact. |
| Medium | Meaningful behavior changes with bounded impact and a practical recovery path. |
| High | Material danger to stored data, security, money, shared consumers, or effects that are difficult to reverse or recover. |

If missing impact or recovery evidence prevents a supported rating, write `Risk: Unassessed` and name the missing evidence. Unknown does not mean Low. Do not invent facts to complete the rubric.

Add `Do not merge` immediately after the rating when a known Blocker or an unmet required merge gate prevents merging. State what must be fixed or verified to clear the hold. Keep the calling workflow's verdict and finding classifications unchanged. High does not automatically mean blocked; Low does not grant approval or waive any gate. A rating never authorizes a merge.

Use a short paragraph for routine changes; expand for material risks. Explain merge consequences and recovery rather than repeating findings. Do not infer safety from diff size, passing tests, or the author's assurance. If reversibility or recovery is unknown, say what remains unverified; do not invent a guarantee. Keep ratings and merge holds out of individual inline comments and review replies, which retain their existing finding severity and disposition.

Weak:

> Merge Danger: Low risk. All tests pass.

Better:

> Risk: Low. Only CLI help wording changes; runtime behavior and stored data are unchanged. The exact-output check passes. Reverting restores the previous wording.

> Risk: High. Do not merge. The migration deletes stored approval records, and its required restore check has not run. Reverting code cannot recover deleted rows. Verify a usable backup and the restore procedure before merging.

Before publishing, check that the action, severity, evidence, and uncertainty remain clear. Remove sentences that add no useful information.
