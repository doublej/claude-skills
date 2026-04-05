# Cache Components (Next.js 15/16)

## Setup

```tsx
// next.config.ts
import type { NextConfig } from 'next';
const nextConfig: NextConfig = { cacheComponents: true };
export default nextConfig;
```

## Core Concept

Cache Components replace segment-level config (`export const revalidate`) with compositional caching:

| Before (Deprecated) | After (Cache Components) |
|---------------------|--------------------------|
| `export const revalidate = 3600` | `cacheLife('hours')` inside `'use cache'` |
| `export const dynamic = 'force-static'` | `'use cache'` + Suspense boundaries |

## `"use cache"` Directive

Marks code as cacheable. Can be applied at file, component, or function level:

```tsx
// Component-level
async function UserCard({ id }: { id: string }) {
  'use cache';
  const user = await fetchUser(id);
  return <Card>{user.name}</Card>;
}

// Function-level
async function fetchWithCache(url: string) {
  'use cache';
  return fetch(url).then(r => r.json());
}

// File-level: all exports cached
'use cache';
export async function getData() { /* ... */ }
```

**All cached functions must be `async`.**

## `cacheLife()` — Cache Duration

```tsx
import { cacheLife } from 'next/cache';

async function Posts() {
  'use cache';
  cacheLife('hours'); // Predefined profile

  // Or custom:
  cacheLife({
    stale: 60,        // 1 min — client cache validity
    revalidate: 3600, // 1 hr — background refresh starts
    expire: 86400,    // 1 day — absolute expiration
  });

  return await db.posts.findMany();
}
```

Predefined profiles: `'default'`, `'seconds'`, `'minutes'`, `'hours'`, `'days'`, `'weeks'`, `'max'`

## `cacheTag()` — Tag for Invalidation

```tsx
import { cacheTag } from 'next/cache';

async function BlogPosts() {
  'use cache';
  cacheTag('posts');
  cacheLife('days');
  return await db.posts.findMany();
}

async function UserProfile({ userId }: { userId: string }) {
  'use cache';
  cacheTag('users', `user-${userId}`); // Multiple tags
  return await db.users.findUnique({ where: { id: userId } });
}
```

## `updateTag()` — Immediate Invalidation

For **read-your-own-writes** in Server Actions:

```tsx
'use server';
import { updateTag } from 'next/cache';

export async function createPost(formData: FormData) {
  await db.posts.create({ data: { title: formData.get('title') } });
  updateTag('posts'); // Immediate invalidation, user sees fresh data
}
```

`updateTag()` vs `revalidateTag()`:
- `updateTag()` — immediate, same-request consistency (Server Actions only)
- `revalidateTag(tag, profile)` — background SWR revalidation (Next.js 16 requires profile)

## Decision Tree

```
Does component fetch data or do I/O?
├── NO → Pure component, no caching needed
└── YES
    ├── Depends on request context (cookies, headers, searchParams)?
    │   ├── YES → Wrap in <Suspense>, keep dynamic
    │   └── NO → Can be cached
    │       ├── Same for all users? → 'use cache' + cacheTag + cacheLife
    │       └── User-specific?
    │           ├── Can extract as params? → Pass as args to cached fn
    │           └── Cannot extract? → 'use cache: private' (last resort)
```

## Composition: Static + Cached + Dynamic

```tsx
export default async function Page() {
  return (
    <>
      <Header />                              {/* Static shell */}
      <CachedPosts />                         {/* Cached */}
      <Suspense fallback={<Skeleton />}>
        <DynamicComments />                   {/* Dynamic, streams */}
      </Suspense>
    </>
  );
}

async function CachedPosts() {
  'use cache';
  cacheTag('posts');
  cacheLife('hours');
  const posts = await db.posts.findMany();
  return <PostList posts={posts} />;
}
```

## Critical Rule

**Server Actions are for mutations only. Never use `'use server'` for data fetching:**

```tsx
// WRONG
'use server';
export async function getProducts() {
  return await db.products.findMany(); // Not a mutation!
}

// RIGHT
export async function getProducts() {
  'use cache';
  cacheTag('products');
  return await db.products.findMany();
}
```
