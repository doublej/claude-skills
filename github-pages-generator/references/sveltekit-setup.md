# SvelteKit Static Site Setup

Complete guide for configuring SvelteKit for static site generation and GitHub Pages deployment.

## Project Structure

```
docs/
├── src/
│   ├── app.html                # HTML template with fonts
│   ├── routes/
│   │   ├── +layout.svelte     # Root layout (imports global CSS)
│   │   ├── +layout.ts         # Layout config (prerender: true)
│   │   └── +page.svelte       # Main page content
│   └── lib/
│       ├── components/        # Reusable Svelte components
│       ├── styles/
│       │   └── global.css     # Global styles and animations
│       └── assets/            # Images, icons
├── static/
│   ├── .nojekyll             # Disable Jekyll processing
│   ├── icon.svg              # Favicon
│   └── robots.txt            # SEO
├── build/                     # Build output (git-ignored)
├── package.json
├── svelte.config.js          # Static adapter config
├── vite.config.ts            # Vite build config
└── tsconfig.json             # TypeScript config
```

## Configuration Files

### package.json

```json
{
  "name": "project-docs",
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

### svelte.config.js

```javascript
import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  kit: {
    adapter: adapter({
      pages: 'build',      // Output directory
      assets: 'build',     // Assets directory
      fallback: null,      // No SPA fallback
      precompress: false,  // Don't precompress files
      strict: true         // Strict mode
    }),
    paths: {
      // Set base path for GitHub Pages subpath deployment
      base: process.env.NODE_ENV === 'production' ? '/repo-name' : ''
    }
  }
};

export default config;
```

**Important:** The `base` path must match your GitHub repository name for subpath deployment.

### vite.config.ts

```typescript
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()]
});
```

### tsconfig.json

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

## Core Files

### src/app.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="icon" href="%sveltekit.assets%/icon.svg" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <!-- Google Fonts: Instrument Sans + DM Mono -->
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

### src/routes/+layout.svelte

```svelte
<script lang="ts">
  import '../lib/styles/global.css';
  let { children } = $props();
</script>

{@render children()}
```

### src/routes/+layout.ts

```typescript
// Enable prerendering for all pages
export const prerender = true;
```

## Static Files

### static/.nojekyll

Empty file. This tells GitHub Pages not to process the site with Jekyll.

```bash
touch static/.nojekyll
```

### static/robots.txt

```
User-agent: *
Allow: /
```

### static/icon.svg

Simple SVG favicon (replace with project-specific icon):

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" fill="#1a1a1a"/>
  <text x="50" y="70" font-family="system-ui" font-size="60" font-weight="bold" fill="white" text-anchor="middle">P</text>
</svg>
```

## Build Process

### Development

```bash
bun run dev
# Opens at http://localhost:5173
```

### Production Build

```bash
bun run build
# Outputs to build/ directory
```

### Preview Production Build

```bash
bun run preview
# Opens at http://localhost:4173
```

## GitHub Pages Deployment

### Setup Steps

1. **Enable GitHub Pages:**
   - Go to repository Settings > Pages
   - Source: **GitHub Actions** (not "Deploy from branch")
   - Save

2. **Create Workflow:**
   - Create `.github/workflows/deploy-docs.yml`
   - Use workflow template (see GitHub Actions section)

3. **Push to Trigger:**
   - Push changes to `main` branch
   - Workflow runs automatically
   - Site deploys to `https://username.github.io/repo-name/`

### GitHub Actions Workflow

See `references/github-actions-workflow.yml` for complete workflow template.

## Base Path Configuration

For GitHub Pages subpath deployment (e.g., `/repo-name`):

1. **In svelte.config.js:**
   ```javascript
   paths: {
     base: process.env.NODE_ENV === 'production' ? '/repo-name' : ''
   }
   ```

2. **In Svelte components:**
   ```svelte
   <script>
     import { base } from '$app/paths';
   </script>

   <a href="{base}/">Home</a>
   <img src="{base}/image.png" alt="..." />
   ```

3. **For static assets in `static/`:**
   - Use `%sveltekit.assets%` in `app.html`
   - SvelteKit automatically handles base path

## Common Issues

### 404 on GitHub Pages

**Problem:** All pages return 404

**Solution:**
- Verify `base` path in `svelte.config.js` matches repo name exactly
- Check GitHub Pages settings (Source: GitHub Actions)
- Verify workflow ran successfully (check Actions tab)
- Ensure `.nojekyll` file exists in `static/`

### Broken Assets/Links

**Problem:** Images, CSS, or links don't work on GitHub Pages

**Solution:**
- Use `base` from `$app/paths` for all internal links
- Use `%sveltekit.assets%` in `app.html` for static assets
- Don't hardcode absolute paths

### Build Fails

**Problem:** `bun run build` fails

**Solution:**
- Check Node.js version (≥18 required)
- Verify all dependencies installed: `bun install`
- Check for TypeScript errors: `tsc --noEmit`
- Check for Svelte syntax errors

### Prerender Errors

**Problem:** "Not all routes can be prerendered"

**Solution:**
- Ensure `export const prerender = true` in `+layout.ts`
- Remove any dynamic routes (e.g., `[slug]`)
- Remove any server-side logic (e.g., `+server.ts`)

## Performance Optimization

### Recommended Optimizations

1. **Preconnect to fonts:**
   ```html
   <link rel="preconnect" href="https://fonts.googleapis.com">
   <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
   ```

2. **Font display swap:**
   ```
   &display=swap
   ```

3. **Image optimization:**
   - Use modern formats (WebP, AVIF)
   - Provide width/height attributes
   - Use responsive images (`srcset`)

4. **Code splitting:**
   - SvelteKit automatically code-splits by route
   - Keep components small and focused

5. **Minimize dependencies:**
   - Only use `devDependencies` (site is static)
   - Avoid runtime dependencies

## Version Compatibility

This setup is tested with:
- SvelteKit 2.11.1+
- Svelte 5.17.0+
- Vite 7.0.5+
- Bun 1.0+
- Node.js 18+

## Further Reading

- [SvelteKit Static Adapter Docs](https://kit.svelte.dev/docs/adapter-static)
- [GitHub Pages Documentation](https://docs.github.com/pages)
- [Vite Configuration](https://vite.dev/config/)
