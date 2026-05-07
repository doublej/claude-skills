# Lightroom Services REST API

Two endpoints with different concerns:

| Base | Purpose |
|---|---|
| `https://lr.adobe.io/v2/` | Catalog: assets, albums, account, metadata. Sync and CRUD. |
| `https://image.adobe.io/lrService/` | Async image-processing jobs: auto-tone, auto-straighten, apply preset. See `firefly-services.md`. |

Reference docs (Adobe-hosted): https://www.adobe.io/apis/creativecloud/lightroom/apidocs.html

## Auth setup (one-time)

1. **Create an Adobe Developer Console project**: https://developer.adobe.com/console/projects
2. **Add API → Adobe Services → Lightroom Services API** (also called "Lightroom Partner APIs"). Ask for `lr_partner_apis` scope.
3. **Add OAuth Web App** credential. Set redirect URI to `https://localhost:8443` for local dev.
4. **Download the `config.json`** — contains `client_id` (X-API-Key), `client_secret`, OAuth endpoints.

### Get a user token (OAuth Web flow)

Lightroom Services requires **per-user tokens** (not service tokens). User must consent in browser.

```
1. Build authorize URL:
   https://ims-na1.adobelogin.com/ims/authorize/v2
     ?client_id=<X-API-Key>
     &scope=openid,offline_access,lr_partner_apis
     &response_type=code
     &redirect_uri=https://localhost:8443

2. User opens, signs in, approves → browser redirects to localhost:8443?code=<auth_code>

3. Exchange code for tokens:
   POST https://ims-na1.adobelogin.com/ims/token/v3
     client_id=<X-API-Key>
     client_secret=<from config.json>
     grant_type=authorization_code
     code=<auth_code>

   Returns:
   { "access_token": "...", "refresh_token": "...", "expires_in": 86400 }
```

