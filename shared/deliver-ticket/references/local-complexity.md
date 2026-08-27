# Local Complexity Guardrail

Use complexity as local delivery evidence, not as permission to change repository policy. Do not add analyzer packages, configuration, suppressions, or CI steps to the target repository unless the ticket explicitly requires a shared rule.

## Select the check

Inspect the repository's analyzer or linter configuration and established commands.

- When it already enforces cyclomatic complexity, cognitive complexity, or nesting depth, run that check through the repository's affected build or lint command. Its configured thresholds are authoritative.
- Otherwise, use the local fallback below only when the required SDK or installed linter is already available. Do not install a tool or modify the repository to make the fallback work. Mark the complexity path `UNPROVEN` when neither route is available.

## Capture the baseline

Before editing, run the selected check against the mapped files or affected project and retain diagnostics for the functions that may change. If editing already started, analyze the verified task base in an isolated worktree only when it represents the actual pre-change state; do not reset, stash, or overwrite existing work.

Compare functions by file and symbol, accounting for an evident rename or move. A repository-wide warning count is not a baseline because one removed warning can hide one added warning.

## Local fallback

For C#, run the affected-project build before and after the edit. Add `--no-incremental` to the pre-change build unless the established command already guarantees compilation, then append this property, resolving the targets path from this reference directory:

```text
-p:CustomAfterMicrosoftCommonTargets=<deliver-ticket>/references/complexity.targets
```

The injected Roslyn `CA1502` check uses a cyclomatic-complexity limit of 25 and keeps that diagnostic at warning severity even when the project treats other warnings as errors. It changes only that command invocation and does not write project configuration. Do not replace an existing `CustomAfterMicrosoftCommonTargets` value; if the build already uses that extension point, mark the fallback `UNPROVEN`.

For JavaScript or TypeScript, invoke the repository's installed ESLint binary on the changed files with these command-line rules:

```sh
./node_modules/.bin/eslint <changed-files> \
  --rule 'complexity:["warn",{"max":20,"variant":"modified"}]' \
  --rule 'max-depth:["warn",{"max":4}]'
```

Do not use a package runner that can download ESLint. The fallback requires an existing compatible ESLint installation.

## Decide the result

Compare each touched function with its pre-change result under the same rule and threshold. Proof fails when:

- a new function exceeds a threshold;
- a previously compliant function crosses a threshold;
- a function that already exceeded a threshold increases its reported complexity or nesting; or
- the change adds a broad suppression.

Leave untouched legacy violations out of scope. For an unchanged violation in a touched function, report the result without expanding the ticket. When an inherently branch-heavy decision table or state machine remains readable, require focused behavior tests and a narrow documented exception, then report it.

Refactor along an existing responsibility boundary and rerun the affected behavior tests. Do not create pass-through helpers only to lower a metric.
