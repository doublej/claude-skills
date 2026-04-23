# Schema Builder — Programmatic Schema Management

Three ways to manage a Directus schema, in order of complexity:

1. **Admin UI** — one-off changes, never in CI
2. **Snapshot / apply CLI** — reproducible between environments, YAML in git
3. **REST POST** to `/collections`, `/fields`, `/relations` — generated schemas, per-tenant schemas, CI-driven builds

This reference focuses on (2) and (3). Pattern (3) is lifted from the battle-tested `haist-cms/seed/lib/buildSchema.ts`.

---

## 1. Snapshot / apply

### Snapshot current schema to YAML

```bash
# Local binary
npx directus schema snapshot --yes ./snapshots/schema.yaml

# Inside Docker compose (haist-cms pattern)
docker compose exec directus npx directus schema snapshot --yes ./snapshots/schema.yaml
```

Commit `schema.yaml` to git.

### Apply in another environment

```bash
npx directus schema apply ./snapshots/schema.yaml
docker compose exec directus npx directus schema apply ./snapshots/schema.yaml
```

### Via SDK (for CI dashboards)

```ts
import { schemaSnapshot, schemaDiff, schemaApply } from '@directus/sdk'

const source = await sourceClient.request(schemaSnapshot())
const diff   = await targetClient.request(schemaDiff(source))
if (diff) await targetClient.request(schemaApply(diff))
```

When to use snapshot vs programmatic:
- **Snapshot**: schema was designed in the UI, same across environments
- **Programmatic**: schema is derived from code, generated per-tenant, or needs to be re-runnable with a single script

---

## 2. Programmatic schema via REST

### Idempotent POST wrapper (`safePost`)

Re-runnable scripts must tolerate "already exists" errors.

```ts
// lib/api.ts
type Json = Record<string, unknown>

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
    const e = new Error(`${method} ${path} → ${res.status}: ${first?.message ?? text}`) as Error & { code?: string }
    e.code = first?.extensions?.code
    throw e
  }
  return data
}

export const api = {
  get:    (path: string)             => request('GET', path),
  post:   (path: string, body: Json) => request('POST', path, body),
  patch:  (path: string, body: Json) => request('PATCH', path, body),
  delete: (path: string)             => request('DELETE', path),
}

export async function safePost(path: string, body: Json): Promise<void> {
  try {
    await api.post(path, body)
  } catch (e) {
    const err = e as Error & { code?: string }
    if (
      err.code === 'RECORD_NOT_UNIQUE' ||
      /already exists/i.test(err.message) ||
      /already has an associated/i.test(err.message)
    ) {
      return // idempotent — acceptable
    }
    throw e
  }
}
```

### Existence checks

```ts
async function collectionExists(name: string): Promise<boolean> {
  try { await api.get(`/collections/${name}`); return true }
  catch { return false }
}

async function fieldExists(collection: string, field: string): Promise<boolean> {
  try { await api.get(`/fields/${collection}/${field}`); return true }
  catch { return false }
}
```

---

## 3. Creating a collection (with UUID PK)

Directus does **not** auto-create a primary-key field when you POST a new collection via REST. You must include it in `fields`:

```ts
async function createCollection(spec: CollectionSpec): Promise<void> {
  if (await collectionExists(spec.collection)) return

  await safePost('/collections', {
    collection: spec.collection,
    meta: {
      singleton: spec.singleton ?? false,
      icon: spec.icon ?? 'box',
    },
    schema: {},
    fields: [
      {
        field: 'id',
        type: 'uuid',
        meta: {
          hidden: true,
          readonly: true,
          interface: 'input',
          special: ['uuid'],          // tells Directus to auto-generate
        },
        schema: { is_primary_key: true, has_auto_increment: false },
      },
    ],
  })
}
```

For integer PK with auto-increment (e.g., junction collections):

```ts
{
  field: 'id',
  type: 'integer',
  meta: { hidden: true, interface: 'input' },
  schema: { is_primary_key: true, has_auto_increment: true },
}
```

## 4. Adding fields

Call `POST /fields/<collection>` with `{ field, type, meta, schema }`.

```ts
function fieldPayload(f: FieldSpec) {
  return {
    field: f.field,
    type: f.type,
    meta: {
      interface: f.interface ?? 'input',
      special: f.special,
      options: f.options,
      required: f.required ?? false,
    },
    schema: { default_value: f.defaultValue ?? null, ...(f.schemaExtras ?? {}) },
  }
}

for (const f of spec.fields) {
  if (await fieldExists(spec.collection, f.field)) continue
  await safePost(`/fields/${spec.collection}`, fieldPayload(f))
}
```

