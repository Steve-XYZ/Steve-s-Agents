# Checking workflow changes

Run the checks that do not spend model tokens first:

```sh
python3 scripts/validate-skills.py
python3 scripts/test-install-agent-links.py
python3 scripts/test-workflow-helpers.py
```

The validator checks this repository's single-line name/description fields,
installed-name collisions, reference file existence, and routing fixture structure.
It is not a general YAML parser, a semantic router, or evidence of model compliance.
Use the harness's skill validator too when changing other frontmatter fields.

`routing.json` contains prompts, expected skill loads, skills to avoid, and
observable expectations. For a changed trigger, run only its affected cases in
a fresh session of each supported harness. Supply the prompt and minimum relevant
fixture, not the expected answer. Record the harness/version, model, guidance
commit, actual skill/file reads, outcome, and transcript path outside the worktree.
For continuation cases such as status, provide prior completed work first.
Respect explicit-only settings: invoke that skill explicitly where the harness
disables automatic selection, and label that result as explicit invocation.

A routing case needs the relevant repository or PR fixture to assess execution;
an unavailable fixture is blocked, not passed. Do not point fix prompts at live
PRs. Use disposable repositories or captured read-only PR data. No provider is
launched by the validator, and these cases have not been run merely by validating
the JSON. Do not present lexical similarity as model routing accuracy.

When behavior changes, add a focused pressure case for the changed rule: e.g.
an author claims a fix is complete but the fix diff still permits the failing
state. Check the action and evidence, not whether the agent repeats the rule.
An installer or helper change needs executable fixture coverage instead.

Method adapted from [Addy's layered evaluations](https://github.com/addyosmani/agent-skills/blob/main/evals/README.md)
and [Superpowers' skill testing](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md).
