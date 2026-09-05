# Prove It Works

Run the cheapest check that can go red on the behavior the ticket requires. Prove the requested change and the material behavior that must remain unchanged.

Test observable behavior through the existing public or integration boundary.
Derive expected values from the requirement, a worked example, or an independent
oracle, not the implementation's own calculation. Ask whether the assertion would
fail if the original defect returned. Work one behavior and its proof at a time;
do not bulk-write tests against an imagined implementation.

When repeated setup or fixture discovery blocks proof and tooling work is in
scope, read [project verification](project-verification.md). Put executable
knowledge in that project rather than expanding global framework guidance.

Use repository-native complexity rules when the normal affected build or lint command already enforces them. Read [local-complexity](local-complexity.md) and consider its fallback only when the final diff adds or reshapes material branching, nesting, state selection, retry, or failure coordination, or when a native diagnostic or reviewer has identified a concrete complexity risk. Routine changed functions do not justify a separate whole-project complexity pass.

Prefer, in order:

1. focused tests that exercise the invariant, target case, and relevant negative or preserved case;
2. affected project or module tests;
3. a throwaway local host and real request when tests cannot reach an API, money path, provider boundary, or contract;
4. the relevant build;
5. broader suites only when risk or repository CI justifies them.

Do not disturb a stack the user already has running. Use a throwaway port, database, or container. Do not hit shared, staging, production, or paid systems without explicit authorization.

For money, durable state, retries, migrations, concurrency, or partial failure, test the applicable failure class. For configuration or tenant-specific behavior, prove both the intended target and a non-target/default path. For an API or external contract, observe the response or serialized artifact rather than inferring it from source code.

For a changed shared state or predicate, confirm that at least one test executes the changed branch and would fail if the old behavior returned. Inspect every test project and fixture that seeds the affected state; a green changed-test project does not cover stale integration fixtures elsewhere.

Assertions must distinguish expected from actual state. A successful restore, green build, clean diff, or test that cannot fail for the changed behavior is not proof of the ticket. A relevant failure blocks completion unless the same command fails on the verified base for the same reason. Record the head/base delta; do not turn recurring baseline failures into a permanent exemption. Fix or explicitly quarantine them with an owner and follow-up outside the ticket when necessary.

Report the exact command, filter or request, observed result, and any path that remains unverified. Mark missing material evidence `UNPROVEN`.

Tie results to the tested commit or explicit working-tree state and retain output
needed by the next reviewer. Reuse valid evidence for unchanged behavior; a new
edit requires rechecking affected behavior, not automatically every suite.
