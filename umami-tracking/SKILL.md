---
name: umami-tracking
description: Add Umami analytics tracking to any website project. Use when user wants to add tracking, analytics, or Umami to a site.
---

# Umami Tracking Injection

Add Umami analytics to any website. No questions asked — uses the default instance URL and a placeholder website ID that can be filled in later.

## Defaults

- **Umami URL**: `https://umami-inky-two.vercel.app`
- **Website ID**: `YOUR_WEBSITE_ID` (placeholder — user fills in from Umami dashboard later)

## Workflow

1. Detect the project type (framework or static HTML)
2. Inject the tracking snippet immediately using defaults
3. Report which files were modified and remind user to replace `YOUR_WEBSITE_ID`

Do NOT ask for the Umami URL or website ID. Just inject with defaults.

## Injection

### Framework Projects (preferred — detect these first)

Check for framework markers and add the snippet directly to the app shell:

| Framework | Marker | File |
|-----------|--------|------|
| SvelteKit | `svelte.config.js` | `src/app.html` |
| Next.js | `next.config.*` | `src/app/layout.tsx` or `pages/_document.tsx` |
| Nuxt | `nuxt.config.*` | `nuxt.config.ts` (`app.head.script`) |
| Astro | `astro.config.*` | `src/layouts/Layout.astro` |

Add inside `<head>`:
```html
<script defer src="https://umami-inky-two.vercel.app/script.js" data-website-id="YOUR_WEBSITE_ID"></script>
```

### Static HTML Projects

Run the bundled script:

```bash
python3 <skill_dir>/scripts/inject_tracking.py <project_dir> YOUR_WEBSITE_ID [--auto]
```

- Tries placeholder replacement (`<!-- TRACKING_PLACEHOLDER -->`) first
- Falls back to auto-inject before `</head>` if no placeholders found

## Post-Injection

Notify the user: "Tracking added. Replace `YOUR_WEBSITE_ID` with your actual ID from the Umami dashboard."

The script is idempotent — files already containing the snippet are skipped.
