# Drive the app

Use this when a claim needs `observed` evidence and the project has no working recipe. The result is a repeatable way for any agent to start the project, drive the changed behavior the way its user does, and keep proof.

## Discover from the repository

Answer these from code, documentation, and configuration. Ask the user only for what the repository cannot show, such as where test credentials live or which shared environment is safe to touch.

- **Surface.** What the user or consuming system touches: a web UI, an API, a CLI, a worker or scheduled job, a library, a report or export. Pick the one the claim is about.
- **Launch.** The project's own dev command from scripts, a Makefile, compose files, launch settings, or the README. Note ports, environment variables, configuration files, seed data, migrations, and authentication.
- **Ready.** One read-only check that the instance is the one this run started and is current: the process is up, the port belongs to it, the build or commit matches, a health endpoint answers, migrations are applied.
- **Drive.** Existing harnesses first: end-to-end specs, HTTP request files, test hosts, the CLI itself. Otherwise plain HTTP for a service, browser automation for a UI, a direct trigger for a job.
- **Observe.** The response body, the rendered state, stdout, stderr and exit code, stored rows read back with a read-only query, emitted messages, and logs correlated by request id.
- **Isolate.** This run's own ports, database or schema, data directory, and test identities. If two instances cannot coexist, do not drive one this run did not start.

## Drive and capture

- Exercise the user's path, not internal setters or test-only endpoints.
- Capture the action and the state it produced. After a mutation, read the stored value back through a second path.
- Wait for a specific state rather than a fixed sleep. Never repeat a state-changing action to make a check pass.
- Confirm what a dry-run or sandbox mode skips by observing files, network calls, or refs, not by trusting its name.
- Keep evidence outside the worktree in a named location. Cleanup never deletes it.

## Clean up

Stop what this run started by its process or container id, never by process name. Remove scratch data. Leave the user's running stack alone.

## Record the recipe

When any of the above had to be discovered, record what worked so the next agent starts at Drive:

- **Where.** A `## Verify` section in the agent instructions file closest to the surface (`AGENTS.md` or `CLAUDE.md`), or the file that section points to.
- **Tracked files.** Update an untracked or local instructions file directly. For a tracked one, put the proposed section in the report unless the user asked for it in this change.
- **What.** The exact launch command, the readiness check, the isolation settings, the evidence location, the gotchas you hit, the test identities and where their credentials live (never the values), and one line per feature you drove: how a user reaches it, the command, and the result that proves it.

When a recorded recipe fails, fix the recipe if the project legitimately changed and report a regression if the project broke. Never edit a recipe to match broken behavior.
