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

Keep the five workflow entry points small. Put repeatable facts in tools and project-owned knowledge in scoped instructions. Every new reference or rule needs a failure it prevents and a case where it stays out of the way. Passing structural checks does not establish workflow effectiveness.
