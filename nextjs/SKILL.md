---
name: nextjs
description: "App Router: server/client components, caching, streaming, Next.js 15/16 APIs"
---

# Next.js App Router Development

<before_writing>

## Before Writing Code

1. **Detect repo setup** (do not guess):
   - Next.js version: `node -p "require('./node_modules/next/package.json').version"`
   - React version: check `node_modules/react/package.json`
   - TypeScript or JavaScript
   - Styling: Tailwind / CSS Modules / styled-components
   - State management: none / Zustand / Jotai / Redux
   - Cache Components enabled: `grep -r "cacheComponents" next.config.* 2>/dev/null`

2. **Run repo audit** (if scripts available):
   ```bash
   node scripts/nextjs-doctor.mjs
   ```

3. **Identify existing patterns**:
   - Are server actions in `app/actions.ts` or colocated?
   - Is there a `lib/` or `utils/` directory for shared code?
   - How are layouts structured (nested, route groups)?

</before_writing>

<file_conventions>

| File | Purpose | Notes |
|------|---------|-------|
| `layout.tsx` | Shared UI, preserves state across navigations | Root layout MUST have `<html>` + `<body>` |
| `page.tsx` | Route UI, makes route publicly accessible | Only file that creates a route |
| `loading.tsx` | Suspense fallback for the segment | Auto-wrapped in `<Suspense>` |
| `error.tsx` | Error boundary for the segment | Must be `'use client'` |
| `not-found.tsx` | 404 UI | Triggered by `notFound()` |
| `template.tsx` | Like layout but re-renders on navigation | Use for animations, per-page state |
| `route.ts` | API endpoint (Route Handler) | Cannot coexist with `page.tsx` in same dir |
| `default.tsx` | Fallback for parallel route slots | Required for parallel routes |
| `middleware.ts` | Request interception (root only) | Deprecated in Next.js 16 → `proxy.ts` |
| `proxy.ts` | Network boundary (Next.js 16+) | Replaces middleware, Node.js only |

</file_conventions>

<server_client>

## Server vs Client Decision Tree

**All components are Server Components by default.** Only add `'use client'` when needed.

```
Does this component need...
├── React hooks (useState, useEffect, useContext)? → Client
├── Event handlers (onClick, onChange, onSubmit)?  → Client
├── Browser APIs (window, localStorage)?           → Client
├── Third-party libs requiring browser?            → Client
└── None of the above?                             → Server (default)

Server Component benefits:
- Zero client JS, direct DB/API access, secure secrets, smaller bundles
```

</server_client>

<composition_pattern>

### The Composition Pattern (Children Slot)

The #1 pattern LLMs get wrong. Server Components CAN be children of Client Components:

```tsx
// ClientWrapper.tsx
'use client';
import { useState } from 'react';
export function ClientWrapper({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  return <div>{open && children}</div>; // children stay Server Components!
}

// page.tsx (Server Component)
import { ClientWrapper } from './ClientWrapper';
import { ServerData } from './ServerData'; // Server Component
export default function Page() {
  return (
    <ClientWrapper>
      <ServerData /> {/* Stays on server, NOT converted to client */}
    </ClientWrapper>
  );
}
```

**Rules:**
- `'use client'` marks the boundary — all *imports* become client
- But `children` (passed as props) keep their original rendering
- Use this to wrap server content with client interactivity

</composition_pattern>

<core_patterns>

### Data Fetching (Server Components)

```tsx
// Server Component — fetch directly, no hooks needed
export default async function ProductsPage() {
  const products = await fetch('https://api.example.com/products', {
    next: { revalidate: 3600 } // ISR: revalidate every hour
  });
  const data = await products.json();
  return <ProductList products={data} />;
}
```

**Key rules:**
- Fetch in Server Components, not `useEffect` — see `references/anti-patterns.md`
- Use `next: { revalidate: N }` for ISR
- Parallel fetch with `Promise.all()` — never create waterfalls
- Wrap dynamic content in `<Suspense>` for streaming

### Server Actions

