# CSS Conventions for Shopify Themes

Source: Shopify/horizon cursor rules

## Specificity Rules

- **Never** use IDs as selectors
- **Avoid** elements as selectors
- **Avoid** `!important` — if used, comment why
- Target `0 1 0` specificity (single `.class`)
- Max `0 4 0` for parent/child relationships

## BEM Naming

```css
.product-card { }              /* Block */
.product-card__image { }       /* Element */
.product-card__title { }       /* Element */
.product-card--featured { }    /* Modifier */
```

- Single element level only (no `.block__el1__el2`)
- Modifiers always paired with base class in HTML
- Start new BEM scope for standalone sub-components

## Scoping CSS to Sections/Blocks

Set CSS variables inline via `style` attribute — keeps CSS in `{% stylesheet %}`:

```html
<!-- DO -->
<section style="--background: {{ settings.bg_color }}; --padding: {{ settings.padding }}px;">

<!-- DON'T -->
{% style %} .selector--{{ block.id }} { --bg: {{ settings.bg_color }}; } {% endstyle %}
```

## CSS Variables

- Namespace to component: `--component-padding` not `--padding`
- Never hardcode colors — use color schemes
- Global vars in `:root` via `snippets/theme-styles-variables.liquid`
- Scoped vars on component class

```css
.facets {
  --drawer-padding: var(--padding-md);
  --facets-upper-z-index: 3;
}
```

## CSS Nesting

- No `&` operator in nested selectors (except states: `&:hover`, `&:focus`)
- Never nest beyond first level (except media queries)
- Use nesting for media queries and parent-modifier → child patterns:

```css
.parent--full-screen {
  grid-columns: 1fr;
  .child { grid-column: 1; }
}
```

## Modern CSS

- Container queries for responsive components
- `clamp()` for fluid spacing
- `color-mix()` for progressive enhancement only (iOS <16.2)
- Logical properties for RTL: `padding-inline`, `margin-block`, `text-align: start`
- `@layer` for cascade control
- Mobile-first: `min-width` media queries

## Accessibility

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

.button:focus-visible {
  outline: 2px solid rgb(var(--color-focus));
  outline-offset: 2px;
}
```

## Performance

- Animate only `transform` and `opacity`
- Use `contain: content` on grids
- Limit `:has()` — use direct child combinators (`>`) to reduce traversal
- Prefer server-rendered classes over `:has()` for dynamic state
