# Lightroom Service / Firefly Services AI Ops

Async image-processing endpoints. Submit a job, poll for status, fetch the result. All under `https://image.adobe.io/lrService/`.

These are part of **Adobe Firefly Services** (Lightroom Service is the Lightroom-flavored subset). They run on Adobe-hosted infra — your inputs/outputs are storage references (Adobe Cloud Storage, AWS S3, Azure Blob, signed HTTPS URLs).

Reference docs: https://developer.adobe.com/firefly-services/docs/lightroom/

## Auth

Same as `rest-api.md`:
```http
X-API-Key: <client_id>
Authorization: Bearer <user_access_token>
```

Lightroom Service jobs run **on behalf of the user** — token must be a user OAuth token, not a service token. (Firefly Services as a whole supports service tokens for some endpoints, but Lightroom Service requires user context for catalog access.)

## Job lifecycle

```
1. POST /<operation>          → 202 Accepted, returns { jobId, _links.self }
2. GET  /status/<jobId>       → poll: status ∈ {pending, running, succeeded, failed}
3. When succeeded:            outputs[].href points to the result file
```

Sample status responses:

**Pending**
```json
{
  "jobId": "f54e0fcb-260b-47c3-b520-de0d17dc2b67",
  "created": "2026-05-07T12:57:15Z",
  "modified": "2026-05-07T12:58:36Z",
  "outputs": [{"input": "/in/photo.jpg", "status": "pending"}]
}
```

**Succeeded**
```json
{
  "jobId": "...",
  "outputs": [{
    "input": "/in/photo.jpg",
    "status": "succeeded",
    "_links": { "self": { "href": "/out/photo.jpg", "storage": "adobe" } }
  }]
}
```

**Failed**
```json
{
  "jobId": "...",
  "outputs": [{
    "input": "/in/photo.jpg",
    "status": "failed",
    "errorDetails": "request parameters didn't validate"
  }]
}
```

## Operations

### autoTone — auto-balance exposure / contrast / color

```http
POST https://image.adobe.io/lrService/autoTone HTTP/1.1
Content-Type: application/json
X-API-Key: ...
Authorization: Bearer ...

{
  "inputs":  [{"href": "https://your-server/in.jpg",  "storage": "external"}],
  "outputs": [{"href": "s3://bucket/out.jpg", "storage": "external"}]
}
```

Response: `202 Accepted`, `{ jobId, _links }`.

`storage` values: `adobe` (Adobe Cloud Storage), `external` (signed HTTPS / S3 / Azure URL). Inputs and outputs can mix.

### autoStraighten — level horizon / fix tilt

Same shape as autoTone:
```http
POST /lrService/autoStraighten
{ "inputs": [...], "outputs": [...] }
```

### presets — apply a preset XMP

```http
POST /lrService/presets
{
  "inputs":  [{"href": "...", "storage": "..."}],
  "outputs": [{"href": "...", "storage": "..."}],
  "options": {
    "preset": {"href": "...", "storage": "..."}    # XMP preset file
  }
}
```

Preset must be a valid Lightroom preset XMP (see `xmp-sidecar.md` for the format). Hosted at one of the supported storage backends.

### presets/xmp — Camera Raw / develop adjustments inline

```http
POST /lrService/presets/xmp
{
  "inputs":  [...],
  "outputs": [...],
  "options": {
    "xmp": {
      "Exposure2012": 0.5,
      "Contrast2012": 20,
      "Vibrance": 15
    }
  }
}
```

Pass develop settings directly as a JSON object — server constructs the preset, applies, and renders. Same key vocabulary as `develop-settings-keys.md`.

### Edits combined

Auto-tone + auto-straighten + preset can be combined in a single request via the `edit` field:
```json
{
  "inputs": [...],
  "outputs": [...],
  "options": {
    "edit": {
      "autoTone": true,
      "autoStraighten": true,
      "preset": {"href": "...", "storage": "..."}
    }
  }
}
```
One round-trip, ~30-60s for typical RAW.

## Polling pattern

