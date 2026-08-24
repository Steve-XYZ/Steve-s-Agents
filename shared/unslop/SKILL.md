---
name: unslop
description: Rewrite agent prose a person will read so it is specific, active, and free of LLM filler. Use when writing a pull request description, review comment, or report longer than a short status line. Loaded by deliver-ticket at finish. Do not use on code, diffs, command output, or checklists.
---

# Unslop

Read [WRITING.md](../global-guidance/WRITING.md) and apply it. This skill does not outrank being correct, in scope, and evidence-based.

## Do not ship

- A generated summary block (CodeRabbit or similar) as the PR body.
- An opener that would fit any other repository: "this PR introduces", "comprehensive", "robust", "seamless", "end-to-end solution".
- A claim without a file, test, command, or number next to it.
- Synonym cycling for the same thing ("the installer", "the script", "the helper").

## Do ship

- What changed, in the repository's language (BOS review comments: concise English, findings first).
- The Linear ticket when a BOS PR is requested.
- Validation actually executed, and what was not.
- Remaining risk in one line, or omit it.

Command results, diffs, file lists, and checklists stay terse. Do not unslop those.
