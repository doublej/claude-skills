---
name: lightroom
description: Automate Adobe Lightroom (the cloud/desktop app, version 7.x-9.x — formerly "Lightroom CC") via two paths. Path A is XMP sidecar editing — offline, no auth, write develop settings/ratings/keywords to .xmp files alongside RAW/JPEG. Path B is the Lightroom Services REST API — cloud catalog (assets, albums, metadata) plus async AI ops (auto-tone, auto-straighten, preset application) via Lightroom Service / Firefly Services. NOT for Lightroom Classic — that's a different app with .lrcat catalogs and a Lua plugin SDK. Triggers on "lightroom" (no "Classic"), "Lightroom CC", "Lightroom desktop", "Lightroom cloud", "XMP sidecar", "develop preset XMP", "auto-tone via API", "Adobe Lightroom REST", ".xmp file", "edit metadata on RAW".
---

# Lightroom (cloud / desktop)

The "new Lightroom" — versions 7.x-9.x, formerly Lightroom CC. Edits live in Adobe's cloud, sync across devices. **No Lua plugin SDK** — automation goes through XMP sidecars (offline) or the REST API (cloud).

<not_lightroom_classic>
This skill is **NOT** for Lightroom Classic (versions 13.x-15.x, the .lrcat catalog app). For that, see the deprecated `Automaat/lightroom-mcp` plugin path. The two products have unrelated automation surfaces.
</not_lightroom_classic>

<path_selection>
| Need | Path | Why |
|---|---|---|
| Develop settings / ratings / keywords on local files | **XMP sidecar** | No auth. Files re-sync into Lightroom on next import or `Read Metadata from File`. |
| List/upload/download cloud assets and albums | **REST API** | Direct cloud catalog control. OAuth2 required. |
| AI auto-tone, auto-straighten, preset apply on arbitrary images | **REST API → Lightroom Service / Firefly Services** | Async job queue, returns processed file. |
| Discover what edits are on a photo | **XMP** (read crs: keys) or REST `asset.develop` | XMP for local files, REST for cloud-only photos. |
| Bulk metadata changes across thousands of files | **XMP** | Faster than REST round-trips, no API quota. |
</path_selection>

## Path A — XMP sidecar editing

Works on **any RAW/JPEG file** with or without a paired `.xmp`. Lightroom (cloud) reads sidecars on import and on **Photo → Read Metadata from File**.

### Format basics

`.xmp` is XML with namespaced attributes. Lightroom develop settings live in the `crs:` (Camera Raw Settings) namespace. Same key names as Lightroom Classic SDK — see `references/develop-settings-keys.md`.

Minimal example (set exposure +0.5, contrast +20, 5-star rating):
```xml
<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about=""
      xmlns:crs="http://ns.adobe.com/camera-raw-settings/1.0/"
      xmlns:xmp="http://ns.adobe.com/xap/1.0/"
      xmlns:dc="http://purl.org/dc/elements/1.1/"
      crs:Version="15.4"
      crs:ProcessVersion="11.0"
      crs:Exposure2012="+0.50"
      crs:Contrast2012="+20"
      xmp:Rating="5">
      <dc:subject>
        <rdf:Bag>
          <rdf:li>portrait</rdf:li>
          <rdf:li>2026</rdf:li>
        </rdf:Bag>
      </dc:subject>
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>
```

### Tools

| Tool | Use | Pros / cons |
|---|---|---|
| **ExifTool** (`brew install exiftool`) | Read/write any XMP attribute via CLI | Battle-tested, scriptable, handles RAW embedded XMP |
| **python-xmp-toolkit** (`pip install python-xmp-toolkit`) | Programmatic XMP read/write | Wraps Adobe XMP Toolkit |
| **lxml + plain string templating** | Write fresh `.xmp` files | Simplest for batch writes, no library deps beyond lxml |

ExifTool one-liner pattern:
```bash
exiftool -xmp-crs:Exposure2012=+0.5 -xmp-crs:Contrast2012=+20 \
         -xmp-dc:Subject="portrait" -xmp:Rating=5 \
         -overwrite_original photo.cr3
```
For RAW formats (CR3, NEF, ARW, RAF), ExifTool writes a sidecar `photo.xmp` automatically when the format is read-only.

Full XMP details + write recipes: `references/xmp-sidecar.md`.

### Lightroom round-trip

1. Edit `.xmp` next to source file.
2. In Lightroom (desktop): **Photo → Read Metadata from File** (or re-import). Develop settings and metadata are picked up.
3. Edits then sync to cloud and other devices.

<xmp_traps>
- New Lightroom does **not** auto-watch sidecars. User must trigger Read Metadata.
- Already-imported photos: edits in cloud win unless Read Metadata is run. Don't assume sidecar changes are live.
- Local adjustments (masks, brushes, AI subject/sky) are stored as nested XMP structures — easier to copy from a reference photo's XMP than to author from scratch.
- Some develop keys (e.g. AI denoise) are not representable in XMP — they require running the AI model.
</xmp_traps>

## Path B — Lightroom Services REST API

Two endpoints serve different concerns:

| Base URL | Purpose |
|---|---|
| `https://lr.adobe.io/v2/` | Cloud catalog: assets, albums, account, metadata |
| `https://image.adobe.io/lrService/` | Async image ops: auto-tone, auto-straighten, apply preset |

### Auth setup (one-time)

