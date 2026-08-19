# Design Complexity

## Use when

Use this lens when a change chooses a public API, module boundary, responsibility owner, abstraction, or representation. Skip it when the repository already establishes the shape and the task simply extends that pattern.

## Decision questions

- What concepts must every caller understand, and which details can one module own completely?
- Does the proposed interface hide a meaningful mechanism or merely rename/delegate it?
- Where do important invariants live, and can the chosen owner enforce them without caller coordination?
- Which decision is likely to change, and how many places would that change reach?
- Are special cases evidence of a poor contract, or unavoidable domain behavior that should remain explicit?
- Does an abstraction simplify current uses, or depend on imagined future variation?
- Are errors expressed at the abstraction level where callers can act on them?

## Preferred defaults

- Minimize exposed concepts, not merely method count. Prefer an interface that lets callers state intent while the module owns sequencing, representation, and invariant enforcement.
- Keep volatile knowledge in one authoritative place. Do not duplicate policy across callers, adapters, reports, and exports.
- Pull complexity behind a boundary when the boundary can make behavior safer and easier to use correctly.
- Prefer a narrow design grounded in current requirements. Generalize only when existing variation demonstrates a stable common contract.
- Remove exceptional paths by clarifying semantics when possible; otherwise make exceptional behavior explicit and testable.
- Preserve established ownership boundaries unless moving one is necessary to fix a demonstrated problem.

## Evidence required

Compare designs against actual callers, current invariants, likely change points visible in the code or ticket, and existing failure behavior. Trace at least one representative call path. Favor evidence such as duplicated decisions, coordinated edits, leaked implementation details, invalid states callers can create, or a contract that cannot express required behavior. Record the concrete trade-off when one design improves one dimension while worsening another.

## Do not overapply

A small interface is not automatically a deep or good module, and a large module is not automatically wrong. Do not create wrappers, factories, layers, or generic frameworks solely to appear encapsulated. Do not reorganize working code because another shape is aesthetically cleaner. In review, "this could be more elegant" is not a finding; show how the current design causes incorrectness, material change propagation, misuse, or an explicit convention violation.
