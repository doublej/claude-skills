---
name: mobile-web
description: Mobile website optimization best practices. Use when building or auditing HTML pages for mobile — covers viewport, meta tags, safe areas, touch targets, dark mode, forms, fonts, images, PWA, and performance.
---

# Mobile Web Optimization

Apply these practices when generating HTML/CSS for mobile websites. Degree of freedom: **medium** — follow the patterns below but adapt to project context.

## HTML Head Essentials

```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#1a1a1a" media="(prefers-color-scheme: dark)">
<meta name="description" content="...">
<meta name="format-detection" content="telephone=no">
```

### When to disable zoom

Only add `maximum-scale=1, user-scalable=no` for **app-like experiences** (kiosk, PWA). Never on content sites — it harms accessibility (WCAG 1.4.4).

### Apple-specific (when targeting iOS home screen)

```html
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="AppName">
```

## Favicons (minimal set, 2025)

```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png"><!-- 180x180 -->
```

SVG favicons can respond to dark mode via embedded `<style>` with `prefers-color-scheme`.

## Safe Area Insets

When using `viewport-fit=cover`, content can render behind notches and home indicators. Protect it:

```css
body {
  padding: env(safe-area-inset-top) env(safe-area-inset-right)
           env(safe-area-inset-bottom) env(safe-area-inset-left);
}

/* Fixed bottom bars */
.bottom-bar {
  padding-bottom: max(1rem, env(safe-area-inset-bottom));
}

/* Fixed top bars */
.top-bar {
  padding-top: max(1rem, env(safe-area-inset-top));
}
```

## Dark Mode

```css
:root {
  color-scheme: light dark;
  --bg: #fff;
  --text: #111;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1a1a1a;
    --text: #eee;
  }
}
```

Both the `<meta name="color-scheme">` tag AND the CSS `color-scheme` property are needed — the meta tag prevents flash on load, the CSS property styles form controls.

## Touch & Interaction

| Rule | Value |
|------|-------|
| Minimum touch target | 44x44 CSS px (WCAG 2.5.5 AAA) |
| Absolute minimum | 24x24 CSS px (WCAG 2.5.8 AA) |
| Spacing between targets | >=8px gap |
| Min body font size | 16px (prevents iOS auto-zoom on inputs) |

```css
/* Remove tap highlight on mobile */
* { -webkit-tap-highlight-color: transparent; }

/* Prevent pull-to-refresh and overscroll bounce */
html { overscroll-behavior: none; }

/* Smooth anchor scrolling */
html { scroll-behavior: smooth; }

/* Respect motion preferences */
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Forms

Always set `type`, `inputmode`, `autocomplete`, and `enterkeyhint` together:

| Field | type | inputmode | autocomplete | enterkeyhint |
|-------|------|-----------|-------------|-------------|
| Email | `email` | `email` | `email` | `next` |
| Phone | `tel` | `tel` | `tel` | `next` |
| PIN / OTP | `text` | `numeric` | `one-time-code` | `done` |
| Search | `search` | `search` | `off` | `search` |
| URL | `url` | `url` | `url` | `go` |
| Currency | `text` | `decimal` | `off` | `done` |
| Name | `text` | `text` | `name` | `next` |
| Password (login) | `password` | — | `current-password` | `done` |
| Password (signup) | `password` | — | `new-password` | `done` |

Disable autocapitalize for usernames/codes: `autocapitalize="off"`.

## Fonts

```html
<!-- Self-hosted (preferred) -->
<link rel="preload" href="/fonts/main.woff2" as="font"
      type="font/woff2" crossorigin media="(min-width: 768px)">
```

```css
@font-face {
  font-family: 'Main';
  src: url('/fonts/main.woff2') format('woff2');
  font-display: swap; /* mobile: show text immediately */
  unicode-range: U+0000-00FF; /* subset to latin if possible */
}
```

Key rules:
- WOFF2 only (97%+ support, 30% smaller than WOFF)
- `font-display: swap` on mobile, `optional` on desktop
- Preload only above-the-fold fonts, only on desktop (`min-width: 768px`)
- Reduce layout shift: use `size-adjust`, `ascent-override`, `descent-override` on fallback

## Responsive Images

```html
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg"
       srcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1200.jpg 1200w"
       sizes="(max-width: 768px) 100vw, 50vw"
       loading="lazy"
       decoding="async"
       width="1200" height="800"
       alt="Description">
</picture>
```

Key rules:
- Always set `width` and `height` attributes (prevents layout shift)
- `loading="lazy"` on everything except the LCP image
- LCP image: add `fetchpriority="high"`, no lazy loading
- AVIF > WebP > JPEG fallback chain
- Mobile images < 200KB, hero images < 300KB
- 3-5 srcset widths: 400, 800, 1200, 1600, 2560

## PWA Manifest

Only include if building a PWA or home-screen-installable site.

```html
<link rel="manifest" href="/manifest.webmanifest">
```

See `references/pwa-manifest.md` for full manifest template.

## CSS Units & Layout

- Use `rem` for font sizes, `em` for component spacing
- Use `dvh` (dynamic viewport height) instead of `vh` — accounts for mobile browser chrome
- Use `svh` for minimum guaranteed viewport, `lvh` for maximum
- Avoid fixed heights; prefer `min-height: 100dvh`
- Mobile layout width: design for 360-430px range

## Performance Checklist

For the full checklist, see `references/performance-checklist.md`.

Quick wins:
- Inline critical CSS (<14KB)
- `<link rel="preconnect">` for external origins
- `defer` all non-critical JS
- Set `Cache-Control` headers
- Compress with Brotli > gzip
