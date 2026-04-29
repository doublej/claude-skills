# Enable Banking API endpoints

Base: `https://api.enablebanking.com`. Auth: `Authorization: Bearer <RS256-JWT>` on every request.

## Misc

### `GET /application`
Returns app metadata: `name`, `kid`, `redirect_urls`, `active`, `paying_user`, etc. Use to read configured `redirect_urls` for the auth body.

### `GET /aspsps`
Returns `{"aspsps": [{name, country, logo, psu_types, auth_methods, payment_products, ...}]}`. Filter by `country` first, then `name`. Names are case-sensitive (e.g. `ABN_AMRO`, not `ABN AMRO`).

## User sessions

### `POST /auth`
Start authorization. Body:
```json
{
  "access": {
    "valid_until": "2026-05-09T12:00:00+00:00",
    "balances": true,        // optional, default true
    "transactions": true,    // optional, default true
    "accounts": [{"iban": "..."}]  // optional, restrict to specific accounts
  },
  "aspsp": {"name": "ING", "country": "NL"},
  "state": "<your-uuid>",
  "redirect_url": "https://yourapp.tld/cb",
  "psu_type": "personal",    // or "business"
  "psu_id": "...",           // some ASPSPs require (e.g. login, BIC)
  "auth_method": "redirect"  // optional, defaults per ASPSP
}
```
Returns `{"url": "...", "authorization_id": "..."}`. Send PSU to `url`.

### `POST /sessions`
Exchange callback code for session. Body: `{"code": "..."}`. Returns:
```json
{"session_id": "...", "accounts": [{"uid", "iban", "name", "currency", "product", ...}],
 "access": {...}, "aspsp": {...}, "psu_type": "personal", "created": "..."}
```

### `GET /sessions/{session_id}`
Re-fetch session metadata + accounts. Use to recover after restart if you stored `session_id`.

### `DELETE /sessions/{session_id}`
Revoke. Idempotent.

## Account data (uses account `uid` from session)

### `GET /accounts/{uid}/details`
Full account info: holder name, IBAN, BBAN, BIC, currency, product, type (`CACC`, `CARD`, `LOAN`, `SVGS`).

### `GET /accounts/{uid}/balances`
```json
{"balances": [
  {"balance_type": "CLAV", "balance_amount": {"amount": "123.45", "currency": "EUR"},
   "reference_date": "2026-04-29", "credit_limit_included": false}
]}
```

Balance types:
- `CLAV` closing available (spendable now)
- `CLBD` closing booked (settled)
- `ITAV` interim available
- `ITBD` interim booked
- `OPBD` opening booked
- `XPCD` expected
- `OTHR` other

### `GET /accounts/{uid}/transactions`
Query params:
- `date_from` (required-ish, defaults to 90d ago) — `YYYY-MM-DD`
- `date_to` — `YYYY-MM-DD`
- `transaction_status` — `BOOK` (booked) | `PDNG` (pending) | `INFO`
- `strategy` — `default` | `longest` (some ASPSPs)
- `continuation_key` — pagination cursor

Response:
```json
{"transactions": [
  {"entry_reference": "...", "transaction_amount": {"amount": "-12.34", "currency": "EUR"},
   "creditor": {"name": "..."}, "debtor": {...},
   "creditor_account": {"iban": "..."}, "debtor_account": {...},
   "transaction_date": "2026-04-28", "value_date": "2026-04-28", "booking_date": "2026-04-28",
   "remittance_information": ["..."], "merchant_category_code": "5812",
   "transaction_id": "...", "status": "BOOK", "bank_transaction_code": "..."}
],
"continuation_key": "..."}
```

Loop until `continuation_key` absent.

### `GET /accounts/{uid}/transactions/{transaction_id}`
Single transaction details. Not all ASPSPs support.

### `GET /accounts/{uid}/standing-orders`
Recurring instructions (where supported).

## Payments (PIS, licensed PISPs only)

### `POST /payments`
Body shape depends on `payment_type`. Minimal SEPA:
```json
{
  "access": {"valid_until": "2026-04-30T12:00:00+00:00"},
  "aspsp": {"name": "ING", "country": "NL"},
  "state": "<uuid>",
  "redirect_url": "...",
  "psu_type": "personal",
  "payment_request": {
    "payment_type": "SEPA",
    "credit_transfer_transaction": [{
      "instructed_amount": {"amount": "10.00", "currency": "EUR"},
      "creditor_account": {"iban": "NL00BANK0123456789"},
      "creditor": {"name": "Acme BV"},
      "remittance_information": ["Invoice 123"],
      "end_to_end_identifier": "E2E-123"
    }],
    "debtor_account": {"iban": "NL00YOUR0000000000"}
  }
}
```
Returns auth `url` + `payment_id`. PSU authorizes at bank, redirected back with `code`. Confirm via `POST /payments/confirm` with the `code`.

### `GET /payments/{payment_id}`
Status: `RCVD` received, `PDNG` pending, `ACTC` accepted technical, `ACSC` accepted settlement complete, `ACCC` accepted credit complete, `RJCT` rejected, `CANC` cancelled.

### `DELETE /payments/{payment_id}`
Cancel (where ASPSP supports).

## Webhooks

Configure callback URL in Control Panel. Events: `session.created`, `session.deleted`, `payment.status.changed`. Verify HMAC signature header.

## Rate limits

Not publicly documented. Backoff on 429. Cache JWT for full TTL (3600s typical). Avoid re-fetching `/aspsps` per request — cache 24h.