```python
import requests, time, json

API = "https://image.adobe.io/lrService"
HEADERS = {"X-API-Key": API_KEY, "Authorization": f"Bearer {TOKEN}",
           "Content-Type": "application/json"}

def submit_auto_tone(input_url, output_url):
    r = requests.post(f"{API}/autoTone", headers=HEADERS, json={
        "inputs":  [{"href": input_url,  "storage": "external"}],
        "outputs": [{"href": output_url, "storage": "external"}]
    })
    r.raise_for_status()
    return r.json()["jobId"]

def wait_for_job(job_id, timeout=300, interval=2):
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.get(f"{API}/status/{job_id}", headers=HEADERS)
        r.raise_for_status()
        body = r.json()
        out = body["outputs"][0]
        if out["status"] == "succeeded":
            return out["_links"]["self"]["href"]
        if out["status"] == "failed":
            raise RuntimeError(out.get("errorDetails", "job failed"))
        time.sleep(interval)
    raise TimeoutError(f"job {job_id} did not complete within {timeout}s")

job = submit_auto_tone("https://my-cdn/in.jpg", "https://my-cdn/out.jpg")
result = wait_for_job(job)
```

## Storage backends

### Adobe Cloud Storage
- `storage: "adobe"`
- `href` is a path like `/files/<uuid>/photo.jpg`
- Upload via Adobe I/O Storage API (separate auth flow)
- Best when you stay inside Adobe ecosystem

### External (S3, Azure, signed HTTPS)
- `storage: "external"`
- `href` is a full URL with auth (signed URL or pre-shared)
- Adobe pulls input via GET, pushes output via PUT
- URL must be reachable from Adobe data centers

For signed S3 PUT URLs:
```python
import boto3
s3 = boto3.client("s3")
url = s3.generate_presigned_url(
    "put_object",
    Params={"Bucket": "my-bucket", "Key": "out.jpg", "ContentType": "image/jpeg"},
    ExpiresIn=3600
)
```

For S3 GET URLs (input):
```python
url = s3.generate_presigned_url("get_object", Params={"Bucket": "...", "Key": "..."}, ExpiresIn=3600)
```

URL must remain valid for the full job duration — give 1h+ buffer.

## Concurrency + rate limits

- Default: ~10 concurrent jobs per user, ~100 jobs/hour.
- 429 with `Retry-After` if exceeded.
- For batch processing, queue submits with a worker pool of 5-10 and exponential backoff.

## Error semantics

| Status | Meaning |
|---|---|
| 202 | Job accepted, poll status |
| 400 | Bad request (validate inputs/outputs URLs) |
| 401 | Token expired |
| 403 | Missing scope / Firefly Services not enabled on account |
| 415 | Unsupported input format (some RAW types not accepted — check codec list) |
| 429 | Rate limit |
| 500/502/503 | Adobe-side, retry with backoff |

Failed jobs return 202 too — failure is reported in `outputs[].status`. Always check `status`, not just HTTP code.

## Supported input formats

JPEG, PNG, TIFF, DNG, plus most camera RAW formats (CR2, CR3, NEF, ARW, RAF, ORF, RW2, etc.). HEIC/HEIF supported on newer plan tiers.

Output: JPEG by default. Some operations support DNG output for raw → raw pipelines (check Adobe docs for current matrix).

## Cost model

Firefly Services is **paid metered** — each job consumes "Generative Credits" or "Edit Credits" depending on the operation:
- autoTone / autoStraighten: Edit Credits (~1 per call)
- preset apply: Edit Credits (~1 per call)
- AI denoise / super-resolution (separate endpoints, not covered): Generative Credits (10-50 per call)

Free tier on Photography plan covers light usage. Heavy automation pipelines should budget against the metered tier — see Adobe Firefly Services pricing.

## When to use REST AI vs XMP-only

| Goal | Use |
|---|---|
| Apply known-good preset to a folder, no AI inference needed | **XMP** (free, faster, no auth) |
| Auto-balance exposure when you don't know the right values | **autoTone via API** |
| Straighten a tilted horizon programmatically | **autoStraighten via API** |
| Generate develop settings from scratch using AI | **autoTone, then read back result XMP via REST asset.develop** |
| Apply a preset to 1000 RAWs in a loop | **XMP** (avoids per-call quota) |
| Apply preset *and* AI normalize each image | **/presets/xmp with autoTone option** |

The split: deterministic edits → XMP, inference-driven edits → API.
