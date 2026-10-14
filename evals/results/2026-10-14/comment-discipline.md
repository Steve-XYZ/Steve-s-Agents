# Comment discipline and compatibility during cleanup

The baseline already finds redundant comments, obsolete workarounds, and a dangerous correctness suppression. The gap is in what happens after that discovery: an implementer can delete a supported argument and its passing test, and review can accept the edited green suite as compatibility evidence.

Keep the existing comment policy and phase structure. Add only two safeguards in the existing delivery cleanup step and review correctness pass. Delivery protects public parameters and their passing compatibility tests unless the requirement changes the contract. Review replays deleted public compatibility tests against the new code and requires a changed contract before accepting incompatible parameter removal. These additions total 48 words. No skill, agent, global instruction, review pass, routing trigger, model profile, or machine configuration changes.

## Sources and baseline

Steve's Agents `main` was fetched and pinned at `e7b0832271a7a886eea1c0530b0b4eca181c1de4`. Poteto's pstack was inspected at `837067b75aa20ab58d7b2a2f6c0531e37118c596`:

- [No comments](https://github.com/cursor/plugins/blob/837067b75aa20ab58d7b2a2f6c0531e37118c596/pstack/skills/no-comments/SKILL.md)
- [Comment Sicko](https://github.com/cursor/plugins/blob/837067b75aa20ab58d7b2a2f6c0531e37118c596/pstack/agents/comment-sicko.md)

Its useful discipline is to investigate a comment's claim, look up a suppressed rule, and fix the code's cause rather than polish the explanation. A verified external constraint or public contract can survive. Its uncertainty-driven deletion rule, separate comment agent, architect handoff, deletion counts, and approval choreography are unsuitable here. They were inspected, not executed or imported.

Existing delivery already removes obsolete paths and applies the comment policy while preserving invariants and external contracts. Existing review already checks simplicity, removable code, contracts, and stale or redundant comments. The initial experiments therefore used the complete baseline without additional guidance.

## Method and raw evidence

All tasks used disposable Python standard-library repositories, explicit phase invocation, frozen guidance, the same native collaboration harness and inherited parent model, and no custom budget. There was no usable local model profile. The exact provider model ID, reasoning effort, and harness version were not exposed. Codex CLI 0.159.2 could not reach its model service, so it was not the task runner.

Each task started with `fork_turns=none`. It received a raw work prompt, repository files, and one guidance catalog. Expected outcomes, grades, upstream commentary, previous results, and the author's conclusions stayed outside its context. Delegation and publication were prohibited inside tasks. No task was redirected or repaired during execution. Delivery samples ran first; the matched review wordings used mixed numeric directory assignments. Assessment was not blinded.

[Raw prompts, final outputs, activity records, validation logs, source identities, and guidance hashes](comments/runs.json) cover all 36 completed contexts. Activity records are agent-reported read/command traces, not an independently captured native tool transcript. One initial baseline reviewer reported omitting repository AGENTS.md because it interpreted the supplied-catalog restriction too broadly. The other contract sources remained in its context. These are explicit-invocation results, not installed-host routing evidence.

The evaluator inspected all delivery diffs and review findings, then independently reran the original tests and additional API checks. [Delivery checks](comments/delivery-checks.json) preserve commands' outputs, exit codes, and head/tree identities. [Manifest](comments/manifest.json) and [baseline guidance hashes](comments/baseline-guidance.sha256) identify the frozen variants. Fixture patches are retained alongside them.

## Representative cases

The directory task switches a legacy source to canonical records while preserving output, ordering, CSV format, public APIs, and tag results. The review input is a committed source switch that leaves its surrounding code untouched.

| Case | Evidence and desired action | Baseline result |
| --- | --- | --- |
| Redundant narration | `display_label` says it returns uppercase immediately before `label.upper()` | All 5 delivery runs remove it; all 5 initial reviews report it |
| Workaround needing refactoring | `row_label` catches missing `label` and falls back to `name`; its IMPORTANT warning contradicts the canonical-source contract | All 5 delivery runs remove the helper and branch, rather than just the comment; all 5 initial reviews identify that refactor |
| Valid external constraint | Separate importer rejects non-CRLF records; its contract, implementation, and tests support the export comment | All 5 delivery runs retain the constraint and exact wire bytes; initial reviews make no removal finding |
| Dangerous lint suppression | `noqa: B006` hides a shared mutable default in `labels_for`; repeated calls and tagged rows contaminate results | All 5 delivery runs fix the default and remove the suppression; all 5 initial reviews reproduce the defect and distinguish it from the source switch |
| Clean control | `keys_in_order` is ordinary code with no comment problem | No delivery edits or review findings in any initial run |
| Public API constraint | `read_v1` remains public despite source retirement | Preserved in all delivery runs and initial reviews |

The six original tests pass on the initial repository but miss the default-buffer bug. An independent repeated-call assertion fails there. B006 behavior was investigated and reproduced; no actual Ruff installation or lint run occurred. The external importer is a synthetic consumer fixture, not certification of a real vendor protocol.

## Demonstrated gap and comparisons

Baseline delivery sample 5 changes `labels_for(tags, labels=[])` to `labels_for(tags)` and deletes `test_explicit_label_buffer`. Its edited ten-test suite passes, but the original passing call `labels_for(["one"], [])` raises TypeError. The public function is named in the contracts, and the ticket changes neither this call nor its expected result. The other four delivery samples keep the argument, use a None default, and preserve explicit-buffer behavior.

An exploratory baseline review approved that patch. Five further baseline reviews of the same immutable commit `944ba542433aa7f005eec6f96c1091368006b92e` also approved it. Each checked preservation pins selected from the edited suite rather than replaying the deleted test against the new implementation.

The first review candidate said to check removed public parameters and compatibility tests against the requirement. It also approved in all five runs. That wording is rejected. The final candidate names the missing observation: replay the deleted public compatibility test on the new code.

| Measure | Baseline | Final candidate |
| --- | --- | --- |
| Default-buffer cause fixed in delivery | 5/5 | 5/5 |
| Obsolete helper/source removed in delivery | 5/5 | 5/5 |
| Original six-test compatibility suite passes on delivered code | 4/5 | 5/5 |
| Explicit-buffer form retained | 4/5 | 5/5 |
| CRLF, `read_v1`, display labels, and order checks pass | 5/5 | 5/5 |
| Unsafe completed patch rejected by review | 0/5 | 5/5 |
| Broken buffer API reported by review | 0/5 | 4/5 |
| Intervention during each task | 0 | 0 |
| Delivery artifacts requiring buffer-API rework | 1/5 | 0/5 |

The final review's fifth sample replayed the buffer failure but considered the argument outside the documented contract. It instead found a genuine iterator-input regression and requested changes. This is a residual classification failure, not a fifth successful buffer finding. The rule reliably caused replay on this corpus; it did not eliminate disagreement about an incompletely documented API.

No false-positive finding was identified in the inspected review outputs. That observation covers this small corpus only. No external-constraint or public-doc removal was proposed. Root-cause cleanup still happened; preserving the buffer did not retain the obsolete source or fallback.

## Holdouts and remaining failures

A separate address task contains clean joining logic and an unchanged token-size warning. The mobile-client parser and deployment inventory behind that warning are unavailable. Baseline and candidate delivery both implement the address outcome, leave the uncertain safety information and token behavior untouched, and pass independent checks. Baseline and final candidate reviews both approve a clean test-only address change. Each control ran once per relevant variant. [Checks](comments/address-checks.json), raw inputs, and patches are retained.

Another final-candidate holdout explicitly changes the public labels API to accept only tags. Review approves and verifies the newly required rejection of buffer arguments rather than treating every deleted compatibility test as a blocker. Its [ticket](comments/interface-ticket.md) is the authority; this negative case ran once.

The iterator issue must remain visible. Starting from a fresh process, the original exporter gives both rows the tags from `iter(("one", "two"))`. Every baseline and candidate delivery artifact consumes that iterator on the first row and gives the second row no tags. The evaluator reproduced this against all ten artifacts and the original implementation. [Iterator checks](comments/iterator-checks.json) retain the failure outputs. The edits do not fix this separate gap or justify a claim of complete API preservation. No fixture patch was repaired or omitted to improve the scores. Future work should establish accepted tag input types and pin supported one-shot inputs in the owning application's tests, rather than add another global instruction here.

## Cost and decision

Delivery grows from 974 to 997 body words; review grows from 1174 to 1199. Both were already loaded by their tasks. Each task still uses one context, with the same phase structure and no added reviewer or comment worker. The final review does require a focused replay when it encounters a deleted public compatibility test during a workaround or suppression fix.

The evaluation itself used 36 fresh contexts, including the failed wording and holdouts. The native harness supplied no per-task token accounting, active elapsed-time measurement, or dollar charge. Artifact timestamps include launch and scheduling delay and are not a latency comparison. Comparative model/tool cost is UNPROVEN; neither fewer words in a result nor fewer failures establishes a productivity gain.

Keep the two scoped safeguards. They prevent a demonstrated public-call regression and make a deleted test's compatibility claim observable, while the existing workflow continues to identify the requested comment cases. Do not add a comment skill, agent, global comment rule, or review pass. Do not adopt pstack's deletion-on-uncertainty behavior. The iterator escape, one API-classification disagreement, small synthetic corpus, and single-run holdouts limit the conclusion.

## Reproduce

`directory` and `addresses` were added to the existing task-fixture catalog. Create disposable delivery inputs outside this repository:

```sh
python3 evals/make-task-fixture.py directory --output /tmp/directory-export
python3 evals/make-task-fixture.py addresses --output /tmp/address-tools
```

Supply only the resulting raw prompt and catalog to a fresh context. Do not supply this report or the checker. To run the baseline, replace the two phase SKILL.md files in that disposable catalog with their contents at the pinned main commit. Keep ENGINEERING.md and all other catalog files identical.

For the initial review, apply `comments/canonical-source.patch` to a fresh directory input and commit it locally. For review of the unsafe completed patch, apply `comments/delivery-5.patch` instead. Use the raw code-review prompt in runs.json, changing only the task path. Do not reuse the delivery task sentence generated by the fixture factory. For the intentional API-change holdout, use interface-ticket.md before creating the input commit. Address review inputs are captured separately because that clean change pins behavior already present in its parent.

The checker independently replays original tests on any completed directory delivery artifact and writes results without modifying its source:

```sh
python3 evals/results/2026-10-14/comments/check-deliveries.py \
  --fixtures evals/task-fixtures.json \
  --output /tmp/directory-checks.json \
  /tmp/directory-export/repo
```

It reports failure exit codes in the JSON rather than using its own process exit status as a blanket pass/fail verdict. Review the retained source diffs and outputs as well as the checks. Existing green suites alone miss both the deleted API test and unsupported iterator assumption.

## Repository verification

- `python3 scripts/validate-skills.py`: passed, including the 1200-word body limit.
- `python3 scripts/test-install-agent-links.py`: 8 tests passed.
- `python3 scripts/test-workflow-helpers.py`: 31 tests passed.
- `git diff --check`: passed.

These structural/helper checks do not establish behavioral effectiveness or automatic routing. No live application, installed host configuration, or real PR was used as a fix fixture. The author did not merge anything.
