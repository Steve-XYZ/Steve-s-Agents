---
name: prove-it-works
description: Prove a change against the cheapest honest artifact. A green build is not proof. Use after implementing a ticket and before claiming success. Loaded by deliver-ticket. Do not use as a substitute for diagnosis, and do not treat inspection as execution.
---

# Prove It Works

Run the cheapest check that can go red on the behavior the ticket requires. Report exactly what ran. If a check could not be run, say so; do not imply it passed.

## 1. Choose the seam

Prefer, in order:

1. a focused test that exercises the invariant, including the negative case a guard claims to catch,
2. the affected project or module tests,
3. a throwaway local host and a real request (`curl` or equivalent) when the change is an API, money path, or contract the tests cannot reach,
4. the relevant build.

Broader suites only when risk or repository CI justifies them.

Do not disturb a stack the user already has running. Use a throwaway port, database, or container. Do not hit shared, staging, or production systems.

## 2. What counts

- A test of the invariant, not only the happy path. If a catalogue, seed, or allow-list guard was added, a case that must fail has to fail.
- For money, stamps, retries, or partial failure: a test of that class, or an explicit statement that no honest seam exists.
- For an API contract: the response shape actually observed, not the shape assumed from the code.
- Assertions should name expected versus actual state. `Assert.True(ok)` is not evidence.

A green build, a clean diff, or a successful restore is not proof of the ticket.

## 3. Report

State the commands, the filter or request used, and the result. Name any path that remains unverified. Then stop; `deliver-ticket` continues with self-review.
