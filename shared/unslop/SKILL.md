---
name: unslop
description: Rewrite user-facing prose so it is specific, active, and free of LLM filler. Use only when the user invokes unslop or explicitly asks to rewrite prose. Do not auto-select for routine conversation, code, diffs, command output, or checklists.
disable-model-invocation: true
---

# Unslop

Read [WRITING.md](../global-guidance/WRITING.md) and apply it to the supplied prose.

Preserve:

- meaning and factual claims,
- uncertainty and missing evidence,
- intended tone and audience,
- repository vocabulary and required format.

Do not add confidence, evidence, conclusions, or scope that the source does not contain. Do not rewrite code, diffs, command output, file lists, or checklists unless the user explicitly includes them in the prose task.

Return the rewritten prose without narrating the editing pass unless the user asks for an explanation.
