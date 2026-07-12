---
name: doublej-widget
description: "Set up, deploy, and embed the DoubleJ project-linking widget. Use when adding a new project to the widget system, deploying widget changes, embedding the widget on a site, or managing widget profiles and matching rules."
---

# DoubleJ Project-Linking Widget

Embeddable corner widget with path-based profile matching. Lives at:
`~/Documents/development/web/doublej-project-linking`

<tech_stack>

SvelteKit 5 + Svelte 5, Bun, Vite. Deployed to GitHub Pages via GitHub Actions.
Widget compiles to a single IIFE `widget.js` with injected CSS (shadow DOM).

</tech_stack>

<quick_reference>

### CLI (`widget-link`)

```bash
# Must run from project root, or use `bun link` for global access
widget-link list                          # List profiles + rules
widget-link add <slug> --repo <url>       # Create profile + rule
widget-link remove <slug>                 # Delete profile + rules
widget-link deploy                        # Build, commit, push
```

### Add Options

| Flag | Default |
|------|---------|
| `--repo <url>` | required |
| `--domain <domain>` | `doublej.github.io` |
| `--name <name>` | Derived from slug |
| `--color <hex>` | `#e63946` |
| `--no-star` | Star enabled |
| `--no-other` | "Other projects" link included |

### Build Commands

```bash
bun run build:widget     # → dist/widget.js (IIFE bundle)
bun run build:manifest   # → dist/widget-manifest.json (static fallback)
bun run build:static     # Both of the above
bun run dev              # Dev server on :5173 (management UI)
```

</quick_reference>

<workflows>

### 1. Initial Setup (first time only)

```bash
cd ~/Documents/development/web/doublej-project-linking
bun install
bun link  # Makes `widget-link` available globally
```

Optional — Short.io URL shortening:
```bash
cp .env.example .env
# Edit .env: set SHORTIO_API_KEY and SHORTIO_DOMAIN
```

### 2. Add a New Project

Use the CLI to create a profile + matching rule:

```bash
widget-link add my-project --repo https://github.com/doublej/my-project
```

This creates:
- `profiles/profiles/my-project.json` — widget config (CTA, color, links)
- `profiles/rules/my-project-rule.json` — matching rule (`doublej.github.io/my-project/**`)

For custom settings:
```bash
widget-link add my-project \
  --repo https://github.com/doublej/my-project \
  --name "My Cool Project" \
  --color "#3b82f6" \
  --no-star
```

### 3. Deploy Changes

```bash
widget-link deploy
```

This runs: `build:static` → `git add profiles/ dist/` → commit → push.
GitHub Actions then builds the docs site + widget and deploys to Pages.

The deploy workflow triggers on pushes to `main` that touch: `profiles/`, `src/lib/widget/`, `src/lib/shared/`, `docs/`, `scripts/`, or the workflow file.

### 4. Embed the Widget

Single script tag, no configuration needed:

```html
<script src="https://doublej.github.io/doublej-project-linking/widget.js"></script>
```

The widget auto-detects the page URL and loads the matching profile. Hides itself if no match.

Legacy attribute-based embedding (still supported):

```html
<script src="https://doublej.github.io/doublej-project-linking/widget.js"
  data-links='[{"label":"My Project","url":"https://...","icon":"github"}]'
  data-cta="Projects"
  data-color="#e63946">
</script>
```

### 5. Manual Profile Editing

Profiles live in `profiles/profiles/<slug>.json`:

```json
{
  "id": "my-project",
  "name": "My Project",
  "config": {
    "cta": "Projects",
    "color": "#e63946",
    "showStar": true,
    "links": [
      { "label": "View project on GitHub", "url": "https://github.com/doublej/my-project", "icon": "github" },
      { "label": "See my other projects", "url": "https://l.jurrejan.com/doublej-gh", "icon": "link" }
    ]
  },
  "createdAt": "2025-01-01T00:00:00.000Z",
  "updatedAt": "2025-01-01T00:00:00.000Z"
}
```

Rules live in `profiles/rules/<slug>-rule.json`:

```json
{
  "id": "my-project-rule",
  "profileId": "my-project",
  "domain": "doublej.github.io",
  "pathPattern": "/my-project/**",
  "priority": 101,
  "enabled": true
}
```

### Path Pattern Specificity

```
/blog/featured  → priority 1200 (exact)
/blog/*         → priority 110  (single-level wildcard)
/blog/**        → priority 101  (multi-level wildcard)
/**             → priority 1    (catch-all)
```

<architecture>

```
src/
├── cli.ts                      # CLI tool (widget-link)
├── lib/
│   ├── server/profiles/        # Storage, types, matching
│   ├── shared/matcher.ts       # Path matching (shared with widget)
│   └── widget/                 # Widget components (Svelte, shadow DOM)
├── routes/
│   ├── +page.svelte            # Management UI
│   └── api/                    # CRUD endpoints + widget-config
└── hooks.server.ts             # CORS headers

profiles/
├── profiles/*.json             # Widget configurations
└── rules/*.json                # Matching rules
```

Widget fetches config flow: script tag → detect URL → `/api/widget-config?domain=X&pathname=Y` → fallback to static `widget-manifest.json` → mount in shadow DOM or hide.

</architecture>

Run `bun run dev` and open http://localhost:5173 to:
- Create/edit profiles visually
- Configure matching rules
- Test URL matching
- Copy embed code

</workflows>
