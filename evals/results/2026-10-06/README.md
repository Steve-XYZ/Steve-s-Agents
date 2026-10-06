# Restructure trials, 6 October 2026

Fresh Claude Sonnet subagents ran two disposable tasks from `task-fixtures.json` before and after the restructure. Each run got the raw prompt, the fixture repository, and a copy of one guidance catalog, and used explicit skill invocation. No run saw expected outcomes. The global guidance each subagent loaded was this machine's installed copy from before the restructure, so the new `verify-work` line in `ENGINEERING.md` was not exercised.

| Catalog | SHA-256 (method in the [September 21 record](../2026-09-21/README.md)) |
| --- | --- |
| Before, commit `0127435` | `5884481a99193e9e71fb4e943d9c7acfd2dc25fe67f974374390352704aaa02c` |
| After, trial copy | `6e67f7349e6e2553e0863171fe118fd534fd488868a8cdde309923821cc5ae97` |
| Committed, after the review fixes and the wording comparison | `c8448cad9910def68513ff28d7de2dc6783e51195baeca2dd62c1fac138e3e23` |

Three of the four after runs labeled a test-suite run or a direct function call `observed`. The [wording comparison](#evidence-level-wording) below tested two rewrites of the level table; the committed catalog carries the second.

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
| [base-claims-1](base-claims-1.md) | old `diagnosing-bugs` | confirmed, narrowed | ours | ours | prose confidence |
| [base-claims-2](base-claims-2.md) | old `diagnosing-bugs` | confirmed, narrowed | ours | ours | prose confidence |
| [new-claims-1](new-claims-1.md) | new `verify-work` | confirmed, narrowed | ours | ours | per claim |
| [new-claims-2](new-claims-2.md) | new `verify-work` | confirmed, narrowed | ours | ours | per claim, with `UNPROVEN` and what would settle it |

The claims rows link each run's final report. The task is read-only, so the report is its deliverable.

## Evidence-level wording

Each run got the finished currency change, uncommitted, and five claims to check with `verify-work`, including "the full test suite passes". A run is graded wrong when its table labels that suite run `observed`; the correct level is `tested`. Directories were named `stockreport-N` and assigned to wordings in mixed order. Six runs in the first batch stopped at an account session limit and were rerun on fresh copies; those six are excluded.

| Wording | Level table | Suite labeled `observed` | Runs |
| --- | --- | --- | --- |
| Trialed (`6e67f734…`) | `observed` lists "the app, command, endpoint, job" | 4 of 5 | [1](wording/run-1-old.md), [6](wording/run-6-old.md), [7](wording/run-7-old.md), [12](wording/run-12-old.md), [15](wording/run-15-old.md) |
| First rewrite (`68015034…`) | adds "Calling a function directly is `tested`" | 3 of 5 | [3](wording/run-3-new.md), [11](wording/run-11-new.md), [13](wording/run-13-new.md), [14](wording/run-14-new.md), [16](wording/run-16-new.md) |
| Committed (`c8448cad…`) | levels keyed on what ran: the product's entry point, a test runner or script, or nothing | 0 of 5 | [17](wording/run-17-v3.md), [18](wording/run-18-v3.md), [19](wording/run-19-v3.md), [20](wording/run-20-v3.md), [21](wording/run-21-v3.md) |

The first rewrite did not bind: a suite started with `python3 -m unittest` is a command, and the `observed` row named commands. Keying the table on what ran removed that overlap. Five samples per wording on one task and one model is a wording check, not a general result.

## What this shows

The control conditions already behaved. Sonnet with the old catalog, and with no skill at all, drove the real command and caught the override, and the old diagnosing route rejected both false claims. These fixtures therefore show no failure for the restructure to fix and cannot show an improvement. Two after runs per task reached the same outcomes; that is too few to rule out a regression. The visible difference is the per-claim evidence table, and the wording comparison shows its labels were unreliable until the level table was keyed on what ran.

The case for the restructure rests on structural evidence from real sessions, recorded in the [foundation decisions](../../../docs/workflow-foundation.md): verification guidance reachable only from `deliver-ticket`, fresh reviews that ran no commands, and questions routed into delivery skills. None of those failure modes is reproduced here. Automatic routing, the global completion gate, `investigate`, `blast-radius`, `orchestrate`, and the model fallback remain unassessed. Trial directories were named `wf-trials`, which breaks the naming rule this change adds to `AGENTS.md`.