```tsx
// app/actions.ts
'use server';
import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  await db.posts.create({ data: { title } });
  revalidatePath('/posts');
  // No return for <form action={...}> — must return void
}

// For feedback, use useActionState:
export async function createPostWithState(prevState: any, formData: FormData) {
  const title = formData.get('title') as string;
  if (!title) return { error: 'Title required' };
  await db.posts.create({ data: { title } });
  revalidatePath('/posts');
  return { success: true };
}
```

**Rules:**
- `<form action={fn}>` expects void — use `useActionState` for return values
- Server Actions are for **mutations only**, never data fetching
- Validate all inputs — server actions are public HTTP endpoints
- See `references/server-actions.md` for full patterns

</core_patterns>

<async_apis>

### Async Request APIs (Next.js 15+)

```tsx
// params, searchParams, cookies, headers are all async in Next.js 15+
export default async function Page({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ q?: string }>;
}) {
  const { slug } = await params;
  const q = (await searchParams).q || '';
  // ...
}
```

</async_apis>

<anti_patterns>

## Anti-Patterns Quick Reference

| Anti-Pattern | Fix | Reference |
|-------------|-----|-----------|
| `useEffect` for data fetching | Use Server Component async fetch | `anti-patterns.md` |
| `useState` + `useEffect` for server data | Server Component with direct access | `anti-patterns.md` |
| `'use client'` on data-only components | Remove directive, use Server Component | `server-client-components.md` |
| Importing Server Component into Client | Use children slot (composition) | `server-client-components.md` |
| Sequential fetches (waterfall) | `Promise.all()` for parallel fetches | `performance.md` |
| `useEffect` for browser detection | Direct check in component body | `anti-patterns.md` |
| Server Action returning data for forms | Use `useActionState` or return void | `server-actions.md` |
| Barrel file imports | Import directly from source | `performance.md` |

</anti_patterns>

<changes>

## Next.js 15/16 Changes

### Next.js 15 (Breaking)
- **Async Request APIs**: `params`, `searchParams`, `cookies()`, `headers()` are all `Promise`
- `fetch` no longer cached by default (was cached in 14)
- `GET` Route Handlers no longer cached by default

### Next.js 16 (Breaking)
- **`proxy.ts`** replaces `middleware.ts` (middleware deprecated, Edge not supported in proxy)
- **Cache Components**: `"use cache"` directive with `cacheLife()`, `cacheTag()`, `updateTag()`
- **Turbopack**: stable, default bundler (opt out with `--webpack` flag)
- **Node.js 20.9+** required (18 dropped)
- **`next lint` removed** — use ESLint/Biome directly
- **`revalidateTag(tag)`** single-arg form deprecated — needs cacheLife profile
- Parallel route slots require explicit `default.js`
- `experimental.turbopack` → top-level `turbopack` config
- Run `npx @next/codemod@canary upgrade latest` for automated migration

</changes>

<context7>

## Context7 Integration

For up-to-date API details, use Context7 MCP:
```
resolve-library-id: "next.js" or "react"
query-docs: "use cache directive" or "server actions" or "metadata API"
```

</context7>

<quality_gates>

- [ ] `npm run build` succeeds (no type errors)
- [ ] `npm run dev` renders without console errors
- [ ] No `'use client'` on components that only fetch data
- [ ] No `useEffect` for data that could be fetched server-side
- [ ] Server actions validate inputs
- [ ] Dynamic content wrapped in `<Suspense>`
- [ ] Run `node scripts/nextjs-doctor.mjs` — no warnings

## Deep Reference

Load on demand from `references/`:

| Reference | Use When |
|-----------|----------|
| `server-client-components.md` | Composition patterns, serialization boundary, decision tree |
| `data-fetching.md` | RSC fetch, cache, revalidation, Suspense streaming |
| `routing-advanced.md` | Parallel/intercepting routes, route groups, middleware |
| `server-actions.md` | Forms, revalidation, progressive enhancement, security |
| `metadata-seo.md` | Metadata API, OpenGraph, JSON-LD, sitemap, robots |
| `cache-components.md` | `"use cache"`, `cacheLife`, `cacheTag` (Next.js 15/16) |
| `anti-patterns.md` | Catalog with before/after code fixes |
| `performance.md` | Waterfall elimination, bundle size, parallel fetching |

</deep_reference>

<scripts>

Run without loading source:
- `scripts/nextjs-doctor.mjs` — Repo pattern audit

</scripts>
