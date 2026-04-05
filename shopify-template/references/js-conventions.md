# JavaScript Conventions for Shopify Themes

Source: Shopify/horizon cursor rules

## General Principles

- **Zero external dependencies** — native browser APIs only
- `const` over `let`; `for...of` over `.forEach()`
- `async/await` over `.then()` chaining
- Early returns over nested conditionals

## Web Components with Component Framework

```javascript
import { Component } from '@theme/component';

/**
 * @typedef {Object} ProductCardRefs
 * @property {HTMLButtonElement} addButton
 * @property {HTMLElement} priceDisplay
 */

/** @extends {Component<ProductCardRefs>} */
class ProductCard extends Component {
  connectedCallback() {
    super.connectedCallback();
    this.#init();
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    this.#cleanup();
  }

  async handleAddToCart(event) {
    event.preventDefault();
    this.refs.addButton.disabled = true;
    try {
      await addToCart(this.dataset.productId);
      this.dispatchEvent(new CustomEvent('cart:item-added', {
        detail: { productId: this.dataset.productId },
        bubbles: true
      }));
    } catch (error) {
      console.error('Add to cart error:', error);
    }
  }

  #init() { /* private setup */ }
  #cleanup() { /* private teardown */ }
}

customElements.define('product-card', ProductCard);
```

**HTML usage with refs and event binding:**
```html
<product-card data-product-id="{{ product.id }}">
  <div ref="priceDisplay">{{ product.price | money }}</div>
  <button ref="addButton" on:click="/handleAddToCart">Add to cart</button>
</product-card>
```

## Component Communication

**Parent → Child:** invoke public methods directly
**Child → Parent:** dispatch custom events with `bubbles: true`

```javascript
// Child emits
this.dispatchEvent(new CustomEvent('variant:select', {
  detail: { variantId, price, available },
  bubbles: true
}));

// Parent listens
document.addEventListener('variant:select', (e) => {
  gallery.selectImage(0);
});
```

## JavaScript in Liquid Files

Use `{% javascript %}` for component-specific scripts:

```liquid
{% javascript %}
import { Component } from '@theme/component';

class FeaturedCollection extends Component {
  async handleFilter(filterValue, event) {
    event.preventDefault();
    const url = new URL(window.location.href);
    url.searchParams.set('filter', filterValue);
    // fetch + replace grid content
  }
}

customElements.define('featured-collection', FeaturedCollection);
{% endjavascript %}
```

## Error Handling & Cleanup

Always use AbortController for cancellable requests:

```javascript
#abortController = null;

async loadData(url) {
  this.#abortController?.abort();
  this.#abortController = new AbortController();
  try {
    const response = await fetch(url, { signal: this.#abortController.signal });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    if (error.name !== 'AbortError') throw error;
  }
}

disconnectedCallback() {
  super.disconnectedCallback();
  this.#abortController?.abort();
}
```

## URL Manipulation

Always use `URL` and `URLSearchParams` — never string manipulation:

```javascript
const url = new URL(window.location.href);
url.searchParams.set('filter', filterValue);
history.pushState({ filter: filterValue }, '', url.toString());
```

## File Structure

Group by feature: `product.js`, `cart.js`, `collection.js`, `search.js`
