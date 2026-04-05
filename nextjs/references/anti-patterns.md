# Next.js Anti-Patterns

## 1. useEffect for Data Fetching

```tsx
// WRONG
'use client';
import { useEffect, useState } from 'react';

export default function Posts() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/posts').then(r => r.json()).then(data => {
      setPosts(data);
      setLoading(false);
    });
  }, []);

  if (loading) return <div>Loading...</div>;
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>;
}
```

```tsx
// RIGHT — Server Component, zero client JS
export default async function Posts() {
  const posts = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 }
  }).then(r => r.json());

  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>;
}
```

## 2. useEffect for Browser Detection

```tsx
// WRONG — flash of wrong content, unnecessary state
'use client';
export default function Guard() {
  const [isSafari, setIsSafari] = useState(false);
  useEffect(() => { setIsSafari(/Safari/.test(navigator.userAgent)); }, []);
  return <div>{isSafari ? 'Unsupported' : 'Welcome'}</div>;
}
```

```tsx
// RIGHT — direct detection, no hooks
'use client';
export default function Guard() {
  const isSafari = typeof navigator !== 'undefined'
    && /Safari/.test(navigator.userAgent)
    && !/Chrome/.test(navigator.userAgent);

  return <div>{isSafari ? 'Unsupported' : 'Welcome'}</div>;
}
```

## 3. useEffect for URL Access

```tsx
// WRONG
'use client';
export default function ShareButton() {
  const [url, setUrl] = useState('');
  useEffect(() => { setUrl(window.location.href); }, []);
  return <button onClick={() => navigator.share({ url })}>Share</button>;
}
```

```tsx
// RIGHT — access in event handler
'use client';
export default function ShareButton() {
  return (
    <button onClick={() => navigator.share({ url: window.location.href })}>
      Share
    </button>
  );
}
```

## 4. Unnecessary 'use client' Directive

```tsx
// WRONG — Link works in Server Components
'use client';
import Link from 'next/link';
export function Nav() {
  return <Link href="/about">About</Link>;
}
```

```tsx
// RIGHT — no directive needed
import Link from 'next/link';
export function Nav() {
  return <Link href="/about">About</Link>;
}
```

## 5. Sequential Data Fetching (Waterfall)

```tsx
// WRONG — 500ms total (200 + 300)
export default async function Page() {
  const user = await getUser();     // 200ms wait
  const posts = await getPosts();   // 300ms wait after user completes
  return <div>{user.name}: {posts.length} posts</div>;
}
```

```tsx
// RIGHT — 300ms total (parallel)
export default async function Page() {
  const [user, posts] = await Promise.all([getUser(), getPosts()]);
  return <div>{user.name}: {posts.length} posts</div>;
}
```

## 6. Barrel File Imports

```tsx
// WRONG — imports entire barrel, tree-shaking may fail
import { Button, Input } from '@/components';
```

```tsx
// RIGHT — import directly
import { Button } from '@/components/Button';
import { Input } from '@/components/Input';
```

## 7. Server Action Returning Data for Forms

```tsx
// WRONG — build error: form action expects void
export async function save(formData: FormData) {
  'use server';
  await db.save(formData);
  return { success: true }; // Type error!
}
<form action={save}>...</form>
```

```tsx
// RIGHT — use useActionState for feedback
export async function save(prev: any, formData: FormData) {
  'use server';
  await db.save(formData);
  return { success: true }; // OK with useActionState
}

// Client component
const [state, action] = useActionState(save, null);
<form action={action}>...</form>
```

## 8. Server Action for Data Fetching

```tsx
// WRONG — server actions are for mutations
'use server';
export async function getProducts() {
  return await db.products.findMany();
}
```

```tsx
// RIGHT — use server component or cached function
export async function getProducts() {
  'use cache';
  return await db.products.findMany();
}
```

## 9. Missing Suspense for Dynamic Content

```tsx
// WRONG — entire page blocked by slow query
export default async function Page() {
  const slowData = await fetchSlowData(); // blocks everything
  return <div>{slowData.content}</div>;
}
```

```tsx
// RIGHT — stream slow content independently
import { Suspense } from 'react';

export default function Page() {
  return (
    <div>
      <h1>Fast Header</h1>
      <Suspense fallback={<Skeleton />}>
        <SlowContent />
      </Suspense>
    </div>
  );
}
```

## 10. Client Component Importing Server Module

```tsx
// WRONG — leaks server code to client
'use client';
import { db } from '@/lib/db';

// RIGHT — protect with server-only
// lib/db.ts
import 'server-only';
export const db = new PrismaClient();
```

Add `import 'server-only'` to any module that should never reach the client bundle.
