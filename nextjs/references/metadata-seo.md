# Metadata & SEO

## Static Metadata

```tsx
// app/layout.tsx
import type { Metadata, Viewport } from 'next';

// Viewport must be a separate export (Next.js 14+)
export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#0a0a0a' },
  ],
};

export const metadata: Metadata = {
  metadataBase: new URL('https://example.com'),
  title: {
    default: 'Site Name',
    template: '%s | Site Name', // pages use template
  },
  description: 'Site description (150-160 chars)',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    siteName: 'Site Name',
    images: [{ url: '/og.png', width: 1200, height: 630 }],
  },
  twitter: {
    card: 'summary_large_image',
  },
  alternates: {
    canonical: '/',
  },
  robots: { index: true, follow: true },
};
```

## Dynamic Metadata

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next';

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>; // async in Next.js 15+
}): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPost(slug);

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
    },
    alternates: {
      canonical: `/blog/${slug}`,
    },
  };
}
```

**Rules:**
- Don't mix `metadata` object and `generateMetadata` in the same file
- `metadataBase` is required for relative URLs
- Viewport must be a separate export (not inside metadata)

## Sitemap

```tsx
// app/sitemap.ts
import type { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await getAllPosts();
  const postUrls = posts.map((post) => ({
    url: `https://example.com/blog/${post.slug}`,
    lastModified: post.updatedAt,
    changeFrequency: 'weekly' as const,
    priority: 0.7,
  }));

  return [
    { url: 'https://example.com', lastModified: new Date(), priority: 1 },
    { url: 'https://example.com/about', lastModified: new Date(), priority: 0.8 },
    ...postUrls,
  ];
}
```

## Robots

```tsx
// app/robots.ts
import type { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [{ userAgent: '*', allow: '/', disallow: ['/api/', '/admin/'] }],
    sitemap: 'https://example.com/sitemap.xml',
  };
}
```

## JSON-LD Structured Data

```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPost({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = await getPost(slug);

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: post.title,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: { '@type': 'Person', name: post.author.name },
    image: post.coverImage,
    description: post.excerpt,
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <article>{post.content}</article>
    </>
  );
}
```

## Common Mistakes

1. **Mixing next-seo with Metadata API** — use only Metadata API in App Router
2. **Missing `metadataBase`** — required for relative URLs in OG images
3. **Viewport in metadata object** — must be separate `viewport` export
4. **CSR for SEO pages** — use SSG/SSR for indexable content
5. **Blocking CSS/JS in robots.txt** — Googlebot needs these to render
