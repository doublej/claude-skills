---
name: umami-tracking
description: "Add Umami analytics tracking to any website project"
---

# Umami Tracking Injection

Add Umami analytics to any website. Automatically registers the site in the Umami dashboard and injects the tracking snippet with the real website ID.

<defaults>

- **Umami URL**: `https://umami-inky-two.vercel.app`
- **Dashboard**: `https://umami-inky-two.vercel.app/websites`

</defaults>

<workflow>

1. Detect the project type (framework or static HTML)
2. Determine the site name and domain from the project (package.json name, deploy config, or folder name)
3. Register the website via `register_website.py` to get a real website ID
4. Inject the tracking snippet with the actual website ID
5. Report which files were modified and link to the dashboard

Do NOT ask for credentials, URL, or website ID. Everything is preconfigured.

</workflow>

<steps>

## Step 1: Register the Website

```bash
python3 <skill_dir>/scripts/register_website.py "<site-name>" "<domain>"
```

- `site-name`: Human-readable name (e.g. "My Portfolio")
- `domain`: The deployment domain (e.g. "portfolio.example.com")
- Prints the website ID (UUID) to stdout

If the domain is unknown, use the project/folder name as both name and domain.

If the user provides a website ID directly, skip registration and proceed to Step 2 with that ID.

## Step 2: Inject Tracking

### Framework Projects (detect these first)

| Framework | Marker | File |
|-----------|--------|------|
| SvelteKit | `svelte.config.js` | `src/app.html` |
| Next.js | `next.config.*` | `src/app/layout.tsx` or `pages/_document.tsx` |
| Nuxt | `nuxt.config.*` | `nuxt.config.ts` (`app.head.script`) |
| Astro | `astro.config.*` | `src/layouts/Layout.astro` |

Add inside `<head>`:
```html
<script defer src="https://umami-inky-two.vercel.app/script.js" data-website-id="WEBSITE_ID"></script>
```

### Static HTML Projects

```bash
python3 <skill_dir>/scripts/inject_tracking.py <project_dir> <website_id> [--auto]
```

## Post-Injection

Notify the user: "Tracking added for **<site-name>**. View stats at https://umami-inky-two.vercel.app/websites"

The inject script is idempotent — files already containing the snippet are skipped.

</steps>
