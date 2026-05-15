# Example: Root CLAUDE.md (web/SaaS monorepo)

Worked example. Adapt the headings and content; keep the structure. Under 200 lines.

```markdown
# Project Context

## What this project is
Acme is a B2B SaaS for [thing]. This repo contains the web app, public API,
shared UI package, and background workers.

## Stack
- Runtime: Node 22, pnpm 9, TypeScript 5.6
- Frontend: Next.js 15 (App Router), Tailwind, shadcn/ui
- Backend: Fastify, Drizzle, Postgres 16, Redis
- Tests: Vitest (unit), Playwright (e2e)
- Infra: AWS (ECS + RDS), Terraform

## Architecture map
- `apps/web/` — Next.js frontend.
- `apps/api/` — Fastify API server.
- `apps/worker/` — Background jobs (BullMQ).
- `packages/ui/` — Shared design system. Used by `apps/web` only.
- `packages/db/` — Drizzle schema + migrations. Source of truth for DB shape.
- `src/billing/` — Subscription, invoicing, Stripe webhooks, entitlements.
- `src/auth/` — Session, tokens, RBAC.
- `docs/` — ADRs, runbooks, domain docs.

## Context boundaries
Before editing a specialized area, read the nearest CLAUDE.md in that subtree:
- `packages/db/CLAUDE.md` — schema and migration discipline
- `src/billing/CLAUDE.md` — money, webhooks, entitlements
- `src/auth/CLAUDE.md` — sessions, tokens, RBAC
- `apps/api/CLAUDE.md` — API contract and error format
- `packages/ui/CLAUDE.md` — design system

Path-scoped rules in `.claude/rules/` also apply when matching files are read:
- `testing.md` — test conventions
- `api-contracts.md` — endpoint shape and versioning
- `accessibility.md` — a11y for any UI under `apps/web` and `packages/ui`
- `generated-files.md` — what is generated and must not be hand-edited

## Global invariants
- Migrations are append-only. Never edit a shipped migration; supersede with a new one.
- Public API responses are versioned. Do not change a v1 response shape; add v2.
- Secrets live in `.env.local` (gitignored) and AWS Secrets Manager. Never commit them.
- Never push to `main` directly. PRs only, with the lint + test workflow green.

## Commands
- Install: `pnpm install`
- Dev: `pnpm dev` (runs web, api, worker in parallel)
- Build: `pnpm build`
- Test: `pnpm test` (Vitest), `pnpm e2e` (Playwright)
- Lint: `pnpm lint`
- Format: `pnpm format`
- Typecheck: `pnpm typecheck`
- DB migrate (dev): `pnpm db:migrate`
- DB new migration: `pnpm db:gen --name <slug>`

## When unsure
- Pricing/billing change → read `src/billing/CLAUDE.md`.
- Adding an API endpoint → read `apps/api/CLAUDE.md` and the `api-contracts` rule.
- Schema change → read `packages/db/CLAUDE.md` and the `migrations` rule.

## See also
- `docs/architecture.md` — system diagram
- `docs/adr/` — design decisions
- `docs/runbooks/` — on-call procedures
```

Notes on this example:

- **It's a map.** Every section either orients (project, stack, architecture) or points to a specific deeper file.
- **Commands are concrete.** Not "run the tests" — `pnpm test` and `pnpm e2e`.
- **Global invariants are actually global.** Migrations being append-only is a no-exceptions rule; specifying that here means it survives compaction.
- **No domain detail.** No specifics about Stripe vs Adyen, no DB column names, no a11y rules — all of those live in their proper homes.
- **Under 100 lines.** Plenty of headroom under the 200-line guidance.
