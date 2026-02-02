# GitHub Pages Documentation Generator

Automates creation of beautiful, animated GitHub Pages documentation sites using SvelteKit.

## What This Skill Does

This skill generates complete documentation websites for GitHub repositories by:

1. **Analyzing** your project (README, package.json) to extract content
2. **Scaffolding** a SvelteKit static site with optimal configuration
3. **Designing** with proven aesthetic patterns (Instrument Sans typography, light theme, subtle animations)
4. **Generating** content sections (hero, features, installation, getting started)
5. **Animating** with fadeSlideUp entrance effects and staggered delays
6. **Deploying** via GitHub Actions to GitHub Pages
7. **Verifying** the build and providing post-generation recommendations

## Key Features

- **Fully Automated**: Extracts all content from your existing project files
- **Beautiful Design**: Follows proven patterns from successful open-source docs
- **Responsive**: Mobile-first design with tested breakpoints
- **Accessible**: Reduced-motion support, semantic HTML, keyboard navigation
- **Fast**: SvelteKit static generation for optimal performance
- **Consistent**: Uses exact design system (colors, typography, spacing)

## Design System

- **Fonts**: Instrument Sans (primary) + DM Mono (code)
- **Colors**: Light theme (#fafafa backgrounds, #1a1a1a text)
- **Animation**: fadeSlideUp (500ms ease-out, 200ms stagger)
- **Layout**: Max-width 1200px, 60px section padding
- **Responsive**: 375px (mobile), 768px (tablet), 1440px (desktop)

## Output Structure

```
docs/
├── src/
│   ├── app.html
│   ├── routes/
│   │   ├── +layout.svelte
│   │   ├── +layout.ts
│   │   └── +page.svelte
│   └── lib/
│       └── styles/
│           └── global.css
├── static/
│   ├── .nojekyll
│   ├── icon.svg
│   └── robots.txt
├── package.json
├── svelte.config.js
├── vite.config.ts
└── tsconfig.json

.github/
└── workflows/
    └── deploy-docs.yml
```

## Technologies

- SvelteKit 2.x with static adapter
- Bun for package management
- TypeScript strict mode
- Vite 7.x build tooling
- GitHub Actions deployment

## References

- `references/sveltekit-setup.md` - Complete SvelteKit configuration guide
- `references/design-patterns.md` - Full design system specification
- `references/content-strategy.md` - Content extraction patterns
- `references/animation-patterns.md` - Animation timing and accessibility

## Helper Scripts

- `scripts/init-docs.sh` - Quick scaffold script

## Related Skills

This skill integrates well with:
- `mobile-web` - Verify mobile optimization after generation
- `usability-fundamentals` - Evaluate against Nielsen's heuristics
- `frontend-design` - Review aesthetic patterns

## Success Criteria

Generated sites should:
- Build successfully with `bun run build`
- Match the proven design system exactly
- Include smooth animations with proper timing
- Deploy automatically via GitHub Actions
- Be responsive at all breakpoints
- Pass accessibility checks

## Example Output

See these projects for examples of the design patterns:
- consult-user-mcp documentation
- beads-kanban documentation

Both follow the exact same design system that this skill generates.
