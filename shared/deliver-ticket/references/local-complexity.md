# Local Complexity Guardrail

Use complexity as local delivery evidence when the diff creates a concrete readability or verification risk, not as a mandatory metric for every changed function or as permission to change repository policy. Do not add analyzer packages, configuration, suppressions, or CI steps to the target repository unless the ticket explicitly requires a shared rule.

Verified end to end on 2026-09-04. With .NET SDK 10.0.400 the injection below
emitted `CA1502: 'Pick' has a cyclomatic complexity of '40' ... below '26'` on a
project that built with zero warnings without it. With ESLint 10.10.0 all three
rule forms fired on a function of complexity 31 and nesting depth 5, including
the `variant: "modified"` option. Read counts cannot condemn this file: the
gates are narrow by design, so no opens means no gate opened, not that the
harness is broken.

## Decide whether to run

Inspect the repository's analyzer or linter configuration and established commands. Run repository-native rules through the normal affected build or lint command when they already apply. Use a local fallback only when at least one of these is true:

- a new or materially expanded production function adds or reshapes branching, nesting, state selection, retry, or failure coordination;
- a repository-native diagnostic already identifies the changed function; or
- the delivery brief or a reviewer names that function's control flow as a material risk.

Skip generated or vendored code, migration designers and snapshots, declarations, and test builders or fixtures unless their control flow itself makes required behavior hard to verify. Do not mark an irrelevant or intentionally skipped metric `UNPROVEN`.

Track only the dimensions that apply to the named risk. The repository's configured metric and threshold are authoritative for each native dimension. A local fallback can supply C# cyclomatic complexity or JavaScript and TypeScript cyclomatic complexity and nesting depth. Cognitive complexity is independent; do not claim it was measured when no native rule provides it.

Use a fallback only when the required SDK or installed linter is already available. Do not install a tool or modify the repository to make it work. If a named material risk cannot be measured, mark that risk `UNPROVEN`; otherwise report that the optional fallback was not run without weakening the ticket's evidence.

## Check final code first

Run the selected checks on the final changed production functions. Retain only diagnostics for the changed symbols plus the command result; do not load or report the affected project's unrelated legacy warnings. If no changed function violates its threshold, stop; no baseline pass is needed.

Only when a final function violates a threshold, run the same metric and threshold against its actual pre-change version. Use the verified task base in an isolated worktree when it represents that state. If the function was already dirty before delivery or its pre-change state will otherwise be unrecoverable, retain its source or diagnostic before editing. Do not reset, stash, or overwrite existing work. Mark the comparison `UNPROVEN` if the actual pre-change function cannot be recovered.

Compare functions by file and symbol, accounting for an evident rename or move. A repository-wide warning count is not a baseline because one removed warning can hide one added warning.

## Local fallback

For a named C# cyclomatic risk that the repository does not measure, run the affected-project build below. Resolve the targets path from this reference directory. Keep `--no-incremental` on every diagnostic pass so Roslyn must emit fresh analyzer diagnostics. Reuse this as the required affected-project build when possible rather than running an equivalent build twice.

```sh
dotnet build <project> --no-incremental \
  -p:EnableNETAnalyzers=true \
  -p:RunAnalyzersDuringBuild=true \
  -p:CustomAfterMicrosoftCommonTargets=<deliver-ticket>/references/complexity.targets
```

The injected Roslyn `CA1502` check uses a cyclomatic-complexity limit of 25 and keeps that diagnostic at warning severity even when the project treats other warnings as errors. It changes only that command invocation and does not write project configuration. Do not replace an existing `CustomAfterMicrosoftCommonTargets` value; if the build already uses that extension point, mark the named complexity risk `UNPROVEN`.

Before accepting a clean C# result, verify the evaluated build includes this reference directory's `complexity.globalconfig` as an `EditorConfigFiles` item, `CodeMetricsConfig.txt` as an `AdditionalFiles` item, and the SDK's .NET analyzer assembly. When the installed MSBuild supports evaluation queries, obtain that evidence without another build:

```sh
dotnet msbuild <project> --nologo \
  -p:EnableNETAnalyzers=true \
  -p:RunAnalyzersDuringBuild=true \
  -p:CustomAfterMicrosoftCommonTargets=<deliver-ticket>/references/complexity.targets \
  -getProperty:NoWarn,CodeAnalysisRuleSet \
  -getItem:EditorConfigFiles,AdditionalFiles,Analyzer
```

Inspect the evaluated `NoWarn`, applicable `.editorconfig` files, and any ruleset for an effective `CA1502` suppression. `global_level = 999` wins only against other global configs; a repository `.editorconfig` or compiler `NoWarn` can still suppress it. If the analyzer inputs or absence of suppression cannot be established, mark the named cyclomatic risk `UNPROVEN` even when the build succeeds.

For a named JavaScript or TypeScript risk that native rules do not measure, invoke the repository's installed ESLint binary on the changed production files with the applicable command-line rule:

```sh
./node_modules/.bin/eslint <changed-files> \
  --rule 'complexity:["warn",{"max":20,"variant":"modified"}]'

./node_modules/.bin/eslint <changed-files> \
  --rule 'max-depth:["warn",{"max":4}]'
```

Combine the rules when both dimensions are material. If the installed ESLint rejects the `variant` option, rerun cyclomatic complexity with the compatible classic form below and use that same form for any baseline comparison. Report that the classic metric was used. If one required rule remains unusable, mark only that named dimension `UNPROVEN` and still run the other.

```sh
./node_modules/.bin/eslint <changed-files> \
  --rule 'complexity:["warn",20]'
```

Do not use a package runner that can download or upgrade ESLint.

## Decide the result

For each final violation, compare the touched function with its pre-change result under the same rule, variant, and threshold. Proof fails when:

- a new function exceeds a threshold;
- a previously compliant function crosses a threshold;
- a function that already exceeded a threshold increases its reported complexity or nesting; or
- the change adds a broad suppression.

Leave untouched legacy violations out of scope. For an unchanged violation in a touched function, report the result without expanding the ticket. When an inherently branch-heavy decision table or state machine remains readable, require focused behavior tests and a narrow documented exception, then report it.

Refactor along an existing responsibility boundary and rerun the affected behavior tests. Do not create pass-through helpers only to lower a metric.
