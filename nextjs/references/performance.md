# Performance

## Waterfall Elimination (Critical)

### Move Await Into Branches

```tsx
// WRONG — await blocks even when not needed
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const data = await fetchData((await params).id);
  if (!data) return <NotFound />;
  return <Display data={data} />;
}

// RIGHT — start early, await late
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const dataPromise = fetchData((await params).id);
  // ... other work ...
  const data = await dataPromise;
  if (!data) return <NotFound />;
  return <Display data={data} />;
}
```

### Parallel with Promise.all

```tsx
// WRONG — sequential
const user = await getUser(id);
const orders = await getOrders(id);
const reviews = await getReviews(id);
// Total: sum of all three

// RIGHT — parallel
const [user, orders, reviews] = await Promise.all([
  getUser(id),
  getOrders(id),
  getReviews(id),
]);
// Total: max of the three
```

### Suspense Boundaries for Streaming

```tsx
export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<CardSkeleton />}>
        <RevenueCard />   {/* streams independently */}
      </Suspense>
      <Suspense fallback={<CardSkeleton />}>
        <UsersCard />     {/* streams independently */}
      </Suspense>
    </div>
  );
}
```

## Bundle Size

### Dynamic Imports

```tsx
import dynamic from 'next/dynamic';

// Heavy component loaded only when needed
const Chart = dynamic(() => import('./Chart'), {
  loading: () => <Skeleton />,
  ssr: false, // skip SSR for browser-only components
});

export default function Dashboard() {
  return <Chart data={data} />;
}
```

### Barrel File Avoidance

Import directly from source files instead of index barrels:

```tsx
// WRONG
import { Button, Card, Modal } from '@/components';

// RIGHT
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
```

### Third-Party Script Loading

```tsx
import Script from 'next/script';

// Load after hydration (non-blocking)
<Script src="https://analytics.example.com/script.js" strategy="afterInteractive" />

// Load when browser is idle
<Script src="https://chat-widget.example.com/widget.js" strategy="lazyOnload" />
```

## Image Optimization

```tsx
import Image from 'next/image';

// Local image (auto-optimized)
import heroImage from './hero.jpg';
<Image src={heroImage} alt="Hero" priority /> {/* priority for LCP image */}

// Remote image
<Image
  src="https://cdn.example.com/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
  sizes="(max-width: 768px) 100vw, 50vw"
/>
```

**Rules:**
- Use `priority` on LCP (above-the-fold) images
- Always provide `sizes` for responsive images
- Configure `images.remotePatterns` in next.config for external images

## Server-Side Performance

### React.cache() for Deduplication

```tsx
import { cache } from 'react';

export const getUser = cache(async (id: string) => {
  return await db.users.findUnique({ where: { id } });
});

// Multiple components calling getUser(same-id) in one request → single query
```

### Minimize Client Props

```tsx
// WRONG — sending entire object to client
<ClientComponent data={largeServerData} />

// RIGHT — send only what client needs
<ClientComponent title={data.title} count={data.items.length} />
```

### Non-Blocking Operations (after())

```tsx
import { after } from 'next/server';

export async function POST(request: Request) {
  const data = await request.json();
  const result = await processData(data);

  // Analytics/logging after response is sent
  after(async () => {
    await logAnalytics({ action: 'process', data });
  });

  return Response.json(result);
}
```

## Core Web Vitals Targets

| Metric | Target | How |
|--------|--------|-----|
| LCP < 2.5s | `priority` on hero images, avoid client-side fetching for above-fold content |
| INP < 200ms | `startTransition` for non-urgent updates, minimize main-thread work |
| CLS < 0.1 | Set explicit `width`/`height` on images, use `next/font` |

## Font Optimization

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'], display: 'swap' });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  );
}
```

`next/font` auto-hosts fonts, eliminates layout shift, and applies `font-display: swap`.
