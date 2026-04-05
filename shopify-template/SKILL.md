---
name: shopify-template
description: "Liquid theme development: sections, blocks, schemas, snippets, localization"
---

# Shopify Template Development

Build Shopify Online Store 2.0 themes following official patterns from Shopify's Horizon theme.

## Architecture

```
theme/
├── assets/          # CSS, JS, images (flat, no subdirs)
├── blocks/          # Theme blocks (.liquid)
├── config/          # settings_schema.json, settings_data.json
├── layout/          # theme.liquid
├── locales/         # en.default.json, en.default.schema.json
├── sections/        # Section files (.liquid)
├── snippets/        # Reusable snippet files (.liquid)
└── templates/       # JSON templates (product.json, etc.)
```

## Critical Rules

1. **Never invent Liquid filters, tags, or objects** — only use what exists in Shopify's Liquid
2. **Use `{% liquid %}` blocks** for multiline logic
3. **Every user-facing text** must use `{{ 'key' | t }}` translation filter
4. **Always include `{{ block.shopify_attributes }}`** on block root elements
5. **Single `{% content_for 'blocks' %}` per file** — capture first if needed in multiple places
6. **Schema names use translation keys:** `"name": "t:names.section_name"`
7. **BEM naming** for CSS classes: `.block__element--modifier`
8. **Zero JS dependencies** — native browser APIs + Web Components only
9. **Inline CSS variables** via `style` attribute for section/block scoping
10. **Escape user content:** `{{ variable | escape }}`

## Reference Files

Load as needed based on the task:

| File | When to load |
|------|-------------|
| `references/liquid-syntax.md` | Writing Liquid: tags, filters, `{% doc %}`, inline variables |
| `references/sections-blocks.md` | Creating sections or blocks, nested blocks, static blocks |
| `references/schemas-templates.md` | Schema settings, JSON templates, theme settings |
| `references/snippets-assets.md` | Creating snippets, working with assets |
| `references/css-conventions.md` | Writing CSS: BEM, variables, specificity, nesting, scoping |
| `references/js-conventions.md` | Writing JS: Web Components, events, AbortController |
| `references/html-accessibility.md` | HTML patterns, a11y, localization |

## Quick Patterns

### New Section

```liquid
<section
  id="SectionName-{{ section.id }}"
  class="section-name"
  style="--padding-top: {{ section.settings.padding_top }}px; --padding-bottom: {{ section.settings.padding_bottom }}px;"
>
  <div class="page-width">
    {% content_for 'blocks' %}
  </div>
</section>

{% stylesheet %}
.section-name {
  padding-top: var(--padding-top, 40px);
  padding-bottom: var(--padding-bottom, 40px);
}
{% endstylesheet %}

{% schema %}
{
  "name": "t:names.section_name",
  "tag": "section",
  "blocks": [{ "type": "@theme" }, { "type": "@app" }],
  "settings": [
    { "type": "range", "id": "padding_top", "label": "t:settings.padding_top", "min": 0, "max": 100, "default": 40, "unit": "px" },
    { "type": "range", "id": "padding_bottom", "label": "t:settings.padding_bottom", "min": 0, "max": 100, "default": 40, "unit": "px" }
  ],
  "presets": [{ "name": "t:names.section_name" }]
}
{% endschema %}
```

### New Block

```liquid
{% doc %}
  Block description
  @param {string} heading - Block heading
  @example
  {% content_for 'block', type: 'block-name', id: 'unique-id' %}
{% enddoc %}

<div {{ block.shopify_attributes }} class="block-name">
  {% if block.settings.heading != blank %}
    <h3 class="block-name__heading">{{ block.settings.heading | escape }}</h3>
  {% endif %}
  {% content_for 'blocks' %}
</div>

{% stylesheet %}
.block-name { padding: var(--block-padding, 1rem); }
{% endstylesheet %}

{% schema %}
{
  "name": "t:names.block_name",
  "settings": [
    { "type": "text", "id": "heading", "label": "t:settings.heading" }
  ],
  "presets": [{ "name": "t:names.block_name" }]
}
{% endschema %}
```

### New Snippet

```liquid
{% doc %}
  Snippet description
  @param {object} product - Product object (required)
  @param {boolean} [show_vendor] - Show vendor (default: false)
  @example
  {% render 'snippet-name', product: product, show_vendor: true %}
{% enddoc %}

{% liquid
  assign product = product | default: empty
  assign show_vendor = show_vendor | default: false
  unless product != empty
    echo '<!-- Error: product required -->'
    break
  endunless
%}

<div class="snippet-name">
  {{ product.title | escape }}
</div>
```

## Validation

Run theme-check for linting:

```bash
bash scripts/theme-check.sh /path/to/theme
bash scripts/theme-check.sh /path/to/theme --auto-correct
```

Requires: `npm install -g @shopify/cli @shopify/theme` or `gem install theme-check`

## Shopify CLI Commands

```bash
shopify theme dev              # Start dev server with hot reload
shopify theme push             # Push to store
shopify theme pull             # Pull from store
shopify theme check            # Lint theme
shopify theme share            # Create preview link
shopify theme info             # Show theme info
```

## Related Skills

- **shopify-api** — Admin REST/GraphQL API operations
- **shopify-data** — Product data modeling (options, variants, metafields, collections)
