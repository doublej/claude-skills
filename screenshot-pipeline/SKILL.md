---
name: screenshot-pipeline
description: Create polished promotional screenshots for apps, tools, and websites. Use when creating visual assets for social media, GitHub, App Store, or marketing. Covers full-page capture, individual element capture with transparency, device framing, compositing, manifest generation, and multi-platform export.
---

# Screenshot Pipeline

Produce polished, platform-optimized promotional screenshots from any project type. Supports full-page, window, and individual element capture with transparency preservation.

## Before Starting

Before doing any work, present the user with a plan overview. Scan the project to determine:

1. **Project type** — what kind of project is this (web app, Swift app, CLI, etc.)?
2. **Capture method** — which tool/approach will be used (Playwright, screencapture, simulator)?
3. **Capture targets** — full pages, specific elements, or both?
4. **Transparency needs** — any elements requiring alpha / border-radius preservation?
5. **Platform targets** — which export dimensions are needed (X, GitHub, App Store, etc.)?
6. **Manifest** — will OCR / color analysis be generated?

Print a short summary table like:

```
Screenshot Pipeline Plan
────────────────────────
Project type:    SvelteKit web app
Capture method:  Playwright (localhost:5173)
Targets:         3 full-page, 2 element (card, hero)
Transparency:    yes (card element — omitBackground)
Export to:       X/Twitter (1200×675), GitHub (1280×640)
Manifest:        yes — OCR, colors, contrast, dimensions
```

Wait for user confirmation before proceeding.

## Workflow

```
DETECT → CAPTURE → COMPOSE → EXPORT → MANIFEST → REVIEW
```

### 1. DETECT — Identify project type and capture method

```
Project type?
├── macOS/iOS Swift app
│   ├── Running app or simulator → screencapture / xcrun simctl
│   └── No build available → Faux HTML fallback
├── Web app (SvelteKit, Next.js, etc.)
│   → Playwright with device emulation on dev server
├── Electron/Tauri app
│   → Playwright against localhost OR screencapture
├── CLI tool
│   → ANSI-to-HTML terminal render + Playwright capture
└── API / Library (no UI)
    → Code snippet render (Shiki) + Playwright capture
```

Ask the user which screens/states to capture and for which platforms.

### 2. CAPTURE — Take raw screenshots

Use the best method for the project type. See `references/capture-methods.md` for detailed instructions per type.

For macOS native capture, use `scripts/capture.sh` helper.

**Capture modes:**
- **Full page / window** — standard capture (see capture-methods.md)
- **Element capture** — screenshot individual DOM elements with optional transparency (see `references/element-capture.md`)

**Capture checklist:**
- Use 2x resolution (Retina) when possible
- Capture the exact viewport/window — no desktop clutter
- If capturing multiple states, name files descriptively (e.g., `home-dark.png`, `settings-light.png`)
- Prefer PNG for lossless quality (required for transparency)

### 3. COMPOSE — Frame and style the screenshot

Build an HTML file that composites the raw screenshot into a polished promotional image.

**Composition elements:**
- **Frame style**: default, glass-light, glass-dark, liquid-glass, inset-light, inset-dark, outline (see `references/frame-styles.md`)
- **Background**: 10 named presets (cosmic, ocean, sunset, etc.) or custom gradient (see `references/background-presets.md`)
- **Shadow**: none, spread, hug, adaptive, elevated (see `references/shadow-presets.md`)
- **Effects** (optional): noise grain, VHS scan lines, subtle dot texture (see `references/effects-and-transforms.md`)
- **Transforms** (optional): zoom, tilt, or combined for 3D depth (see `references/effects-and-transforms.md`)
- **Watermark** (optional): logo or text in any corner (see `references/effects-and-transforms.md`)
- **Device bezel** (optional): iPhone, MacBook, browser chrome, or terminal frame
- **Annotations** (optional): feature callouts, text overlays, version badges
- **Padding**: ensure content doesn't touch edges — minimum 5% margin

See `references/compose-guide.md` for the parameters table and compositing principles. Use `references/html-template.md` for the base HTML template.

Generate a custom HTML file per composition. Use Playwright to render it at exact target dimensions.

### 4. EXPORT — Render at platform dimensions

Use Playwright to screenshot the HTML composition at exact pixel dimensions.

Quick reference (full specs in `references/platform-specs.md`):

| Platform | Dimensions | Aspect |
|----------|-----------|--------|
| X/Twitter | 1200×675 | 16:9 |
| Threads | 1080×1350 | 4:5 |
| LinkedIn | 1200×1200 | 1:1 |
| Substack | 1456×750 | ~2:1 |
| GitHub | 1280×640 | 2:1 |
| App Store (6.9") | 1320×2868 | ~1:2.2 |

Export as PNG. Generate one file per platform target.

**X.com multi-image layout:** When exporting multiple screenshots for X/Twitter, use the dual layout strategy — first and last images are single-screenshot, middle images pack two screenshots side-by-side. See `references/compose-guide.md` for the mapping logic and `references/html-template.md` for the dual template.

**Playwright export pattern:**
```bash
npx playwright screenshot --viewport-size="1200,675" compose.html output-twitter.png
```

Or use a short Node script if Playwright CLI isn't available — see compose-guide for the snippet.

### 5. MANIFEST — Generate screenshot index

Run `scripts/manifest.mjs` against the screenshots directory to produce `screenshots/manifest.json`.

```bash
node scripts/manifest.mjs screenshots/
```

The manifest records per screenshot:
- **ocr** — extracted text via tesseract.js
- **dimensions** — width × height in pixels
- **contrast** — estimated contrast ratio (light vs dark regions)
- **primaryColors** — top 5 dominant colors as hex values

See `references/element-capture.md` for manifest schema and usage details.

**Dependencies:** `npm install tesseract.js sharp get-image-colors` (install once in the project).

### 6. REVIEW — Show results and iterate

Present all generated images to the user. Offer adjustments:
- Frame style (e.g., switch from default to glass-dark or liquid-glass)
- Background preset or custom gradient
- Shadow intensity (e.g., spread to elevated, or none)
- Effects (add/remove noise, VHS, texture)
- Transforms (add tilt or zoom for depth)
- Watermark placement or text
- Bezel style changes (add/remove device frame)
- Annotation text or positioning
- Different app states or screens

## Integration with social-promotion

This skill creates the visuals; `social-promotion` writes the copy. Natural chain:
1. Run screenshot-pipeline to create images
2. Run social-promotion referencing those images

## Output

Place all generated files in a `screenshots/` directory in the project root:
```
screenshots/
├── raw/              # Original captures (full-page and element)
├── twitter.png       # Platform-specific exports
├── threads.png
├── linkedin.png
├── github-social.png
├── compose.html      # Source composition (for iteration)
└── manifest.json     # OCR, dimensions, contrast, colors per screenshot
```
