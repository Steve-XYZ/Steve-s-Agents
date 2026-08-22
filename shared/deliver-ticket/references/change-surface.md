# Change-surface Enumeration

Read this when the affected surface is unfamiliar or the change is material.
It is a search recipe, not a review checklist. Every step answers "what already
exists around this?" and nothing here decides whether something is a problem.
That belongs to [engineering-judgment](../../engineering-judgment/SKILL.md).

Work from the concrete things the change touches: a symbol, a setting key, a
table or column, a message or event, an endpoint, a template identifier. For
each one, search rather than recall.

## Readers and writers

Search the identifier across the whole repository, not the project you are
editing. Record every read and every write with `file:line`. A setting with one
writer and four readers behaves differently from one with four writers.

Include indirect access: dependency injection, reflection, generated clients,
string-keyed lookups, and anything that reaches the value through a wrapper.
Grep the literal key as well as the symbol, because configuration and messages
are usually reached by name.

## Callers and sibling paths

For a changed function or endpoint, list its callers. Then look for the paths
that solve the same problem elsewhere: a second entry point, a guest or
anonymous variant, an admin path, a bulk or import route, a retry or backfill
job. A sibling that was written by copying the original will not appear in a
caller graph, so search by behavior and by name, not only by reference.

Note which siblings the ticket intends to change and which it does not. That
distinction is what makes an incomplete change visible later.

## Persistence and migrations

Record the schema objects involved, the migrations that create or alter them,
and whether existing rows are affected. For a change with a backfill, state the
population it covers and the population it leaves alone. For a default value,
state whether it applies to existing rows, new rows, or both.

## Configuration layers and overrides

List every layer that can supply the value, in resolution order, with paths:
committed defaults, per-environment files, compose or deployment manifests,
environment variables, secret stores, and any per-tenant layer. An override in
one environment is the usual reason a change works locally and not elsewhere.

## Deployment scopes and tenants

Name the scopes the change reaches: environments, regions, brands, tenants. If
a value is shared across tenants, say so explicitly, and say whether the ticket
intends the same value everywhere.

## Asynchronous consumers and external contracts

List queue or event consumers, scheduled jobs, webhooks, and outbound
integrations that read anything the change touches, including external template
or campaign identifiers. Record the contract as it exists today: shape,
required fields, and who else produces or consumes it.

## Reachable failure paths

List the durable and external side effects in execution order, and note where
execution can stop between them. Include the fallback or legacy path that is
still live, if one exists; a superseded path that was never removed behaves as
a second writer.

## Output shape

Group by the thing that changed, and cite locations:

```
Changed: PaymentRetryWindow

Readers:
- PaymentRetryService.Schedule:41
- PaymentRetryService.Recover:113

Config layers:
- Api/appsettings.json:36
- Api/appsettings.Development.json:16
- deploy/compose.tenant.yml:46

Deployment scopes:
- three tenants share this value

External consumers:
- PaymentFailedConsumer
- BillingEmailService -> provider template RETRY_NOTICE
```

Stop when the categories that apply are enumerated. Do not add a category with
no members, and do not annotate entries with opinions.