1. **Register an Adobe Developer Console app**: https://developer.adobe.com/console/
2. **Add the Lightroom Services API** to the project. Scopes: `openid`, `offline_access`, `lr_partner_apis`.
3. **OAuth Web flow** to get a user token. Redirect URI must be HTTPS — local dev uses `https://localhost:8443` with a self-signed cert.
4. Tokens expire — use `offline_access` scope to get a refresh token.

Helper: `lou-k/adobe-io-auth` (Python) automates the local-callback dance. See `references/rest-api.md` for the full flow.

Every request:
```
X-API-Key: <client_id from Developer Console>
Authorization: Bearer <user_token>
```

### Quirk: leading garbage prefix

All JSON responses are prefixed with `while (1) {}` to defeat JSON hijacking. Strip it before parsing:
```python
text = response.text.replace('while (1) {}', '')
data = json.loads(text)
```

### Common endpoints

| Verb | Path | Purpose |
|---|---|---|
| GET | `/health` | Service health |
| GET | `/account` | Authed user account info |
| GET | `/catalog` | User's catalog id (one per account) |
| GET | `/catalogs/{cat}/assets` | List assets, paginated via `next` link |
| GET | `/catalogs/{cat}/assets/{asset}` | Asset detail (metadata, develop settings, links) |
| PUT | `/catalogs/{cat}/assets/{asset}/revisions/{rev}` | Create new revision (asset version) |
| PUT | `/catalogs/{cat}/assets/{asset}/revisions/{rev}/master` | Upload original bytes |
| GET | `/catalogs/{cat}/assets/{asset}/renditions/{type}` | Get rendition (thumbnail/preview) |
| GET | `/catalogs/{cat}/albums` | List albums |
| GET | `/catalogs/{cat}/albums/{album}` | Album detail |
| PUT | `/catalogs/{cat}/albums/{album}` | Create / update album |
| PUT | `/catalogs/{cat}/albums/{album}/assets` | Add assets to album |
| GET | `/catalogs/{cat}/albums/{album}/assets` | List assets in album |

Asset / album IDs are 32-char hex strings (UUID with dashes stripped). Generate client-side with `uuid.uuid4().hex`.

Full endpoint catalog + Python wrappers: `references/rest-api.md`.

### Lightroom Service / Firefly Services (AI ops)

Async job pattern — POST a request, poll status until `succeeded` or `failed`.

```
POST https://image.adobe.io/lrService/autoTone
POST https://image.adobe.io/lrService/autoStraighten
POST https://image.adobe.io/lrService/presets    (apply preset)
GET  https://image.adobe.io/lrService/status/{jobId}
```

Inputs and outputs reference Adobe Cloud Storage paths. Output appears at `_links.self.href` once the job's `status` is `succeeded`.

Details: `references/firefly-services.md`.

## Develop settings — key reference

Both paths use the same key vocabulary:
- **XMP**: attributes in `crs:` namespace (e.g., `crs:Exposure2012="+0.50"`)
- **REST asset.develop**: object keys (e.g., `{"Exposure2012": 0.5}`)

See `references/develop-settings-keys.md` for the full list (basic, tone curve, HSL, color grading, detail, lens, transform, effects, calibration) and traps (`Vibrance` has no `2012` suffix, etc.).

## Workflow recipes

### Batch-rate + keyword via XMP
```bash
# Mark these CR3s as 5-star + tag
for f in /shoots/2026-05-06/*.CR3; do
  exiftool -xmp:Rating=5 -xmp-dc:Subject+="client-acme" -xmp-dc:Subject+="2026" \
           -overwrite_original "$f"
done
# In Lightroom desktop: select photos → Photo → Read Metadata from File
```

### Apply a preset XMP to a directory
A `.xmp` exported from Lightroom (or generated by AI) is itself a complete crs: blob. Use ExifTool to copy it onto each photo:
```bash
exiftool -tagsFromFile preset.xmp -all:all -overwrite_original /shoots/2026-05-06/*.CR3
```
Then in Lightroom: Read Metadata from File. Photos pick up the preset's settings.

### List recent cloud assets via REST
```python
import requests, json
def lr_get(path):
    r = requests.get(f"https://lr.adobe.io/v2/{path}",
                     headers={"X-API-Key": API_KEY, "Authorization": f"Bearer {TOKEN}"})
    return json.loads(r.text.replace("while (1) {}", ""))

cat = lr_get("catalog")["id"]
assets = lr_get(f"catalogs/{cat}/assets?limit=50&order_after=2026-05-01")
```

### Auto-tone a folder via Firefly Services
```python
# 1. Upload originals to Adobe Cloud Storage (or pass signed URLs)
# 2. POST job
job = requests.post("https://image.adobe.io/lrService/autoTone",
    headers={"X-API-Key": API_KEY, "Authorization": f"Bearer {TOKEN}"},
    json={"inputs": [{"href": "s3://...", "storage": "external"}],
          "outputs": [{"href": "s3://.../out.jpg", "storage": "external"}]})
job_id = job.json()["jobId"]
# 3. Poll /status/{job_id} until status == 'succeeded'
```

Detailed multi-step recipes: `references/rest-api.md` and `references/firefly-services.md`.

## Out of scope

- **Lightroom Classic** (.lrcat, version 13+) — separate product, has Lua SDK + community MCP. Not covered here.
- **Lightroom mobile (iOS/Android)** — same cloud backend as desktop, controlled via the same REST API. Mobile app itself is opaque.
- **Generating develop AI masks** (subject/sky) from scratch — proprietary models. Apply via preset or copy from a reference photo's XMP.
- **Real-time edit streaming** — REST API is request/response, not push. Use webhooks (Adobe Sign-up required) for change notifications.
