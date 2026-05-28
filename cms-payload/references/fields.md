# Payload CMS 3.0 Field Types Reference

## Data Fields

### text
```ts
{ name: 'title', type: 'text', required: true, unique: true, minLength: 1, maxLength: 200 }
```

### textarea
```ts
{ name: 'bio', type: 'textarea', maxLength: 1000 }
```

### number
```ts
{ name: 'price', type: 'number', min: 0, max: 99999, hasMany: false }
```

### email
```ts
{ name: 'contact', type: 'email' }
```

### code
```ts
{ name: 'snippet', type: 'code', admin: { language: 'typescript' } }
```

### json
```ts
{ name: 'metadata', type: 'json', jsonSchema: { /* optional JSON Schema */ } }
```

### date
```ts
{ name: 'publishedAt', type: 'date', admin: { date: { pickerAppearance: 'dayAndTime' } } }
```

### point
```ts
{ name: 'location', type: 'point' }  // [longitude, latitude]
```

### checkbox
```ts
{ name: 'isPublished', type: 'checkbox', defaultValue: false }
```

### select
```ts
{
  name: 'status',
  type: 'select',
  options: [
    { label: 'Draft', value: 'draft' },
    { label: 'Published', value: 'published' },
  ],
  defaultValue: 'draft',
  hasMany: false, // true for multi-select
}
```

### radio
```ts
{
  name: 'color',
  type: 'radio',
  options: [
    { label: 'Red', value: 'red' },
    { label: 'Blue', value: 'blue' },
  ],
}
```

## Relational Fields

### relationship
```ts
{
  name: 'author',
  type: 'relationship',
  relationTo: 'users',          // single collection
  hasMany: false,
  // OR polymorphic:
  // relationTo: ['users', 'orgs'],
}
```

### upload
```ts
{
  name: 'image',
  type: 'upload',
  relationTo: 'media',
}
```

### join
```ts
{
  name: 'posts',
  type: 'join',
  collection: 'posts',
  on: 'author',  // the relationship field on posts pointing back
}
```

## Rich Text

### richText
```ts
{
  name: 'content',
  type: 'richText',
  // Uses editor from config (lexicalEditor by default)
}
```

## Layout / Structural Fields (no data stored)

### group
```ts
{
  name: 'seo',
  type: 'group',
  fields: [
    { name: 'title', type: 'text' },
    { name: 'description', type: 'textarea' },
  ],
}
```

### array
```ts
{
  name: 'links',
  type: 'array',
  minRows: 1,
  maxRows: 10,
  fields: [
    { name: 'label', type: 'text', required: true },
    { name: 'url', type: 'text', required: true },
  ],
}
```

### blocks
```ts
{
  name: 'layout',
  type: 'blocks',
  blocks: [
    {
      slug: 'hero',
      fields: [
        { name: 'heading', type: 'text', required: true },
        { name: 'image', type: 'upload', relationTo: 'media' },
      ],
    },
    {
      slug: 'content',
      fields: [
        { name: 'richText', type: 'richText' },
      ],
    },
  ],
}
```

### tabs
```ts
{
  type: 'tabs',
  tabs: [
    {
      label: 'Content',
      fields: [{ name: 'title', type: 'text' }],
    },
    {
      label: 'SEO',
      fields: [{ name: 'metaTitle', type: 'text' }],
    },
  ],
}
```

### row
```ts
{
  type: 'row',
  fields: [
    { name: 'city', type: 'text' },
    { name: 'state', type: 'text' },
  ],
}
```

### collapsible
```ts
{
  type: 'collapsible',
  label: 'Advanced',
  fields: [{ name: 'customCSS', type: 'code' }],
}
```

### ui
```ts
{
  name: 'myCustomUI',
  type: 'ui',
  admin: {
    components: {
      Field: '/path/to/CustomField',
      Cell: '/path/to/CustomCell',
    },
  },
}
```

## Common Field Properties

All fields support:
- `name` (required for data fields)
- `label` - admin display label
- `required` - boolean
- `unique` - boolean (adds DB unique constraint)
- `index` - boolean (adds DB index)
- `defaultValue` - static value or function
- `validate` - custom validation function
- `access` - field-level access control `{ create, read, update }`
- `hooks` - field-level hooks `{ beforeValidate, beforeChange, afterChange, afterRead }`
- `admin` - admin UI config `{ condition, description, readOnly, hidden, width, position }`
- `localized` - boolean (requires localization in config)
- `saveToJWT` - boolean (for auth collections)
- `custom` - extension point for plugins
