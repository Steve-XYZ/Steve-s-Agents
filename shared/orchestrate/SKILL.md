---
name: orchestrate
description: Use when several tickets need required edits in two or more repositories, when one thread on a cross-repository change has lost context to compaction, or when the user asks to run workers, delegate per repository, or orchestrate.
---

# Orchestrate delivery across repositories

You own the scope map, the shared contracts, the briefs, and the integration check. Workers own the code. Edit repository code yourself only to integrate when a worker cannot.

## Decide whether to orchestrate

Orchestrate when one of these holds:

- several tickets need required edits in two or more repositories;
- a single thread working a cross-repository change has been compacted and must recover from notes;
- the user asks for workers.

Otherwise stay in one thread, including for one ticket whose edits span two repositories; `blast-radius` still supplies the shared cases and deploy order. A repository that only needs reading gets no worker.

## Before any worker edits

Map scope with `blast-radius`. Its ticket-scope reference defines the set note, the shared contract cases, and the deploy order. Write all three before any worker edits.

## Choose each worker's model

Classify each repository's work separately by complexity and the cost of a mistake. One ticket can need a high-tier backend worker and a low-tier frontend worker on the same contract.

- **Low.** Localized change with clear expected behavior and direct validation. No change to a shared contract, permission, money flow, or persistent data rule. An unknown cause is not low.
- **Medium.** A regular feature that follows established contracts and architecture.
- **High.** Money, critical business rules, authorization, data integrity, or a difficult shared-contract change. A small diff can still be high.

Take the model and thinking option from the first source that has a usable entry:

1. the user's instruction for this worker or role;
2. `~/.config/agents/model-profiles.toml`: the tier entry, or its `fallback` entry when the preferred model is unavailable;
3. the current session's provider, model, and thinking option.

An entry is usable when it has no `<placeholder>` and the provider reports its model as supported. Option names and values differ between providers; read them from the provider. When the host cannot set a thinking option, launch with the model alone and record the option as the host default. Record each worker's model, thinking option, tier, and source (`user`, `profile`, `fallback`, or `session`) in the set note before launch, and pass all of them explicitly in the launch.

A low-tier worker that finds work above its tier stops and reports. Reclassify the work and launch it at the new tier.

## Launch workers

Bind each worker to its repository's worktree with the host's explicit workspace binding, such as T3 Code's thread launch with a project and worktree. A delegation call without a workspace selector does not guarantee a separate checkout. If the host cannot bind a worktree, say so and continue in one thread.

Each worker gets one brief. A field you cannot fill means that repository's work is not scoped yet.

```text
GOAL        the outcome for this repository in one sentence
TIER        low, medium, or high; a low-tier worker stops and reports on any shared-contract,
            permission, money, or persistent-data change
SCOPE       repository, worktree path, base commit, branch; paths it must not touch
CONTEXT     set-note path, this repository's scope rows, upstream worker reports it depends on
CONTRACT    the shared cases this repository must pass
ACCEPTANCE  checkable criteria, one per line
VERIFY      exact commands and the verify-work evidence level each criterion needs
FORBIDDEN   other repositories, launching threads, publishing unless authorized
REPORT      branch, commit SHAs, commands with results, shared cases run, evidence levels,
            unresolved issues, changes another repository needs
```

Hand over files and pointers, not your history. Launch in dependency order with no more workers at once than `max_concurrent_workers` from the profile, or two without one. A subscription session limit stops every running worker at once.

## Keep the set note as the ledger

After each worker report, record per repository the head SHA and each acceptance item's evidence level. A new head SHA voids that repository's rows. After compaction or a restart, trust the set note and `git log` over memory, and never relaunch work the note marks done.

Decide what the requirements and evidence settle, and record each ruling with what it costs if wrong. Ask the user only about scope, business policy, authority, or an irreversible action.

## Integrate

- Inspect the combined diffs against the set note. Confirm the shared cases ran in every repository that computes the fact, and that what one repository produces is what the next one reads.
- Treat worker reports as claims. Check them with `verify-work`, running the cross-repository checks yourself.
- Send findings back to the worker that owns the repository. After two fix rounds on the same finding without progress, give it to a fresh worker one tier up, with the report file.
- Send the combined change as one package with the set note to one fresh `code-review` context.

## Cost

Every worker investigates its own repository again, so this costs more than one thread on small sets. Record usage per set so a replay against a single-thread run can compare missed surfaces, repeated investigation, total usage, and elapsed time.
