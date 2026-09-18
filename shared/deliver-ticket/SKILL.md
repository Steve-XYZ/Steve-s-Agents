---
name: deliver-ticket
description: Use when the user asks to implement, fix, complete, or deliver behavior already defined in a tracker, an accepted feature brief, or the user request itself. Do not use for unclear product requirements, unknown-cause diagnosis, planning-only requests, or pure code review.
---

# Deliver Ticket

The ticket, accepted feature brief, or explicit user request is authoritative for the required outcome, its acceptance criteria, and any constraint it states. Do not rewrite those into another specification.

Its cause analysis, named files, and suggested approach are leads, written before anyone read the current code. Where repository evidence contradicts a lead, implement what the evidence supports and record the contradiction in the brief. User corrections, repository instructions, and verified repository facts still apply.

## 0. Orient

Before reading the ticket, run one batch of commands so the rest of the workflow reasons from observed state rather than assumption:

```sh
git rev-parse --show-toplevel || exit 1
git rev-parse --abbrev-ref HEAD && git status --short && git log --oneline -5
git remote; git rev-parse --abbrev-ref '@{upstream}' 2>/dev/null || echo '<no upstream>'
```

Use `git remote` and not `git remote -v`: a remote URL can carry an embedded token, and the name is all this step needs. Add the repository's own version and toolchain check when its `AGENTS.md` names one. Do not restate the output; use it. If the branch, base, or working tree does not match what the request assumes, stop and say so before editing.

## 1. Understand

Read the ticket and relevant linked context. Inspect enough of the repository to identify:

- acceptance criteria and affected behavior,
- the existing analogous implementation,
- relevant tests and validation seams,
- public, shared, data, deploy, or cross-system contracts involved.

Investigate discoverable facts. Ask only about unresolved decisions that materially change the implementation. If a reported bug has no established cause, use `diagnosing-bugs` as the primary workflow.

When the user supplies a repository, base, or branch, resolve it rather than reconciling against the orientation output, which carries only the current branch's own upstream:

```sh
git rev-parse --verify '<ref>^{commit}'   # resolve the supplied ref to a commit
git merge-base --is-ancestor <base-ref> HEAD
```

An ancestor check returning `1` means the base is not an ancestor of HEAD; it does not explain why. Inspect the divergence before deciding whether an update is needed. These commands inspect local refs only. When remote freshness matters, fetch the intended remote first and report any inability to refresh it. Do not silently continue from an unexpected branch or a conflicting remote branch.

## 2. Map and brief

Before choosing an implementation, read [change-impact](references/change-impact.md) and perform its pre-change pass. Build the brief from concrete locations and evidence, not from repository categories or an assumed design.

Then read [grill](references/grill.md) and pressure-test the behavior found in the map. If a product or architectural decision remains unresolved, stop and ask with a recommendation when evidence supports one. Do not implement around the gap.

If the map contains multiple independently deliverable state machines or durable or external side-effect clusters, stop before editing and recommend a split. Keep them together only when one acceptance criterion or invariant requires the combined change to be atomic; record that reason in the brief.

Keep one compact brief in the conversation containing only what applies:

- goal and acceptance criteria,
- existing pattern,
- the chosen design, and what makes it simpler than the alternative considered: fewer concepts a caller must know, less duplicated policy, fewer invalid states, fewer coordinated edits,
- locations that change and behavior that must remain unchanged,
- invariant, owner, states, writers, or partial-failure boundary,
- scope decision when more than one behavioral cluster was inspected,
- validation approach,
- material risks or blockers.

Do not create a separate planning artifact. A trivial, local, low-risk change may use the short form defined by `change-impact`.

## 3. Implement

Implement the smallest coherent vertical change that satisfies the ticket. Prefer the design with the fewest concepts a caller must know, the least duplicated policy, the fewest invalid states it permits, and the fewest coordinated edits the next change would need. Follow repository patterns and preserve existing contracts unless the ticket explicitly changes them.

Evidence found while implementing can invalidate the chosen approach. When it does, change the approach and say so in the brief instead of working around what the map got wrong.

When the brief names an invariant or expensive failure, write or extend the test that can go red on that behavior before or with the production change. Cover the relevant failure class, not only the intended path.

Do not expand scope or perform unrelated cleanup. Do not add fields, settings, or compatibility paths without a demonstrated caller or contract. Add an abstraction only when it removes coordination that exists today or makes a required invariant enforceable; hypothetical reuse is not enough.

## 4. Prove

Read [prove-it-works](references/prove-it-works.md) and follow it. Prove both the requested behavior and any nearby behavior the brief says must remain unchanged.

Never claim success from inspection alone. A green build is not proof. State exactly what ran and what remains unverified.

If a required acceptance criterion remains materially `UNPROVEN`, do not describe the change as ready, publish it as non-draft, or request review. Obtain the missing evidence, keep the change draft, or ask the user to accept the named risk explicitly. An unavailable optional metric is not material evidence by itself.

## 5. Cold self-review

Re-read the ticket, final diff, and test results without using the implementation rationale as proof. Derive what changed from the diff itself.

Run the post-change pass in [change-impact](references/change-impact.md). If the diff reveals a location or behavior absent from the original map, update the map and inspect that impact before continuing.

Confirm only what applies:

1. Every acceptance criterion has an observable implementation and proof.
2. The owning component enforces each invariant; callers do not duplicate or bypass it.
3. Every writer and reader of a changed shared fact still satisfies the provenance map from `change-impact`.
4. Primary and ancillary effects have the failure, retry, concurrency, and partial-success outcomes `grill` settled.
5. Tests can fail for the target behavior and at least one material preserved or negative case.
6. The diff contains no dead fields, speculative compatibility, or unrequested cleanup.
7. Every new comment block past two lines names the invariant, external constraint, or failure semantic it carries that the code and tests cannot. None restates ticket history, a ticket ID, or the PR description. The diff contains no comment-only hunks and no rewritten comment wording without a behavior change.

Mark material claims without executable evidence as `UNPROVEN`. Do not create a critic or invoke `code-review` automatically. Recommend independent review when risk remains material.

## 6. Finish

Report:

- what changed,
- validation actually executed,
- remaining risks or unresolved items.

When preparing a PR body, findings, or final report, load `unslop` if it is not already in context and apply it while drafting.

Do not create extra documentation, commit, push, open a PR, publish comments, or send external messages unless explicitly requested or required by an established repository workflow.

When publication is authorized, review the final diff and validation first. Confirm the intended repository, remote branch state, and PR base immediately before publishing, then verify the resulting remote head and PR base/head.
