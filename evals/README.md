# Checking workflow changes

Run the checks that do not spend model tokens first:

```sh
python3 scripts/validate-skills.py
python3 scripts/test-install-agent-links.py
python3 scripts/test-workflow-helpers.py
python3 evals/test-task-evals.py
```

The validator checks this repository's single-line name/description fields, installed-name collisions, reference file existence, and routing fixture structure. It is not a general YAML parser, a semantic router, or evidence of model compliance. Use the harness's skill validator too when changing other frontmatter fields.

`routing.json` contains prompts, expected skill loads, skills to avoid, and observable expectations. For a changed trigger, run only its affected cases in a fresh session of each supported harness. Supply the prompt and minimum relevant fixture, not the expected answer. Record the harness/version, model, guidance commit, actual skill/file reads, outcome, and transcript path outside the worktree. The `load` list covers the complete case, not just the initial response: GitHub artifacts use `engineering-writing`, which loads `unslop` if absent; internal findings and reports use `unslop` alone. For continuation cases such as status, provide prior completed work first. Run status with and without writing guidance already in context; neither should cause a new read. Stop before report preparation only if the case is blocked, and record the remaining loads as unassessed. Respect explicit-only settings: invoke that skill explicitly where the harness disables automatic selection, and label that result as explicit invocation.

A routing case needs the relevant repository or PR fixture to assess execution; an unavailable fixture is blocked, not passed. Do not point fix prompts at live PRs. Use disposable repositories or captured read-only PR data. No provider is launched by the validator, and these cases have not been run merely by validating the JSON. Do not present lexical similarity as model routing accuracy.

When behavior changes, add a focused pressure case for the changed rule: e.g. an author claims a fix is complete but the fix diff still permits the failing state. Check the action and evidence, not whether the agent repeats the rule. An installer or helper change needs executable fixture coverage instead.

