---
name: blast-radius
description: Identify every surface a change must touch before editing. Use when delivering a ticket that may affect more than one project, service, contract, cache, or deploy file. Loaded by deliver-ticket after grill. Do not use for diagnosis-only or review-only requests.
---

# Blast Radius

List the surfaces the brief implies, then inspect only those. Do not expand the ticket to touch a surface that is merely nearby.

## 1. Start from the brief

Use the grill brief's owner, consumers, and deploy implications. If grill recorded `no material risk`, skip this skill.

## 2. Mark what applies

Check each item that the change can reach. Unchecked means inspected and out of scope, not forgotten.

- Core (or equivalent) service that owns the invariant
- Public API endpoint and its contract
- Admin / PAM / operator UI
- Worker / background job
- Schema: migration, Designer, and model snapshot together
- Deploy configuration for the service that *reads* each setting (`compose.tenant.yml` or equivalent); Admin, API, and Worker are separate
- Frontend consumer (`lotto-app-v2` or equivalent) of a payload, flag, or label
- Live query, cached projection, filter, export, and displayed label for the same fact
- Permissions, nav gating, and authorization on the new path
- Sibling repository that shares the flow, payload, or job

## 3. Record

Keep the list in the conversation, naming the files or projects that will change and the ones that must stay aligned without changing. Implementation stays inside that list unless evidence forces a new surface, in which case update the list before editing it.
