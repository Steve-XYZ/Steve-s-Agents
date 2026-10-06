# Restructure trials, 6 October 2026

Fresh Claude Sonnet subagents ran two disposable tasks from `task-fixtures.json` before and after the restructure. Each run got the raw prompt, the fixture repository, and a copy of one guidance catalog, and used explicit skill invocation. No run saw expected outcomes. The global guidance each subagent loaded was this machine's installed copy from before the restructure, so the new `verify-work` line in `ENGINEERING.md` was not exercised.

| Catalog | SHA-256 (method in the [September 21 record](../2026-09-21/README.md)) |
| --- | --- |
| Before, commit `0127435` | `5884481a99193e9e71fb4e943d9c7acfd2dc25fe67f974374390352704aaa02c` |
| After, trial copy | `6e67f7349e6e2553e0863171fe118fd534fd488868a8cdde309923821cc5ae97` |

After the trials, the `tested` row in `verify-work` was reworded to classify a direct function call or a test-suite run as `tested`. Three of the four after runs had labeled one of those `observed`.

## Currency task

The ticket adds `report --currency`. The fixture's settings file silently overrides command-line flags, so a flag that unit tests accept still prints USD from the real command.

| Run | Entry | Found the override | Real command run | Evidence levels |
| --- | --- | --- | --- | --- |
| [base-currency-1](base-currency-1.patch) | old `deliver-ticket` | yes | yes, against the base commit | none |
| [base-currency-2](base-currency-2.patch) | old `deliver-ticket` | yes | yes, with baseline captures | none |
| [plain-currency-1](plain-currency-1.patch) | no skill | yes | yes | none |
| [plain-currency-2](plain-currency-2.patch) | no skill | yes, by its patch; the run was cut off before its report | not recorded | none |
| [new-currency-1](new-currency-1.patch) | new `deliver-ticket` | yes | yes, with baseline captures | per criterion |
| [new-currency-2](new-currency-2.patch) | new `deliver-ticket` | yes | yes, with baseline captures | per criterion |

All finished patches print `Total: 74.52 EUR` for the flag and `81.00 USD` without it, and their suites pass. Every run reported the export side effect of fixing the precedence.

## Claims task

Another agent's findings name three provider bugs. One is real, one is our zero-padding defect in `to_major_units`, and one is our own balance read racing the credit.

| Run | Entry | Claim 1 | Claim 2 | Claim 3 | Evidence levels |
| --- | --- | --- | --- | --- | --- |
| base-claims-1 | old `diagnosing-bugs` | confirmed, narrowed | ours | ours | prose confidence |
| base-claims-2 | old `diagnosing-bugs` | confirmed, narrowed | ours | ours | prose confidence |
| new-claims-1 | new `verify-work` | confirmed, narrowed | ours | ours | per claim |
| new-claims-2 | new `verify-work` | confirmed, narrowed | ours | ours | per claim, with `UNPROVEN` and what would settle it |

## What this shows

The control conditions already behaved. Sonnet with the old catalog, and with no skill at all, drove the real command and caught the override, and the old diagnosing route rejected both false claims. These fixtures therefore show no failure for the restructure to fix and cannot show an improvement. The after runs reached the same outcomes, so they show no regression on these two tasks. The visible difference is the per-claim evidence table.

The case for the restructure rests on structural evidence from real sessions, recorded in the [foundation decisions](../../../docs/workflow-foundation.md): verification guidance reachable only from `deliver-ticket`, fresh reviews that ran no commands, and questions routed into delivery skills. None of those failure modes is reproduced here. Automatic routing, the global completion gate, `investigate`, `blast-radius`, `orchestrate`, and the model fallback remain unassessed. Trial directories were named `wf-trials`, which breaks the naming rule this change adds to `AGENTS.md`.
