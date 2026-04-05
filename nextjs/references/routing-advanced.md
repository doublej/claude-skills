# Advanced Routing

## Route Groups

Organize routes without affecting URL structure:

```
app/
├── (marketing)/
│   ├── layout.tsx      # Marketing layout
│   ├── page.tsx        # /
│   └── about/page.tsx  # /about
├── (shop)/
│   ├── layout.tsx      # Shop layout
│   └── products/page.tsx  # /products
└── layout.tsx          # Root layout
```

Parentheses `()` are stripped from the URL.

## Dynamic Routes

```
app/
├── blog/
│   ├── [slug]/page.tsx           # /blog/hello-world
│   ├── [...slug]/page.tsx        # /blog/a/b/c (catch-all)
│   └── [[...slug]]/page.tsx      # /blog or /blog/a/b (optional catch-all)
```

```tsx
// app/blog/[slug]/page.tsx
export default async function Post({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params; // Next.js 15+: params is async
  const post = await getPost(slug);
  return <article>{post.content}</article>;
}

// Static generation for dynamic routes
export async function generateStaticParams() {
  const posts = await getAllPosts();
  return posts.map((post) => ({ slug: post.slug }));
}
```

## Parallel Routes

Render multiple pages simultaneously in the same layout:

```
app/
├── layout.tsx
├── page.tsx
├── @analytics/
│   ├── page.tsx
│   └── default.tsx    # REQUIRED in Next.js 16
└── @team/
    ├── page.tsx
    └── default.tsx    # REQUIRED in Next.js 16
```

```tsx
// app/layout.tsx
export default function Layout({
  children,
  analytics,
  team,
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
  team: React.ReactNode;
}) {
  return (
    <div>
      {children}
      <div className="grid grid-cols-2">
        {analytics}
        {team}
      </div>
    </div>
  );
}
```

**Next.js 16**: All parallel route slots MUST have a `default.tsx` file.

## Intercepting Routes

Show a route in a modal while preserving URL:

```
app/
├── feed/
│   └── page.tsx
├── photo/[id]/
│   └── page.tsx          # Full page view: /photo/123
└── @modal/
    ├── (..)photo/[id]/
    │   └── page.tsx      # Modal interceptor
    └── default.tsx
```

Convention: `(.)` same level, `(..)` one up, `(..)(..)` two up, `(...)` root.

## Route Handlers (API Routes)

```tsx
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const page = searchParams.get('page') || '1';
  const posts = await db.posts.findMany({ skip: (+page - 1) * 10, take: 10 });
  return NextResponse.json(posts);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const post = await db.posts.create({ data: body });
  return NextResponse.json(post, { status: 201 });
}
```

**Next.js 15+ change**: `GET` Route Handlers are no longer cached by default.

## Middleware / Proxy

```tsx
// middleware.ts (Next.js 14-15) or proxy.ts (Next.js 16+)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Redirect
  if (request.nextUrl.pathname === '/old') {
    return NextResponse.redirect(new URL('/new', request.url));
  }
  // Rewrite
  if (request.nextUrl.pathname.startsWith('/api/v1')) {
    return NextResponse.rewrite(new URL('/api/v2' + request.nextUrl.pathname.slice(7), request.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: ['/old', '/api/v1/:path*'],
};
```

**Next.js 16**: `middleware.ts` deprecated in favor of `proxy.ts`. Proxy runs on Node.js only (no Edge).

## Error Handling

```tsx
// app/posts/error.tsx — MUST be 'use client'
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

`error.tsx` catches errors from `page.tsx` and children in the same segment. Root layout errors need `app/global-error.tsx`.
