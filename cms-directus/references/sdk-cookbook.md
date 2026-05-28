# SDK Cookbook — `@directus/sdk` v19+

Copy-paste patterns for `@directus/sdk`. Install: `npm i @directus/sdk` (or `bun add @directus/sdk`).

## Client initialization

### Static token (server-side, CI, seed)

```ts
import { createDirectus, rest, staticToken } from '@directus/sdk'

const directus = createDirectus(process.env.DIRECTUS_URL!)
  .with(staticToken(process.env.ADMIN_TOKEN!))
  .with(rest())
```

### Email/password with auto-refresh (user sessions)

```ts
import { createDirectus, authentication, rest } from '@directus/sdk'

const directus = createDirectus(url)
  .with(authentication('json'))  // 'json' for SPA, 'cookie' for SSR
  .with(rest())

await directus.login({ email, password })
// tokens stored inside the client; refresh happens automatically on 401
await directus.logout()
```

### Typed client

```ts
interface Schema {
  posts: Post[]
  authors: Author[]
  site: Site          // singleton — note: not an array
}
interface Post { id: string; title: string; author: string | Author; status: 'draft' | 'published' }
interface Author { id: string; name: string }
interface Site { id: number; title: string }

const directus = createDirectus<Schema>(url).with(rest())
// Now readItems('posts', ...) returns Post[]
```

## CRUD

```ts
import {
  readItems, readItem, createItem, createItems,
  updateItem, updateItems, deleteItem, deleteItems,
  readSingleton, updateSingleton,
} from '@directus/sdk'

// List with filter/sort/limit/fields
const published = await directus.request(
  readItems('posts', {
    fields: ['id', 'title', { author: ['name'] }],
    filter: { status: { _eq: 'published' } },
    sort: ['-date_published'],
    limit: 20,
  })
)

// Single by id
const post = await directus.request(
  readItem('posts', postId, { fields: ['*', 'author.name'] })
)

// Create one (server fills id)
const created = await directus.request(
  createItem('posts', { title: 'Hi', status: 'draft' })
)

// Create many
await directus.request(
  createItems('tags', [{ name: 'a' }, { name: 'b' }])
)

// Update one
await directus.request(
  updateItem('posts', postId, { status: 'published' })
)

// Update many (same payload to each id)
await directus.request(
  updateItems('posts', [id1, id2, id3], { status: 'archived' })
)

// Delete
await directus.request(deleteItem('posts', postId))
await directus.request(deleteItems('posts', [id1, id2]))

// Singleton
const site = await directus.request(readSingleton('site'))
await directus.request(updateSingleton('site', { title: 'Renamed' }))
```

## Field selection (sparse fieldsets)

| Goal | Syntax |
|---|---|
| All direct fields | `fields: ['*']` |
| Specific fields | `fields: ['id', 'title']` |
| M2O relation field | `fields: ['author.name']` (dot) or `[{ author: ['name'] }]` |
| All direct + nested all | `fields: ['*', { author: ['*'] }]` |
| O2M relation | `fields: ['*', { comments: ['id', 'text'] }]` |
| Everything two levels deep | `fields: ['*.*']` (careful — can be huge) |
| M2M via junction alias | `fields: ['*', { tags: [{ tags_id: ['name'] }] }]` |
| M2A (any type) | `fields: ['*', { blocks: [{ item: { block_hero: ['*'], block_text: ['*'] } }] }]` |

## Me / current user

```ts
import { readMe, updateMe } from '@directus/sdk'

const me = await directus.request(
  readMe({ fields: ['id', 'email', 'first_name', { role: ['name'] }] })
)
await directus.request(updateMe({ theme: 'dark' }))
```

## Relationships

### M2O (post belongs to author)

```ts
// Read: expand
readItems('posts', { fields: ['*', { author: ['name', 'email'] }] })

// Create: pass id directly, or nested object to create + link
createItem('posts', { title: 'A', author: existingAuthorId })
createItem('posts', { title: 'A', author: { name: 'New author' } })
```

### O2M (author has many posts)

```ts
// Read: inline children
readItems('authors', {
  fields: ['*', { posts: ['id', 'title'] }],
})

// Create author + posts in one call
createItem('authors', {
  name: 'Jane',
  posts: [
    { title: 'First' },
    { title: 'Second' },
  ],
})
```

### M2M (article ↔ tag via `articles_tags` junction)

```ts
// Read (junction is transparent)
readItems('articles', {
  fields: ['*', { tags: [{ tags_id: ['name'] }] }],
})

// Create + link existing tag
createItem('articles', {
  title: 'A',
  tags: [{ tags_id: existingTagId }],
})

// Create + create new tag
createItem('articles', {
  title: 'A',
  tags: [{ tags_id: { name: 'New tag' } }],
})
```

