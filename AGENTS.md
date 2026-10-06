# Working on this repository

This repository distributes agent guidance and small helpers. It does not contain the BOS applications or their runtime environments.

- Workflow entry points and references live in `shared/`; `dotnet/` holds conditional framework knowledge.
- `configs/` contains machine reference copies. Preserve machine-specific paths and setup. Editing these files does not install them or change a BOS checkout.
- `scripts/install-agent-links.sh` discovers skills by directory and preserves local routing settings. Keep existing skill names unless migration is part of the request.
- `scripts/review-package.py` freezes committed diffs and optional evidence. `scripts/pr-state.py` reads GitHub state. Neither proves code correctness.
- `evals/` separates structural checks, task behavior, and host routing.

Run the relevant deterministic checks:

```sh
python3 scripts/validate-skills.py
python3 scripts/test-install-agent-links.py
python3 scripts/test-workflow-helpers.py
```

Use disposable fixtures for helper tests and workflow trials. Do not run fix prompts against live PRs. For substantial workflow changes, use fresh-context tasks with raw prompts and fixtures; keep expected outcomes and the author's conclusions out of the task context. State whether a run tested explicit invocation or actual host routing.

Put repeatable facts in tools and project-owned knowledge in scoped instructions. Every new reference or rule needs a failure it prevents and a case where it stays out of the way. Passing structural checks does not establish workflow effectiveness.

## Writing a skill

- A description states only when to use the skill and starts with "Use". A description that summarizes the workflow gets followed instead of the body.
- Knowledge that several phases need lives in a gate skill that they name. It does not live in one phase's references. The only cross-skill link allowed is to a handoff contract listed in `HANDOFF_REFERENCES` in the validator, such as the review package `code-review` expects.
- Content most invocations need stays in `SKILL.md`. A reference holds what only some invocations need. Judge that from open counts in sessions that met the reference's trigger.
- Match the form to the failure. A rule agents break under pressure gets a prohibition and red flags. Output with the wrong shape gets a recipe naming its parts. An omitted element gets a required slot. Behavior that depends on a condition gets a conditional on an observable predicate. Do not add "unless it matters" clauses; they reopen the rule.
- Before adding guidance, run the task without it. If that control already behaves, there is nothing to write.
- Name trial directories and write trial prompts like real work; never call them an eval, trial, test, or comparison. Grade from the files an agent actually read and changed, not from its report.
- `scripts/validate-skills.py` checks description form and length, the body word limit, Codex metadata, and cross-skill links. It cannot tell whether a description summarizes the workflow; review that by hand.
