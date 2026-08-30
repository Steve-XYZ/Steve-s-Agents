---
name: unslop
description: Polish every user-facing response so it is specific, active, and free of LLM filler, including routine conversation, explanations, reviews, and delivery reports. Do not rewrite code, diffs, command output, file lists, or checklists unless the user asks.
---

# Unslop

Read [WRITING.md](../global-guidance/WRITING.md) and apply it while drafting every user-facing response. When the user supplies prose, rewrite it directly.

Preserve:

- meaning and factual claims,
- uncertainty and missing evidence,
- intended tone and audience,
- repository vocabulary and required format.

Do not add confidence, evidence, conclusions, or scope that the source does not contain. Do not rewrite code, diffs, command output, file lists, or checklists unless the user explicitly includes them in the prose task.

Return the response without narrating the editing pass unless the user asks for an explanation.