### Field type reference

| Directus type | DB type | Common `interface` |
|---|---|---|
| `string` | varchar | `input`, `select-dropdown` |
| `text` | text | `input-multiline`, `input-rich-text-html` |
| `integer` | int | `input`, `slider` |
| `bigInteger` | bigint | `input` |
| `float` / `decimal` | numeric | `input` |
| `boolean` | boolean | `boolean` |
| `date` / `dateTime` / `timestamp` | — | `datetime` |
| `json` | json | `input-code`, `tags` |
| `uuid` | uuid | `input` (with `special: ['uuid']`) |
| `csv` | string | `tags` |
| `hash` | string | `input-hash` |
| `alias` | — | (used for relational aliases — O2M, M2M, M2A) |

`special` flags control auto-behavior: `['uuid']`, `['date-created']`, `['date-updated']`, `['user-created']`, `['user-updated']`, `['m2o']`, `['o2m']`, `['m2m']`, `['m2a']`, `['file']`, `['files']`.

---

## 5. Relations — O2M recipe (3 steps)

An O2M (parent has many children) is implemented as an **M2O on the child** with an **alias field on the parent**. Three POSTs.

```ts
async function createO2MRelation(rel: {
  parent: string
  parentField: string   // alias field name on parent
  child: string
  childField: string    // FK field name on child
}): Promise<void> {
  // 1. FK field on the child (uuid M2O → parent)
  if (!(await fieldExists(rel.child, rel.childField))) {
    await safePost(`/fields/${rel.child}`, {
      field: rel.childField,
      type: 'uuid',
      meta: { interface: 'select-dropdown-m2o', special: ['m2o'] },
      schema: {},
    })
  }

  // 2. Alias field on the parent (O2M)
  if (!(await fieldExists(rel.parent, rel.parentField))) {
    await safePost(`/fields/${rel.parent}`, {
      field: rel.parentField,
      type: 'alias',
      meta: {
        interface: 'list-o2m',
        special: ['o2m'],
        options: { enableSelect: false },
      },
    })
  }

  // 3. The relation itself
  await safePost('/relations', {
    collection: rel.child,
    field: rel.childField,
    related_collection: rel.parent,
    meta: {
      one_field: rel.parentField,
      sort_field: 'sort',
      one_collection_field: null,
      one_allowed_collections: null,
      junction_field: null,
    },
    schema: { on_delete: 'CASCADE' },
  })
}
```

---

## 6. Relations — M2A recipe (5 steps)

Many-to-Any lets a parent link to items from several different collections. Implemented with a junction collection carrying `{ parent_fk, item, collection, sort }`.

