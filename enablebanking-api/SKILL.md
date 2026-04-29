---
name: enablebanking-api
description: Enable Banking (formerly Tilisy) PSD2 / Open Banking aggregation API for European bank accounts. Covers JWT RS256 auth, RSA key generation, ASPSP discovery, AIS session lifecycle (auth → callback → session_id → fetch), account balances, transaction pagination via continuation_key, and SEPA payment initiation. Triggers on "enable banking", "enablebanking", "tilisy", "PSD2 API", "open banking aggregation", "AISP integration", "fetch bank transactions Europe", or any work against api.enablebanking.com (NL banks ING/ABN/Rabobank, FI Nordea/OP, DE banks).
---

# Enable Banking API

PSD2 aggregation API: read European bank accounts, balances, transactions; initiate SEPA payments. One contract, all banks.

- **Base URL**: `https://api.enablebanking.com` (legacy: `api.tilisy.com`)
- **Auth**: JWT RS256, RSA keypair, app registered in Control Panel
- **Sandbox**: auto-active on signup. Production: contract + whitelist.
- **Official samples** (Python/JS/Go/C#/PHP/Ruby/Postman): https://github.com/enablebanking/enablebanking-api-samples
- **Reference docs**: https://enablebanking.com/docs/api/reference/

## Setup (one-time)

1. Generate RSA keypair:
   ```bash
   openssl genrsa -out enablebanking.key 2048
   openssl req -new -x509 -key enablebanking.key -out enablebanking.cert -days 730 -subj "/CN=enablebanking-app"
   ```
2. Sign up at https://enablebanking.com/, upload `enablebanking.cert` in Control Panel.
3. Save returned `application_id`. Store in `config.json`:
   ```json
   {"applicationId": "uuid-here", "keyPath": "enablebanking.key"}
   ```
4. Install deps:
   ```bash
   uv add pyjwt[crypto] requests cryptography
   ```

## JWT generation

RS256, max 24h validity, signed with RSA private key. See `scripts/jwt_token.py`.

```python
import jwt as pyjwt
from datetime import datetime

def make_jwt(app_id: str, key_path: str, ttl_seconds: int = 3600) -> str:
    iat = int(datetime.now().timestamp())
    return pyjwt.encode(
        {"iss": "enablebanking.com", "aud": "api.enablebanking.com",
         "iat": iat, "exp": iat + ttl_seconds},
        open(key_path, "rb").read(),
        algorithm="RS256",
        headers={"kid": app_id},
    )
```

Send as `Authorization: Bearer <jwt>` on every request. Cache for full TTL.

## Core flow (AIS — read accounts/transactions)

1. **List ASPSPs** — `GET /aspsps` → pick `name` + `country` (e.g. `ING`/`NL`, `ABN_AMRO`/`NL`, `Rabobank`/`NL`, `Nordea`/`FI`). Names case-sensitive.
2. **Start auth** — `POST /auth`:
   ```json
   {"access": {"valid_until": "2026-05-09T12:00:00+00:00"},
    "aspsp": {"name": "ING", "country": "NL"},
    "state": "<uuid4>",
    "redirect_url": "<one of app.redirect_urls>",
    "psu_type": "personal"}
   ```
   → `{"url": "..."}`. Send PSU there.
3. **PSU authenticates at bank**, redirected to `redirect_url?code=...&state=...`
4. **Exchange code** — `POST /sessions` with `{"code": "..."}` → `{"session_id", "accounts": [{"uid", "iban", ...}]}`
5. **Fetch data** using `account_uid`:
   - `GET /accounts/{uid}/details`
   - `GET /accounts/{uid}/balances`
   - `GET /accounts/{uid}/transactions?date_from=YYYY-MM-DD[&continuation_key=...]`
6. **Cleanup** — `DELETE /sessions/{session_id}`

Full runnable flow: `scripts/ais_flow.py`

## Transaction pagination

Loop until `continuation_key` absent:

```python
query = {"date_from": "2026-01-29"}
key = None
while True:
    if key: query["continuation_key"] = key
    r = requests.get(f"{API}/accounts/{uid}/transactions", params=query, headers=h).json()
    process(r["transactions"])
    key = r.get("continuation_key")
    if not key: break
```

`date_from` defaults ~90d back. Some ASPSPs cap history at 90d without re-consent.

## Balance types

Multiple per account, distinguish via `balance_type`:
- `CLAV` closing available — "spendable now" (most UX wants this)
- `CLBD` closing booked — settled
- `ITBD` interim booked
- `OPBD` opening booked
- `XPCD` expected
- `ITAV` interim available

## Payments (PIS) — licensed PISPs only

`POST /payments` with payment object. Body varies by `payment_type` (`SEPA`, `SEPA_INSTANT`, `BULK`). Track via `GET /payments/{id}`. Statuses: `RCVD` → `PDNG` → `ACSC`/`ACCC` (accepted) or `RJCT`. See `references/endpoints.md` for SEPA body shape.

Skip unless user has PISP license + production access.

## Errors

| Code | Cause | Fix |
|------|-------|-----|
| 401 | JWT expired/malformed/bad kid | Regenerate JWT, verify `kid` = app_id |
| 403 | App not authorized for ASPSP/country | Check Control Panel ASPSP enablement |
| 404 on `/sessions/{id}` | Session expired (consent valid_until passed) | Re-run auth flow |
| 422 | Bad body (missing redirect_url, unknown ASPSP) | `GET /aspsps` to confirm exact name/country |
| 429 | Rate limited | Backoff + cache JWT |

ASPSP quirks:
- **NL ING/ABN/Rabobank**: `psu_type` must match account holder type
- **DE banks**: many require `psu_id` in auth body
- **FI**: BBAN-only accounts; `iban` may be null, use `uid`
- **SCA re-auth**: every 90d (PSD2 RTS art.10a regulation, no workaround)

## Reference files

- `references/endpoints.md` — full endpoint shapes incl. payments
- `scripts/jwt_token.py` — standalone JWT minter
- `scripts/ais_flow.py` — end-to-end AIS demo

For non-Python: clone https://github.com/enablebanking/enablebanking-api-samples — same flow, same endpoints.
