# Sections & Blocks

Source: Shopify/horizon cursor rules

## Section Structure

Every section must include: `{% schema %}` with valid JSON, semantic HTML, CSS scoping, translation keys.

```liquid
{% liquid
  assign section_id = section.settings.custom_id | default: section.id
  assign section_class = 'section-' | append: section.type
%}

<section
  id="{{ section_id }}"
  class="{{ section_class }}"
  style="
    --section-padding-top: {{ section.settings.padding_top }}px;
    --section-padding-bottom: {{ section.settings.padding_bottom }}px;
  "
>
  <div class="page-width">
    {% content_for 'blocks' %}
  </div>
</section>

{% stylesheet %}
.{{ section_class }} {
  padding-top: var(--section-padding-top, 40px);
  padding-bottom: var(--section-padding-bottom, 40px);
}
{% endstylesheet %}

{% schema %}
{
  "name": "t:names.section_name",
  "tag": "section",
  "class": "section-name",
  "blocks": [
    {"type": "@theme"},
    {"type": "@app"}
  ],
  "settings": [...],
  "presets": [{"name": "t:names.section_name"}]
}
{% endschema %}
```

## Block Structure

Blocks are reusable components: nestable under sections/blocks, configurable in theme editor.

```liquid
{% doc %}
  Block description
  @example
  {% content_for 'block', type: 'block-name', id: 'unique-id' %}
{% enddoc %}

<div {{ block.shopify_attributes }} class='block-name'>
  <!-- Block content -->
</div>

{% stylesheet %}
.block-name { padding: var(--block-padding, 1rem); }
{% endstylesheet %}

{% schema %}
{
  "name": "Block Name",
  "settings": [],
  "presets": []
}
{% endschema %}
```

**Block Properties:**
- `{{ block.id }}` — unique identifier
- `{{ block.type }}` — block type name
- `{{ block.shopify_attributes }}` — **required** for theme editor
- `{{ block.settings.text }}` — access settings

## Static Blocks

Rendered directly in templates by developers (not dynamically added through editor):

```liquid
{% content_for 'block', type: 'breadcrumb', id: 'product-breadcrumb' %}

{% content_for 'block', type: 'product-gallery', id: 'main-gallery', settings: {
  enable_zoom: true,
  thumbnails_position: "bottom"
} %}
```

- Fixed `id` makes them identifiable in editor
- Appear as locked blocks (can't be removed/reordered)
- Mix with dynamic areas: `{% content_for 'blocks' %}`

## Nested Blocks

**Critical: Single `content_for 'blocks'` Per File**

```liquid
<!-- CORRECT: capture once, use multiple times -->
{% capture blocks_content %}{% content_for 'blocks' %}{% endcapture %}

{% if condition %}
  <div class='layout-a'>{{ blocks_content }}</div>
{% else %}
  <div class='layout-b'>{{ blocks_content }}</div>
{% endif %}

<!-- WRONG: duplicate content_for causes errors -->
{% if condition %}
  {% content_for 'blocks' %}
{% else %}
  {% content_for 'blocks' %}  <!-- ERROR -->
{% endif %}
```

**Nested Blocks with Layout:**
```liquid
<div
  class='group {{ block.settings.layout_direction }}'
  style='--gap: {{ block.settings.gap }}px;'
  {{ block.shopify_attributes }}
>
  {% content_for 'blocks' %}
</div>
```

**Presets with nested blocks using object notation need `block_order`:**
```json
{
  "blocks": {
    "header": {
      "type": "group",
      "blocks": {
        "title": { "type": "product-title" },
        "price": { "type": "price" }
      },
      "block_order": ["title", "price"]
    }
  }
}
```

## Block Targeting

```json
{
  "blocks": [
    { "type": "@theme" },
    { "type": "@app" }
  ]
}
```

Restricted:
```json
{
  "blocks": [
    { "type": "text", "name": "Text Content" },
    { "type": "image", "name": "Image Content" }
  ]
}
```

## Common Block Patterns

**Content Block:**
```liquid
<div class='content-block {{ block.settings.style }}' {{ block.shopify_attributes }}>
  {% if block.settings.heading != blank %}
    <h3 class='content-block__heading'>{{ block.settings.heading | escape }}</h3>
  {% endif %}
  {% if block.settings.text != blank %}
    <div class='content-block__text'>{{ block.settings.text }}</div>
  {% endif %}
</div>
```

**Media Block:**
```liquid
<div class='media-block' {{ block.shopify_attributes }}>
  {% if block.settings.image %}
    {{ block.settings.image | image_url: width: 800 | image_tag: alt: block.settings.image.alt | default: block.settings.alt_text }}
  {% endif %}
</div>
```

**Layout Block (Container):**
```liquid
<div
  class='layout-block layout-block--{{ block.settings.layout_type }}'
  style='--columns: {{ block.settings.columns }}; --gap: {{ block.settings.gap }}px;'
  {{ block.shopify_attributes }}
>
  {% content_for 'blocks' %}
</div>
```
