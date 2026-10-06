# Ticket scope and related work

A ticket's named repositories, surfaces, and blast radius are leads, like its suggested cause. Authors miss a repository, underestimate who reads a changed fact, or file related work as separate tickets that never mention each other. Establish scope from evidence before choosing the first slice.

Use this when the work runs from a multi-repository workspace, names several tickets, or changes a fact that another repository, process, or customer line reads. When the contract map and a search show no reader outside the owning repository, record `scope: single repository; no outside reader`. With several tickets in scope, still find related work and plan the set's shared facts below. With one ticket, return to delivery.

## Read every ticket in scope

Read each ticket's description, comments, attachments, and linked tickets. Quote its scope words exactly: the repositories, products, and surfaces it names, and phrases such as "all draws" or "consistently across". The ticket's stated outcome stays authoritative. Its list of places to change does not.

## Map each changed fact across repositories

Name the facts the outcome changes, such as a display label, a date boundary, an eligibility predicate, a payload field, or a setting. For each fact:

1. Find its owner and every writer, reader, and display surface in every repository of the workspace. Start from the workspace contract map, then search by symbol, field, setting, and visible text. Follow it through events, HTTP clients, sync jobs, caches, exports, and frontends.
2. When two repositories compute the same fact independently, record both locations and whether they currently agree. Silent divergence between copies is a defect the set must not widen.
3. Note the customer line each repository's change targets and whether another line carries its own version of the code.

Compare the evidence with the ticket and record three lists: surfaces the ticket names and the evidence confirms, surfaces the evidence adds, and named surfaces the evidence excludes. A search that found nothing counts as evidence only with its query and scope.

## Find related work

Look for other work on the same facts before editing:

- **Tickets.** With a tracker tool, search open and in-progress tickets in the same team, project, and cycle for the fact names, surfaces, and visible text. Read the matches. Without one, state that ticket relatedness is unassessed and ask for the list when the set is large or touches a shared fact.
- **In-flight code.** Run this guidance repository's `scripts/related-work.py` from the workspace or set folder with the changed paths or symbols, such as `python3 /path/to/Steve-s-Agents/scripts/related-work.py --base <line> --path '*Formatter*' --grep '<symbol>'`. It lists unmerged local and origin branches, uncommitted changes in other worktrees, and recent commits on the line that touch them. It cannot see work that exists only in a ticket, and a squash-merged branch looks unmerged until it is deleted. Another thread editing the same file is related work even when its ticket looks unrelated.
- **Recent merges.** Treat recent commits on the line that touch the same fact as the current shape to build on, not to redo.

Classify each related item as independent, sharing a fact, or conflicting. Shared facts need one shape and an order. Conflicting requirements need the user.

## Decide scope

- An added surface that the stated outcome cannot be met without is in scope. Record why and continue.
- An added surface that would merely benefit, or that changes another customer line, is out of scope until the user decides. Report it with its evidence.
- A named surface the evidence excludes stays in the report with the evidence that excluded it.
- A conflict between tickets, or a fix the outcome requires in a repository the user has not authorized, needs the user's decision before that slice.

## Plan a set

When several tickets share a fact, land the fact's shape once, in the repository that owns it, before the tickets that consume it. Keep one implementer per repository across tickets that share a fact, never one per ticket. When the set qualifies, `orchestrate` assigns one worker per repository after the shared cases are written. Run tickets in parallel only when they share no fact and no file. When the same rule must live in two repositories, make both implementations pass the same cases. Do not copy one and adapt it silently.

Keep the set note at the workspace root, or the set folder root when one exists, outside every repository. Report its path. It holds:

- ticket by repository by surface, with the ticket's scope words beside the evidence;
- each shared fact with its owner and every copy;
- per repository: the line, checkout path, branch, and latest commit, plus deploy order and companion PRs;
- related tickets and branches with their classification;
- the order of slices, validation run per repository, and the decisions still open.

## Before publishing

Check the integrated change against the note. Every repository and surface in scope has a change or a recorded reason. Every copy of a shared fact gives the same result for the same cases. Every companion PR links the others and states its deploy order.
