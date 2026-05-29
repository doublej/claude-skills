---
name: deploy-github-pages
description: "Generate an flt-style multi-page animated docs site (SvelteKit) and deploy it to GitHub Pages via Actions"
allowed-tools: [Bash, Read, Write, Glob, Grep, Edit]
---

# GitHub Pages Documentation Generator

Generates polished, animated, **multi-page** GitHub Pages documentation sites using the proven structure of the reference site `https://doublej.github.io/flt/`. The bundled scaffold ships the exact design system, a sticky `Nav`, and an animated `Terminal` demo component, then deploys via GitHub Actions.

<reference_site>
The canonical "good" output is **flt** (`https://doublej.github.io/flt/`): sticky blurred nav, a hero with a run/install/agent toggle, an animated `Terminal` demo carousel, a features grid, command reference, and a CTA — across multiple pages.

The anti-pattern is a bare single page (generic hero + features grid + footer, no nav, no `<title>`). Always produce flt-quality, not the bare template.
</reference_site>

<when_to_use>
Use this skill to:
- Create documentation / landing sites for GitHub repos (CLI tools, libraries, MCP servers, web apps)
- Generate marketing sites for open-source projects
- Set up automated GitHub Pages deployment

Single-page and multi-page are both supported. Default to **multi-page** (home + a features page) — it is what makes the site feel finished. Collapse to one page only for trivial projects (then delete the features page and its nav link).
</when_to_use>

<workflow_overview>
Low degree of freedom — follow the proven flt structure. The scaffold script lays down every config/component file; the skill's real work is **filling the pages with real content** built around `Terminal` demos.

```
ANALYZE → SCAFFOLD → CONTENT → DEPLOY → VERIFY
```
</workflow_overview>

<step_1_analyze>

Extract everything from the project automatically. Make intelligent defaults — don't ask questions.

```bash
cd <project-root>          # the repo root, not a subdirectory
cat README.md
cat package.json || cat pyproject.toml || cat Cargo.toml || cat go.mod
git remote get-url origin  # for REPO_SLUG / REPO_URL
```

Extract:
- **Title** — first H1, or package name. Compose a real `<title>` like `name — short value proposition`.
- **Description** — first paragraph / package description (one sentence). Used in `<meta description>` and the hero tagline.
- **Wordmark** — short name for the nav (usually the bare repo/command name).
- **Features** — the "Features" / "Why X" / "What it does" section; aim for 3 or 6 cards.
- **Install / run commands** — code blocks with install/run. Default to git installs (`bun install -g github:owner/repo`, `go install github.com/owner/repo@latest`, `pip install git+https://…`); only use registry installs if the package is confirmed published.
- **Usage / getting-started steps** — the real end-to-end story to dramatize in the `Terminal` demo.
- **Project type** — CLI / library / MCP server / web app (informs which commands and demos to show).

</step_1_analyze>

<step_2_scaffold>

Run the scaffold script from the **project root**. It copies the templates, substitutes placeholders, and installs the deploy workflow.

```bash
REPO_NAME=<repo> \
PROJECT_TITLE="<name — value prop>" \
PROJECT_DESCRIPTION="<one-sentence description>" \
WORDMARK=<short-name> \
~/.claude/skills/deploy-github-pages/scripts/init-docs.sh <project-root>

cd <project-root>/docs && bun install
```

`REPO_SLUG`/`REPO_URL` are derived from the git remote; override them with env vars if there is no `origin`. The base path is set to `/<REPO_NAME>` for production automatically.

This produces (see `assets/scaffold/` for the source of truth):
```
docs/
  package.json  svelte.config.js  vite.config.ts  tsconfig.json
  src/
    app.html                       # <title>, <meta>, fonts, umami, project-linking widget
    lib/styles/global.css          # flt design system (tokens, .tg terminal colors, .compare-table)
    lib/components/Nav.svelte       # sticky blurred nav, base-aware links, active state
    lib/components/Terminal.svelte  # traffic-light terminal (dark | green variants)
    routes/+layout.svelte           # imports global.css + renders <Nav/>
    routes/+layout.ts               # prerender = true
    routes/+page.svelte             # home (starter to fill in)
    routes/features/+page.svelte    # features page (starter to fill in)
  static/  .nojekyll  robots.txt  icon.svg
.github/workflows/deploy-docs.yml   # setup-bun@v2 → build → configure-pages@v5 → deploy
```

</step_2_scaffold>

