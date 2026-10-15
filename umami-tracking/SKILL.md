---
name: umami-tracking
description: "Add Umami analytics tracking to any website project, or to a native/non-browser app via /api/send"
---

# Umami Tracking Injection

Add Umami analytics to any website. Automatically registers the site in the Umami dashboard and injects the tracking snippet with the real website ID.

<presentation>
Print this banner once, first in the response. Close with the Step 3 report.

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   UMAMI TRACKING                                             ║
║   Register a site and inject Umami analytics                 ║
║   github.com/doublej                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```
</presentation>

<defaults>

- **Umami URL**: `https://umami-inky-two.vercel.app`
- **Dashboard**: `https://umami-inky-two.vercel.app/websites`

</defaults>

<workflow>

1. Detect the project type (framework or static HTML)
2. Determine the site name and domain from the project (package.json name, deploy config, or folder name)
3. Register the website via `register_website.py` to get a real website ID
4. Inject the tracking snippet with the actual website ID (native/non-browser apps: POST to `/api/send` instead)
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

### Native / non-browser clients (macOS/iOS app, CLI, server)

No snippet to inject — the app POSTs events itself, mirroring what `script.js` sends:

```
POST https://umami-inky-two.vercel.app/api/send
Content-Type: application/json
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36
x-umami-website-id: <website_id>
x-umami-hostname: <domain>

{"type":"event","payload":{"website":"<website_id>","hostname":"<domain>","url":"/screen-name",
 "title":"…","language":"en-US","screen":"1512x982","referrer":"","name":"<event>","data":{}}}
```

Omit `name` for a pageview. Umami runs `isbot` on the User-Agent: a non-browser UA (`curl/…`,
`MyApp/1.0 CFNetwork/…`, URLSession defaults) gets **200 `{"beep":"boop"}` and nothing is
recorded** — always send a browser-shaped UA. A real hit returns `{"cache":…,"sessionId":…}`;
`400 Website not found` = wrong id; `403` = the caller's IP is on the server's ignore list.

## Step 3: Report (required — do not skip, even when other work follows)

Report to the user with this block, one row per file touched, then the dashboard link on one line under it: "View stats at https://umami-inky-two.vercel.app/websites"

```
UMAMI TRACKING  ──  <site-name>   domain: <domain>   website id: <uuid>   framework: <name|static>

FILE                              SNIPPET
──────────────────────────────────────────────────────────────
<path>                            ✓ added | — already present

github.com/doublej
```

The inject script is idempotent — files already containing the snippet are skipped.

</steps>