```ts
const BLOCK_COLLECTIONS = ['block_hero', 'block_text', 'block_image'] as const

async function createM2ARelation(rel: {
  parent: string
  parentField: string    // alias on parent, e.g. 'blocks'
  junction: string       // e.g. 'pages_blocks'
  parentFkField: string  // e.g. 'pages_id'
}): Promise<void> {
  // 1. Junction collection with integer PK
  if (!(await collectionExists(rel.junction))) {
    await safePost('/collections', {
      collection: rel.junction,
      meta: { hidden: true, icon: 'import_export' },
      schema: {},
      fields: [
        {
          field: 'id',
          type: 'integer',
          meta: { hidden: true, interface: 'input' },
          schema: { is_primary_key: true, has_auto_increment: true },
        },
      ],
    })
  }

  // 2. Junction fields: parent_fk, item, collection, sort
  if (!(await fieldExists(rel.junction, rel.parentFkField))) {
    await safePost(`/fields/${rel.junction}`, {
      field: rel.parentFkField,
      type: 'uuid',
      meta: { interface: 'select-dropdown-m2o', special: ['m2o'] },
      schema: {},
    })
  }
  if (!(await fieldExists(rel.junction, 'item'))) {
    await safePost(`/fields/${rel.junction}`, {
      field: 'item',
      type: 'string',
      meta: { interface: 'select-dropdown-m2a', special: ['m2a'] },
      schema: {},
    })
  }
  if (!(await fieldExists(rel.junction, 'collection'))) {
    await safePost(`/fields/${rel.junction}`, {
      field: 'collection',
      type: 'string',
      meta: { interface: 'select-dropdown', hidden: true },
      schema: {},
    })
  }
  if (!(await fieldExists(rel.junction, 'sort'))) {
    await safePost(`/fields/${rel.junction}`, {
      field: 'sort',
      type: 'integer',
      meta: { interface: 'input', hidden: true },
      schema: {},
    })
  }

  // 3. Alias field on the parent
  if (!(await fieldExists(rel.parent, rel.parentField))) {
    await safePost(`/fields/${rel.parent}`, {
      field: rel.parentField,
      type: 'alias',
      meta: {
        interface: 'list-m2a',
        special: ['m2a'],
        options: { enableSelect: false },
      },
    })
  }

  // 4. Relation: junction.parent_fk → parent
  await safePost('/relations', {
    collection: rel.junction,
    field: rel.parentFkField,
    related_collection: rel.parent,
    meta: {
      one_field: rel.parentField,
      sort_field: 'sort',
      one_collection_field: null,
      one_allowed_collections: null,
      junction_field: 'item',
    },
    schema: { on_delete: 'CASCADE' },
  })

  // 5. Relation: junction.item ↔ allowed collections (M2A side)
  await safePost('/relations', {
    collection: rel.junction,
    field: 'item',
    related_collection: null,
    meta: {
      one_collection_field: 'collection',
      one_allowed_collections: [...BLOCK_COLLECTIONS],
      sort_field: 'sort',
      junction_field: rel.parentFkField,
    },
    schema: null,
  })
}
```

## 7. M2M recipe

Standard junction with two M2O fks. Three field POSTs + one relation on each side:

```ts
// articles_tags junction
await safePost('/collections', {
  collection: 'articles_tags',
  meta: { hidden: true },
  schema: {},
  fields: [{
    field: 'id', type: 'integer',
    meta: { hidden: true }, schema: { is_primary_key: true, has_auto_increment: true },
  }],
})
await safePost('/fields/articles_tags', { field: 'articles_id', type: 'uuid', meta: { special: ['m2o'] }, schema: {} })
await safePost('/fields/articles_tags', { field: 'tags_id',     type: 'uuid', meta: { special: ['m2o'] }, schema: {} })

// Alias on articles
await safePost('/fields/articles', {
  field: 'tags', type: 'alias',
  meta: { interface: 'list-m2m', special: ['m2m'] },
})

// Relations (articles side)
await safePost('/relations', {
  collection: 'articles_tags', field: 'articles_id',
  related_collection: 'articles',
  meta: { one_field: 'tags', junction_field: 'tags_id', sort_field: null },
  schema: { on_delete: 'CASCADE' },
})
// Relations (tags side)
await safePost('/relations', {
  collection: 'articles_tags', field: 'tags_id',
  related_collection: 'tags',
  meta: { one_field: null, junction_field: 'articles_id' },
  schema: { on_delete: 'CASCADE' },
})
```

---

## 8. Order of operations

When building from scratch:

1. **Collections first** (each with its id field)
2. **Regular fields** (strings, bools, json, etc.)
3. **O2M/M2O relations** (creates FK fields + aliases + `/relations` rows)
4. **M2M relations** (junction + FKs + two relation rows)
5. **M2A relations** (junction + polymorphic + two relation rows)
6. **Seed data** (items come last — relations must exist first)

Wrap step 3+ in `try { ... } catch (e) { if (/already exists/i.test(e.message)) continue; throw e }` to keep the script re-runnable.

## 9. Idempotent seed pattern (delete-then-create)

For items with a stable slug, the haist-cms `seed.ts` uses delete-then-create:

```ts
async function deletePageBySlug(slug: string): Promise<void> {
  const res = (await api.get(`/items/pages?filter[slug][_eq]=${slug}&fields=id`)) as { data?: { id: string }[] } | null
  for (const p of res?.data ?? []) {
    await api.delete(`/items/pages/${p.id}`)
  }
}

async function seedPage(slug: string): Promise<void> {
  const payload = await buildPayload(slug)
  await deletePageBySlug(slug)
  await api.post('/items/pages', payload)
}
```

This replaces the row cleanly on every run — simpler than diffing.

## 10. Clearing the schema cache

After a programmatic schema change, an already-initialized SDK client must drop its cached schema:

```ts
directus.reset()
```

Or re-instantiate the client.
