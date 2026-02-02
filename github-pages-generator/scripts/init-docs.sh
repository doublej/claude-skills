#!/bin/bash
# Quick scaffold script for GitHub Pages documentation

set -e

PROJECT_ROOT=${1:-.}
REPO_NAME=$(basename "$PROJECT_ROOT")

echo "Initializing GitHub Pages docs for: $REPO_NAME"

# Create directory structure
mkdir -p "$PROJECT_ROOT/docs/src/routes"
mkdir -p "$PROJECT_ROOT/docs/src/lib/styles"
mkdir -p "$PROJECT_ROOT/docs/src/lib/components"
mkdir -p "$PROJECT_ROOT/docs/static"
mkdir -p "$PROJECT_ROOT/.github/workflows"

# Create package.json
cat > "$PROJECT_ROOT/docs/package.json" <<EOF
{
  "name": "${REPO_NAME}-docs",
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
EOF

# Create svelte.config.js
cat > "$PROJECT_ROOT/docs/svelte.config.js" <<EOF
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
      base: process.env.NODE_ENV === 'production' ? '/${REPO_NAME}' : ''
    }
  }
};

export default config;
EOF

# Create vite.config.ts
cat > "$PROJECT_ROOT/docs/vite.config.ts" <<EOF
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()]
});
EOF

# Create tsconfig.json
cat > "$PROJECT_ROOT/docs/tsconfig.json" <<EOF
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
EOF

# Create .nojekyll
touch "$PROJECT_ROOT/docs/static/.nojekyll"

# Create robots.txt
cat > "$PROJECT_ROOT/docs/static/robots.txt" <<EOF
User-agent: *
Allow: /
EOF

# Create app.html
cat > "$PROJECT_ROOT/docs/src/app.html" <<EOF
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
EOF

# Create +layout.svelte
cat > "$PROJECT_ROOT/docs/src/routes/+layout.svelte" <<EOF
<script lang="ts">
  import '../lib/styles/global.css';
  let { children } = \$props();
</script>

{@render children()}
EOF

# Create +layout.ts
cat > "$PROJECT_ROOT/docs/src/routes/+layout.ts" <<EOF
export const prerender = true;
EOF

# Create global.css
cat > "$PROJECT_ROOT/docs/src/lib/styles/global.css" <<EOF
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
EOF

echo "Directory structure created"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_ROOT/docs"
echo "  bun install"
echo "  bun run dev"
