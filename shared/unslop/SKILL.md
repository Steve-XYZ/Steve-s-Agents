---
name: unslop
description: Polish user-facing prose while drafting a requested deliverable, or rewrite supplied prose so it is specific, active, and free of LLM filler. Use only when the user invokes unslop or explicitly asks for a rewrite. Do not auto-select for routine conversation, code, diffs, command output, or checklists.
disable-model-invocation: true
---

# Unslop

Read [WRITING.md](../global-guidance/WRITING.md). When prose does not exist yet, apply it while drafting the final output in the current task. When the user supplies prose, rewrite it directly.

Preserve:

- meaning and factual claims,
- uncertainty and missing evidence,
- intended tone and audience,
- repository vocabulary and required format.

Do not add confidence, evidence, conclusions, or scope that the source does not contain. Do not rewrite code, diffs, command output, file lists, or checklists unless the user explicitly includes them in the prose task.

Return the rewritten prose without narrating the editing pass unless the user asks for an explanation.
