# Example: packages/db/CLAUDE.md (data-layer packet)

Worked example for a folder owning the database schema + migrations. The high-leverage zone: schema bugs are the most expensive bugs.

```markdown
# Database Layer Context

## What this folder owns
Drizzle schema definitions, migrations, and the typed query helpers other
packages import. **Does not own:** repository functions or domain logic;
those live next to their feature (e.g. `src/billing/queries.ts`).

## Mental model
The schema is **append-only** in production. Migrations are immutable once
shipped. Rollbacks are forward migrations, not reverse — we never run
`down`. A column is dropped via a follow-up migration after all readers
are off it.

`packages/db/schema/` is the single source of truth for shape. Drizzle
generates types from it; the API and the worker both import those types
directly. Hand-writing types that shadow schema entities is a bug.

## Important invariants
- One migration = one logical change. Why: makes review and bisection
  tractable.
- Never edit a shipped migration. Why: production already applied it;
  editing creates schema drift between environments.
- Every migration must be runnable on an empty DB AND on the current
  prod schema. Why: CI runs the empty path; production runs the prod
  path. We test both.
- Foreign-key cascades are explicit. Why: silent cascades have deleted
  customer data before. Use `onDelete: 'restrict'` or `'set null'`
  explicitly.
- No raw SQL in feature code. Why: it bypasses type generation and
  search/refactor breaks. If a query needs raw SQL, add a typed helper
  here.

## Common change patterns
- Adding a column:
  1. Edit the schema in `packages/db/schema/<table>.ts`.
  2. `pnpm db:gen --name add-<column>` to generate migration.
  3. Review the generated SQL — Drizzle sometimes picks unsafe defaults
     for NOT NULL on populated tables.
  4. `pnpm db:migrate` locally; check the migration applies cleanly.
- Renaming a column: do not. Add the new column, backfill, drop the
  old in a follow-up migration after all readers ship.

## Verification
- `pnpm db:migrate --dry-run` — print SQL without applying
- `pnpm db:migrate` — apply on local DB
- `pnpm test db` — type and helper tests
- For destructive migrations: bring up a prod-shaped DB via
  `pnpm db:restore-snapshot` and apply.

## Related context
- `docs/adr/002-append-only-migrations.md`
- `docs/runbooks/migration-rollback.md`
- `.claude/rules/migrations.md` — path-scoped enforcement
```

Notes on this example:

- **The append-only philosophy is the central mental model.** Claude defaults to "edit and re-run" patterns from other ecosystems; saying this out loud here prevents disasters.
- **Invariants are *all* high-stakes**, each with a clear "why."
- **"Adding a column" is concrete enough to follow.** Renaming explicitly forbidden — the right play is in two migrations, not a rename.
- **Verification scales by risk:** dry-run, local apply, then the prod-snapshot path for destructive changes.
- **Cross-references** to ADRs, runbooks, and the corresponding path-scoped rule.
