# Engineering writing: GitHub artifact boundaries

## Scope and sources

Base: `eb249359edfe3393cffacd05afa3b7b0d64e3c4a` (`main`). Candidate: the uncommitted `feat/engineering-writing` working tree. Frozen candidate skill SHA-256: `b32b78eed8a14548d208a98f03f56086fa04a2ba295b767258b913050ff07675`; candidate unslop SHA-256: `0317c1f3096185ac4178558950582650728e955a8f242824b84aeab85076e756`.

Compared pstack's [unslop](https://github.com/cursor/plugins/blob/70b2dc8b4b85c8d5648624ca40d692c421fff32f/pstack/skills/unslop/SKILL.md) and [technical-writing](https://github.com/cursor/plugins/blob/70b2dc8b4b85c8d5648624ca40d692c421fff32f/pstack/skills/technical-writing/SKILL.md). Adapted rules 32 and 33 into the local numbering and reused the dependency pattern. Kept local language rules, frontmatter, examples, and other customizations. The upstream removals and formatting changes did not justify replacing them; its broader documentation workflow is outside this request.

The draft's optional severity label conflicts with `code-review`'s Nit/follow-up classification. The new skill delegates classification rather than restating or renaming it. It also preserves evidence fields and material uncertainty, and retains deferred or evidence-dependent reply dispositions. The only ordering change in `code-review` removes an instruction to end with validation and verdict, so the GitHub footer can come last.

## Method

Five fresh native Codex agents per variant, Codex CLI `0.161.0` in T3 Code, `gpt-6.1-sol` with medium reasoning from the usable verifier profile. Same raw engineering record, output filenames, host, tools, and model settings. No custom token budget. The baseline explicitly invoked frozen existing `unslop`; the candidate explicitly invoked `engineering-writing` and its frozen `unslop` dependency. The candidate includes both additions, so this comparison does not isolate the effect of unslop rules 32 and 33.

Agents received only the raw task, the allowed skill paths, and the output directory. They did not receive expected outcomes or the author's conclusions. Each wrote six local drafts. No application review, tests, browser work, or GitHub publication was assigned. The applications and test results below are supplied writing facts, not verification performed by these agents.

Read every draft and inspected actual tool calls in the native transcripts. Baseline agents read the task and existing unslop. Candidate agents read the task and both writing skills once. They did not read the phase skills or change application code. Scratch inputs, frozen guidance, and outputs remain at `/var/folders/hc/27jsz_dj46d_36mcj7cxdsm00000gn/T/engineer-notes-loq2k3sb`; transcripts remain under `/Users/stive/.codex/sessions/2026/10/08/`.

## Observed results

The baseline already preserved technical facts, reproduction evidence, and verification gaps. All five candidate samples also retained the request-changes verdict, one blocker, one should-fix, and one optional finding; they kept the existing Nit/follow-up label. Comments retained the file location, month-switch trigger, March-to-April reproduction, consequence, and correction. Accepted replies retained fail-before/pass-after evidence and the browser gap. Rejected replies retained the backend role check and direct-call HTTP 403 evidence.

All ten candidate PR descriptions/full summaries placed an explicit Merge Danger section last. None of the twenty candidate inline comments/replies added that section. The baseline had no explicitly named Merge Danger footer, and only one of its five full summaries ended with recovery consequences; the others ended with validation. Two baseline summaries omitted the recovery consequence from the body even though their inline comments retained it. Candidate footers retained rollback limitations and unexercised recovery without inventing a safety rating.

Total draft words increased from a median of 388 to 432. This supports consistent artifact structure and evidence retention on this fixture, not a claim of fewer total words. Inline blocker comments still used more than two sentences to carry the supplied evidence and persistent-data impact. The default length did not override required evidence.

| Sample | Before words | Seconds | Input tokens | Output tokens | After words | Seconds | Input tokens | Output tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 414 | 37.8 | 100759 | 1114 | 432 | 42.3 | 102448 | 1224 |
| 2 | 372 | 35.6 | 100730 | 1002 | 431 | 33.5 | 102238 | 1128 |
| 3 | 388 | 36.6 | 100596 | 1224 | 425 | 36.8 | 101681 | 1105 |
| 4 | 412 | 35.2 | 100734 | 1005 | 433 | 34.3 | 102043 | 1059 |
| 5 | 376 | 34.1 | 100297 | 963 | 443 | 38.3 | 102208 | 1137 |

Token counts are native cumulative totals for each initial task, including harness/tool overhead and cached input. They do not establish dollar cost or an efficiency improvement. There was no intervention or rewriting during the ten samples.

