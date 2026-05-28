# Fonts

The system uses **Geist Variable** (sans) and **Geist Mono** (numerals, code).

## Sourcing

In production, install via:

```bash
bun add @fontsource-variable/geist @fontsource-variable/geist-mono
```

And import in your app entry:

```ts
import "@fontsource-variable/geist";
import "@fontsource-variable/geist-mono";
```

## In this project

For HTML previews and UI kit pages, fonts load via **Google Fonts CDN**:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

This is the **Google Fonts** flavor of Geist (Vercel publishes both there and on Fontsource). If you need fully offline self-hosted variable WOFF2s, drop them into this folder as:

- `geist-variable.woff2`
- `geist-mono-variable.woff2`

…and the `@font-face` rule in `colors_and_type.css` will fall back to local files automatically (it lists `local("Geist Variable")` first).

## Font feature settings

We enable `tabular-nums` globally and `ss01` + `cv11` stylistic alternates for tighter numerals. The `.num` helper additionally applies the mono family.

## Caveats

- No font files were attached. If your team self-hosts Geist with a specific subset or weight range, please drop the WOFF2s into this folder so the preview matches your shipped product.
