---
name: github-pages-generator
description: Generate beautiful, animated GitHub Pages docs using SvelteKit. Analyzes project structure, creates responsive sites with proven design patterns (Instrument Sans, fadeSlideUp animations, feature showcases), sets up automated GitHub Actions deployment.
allowed-tools: [Bash, Read, Write, Glob, Grep, Edit]
---

# GitHub Pages Documentation Generator

Automates creation of beautiful, animated GitHub Pages documentation sites using proven patterns from successful open-source projects.

## When to Use This Skill

Use this skill when you need to:
- Create documentation sites for GitHub repositories
- Build landing pages for open-source projects
- Generate marketing sites for libraries, CLI tools, or web apps
- Set up automated documentation deployment with GitHub Actions

**Don't use** for:
- Complex documentation with multiple pages (this creates single-page sites)
- Projects requiring dark mode toggle (uses light theme only)
- Sites needing custom domains or complex routing

## Workflow Overview

This is a **low degree of freedom** skill - follow the exact proven structure and design patterns. The workflow is fully automated with minimal user intervention.

```
ANALYZE → SCAFFOLD → DESIGN → CONTENT → ANIMATE → DEPLOY → VERIFY
```

## Step 1: ANALYZE - Extract Project Information

Automatically extract all information from the project. Make intelligent defaults - don't ask questions.

### 1.1 Read Project Files

```bash
# Navigate to project root (if in a subdirectory)
cd ../..

# Read key files
cat README.md
cat package.json || cat pyproject.toml || cat Cargo.toml
```

### 1.2 Extract Information

From README.md:
- Project title (first H1 or from package.json name)
- Description (first paragraph after title)
- Features (look for "Features" section, bullet lists)
- Installation command (look for code blocks with install commands)
- Getting started steps (look for "Getting Started" or "Usage")

From package.json/pyproject.toml:
- Package name
- Version
- Repository URL
- Dependencies (for tech stack showcase)

### 1.3 Determine Project Type

Automatically classify:
- **CLI Tool**: Has bin field in package.json or CLI-related dependencies
- **Library**: Has main/exports field, no bin
- **MCP Server**: Contains "mcp" in name or dependencies
- **Web App**: Has frontend framework dependencies

### 1.4 Make Intelligent Defaults

If information is missing:
- No features in README? Extract from description or create generic ones
- No installation command? Generate standard one (npm install, pip install, etc.)
- No repository URL? Use GitHub API to find it from package name
- No description? Use package.json description

## Step 2: SCAFFOLD - Create Documentation Structure

### 2.1 Create Directory Structure

```bash
mkdir -p docs/{src/{routes,lib/{components,styles,assets}},static,.github/workflows}
```

### 2.2 Initialize SvelteKit Project

Create `docs/package.json`:

```json
{
  "name": "{{PROJECT_NAME}}-docs",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite dev",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "@sveltejs/adapter-static": "^3.0.7",
    "@sveltejs/kit": "^2.11.1",
    "@sveltejs/vite-plugin-svelte": "^5.0.4",
    "svelte": "^5.17.0",
    "typescript": "^5.7.3",
    "vite": "^7.0.5"
  }
}
```

### 2.3 Configure SvelteKit for Static Export

Create `docs/svelte.config.js`:

```javascript
import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  kit: {
    adapter: adapter({
      pages: 'build',
      assets: 'build',
      fallback: null,
      precompress: false,
      strict: true
    }),
    paths: {
      base: process.env.NODE_ENV === 'production' ? '/{{REPO_NAME}}' : ''
    }
  }
};

export default config;
```

### 2.4 Configure Vite

Create `docs/vite.config.ts`:

```typescript
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()]
});
```

### 2.5 Configure TypeScript

Create `docs/tsconfig.json`:

```json
{
  "extends": "./.svelte-kit/tsconfig.json",
  "compilerOptions": {
    "allowJs": true,
    "checkJs": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "skipLibCheck": true,
    "sourceMap": true,
    "strict": true,
    "moduleResolution": "bundler"
  }
}
```

