---
name: abstracted-project-spec
description: Extract an implementation-free product specification from an existing codebase — what a user can do and what it does for them, with every framework, file, schema, and past coding decision stripped out. Use when the user says "spec this project", "abstract spec", "what does this project actually do", "spec I could rebuild from", "/abstracted-project-spec", or wants a product brief derived from code rather than from docs. NOT for architecture docs, API reference, or codebase maps — those keep the implementation (use code-map / code-audit).
---

# Abstracted Project Spec

## Overview

Read a project, throw away how it was built, and write down only what it does for whoever uses it. The output must be reimplementable in any stack by someone who never sees this code.

## The one rule

**Every line of the spec survives a rewrite of the entire codebase.** If a sentence would become false after swapping the framework, database, file layout, or language, it is implementation and does not belong.

Test each line: *would this still be true if the project were rebuilt from scratch in a different stack?* No → cut or re-state it as a user outcome.

## Include / exclude

| Include | Exclude |
|---|---|
| What a user can do, in their words | Function, file, class, module names |
| What they get back / what changes for them | Frameworks, libraries, languages, package names |
| Rules the user can feel (limits, validation, defaults) | Schemas, tables, endpoints, config keys |
| Who can do what (roles, permissions) | Directory layout, build steps, deploy targets |
| What the system remembers about them | Design patterns, refactors, "we chose X because Y" |
| Outside services the user notices (login with X, pays via Y) | Internal service boundaries the user never sees |
| Qualities the user experiences (works offline, instant, private) | Performance numbers tied to current implementation |

Borderline: a constraint counts as user-facing only if the user could discover it without reading code. "Uploads cap at 50 MB" — in. "Uses S3 multipart above 5 MB" — out.

## Process

1. **Find the surfaces.** Locate every way a human enters the system: screens/routes, CLI commands, API consumers, scheduled jobs the user sees results of, config the user edits.
2. **Delegate the reading.** Send subagents per surface (UI, CLI, API, background/data) with the brief: *report user-visible capabilities only — what a user triggers, what happens for them, what rules bind it. Do not report file names, function names, or libraries.* Conclusions come back, not code.
3. **Also read what users were told.** README, help text, error messages, onboarding copy, marketing pages. Intent lives there.
4. **Draft to the template below.**
5. **Scrub.** Grep the draft for stack leakage before delivering — see Scrub pass.
6. **Flag the gaps.** Anything found in code whose *purpose* was not inferable goes under Unresolved, phrased as a question. Never invent a rationale.

Skip subagents only for a project under ~20 source files; read it directly then.

## Template

```markdown
# <Product> — Specification

## What it is
One paragraph. What it is for, for whom. No stack.

## Who uses it
Each user type, one line: who they are and what they come to do.
Note when there is only one type.

## What a user can do
One bullet per distinct user action — the list is meant to be long and complete.
Group under goal headings only to keep it navigable; never merge two actions into
one bullet to shorten it.

### <Goal, e.g. "Track spending">
- **<Action, verb-first>** — <what the user does> → <what they get>. <rules: limits,
  required inputs, defaults>. <Only for: role, if restricted.>

Split anything with an "and" in it: "Edit and delete a note" is two bullets.
Variants that differ in outcome or permission are separate bullets too.

## What the system remembers
What persists about a user or their work, in plain terms, and how long.

## What it connects to
Outside services the user is aware of, and what each is for from the user's side.

## Rules that always hold
Invariants a user can rely on regardless of path taken.

## Qualities
Only ones a user would notice: offline, real-time, private, multi-device, accessible.

## Not in scope
Things a reader would reasonably assume are here and are not.

## Unresolved
Open questions for the owner, each a real question with the observation that raised it.
```

Drop any section that is genuinely empty. Do not pad.

## Scrub pass

Before writing the file, scan the draft for:

- Proper nouns of tools — React, Postgres, Redis, Docker, Stripe SDK, FastAPI. Keep only user-visible services ("sign in with Google" stays; "uses NextAuth" goes).
- `.py` `.ts` `.json` `/src/` `/api/` — any path or extension.
- camelCase or snake_case identifiers.
- "the handler", "the endpoint", "the component", "the model", "the service".
- Sentences a user could not verify from using the product.

Each hit: re-state as user outcome, or delete.

## Rewrites

| Found in code | Spec line |
|---|---|
| `POST /api/v2/invoices` with `retry_count=3` | Sending an invoice; keeps trying briefly if delivery fails. |
| Redis-cached session, 30-day TTL | Stays signed in for 30 days without re-entering a password. |
| `if user.plan != "pro": raise` | Exporting is available on the paid plan only. |
| A `LegacyImporter` class handling two formats | Imports data from the older format as well as the current one. |
| Cron job pruning rows older than 90 days | History is kept for 90 days, then removed. |

## Output

Write to the session scratchpad directory named in the system prompt, as
`<project-name>-SPEC.md`. Never write into the project itself unless the user asks —
this is a derived artefact, not project documentation. No scratchpad in the system
prompt → `/tmp/<project-name>-SPEC.md`.

Then send the file with SendUserFile and report inline: absolute path, action count,
and the Unresolved questions (those need an answer, not a file).
