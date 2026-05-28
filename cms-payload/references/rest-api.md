# Payload CMS 3.0 REST API Reference

Base path: `/api` (configurable via `routes.api`)

## Collections

All routes use the collection `slug` (kebab-case).

| Operation | Method | Path | Body |
|-----------|--------|------|------|
| Find | GET | `/api/{slug}` | - |
| Find by ID | GET | `/api/{slug}/{id}` | - |
| Count | GET | `/api/{slug}/count` | - |
| Create | POST | `/api/{slug}` | Document data |
| Update by ID | PATCH | `/api/{slug}/{id}` | Partial data |
| Update many | PATCH | `/api/{slug}?where[field][equals]=value` | Partial data |
| Delete by ID | DELETE | `/api/{slug}/{id}` | - |
| Delete many | DELETE | `/api/{slug}?where[field][equals]=value` | - |

## Globals

| Operation | Method | Path |
|-----------|--------|------|
| Get | GET | `/api/globals/{slug}` |
| Update | POST | `/api/globals/{slug}` |

## Query Parameters

| Param | Example | Description |
|-------|---------|-------------|
| `depth` | `?depth=2` | Populate relationships N levels deep |
| `locale` | `?locale=en` | Retrieve in specific locale |
| `fallback-locale` | `?fallback-locale=en` | Fallback if locale missing |
| `select` | `?select[title]=true` | Include only specified fields |
| `populate` | `?populate[author][select][name]=true` | Control populated field selection |
| `limit` | `?limit=25` | Results per page (default 10) |
| `page` | `?page=2` | Pagination page number |
| `sort` | `?sort=-createdAt` | Sort field (prefix `-` for desc) |
| `where` | see below | Filter documents |

## Where Queries

```
?where[field][operator]=value
```

| Operator | Description |
|----------|-------------|
| `equals` | Exact match |
| `not_equals` | Not equal |
| `greater_than` | > |
| `greater_than_equal` | >= |
| `less_than` | < |
| `less_than_equal` | <= |
| `like` | Case-insensitive contains |
| `contains` | Contains substring |
| `in` | Value in comma-separated list |
| `not_in` | Value not in list |
| `exists` | Field exists (true/false) |
| `near` | Geo near (point fields) |

### Compound queries
```
?where[or][0][status][equals]=published&where[or][1][featured][equals]=true
?where[and][0][status][equals]=published&where[and][1][author][equals]=123
```

## Auth Endpoints (auth-enabled collections)

| Operation | Method | Path |
|-----------|--------|------|
| Login | POST | `/api/{slug}/login` |
| Logout | POST | `/api/{slug}/logout` |
| Me | GET | `/api/{slug}/me` |
| Refresh | POST | `/api/{slug}/refresh-token` |
| Forgot Password | POST | `/api/{slug}/forgot-password` |
| Reset Password | POST | `/api/{slug}/reset-password` |
| Verify Email | POST | `/api/{slug}/verify/{token}` |
| Unlock | POST | `/api/{slug}/unlock` |

## Custom Endpoints

```ts
import type { CollectionConfig } from 'payload'

export const Posts: CollectionConfig = {
  slug: 'posts',
  endpoints: [
    {
      path: '/custom-route',
      method: 'get',
      handler: async (req) => {
        const docs = await req.payload.find({ collection: 'posts', limit: 5 })
        return Response.json(docs)
      },
    },
  ],
  fields: [],
}
```

## Response Formats

### Find (paginated)
```json
{
  "docs": [...],
  "totalDocs": 100,
  "limit": 10,
  "totalPages": 10,
  "page": 1,
  "pagingCounter": 1,
  "hasPrevPage": false,
  "hasNextPage": true,
  "prevPage": null,
  "nextPage": 2
}
```

### Create / Update
```json
{
  "message": "Successfully created.",
  "doc": { ... }
}
```

## Payload SDK (REST client)

```ts
import { getPayload } from '@payloadcms/next/utilities'
import config from '@payload-config'

// Server-side (Local API, preferred in Next.js)
const payload = await getPayload({ config })
const posts = await payload.find({ collection: 'posts', limit: 10 })

// Client-side REST
const res = await fetch('/api/posts?limit=10&sort=-createdAt')
const data = await res.json()
```
