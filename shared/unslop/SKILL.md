---
name: unslop
description: Rewrite prose the user supplies. Use only when the user pastes text and asks to tighten, clean up, or unslop it. The rules for your own output load unconditionally from global guidance and need no invocation.
---

# Unslop

The writing rules are already in context, under `## Writing` in the global engineering guidance. Apply them to the text the user supplied — not to your own surrounding response, which already follows them.

Keep meaning and factual claims, uncertainty and missing evidence, intended tone and audience, and repository vocabulary and required format. Do not add confidence, evidence, conclusions, or scope the source does not contain. Do not touch code, diffs, command output, file lists, or checklists unless the user includes them in the task.

Return the result without narrating the editing pass.