Method adapted from [Addy's layered evaluations](https://github.com/addyosmani/agent-skills/blob/main/evals/README.md)
and [Superpowers' skill testing](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md).

## Outcome and cost comparisons

Before adopting a material rule broadly, compare the old and new guidance on the same task fixtures with the same model, host, tools, and budget. Use repeated runs where variability could reverse the decision and holdout cases that were not used to write the rule. Blind subjective patch assessment to the workflow version when possible.

Record actual behavior, invariant preservation, invalid findings, escaped defects, human intervention/rework, elapsed time, and attributable model/tool cost. Keep blocked or unobservable cases separate from failures and passes. Do not infer improvement from loads, checklist completion, test counts, or one successful run.

For each proposed rule, include the failure it targets and a negative case where it should stay out of the way. Retain or revert based on those results. Keep the failure, proposed prevention, comparison, cost, and decision in the evaluation record; retire superseded rules instead of appending permanent global instructions.

The added routing cases cover simple delivery, ambiguous existing systems, shaping-to-delivery continuation, authorized independent slices, invalidated plans, risky review, stale runtime evidence, and false review findings. The October cases add read-only questions, claim validation, completion under time pressure, an undocumented run recipe, blast-radius questions, a single ticket across two repositories, and delegated model sources. Some require a dedicated runtime or PR fixture; until that fixture is available and run, they remain unassessed.

Before writing new guidance, run the task without it. When that control already behaves, the guidance has nothing to fix. To check wording, run five or more fresh samples per variant against a no-guidance control and read every flagged output yourself; varied interpretations across samples mean the wording does not bind. Name trial directories and prompts like real work, and grade from the files an agent read and changed rather than from its report.

## Replay a real ticket set

The `blast-radius` ticket-scope reference has a replay record for a real multi-repository ticket set: base commits, what happened without the reference, and how to score a rerun. It names private repositories, so it stays with the project's workspace guidance rather than here, and remains unassessed until run on a machine that has them.

Orchestrated delivery is the rule for ticket sets with required edits in several repositories, and its effect is unassessed. Run the same replay with orchestration and with one thread, plus a single-repository control, and compare missed surfaces, worker count, repeated investigation, total usage, and elapsed time. Revise the rule from the result.

## Reproduce an explicit-invocation task

Create an isolated task outside this repository:

```sh
python3 evals/make-task-fixture.py slices --output /tmp/orders-export
```

The destination must not exist and must sit outside Git checkouts. The command prints `prompt.txt`; supply its contents to a fresh agent. Tasks are the keys of `task-fixtures.json`. In addition to the original delivery, shape, feedback, currency, claims, parcel and discount cases, `discounts-clean` is a corrected review control, `dispatch` covers starvation and retry workarounds, and `workspace` covers one policy across three independent repositories. A task with a `change` entry gets a second commit so a review task can review the latest commit.

Pass `--skill <name>` for another entry skill, `--guidance-root /path/to/checkout` for another Steve's Agents catalog, or `--control` for an empty optional catalog and no explicit skill. Skill files and global defaults are copied without changing application commits. The prompt explicitly invokes only the entry skill; global-default loading and host routing remain separate questions. Only the raw task, fixture files and optional catalog enter the task directory. Grading code, expected outcomes, prior results and receipts stay outside it.

The [September 21 trial record](results/2026-09-21/README.md) includes resulting patches, rerun output, and limits. The [October 6 record](results/2026-10-06/README.md) compares the `currency` and `claims` tasks before and after the restructure. Explicit invocation proves neither automatic selection nor comparative effectiveness.

## Run and retain one task

Start with an offline pilot. This creates an organic task and a separate record without launching a model:

```sh
python3 evals/run-task.py currency \
  --task-dir /tmp/warehouse-report \
  --record-dir /tmp/outcome-records/report-1 --prepare-only
```

Give `/tmp/warehouse-report/prompt.txt` to a fresh context in the intended host. Keep the response and any transcript export in the record directory, outside candidate context. Then grade the resulting files:

```sh
python3 evals/grade-task.py --record-dir /tmp/outcome-records/report-1
```

A Codex CLI run uses the same fixture with explicit model, effort and wall-clock limit:

```sh
python3 evals/run-task.py currency \
  --task-dir /tmp/stock-report \
  --record-dir /tmp/outcome-records/report-2 \
  --model <exact-supported-model-id> --effort high --timeout 300
```

The adapter uses `codex exec`, `--ignore-user-config`, `--ephemeral`, JSONL output and `workspace-write`. `--codex /path/to/codex` selects an executable. It uses the existing CLI credentials and never provisions a key or changes installed settings. These controls do not create a hermetic host: installed global instructions, host capabilities and provider behavior can still matter. The prompt requests one context without delegation; that is an instruction, not enforcement or aggregate child-usage accounting. No Claude Code or T3 adapter is implemented; use the prepared-task path for those hosts and label what actually ran.

`receipt.json` records fixture and prompt hashes, copied-guidance hash and source commit, initial and final source hashes including untracked files, repository heads, requested model/effort, CLI/Python/host versions, actual elapsed execution time, raw output hashes and execution status. `events.jsonl`, `stderr.txt` and any `response.txt` retain the CLI output. Inspect the exact source hash when the guidance checkout has uncommitted changes; its commit alone is not the supplied catalog identity.

Execution states are `prepared`, `completed`, `blocked`, `timed_out` and `cancelled`. A successful CLI exit without a completed model turn is blocked. Timeout or cancellation terminates the process group and preserves its output. The wall limit covers CLI version detection and execution, plus up to a second for termination; fixture preparation and subsequent grading have separate bounded commands. No token or tool-call cap is implemented. Usage sums valid `turn.completed` counters only when every turn supplies them and the stream is well formed. Missing or invalid usage, resolved model identity, dollar cost and total tool calls stay null. Completed item counts are diagnostic observations, not a substitute for total tool usage. Cached input is a subset of input tokens, not extra input to add again.

The runner exits 0 for a prepared task or completed model turn, and 2 for execution/setup gaps. Exit 0 does not mean the candidate passed. A provider/auth/network failure without a completed turn has no automatic correctness grade. Keep those cases separate from candidate defects.

## Grade behavior independently

`task_oracles.py` checks actual CLI/public-function behavior against literal contract expectations. It covers currency defaults under both USD and EUR configuration, unchanged CSV output, quantity nonmutation, escaping and generators, empty-result schema, tier boundaries, retry progress and work retention, and agreement across every workspace reader. The supplied unittest suite runs separately. Its pass cannot override an independent failure, and empty discovery is `not_applicable`.

Review and claims tasks require manual assessment against the retained response, diff and evidence. The grader exposes the fixture rubric only after execution. It checks read-only source preservation but never declares a review correct from keywords, invocation counts or an agent's claim. Delivery hygiene, unnecessary changes, verification quality and human intervention also need an assessor; a passing behavioral oracle does not score those dimensions.

Grades report `passed`, `failed`, `manual_required`, `blocked` or `stale`. Source or raw-output changes after a completed receipt, changed fixture definitions, or source changes during validation cannot receive a current-state pass. A prepared/manual task can be graded, but its execution metrics remain unassessed. Each grade includes its source state, grader hash, interpreter/host identity, commands, exit codes and raw outputs. Existing grades are preserved; use `--output /tmp/outcome-records/report-1/recheck.json` for a new result. Grader exit codes are 0 for automated checks passed, 1 for a demonstrated failure and 2 for an assessment gap. Neither 0 nor an empty manual rubric certifies engineering quality beyond the implemented checks.

For comparisons, use separate fresh task/record pairs, pinned catalogs, the same explicit model and effort, the same host/tools and common limits. Alternate or randomize arm order; repeat where variability could change the decision and retain holdouts. Keep no-guidance and clean controls. A native full-system comparison must also account for all child execution and any token/tool budgets the host can enforce. The runner's explicit single-context task does not establish native routing, orchestration effectiveness or a productivity gain. Do not label missing measurements as zero or compare costs from report length.
