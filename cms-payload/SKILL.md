---
name: cms-payload
description: Payload CMS 3.0 development — scaffold projects, generate collections/fields/globals/hooks/access, connect MCP servers to live instances. TRIGGER when user mentions Payload CMS, payload.config.ts, or asks to scaffold/generate Payload components.
---

# Payload CMS 3.0

<description>
Scaffold, generate, and manage Payload CMS 3.0 projects. Payload is a fullstack Next.js framework with a TypeScript-first config-based CMS.
</description>

<architecture>

Payload 3.0 = Next.js app + Payload config. Key concepts:

- **Collections** — groups of documents with shared schema (posts, users, media)
- **Globals** — singleton documents (nav, settings, footer)
- **Fields** — schema building blocks defining data structure
- **Hooks** — lifecycle callbacks (beforeChange, afterRead, etc.)
- **Access Control** — per-operation permission functions
- **Admin Panel** — auto-generated React UI at `/admin`
- **APIs** — auto-generated REST (`/api/{slug}`) + GraphQL + Local API

**Headless / decoupled topology:** Payload can run standalone as a backend API (REST/GraphQL) consumed by any frontend framework — not only co-located inside a Next.js app (e.g. a separate SvelteKit/Astro/Nuxt frontend fetching a deployed Payload Worker). In this pattern the Local API is unavailable from the frontend; all reads go through the REST/GraphQL API via `fetch`.

</architecture>

<scaffolding>

Run `bash scripts/scaffold.sh` from the skill directory to scaffold a project:

```bash
bash "$(dirname "$0")/../scripts/scaffold.sh" my-project --db postgres --dir /path/to/parent
```

Options: `--db mongodb|postgres` (default: mongodb), `--dir <path>` (default: cwd)

Creates a complete project structure:
```
my-project/
├── src/
│   ├── payload.config.ts      # Main config
│   ├── collections/           # Users.ts, Media.ts
│   ├── globals/               # Add globals here
│   ├── hooks/                 # Shared hooks
│   ├── access/                # Shared access functions
│   └── app/
│       ├── (payload)/         # Admin panel routes (auto-generated)
│       └── (frontend)/        # Your frontend
├── package.json
├── next.config.ts
├── tsconfig.json
└── .env.example
```

After scaffolding: `cp .env.example .env` → fill in `DATABASE_URL` + `PAYLOAD_SECRET` → `pnpm install` → `pnpm dev`

</scaffolding>

<generating>

## Generating Components

### Collection

```ts
import type { CollectionConfig } from 'payload'

export const Posts: CollectionConfig = {
  slug: 'posts',
  admin: { useAsTitle: 'title' },
  access: {
    read: () => true,
    create: ({ req: { user } }) => Boolean(user),
    update: ({ req: { user } }) => Boolean(user),
    delete: ({ req: { user } }) => user?.role === 'admin',
  },
  hooks: {
    beforeChange: [/* hooks */],
  },
  fields: [
    { name: 'title', type: 'text', required: true },
    { name: 'slug', type: 'text', required: true, unique: true, index: true },
    { name: 'content', type: 'richText' },
    { name: 'author', type: 'relationship', relationTo: 'users' },
    { name: 'status', type: 'select', options: ['draft', 'published'], defaultValue: 'draft' },
    { name: 'publishedAt', type: 'date' },
  ],
  versions: { drafts: true },
}
```

Then register in `payload.config.ts`: add to `collections` array + add import.

</generating>

<components>

### Global

```ts
import type { GlobalConfig } from 'payload'

export const Nav: GlobalConfig = {
  slug: 'nav',
  access: {
    read: () => true,
    update: ({ req: { user } }) => user?.role === 'admin',
  },
  fields: [
    {
      name: 'items',
      type: 'array',
      maxRows: 8,
      fields: [
        { name: 'label', type: 'text', required: true },
        { name: 'page', type: 'relationship', relationTo: 'pages', required: true },
      ],
    },
  ],
}
```

Register in `payload.config.ts`: add to `globals` array.

</components>

<auth>

### Auth Collection

```ts
export const Users: CollectionConfig = {
  slug: 'users',
  auth: true,  // enables login, JWT, password hashing
  admin: { useAsTitle: 'email' },
  access: {
    admin: ({ req: { user } }) => user?.role === 'admin',
  },
  fields: [
    { name: 'role', type: 'select', options: ['admin', 'editor', 'user'], defaultValue: 'user', required: true },
    { name: 'name', type: 'text' },
  ],
}
```

</auth>

<upload>

