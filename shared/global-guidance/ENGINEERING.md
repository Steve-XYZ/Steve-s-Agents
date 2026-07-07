# Engineering Defaults

## Communication

- Be direct, concise, and evidence-based.
- Start with the result or next action; do not restate the task or narrate routine reads, searches, or commands.
- Plan before editing only when the task is ambiguous, crosses module or contract boundaries, changes schema/data, affects deployment, or has material risk.
- Surface only material assumptions, blockers, trade-offs, or missing evidence.
- Explain decisions only when they are non-obvious, risky, irreversible, or requested.
- Prefer actionable findings over general advice.

## Change Discipline

- Repository instructions and established conventions override these defaults.
- Keep changes minimal, cohesive, and reviewable.
- Reuse existing platform features and repository dependencies before adding new ones.
- Do not introduce dependencies, abstractions, layers, or configuration without a demonstrated need.
- Do not refactor unrelated code while implementing a ticket.
- Use the narrowest reliable validation; add or run tests when they prove the changed behavior.

## Final Response

For implementation, bug fixes, or reviews, report only:
1. What changed or what was found.
2. Validation performed.
3. Material blockers, risks, or follow-ups.

Include files touched only when useful for review.
Include a commit or PR summary only when requested, preparing a commit/PR, or the change is substantial.

## Skills

- Use an available skill when its trigger clearly matches the task.
- Do not invoke a skill merely because it is available.
- Keep skill instructions scoped to their stated purpose.
