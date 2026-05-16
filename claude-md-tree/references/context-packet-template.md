# Context Packet Template

Use this for any nested `CLAUDE.md` inside a subfolder. Keep the whole file **under 100 lines**. If it's growing past that, move long explanations into `docs/` and link them under "Related context."

## The template

```markdown
# <Folder> Context

## What this folder owns
<One short paragraph naming what lives here and what does NOT live here.
Bound the scope explicitly — "this folder owns X. Y lives in <other-folder>.">

## Mental model
<2–6 sentences. The non-obvious framing a senior engineer would give before
letting someone touch the code. Source of truth, layering, what depends on what,
what's a leaky abstraction. Skip the obvious.>

## Important invariants
- <Invariant 1>. Why: <reason if not obvious>.
- <Invariant 2>. Why: <…>.
- <Invariant 3>. Why: <…>.

## Common change patterns
- Adding <thing> usually requires:
  - <step / file / test>
  - <step / file / test>
- Changing <thing> often breaks <thing else>; check <…> first.

## Verification
- `<command 1>` — <what it covers>
- `<command 2>` — <what it covers>

## Related context
- <../parent/CLAUDE.md> — parent context
- `docs/<domain>.md` — long background
- `docs/adr/<NNN>-<title>.md` — relevant ADR
- External spec / dashboard / runbook URLs
```

## Section guidance

### "What this folder owns"

State scope and **anti-scope**. Anti-scope is what's worth half a sentence: "Webhook handlers live here; the HTTP server is in `apps/api`." Without anti-scope, Claude will guess and pull responsibility into the wrong folder over time.

### "Mental model"

This is the highest-value section. The test: would a senior engineer say this out loud during onboarding? If yes, write it. If it's just "this folder has billing code," skip the section.

Good mental-model lines look like:

- "The payment provider is **not** the source of truth for app access. The local subscription row is. Webhooks update it; the app reads from our DB."
- "Migrations are append-only. Once a migration ships, it is never edited; it is superseded by a follow-up migration."
- "Charts here receive already-filtered data from page-level containers. They do not fetch."

### "Important invariants"

Each line: one invariant, one short "why." The why prevents Claude from breaking the invariant when a tempting shortcut presents itself.

Bad:
```
- Webhook handlers must be idempotent.
```

Good:
```
- Webhook handlers must be idempotent. Why: providers retry on any non-2xx and on network failures; non-idempotent handlers double-credit accounts.
```

### "Common change patterns"

Explain the *shape* of common changes — which files move together. This is where you save Claude from making half-changes that pass tests but break in production.

### "Verification"

The smallest relevant test commands. Not the full test suite — the subset that exercises this folder. If verification requires fixtures or test data, name them.

### "Related context"

Outbound links. Use relative paths for in-repo files; full URLs for external dashboards. ADRs are especially valuable — they explain *why* a non-obvious design exists.

## Use canonical vocabulary

When writing the packet, **use the terms defined in the project's `GLOSSARY.md`** — not synonyms. If the glossary says `Product`, do not write "wallpaper" or "decoration" in the mental model section. Rejected synonyms from the glossary should never appear in a CLAUDE.md.

If a term you need is missing from the glossary, that is a glossary update — pause and route to the `ubiquitous-language` skill before completing the packet. Inventing a new word in a CLAUDE.md is the most common way vocabulary drift starts.

## Things to leave out

- Anything Claude can infer by reading the code (file names, exports, type signatures).
- Restating parent CLAUDE.md content.
- Build/test commands that are global — those live in root CLAUDE.md.
- Personal preferences — those go in `CLAUDE.local.md` or user-level config.
- Long historical explanations — link to `docs/` instead.
- Multi-step procedures — those are skills.

## Size discipline

| Lines       | Verdict                                                   |
| ----------- | --------------------------------------------------------- |
| Under 30    | Excellent. Tight context packet.                          |
| 30–80       | Healthy.                                                  |
| 80–150      | Watch the budget — consider extracting to `docs/`.        |
| 150+        | Too large. Split or link out.                             |
| Under 5     | Probably should not exist — delete or fold into parent.   |
