---
name: cms-directus
description: "Headless CMS: SDK v19 queries, filter rules, programmatic schema, extensions, self-hosted Docker, @directus/content-mcp"
---

# Directus

Self-hosted headless CMS. This skill covers the TypeScript SDK (`@directus/sdk` v19+), REST admin calls, programmatic schema management, extensions, Docker self-hosting, and the official MCP server.

<when_to_use>

Trigger: user asks about Directus, mentions `@directus/sdk`, `directus_*` collections, writes Directus flows/extensions, edits `docker-compose.yml` with `directus/directus` image, or runs `directus schema snapshot`.

Not this skill: generic headless CMS comparison, other CMSes (Strapi, Payload, Contentful), custom frontend rendering unrelated to Directus APIs.

</when_to_use>

<setup>

Env vars (match the user's haist-cms convention):

```bash
DIRECTUS_URL=http://localhost:8055    # or https://cms.example.com
ADMIN_TOKEN=<static token from User Directory → your user → Token>
```

Static token init (server-side scripts, seed tools, CI):

```ts
import { createDirectus, rest, staticToken } from '@directus/sdk'
const directus = createDirectus(process.env.DIRECTUS_URL!)
  .with(staticToken(process.env.ADMIN_TOKEN!))
  .with(rest())
```

Email/password with auto-refresh (user sessions, browser apps):

```ts
import { createDirectus, authentication, rest } from '@directus/sdk'
const directus = createDirectus(url).with(authentication()).with(rest())
await directus.login({ email, password })    // tokens stored; auto-refresh
```

Deep dive: `references/sdk-cookbook.md`.

</setup>

<crud_quick_reference>

All requests go through `directus.request(<composable>(...))`.

| Operation | Composable | Example |
|---|---|---|
| List | `readItems` | `readItems('posts', { filter: { status: { _eq: 'published' } }, limit: 10 })` |
| Single | `readItem` | `readItem('posts', id, { fields: ['*', 'author.name'] })` |
| Create | `createItem` | `createItem('posts', { title: 'Hi', status: 'draft' })` |
| Create many | `createItems` | `createItems('tags', [{ name: 'a' }, { name: 'b' }])` |
| Update | `updateItem` | `updateItem('posts', id, { status: 'published' })` |
| Update many | `updateItems` | `updateItems('posts', [id1, id2], { status: 'archived' })` |
| Delete | `deleteItem` | `deleteItem('posts', id)` |
| Singleton | `readSingleton` / `updateSingleton` | `updateSingleton('site', { title: 'New' })` |
| Me | `readMe` | `readMe({ fields: ['*', 'role.*'] })` |

</crud_quick_reference>

<filter_essentials>

Filters are JSON — field → operator → value. `_and` / `_or` for logic. Dynamic: `$CURRENT_USER`, `$CURRENT_ROLE`, `$NOW`, `$NOW(+7 days)`.

```ts
filter: {
  _and: [
    { status: { _eq: 'published' } },
    { date_published: { _lte: '$NOW' } },
    { _or: [
      { author: { _eq: '$CURRENT_USER' } },
      { visibility: { _eq: 'public' } },
    ]},
  ]
}
```

Full operator table + nested / relational / `_some` / `_none`: `references/filter-rules.md`.

</filter_essentials>

<schema_management>

| Situation | Approach |
|---|---|
| One-off change by an admin | Directus Admin UI → Settings → Data Model |
| Reproducible between environments (dev → staging → prod) | `directus schema snapshot` → commit `schema.yaml` → `directus schema apply` in CI |
| Programmatic / generated from code / per-tenant | REST POST to `/collections`, `/fields`, `/relations` — use the idempotent pattern below |

Snapshot via docker compose (matches user's stack):

```bash
docker compose exec directus npx directus schema snapshot --yes ./snapshots/schema.yaml
docker compose exec directus npx directus schema apply ./snapshots/schema.yaml
```

Programmatic: `references/schema-builder.md` — contains the battle-tested M2A junction recipe (5 steps), O2M recipe (3 steps), UUID primary-key pattern, and the `safePost` idempotency wrapper.

</schema_management>

<idempotent_operations>

Schema/seed scripts must be re-runnable. Catch `RECORD_NOT_UNIQUE` and existence errors so CI doesn't fail on the second run:

```ts
async function safePost(path: string, body: Json): Promise<void> {
  try {
    await api.post(path, body)
  } catch (e) {
    const err = e as Error & { code?: string }
    if (err.code === 'RECORD_NOT_UNIQUE' || /already exists/i.test(err.message)) return
    throw e
  }
}
```

Use for `/collections`, `/fields`, `/relations`, `/presets`. For items with unique slugs, prefer the delete-then-create pattern — see `references/schema-builder.md`.

</idempotent_operations>

<singletons>

Collections with a single row. At creation time: `meta: { singleton: true }`. At runtime:

```ts
// Read / update — no id
await directus.request(readSingleton('site', { fields: ['*'] }))
await directus.request(updateSingleton('site', { title: 'New' }))

// Or REST:
//   GET   /items/site
//   PATCH /items/site   (no id in path)
```

</singletons>

<files_assets>

```ts
// Upload (FormData required)
const fd = new FormData()
fd.append('file', blob)
fd.append('title', 'hero')
const file = await directus.request(uploadFiles(fd))

// Serve with transforms (URL query params)
// /assets/{id}?width=800&height=600&fit=cover&quality=80&format=webp
```

`fit`: `cover` (default), `contain`, `inside`, `outside`. `format`: `jpg`, `png`, `webp`, `tiff`, `avif`. Details in `references/sdk-cookbook.md`.

</files_assets>

<extensions>

Nine types: `interface`, `display`, `layout`, `module`, `panel` (app), `hook`, `endpoint`, `operation`, `bundle` (api). Scaffold:

```bash
npx create-directus-extension@latest
# or
npx directus-extension create interface my-slider
```

Each type + minimal snippet: `references/extensions.md`.

</extensions>

<common_gotchas>

- **Schema cache** — SDK caches collection schemas; call `directus.reset()` after schema changes within the same process
- **Permissions vs Policies** — Directus 11+ uses **Policies** (attached to roles). Old `directus_permissions` rules still work but admin UI edits go through Policies
- **Public role is default-deny** — explicitly grant read permissions for any public API endpoint
- **M2A payload shape** — junction rows carry `{ item: '<id>', collection: '<collection_name>' }`, not just an id
- **Access token expiry** — default 15 min; `authentication()` composable refreshes automatically, `staticToken()` does not
- **`directus_*` system collections** — users, roles, files, policies; non-admins have limited visibility
- **UUID primary keys** — when creating collections via REST, explicitly include the id field with `special: ['uuid']` and `is_primary_key: true` (Directus does NOT auto-create one)

</common_gotchas>

<official_mcp_server>

`@directus/content-mcp` is the Directus-team-maintained MCP. Use it for **runtime data operations** from an LLM (read/write items, files, fields, flows). It's complementary to this skill — the skill teaches authoring patterns, the MCP exposes live Directus tools.

```json
{
  "mcpServers": {
    "directus": {
      "command": "npx",
      "args": ["@directus/content-mcp@latest"],
      "env": {
        "DIRECTUS_URL": "https://your-instance.com",
        "DIRECTUS_TOKEN": "<static token>"
      }
    }
  }
}
```

Safety: the MCP intentionally blocks destructive schema ops (delete collections, delete fields). Restrict further with `DISABLE_TOOLS=delete-item,update-field`. Full tool list + env vars: `references/mcp-server.md`.

</official_mcp_server>

<self_hosting>

Minimal `docker-compose.yml`, required env vars (`KEY`, `SECRET`, `DB_*`, `STORAGE_*`), websockets, and the snapshot workflow: `references/self-hosting.md`.

</self_hosting>

<references_index>

| File | Load when |
|---|---|
| `sdk-cookbook.md` | Writing any SDK code — CRUD, relationships, files, realtime, auth |
| `filter-rules.md` | Composing non-trivial filters or using dynamic variables |
| `schema-builder.md` | Programmatic schema changes, M2A/O2M setup, idempotent seeds |
| `extensions.md` | Building any of the 9 extension types |
| `self-hosting.md` | Editing `docker-compose.yml`, env vars, upgrades, backups |
| `mcp-server.md` | Installing or configuring `@directus/content-mcp` |

</references_index>