### 2.6 Install Dependencies

```bash
cd docs
bun install
```

## Step 3: DESIGN - Apply Aesthetic Patterns

### 3.1 Design System Specification

**Typography:**
- Primary: Instrument Sans (400, 500, 600)
- Monospace: DM Mono
- Load via Google Fonts CDN

**Colors (Light Theme):**
```css
--bg-primary: #fafafa;
--bg-secondary: #fff;
--bg-code: #f0f0f0;
--text-primary: #1a1a1a;
--text-secondary: #404040;
--text-tertiary: #606060;
--border: #e0e0e0;
--accent: #1a1a1a;
```

**Spacing:**
```css
--section-padding: 60px;
--container-max-width: 1200px;
--container-padding: 24px;
--grid-gap: 24px;
```

**Responsive Breakpoints:**
- Desktop: 1000px+
- Tablet: 700px - 999px
- Mobile: < 700px

### 3.2 Create HTML Template

Create `docs/src/app.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="icon" href="%sveltekit.assets%/icon.svg" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  %sveltekit.head%
</head>
<body>
  <div style="display: contents">%sveltekit.body%</div>
</body>
</html>
```

### 3.3 Create Root Layout

Create `docs/src/routes/+layout.svelte`:

```svelte
<script lang="ts">
  import '../lib/styles/global.css';
  let { children } = $props();
</script>

{@render children()}
```

Create `docs/src/routes/+layout.ts`:

```typescript
export const prerender = true;
```

### 3.4 Create Global Styles

Create `docs/src/lib/styles/global.css`:

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --bg-primary: #fafafa;
  --bg-secondary: #fff;
  --bg-code: #f0f0f0;
  --text-primary: #1a1a1a;
  --text-secondary: #404040;
  --text-tertiary: #606060;
  --border: #e0e0e0;
  --accent: #1a1a1a;
  --section-padding: 60px;
  --container-max-width: 1200px;
  --container-padding: 24px;
  --grid-gap: 24px;
}

body {
  font-family: 'Instrument Sans', system-ui, -apple-system, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.6;
  font-size: 1.1rem;
}

code, pre {
  font-family: 'DM Mono', monospace;
}

@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

## Step 4: CONTENT - Generate Documentation Sections

Create `docs/src/routes/+page.svelte` with these sections:

### 4.1 Hero Section

```svelte
<section class="hero">
  <div class="container">
    <h1>{{PROJECT_TITLE}}</h1>
    <p class="description">{{PROJECT_DESCRIPTION}}</p>
  </div>
</section>

<style>
  .hero {
    padding: var(--section-padding) var(--container-padding);
    text-align: center;
    animation: fadeSlideUp 0.5s ease-out forwards;
  }

  h1 {
    font-size: 2.5rem;
    font-weight: 600;
    letter-spacing: -0.03em;
    margin-bottom: 1rem;
  }

  .description {
    font-size: 1.1rem;
    color: var(--text-secondary);
    max-width: 700px;
    margin: 0 auto;
  }
</style>
```

### 4.2 Install Section

```svelte
<section class="install">
  <div class="container">
    <div class="install-box">
      <code>{{INSTALL_COMMAND}}</code>
      <button onclick={copyInstall}>Copy</button>
    </div>
  </div>
</section>

<script>
  function copyInstall() {
    navigator.clipboard.writeText('{{INSTALL_COMMAND}}');
  }
</script>
```

### 4.3 Features Grid

```svelte
<section class="features">
  <div class="container">
    <h2>Features</h2>
    <div class="grid">
      {#each features as feature, i}
        <div class="feature-card" style="animation-delay: {i * 200}ms">
          <h3>{feature.title}</h3>
          <p>{feature.description}</p>
        </div>
      {/each}
    </div>
  </div>
</section>

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--grid-gap);
  }

  .feature-card {
    background: var(--bg-secondary);
    padding: 24px;
    border: 1px solid var(--border);
    border-radius: 8px;
    animation: fadeSlideUp 0.5s ease-out forwards;
    opacity: 0;
  }

  @media (max-width: 1000px) {
    .grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 700px) {
    .grid {
      grid-template-columns: 1fr;
    }
  }
</style>
```

