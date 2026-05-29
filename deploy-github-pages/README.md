# GitHub Pages Documentation Generator

Generates polished, animated, **multi-page** GitHub Pages documentation sites with SvelteKit, modeled on the reference site `https://doublej.github.io/flt/`, and deploys them via GitHub Actions.

## Reference output

The canonical "good" output is **flt** (`https://doublej.github.io/flt/`): a sticky blurred nav, a hero with a run/install/agent toggle, an animated `Terminal` demo carousel, a features grid, a command reference, and a CTA — across multiple pages. The skill exists to reproduce that quality, not the bare single-page template it grew out of.

## What This Skill Does

1. **Analyzes** the project (README, manifest, git remote) to extract content
2. **Scaffolds** the full SvelteKit site from `assets/scaffold/` via `scripts/init-docs.sh`
3. **Fills** the pages with real content built around `Terminal` demos
4. **Deploys** via a GitHub Actions workflow (`setup-bun@v2` → build → `configure-pages@v5` → deploy)
5. **Verifies** the production build and prerendered pages

## Design System (flt)

- **Fonts**: Instrument Sans (UI) + DM Mono (code/terminals)
- **Palette**: light page (`#f8f8f8`), **dark terminals** (`#1e1e1e`), blue accent (`#2266cc`)
- **Components**: `Nav.svelte` (sticky, blurred, base-aware) + `Terminal.svelte` (traffic-light, dark/green variants)
- **Animation**: `fadeSlideUp` (500ms ease-out), `prefers-reduced-motion` respected
- **Orphan control**: `orphan-obliterator` as a GitHub dependency

## Output Structure

```
docs/
├── package.json  svelte.config.js  vite.config.ts  tsconfig.json
├── src/
│   ├── app.html                       # <title>, <meta>, fonts, umami, project-linking widget
│   ├── lib/
│   │   ├── styles/global.css          # flt design system
│   │   └── components/
│   │       ├── Nav.svelte             # sticky blurred nav
│   │       └── Terminal.svelte        # animated terminal demos
│   └── routes/
│       ├── +layout.svelte             # imports global.css + <Nav/>
│       ├── +layout.ts                 # prerender = true
│       ├── +page.svelte               # home
│       └── features/+page.svelte      # features page
└── static/  .nojekyll  icon.svg  robots.txt

.github/workflows/deploy-docs.yml
```

## Bundled Resources

- `assets/scaffold/` — the actual files emitted (source of truth)
- `assets/deploy-docs.template.yml` — the GitHub Actions workflow
- `scripts/init-docs.sh` — scaffold + placeholder substitution
- `references/design-patterns.md` — full design system + component patterns
- `references/content-strategy.md` — content extraction patterns
- `references/animation-patterns.md` — animation timing and accessibility
- `references/sveltekit-setup.md` — SvelteKit / adapter-static configuration

## Related Skills

- `design-frontend` — review aesthetics after generation
- `ui-mobile` — verify mobile optimization
- `ui-usability` — evaluate against Nielsen's heuristics

## Success Criteria

Generated sites should:
- Build successfully with `NODE_ENV=production bun run build` (adapter-static, strict)
- Prerender every linked page (`build/index.html`, `build/features.html`, …)
- Match the flt design system (dark terminals on a light page, blue accent)
- Ship a real `<title>`/`<meta>`, a sticky nav, and at least one animated `Terminal` demo
- Deploy automatically via GitHub Actions to `https://<owner>.github.io/<repo>/`
