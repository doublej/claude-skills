# Data Fetching

## Server Component Fetching

### Basic Fetch with Caching

```tsx
// Static (cached forever until revalidated)
const data = await fetch('https://api.example.com/data');

// ISR (revalidate after N seconds)
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 } // 1 hour
});

// Dynamic (no cache)
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store'
});
```

**Next.js 15+ change**: `fetch` is no longer cached by default. Add `next: { revalidate }` or `cache: 'force-cache'` explicitly.

### Parallel Fetching (Eliminate Waterfalls)

```tsx
// WRONG: Sequential — second fetch waits for first
export default async function Page() {
  const user = await getUser();        // 200ms
  const posts = await getPosts();      // 300ms
  // Total: 500ms (waterfall)
}

// RIGHT: Parallel — both start immediately
export default async function Page() {
  const [user, posts] = await Promise.all([
    getUser(),   // 200ms
    getPosts(),  // 300ms
  ]);
  // Total: 300ms (parallel)
}
```

### Streaming with Suspense

```tsx
import { Suspense } from 'react';

export default function Page() {
  return (
    <div>
      <h1>Dashboard</h1>           {/* Sent immediately */}
      <Suspense fallback={<Skeleton />}>
        <SlowComponent />           {/* Streams when ready */}
      </Suspense>
      <Suspense fallback={<Spinner />}>
        <AnotherSlowComponent />    {/* Streams independently */}
      </Suspense>
    </div>
  );
}

async function SlowComponent() {
  const data = await fetchSlowData(); // takes 2s
  return <div>{data.content}</div>;
}
```

### React `cache()` for Deduplication

```tsx
import { cache } from 'react';

// Multiple components calling getUser(id) in the same request
// only trigger ONE actual fetch
export const getUser = cache(async (id: string) => {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
});
```

`React.cache()` deduplicates within a single request. For cross-request caching, use `"use cache"` (Next.js 15+).

## Database / ORM Fetching

```tsx
// Server Component — query directly
export default async function UsersPage() {
  const users = await prisma.user.findMany({
    select: { id: true, name: true, email: true },
  });
  return <UserList users={users} />;
}
```

No API route needed for server-only data access.

## Client-Side Data Fetching

Use only when server fetching isn't possible (real-time, user-specific after initial load):

```tsx
'use client';
import useSWR from 'swr';

const fetcher = (url: string) => fetch(url).then(r => r.json());

export function LivePrice({ symbol }: { symbol: string }) {
  const { data, error } = useSWR(`/api/price/${symbol}`, fetcher, {
    refreshInterval: 5000, // poll every 5s
  });
  if (error) return <div>Error</div>;
  if (!data) return <div>Loading...</div>;
  return <div>${data.price}</div>;
}
```

## Revalidation Strategies

| Strategy | When | How |
|----------|------|-----|
| Time-based | Content updates periodically | `next: { revalidate: 3600 }` |
| On-demand | After a mutation | `revalidatePath('/posts')` or `revalidateTag('posts')` |
| Tag-based | Granular cache control | `fetch(url, { next: { tags: ['posts'] } })` |

```tsx
// On-demand revalidation in a Server Action
'use server';
import { revalidatePath, revalidateTag } from 'next/cache';

export async function updatePost(id: string, data: FormData) {
  await db.posts.update({ where: { id }, data: { title: data.get('title') } });
  revalidateTag('posts');        // invalidate all fetches tagged 'posts'
  revalidatePath('/posts');      // revalidate the /posts page
}
```

## Loading States (loading.tsx)

```tsx
// app/posts/loading.tsx — automatic Suspense boundary
export default function Loading() {
  return <div className="animate-pulse">Loading posts...</div>;
}
```

This file automatically wraps `page.tsx` and nested layouts in `<Suspense>`.
