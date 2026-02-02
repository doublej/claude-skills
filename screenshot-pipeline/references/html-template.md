# HTML Template

Base templates for screenshot compositing. Replace `{{PLACEHOLDERS}}` with actual values.

## Minimal Template

Bare essentials — screenshot + background + frame.

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: {{WIDTH}}px;
    height: {{HEIGHT}}px;
    display: flex;
    align-items: center;
    justify-content: center;
    {{BACKGROUND}}
    overflow: hidden;
    position: relative;
  }
  .device-frame {
    {{FRAME_STYLE}}
    {{SHADOW}}
    {{TRANSFORM}}
  }
  .device-frame img {
    display: block;
    max-height: {{MAX_IMG_HEIGHT}}px;
    width: auto;
  }
</style>
</head>
<body>
  <div class="device-frame">
    <img src="{{IMAGE_PATH}}" alt="">
  </div>
</body>
</html>
```

## Full-Featured Template

All composition options: headline, subtitle, frame, effects, watermark.

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: {{WIDTH}}px;
    height: {{HEIGHT}}px;
    display: flex;
    align-items: center;
    justify-content: center;
    {{BACKGROUND}}
    font-family: system-ui, -apple-system, sans-serif;
    overflow: hidden;
    position: relative;
  }
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 24px;
  }
  .headline {
    color: {{TEXT_COLOR}};
    font-size: 32px;
    font-weight: 700;
    text-align: center;
    max-width: 80%;
  }
  .subtitle {
    color: {{TEXT_COLOR_MUTED}};
    font-size: 18px;
    text-align: center;
  }
  .device-frame {
    {{FRAME_STYLE}}
    {{SHADOW}}
    {{TRANSFORM}}
  }
  .device-frame img {
    display: block;
    max-height: {{MAX_IMG_HEIGHT}}px;
    width: auto;
  }
  /* Watermark — remove block if not needed */
  .watermark {
    position: absolute;
    {{WATERMARK_POSITION}}
    font-size: 13px;
    font-weight: 600;
    color: {{WATERMARK_COLOR}};
    z-index: 20;
  }
</style>
</head>
<body>
  {{EFFECT_SVG}}

  <div class="container">
    <div class="headline">{{HEADLINE}}</div>
    <div class="subtitle">{{SUBTITLE}}</div>
    <div class="device-frame">
      <img src="{{IMAGE_PATH}}" alt="">
    </div>
  </div>

  {{EFFECT_OVERLAY}}
  <div class="watermark">{{WATERMARK_TEXT}}</div>
</body>
</html>
```

## Dual Screenshot Template

Two screenshots side-by-side in one image. Used for X.com middle images (see compose-guide.md).

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: {{WIDTH}}px;
    height: {{HEIGHT}}px;
    display: flex;
    align-items: center;
    justify-content: center;
    {{BACKGROUND}}
    font-family: system-ui, -apple-system, sans-serif;
    overflow: hidden;
    position: relative;
  }
  .dual-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 24px;
    padding: 0 5%;
  }
  .device-frame {
    {{FRAME_STYLE}}
    {{SHADOW}}
    flex: 0 1 48%;
  }
  .device-frame img {
    display: block;
    width: 100%;
    height: auto;
    max-height: {{MAX_IMG_HEIGHT}}px;
    object-fit: contain;
  }
</style>
</head>
<body>
  <div class="dual-container">
    <div class="device-frame">
      <img src="{{IMAGE_PATH_LEFT}}" alt="">
    </div>
    <div class="device-frame">
      <img src="{{IMAGE_PATH_RIGHT}}" alt="">
    </div>
  </div>
</body>
</html>
```

Additional placeholders for this template:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{IMAGE_PATH_LEFT}}` | Left screenshot path | `raw/screenshot-2.png` |
| `{{IMAGE_PATH_RIGHT}}` | Right screenshot path | `raw/screenshot-3.png` |

All other placeholders (`{{WIDTH}}`, `{{HEIGHT}}`, `{{BACKGROUND}}`, etc.) work the same as the standard templates.

## Placeholder Reference

| Placeholder | Source | Example |
|-------------|--------|---------|
| `{{WIDTH}}` / `{{HEIGHT}}` | platform-specs.md | `1200` / `675` |
| `{{BACKGROUND}}` | background-presets.md | `background: linear-gradient(...)` |
| `{{FRAME_STYLE}}` | frame-styles.md | CSS from any frame preset |
| `{{SHADOW}}` | shadow-presets.md | `box-shadow: ...` |
| `{{TRANSFORM}}` | effects-and-transforms.md | `transform: perspective(...)` |
| `{{MAX_IMG_HEIGHT}}` | 60-80% of `{{HEIGHT}}` | `500` |
| `{{IMAGE_PATH}}` | raw capture path | `raw/screenshot.png` |
| `{{TEXT_COLOR}}` | white or #1a1a1a | `white` |
| `{{TEXT_COLOR_MUTED}}` | 70% opacity variant | `rgba(255,255,255,0.7)` |
| `{{HEADLINE}}` | user-provided | `Your App Name` |
| `{{SUBTITLE}}` | user-provided | `A short tagline` |
| `{{WATERMARK_POSITION}}` | effects-and-transforms.md | `bottom: 16px; right: 16px` |
| `{{WATERMARK_COLOR}}` | match bg tone | `rgba(255,255,255,0.4)` |
| `{{WATERMARK_TEXT}}` | user-provided | `appname.com` |
| `{{EFFECT_SVG}}` | effects-and-transforms.md | noise SVG filter |
| `{{EFFECT_OVERLAY}}` | effects-and-transforms.md | `<div class="noise-overlay">` |

Omit any placeholder block (headline, subtitle, watermark, effects) that isn't needed — the template degrades gracefully.