### 4.4 Getting Started Section

```svelte
<section class="getting-started">
  <div class="container">
    <h2>Getting Started</h2>
    <div class="steps">
      {#each steps as step, i}
        <div class="step" style="animation-delay: {(i + 3) * 200}ms">
          <div class="step-number">{i + 1}</div>
          <div class="step-content">
            <h3>{step.title}</h3>
            <p>{step.description}</p>
            {#if step.code}
              <pre><code>{step.code}</code></pre>
            {/if}
          </div>
        </div>
      {/each}
    </div>
  </div>
</section>
```

### 4.5 Footer

```svelte
<footer>
  <div class="container">
    <p>
      <a href="{{REPO_URL}}" target="_blank">GitHub</a>
      {#if LICENSE} • {{LICENSE}}{/if}
    </p>
  </div>
</footer>
```

## Step 5: ANIMATE - Add Entrance Animations

### 5.1 Animation Timing Guidelines

Follow animation-easing best practices:
- Duration: 400-500ms for most elements
- Easing: ease-out for entrance animations
- Stagger: 200ms intervals for sequential elements
- Distance: 20px translateY for subtle lift

### 5.2 Apply Staggered Delays

For grids and lists:
```svelte
{#each items as item, i}
  <div style="animation-delay: {i * 200}ms">
```

For sections:
- Hero: 0ms
- Install: 200ms
- Features: 400ms (then stagger cards)
- Getting Started: 600ms
- Footer: 1000ms

### 5.3 Accessibility

Respect prefers-reduced-motion (already in global.css):
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

## Step 6: DEPLOY - Configure GitHub Actions

### 6.1 Create Deployment Workflow

Create `docs/.github/workflows/deploy-docs.yml`:

```yaml
name: Deploy Documentation

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Bun
        uses: oven-sh/setup-bun@v1
        with:
          bun-version: latest

      - name: Install dependencies
        run: cd docs && bun install

      - name: Build
        run: cd docs && bun run build
        env:
          NODE_ENV: production

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs/build

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 6.2 Create Static Files

Create `docs/static/.nojekyll` (empty file):
```bash
touch docs/static/.nojekyll
```

Create `docs/static/robots.txt`:
```
User-agent: *
Allow: /
```

Create `docs/static/icon.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" fill="#1a1a1a"/>
  <text x="50" y="70" font-family="system-ui" font-size="60" font-weight="bold" fill="white" text-anchor="middle">{{FIRST_LETTER}}</text>
</svg>
```

### 6.3 Add Workflow to Project Root

Copy workflow to project root:
```bash
mkdir -p ../.github/workflows
cp docs/.github/workflows/deploy-docs.yml ../.github/workflows/
```

## Step 7: VERIFY - Build, Test, and Validate

### 7.1 Build the Site

```bash
cd docs
bun run build
```

Check for errors. If build fails, debug and fix issues.

### 7.2 Preview Locally

```bash
bun run preview
```

### 7.3 Validation Checklist

Use this checklist from usability-fundamentals:

- [ ] Clear information hierarchy (h1 > h2 > h3 > p)
- [ ] Touch targets ≥44px on mobile (buttons, links)
- [ ] Readable font sizes (≥16px body text)
- [ ] Sufficient color contrast (WCAG AA minimum)
- [ ] Keyboard navigation works (tab through all interactive elements)
- [ ] Reduced-motion support (prefers-reduced-motion media query)
- [ ] Semantic HTML structure (header, main, section, footer)
- [ ] Responsive at 375px, 768px, 1440px viewports

### 7.4 Manual Testing Steps

1. Open in browser
2. Test responsive design:
   - Mobile: 375px width
   - Tablet: 768px width
   - Desktop: 1440px width
3. Test animations (should fade and slide up)
4. Test copy button for install command
5. Test all links (GitHub, etc.)
6. Test keyboard navigation (Tab key)
7. Test with prefers-reduced-motion enabled

### 7.5 Post-Generation Recommendations

After generating the site, suggest these follow-up skills:

**For mobile optimization:**
```
Run the mobile-web skill to verify mobile-specific optimizations like viewport settings, touch targets, safe areas, and performance.
```

**For usability evaluation:**
```
Run the usability-fundamentals skill to evaluate against Nielsen's heuristics and Laws of UX.
```

**For aesthetic review:**
```
Run the frontend-design skill to review aesthetic patterns and identify anti-patterns.
```

### 7.6 Setup Instructions for User

Print these instructions:

```
Documentation site created successfully!

