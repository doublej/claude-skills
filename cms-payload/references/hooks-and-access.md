# Payload CMS 3.0 Hooks & Access Control Reference

## Collection Hooks

```ts
import type { CollectionConfig } from 'payload'

export const Posts: CollectionConfig = {
  slug: 'posts',
  hooks: {
    beforeOperation: [(args) => { /* args: { args, operation, req } */ }],
    beforeValidate: [(args) => { /* args: { data, originalDoc, operation, req } → return data */ }],
    beforeChange: [(args) => { /* args: { data, originalDoc, operation, req } → return data */ }],
    beforeRead: [(args) => { /* args: { doc, query, req } */ }],
    beforeDelete: [(args) => { /* args: { id, req } */ }],
    afterChange: [(args) => { /* args: { doc, previousDoc, operation, req } */ }],
    afterRead: [(args) => { /* args: { doc, req } → return doc */ }],
    afterDelete: [(args) => { /* args: { doc, id, req } */ }],
    afterOperation: [(args) => { /* args: { operation, result, req } → return result */ }],
    afterError: [(args) => { /* args: { error, req } */ }],
  },
  fields: [],
}
```

### Auth-only hooks
```ts
hooks: {
  beforeLogin: [(args) => { /* args: { user, req } */ }],
  afterLogin: [(args) => { /* args: { user, token, req } */ }],
  afterLogout: [(args) => { /* args: { req } */ }],
  afterRefresh: [(args) => { /* args: { token, req } */ }],
  afterMe: [(args) => { /* args: { response, req } */ }],
  afterForgotPassword: [(args) => { /* args: { args, req } */ }],
}
```

## Common Hook Patterns

### Auto-populate slug
```ts
const generateSlug: CollectionBeforeChangeHook = async ({ data, operation }) => {
  if (operation === 'create' && data?.title && !data.slug) {
    data.slug = data.title.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')
  }
  return data
}
```

### Set author on create
```ts
const setAuthor: CollectionBeforeChangeHook = async ({ data, req, operation }) => {
  if (operation === 'create' && req.user) {
    data.author = req.user.id
  }
  return data
}
```

### Publish date
```ts
const setPublishDate: CollectionBeforeChangeHook = async ({ data, originalDoc }) => {
  if (data?.status === 'published' && originalDoc?.status !== 'published') {
    data.publishedAt = new Date().toISOString()
  }
  return data
}
```

## Global Hooks

```ts
import type { GlobalConfig } from 'payload'

export const Settings: GlobalConfig = {
  slug: 'settings',
  hooks: {
    beforeValidate: [(args) => { /* → return data */ }],
    beforeChange: [(args) => { /* → return data */ }],
    beforeRead: [(args) => { /* */ }],
    afterChange: [(args) => { /* */ }],
    afterRead: [(args) => { /* → return doc */ }],
  },
  fields: [],
}
```

## Field Hooks

```ts
{
  name: 'price',
  type: 'number',
  hooks: {
    beforeValidate: [({ value, data }) => { return value }],
    beforeChange: [({ value, previousValue, data }) => { return value }],
    afterChange: [({ value, previousValue, data }) => { /* side effects */ }],
    afterRead: [({ value, data }) => { return value }],
  },
}
```

---

## Access Control

### Collection Access
```ts
export const Posts: CollectionConfig = {
  slug: 'posts',
  access: {
    create: ({ req: { user } }) => Boolean(user),
    read: () => true,  // public
    update: ({ req: { user } }) => Boolean(user),
    delete: ({ req: { user } }) => user?.role === 'admin',
    // Auth collections only:
    admin: ({ req: { user } }) => user?.role === 'admin',
    unlock: ({ req: { user } }) => user?.role === 'admin',
    // Version-enabled only:
    readVersions: ({ req: { user } }) => Boolean(user),
  },
  fields: [],
}
```

### Where-based access (filter results per user)
```ts
read: ({ req: { user } }) => {
  if (!user) return false
  if (user.role === 'admin') return true
  // Regular users only see their own
  return { author: { equals: user.id } }
}
```

### Global Access
```ts
export const Settings: GlobalConfig = {
  slug: 'settings',
  access: {
    read: () => true,
    update: ({ req: { user } }) => user?.role === 'admin',
    readVersions: ({ req: { user } }) => user?.role === 'admin',
  },
  fields: [],
}
```

### Field-Level Access
```ts
{
  name: 'internalNotes',
  type: 'textarea',
  access: {
    create: ({ req: { user } }) => user?.role === 'admin',
    read: ({ req: { user } }) => user?.role === 'admin',
    update: ({ req: { user } }) => user?.role === 'admin',
  },
}
```

## Common Access Patterns

### Role-based (RBAC)
```ts
const isAdmin = ({ req: { user } }: { req: { user: any } }) =>
  user?.role === 'admin'

const isAdminOrSelf = ({ req: { user }, id }: { req: { user: any }; id?: string }) =>
  user?.role === 'admin' || user?.id === id
```

### Organization-scoped
```ts
const sameOrg = ({ req: { user } }) => {
  if (!user) return false
  if (user.role === 'admin') return true
  return { organization: { equals: user.organization } }
}
```
