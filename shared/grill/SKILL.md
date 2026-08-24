---
name: grill
description: Adversarial pass over a ticket before implementation. Use when delivering a defined ticket, or when the user asks to grill, pressure-test, or interrogate a plan. Loaded by deliver-ticket. Do not use for diagnosis, code review, or as a substitute for repository inspection.
---

# Grill

Settle what must remain true before writing code. The output is a compact brief in the conversation, or a stop because a product or architectural decision is unresolved. Do not create a spec file unless the user asked for one or the work must survive across sessions.

## 1. Inspect first

Read the ticket and enough of the repository to name the existing analogous path, the owner of the behavior, and the validation seam. Do not ask the user for facts available in the repository, the ticket, or linked evidence.

If a review-memory file or skill is already present in this clone or the target repository, consult it for prior findings on the same surface. Do not create one.

## 2. Apply judgment

Read [engineering-judgment](../engineering-judgment/SKILL.md) and apply its compact pass. Let that pass shape the brief; do not treat an earlier draft plan as fixed.

## 3. Pressure-test

Ask only the questions whose answers would change the implementation. Skip any that the ticket and repository already settle. Stop and ask the user when a product or architectural decision remains open; do not invent the missing rule.

When the change touches money, durable state, provider calls, deploy configuration, or shared contracts, answer each item that applies:

1. What is the invariant, and which Core (or equivalent) component owns it? Endpoints, UI, and workers do not own it.
2. Which states and transitions exist? Which combinations must be impossible?
3. What remains if the process dies mid-operation? What happens on retry, duplicate delivery, stamp conflict, or replay?
4. Is a capability (`canX`, eligibility, entitlement) a separate fact from performing the provider or ledger side effect?
5. Which service reads each new setting, and does that service's deploy configuration actually set it?
6. Which consumer (frontend, Admin/PAM, export, cache, sibling API) breaks if the payload or label changes?
7. If there is a catalogue, seed, or allow-list guard, which test goes red on the case the guard claims to catch?
8. Are confirmation, cancellation, actor, or stamp fields real writes, or dead storage?

For any other change, name only: the invariant if one exists, the owner, the failure that would be expensive, and the evidence that will prove the result.

## 4. Brief

Keep the brief in the conversation. Include only what applies:

- goal and acceptance criteria,
- existing pattern and affected surface,
- invariant, owner, states, writers, and partial-failure boundary,
- validation approach,
- material risks or blockers.

Skip the brief for a trivial, single-file, low-risk change when the judgment pass confirms no material risk. One line is enough: `grill: no material risk`.

Do not start implementation from this skill. `deliver-ticket` continues from the brief.