Next steps:
1. Commit and push the docs/ folder
2. Enable GitHub Pages:
   - Go to Settings > Pages
   - Source: GitHub Actions
   - Save
3. Push to trigger deployment
4. Site will be live at: https://{{USERNAME}}.github.io/{{REPO_NAME}}/

Local development:
  cd docs
  bun run dev      # Start dev server
  bun run build    # Build for production
  bun run preview  # Preview production build

Optional: Run these skills for validation:
  - mobile-web (verify mobile optimization)
  - usability-fundamentals (evaluate usability)
  - frontend-design (review aesthetics)
```

## Content Extraction Patterns

### From README.md

**Extract project title:**
```regex
# (.+)
```
First H1 heading

**Extract description:**
First paragraph after title, usually 1-3 sentences

**Extract features:**
Look for sections titled:
- "Features"
- "Why [Project Name]"
- "What it does"

Parse bullet points:
```markdown
- **Feature name**: Description
- Feature name - Description
* Feature name: Description
```

**Extract installation:**
Look for code blocks containing:
- `npm install`
- `pip install`
- `cargo install`
- `bun add`

**Extract getting started:**
Look for sections titled:
- "Getting Started"
- "Quick Start"
- "Usage"
- "How to use"

### From package.json

```json
{
  "name": "package-name",
  "description": "Project description",
  "repository": {
    "url": "https://github.com/user/repo"
  },
  "bin": { /* CLI tool */ },
  "main": "index.js", /* Library */
  "dependencies": { /* Tech stack */ }
}
```

### Intelligent Defaults

If README is minimal:
1. Use package.json description
2. Generate generic features based on project type
3. Create standard installation command
4. Generate basic getting started steps

## References

For detailed information, see:
- `references/sveltekit-setup.md` - Complete SvelteKit configuration
- `references/design-patterns.md` - Full design system specification
- `references/content-strategy.md` - Content extraction patterns
- `references/animation-patterns.md` - Animation timing and accessibility

## Success Criteria

The skill should produce:
- Working SvelteKit site that builds successfully
- Visually consistent output matching design system
- Smooth fadeSlideUp animations with proper timing
- Automated GitHub Pages deployment workflow
- Mobile-responsive layouts (375px, 768px, 1440px)
- Accessibility features (reduced-motion, semantic HTML)
- All sections populated with extracted content
- Copy button for installation command

## Troubleshooting

**Build fails:**
- Check Node.js version (≥18 required)
- Verify all dependencies installed (`bun install`)
- Check for syntax errors in Svelte files

**Animations not working:**
- Verify global.css is imported in +layout.svelte
- Check browser DevTools for CSS errors
- Test with prefers-reduced-motion disabled

**GitHub Pages 404:**
- Verify base path in svelte.config.js matches repo name
- Check GitHub Pages settings (Source: GitHub Actions)
- Verify workflow ran successfully (Actions tab)

**Deployment fails:**
- Check workflow file is in `.github/workflows/`
- Verify permissions in workflow (contents: read, pages: write)
- Check GitHub Pages is enabled in repo settings