<step_3_content>

This is the bulk of the work. Replace the starter placeholders with real content. **Keep the section order and the `Terminal`-based demo** — that is what makes the site look good rather than generic.

### 3.1 Home page (`docs/src/routes/+page.svelte`)
- **Hero**: real `<h1>` + tagline. Wire the run/install/agent toggle to real commands (drop modes that don't apply, e.g. no `agent` mode for a plain library).
- **Animated demo**: fill `steps[]` with a real end-to-end story (one frame per step) and render each frame's command + output inside `<Terminal>`. Use `.tg-prompt` for the `$`, `.tg` / `.tg-bright` / `.tg-dim` for green output, or the default dark variant for normal shells. This is the centerpiece.
- **Features grid**: 3 or 6 real cards with a short icon glyph, title, description.
- **CTA**: real install command.

### 3.2 Features page (`docs/src/routes/features/+page.svelte`)
- One block per major feature, each with its own `Terminal` demo.
- A comparison table vs. alternatives reads well — use `class="compare-table"`.

### 3.3 Nav (`docs/src/lib/components/Nav.svelte`)
- Edit the `links` array to match the pages you actually create. Keep the GitHub link last and external.
- Add more routes (e.g. a `prime`/usage page) by creating `docs/src/routes/<name>/+page.svelte` and a matching nav link.

### 3.4 Content rules
- Use the `Terminal` component for **every** command demo — never inline `<pre>` for CLI output.
- `obliterate` is already wired in the home page's `onMount`; add any new long-paragraph selectors to its `selectors` list.
- Respect the design tokens in `global.css`; don't introduce new colors/fonts.

</step_3_content>

<step_4_deploy>

The workflow is already installed at `.github/workflows/deploy-docs.yml`. Commit and push, then enable Pages.

```bash
git add docs .github/workflows/deploy-docs.yml
git commit -m "docs: add GitHub Pages site"
git push
```

Then tell the user to enable Pages **once**:
- Settings → Pages → Source: **GitHub Actions** → Save
- The next push to `main` touching `docs/**` deploys (or run the workflow manually via `workflow_dispatch`).

Site goes live at `https://<owner>.github.io/<REPO_NAME>/`.

</step_4_deploy>

<step_5_verify>

```bash
cd docs
NODE_ENV=production bun run build   # must succeed (adapter-static, strict)
bun run preview                     # spot-check locally
```

Verify the build output (`docs/build/index.html`):
- [ ] `<title>` and `<meta name="description">` are present and real
- [ ] `_app/` assets resolve (relative `./_app/...` — correct under the base path)
- [ ] Every linked page prerendered (e.g. `build/features.html` exists)
- [ ] Nav renders; the project-linking widget + umami script tags are present

Quality checklist:
- [ ] Sticky nav with working active states
- [ ] At least one animated `Terminal` demo with real commands
- [ ] Responsive at 375 / 768 / 1440px (grid collapses, demo header stacks)
- [ ] `prefers-reduced-motion` respected (already in `global.css`)
- [ ] Semantic structure (`main`, `section`, `nav`, headings in order)

Then consider these follow-up skills: `frontend-design` (aesthetics), `mobile-web` (mobile), `usability-fundamentals` (heuristics).

</step_5_verify>

## Post-deploy reminders

- Replace `YOUR_WEBSITE_ID` in `docs/src/app.html` with the real Umami id from `https://umami-inky-two.vercel.app`.
- The project-linking widget (`doublej.github.io/doublej-project-linking/widget.js`) is included by default — leave it unless the user opts out.

## Troubleshooting

**Build fails** — check Bun/Node present; `bun install` ran; no Svelte syntax errors. `strict: true` fails the build if a linked page can't prerender, so ensure every nav link points at a real route.

**Pages 404 / unstyled** — base path in `svelte.config.js` must equal the repo name; Pages Source must be **GitHub Actions**; check the Actions run succeeded.

**orphan-obliterator install fails** — it's a GitHub dependency (`github:doublej/orphan-obliterator`); the repo must be reachable at build time. CI uses the default `GITHUB_TOKEN`, which can read public repos.

## References

- `references/design-patterns.md` — full design system + component patterns
- `references/content-strategy.md` — content extraction patterns
- `references/animation-patterns.md` — animation timing and accessibility
- `references/sveltekit-setup.md` — SvelteKit/adapter-static configuration details
- `assets/scaffold/` — the actual files emitted (source of truth)
