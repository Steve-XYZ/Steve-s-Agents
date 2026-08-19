# Construction

## Use when

Use this lens when implementing or reviewing a non-trivial routine, state transition, parser, algorithm, validation boundary, error policy, or data representation. Skip it for simple idiomatic plumbing already governed by repository conventions.

## Decision questions

- What preconditions, postconditions, and invariants define correct behavior?
- Which inputs cross a trust boundary, and which impossible states indicate a programmer error?
- Is the normal path easy to follow, and are side effects ordered deliberately?
- Does the chosen representation make valid states natural and invalid states difficult to construct?
- At what abstraction level can an error be handled meaningfully without losing context?
- Would a stable mapping be clearer as data than as repeated branching?
- Which branches, transitions, and failure modes need direct tests?
- Is any optimization or compact expression hiding behavior that should remain inspectable?

## Preferred defaults

- Choose names, types, and structures that expose intent and relevant invariants.
- Keep the normal path visible; use guards, helpers, or local decomposition only when they reduce the reasoning burden.
- Validate untrusted input at the boundary. Use invariant checks for impossible internal states and domain outcomes for expected business failures.
- Handle errors where the code has enough context to choose a recovery or translation; otherwise preserve context and propagate them.
- Limit mutable state and derive repeated values from one authoritative calculation.
- Use table-driven logic for stable, inspectable mappings, but keep complex behavior in code when encoding it as data would obscure control flow.
- Comment rationale, constraints, and surprising trade-offs rather than narrating statements.

## Evidence required

Walk representative normal, boundary, and failure cases through the implementation. Tie concerns to a reachable branch, ambiguous state, swallowed context, duplicated rule, or test gap. Use compiler/static checks and focused tests to validate the decisive paths. Measure before changing code for performance, and compare before/after behavior when restructuring a complex routine.

## Do not overapply

Do not enforce arbitrary limits on routine length, parameters, nesting, files, or classes. Extraction is harmful when it fragments one coherent operation or hides ordering. Do not add defensive checks at every internal call, speculative null handling, or exceptions for states that types and callers already exclude. In review, style preference, unfamiliar syntax, or possible elegance is not a finding without demonstrated defect risk or a violated local rule.
