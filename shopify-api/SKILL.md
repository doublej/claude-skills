---
name: shopify-api
description: Build Shopify integrations using Admin REST/GraphQL APIs. Use when creating products, managing orders, updating inventory, handling customers, or automating store operations. Covers authentication, rate limiting, webhooks, and common e-commerce workflows.
---

# Shopify API

Build Shopify store integrations using the Admin API (REST and GraphQL).

## Authentication

### Custom App Setup (Recommended)

1. Shopify Admin → Settings → Apps and sales channels → Develop apps
2. Create app → Configure Admin API scopes → Install
3. Copy Admin API access token

```javascript
// Node.js with @shopify/shopify-api
import '@shopify/shopify-api/adapters/node';
import { shopifyApi, LATEST_API_VERSION } from '@shopify/shopify-api';

const shopify = shopifyApi({
  apiKey: process.env.SHOPIFY_API_KEY,
  apiSecretKey: process.env.SHOPIFY_API_SECRET,
  scopes: ['read_products', 'write_products', 'read_orders'],
  hostName: process.env.SHOPIFY_STORE_DOMAIN,
  apiVersion: LATEST_API_VERSION,
  isEmbeddedApp: false,
});

// Create REST client
const session = { shop: 'your-store.myshopify.com', accessToken: process.env.SHOPIFY_ACCESS_TOKEN };
const client = new shopify.clients.Rest({ session });
```

```python
# Python with shopify library
import shopify

shopify.ShopifyResource.set_site(f"https://{api_key}:{password}@{shop_name}.myshopify.com/admin/api/2024-01")
# Or with access token
shopify.ShopifyResource.set_site(f"https://{shop_name}.myshopify.com/admin/api/2024-01")
shopify.ShopifyResource.set_headers({'X-Shopify-Access-Token': access_token})
```

### Required Scopes by Operation

| Operation | Scopes |
|-----------|--------|
| Products | `read_products`, `write_products` |
| Orders | `read_orders`, `write_orders` |
| Customers | `read_customers`, `write_customers` |
| Inventory | `read_inventory`, `write_inventory` |
| Fulfillment | `read_fulfillments`, `write_fulfillments` |

## Products

### List Products (REST)

```javascript
const response = await client.get({ path: 'products', query: { limit: 50 } });
const products = response.body.products;
```

### Get Product by ID

```javascript
const response = await client.get({ path: `products/${productId}` });
const product = response.body.product;
```

### Create Product

```javascript
const response = await client.post({
  path: 'products',
  data: {
    product: {
      title: 'New Product',
      body_html: '<p>Description here</p>',
      vendor: 'Vendor Name',
      product_type: 'Category',
      status: 'draft', // 'active', 'draft', 'archived'
      variants: [
        { price: '29.99', sku: 'SKU-001', inventory_quantity: 100 }
      ],
      images: [
        { src: 'https://example.com/image.jpg' }
      ]
    }
  }
});
```

### Update Product

```javascript
await client.put({
  path: `products/${productId}`,
  data: {
    product: {
      id: productId,
      title: 'Updated Title',
      variants: [{ id: variantId, price: '39.99' }]
    }
  }
});
```

### GraphQL: Products with Variants

```javascript
const gqlClient = new shopify.clients.Graphql({ session });

const query = `{
  products(first: 10) {
    edges {
      node {
        id
        title
        variants(first: 5) {
          edges {
            node {
              id
              price
              inventoryQuantity
            }
          }
        }
      }
    }
  }
}`;

const response = await gqlClient.query({ data: query });
```

## Orders

### List Orders

```javascript
const response = await client.get({
  path: 'orders',
  query: {
    status: 'any', // 'open', 'closed', 'cancelled', 'any'
    financial_status: 'paid',
    created_at_min: '2024-01-01T00:00:00Z',
    limit: 50
  }
});
```

### Get Order by ID

```javascript
const response = await client.get({ path: `orders/${orderId}` });
const order = response.body.order;
// Access: order.line_items, order.shipping_address, order.customer
```

### Cancel Order

```javascript
await client.post({ path: `orders/${orderId}/cancel` });
```

### Create Refund

```javascript
await client.post({
  path: `orders/${orderId}/refunds`,
  data: {
    refund: {
      notify: true,
      note: 'Refund reason',
      refund_line_items: [
        { line_item_id: lineItemId, quantity: 1, restock_type: 'return' }
      ]
    }
  }
});
```

## Customers

### List Customers

```javascript
const response = await client.get({
  path: 'customers',
  query: { limit: 50 }
});
```

### Search Customers

```javascript
const response = await client.get({
  path: 'customers/search',
  query: { query: 'email:customer@example.com' }
});
```

### Create Customer

```javascript
await client.post({
  path: 'customers',
  data: {
    customer: {
      first_name: 'John',
      last_name: 'Doe',
      email: 'john@example.com',
      phone: '+1234567890',
      tags: 'vip,newsletter',
      accepts_marketing: true
    }
  }
});
```

### Update Customer Tags

```javascript
await client.put({
  path: `customers/${customerId}`,
  data: {
    customer: { id: customerId, tags: 'vip,loyalty-gold' }
  }
});
```

## Inventory

### Get Inventory Levels

