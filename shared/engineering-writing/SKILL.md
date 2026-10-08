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

Place this section last in PR descriptions and full review summaries. Identify the affected behavior or data, whether reverting restores the previous state, and any recovery requirement or unverified risk.

Use a short paragraph for routine changes; expand for material risks. Explain merge consequences and recovery rather than repeating findings. Do not infer safety from diff size or passing tests. If reversibility or recovery is unknown, say what remains unverified; do not invent a risk rating or guarantee.

Weak:

> Merge Danger: Low risk. All tests pass.

Better:

> Merge Danger: The migration deletes stored approval records. Reverting the code cannot recover them. Recovery needs a usable backup and a tested restore procedure. Neither has been verified.

Before publishing, check that the action, severity, evidence, and uncertainty remain clear. Remove sentences that add no useful information.
