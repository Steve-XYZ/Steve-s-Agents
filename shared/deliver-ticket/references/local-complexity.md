# Local Complexity Guardrail

Use complexity as local delivery evidence, not as permission to change repository policy. Do not add analyzer packages, configuration, suppressions, or CI steps to the target repository unless the ticket explicitly requires a shared rule.

## Select the check

Inspect the repository's analyzer or linter configuration and established commands. Track cyclomatic complexity, cognitive complexity, and nesting depth as separate dimensions.

- Run every repository-native dimension through the affected build or lint command. Its configured metric and threshold are authoritative for that dimension.
- Use the local fallback only for a dimension the repository does not enforce: C# can fill cyclomatic complexity; JavaScript and TypeScript can fill cyclomatic complexity and nesting depth. Cognitive complexity is complementary and does not disable either fallback dimension.
- Use a fallback only when the required SDK or installed linter is already available. Do not install a tool or modify the repository to make it work. Mark each unavailable dimension `UNPROVEN`.

## Check final code first

Run the selected checks on the final changed functions. If none violates its threshold, stop; no baseline pass is needed.

Only when a final function violates a threshold, run the same metric and threshold against its actual pre-change version. Use the verified task base in an isolated worktree when it represents that state. If the function was already dirty before delivery or its pre-change state will otherwise be unrecoverable, retain its source or diagnostic before editing. Do not reset, stash, or overwrite existing work. Mark the comparison `UNPROVEN` if the actual pre-change function cannot be recovered.

Compare functions by file and symbol, accounting for an evident rename or move. A repository-wide warning count is not a baseline because one removed warning can hide one added warning.

## Local fallback

For a missing C# cyclomatic check, run the affected-project build below. Resolve the targets path from this reference directory. Keep `--no-incremental` on every diagnostic pass so Roslyn must emit fresh analyzer diagnostics.

```sh
dotnet build <project> --no-incremental \
  -p:EnableNETAnalyzers=true \
  -p:RunAnalyzersDuringBuild=true \
  -p:CustomAfterMicrosoftCommonTargets=<deliver-ticket>/references/complexity.targets
```

The injected Roslyn `CA1502` check uses a cyclomatic-complexity limit of 25 and keeps that diagnostic at warning severity even when the project treats other warnings as errors. It changes only that command invocation and does not write project configuration. Do not replace an existing `CustomAfterMicrosoftCommonTargets` value; if the build already uses that extension point, mark the fallback `UNPROVEN`.

Before accepting a clean C# result, verify the evaluated build includes this reference directory's `complexity.globalconfig` as an `EditorConfigFiles` item, `CodeMetricsConfig.txt` as an `AdditionalFiles` item, and the SDK's .NET analyzer assembly. When the installed MSBuild supports evaluation queries, obtain that evidence without another build:

```sh
dotnet msbuild <project> --nologo \
  -p:EnableNETAnalyzers=true \
  -p:RunAnalyzersDuringBuild=true \
  -p:CustomAfterMicrosoftCommonTargets=<deliver-ticket>/references/complexity.targets \
  -getProperty:NoWarn,CodeAnalysisRuleSet \
  -getItem:EditorConfigFiles,AdditionalFiles,Analyzer
```

Inspect the evaluated `NoWarn`, applicable `.editorconfig` files, and any ruleset for an effective `CA1502` suppression. `global_level = 999` wins only against other global configs; a repository `.editorconfig` or compiler `NoWarn` can still suppress it. If the analyzer inputs or absence of suppression cannot be established, mark cyclomatic complexity `UNPROVEN` even when the build succeeds.

For missing JavaScript or TypeScript dimensions, invoke the repository's installed ESLint binary on the changed files with the applicable command-line rule:

```sh
./node_modules/.bin/eslint <changed-files> \
  --rule 'complexity:["warn",{"max":20,"variant":"modified"}]'

./node_modules/.bin/eslint <changed-files> \
  --rule 'max-depth:["warn",{"max":4}]'
```

Combine the rules when both dimensions are missing. If the installed ESLint rejects the `variant` option, rerun cyclomatic complexity with the compatible classic form below and use that same form for any baseline comparison. Report that the classic metric was used. If one rule remains unusable, mark only that dimension `UNPROVEN` and still run the other.

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