### M2A (page has any of several block types)

```ts
createItem('pages', {
  slug: 'home',
  blocks: [
    { collection: 'block_hero', item: { headline: 'Welcome' } },
    { collection: 'block_text', item: { body: 'Lorem ipsum' } },
  ],
})

// Read with type-discrimination
readItems('pages', {
  fields: ['*', { blocks: [
    'id', 'collection',
    { item: {
      block_hero: ['headline', 'image'],
      block_text: ['body'],
    }},
  ]}],
})
```

## Files

```ts
import { uploadFiles, readFile, readFiles, updateFile, deleteFile } from '@directus/sdk'

// Upload — FormData is required (Node 18+, Bun, browsers all have it)
const fd = new FormData()
fd.append('title', 'hero')           // any metadata fields go before 'file'
fd.append('folder', folderId)
fd.append('file', blob, 'hero.jpg')  // file must be last
const uploaded = await directus.request(uploadFiles(fd))

// Metadata only
const meta = await directus.request(readFile(uploaded.id))
await directus.request(updateFile(uploaded.id, { title: 'Updated' }))
await directus.request(deleteFile(uploaded.id))
```

### Asset transforms (URL query params)

Public URL: `${DIRECTUS_URL}/assets/${fileId}?width=800&height=600&fit=cover&quality=80&format=webp`

| Param | Values |
|---|---|
| `width` / `height` | integer px |
| `fit` | `cover` (default), `contain`, `inside`, `outside` |
| `quality` | 1–100 |
| `format` | `jpg`, `png`, `webp`, `tiff`, `avif` |
| `key` | named preset from Settings → Project Settings → Storage Assets |

Use named presets in production — direct transform params can be disabled for untrusted clients.

## Auth helpers

```ts
import { withToken } from '@directus/sdk'

// Temporary one-off token (e.g., invite link)
const data = await directus.request(
  withToken('ONE_TIME_TOKEN', readItems('posts'))
)

// Manual refresh
await directus.refresh()

// Manual logout
await directus.logout()
```

### Filter by current user/role

```ts
readItems('posts', {
  filter: { user_created: { _eq: '$CURRENT_USER' } },
})
```

## Realtime / WebSockets

```ts
import { createDirectus, staticToken, realtime } from '@directus/sdk'

const ws = createDirectus(url).with(staticToken(token)).with(realtime())
await ws.connect()

// Subscribe
const { subscription } = await ws.subscribe('messages', {
  event: 'create',
  query: { fields: ['id', 'text', { user_created: ['email'] }] },
})

for await (const change of subscription) {
  console.log('new message', change.data)
}

// Fire-and-forget create via WS
ws.sendMessage({
  type: 'items',
  collection: 'messages',
  action: 'create',
  data: { text: 'Hello' },
})
```

Enable with `WEBSOCKETS_ENABLED=true` in Directus env.

## Raw REST fallback

Sometimes the SDK lacks a composable (e.g., custom endpoint from an extension) or you need raw control. The haist-cms project uses a thin wrapper:

```ts
// lib/api.ts — direct REST with typed error handling
async function request(method: string, path: string, body?: Json): Promise<Json | null> {
  const res = await fetch(`${directusUrl}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${directusToken}`,
    },
    body: body ? JSON.stringify(body) : undefined,
  })
  const text = await res.text()
  const data = text ? JSON.parse(text) : null
  if (!res.ok) {
    const err = data as { errors?: { message: string; extensions?: { code?: string } }[] } | null
    const first = err?.errors?.[0]
    const code = first?.extensions?.code
    const e = new Error(`${method} ${path} → ${res.status}: ${first?.message ?? text}`) as Error & { code?: string }
    e.code = code
    throw e
  }
  return data
}

export const api = {
  get:    (path: string)              => request('GET', path),
  post:   (path: string, body: Json)  => request('POST', path, body),
  patch:  (path: string, body: Json)  => request('PATCH', path, body),
  delete: (path: string)              => request('DELETE', path),
}
```

Pair with the `safePost` idempotency wrapper — see `schema-builder.md`.

## Error codes to know

| Code | Meaning | Action |
|---|---|---|
| `RECORD_NOT_UNIQUE` | Unique constraint violation | Swallow in idempotent seed scripts |
| `INVALID_PAYLOAD` | Schema mismatch | Log payload, fix shape |
| `INVALID_CREDENTIALS` | Bad login | Surface to user |
| `TOKEN_EXPIRED` | JWT expired | Refresh (or use `authentication()`) |
| `FORBIDDEN` | Permission denied by role/policy | Check `directus_policies` |
| `ROUTE_NOT_FOUND` | Collection doesn't exist | Check `readCollections()` |

Errors are returned as `{ errors: [{ message, extensions: { code } }] }`.
