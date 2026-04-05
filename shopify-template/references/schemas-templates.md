# Schemas & Templates

Source: Shopify/horizon cursor rules

## Schema Setting Types

**Input settings:** `text`, `textarea`, `number`, `range`, `color`, `checkbox`, `select`, `radio`, `collection`, `product`, `blog`, `page`, `image_picker`, `font_picker`, `video`, `richtext`

**Sidebar settings (informational):** `header`, `paragraph`

**Setting ID pattern:** `^[a-z][a-z0-9_]*$`
**Label max length:** 30 characters
**Block type pattern:** `^(@theme|@app|[a-z][a-z0-9_]*)$`

## Label Guidelines

- Keep concise (under 30 characters)
- Setting type provides context: "Columns" not "Number of columns"
- No verb-based labels for checkboxes
- Use title case: "Show Vendor"

## Setting Organization

1. **Resource Pickers First** — collection, product, blog, page
2. **Visual Impact Order** — layout, typography, colors, padding/margin
3. **Group with Headers:**

```json
{
  "type": "header",
  "content": "Layout"
}
```

## Translation Keys

- Schema names must use `'t:names.keyname'`
- Keys must exist in `locales/en.default.schema.json` under `names`
- If a key doesn't exist, add it

## Minimal Schema

```json
{
  "name": "t:names.section",
  "settings": [],
  "presets": [{ "name": "t:names.section" }]
}
```

## Conditional Visibility

```json
{
  "type": "text",
  "id": "custom_title",
  "label": "Custom title",
  "visible_if": "{{ show_custom_title }}"
}
```

## JSON Template Structure

```json
{
  "sections": {
    "header": { "type": "header" },
    "main": {
      "type": "main-product",
      "settings": { "show_vendor": true },
      "blocks": {
        "title": { "type": "title" },
        "price": { "type": "price", "settings": { "show_compare_at": true } }
      },
      "block_order": ["title", "price"]
    },
    "footer": { "type": "footer" }
  },
  "order": ["header", "main", "footer"]
}
```

**Standard template types:** `index.json`, `product.json`, `collection.json`, `page.json`, `blog.json`, `article.json`, `cart.json`, `search.json`

**Alternate templates:** `product.alternate.json`

## Theme Settings Schema (`config/settings_schema.json`)

```json
[
  {
    "name": "theme_info",
    "theme_name": "Theme Name",
    "theme_version": "1.0.0",
    "theme_author": "Author Name"
  },
  {
    "name": "Colors",
    "settings": [
      { "type": "header", "content": "Brand Colors" },
      { "type": "color", "id": "color_primary", "label": "Primary", "default": "#121212" }
    ]
  }
]
```

**Typography:** `font_picker`, `range` (12-72px), `select` (weights)
**Layout:** `range` (0-100px), `select`, `checkbox`
**Performance:** `checkbox` (lazy loading), `select` (image quality)
