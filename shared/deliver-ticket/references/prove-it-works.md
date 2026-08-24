# Prove It Works

Run the cheapest check that can go red on the behavior the ticket requires. Prove the requested change and the material behavior that must remain unchanged.

Prefer, in order:

1. focused tests that exercise the invariant, target case, and relevant negative or preserved case;
2. affected project or module tests;
3. a throwaway local host and real request when tests cannot reach an API, money path, provider boundary, or contract;
4. the relevant build;
5. broader suites only when risk or repository CI justifies them.

Do not disturb a stack the user already has running. Use a throwaway port, database, or container. Do not hit shared, staging, production, or paid systems without explicit authorization.

For money, durable state, retries, migrations, concurrency, or partial failure, test the applicable failure class. For configuration or tenant-specific behavior, prove both the intended target and a non-target/default path. For an API or external contract, observe the response or serialized artifact rather than inferring it from source code.

Assertions must distinguish expected from actual state. A successful restore, green build, clean diff, or test that cannot fail for the changed behavior is not proof of the ticket.

Report the exact command, filter or request, observed result, and any path that remains unverified. Mark missing material evidence `UNPROVEN`.
