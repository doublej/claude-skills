# Compositing Guide

Orchestrator for screenshot composition. Style catalogs live in dedicated reference files.

## Principles

1. **One focal point** — the screenshot is the hero. Everything else supports it.
2. **Breathing room** — minimum 5% padding on all sides. More is usually better.
3. **Brand alignment** — pull colors from the app itself for backgrounds and accents.
4. **Legible annotations** — if adding text, ensure contrast ratio >= 4.5:1. Bold, short phrases.
5. **Consistent style** — all screenshots for a project share the same composition style.

## Compose Parameters

| Parameter | Options | Default | Reference |
|-----------|---------|---------|-----------|
| Frame style | default, glass-light, glass-dark, liquid-glass, inset-light, inset-dark, outline | default | frame-styles.md |
| Border radius | sharp (8px), curved (20px), round (36px) | curved | frame-styles.md |
| Background | cosmic, mystic, ocean, sunset, earth, radiant, glass, clean, dark, transparent, custom | cosmic | background-presets.md |
| Shadow | none, spread, hug, adaptive, elevated | spread | shadow-presets.md |
| Effect | none, noise, vhs, subtle-texture | none | effects-and-transforms.md |
| Transform | none, zoom, tilt, tilt-zoom | none | effects-and-transforms.md |
| Watermark | none, logo, text | none | effects-and-transforms.md |
| Headline | any string | (none) | html-template.md |
| Subtitle | any string | (none) | html-template.md |

## X.com Multi-Image Layout

X/Twitter supports up to 4 images per post. When exporting multiple screenshots for X.com, use this layout strategy:

- **First image**: single screenshot (hero — strongest visual)
- **Middle images**: dual screenshot (two side-by-side per image, using the Dual Screenshot Template from html-template.md)
- **Last image**: single screenshot (closing — CTA or final state)

### Screenshot-to-image mapping

| Raw screenshots | X.com images | Layout |
|----------------|-------------|--------|
| 1 | 1 | single |
| 2 | 2 | single, single |
| 3 | 2 | single, single (best 2) or 3 → single, single, single |
| 4 | 3 | single, dual(2+3), single |
| 5 | 3 | single, dual(2+3), single (pick best 5 of raw) or 4 → single, dual(2+3), dual(4+5)... |
| 6 | 4 | single, dual(2+3), dual(4+5), single |
| 7 | 4 | single, dual(2+3), dual(4+5), single (pick best 6) |
| 8 | 4 | single, dual(2+3), dual(4+5,6+7), single — or condense as needed |

**Rule of thumb:** with N raw screenshots, fill up to 4 X.com images. First and last are always single. Pack remaining screenshots into middle images as side-by-side pairs. If there are more screenshots than slots, pick the most impactful ones.

### Dual image composition tips

- Use the same frame style, background, and shadow for both frames in a pair
- Screenshots in a pair should be related (e.g., before/after, two features, light/dark)
- Both images should have similar aspect ratios for balanced layout

## Device Bezels

When to use a device frame:
- **Yes**: App Store screenshots, mobile app promotions, "look at this on a phone" context
- **No**: GitHub social preview (too small), web app dashboards (maximize content)

Bezel approaches:
- **CSS mockup**: use a frame preset from frame-styles.md. Lightweight, good for most uses.
- **SVG device frame**: higher fidelity outline for specific device shapes.

### CSS Phone Notch (optional add-on)
```css
.device-frame.with-notch::before {
  content: '';
  position: absolute;
  top: 0; left: 50%;
  transform: translateX(-50%);
  width: 120px; height: 34px;
  background: #1a1a1a;
  border-radius: 0 0 20px 20px;
  z-index: 5;
}
```

## Annotations

```html
<!-- Feature callout -->
<div style="position:absolute;top:15%;right:8%;
  background:rgba(0,0,0,0.7);backdrop-filter:blur(10px);
  color:white;padding:12px 20px;border-radius:12px;
  font-family:system-ui;font-size:18px;font-weight:600;">
  Dark Mode Support
</div>

<!-- Version badge -->
<div style="position:absolute;bottom:5%;right:5%;
  background:#3b82f6;color:white;padding:6px 14px;
  border-radius:20px;font-size:14px;font-weight:700;">
  v2.0
</div>
```

## Playwright Export

Use the template from html-template.md. Render with Playwright:

```bash
npx playwright screenshot --viewport-size="1200,675" compose.html output-twitter.png
```

Node fallback when CLI isn't available:

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1200, height: 675 });
  await page.goto(`file://${__dirname}/compose.html`);
  await page.screenshot({ path: 'output-twitter.png' });
  await browser.close();
})();
```

Run multiple times with different viewport sizes per platform target.