```javascript
const response = await client.get({
  path: 'inventory_levels',
  query: { inventory_item_ids: itemId }
});
```

### Adjust Inventory

```javascript
await client.post({
  path: 'inventory_levels/adjust',
  data: {
    location_id: locationId,
    inventory_item_id: itemId,
    available_adjustment: 10 // positive to add, negative to subtract
  }
});
```

### Set Inventory Level

```javascript
await client.post({
  path: 'inventory_levels/set',
  data: {
    location_id: locationId,
    inventory_item_id: itemId,
    available: 50
  }
});
```

## Webhooks

### Register Webhook

```javascript
await client.post({
  path: 'webhooks',
  data: {
    webhook: {
      topic: 'orders/create', // See topics below
      address: 'https://your-app.com/webhooks/orders',
      format: 'json'
    }
  }
});
```

### Common Webhook Topics

| Topic | Triggers When |
|-------|---------------|
| `orders/create` | New order placed |
| `orders/updated` | Order modified |
| `orders/paid` | Payment received |
| `orders/fulfilled` | Order shipped |
| `products/create` | Product created |
| `products/update` | Product modified |
| `customers/create` | Customer registered |
| `inventory_levels/update` | Stock changed |

### Verify Webhook (HMAC)

```javascript
import crypto from 'crypto';

function verifyWebhook(data, hmacHeader, secret) {
  const hash = crypto.createHmac('sha256', secret).update(data, 'utf8').digest('base64');
  return crypto.timingSafeEqual(Buffer.from(hash), Buffer.from(hmacHeader));
}

// In webhook handler
const hmac = req.headers['x-shopify-hmac-sha256'];
const isValid = verifyWebhook(req.rawBody, hmac, process.env.SHOPIFY_API_SECRET);
```

## Rate Limiting

### REST API Limits

- **Standard**: 40 requests/app/store (bucket refills 2/sec)
- **Plus stores**: Higher limits available

```javascript
// Check rate limit headers
const remaining = response.headers['x-shopify-shop-api-call-limit']; // "32/40"

// Handle 429 with exponential backoff
async function apiCallWithRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.code === 429) {
        const delay = Math.pow(2, i) * 1000;
        await new Promise(r => setTimeout(r, delay));
      } else throw error;
    }
  }
}
```

### GraphQL Cost-Based Limits

- **Budget**: 1000 points/second (refills continuously)
- **Query cost**: Sum of field costs (connections cost more)

```javascript
// Check remaining budget in response
const cost = response.extensions?.cost;
// { requestedQueryCost: 42, actualQueryCost: 35, throttleStatus: { currentlyAvailable: 965 } }
```

## Pagination

### REST Cursor Pagination

```javascript
async function getAllProducts(client) {
  let products = [];
  let pageInfo = null;

  do {
    const response = await client.get({
      path: 'products',
      query: { limit: 250, ...(pageInfo && { page_info: pageInfo }) }
    });

    products.push(...response.body.products);
    pageInfo = response.pageInfo?.nextPage?.query?.page_info;
  } while (pageInfo);

  return products;
}
```

### GraphQL Cursor Pagination

```javascript
const query = `query ($cursor: String) {
  products(first: 50, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    edges { node { id title } }
  }
}`;

let cursor = null;
let allProducts = [];

do {
  const response = await gqlClient.query({ data: { query, variables: { cursor } } });
  const { edges, pageInfo } = response.body.data.products;
  allProducts.push(...edges.map(e => e.node));
  cursor = pageInfo.hasNextPage ? pageInfo.endCursor : null;
} while (cursor);
```

## Bulk Operations (Large Data)

For operations on 1000+ items, use GraphQL bulk operations:

```javascript
// Start bulk query
const bulkQuery = `mutation {
  bulkOperationRunQuery(query: """
    { products { edges { node { id title } } } }
  """) {
    bulkOperation { id status }
    userErrors { field message }
  }
}`;

// Poll for completion
const pollQuery = `{ currentBulkOperation { id status objectCount url } }`;

// Download results from URL when status is COMPLETED
```

## MCP Server (Optional)

For Claude Desktop integration, use [shopify-mcp](https://github.com/GeLi2001/shopify-mcp):

```json
{
  "mcpServers": {
    "shopify": {
      "command": "npx",
      "args": ["shopify-mcp", "--accessToken", "<TOKEN>", "--domain", "<STORE>.myshopify.com"]
    }
  }
}
```

## Error Handling

```javascript
try {
  const response = await client.get({ path: 'products' });
} catch (error) {
  switch (error.code) {
    case 401: // Invalid credentials
    case 403: // Insufficient scopes
    case 404: // Resource not found
    case 422: // Validation error (check error.response.body.errors)
    case 429: // Rate limited (wait and retry)
    case 500: // Shopify server error (retry with backoff)
  }
}
```

## API Versioning

Shopify releases quarterly versions (e.g., `2024-01`, `2024-04`). Use stable versions:

```javascript
import { ApiVersion } from '@shopify/shopify-api';
// ApiVersion.January24, ApiVersion.April24, etc.
// Or LATEST_API_VERSION for newest stable
```

Check deprecations at: https://shopify.dev/docs/api/release-notes
