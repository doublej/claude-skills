# Adobe Firefly Services API Reference

## Authentication

```
POST https://ims-na1.adobelogin.com/ims/token/v3
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id=$FIREFLY_SERVICES_CLIENT_ID
&client_secret=$FIREFLY_SERVICES_CLIENT_SECRET
&scope=openid,AdobeID,session,additional_info,read_organizations,firefly_api,ff_apis
```

Response: `{ access_token, expires_in, token_type }`

## SDK Packages

| Package | Class | Purpose |
|---------|-------|---------|
| `@adobe/photoshop-apis` | `PhotoshopClient` | PSD editing, renditions, masks, background removal |
| `@adobe/firefly-apis` | `FireflyClient` | Text-to-image, generative fill/expand |
| `@adobe/lightroom-apis` | `LightroomClient` | Auto-tone, presets, manual edits |
| `@adobe/firefly-services-common-apis` | `ServerToServerTokenProvider` | Auth token management |

## SDK Authentication Pattern

```typescript
import { ServerToServerTokenProvider } from "@adobe/firefly-services-common-apis";
import { CoreTypes } from "@adobe/firefly-apis";

const authProvider: CoreTypes.TokenProvider = new ServerToServerTokenProvider(
  {
    clientId: process.env.FIREFLY_SERVICES_CLIENT_ID!,
    clientSecret: process.env.FIREFLY_SERVICES_CLIENT_SECRET!,
    scopes: "openid,AdobeID,session,additional_info,read_organizations,firefly_api,ff_apis",
  },
  { autoRefresh: true }
);

const config = { tokenProvider: authProvider, clientId: process.env.FIREFLY_SERVICES_CLIENT_ID! };
```

## Storage Types

```typescript
import { StorageType } from "@adobe/photoshop-apis";

StorageType.EXTERNAL   // Pre-signed URLs (S3, Azure, GCS, Dropbox)
StorageType.AZURE      // Azure Blob Storage
StorageType.DROPBOX    // Dropbox
```

For Firefly upload API, use `uploadId` references instead.

---

## PhotoshopClient Methods

### removeBackground(request)
Remove background from image (AI-powered).

```typescript
const result = await photoshop.removeBackground({
  input: { href: "<input-url>", storage: StorageType.EXTERNAL },
  output: { href: "<output-url>", storage: StorageType.EXTERNAL },
});
```

### createMask(request)
Generate image mask isolating subject.

```typescript
const result = await photoshop.createMask({
  input: { href: "<input-url>", storage: StorageType.EXTERNAL },
  output: { href: "<output-url>", storage: StorageType.EXTERNAL },
});
```

### createDocument(request)
Create new PSD with layers.

```typescript
const result = await photoshop.createDocument({
  options: {
    document: { width: 1920, height: 1080, resolution: 72, fill: "transparent", mode: "rgb" },
    layers: [
      { type: "layer", name: "Background" },
      { type: "textLayer", name: "Title", text: { content: "Hello", characterStyles: [...] } },
    ],
  },
  outputs: [{ href: "<output-url>", storage: StorageType.EXTERNAL, type: "image/vnd.adobe.photoshop" }],
});
```

### modifyDocument(request)
Apply layer edits, add/edit adjustment, pixel, and shape layers.

```typescript
const result = await photoshop.modifyDocument({
  inputs: [{ href: "<psd-url>", storage: StorageType.EXTERNAL }],
  options: {
    layers: [
      { id: 1, edit: {}, adjustments: { brightnessContrast: { brightness: 25 } } },
    ],
  },
  outputs: [{ href: "<output-url>", storage: StorageType.EXTERNAL, type: "image/vnd.adobe.photoshop" }],
});
```

### editTextLayer(request)
Modify text layer content.

```typescript
const result = await photoshop.editTextLayer({
  inputs: [{ href: "<psd-url>", storage: StorageType.EXTERNAL }],
  options: {
    layers: [
      { id: 1, name: "Title", text: { content: "New Text", characterStyles: [{ fontSize: 24, fontName: "Arial" }] } },
    ],
  },
  outputs: [{ href: "<output-url>", storage: StorageType.EXTERNAL, type: "image/vnd.adobe.photoshop" }],
});
```

### createRendition(request)
Create flat image representations of a PSD in multiple formats.

```typescript
const result = await photoshop.createRendition({
  inputs: [{ href: "<psd-url>", storage: StorageType.EXTERNAL }],
  outputs: [
    { href: "<output-jpg>", storage: StorageType.EXTERNAL, type: "image/jpeg", quality: 90 },
    { href: "<output-png>", storage: StorageType.EXTERNAL, type: "image/png" },
  ],
});
```

### getDocumentManifest(request)
Extract metadata including file and layer information from PSDs.

```typescript
const result = await photoshop.getDocumentManifest({
  inputs: [{ href: "<psd-url>", storage: StorageType.EXTERNAL }],
});
// result.result → { document: { width, height, ... }, layers: [...] }
```

### replaceSmartObject(request)
Replace smart object content in a PSD.

