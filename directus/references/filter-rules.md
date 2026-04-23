# Filter Rules

Directus uses a JSON filter language for REST, SDK, GraphQL (via the `_filter` arg), permissions, and flows. Shape: `{ <field>: { <operator>: <value> } }` with `_and` / `_or` for logic.

## Operators

### Equality & comparison

| Operator | Meaning | Example |
|---|---|---|
| `_eq` | Equal | `{ status: { _eq: 'published' } }` |
| `_neq` | Not equal | `{ status: { _neq: 'draft' } }` |
| `_lt` | Less than | `{ age: { _lt: 18 } }` |
| `_lte` | ≤ | `{ age: { _lte: 17 } }` |
| `_gt` | Greater than | `{ price: { _gt: 100 } }` |
| `_gte` | ≥ | `{ price: { _gte: 100 } }` |
| `_between` | Between (inclusive, array) | `{ price: { _between: [10, 50] } }` |
| `_nbetween` | Not between | `{ price: { _nbetween: [10, 50] } }` |

### Sets

| Operator | Example |
|---|---|
| `_in` | `{ status: { _in: ['published', 'draft'] } }` |
| `_nin` | `{ status: { _nin: ['archived'] } }` |

### Null / empty

| Operator | Example |
|---|---|
| `_null` | `{ deleted_at: { _null: true } }` |
| `_nnull` | `{ image: { _nnull: true } }` |
| `_empty` | `{ tags: { _empty: true } }` (string or array) |
| `_nempty` | `{ tags: { _nempty: true } }` |

### String matching

| Operator | Case | Example |
|---|---|---|
| `_contains` | sensitive | `{ title: { _contains: 'hello' } }` |
| `_icontains` | insensitive | `{ title: { _icontains: 'Hello' } }` |
| `_ncontains` | sensitive, negated | |
| `_starts_with` | sensitive | `{ slug: { _starts_with: 'blog-' } }` |
| `_istarts_with` | insensitive | |
| `_ends_with` | sensitive | `{ email: { _ends_with: '@acme.com' } }` |
| `_iends_with` | insensitive | |
| `_regex` | regex match | `{ phone: { _regex: '^\\+31' } }` |

### Geo (for spatial fields)

| Operator | Example |
|---|---|
| `_intersects` | `{ area: { _intersects: geojson } }` |
| `_nintersects` | |
| `_intersects_bbox` | bounding box |
| `_nintersects_bbox` | |

### Relational quantifiers (O2M / M2M / M2A)

| Operator | Meaning |
|---|---|
| `_some` | **Any** related item matches |
| `_none` | **Zero** related items match |

```ts
// Posts that have at least one approved comment
filter: { comments: { _some: { approved: { _eq: true } } } }

// Posts with no comments at all
filter: { comments: { _none: {} } }
```

## Logical grouping

`_and` is implicit at the top level. Use explicit `_and` / `_or` when mixing.

```ts
filter: {
  _and: [
    { status: { _eq: 'published' } },
    {
      _or: [
        { featured: { _eq: true } },
        { views: { _gt: 1000 } },
      ],
    },
  ],
}
```

## Nested field paths (M2O / deep)

Dot notation traverses M2O relations transparently.

```ts
// Posts where author.country.code === 'NL'
filter: { author: { country: { code: { _eq: 'NL' } } } }

// Equivalent — flattened is NOT valid; always nest by relation
```

## Dynamic variables

Usable anywhere a value is expected.

| Variable | Meaning |
|---|---|
| `$CURRENT_USER` | ID of the authenticated user |
| `$CURRENT_ROLE` | ID of the user's role |
| `$CURRENT_POLICIES` | Policy IDs (Directus 11+) |
| `$NOW` | Current timestamp |
| `$NOW(+7 days)` | Offset — `+N days`, `-N hours`, etc. |

```ts
// My own drafts from the last 7 days
filter: {
  _and: [
    { user_created: { _eq: '$CURRENT_USER' } },
    { status: { _eq: 'draft' } },
    { date_created: { _gte: '$NOW(-7 days)' } },
  ],
}
```

## Common recipes

### "Published and scheduled in the past"

```ts
filter: {
  _and: [
    { status: { _eq: 'published' } },
    { publish_at: { _lte: '$NOW' } },
  ],
}
```

### "Mine OR assigned to me"

```ts
filter: {
  _or: [
    { user_created: { _eq: '$CURRENT_USER' } },
    { assignees: { directus_users_id: { _eq: '$CURRENT_USER' } } },
  ],
}
```

### Search across multiple fields

Use the top-level `search` param instead of filter for full-text:

```ts
readItems('posts', { search: 'hello', fields: ['*'] })
```

Directus searches string fields automatically. For targeted multi-field match, combine `_or`:

```ts
filter: {
  _or: [
    { title: { _icontains: q } },
    { body:  { _icontains: q } },
    { slug:  { _icontains: q } },
  ],
}
```

### Exclude soft-deleted

```ts
filter: { deleted_at: { _null: true } }
```

### Permission-style filter (used in Policies)

Same syntax, applied per-role in Settings → Access Policies → Collection Permissions → Custom.

```json
{ "user_created": { "_eq": "$CURRENT_USER" } }
```

## REST query-string form

For raw REST without the SDK:

```
GET /items/posts
  ?filter[status][_eq]=published
  &filter[date_published][_lte]=$NOW
  &fields=id,title,author.name
  &sort=-date_published
  &limit=10
```

For complex filters, prefer JSON body via POST to `/items/<collection>/query` or use the SDK.

## Pitfalls

- **Empty filter**: `{}` matches **everything**. In O2M quantifiers, `_none: {}` means "no related items at all".
- **Dates**: use ISO-8601 strings (`'2026-04-06T00:00:00Z'`) or dynamic vars (`$NOW`). Plain `new Date()` in JSON serializes to ISO, which works.
- **Boolean strings vs booleans**: `{ published: { _eq: true } }` — pass the native boolean, not `'true'`.
- **Filtering by nested relational count**: not supported directly. Use `_some` or compute via a flow / endpoint.
- **Case sensitivity** depends on the database and collation. Use `_icontains` / `_istarts_with` to be explicit.
