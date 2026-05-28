# Mobile Performance Checklist

## Critical Rendering Path

- [ ] Inline critical CSS (< 14KB) in `<head>`
- [ ] Defer non-critical CSS with `media="print" onload="this.media='all'"`
- [ ] All JS uses `defer` or `async` (no render-blocking scripts)
- [ ] Preconnect to critical third-party origins
- [ ] Preload LCP image or hero font

```html
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preload" href="/hero.webp" as="image" fetchpriority="high">
```

## Images

- [ ] Serve AVIF with WebP and JPEG fallbacks (`<picture>`)
- [ ] Set explicit `width` and `height` on all `<img>` tags
- [ ] Use `loading="lazy"` on below-fold images
- [ ] Use `fetchpriority="high"` on LCP image
- [ ] Use `decoding="async"` on non-critical images
- [ ] Responsive images via `srcset` + `sizes`
- [ ] Mobile images under 200KB

## Fonts

- [ ] Self-host fonts (avoid third-party round-trips)
- [ ] WOFF2 format only
- [ ] `font-display: swap` (mobile) or `optional` (desktop)
- [ ] Subset to needed character ranges
- [ ] Preload only above-fold fonts, desktop only
- [ ] Match fallback font metrics (`size-adjust`, `ascent-override`)

## JavaScript

- [ ] Tree-shake unused code
- [ ] Code-split by route
- [ ] Total JS budget: < 200KB compressed
- [ ] No long tasks > 50ms on main thread
- [ ] Use `requestIdleCallback` for non-urgent work
- [ ] Web Workers for heavy computation

## Caching & Compression

- [ ] Brotli compression (fallback to gzip)
- [ ] `Cache-Control: public, max-age=31536000, immutable` for hashed assets
- [ ] `Cache-Control: no-cache` for HTML (always revalidate)
- [ ] Service worker for offline/cache-first patterns

## Layout Stability

- [ ] Set `width`/`height` or `aspect-ratio` on media elements
- [ ] Reserve space for ads, embeds, dynamic content
- [ ] Avoid inserting content above existing content
- [ ] Use CSS `contain` for complex components
- [ ] Font fallback metrics matched to custom font

## Network

- [ ] HTTP/2 or HTTP/3
- [ ] DNS prefetch for third-party domains
- [ ] Minimize third-party scripts
- [ ] Resource hints: `preconnect`, `dns-prefetch`, `preload`, `prefetch`

## Core Web Vitals Targets

| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| LCP | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| INP | ≤ 200ms | ≤ 500ms | > 500ms |
| CLS | ≤ 0.1 | ≤ 0.25 | > 0.25 |

## Testing Tools

- Lighthouse (Chrome DevTools → Audits)
- PageSpeed Insights (lab + field data)
- WebPageTest (real devices, multiple locations)
- Chrome DevTools Performance tab (main thread analysis)
