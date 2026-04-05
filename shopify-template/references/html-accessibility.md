# HTML & Accessibility for Shopify Themes

Source: Shopify/horizon cursor rules

## Native Elements Over JavaScript

- `<details>` / `<summary>` — expandable content (FAQs, product details)
- `<dialog>` — modals (built-in focus management)
- `popover` attribute — tooltips, menus (auto-positioning)
- `<search>` — search forms
- `<output>` — form calculations

## Progressive Enhancement

1. Start with semantic HTML that works without JS
2. Layer CSS for visual enhancement
3. Add JS for advanced interactions
4. Never break core functionality for older browsers

Use "Baseline widely available" features. Progressive enhancement features may be "Baseline 2024".

## ID Naming Convention

CamelCase with section/block identifiers (guaranteed unique):

```html
<section id="FeaturedCollection-{{ section.id }}">
<div id="ProductCard-{{ block.id }}">
<dialog id="ProductModal-{{ product.id }}-{{ section.id }}">
```

## Accessibility Requirements

**Skip Link:**
```html
<a href="#main" class="skip-link visuallyhidden focusable">Skip to main content</a>
<main id="main" tabindex="-1">...</main>
```

**Focus Management:**
- `tabindex="0"` for custom interactive elements
- Never positive tabindex values
- `:focus-visible` for keyboard-only focus rings
- Trap focus in modal contexts

**Screen Readers:**
- Semantic HTML elements
- `aria-label` when visual context isn't enough
- `aria-expanded` for collapsible content
- `aria-hidden="true"` on decorative elements

**Viewport:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```
Never use `maximum-scale=1.0` or `user-scalable=no`.

**Language:** `<html lang="en">`

## Localization

**Every user-facing text must use translation filters:**

```liquid
<!-- DO -->
<h2>{{ 'sections.featured_collection.title' | t }}</h2>
<button>{{ 'products.add_to_cart' | t }}</button>

<!-- DON'T -->
<h2>Featured Collection</h2>
```

**Translation with variables:**
```liquid
{{ 'products.price_range' | t: min: product.price_min | money, max: product.price_max | money }}
```

**Locale file structure (`locales/en.default.json`):**
```json
{
  "general": {
    "accessibility": {
      "skip_to_content": "Skip to content",
      "close": "Close"
    }
  },
  "products": {
    "add_to_cart": "Add to cart",
    "price": {
      "regular": "Regular price",
      "sale": "Sale price"
    }
  }
}
```

- Hierarchical keys, max 3 levels deep
- `snake_case` key names
- Use interpolation, not string appending
- Escape variables: `{{ variable | escape }}`