```typescript
const result = await photoshop.replaceSmartObject({
  inputs: [{ href: "<psd-url>", storage: StorageType.EXTERNAL }],
  options: {
    layers: [{ name: "SmartObjectLayer", input: { href: "<replacement-url>", storage: StorageType.EXTERNAL } }],
  },
  outputs: [{ href: "<output-url>", storage: StorageType.EXTERNAL, type: "image/vnd.adobe.photoshop" }],
});
```

### playPhotoshopActions(request)
Execute Photoshop Action file (.atn) against PSD/JPEG/PNG/TIFF.

```typescript
const result = await photoshop.playPhotoshopActions({
  inputs: [{ href: "<input-url>", storage: StorageType.EXTERNAL }],
  options: {
    actions: [{ href: "<action-file-url>", storage: StorageType.EXTERNAL }],
  },
  outputs: [{ href: "<output-url>", storage: StorageType.EXTERNAL, type: "image/jpeg" }],
});
```

### playPhotoshopActionsJson(request)
Execute operations using actionJSON format (no .atn file needed).

### convertToActionsJson(request)
Convert .atn file to actionJSON format.

### createArtboard(request)
Create artboards from multiple PSD inputs.

### applyDepthBlur(request)
Apply depth blur effect to an image.

### applyAutoCrop(request)
Smart crop preserving subject focus.

---

## FireflyClient Methods

### generateImages({ prompt, ... })
Text-to-image generation.

```typescript
const result = await firefly.generateImages({ prompt: "A mountain landscape at sunset" });
// result.result.outputs[0].image.url → generated image URL
```

### expandImage(request)
Generative expand — resize to new dimensions filling new areas with AI content.

```typescript
const result = await firefly.expandImage({
  image: { source: { uploadId: "<upload-id>" } },
  size: { width: 1920, height: 1080 },
});
```

### fillImage(request)
Generative fill — fill masked area with AI-generated content.

```typescript
const result = await firefly.fillImage({
  image: {
    source: { uploadId: "<source-id>" },
    mask: { uploadId: "<mask-id>" },
  },
  prompt: "A tropical beach background",
});
```

### upload(file)
Upload content to Firefly storage, returns uploadId.

```typescript
// REST approach:
const response = await axios.post("https://firefly-api.adobe.io/v2/storage/image", fileStream, {
  headers: {
    Authorization: `Bearer ${accessToken}`,
    "X-API-Key": clientId,
    "Content-Type": "image/png",
    "Content-Length": fileSizeInBytes,
  },
});
// response.data.images[0].id → uploadId
```

---

## LightroomClient Methods

| Method | Description |
|--------|-------------|
| `applyAutoTone(request)` | Auto-adjust exposure, contrast, sharpness, saturation |
| `applyPreset(request)` | Apply XMP Lightroom preset |
| `applyEdits(request)` | Manual edits (exposure, contrast, sharpness, saturation) |
| `autoStraighten(request)` | Auto Upright transformation |

---

## REST API Endpoints (direct HTTP)

| Endpoint | Operation |
|----------|-----------|
| `POST https://firefly-api.adobe.io/v2/storage/image` | Upload image |
| `POST https://firefly-api.adobe.io/v3/images/generate` | Generate images |
| `POST https://firefly-api.adobe.io/v3/images/expand-async` | Expand image |
| `POST https://firefly-api.adobe.io/v3/images/fill` | Fill image |
| `POST https://image.adobe.io/sensei/cutout` | Remove background |
| `POST https://image.adobe.io/sensei/mask` | Create mask |
| `POST https://image.adobe.io/pie/psdService/documentCreate` | Create document |
| `POST https://image.adobe.io/pie/psdService/documentOperations` | Modify document |
| `POST https://image.adobe.io/pie/psdService/text` | Edit text layer |
| `POST https://image.adobe.io/pie/psdService/renditionCreate` | Create rendition |
| `POST https://image.adobe.io/pie/psdService/documentManifest` | Get manifest |
| `POST https://image.adobe.io/pie/psdService/smartObject` | Replace smart object |
| `POST https://image.adobe.io/pie/psdService/photoshopActions` | Play actions |
| `POST https://image.adobe.io/pie/psdService/actionJSON` | Play actions JSON |
| `POST https://image.adobe.io/pie/psdService/artboardCreate` | Create artboard |
| `POST https://image.adobe.io/sensei/depthBlur` | Depth blur |
| `POST https://image.adobe.io/sensei/autoCrop` | Auto crop |

All REST endpoints require headers:
```
Authorization: Bearer <access_token>
x-api-key: <client_id>
Content-Type: application/json
```

## Output Types

| MIME Type | Extension |
|-----------|-----------|
| `image/vnd.adobe.photoshop` | .psd |
| `image/jpeg` | .jpg |
| `image/png` | .png |
| `image/tiff` | .tiff |

## File Size Limits

- Input files: < 1000 MB
- Supported input: PSD, JPEG, PNG, TIFF (varies per endpoint)