Helper: [`lou-k/adobe-io-auth`](https://github.com/lou-k/adobe-io-auth) automates the local-callback dance with a self-signed cert. Setup:
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
adobe-io-server -c config.json -s openid,offline_access,lr_partner_apis -p 8443 -o token.json
# Browser opens, user approves, token.json gets written.
```

### Refresh token

Tokens expire in 24h. Use the `refresh_token` (long-lived, until user revokes):
```
POST https://ims-na1.adobelogin.com/ims/token/v3
  client_id=<X-API-Key>
  client_secret=<...>
  grant_type=refresh_token
  refresh_token=<...>
```

## Request format

Every request:
```http
GET /v2/<path> HTTP/1.1
Host: lr.adobe.io
X-API-Key: <client_id>
Authorization: Bearer <user_access_token>
```

For POST/PUT with JSON body: `Content-Type: application/json`.

### Response prefix quirk

JSON responses are **prefixed with `while (1) {}`** to defeat JSON hijacking attacks. Strip before parsing:
```python
text = response.text.replace("while (1) {}", "")
data = json.loads(text)
```

This is non-negotiable — it appears on every JSON endpoint. Failing to strip causes parse errors with no useful message.

## Endpoint catalog

### Health + account
| Verb | Path | Returns |
|---|---|---|
| GET | `/health` | Service liveness |
| GET | `/account` | Authed user (id, email, plan info) |
| GET | `/catalog` | User's catalog metadata (one catalog per Adobe account) |

```python
GET /v2/catalog
→ { "id": "<32-hex>", "name": "Lightroom Library", ... }
```

### Assets

| Verb | Path | Purpose |
|---|---|---|
| GET | `/catalogs/{cat}/assets` | List assets, paginated |
| GET | `/catalogs/{cat}/assets/{asset}` | Single asset detail |
| PUT | `/catalogs/{cat}/assets/{asset}/revisions/{rev}` | Create/update revision (required before uploading bytes) |
| PUT | `/catalogs/{cat}/assets/{asset}/revisions/{rev}/master` | Upload original file bytes |
| GET | `/catalogs/{cat}/assets/{asset}/renditions/{type}` | Get rendition (`thumbnail2x`, `1280`, `2048`, `2560`, `fullsize`) |
| POST | `/catalogs/{cat}/assets/{asset}/renditions/{type}` | Request rendition generation (async) |

#### Listing assets — pagination
```http
GET /v2/catalogs/{cat}/assets?limit=50
```
Response includes a `_links.next.href` if more pages exist:
```json
{
  "resources": [...],
  "_links": {
    "next": { "href": "assets?name_after=urn:aaid:..." }
  }
}
```
Pass the relative `href` back as the next request path. Don't try to construct it yourself — the cursor is opaque.

Filters (combine with `&`):
- `subtype=image`, `subtype=video`
- `name_after=<asset_id>` (cursor)
- `captured_after=2026-05-01T00:00:00.000Z`
- `captured_before=2026-05-31T23:59:59.999Z`
- `updated_after=...` (catalog modification time)
- `sha256=<hex>` (find by content hash — useful for dedupe before upload)
- `order_after=<sort_key>` (cursor in current sort order)

#### Asset detail
```python
GET /v2/catalogs/{cat}/assets/{asset_id}
→ {
  "id": "...",
  "subtype": "image",
  "payload": {
    "captureDate": "2026-05-06T14:32:01",
    "develop": {           # Lightroom develop settings, same key vocabulary as XMP
      "Exposure2012": 0.5,
      "Contrast2012": 20,
      ...
    },
    "ratings": {"<user_id>": {"rating": 5}},
    "xmp": { ... },        # Full XMP serialization
    "importSource": {...},
    "video": {...},
  },
  "_links": {
    "/rels/rendition_type/2048": {"href": "..."},
    "/rels/rendition_type/fullsize": {"href": "..."},
    "/rels/master": {"href": "..."},
  }
}
```

#### Upload an asset
Two-step (revision then bytes):
```python
import uuid, hashlib, requests, json

def lr(method, path, **kwargs):
    r = requests.request(method, f"https://lr.adobe.io/v2/{path}",
        headers={"X-API-Key": API_KEY, "Authorization": f"Bearer {TOKEN}"},
        **kwargs)
    r.raise_for_status()
    return json.loads(r.text.replace("while (1) {}", "")) if r.text else {}

def upload(file_path, content_type="image/jpeg"):
    cat = lr("GET", "catalog")["id"]

    asset_id = uuid.uuid4().hex
    rev_id = uuid.uuid4().hex
    sha = hashlib.sha256(open(file_path, "rb").read()).hexdigest()

    # Step 1: declare the revision
    lr("PUT", f"catalogs/{cat}/assets/{asset_id}/revisions/{rev_id}",
       headers={"Content-Type": "application/json", "If-None-Match": sha},
       data=json.dumps({
           "subtype": "image",
           "payload": {
               "captureDate": "0000-00-00T00:00:00",
               "userCreated": "2026-05-07T12:00:00Z",
               "userUpdated": "2026-05-07T12:00:00Z",
               "importSource": {
                   "fileName": file_path.split("/")[-1],
                   "importTimestamp": "2026-05-07T12:00:00Z",
                   "importedOnDevice": "claude-skill",
                   "importedBy": API_KEY,
               }
           }
       }))

    # Step 2: upload the bytes
    with open(file_path, "rb") as f:
        lr("PUT", f"catalogs/{cat}/assets/{asset_id}/revisions/{rev_id}/master",
           headers={"Content-Type": content_type}, data=f)

    return asset_id
```

The `If-None-Match: <sha256>` header lets the server reject duplicate uploads (returns 412 Precondition Failed).

#### Revisions
Each edit creates a new revision under the same `asset_id`. Lightroom keeps the linear history but only the **latest** revision is shown in the UI by default.

### Albums

| Verb | Path | Purpose |
|---|---|---|
| GET | `/catalogs/{cat}/albums` | List albums |
| GET | `/catalogs/{cat}/albums/{album}` | Album detail |
| PUT | `/catalogs/{cat}/albums/{album}` | Create / update |
| DELETE | `/catalogs/{cat}/albums/{album}` | Soft-delete (not always available) |
| GET | `/catalogs/{cat}/albums/{album}/assets` | List assets in album |
| PUT | `/catalogs/{cat}/albums/{album}/assets` | Add assets (body lists asset ids) |

#### Create an album
```python
album_id = uuid.uuid4().hex
lr("PUT", f"catalogs/{cat}/albums/{album_id}",
   headers={"Content-Type": "application/json"},
   data=json.dumps({
       "subtype": "collection",  # "collection" or "collection_set"
       "serviceId": "lr_mobile",
       "payload": {
           "userCreated": "2026-05-07T12:00:00Z",
           "userUpdated": "2026-05-07T12:00:00Z",
           "name": "Spring 2026",
           "parent": { "id": "<parent_album_id>" }   # optional
       }
   }))
```

#### Add assets to an album
```python
lr("PUT", f"catalogs/{cat}/albums/{album_id}/assets",
   headers={"Content-Type": "application/json"},
   data=json.dumps({
       "resources": [
           {"id": asset_id_1, "payload": {"order": "1"}, "subtype": "image"},
           {"id": asset_id_2, "payload": {"order": "2"}, "subtype": "image"},
       ]
   }))
```

### Renditions

Pre-built sizes available without re-rendering: `thumbnail2x`, `1280`, `2048`, `2560`, `fullsize`.

```python
GET /v2/catalogs/{cat}/assets/{asset}/renditions/2048
→ JPEG bytes (Content-Type: image/jpeg)
```

Some renditions are generated on demand:
```python
POST /v2/catalogs/{cat}/assets/{asset}/renditions/2048
→ 202 Accepted (job queued); poll the GET endpoint until 200
```

## Python wrapper — lou-k/lightroom-cc-api

The reference Python implementation (incomplete but functional). Install:
```bash
pip install git+https://github.com/lou-k/lightroom-cc-api.git
brew install libmagic    # required runtime dep
```

Usage:
```python
from lightroom import Lightroom
lr = Lightroom(api_key=API_KEY, token=TOKEN)
catalog = lr.catalog_api()

assets = catalog.assets(limit=50)
for a in assets["resources"]:
    print(a["id"], a["payload"]["captureDate"])

asset_id, was_existing = catalog.upload_media_file_if_not_exists("/path/photo.jpg")
```

Caveats:
- Last meaningful commit ~2020. Schema may have drifted.
- No rendition endpoints implemented.
- No album-update / album-delete.
- Sync logic in `sync.py` is opinionated — read before relying.
- Use as a starting point; expect to drop down to raw `requests` for new endpoints.

## Direct HTTP via curl

For one-off ops or debugging:
```bash
TOKEN="$(jq -r .access_token < ~/lr-token.json)"
API_KEY="<your_client_id>"

# Health
curl -s -H "X-API-Key: $API_KEY" -H "Authorization: Bearer $TOKEN" \
  https://lr.adobe.io/v2/health | sed 's/^while (1) {}//' | jq

# Catalog
curl -s -H "X-API-Key: $API_KEY" -H "Authorization: Bearer $TOKEN" \
  https://lr.adobe.io/v2/catalog | sed 's/^while (1) {}//' | jq

# Assets list
CAT=$(curl -s -H "X-API-Key: $API_KEY" -H "Authorization: Bearer $TOKEN" \
  https://lr.adobe.io/v2/catalog | sed 's/^while (1) {}//' | jq -r .id)
curl -s -H "X-API-Key: $API_KEY" -H "Authorization: Bearer $TOKEN" \
  "https://lr.adobe.io/v2/catalogs/$CAT/assets?limit=10" | sed 's/^while (1) {}//' | jq
```

## Rate limits and quotas

- **Default quota**: ~1000 requests/hour per API key (varies by Adobe plan tier).
- **429 Too Many Requests**: respect `Retry-After` header (seconds).
- **Bulk upload**: serialize, don't fan out. Upload pipeline can saturate at ~5 concurrent PUTs before throttling.
- **Quota lives at the API-key level, not user level** — multiple users sharing one key share the quota.

## Common errors

| Status | Meaning | Fix |
|---|---|---|
| 401 | Token expired or invalid | Refresh via `refresh_token` |
| 403 | Missing scope or unapproved API | Add `lr_partner_apis` scope; ensure Adobe approved your app for production |
| 404 | Asset/album not found | Check ID format (32-hex, no dashes) |
| 409 | Conflict (e.g., revision already exists) | Generate a new UUID |
| 412 | If-None-Match precondition failed (duplicate sha256) | File already uploaded, look it up via `?sha256=` |
| 429 | Rate limit | Back off per `Retry-After` |
| 500/502/503 | Adobe-side issue | Retry with exponential backoff, max 3 attempts |

## Webhooks (change notifications)

Adobe Sign-Up required. Endpoint receives POSTs on asset/album/catalog mutations. Useful to drive an automation that runs after manual edits in Lightroom.
- Register: developer console → Project → Events
- Payload: `{event_type, asset_id, catalog_id, timestamp, ...}`
- Verify HMAC signature: `X-Adobe-Signature` header, signed with `client_secret`.

Out of scope here — see Adobe I/O Events docs for the full lifecycle.