### Upload Collection

```ts
export const Media: CollectionConfig = {
  slug: 'media',
  upload: {
    mimeTypes: ['image/*', 'application/pdf'],
    imageSizes: [
      { name: 'thumbnail', width: 300, height: 300, position: 'centre' },
      { name: 'card', width: 768, height: 1024, position: 'centre' },
    ],
  },
  access: { read: () => true },
  fields: [
    { name: 'alt', type: 'text', required: true },
  ],
}
```

</upload>

<field_types>

## Field Types Quick Reference

Read `references/fields.md` for full field type reference with all options.

**Data**: text, textarea, number, email, code, json, date, point, checkbox, select, radio
**Relational**: relationship, upload, join
**Rich content**: richText (Lexical editor)
**Layout**: group, array, blocks, tabs, row, collapsible, ui

</field_types>

<hooks>

Read `references/hooks-and-access.md` for complete hook/access patterns.

Collection hooks execute in order:
`beforeOperation` → `beforeValidate` → `beforeChange` → DB write → `afterChange` → `afterOperation`

Key patterns:
- Auto-slug: `beforeChange` + generate from title
- Set author: `beforeChange` + `req.user.id` on create
- Publish date: `beforeChange` + set date when status changes to published
- Sync external: `afterChange` + fire-and-forget (no return)

</hooks>

<access_control>

Three levels: Collection → Global → Field. Each returns `boolean` or `Where` query.

```ts
// Public read, auth write, admin delete
access: {
  read: () => true,
  create: ({ req: { user } }) => Boolean(user),
  update: ({ req: { user } }) => Boolean(user),
  delete: ({ req: { user } }) => user?.role === 'admin',
}

// User sees only own docs
read: ({ req: { user } }) => {
  if (user?.role === 'admin') return true
  return { author: { equals: user?.id } }
}
```

</access_control>

<rest_api>

Read `references/rest-api.md` for complete API reference.

Base: `/api/{collection-slug}` — auto-generated CRUD + auth endpoints.
Query: `?where[status][equals]=published&sort=-createdAt&limit=10&depth=2`

</rest_api>

<mcp>

## MCP Server Integration

Read `references/mcp-setup.md` for full setup instructions.

Three options:
1. **ohnicholas93/payload-mcp-server** (Python) — live instance CRUD via REST, 11 stars
2. **Govcraft/payload-mcp** (TS) — type-aware code generation from Payload types
3. **Custom MCP server** — build your own REST wrapper (recommended for production)

</mcp>

<config_ref>

## Config Reference

```ts
import { buildConfig } from 'payload'

export default buildConfig({
  secret: process.env.PAYLOAD_SECRET,       // required
  db: mongooseAdapter({ url: '...' }),      // required: mongodb or postgres adapter
  collections: [],                           // CollectionConfig[]
  globals: [],                               // GlobalConfig[]
  editor: lexicalEditor(),                   // rich text editor
  admin: {
    user: 'users',                           // auth collection slug
    importMap: { baseDir: path.resolve(dirname) },
  },
  plugins: [],                               // Plugin[]
  sharp,                                     // image processing
  typescript: { outputFile: path.resolve(dirname, 'payload-types.ts') },
  // Optional:
  serverURL: 'https://example.com',
  cors: '*',
  localization: { locales: ['en', 'nl'], defaultLocale: 'en' },
  email: emailAdapter({ /* ... */ }),
  upload: { limits: { fileSize: 5000000 } },
  hooks: { afterError: [] },
  endpoints: [],
})
```

DB adapters:
- MongoDB: `@payloadcms/db-mongodb` → `mongooseAdapter({ url })`
- Postgres: `@payloadcms/db-postgres` → `postgresAdapter({ pool: { connectionString } })`
- Cloudflare D1/SQLite: `@payloadcms/db-d1-sqlite` → `sqliteD1Adapter({ binding, push, prodMigrations })` — requires a D1 binding from `@opennextjs/cloudflare` or wrangler's `getPlatformProxy`; no standard local dev DB pattern

</config_ref>

<best_practices>

- One collection per file in `src/collections/`
- One global per file in `src/globals/`
- Shared hooks in `src/hooks/`, shared access fns in `src/access/`
- Use `admin.useAsTitle` on every collection for readable admin labels
- Always set explicit access control — default requires auth for everything
- Use `versions: { drafts: true }` for content that needs review workflows
- Generate types with `pnpm generate:types` after schema changes
- Use Local API (`req.payload.find()`) in server components, REST API for client

</best_practices>
