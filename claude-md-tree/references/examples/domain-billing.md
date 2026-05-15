# Example: src/billing/CLAUDE.md (domain packet)

Worked example for a money/billing folder. Demonstrates a complete context packet with anti-scope, mental model, invariants with reasons, and verification.

```markdown
# Billing Context

## What this folder owns
Subscription state, invoices, Stripe webhook handling, trial logic, and
entitlement updates. **Does not own:** payment-form UI (lives in
`apps/web/app/(billing)/`), or the public `/billing` API routes
(those are thin wrappers in `apps/api/routes/billing/`).

## Mental model
Stripe is **not** the source of truth for app access. The local
`subscriptions` table is. Webhooks update local state; the app reads
entitlements from our database. This means:
- Webhook delivery delay never gates user access (we have a row).
- Stripe outages don't block reads.
- We can audit every state change locally.

The `entitlements` table is derived from `subscriptions` + `addons`. It
is read on every request, so we cache it per-session in Redis with a
30-second TTL.

## Important invariants
- Webhook handlers must be idempotent. Why: Stripe retries on any
  non-2xx and on network failures; non-idempotent handlers double-credit
  accounts. Use `idempotency_key` from the event header.
- Never grant entitlements from an unverified webhook. Why: signature
  verification is the only guard against forged grants. Reject before
  any DB write.
- Subscription changes are auditable. Why: legal + finance require a
  full state-change log per workspace. Always write to `subscription_events`
  before the `subscriptions` update.
- Do not delete billing records. Mark `status = 'inactive'` or
  `superseded_by = <new_id>`.

## Common change patterns
- New subscription state usually requires:
  - migration in `packages/db/migrations/`
  - webhook handler in `src/billing/webhooks/`
  - entitlement calculation in `src/billing/entitlements.ts`
  - tests for upgrade, downgrade, cancel, renewal in `src/billing/__tests__/`
- New plan tier:
  - `plans` config (this folder) + Stripe Price ID env var
  - pricing-page copy in `content/pricing.md` (separate PR is fine)

## Verification
- `pnpm test billing` — unit tests for handlers, entitlements, idempotency
- `pnpm test:fixtures billing` — replays recorded webhook events
- For schema changes: `pnpm db:migrate` on a fresh local DB before opening the PR

## Related context
- `docs/billing.md` — domain overview
- `docs/adr/004-subscription-model.md` — why local-state-of-truth
- `docs/adr/011-idempotent-webhooks.md` — idempotency key strategy
- Stripe events reference: https://stripe.com/docs/api/events/types
```

Notes:

- **Anti-scope is explicit.** "Does not own" prevents Claude from spreading billing logic into the wrong files.
- **The mental model is non-obvious.** "Stripe is not the source of truth" is exactly the kind of framing a senior engineer would say aloud before letting someone touch this folder.
- **Invariants have *why*.** Without the why, Claude will sometimes find a "clever" shortcut. With the why, it knows what's actually at stake.
- **Change patterns name files.** "Updating the schema" is vague; naming `src/billing/webhooks/` and `src/billing/entitlements.ts` is actionable.
- **Verification is the minimal command set, not the global one.** `pnpm test billing` is faster than `pnpm test`.
- **Long history goes to ADRs**, not inline.
- **77 lines.** Comfortably under the 100-line guidance.
