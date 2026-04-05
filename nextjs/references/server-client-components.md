# Server vs Client Components

## The Serialization Boundary

When a Server Component renders a Client Component, props cross the **serialization boundary**. Only serializable values can be passed:

| Serializable | NOT Serializable |
|-------------|-----------------|
| Strings, numbers, booleans | Functions (except Server Actions) |
| Arrays, plain objects | Classes, instances |
| Date, Map, Set | Symbols |
| FormData | DOM nodes, JSX as props (except children) |
| Server Action references | React context values |

## Composition Patterns

### Pattern 1: Children Slot (Most Common)

```tsx
// InteractiveCard.tsx
'use client';
import { useState } from 'react';

export function InteractiveCard({ children }: { children: React.ReactNode }) {
  const [expanded, setExpanded] = useState(false);
  return (
    <div onClick={() => setExpanded(!expanded)}>
      {expanded && children}
    </div>
  );
}

// page.tsx (Server Component)
import { InteractiveCard } from './InteractiveCard';

export default async function Page() {
  const data = await fetchData(); // server-side fetch
  return (
    <InteractiveCard>
      <p>{data.description}</p> {/* stays server-rendered */}
    </InteractiveCard>
  );
}
```

### Pattern 2: Render Prop / Slot Props

```tsx
// Tabs.tsx
'use client';
import { useState } from 'react';

export function Tabs({ tabs }: { tabs: { label: string; content: React.ReactNode }[] }) {
  const [active, setActive] = useState(0);
  return (
    <div>
      {tabs.map((tab, i) => (
        <button key={i} onClick={() => setActive(i)}>{tab.label}</button>
      ))}
      {tabs[active]?.content}
    </div>
  );
}
```

### Pattern 3: Provider Wrapping

```tsx
// Providers.tsx
'use client';
import { ThemeProvider } from 'next-themes';

export function Providers({ children }: { children: React.ReactNode }) {
  return <ThemeProvider attribute="class">{children}</ThemeProvider>;
}

// layout.tsx (Server Component)
import { Providers } from './Providers';

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html><body>
      <Providers>{children}</Providers>
    </body></html>
  );
}
```

## Decision Tree (Extended)

```
Need interactivity?
├── YES: Add 'use client'
│   ├── But also need server data? → Fetch in parent Server Component, pass as props
│   ├── Need server component children? → Use children slot pattern
│   └── Need context? → Create client Provider, wrap in layout
└── NO: Keep as Server Component (default)
    ├── Need async data? → Make component async, fetch directly
    ├── Need cookies/headers? → Import from 'next/headers', await in Next.js 15+
    └── Need to redirect? → Use redirect() from 'next/navigation'
```

## Common Mistakes

### Mistake 1: Adding 'use client' for navigation

```tsx
// WRONG — Link and redirect work in Server Components
'use client';
import Link from 'next/link';
export default function Nav() {
  return <Link href="/about">About</Link>;
}

// RIGHT — no directive needed
import Link from 'next/link';
export default function Nav() {
  return <Link href="/about">About</Link>;
}
```

Only `useRouter()`, `usePathname()`, `useSearchParams()` require `'use client'`.

### Mistake 2: Making entire page client-side

```tsx
// WRONG — entire page becomes client
'use client';
export default function Page() {
  const [data, setData] = useState(null);
  useEffect(() => { fetch('/api/data').then(r => r.json()).then(setData); }, []);
  return <div>{data?.title}</div>;
}

// RIGHT — server component with client islands
export default async function Page() {
  const data = await fetch('https://api.example.com/data').then(r => r.json());
  return (
    <div>
      <h1>{data.title}</h1>
      <LikeButton id={data.id} /> {/* only this is 'use client' */}
    </div>
  );
}
```

### Mistake 3: Importing server-only code in client component

```tsx
// WRONG — db import leaks to client bundle
'use client';
import { db } from '@/lib/db'; // build error or security leak

// RIGHT — fetch via server action or API route
'use client';
import { getData } from '@/app/actions';

export function DataDisplay() {
  const [data, setData] = useState(null);
  useEffect(() => { getData().then(setData); }, []);
  return <div>{data?.title}</div>;
}
```

Use `import 'server-only'` in server modules to get a build error if accidentally imported client-side.
