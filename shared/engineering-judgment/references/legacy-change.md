# Legacy Change

## Use when

Use this lens when the required behavior lives in poorly understood, weakly tested, tightly coupled, or side-effect-heavy code and an edit cannot be validated. Skip it when an existing test seam proves the affected behavior.

## Decision questions

- What observable behavior must remain unchanged, and what behavior is intentionally changing?
- Which real caller reaches the change point, with what inputs and side effects?
- What is the narrowest feedback signal that can detect an accidental behavior change?
- Can a dependency or decision be intercepted at an existing boundary before adding a new one?
- Which enabling edit is needed to gain control or observability, and can it remain behavior-preserving?
- Are current outputs intentional requirements, historical accidents, or unknowns that need clarification?
- Does the proposed test observe behavior, or merely mirror implementation details?

## Preferred defaults

- Characterize the affected path through its real public or integration boundary before changing it when practical.
- Introduce the smallest seam that permits deterministic control of the problematic dependency or decision.
- Separate a mechanical enabling edit from the behavior change when doing so makes equivalence and review materially clearer.
- Preserve unrelated behavior, including awkward edge cases, until evidence or the requirement authorizes changing it.
- Prefer extraction, parameterization, wrapping, or a narrow adapter only when it creates a usable feedback seam for this change.
- Use captured requests, fixtures, logs, or base-versus-head comparison when a conventional unit test cannot honestly reach the behavior.

## Evidence required

Identify the real caller, change point, dependency boundary, and observable result. Demonstrate the baseline with a focused test, replay, captured payload, or static call-path proof. For a bug fix, observe the regression signal fail before the fix when practical and safe. If that is impossible, state what remains unverified and why. Verify that any enabling refactor preserves behavior independently of the intended change.

## Do not overapply

Do not demand broad characterization coverage, refactor an entire class, or replace a subsystem before making a local change. A characterization test records behavior; it does not declare every observed result correct. Avoid seams that exist only to satisfy mocking tools, and avoid mocks that reproduce the implementation. Do not call code "legacy" as a review finding. Report the concrete risk: an unverified behavior change, unreachable test seam, hidden side effect, or dependency that prevents reliable validation.
