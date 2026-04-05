# Liquid Syntax Standards

Source: Shopify/horizon cursor rules

## Valid Tags

**Control Flow:**
- `if condition` / `endif`
- `unless condition` / `endunless`
- `case variable` / `when value` / `endcase`
- `for item in array` / `endfor` (optional `limit:`, `offset:`)

**Variable Assignment:**
- `assign variable = value`
- `capture variable` / `endcapture`
- `increment variable` / `decrement variable`

**Template Inclusion:**
- `render 'snippet-name'` / `render 'snippet-name', param: value`
- `section 'section-name'`

**Forms:**
- `form 'cart'` / `form 'product'` / `form 'customer_login'`

**Other:**
- `paginate collection.products by 12` / `endpaginate`
- `liquid` / `endliquid` — multiline Liquid block
- `comment` / `endcomment` — block comments
- `raw` / `endraw` — output without processing

## Valid Filters

**Array:** `compact`, `concat`, `find: property, value`, `where: property, value`, `map: property`, `sort`, `reverse`, `first`, `last`, `size`

**String:** `escape`, `truncate: 150`, `handleize`, `replace: 'old', 'new'`, `split: 'delimiter'`, `upcase`, `downcase`, `capitalize`

**Money:** `money`, `money_with_currency`, `money_without_currency`

**Media:**
- `image_url: width: 800` — responsive image URL
- `image_tag` — complete img tag
- `asset_url` — theme asset URL (`'style.css' | asset_url`)

## Syntax Rules

- Use `{% liquid %}` for multiline code blocks
- Use `{% # comment %}` for inline comments
- **Never invent** new filters, tags, or objects
- Use object dot notation: `product.title` not `product['title']`

## Snippet Documentation with {% doc %}

All snippets must include documentation using `{% doc %}` / `{% enddoc %}`:

```liquid
{% doc %}
  Volume Pricing Info

  Renders volume pricing information with quantity rules.

  @param {object} variant - The variant object
  @param {string} [unique_id] - Optional unique identifier
  @param {number} [quantity] - Current quantity

  @example
  {% render 'volume-pricing-info',
    variant: item.variant,
    unique_id: item.index,
    quantity: item.quantity
  %}
{% enddoc %}
```

**Parameter types:** `{object}`, `{string}`, `{number}`, `{boolean}`, `{array}`
**Optional params:** Use brackets: `[param_name]`

## Inline Variables Pattern

For straightforward props, inline the Liquid instead of declaring extra variables:

```liquid
<!-- DO: inline approach -->
<div
  class='component component--{{ settings.style_modifier }}'
  style='color: {{ settings.text_color }};'
>
  {{ content | truncate: settings.max_length | default: 200 }}
</div>

<!-- DON'T: unnecessary variable declarations -->
{% liquid
  assign component_class = 'component component--' | append: settings.style_modifier
  assign truncate_length = settings.max_length | default: 200
%}
<div class='{{ component_class }}'>
  {{ content | truncate: truncate_length }}
</div>
```

**Exceptions** — use variables when:
- Filter parameters require string values with complex logic
- Same complex calculation is used multiple times
- Logic is extremely complex and would harm readability
- Building a string incrementally with conditional parts
