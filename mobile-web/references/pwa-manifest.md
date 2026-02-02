# PWA Manifest Reference

## Minimal Installable Manifest

```json
{
  "name": "My App",
  "short_name": "App",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#0072FF",
  "description": "Brief app description",
  "icons": [
    { "src": "/icon-192.png", "type": "image/png", "sizes": "192x192" },
    { "src": "/icon-512.png", "type": "image/png", "sizes": "512x512" },
    { "src": "/icon-mask.png", "type": "image/png", "sizes": "512x512", "purpose": "maskable" }
  ]
}
```

## Display Modes

| Mode | Behavior |
|------|----------|
| `standalone` | App-like, no browser UI (recommended for PWAs) |
| `fullscreen` | No status bar, no browser UI |
| `minimal-ui` | Minimal browser controls |
| `browser` | Normal browser tab |

## Icons

- 192×192: home screen icon
- 512×512: splash screen and install prompt
- 512×512 maskable: safe zone is ~72% center; use solid background, centered logo

## Optional Members

```json
{
  "orientation": "portrait",
  "scope": "/",
  "categories": ["utilities"],
  "screenshots": [
    {
      "src": "/screenshot-wide.png",
      "sizes": "1280x720",
      "type": "image/png",
      "form_factor": "wide"
    },
    {
      "src": "/screenshot-narrow.png",
      "sizes": "750x1334",
      "type": "image/png",
      "form_factor": "narrow"
    }
  ],
  "shortcuts": [
    {
      "name": "New Item",
      "short_name": "New",
      "url": "/new",
      "icons": [{ "src": "/icon-shortcut.png", "sizes": "192x192" }]
    }
  ]
}
```

## File Naming

- Recommended: `manifest.webmanifest` (official extension)
- Alternative: `manifest.json` (widely used)
- Content-Type: `application/manifest+json`
- Place in site root, link from all HTML pages

## iOS Limitations

Safari ignores manifest icons — always include:
```html
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
```
