# Framework Integration Snippets

Drop-in patterns for the common JS/TS frameworks. Each emits llms.txt + JSON-LD + correct robots.txt at build/deploy.

## SvelteKit (preferred default for JJ)

`src/routes/llms.txt/+server.ts`:
```ts
export const prerender = true;
export async function GET() {
  const body = `# Site Name

> One-sentence description.

## Docs
- [Getting Started](https://site.com/docs/start)
- [API Reference](https://site.com/docs/api)

## Blog
- [Latest Post](https://site.com/blog/latest)
`;
  return new Response(body, { headers: { 'content-type': 'text/plain' } });
}
```

`src/routes/+layout.server.ts` — JSON-LD via load:
```ts
export const load = () => ({
  jsonLd: {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'Site Name',
    url: 'https://site.com',
    sameAs: [
      'https://en.wikipedia.org/wiki/Site_Name',
      'https://www.linkedin.com/company/site-name'
    ]
  }
});
```

`src/routes/+layout.svelte`:
```svelte
<script lang="ts">
  let { data, children } = $props();
</script>
<svelte:head>
  {@html `<script type="application/ld+json">${JSON.stringify(data.jsonLd)}</script>`}
</svelte:head>
{@render children()}
```

`static/robots.txt`: hand-written from `references/robots-patterns.md`.

## Astro

```js
// astro.config.mjs
import { defineConfig } from 'astro/config';
import { aeoAstroIntegration } from 'aeo.js/astro';

export default defineConfig({
  site: 'https://site.com',
  integrations: [
    aeoAstroIntegration({
      title: 'Site Name',
      description: 'One sentence.',
      url: 'https://site.com'
    })
  ]
});
```

## Next.js (App Router)

`app/llms.txt/route.ts`:
```ts
export const dynamic = 'force-static';
export async function GET() {
  return new Response(`# Site\n\n> Description.\n\n## Docs\n- [Start](https://site.com/start)\n`, {
    headers: { 'content-type': 'text/plain' }
  });
}
```

`app/layout.tsx`:
```tsx
export default function RootLayout({ children }) {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'Site',
    url: 'https://site.com'
  };
  return (
    <html lang="en">
      <head>
        <script type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

## Nuxt 3+

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['aeo.js/nuxt'],
  aeo: {
    title: 'Site',
    description: 'One sentence.',
    url: 'https://site.com'
  }
});
```

## Vite (any framework)

```ts
// vite.config.ts
import { defineConfig } from 'vite';
import { aeoVitePlugin } from 'aeo.js/vite';

export default defineConfig({
  plugins: [
    aeoVitePlugin({
      title: 'Site',
      description: 'One sentence.',
      url: 'https://site.com'
    })
  ]
});
```

## Plain static / Kirby / WordPress

Drop these files in the public root by hand, regenerate via `geo llms` + `geo schema`:
- `/llms.txt`
- `/llms-full.txt`
- `/robots.txt`
- `/.well-known/ai.txt` (optional)
- `/ai/summary.json` (optional, JSON-LD-ish summary)

## FAQ page pattern (any framework)

Wrap each Q/A in JSON-LD `FAQPage`:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is X?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "X is a concise factual answer with a number: 38%."
    }
  }]
}
</script>
```

FAQPage + Article + Speakable = highest citation odds for Q-style queries.
