# Orchestrated delivery across repositories

Use this mode whenever the scope map shows required edits in two or more repositories. A repository that only needs inspection gets no worker. Edits in one repository stay in the current thread.

Stay in one thread instead only when:

- the user asks for one thread;
- the host cannot launch a thread bound to a specific repository worktree; or
- the model profile below is missing, fails validation, or names a model or option the installed provider does not support.

For the last two, report exactly what is missing and ask before continuing in one thread. Never launch workers with guessed models or default settings.

Its effect is unassessed. Record a replay of a real ticket set and a single-repository control as the [evaluation guidance](../../../evals/README.md) describes, and revise this rule from what it shows.

## Roles

- **Orchestrator.** Runs at the workspace root. Owns the [scope map and set note](ticket-scope.md), the shared contracts, dependency order, worker launches, and the integration check. It edits repository code only to integrate when a worker cannot.
- **Repository worker.** One persistent thread per repository with required edits. It stays with that repository across related tickets and fix rounds. Only the orchestrator launches workers, and workers launch no threads.
- **Reviewer.** One fresh `code-review` context for the combined change, as `deliver-ticket` describes.

Never launch one implementer per ticket for tickets that share a fact.

## Before any worker edits

Write each shared fact's contract into the set note: owner, inputs, outputs, edge cases, and shared cases with concrete inputs and expected outputs. Every repository that computes the fact must pass the same cases before its worker counts as done. A prose contract alone lets two copies drift apart.

Also record per repository the acceptance criteria, the dependencies on other repositories, and the deploy order. Set the order from compatibility with what is already deployed. A producer can ship first only when the deployed consumer can read its new payload. For an incompatible change, ship a consumer that accepts both shapes first, or version the payload. Separate repositories do not prove that work can run independently.

## Load and validate the model profile

Read `~/.config/agents/model-profiles.toml`. This guidance repository's `configs/<machine>/agents/model-profiles.toml.example` shows its shape:

- `[orchestrator]`: the orchestrator's provider and model, `thinking` by default and `thinking_hard_contracts` for difficult shared contracts or dependencies.
- `[tiers.low]`, `[tiers.medium]`, `[tiers.high]`: one worker entry per tier, each with `provider`, `model`, and `thinking`.
- `[fallback.orchestrator]`, `[fallback.medium]`, `[fallback.high]`: complete replacements with their own `thinking` values, used only when the preferred entry's model is unavailable. Low tier has no fallback; when its model is unavailable, the work goes to `[tiers.medium]`.
- `[limits] max_concurrent_workers`.

Before the first launch, check that every entry the set needs exists, has no `<placeholder>` value, and names a model and thinking option the installed provider reports as supported. Read option names and values from the provider; effort levels differ between providers. If a needed entry is incomplete or unsupported, stop and report it. Check a fallback the same way before switching to it.

## Launch workers

- Bind each worker to its repository's worktree with the host's explicit workspace binding, such as T3 Code's thread launch with a project and worktree. A delegation call without a workspace selector does not guarantee a separate checkout.
- Hand over the requirements, the scope-map rows for that repository, the repository path, base commit and branch, the shared contracts and cases, acceptance criteria, required validation, and the worker's tier and model. Do not hand over the orchestrator's history.
- Launch in dependency order, with no more workers at once than the model profile's `max_concurrent_workers`. A subscription session limit stops every running worker at once and loses their work.
- Before each launch, record in the set note and report the repository, exact provider and model, thinking option, tier, and reason. Pass all of them explicitly in the launch; a host may only inherit omitted options from the parent's own provider and model. This is for visibility, not an approval step.
- Take models only from the validated profile. When an entry's model is unavailable, report it and switch to that entry's complete fallback, thinking option included. When no complete fallback exists, stop and report. Never substitute another model silently.

## Classify each repository's work

Classify each repository separately by complexity and by the cost of a mistake. One ticket can need a high-tier backend worker and a low-tier frontend worker on the same contract.

- **Low.** Localized change with clear expected behavior and direct validation. No change to a shared contract, permission, money flow, or persistent data rule. An unknown cause is not low.
- **Medium.** A regular feature that follows established contracts and architecture.
- **High.** Money, critical business rules, authorization, data integrity, or a difficult shared-contract change. A small diff can still be high.

For single-repository work the tier picks the working thread's model; it does not create another thread.

A low-tier worker that finds work above its tier stops and reports what it found. The orchestrator reclassifies the work and hands it to the profile's model for that tier. Do not retry with another low-tier model.

## Worker reports

Each worker reports its branch and commit SHAs, the validation commands it ran with their results, which shared cases ran, unresolved issues, and any change it believes another repository needs. It does not make that change itself.

## Integrate

The orchestrator inspects the combined diffs against the set note, confirms the shared cases ran in every repository that computes the fact, and checks that what one repository produces is what the next one reads. Worker summaries are not proof. Then send the combined package to one fresh reviewer.

## Cost

Every worker investigates its own repository again, so this mode costs more than one thread on small sets. Keep `max_concurrent_workers` low enough that a subscription session limit does not stop every worker at once, and record usage per set so the replay can compare it.
