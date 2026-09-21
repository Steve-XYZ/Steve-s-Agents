# Checking workflow changes

Run the checks that do not spend model tokens first:

```sh
python3 scripts/validate-skills.py
python3 scripts/test-install-agent-links.py
python3 scripts/test-workflow-helpers.py
```

The validator checks this repository's single-line name/description fields, installed-name collisions, reference file existence, and routing fixture structure. It is not a general YAML parser, a semantic router, or evidence of model compliance. Use the harness's skill validator too when changing other frontmatter fields.

`routing.json` contains prompts, expected skill loads, skills to avoid, and observable expectations. For a changed trigger, run only its affected cases in a fresh session of each supported harness. Supply the prompt and minimum relevant fixture, not the expected answer. Record the harness/version, model, guidance commit, actual skill/file reads, outcome, and transcript path outside the worktree. The `load` list covers the complete case, not just the initial response: workflow cases load `unslop` only when preparing findings or a final report. For continuation cases such as status, provide prior completed work first. Run status with and without `unslop` already in context; neither should cause a new read. Stop before report preparation only if the case is blocked, and record the remaining loads as unassessed. Respect explicit-only settings: invoke that skill explicitly where the harness disables automatic selection, and label that result as explicit invocation.

A routing case needs the relevant repository or PR fixture to assess execution; an unavailable fixture is blocked, not passed. Do not point fix prompts at live PRs. Use disposable repositories or captured read-only PR data. No provider is launched by the validator, and these cases have not been run merely by validating the JSON. Do not present lexical similarity as model routing accuracy.

When behavior changes, add a focused pressure case for the changed rule: e.g. an author claims a fix is complete but the fix diff still permits the failing state. Check the action and evidence, not whether the agent repeats the rule. An installer or helper change needs executable fixture coverage instead.

Method adapted from [Addy's layered evaluations](https://github.com/addyosmani/agent-skills/blob/main/evals/README.md)
and [Superpowers' skill testing](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md).

## Outcome and cost comparisons

Before adopting a material rule broadly, compare the old and new guidance on the same task fixtures with the same model, host, tools, and budget. Use repeated runs where variability could reverse the decision and holdout cases that were not used to write the rule. Blind subjective patch assessment to the workflow version when possible.

Record actual behavior, invariant preservation, invalid findings, escaped defects, human intervention/rework, elapsed time, and attributable model/tool cost. Keep blocked or unobservable cases separate from failures and passes. Do not infer improvement from loads, checklist completion, test counts, or one successful run.

For each proposed rule, include the failure it targets and a negative case where it should stay out of the way. Retain or revert based on those results. Keep the failure, proposed prevention, comparison, cost, and decision in the evaluation record; retire superseded rules instead of appending permanent global instructions.

The added routing cases cover simple delivery, ambiguous existing systems, shaping-to-delivery continuation, authorized independent slices, invalidated plans, risky review, stale runtime evidence, and false review findings. Some require a dedicated runtime or PR fixture; until that fixture is available and run, they remain unassessed.

## Reproduce an explicit-invocation task

Create an isolated task outside this repository:

```sh
python3 evals/make-task-fixture.py slices --output /tmp/workflow-slices-trial
```

The destination must not exist. The command prints `prompt.txt`; supply its contents to a fresh agent. Available tasks are `simple`, `slices`, `shape`, and `feedback`. The feedback task preserves the first slices trial's escaped edge case and supplies review claims to adjudicate. Only the raw task, fixture files, and guidance catalog are copied. Expected outcomes and prior results stay here, outside the task context.

The [September 21 trial record](results/2026-09-21/README.md) includes resulting patches, rerun output, and limits. Explicit invocation proves neither automatic selection nor comparative effectiveness.