A fresh negative task supplied a two-skill catalog and asked for an internal report. Its tool calls read only unslop, and its output preserved verification gaps without a Merge Danger section. This is supplied-catalog selection, not installed host routing.

A continuation of the first candidate task asked for a PR description of a destructive migration despite the author's small-diff/green-tests low-risk claim. It did not reread either skill. Its last section stated that rollback cannot recreate rows and recovery is unverified. This checks loaded-guidance reuse and pressure handling in one continued context, not a fresh independent pressure sample.

## Representative full summary

Baseline sample 1:

```markdown
Request changes. The review found one blocker, one should-fix, and one optional nit. The inline findings describe the details.

The blocker can persist an approval against the wrong month. Reverting the UI cannot undo that transaction. An operator would need to identify incorrect approvals and reverse them through the existing correction process, which was not exercised. The should-fix leaves an indefinite spinner after a failed fetch. The naming suggestion is not a merge blocker.

Vitest passed all 8 tests, and the production build succeeded. A local interaction reproduced the March-to-April submission, and a simulated network failure reproduced the spinner. End-to-end browser validation and the operator correction flow were not run. The automated results do not establish either.
```

Candidate sample 1:

```markdown
Request changes. The review found one blocker, one should-fix, and one nit/follow-up.

The blocker allows an old row's amount to be approved against a newly selected month. The should-fix leaves the screen showing an indefinite spinner after a failed fetch. The naming suggestion is optional and does not block merging. Inline comments contain the detailed findings.

Vitest passed all 8 tests, and the production build succeeded. A local interaction reproduced the stale-period submission, and a simulated network-failure test reproduced the indefinite spinner. End-to-end browser validation and the operator correction flow were not run. The automated tests do not establish those missing checks.

## Merge Danger

Merging with the blocker allows incorrect approvals to persist. Reverting the UI cannot undo submitted transactions. Recovery requires an operator to identify incorrect approvals and reverse them through the existing correction process; that process was not exercised.
```

## Validation and limits

- `python3 scripts/validate-skills.py`: catalog, metadata presence, references, and routing fixture structure passed.
- `python3 scripts/test-install-agent-links.py`: 8 tests passed, using disposable installations; discovery includes the new skill without installer changes.
- `python3 scripts/test-workflow-helpers.py`: 31 tests passed.
- `git diff --check`: passed.
- The separate skill-creator `quick_validate.py` could not start because this Python lacks PyYAML. No dependency was installed.

The new routing fixtures cover four artifact types, the three workflow boundaries, unsafe recovery claims, loaded-guidance reuse, and negative internal/status/general-writing routes. Their structure passed; the delivery/review/triage boundary cases were not executed as complete workflows. Automatic installed-host discovery, Claude/OpenCode behavior, actual GitHub publishing, and downstream workflow effectiveness remain untested. The internal sample and migration continuation each ran once. Five paired samples used one fixture, with no blinded grader or holdout corpus; they do not establish broad comparative effectiveness.

No global engineering guidance, installer behavior, machine configuration, model profile, or active skill installation changed.

## Transcript locators

- `writing_after_2`: `rollout-2026-10-08T15-22-21-01a11cf7-71d3-7e40-8493-fcd74806ae7e.jsonl`
- `writing_before_5`: `rollout-2026-10-08T15-24-04-01a11cf9-07f8-71e2-8424-3e4edd1dd1ad.jsonl`
- `writing_before_2`: `rollout-2026-10-08T15-22-16-01a11cf7-6211-7440-a87f-23d1a5062579.jsonl`
- `writing_after_3`: `rollout-2026-10-08T15-23-04-01a11cf8-1c80-7ec1-bb83-4728129b5b65.jsonl`
- `writing_before`: `rollout-2026-10-08T15-14-04-01a11cef-e006-7f02-a5d4-4b8bfcc8cf93.jsonl`
- `writing_after_5`: `rollout-2026-10-08T15-24-09-01a11cf9-1986-7542-88d7-fd4fc222c09d.jsonl`
- `writing_before_3`: `rollout-2026-10-08T15-22-25-01a11cf7-8307-7662-a70c-677ad5dd502b.jsonl`
- `writing_after_4`: `rollout-2026-10-08T15-23-14-01a11cf8-40cc-7c33-a6fe-7499c46af039.jsonl`
- `writing_before_4`: `rollout-2026-10-08T15-23-09-01a11cf8-306a-7262-a081-9684ab3bed18.jsonl`
- `writing_internal`: `rollout-2026-10-08T15-20-16-01a11cf5-89d6-7fe2-8457-1889f4073fe0.jsonl`
- `writing_after`: `rollout-2026-10-08T15-19-32-01a11cf4-df53-7f12-9a59-0973374f6e26.jsonl`
