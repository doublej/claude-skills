# Snippets & Assets

Source: Shopify/horizon cursor rules

## Snippet Documentation

Every snippet must include `{% doc %}` / `{% enddoc %}`:

```liquid
{% doc %}
  Product Card Component

  Renders a product card with customizable options.

  @param product {Object} Product object (required)
  @param show_vendor {Boolean} Display vendor name (default: false)
  @param image_ratio {String} Image aspect ratio (default: 'adapt')
  @param lazy_load {Boolean} Enable lazy loading (default: true)
  @param card_class {String} Additional CSS classes

  @example
    {% render 'product-card',
       product: product,
       show_vendor: true,
       image_ratio: 'square'
    %}
{% enddoc %}
```

## Parameter Handling

Always provide defaults and validate:

```liquid
{% liquid
  assign product = product | default: empty
  assign show_vendor = show_vendor | default: false
  assign image_ratio = image_ratio | default: 'adapt'
  assign lazy_load = lazy_load | default: true

  unless product != empty
    echo '<!-- Error: product parameter required -->'
    break
  endunless
%}
```

## Common Snippet Patterns

**Icon Snippet:**
```liquid
{% liquid
  assign icon = icon | default: ''
  assign size = size | default: 'icon--medium'
  unless icon != blank
    break
  endunless
%}
<svg class="icon {{ size }} {{ class }}" aria-hidden="true" focusable="false">
  <use href="#icon-{{ icon }}"></use>
</svg>
```

**Price Snippet:**
```liquid
<div class="price">
  <div class="price__regular">{{ product.price | money }}</div>
  {% if show_compare_at and product.compare_at_price > product.price %}
    <div class="price__compare-at"><s>{{ product.compare_at_price | money }}</s></div>
  {% endif %}
  {% if show_unit_price and product.selected_or_first_available_variant.unit_price_measurement %}
    <div class="price__unit">
      {{ product.selected_or_first_available_variant.unit_price | money }}/
      {{ product.selected_or_first_available_variant.unit_price_measurement.reference_unit }}
    </div>
  {% endif %}
</div>
```

## Assets Directory

- Flat directory — no subdirectories
- Contains CSS, JS, images, icons
- Reference with `asset_url` filter: `'style.css' | asset_url`
- Inline icons with `inline_asset_content` filter
