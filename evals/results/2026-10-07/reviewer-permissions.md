# Reviewer execution permissions

The captured failure predates this guidance change. In T3 thread `1c172fe3-bb30-4f5c-b5f9-6bb17358a619`, activity item 120 launched the reviewer with `role: "review"` and `runtimeMode: "approval-required"`, despite the parent's `full-access` mode. Claude's session `987005c6-9bb1-4efb-938a-4501ecc83801` records `permissionMode: "bypassPermissions"`.

The resulting Codex session `01a116a3-7511-70e3-a648-b721d947559e` records `approval_policy: "untrusted"` and `sandbox_policy: {"type": "read-only"}`. Its delegated task ends in `bos-2669-review-round-1`. The host recorded 32 command approval requests for that child and none for its parent. Child activity items 34 and 36 show ordinary `dotnet test --no-build --no-restore` commands failing because MSBuild could not create a temporary directory. These session records and failures are the control evidence, rather than a newly repeated run that would ask the user to approve commands again.

The fix belongs in `code-review`: preserve the parent's authorized mode and keep source edits and external writes outside the assignment. `deliver-ticket` now loads that skill before launching a reviewer. Assigned validation may create local scratch, caches, and build outputs. Explicit permission limits still apply.

## Disposable reviewer

The current parent launched a fresh T3-owned reviewer through Codex CLI `0.160.1` with `role: "review"`, `runtimeMode: "inherit"`, provider `codex`, model `gpt-6.1-sol`, and `reasoningEffort: "high"`. The model source was the usable reviewer entry in `~/.config/agents/model-profiles.toml`, checked against the live catalog. The task request ID is `reviewer-permissions-20261007-inherited-round-1`; its task and child thread IDs contain that suffix and command ID `5096cd0b-fec9-4b94-a03d-079a1ac18b75`.

The brief explicitly invoked the updated `code-review` skill, supplied the raw user requirement and the two skill diffs on base `2e79623`, and prohibited source edits, commits, pushes, external feedback, runtime changes, and further delegation. It allowed only local validation outputs. The additional checkout came from:

```sh
python3 evals/make-task-fixture.py discounts --output /tmp/checkout-percentage-review-20261007 --skill code-review
```

The reviewer was asked to read that checkout's instructions and ticket, review its latest commit, and run its documented validation. Expected findings and this diagnosis were not supplied. Its four green tests were not treated as proof that the checkout met its ticket.

The reviewer itself ran all four commands below. All returned exit 0:

- `python3 scripts/validate-skills.py`: catalog, references, and routing fixture structure passed.
- `python3 scripts/test-install-agent-links.py`: 8 tests passed.
- `python3 scripts/test-workflow-helpers.py`: 31 tests passed, using disposable filesystem fixtures.
- `python3 -m unittest discover -v` in the disposable checkout: 4 tests passed.

The new child inherited `full-access`. Its native session `01a11707-8c27-7d02-9bdc-9137f50596ba` records `approval_policy: "never"` and `sandbox_policy: {"type": "danger-full-access"}`. The parent's native session `01a11704-5b62-70c1-9558-6b387e93ed5c` has the same policy. Host runtime request records were checked directly, rather than relying on the reviewer's report.

After the child completed with no pending runs, the host still held zero runtime approval requests for it. The independent review approved both skill changes with no findings. It also identified the disposable checkout's existing shipping-discount defect and weak test oracle through local probes. Those fixture defects are outside the permission fix. Hash comparisons confirmed that the scoped skills, validation scripts, and fixture source files were unchanged by the reviewer; the fixture only gained six Python cache files. It made no external writes.

## Evidence and limits

- `observed`: the original launch overrode the parent's permissions and produced 32 command approval requests. Durable T3 launch, request, and native session records establish this.
- `observed`: the corrected launch inherited the current parent's effective permissions, read files, and ran validation with zero approval requests. The child's durable activity, native session, and host runtime request records establish this.
- `tested`: the three repository checks and the disposable checkout's four tests passed. The reviewer retained command output and exit codes in local scratch logs; those disposable files were removed after verification.
- `inspected`: the new rule preserves explicit permission limits. The negative routing case `reviewer-explicit-permission-limits` was added but was not executed against an approval-required parent.

This was explicit skill invocation and a real T3 delegated launch, not automatic host routing. The current parent deliberately selected `inherit`; autonomous selection by a fresh parent and repeated before/after effectiveness are unassessed. Source preservation was checked by file hashes and diffs. Runtime access was broad, so the assignment's source/external-write exclusions were followed by conduct, not enforced by a separate tool allowlist. No T3 application code or existing thread permissions were changed.
