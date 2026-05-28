# CLAUDE.md Anti-patterns

The failure modes that show up over and over in real codebases. Audit existing CLAUDE.md files against this list.

These are **content/placement** failures (wrong knowledge in the wrong file). For **formatting/shape**
failures (noisy tables, over-nested tags, dense blobs, emphasis overload, fake config, fragmented
sections), see `../../claude-md-optimizer/references/formatting-examples.md`.

## 1. The sprinkle

Adding a `CLAUDE.md` to every folder "just in case." Result: most files are 3 lines saying "follow existing patterns," they consume nothing useful, and the genuinely valuable packets get lost in the noise.

Fix: keep CLAUDE.md only where two-or-more of the high-value criteria apply (see SKILL.md Pass 1). When in doubt, leave it out — you can always add one.

## 2. The commandment file

```md
# CLAUDE.md
- Always use TypeScript
- Never use `any`
- Always run tests
- Never push to main
- Always write JSDoc
```

This is the weakest form. No mental model, no scope, no reasons. Claude has nothing to reason about when an edge case shows up. Worse, half of these rules are either obvious or wrong in specific cases.

Fix: write a context packet (see `context-packet-template.md`). Rules are one short section of a context packet, not the whole thing.

## 3. The duplicated rule

The same rule appears in `src/api/CLAUDE.md`, `src/api/v1/CLAUDE.md`, `src/api/v2/CLAUDE.md`, and `apps/api-tests/CLAUDE.md`. When the rule needs to change, it changes in 0–3 of those places.

Fix: lift into `.claude/rules/api-contracts.md` with `paths: ["src/api/**", "apps/api-tests/**"]`. One source of truth, conditional load.

## 4. The ADR-inside-CLAUDE.md

900 lines of historical context about why the billing model is the way it is, inline in `src/billing/CLAUDE.md`. Loads in full when Claude reads any file in that folder. Burns ~3 KB of context per session for context Claude rarely needs.

Fix: move to `docs/adr/NNN-billing-model.md`. Link from the CLAUDE.md under "Related context." Most of the time Claude doesn't need the history; when it does, it can read the doc.

## 5. The procedure masquerading as a fact

```md
# src/billing/CLAUDE.md
To add a new subscription tier:
1. Update the schema in schema.prisma
2. Add a migration with `pnpm db:migrate add-tier-X`
3. Update the entitlement enum in src/entitlements.ts
4. Add a Stripe price ID in env config
5. Update the pricing-page tests
6. Update marketing copy in /content/pricing.md
```

This is a procedure. It belongs in `.claude/skills/add-subscription-tier/SKILL.md`. CLAUDE.md is for what's *true*, not how to *do* things.

## 6. The compaction trap

A critical invariant ("never grant entitlements from unverified webhooks") lives only in `src/billing/CLAUDE.md`. The user runs `/compact`. The conversation continues. Claude reads a file in `src/billing/` later — at which point the nested CLAUDE.md reloads. But if the next action is in a different folder that touches billing logic indirectly, the invariant is gone.

Fix: invariants that are critical *across the whole project* belong in root CLAUDE.md or in a no-`paths` rule. Folder-local invariants stay in the nested packet — that's fine, just know the trade-off.

## 7. The hand-edited generated note

`packages/types-generated/CLAUDE.md`:
```md
- Files here are generated. Do not edit by hand.
```

Useful, but easily ignored. Better: add a rule with the path scope, AND a hook that blocks edits to those files, AND a comment in the generated file header. Layered defenses for "Claude must not touch this."

## 8. The repeated parent

```md
# src/billing/webhooks/CLAUDE.md
- This is part of billing.
- See src/billing/CLAUDE.md for context.
```

Adds nothing. The parent CLAUDE.md loads when you read files here anyway (it loads when *any* file in `src/billing/` is read, including its children). If you have nothing new to say at the deeper level, don't add a file.

## 9. The everything-bagel root

Root CLAUDE.md hits 600 lines covering project, billing details, db schema, UI conventions, deployment guide, CI tips, coding style, and a brain dump of company culture. Adherence drops sharply.

Fix:
- Root stays at <200 lines: project map + global invariants + commands + links.
- Domain detail → nested CLAUDE.md.
- Coding style / a11y / testing → path-scoped rules.
- Deployment / CI / company culture → `docs/` linked from root.

## 10. The "follow existing patterns" entry

```md
- Follow existing patterns in this folder.
```

Claude already does this by default. It's not actionable. Either name the specific pattern with one concrete example, or delete the line.

## 11. The implicit assumption

```md
# src/billing/CLAUDE.md
- Always use the helper.
```

Which helper? Claude has to guess. Be specific:

```md
- For new webhook handlers, use `wrapWebhook()` from `src/billing/wrap.ts`. It handles signature verification, idempotency keys, and the audit log.
```

## 12. The personal note in a shared file

```md
# CLAUDE.md
- Use my sandbox URL: https://stripe-test-abc123.example.com
```

This is per-user state and shouldn't be in the project CLAUDE.md. Move to `CLAUDE.local.md` (gitignored) or auto memory.

## 13. The skill-listing CLAUDE.md

```md
# CLAUDE.md
This project uses these skills:
- add-component
- create-migration
- deploy-staging
```

Skills are listed automatically at session start (by description). Re-listing them in CLAUDE.md is duplication that goes stale.

## 14. The hooks-as-prose

```md
# CLAUDE.md
- Always run `pnpm format` after editing any file.
```

This is a hook. Configure it in `.claude/settings.json` and it runs whether Claude follows the instruction or not.

```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Edit|Write", "hooks": [{ "type": "command", "command": "pnpm format" }] }
    ]
  }
}
```

## 15. The audit-after-it-rots

Setting up CLAUDE.md once and never revisiting. Code moves, conventions change, half the files now contradict reality. Adherence drops because Claude is reading stale guidance.

Fix: schedule a quarterly audit. Run `/memory` in a real session, walk the files, delete or update anything that no longer matches the code. The `claudeMdExcludes` setting is your friend when other teams' files drift.

## 16. The vocabulary-less tree

A complete CLAUDE.md tree (root + nested packets + rules) with no `GLOSSARY.md` and no `<vocabulary>` block. Each packet uses subtly different words for the same concept — `User` here, `Customer` there, `Account` elsewhere. Agents mirror the drift back into code, commits, and PR titles. Within weeks the codebase has three nouns for the same thing.

Fix: add a `GLOSSARY.md` at root (or per bounded context for ecosystems) and a `<vocabulary>` block in root CLAUDE.md pointing to it. Delegate the curation to the `code-glossary` skill. Then audit existing packets — any rejected synonym appearing in a CLAUDE.md is a defect.

## 17. The competing-vocabulary tree

Multiple sub-projects in an ecosystem each define `Product` to mean different things, with no context map. Agent reading both gets contradictory signals — uses whichever it saw last.

Fix: either align on one shared `GLOSSARY.md` at ecosystem root, or accept per-context glossaries AND write a context-map at ecosystem root that names the translation ("In `wallgen`, `Product` = an unpublished render. In `shopify-template`, `Product` = a published SKU. The two are linked by `WallgenPublishedProductId`.").
