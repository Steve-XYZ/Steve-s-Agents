# Workflow foundation

This update applies the September 2026 practitioner research to PR #7. It preserves the ticket/outcome distinction and subtraction review already in that PR. It changes the execution loop, context boundaries, and evidence handling.

## Decisions and evidence

| Decision | Failure prevented | Source inspected |
| --- | --- | --- |
| Choose proof for the next behavior, implement it, then reassess | Completing an imagined solution before learning from behavior | [Compound implementation loop](https://github.com/EveryInc/compound-engineering-plugin/blob/6be0932b91dc369508da19e6e2bc753b4c038830/skills/ce-work/references/implementation-loop.md) |
| Observe a relevant failure for a feasible material regression | Tests that pass without detecting the original defect | [Superpowers TDD](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/test-driven-development/SKILL.md) |
| Keep contexts and tools optional except where a defined risk requires review | Paying for repeated discovery and orchestration on simple work | [Pi plan extension](https://github.com/earendil-works/pi/blob/890f920884f6d21fc7617d236ef9e1cc5d7a0ef8/packages/coding-agent/examples/extensions/plan-mode/index.ts), [Compound review-cost investigation](https://github.com/EveryInc/compound-engineering-plugin/blob/6be0932b91dc369508da19e6e2bc753b4c038830/docs/solutions/skill-design/review-cost-is-in-entering-the-spine-not-the-findings.md) |
| Keep non-obvious contracts near their owner | A local fix missing required exports, readers, or architectural constraints | [Ghostty C API rules](https://github.com/ghostty-org/ghostty/blob/3c47ca159368eb4a860ffe5333abdf4a85b2767b/src/terminal/c/AGENTS.md), [OpenCode tool rules](https://github.com/anomalyco/opencode/blob/c10134729dd2ce00beb18604ec91f10319f59a78/packages/core/src/tool/AGENTS.md) |
| Prove the actual runtime interaction and build identity | Startup or stale binaries counted as functional evidence | [Pi interactive testing](https://github.com/earendil-works/pi/blob/890f920884f6d21fc7617d236ef9e1cc5d7a0ef8/.pi/skills/interactive-testing.md), [Tidewave runtime tool](https://github.com/tidewave-ai/tidewave_phoenix/blob/82fe4d2acf541d6b503ff7500dd20c83c9d3bf34/lib/tidewave/mcp/tools/eval.ex) |
| Separate CI observations from human gates and reject stale snapshots | Waiting forever for approval or reusing checks from another head | [Sentry iteration fix](https://github.com/getsentry/skills/commit/32fdf36273ac530120134ac484b3ab09717f3410) |
| Route repeated failures to code, tests, local knowledge, or nothing | An expanding global lessons file | [VS Code feedback learning](https://github.com/microsoft/vscode/blob/fc0256deff8a612de2bdb07b3d748299f15f2b63/.github/skills/feedback-learning/SKILL.md) |
| Track the version and owner of specialized knowledge | Stale dependency guidance and conflicting generated references | [UsageRules collision fix](https://github.com/ash-project/usage_rules/commit/2f02ce8481aa816028db2e173b656f3289ac0f33) |
| Review ownership and removable paths beyond the patch | A correct addition leaving duplicate policy or dead code | [Peter Steinberger's deep review](https://github.com/steipete/agent-scripts/blob/95d8d8694953eb82ccbbb33b9b17b1e1f04ebc28/skills/github-deep-review/SKILL.md) |

These sources show implementations and reported failures. They do not prove a productivity gain in this setup. The specific risk triggers and five-entry-point design are local choices to evaluate.

## Placement

- Global instructions retain authority, scope, judgment, and honest evidence.
- Five existing skills handle delivery, shaping, diagnosis, review, and feedback. The name `shape-feature` stays stable for installed links, while its trigger now covers existing systems.
- Conditional references hold impact tracing, failure reasoning, proof, and work-context recovery. Small tickets do not load the entire chain.
- Root and nested project instructions identify commands, invariants, diagnostics, owners, and versioned knowledge.
- Review packaging and PR-state collection enforce mechanical facts. They never infer business correctness or grant merge approval.
- Task trials and helper tests check different claims. See [evaluation guidance](../evals/README.md).

## Deliberate exclusions

No full framework import, mandatory detailed plan, per-slice fresh implementer, default reviewer panel, test-for-every-function rule, forced refactoring, or universal worktree setup. Do not add a hook until a recurring deterministic failure justifies it.

One behavioral slice can span several safe PRs or deployments. Keep rollout constraints explicit instead of treating a vertical slice as an atomic release.

## Project-owned work

This repository supplies guidance and reference configurations. It cannot establish the BOS applications' current runtime commands, database isolation, test hosts, log paths, or provider behavior. Inspect and improve those capabilities in the repository that owns them when a task needs them. No application-specific tool or dependency generator is added on speculation.

Editing `configs/` does not install it on macOS or WSL. Host-specific skill discovery, permissions, and automatic routing need checks in those actual hosts. Fresh explicit-invocation trials do not establish cross-host routing or comparative productivity.
