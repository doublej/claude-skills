# Shopify Integration: Recommended Approach & Architecture

## Recommendation Summary

**DO NOT build a Shopify MCP skill.**

**DO build a "Shopify API Patterns" documentation skill** that teaches users how to integrate Shopify using official tools and SDKs.

---

## Why This Recommendation

### The MCP Trap

Shopify MCP appears attractive because:
- "One-click integration" is appealing
- Claude integration sounds powerful
- Existing MCPs (even small ones) build false confidence

But it fails because:
1. **Completeness is impossible** - Shopify has 1000+ operations; 15-tool MCP covers 1.5%
2. **Versioning is unsustainable** - Quarterly updates + deprecated endpoints = perpetual triage
3. **Rate limiting is fragile** - GraphQL cost model hidden from users; easy to silently exceed budget
4. **Credential risk** - Storing tokens in MCP = single point of compromise
5. **False abstraction** - MCP hides complexity instead of teaching it; users hit walls immediately

### Why Patterns Skill Works Better

A comprehensive "Shopify API Patterns" skill:
1. **Honest** - Upfront about complexity, teaches real patterns
2. **Scalable** - Works for simple and complex workflows
3. **Maintainable** - Documentation updates are low-cost; links to official resources reduce burden
4. **Safe** - No credential storage; users control OAuth scopes
5. **Flexible** - Points to official SDKs for unlimited functionality
6. **Sustainable** - 3-year outlook is manageable (unlike MCP)

---

## Proposed Skill Structure: "Shopify API Patterns"

### Metadata
```yaml
name: shopify-api-patterns
description: Shopify GraphQL Admin API patterns for custom integrations. Covers authentication, rate limiting, versioning, bulk operations, inventory, orders, and webhooks. Use when building Shopify apps, automating store operations, or integrating with custom systems.
```

### Directory Structure
```
shopify-api-patterns/
├── SKILL.md                 (Main guide, ~2000 words)
├── references/
│   ├── authentication.md    (OAuth, tokens, scopes)
│   ├── rate-limiting.md     (GraphQL costs, strategies)
│   ├── versioning.md        (Handling API versions)
│   ├── bulk-operations.md   (Bulk mutations, async jobs)
│   └── patterns/
│       ├── products.md      (CRUD, variants, metafields)
│       ├── orders.md        (Creation, fulfillment, tracking)
│       ├── inventory.md     (Locations, stock levels, reservations)
│       ├── customers.md     (Segmentation, tagging, analytics)
│       ├── webhooks.md      (Event subscriptions, security)
│       └── automation.md    (Flow, background jobs)
└── examples/
    ├── nodejs-sdk/
    │   ├── setup.js
    │   ├── products.js
    │   ├── orders.js
    │   └── bulk-operations.js
    ├── python-sdk/
    │   ├── setup.py
    │   ├── products.py
    │   └── orders.py
    └── graphql/
        ├── product-query.graphql
        ├── bulk-mutation.graphql
        └── inventory-query.graphql
```

### Main Content (SKILL.md)

#### Section 1: Overview & Approach
```markdown
# Shopify API Patterns Skill

## Why This Skill Exists

Shopify's API is powerful but complex:
- **1000+ operations** across products, orders, inventory, fulfillment, analytics
- **GraphQL-first** design with cost-based rate limiting
- **Quarterly versioning** with deprecation cycles
- **Enterprise-grade** complexity (designed for ecommerce experts)

This skill teaches **patterns and best practices** for working with Shopify APIs.
It does NOT provide a simplified wrapper—instead, it gives you the knowledge to
use official Shopify tools effectively.

## Official Resources (Use These)

### Shopify CLI (Easiest for Shopify Apps)
- Built-in authentication (secure OAuth)
- Local development environment
- Hot reloading
- Built-in testing
- **Best for:** Building apps in Shopify admin

### GraphQL Admin API (Most Flexible)
- Complete API surface (all 1000+ operations)
- Cost-based rate limiting (more efficient than REST)
- Single endpoint
- Official Node.js, Python, Ruby SDKs
- **Best for:** Custom integrations, background jobs

### REST Admin API (Simpler Requests)
- 40 requests/minute per store
- Straightforward HTTP calls
- Lower learning curve
- **Best for:** Simple CRUD operations

## Choose Your Path

### Path 1: Building a Shopify App
→ Use **Shopify CLI** (no coding Shopify API directly)

### Path 2: Backend Integration
→ Use **Official SDK** (Node.js, Python, Ruby)

### Path 3: Understanding GraphQL Queries
→ Study this skill's **GraphQL patterns**

## This Skill Covers

✓ Shopify API authentication patterns
✓ Rate limiting strategies (REST & GraphQL)
✓ Handling quarterly API versions
✓ Bulk operations for large datasets
✓ Common workflows (products, orders, inventory)
✓ Webhook integration
✓ Error handling patterns
✗ MCP server (because it's inadequate for real workflows)
✗ Simplified proxy tools (because they hide important complexity)
```

#### Section 2: Authentication

```markdown
## Authentication & Access Tokens

### Token Types

**Public Apps (Recommended)**
- OAuth flow through Shopify
- User explicitly approves scopes
- Token tied to store + app + user
- Good for: Third-party integrations

**Custom Apps**
- Generated in Shopify admin
- Access token (no refresh needed)
- Scopes configured at creation time
- Good for: Your own integrations

**Shopify Plus Partner**
- Service account approach
- Different flow (contact Shopify)

### Setting Up Access

#### Public App (OAuth)
```javascript
// Your app server initiates OAuth
const redirectUri = "https://myapp.com/auth/shopify/callback";
const scopes = ["write_products", "read_orders", "write_orders"];
const authUrl = `https://${shop}/admin/oauth/authorize?` +
  `client_id=${clientId}&` +
  `scope=${scopes.join(',')}&` +
  `redirect_uri=${redirectUri}`;
// User clicks this URL in Shopify admin
```

#### Custom App (Simpler)
1. Go to Shopify admin
2. Settings > Apps & integrations > Develop apps
3. Create an app, set scopes
4. Get access token (store in .env, NEVER commit)
5. Use token in API calls

### Environment Variables (KEEP SECRET)
```bash
# .env (add to .gitignore)
SHOPIFY_ACCESS_TOKEN=shpat_xxxxx...
SHOPIFY_SHOP_NAME=mystore.myshopify.com
SHOPIFY_API_VERSION=2025-01
```

### Testing Your Token
```javascript
const client = new shopify.clients.Graphql({
  session: {...},
});

const response = await client.query({
  data: `query { shop { name } }`,
});
console.log(response.body.data.shop.name); // Should print your store name
```

### Scope Reference (Common)
| Scope | Allows |
|-------|--------|
| `read_products` | View products, variants, images |
| `write_products` | Create/update products |
| `read_orders` | View orders, line items |
| `write_orders` | Modify orders, cancel |
| `write_fulfillments` | Mark items fulfilled |
| `read_inventory` | View stock levels, locations |
| `write_inventory` | Update stock reservations |
| `read_customers` | View customer data |
| `write_customers` | Modify customer tags, notes |

**Rule:** Request only scopes you need. Users are cautious about overpermissioned apps.
```

#### Section 3: Rate Limiting (Critical)

```markdown
## Rate Limiting: The Most Important Section

### REST API: Simple Quota
```
40 requests per minute (Shopify Plus: 400/min)
Replenishment: 2 requests/second
```

**Impact:**
- 100 product updates = 100 requests = 2.5 minutes minimum
- 1000 product updates = 25+ minutes minimum

**Strategy:** Use bulk operations for large datasets

### GraphQL API: Cost-Based (More Complex)

Every GraphQL query has a **cost** based on complexity.

**Budget:** 3,000,000 points per day (resets at midnight UTC)

**Cost Examples:**
```
# Simple query (1 node)
query { shop { name } }
Cost: 1 point

# List 10 products (10 nodes)
query {
  products(first: 10) { # 10 nodes = 10 points
    edges { node { id title } }
  }
}
Cost: ~10 points

# List 100 products (100 nodes, subqueries)
query {
  products(first: 100) {
    edges {
      node {
        id title
        variants(first: 10) { # Subquery costs more
          edges { node { id price } }
        }
        images(first: 5) { # Multiple subqueries
          edges { node { id } }
        }
      }
    }
  }
}
Cost: ~50-100 points (depends on variant count)

# Product write (always costs)
mutation {
  productCreate(input: {...}) {
    product { id title }
    userErrors { field message }
  }
}
Cost: 3 points
```

**Key Insight:** Queries requesting many nodes or deep nesting cost more.

### Cost Calculation Formula
```
Cost = nodes_requested + (subqueries × node_complexity)

Example: List 100 products with 10 variants each
= 100 products + (100 × 10 variants)
= 100 + 1000
= 1100 points
```

### Daily Budget Planning
```
3,000,000 points available

Light usage (development):
- 50 test queries/day × 10 points = 500 points ✓

Moderate usage (daily operations):
- 100 product reads × 10 points = 1000 points
- 50 order updates × 3 points = 150 points
- 10 inventory queries × 5 points = 50 points
= 1200 points ✓ (plenty of room)

Heavy usage (bulk operations):
- Bulk product update (1000 products)
- Init mutation: 1 point
- Monitor queries: 2 points × 50 checks = 100 points
= 101 points ✓ (efficient)

Risky usage (naive approach):
- 1000 individual product update mutations × 3 points each
= 3000 points ⚠️ (still okay, but wasteful)

Very risky usage (poor queries):
- 10,000 product reads with deep variants
= 50,000+ points ⚠️ (wastes budget fast)
```

### Rate Limit Headers (Monitor These)
```
X-Shopify-GraphQL-API-Cost-Throttle-Status: {"maxPoints":3000000, "currentlyAvailable":2999500, "restoreRate":50}

Parse this to understand:
- `maxPoints`: Daily budget (3M)
- `currentlyAvailable`: Points left right now
- `restoreRate`: Points restored per second (50 = 180,000/hour)

After a large query, you might see:
`{"maxPoints":3000000, "currentlyAvailable":2995000, "restoreRate":50}`

This means:
- You've used 5,000 points
- 2,995,000 points left
- You gain 50 points/second (3000/min)
- If you hit 0, you can't query until midnight
```

### Safe Patterns

#### Pattern 1: Batch Queries to Reduce Calls
```javascript
// ❌ Bad: Multiple individual queries
const products = [];
for (let i = 0; i < 100; i++) {
  const query = `query { productById(id: "gid://...${id}") { id } }`;
  products.push(await graphql(query)); // 100 API calls
}
// Cost: ~100 points, 100 requests

// ✓ Good: Single query with aliases
const query = `
  query {
    ${ids.map((id, i) => `p${i}: productById(id: "gid://...${id}") { id }`).join('\n')}
  }
`;
const result = await graphql(query); // 1 API call
// Cost: ~10 points, 1 request
```

#### Pattern 2: Use Bulk Operations for Large Datasets
```javascript
// ❌ Bad for 10,000 products
for (let i = 0; i < 10000; i++) {
  await updateProduct(id, newPrice); // 10,000 mutations
}
// Cost: 30,000+ points, rate limit choked

// ✓ Good: Bulk operation
const bulkMutation = `
  mutation {
    bulkOperationRunMutation(
      mutation: "mutation { productUpdate(...) }"
    ) {
      bulkOperation { id status }
    }
  }
`;
// Cost: 1 point to start, then async processing
```

#### Pattern 3: Optimize Query Shape
```javascript
// ❌ Bad: Fetch unneeded data
const query = `
  query {
    products(first: 100) {
      edges {
        node {
          id title description variants(first: 100) { # All variants
            edges { node { id price weight } }
          }
        }
      }
    }
  }
`;

// ✓ Good: Fetch only what you need
const query = `
  query {
    products(first: 100) {
      edges {
        node {
          id title # Skip description if not needed
          variants(first: 10) { # Limit variants per product
            edges { node { id price } } # Skip weight
          }
        }
      }
    }
  }
`;
```

### Emergency Recovery
```
If you hit the daily limit at 10am (still 14 hours left):
1. Check the restore rate: 50 points/second = 180,000/hour
2. 14 hours = 2,520,000 points restored
3. But you need 3,000,000 points
4. You're stuck until midnight UTC

Prevention: Monitor costs, implement daily budgets, alert at 80% usage
```

### Monitoring Tool
```javascript
function trackCost(response) {
  const header = response.headers.get('X-Shopify-GraphQL-API-Cost-Throttle-Status');
  const cost = JSON.parse(header);

  const percentUsed = ((cost.maxPoints - cost.currentlyAvailable) / cost.maxPoints) * 100;
  console.log(`Cost usage: ${percentUsed.toFixed(1)}%`);

  if (percentUsed > 80) {
    console.warn('⚠️  Approaching daily budget limit!');
  }
}
```

**Takeaway:** GraphQL cost model is powerful but requires awareness. MCP tools that don't track costs will silently exceed budgets.
```

#### Section 4: Common Patterns (Products, Orders, Inventory)

Each would include:
- GraphQL query examples with cost estimates
- SDK implementation patterns
- Error handling
- Pagination strategies
- Common pitfalls

#### Section 5: Webhooks & Background Jobs

```markdown
## Webhooks: Real-Time Automation

Webhooks allow Shopify to notify your system of events (order created, inventory changed, etc.)

### Why Webhooks (Instead of MCP Polling)

MCP is request-response only. For real-time automation, use webhooks:

```javascript
// 1. Register webhook (one-time)
mutation {
  webhookSubscriptionCreate(
    topic: ORDERS_CREATED
    webhookSubscription: {
      callbackUrl: "https://myapp.com/webhooks/orders"
      format: JSON
    }
  ) {
    webhookSubscription { id topic }
  }
}

// 2. Shopify POSTs to your endpoint when event occurs
POST /webhooks/orders
Headers: {
  "X-Shopify-Hmac-SHA256": "...",
  "X-Shopify-Shop-API-Call-Limit": "..."
}
Body: { order: {...} }

// 3. Your server validates signature & processes
function validateWebhook(req) {
  const hmac = req.headers['X-Shopify-Hmac-SHA256'];
  const body = req.body;
  const hash = crypto
    .createHmac('sha256', process.env.SHOPIFY_API_SECRET)
    .update(body)
    .digest('base64');

  return hash === hmac; // Always validate!
}
```

### Available Topics
```
ORDERS_CREATED, ORDERS_UPDATED, ORDERS_CANCELLED
INVENTORY_LEVELS_UPDATED
FULFILLMENTS_CREATED
CUSTOMERS_CREATED, CUSTOMERS_UPDATED
PRODUCTS_CREATED, PRODUCTS_UPDATED, PRODUCTS_DELETED
```

### Background Job Pattern
```javascript
// Webhook receives order created
async function handleOrderWebhook(req, res) {
  const order = req.body.order;

  // 1. Validate immediately
  if (!validateWebhook(req)) {
    return res.status(401).send('Unauthorized');
  }

  // 2. Queue for background processing (DON'T process in webhook handler)
  await queue.add('process-order', { orderId: order.id });

  // 3. Respond immediately to Shopify
  res.status(200).send('OK');
}

// Background job (async)
async function processOrder(job) {
  const { orderId } = job.data;

  // Now you can make API calls without timeout pressure
  const order = await shopify.getOrder(orderId);

  // Fulfill if conditions met
  if (order.total_price > 1000) {
    await shopify.createFulfillment(orderId, {...});
  }

  // This job can retry if it fails
}
```

**Key Point:** Webhooks + background jobs enable real automation. MCP polling is too slow and brittle.
```

### Example Files

#### examples/nodejs-sdk/products.js
```javascript
const shopify = require('@shopify/shopify-app-express');

// Setup
const client = new shopify.clients.Graphql({
  session: {...},
});

// 1. Create product
async function createProduct(title, description) {
  const response = await client.query({
    data: `mutation {
      productCreate(input: {
        title: "${title}"
        descriptionHtml: "${description}"
      }) {
        product { id title }
        userErrors { field message }
      }
    }`,
  });

  if (response.body.data.productCreate.userErrors.length > 0) {
    throw new Error(response.body.data.productCreate.userErrors[0].message);
  }

  return response.body.data.productCreate.product;
}

// 2. Update product (with variants)
async function updateProductPrice(productId, newPrice) {
  const getVariants = await client.query({
    data: `query {
      product(id: "${productId}") {
        variants(first: 10) {
          edges { node { id } }
        }
      }
    }`,
  });

  const variantIds = getVariants.body.data.product.variants.edges
    .map(e => e.node.id);

  // Update first variant
  const update = await client.query({
    data: `mutation {
      productVariantUpdate(
        id: "${variantIds[0]}"
        input: { price: ${newPrice} }
      ) {
        productVariant { id price }
      }
    }`,
  });

  return update.body.data.productVariantUpdate.productVariant;
}

// 3. List products with pagination
async function listProducts(cursor = null) {
  const response = await client.query({
    data: `query {
      products(first: 50 ${cursor ? `after: "${cursor}"` : ''}) {
        edges {
          node { id title }
          cursor
        }
        pageInfo { hasNextPage }
      }
    }`,
  });

  return {
    products: response.body.data.products.edges.map(e => e.node),
    hasMore: response.body.data.products.pageInfo.hasNextPage,
    nextCursor: response.body.data.products.edges[
      response.body.data.products.edges.length - 1
    ]?.cursor,
  };
}

// 4. Bulk operations (for 1000s of products)
async function bulkUpdatePrices(priceMultiplier) {
  // Init bulk operation
  const init = await client.query({
    data: `mutation {
      bulkOperationRunMutation(
        mutation: "mutation {
          productVariantUpdate(id: {{variantId}}, input: {price: {{newPrice}}}) {
            productVariant { id price }
          }
        }"
      ) {
        bulkOperation {
          id
          status
          objectCount
          fileSize
          url
          createdAt
        }
      }
    }`,
  });

  const bulkId = init.body.data.bulkOperationRunMutation.bulkOperation.id;

  // Monitor progress
  const checkProgress = async () => {
    const check = await client.query({
      data: `query {
        node(id: "${bulkId}") {
          ... on BulkOperation {
            id
            status
            errors { displayErrors { message } }
            successfullyProcessedObjectCount
          }
        }
      }`,
    });

    const status = check.body.data.node;
    console.log(`Bulk operation: ${status.status} (${status.successfullyProcessedObjectCount} done)`);

    return status.status === 'COMPLETED';
  };

  // Wait for completion (poll every 5 seconds)
  while (!await checkProgress()) {
    await new Promise(r => setTimeout(r, 5000));
  }

  console.log('Bulk operation complete!');
}

module.exports = { createProduct, updateProductPrice, listProducts, bulkUpdatePrices };
```

---

## Conclusion: Patterns Skill Architecture

This structure:
- ✓ **Honest:** Explains why certain approaches work
- ✓ **Comprehensive:** References all major operations
- ✓ **Actionable:** Working code examples in multiple languages
- ✓ **Maintainable:** Links to official docs; low-maintenance documentation
- ✓ **Sustainable:** 2000 words of docs >> 2000 lines of MCP code

It teaches users how to build real Shopify integrations, not fake ones with MCP.
```

---

## Implementation Plan

### Phase 1: Core Documentation (2-3 days)
1. Write SKILL.md (main guide)
2. Create authentication.md reference
3. Create rate-limiting.md (most important)
4. Create basic examples (Node.js)

### Phase 2: Expand References (2-3 days)
1. versioning.md
2. bulk-operations.md
3. Product, order, inventory pattern guides

### Phase 3: Code Examples (2 days)
1. Python SDK examples
2. GraphQL query examples
3. Webhook + background job example

### Phase 4: Polish (1 day)
1. Link checking
2. Test code examples (run them)
3. Review for accuracy

**Total effort: ~1 week** (much less than MCP maintenance burden)

---

## Why This Wins Over MCP

| Aspect | MCP | Patterns Skill |
|--------|-----|-----------------|
| Coverage | 15 tools (1.5%) | 100% reference |
| Learning Curve | Shallow (incomplete) | Medium (comprehensive) |
| Real Workflows | Limited (incomplete) | Fully supported |
| Maintenance | High (versioning hell) | Low (link checks) |
| Sustainability | 3-year risk: high | 3-year risk: low |
| User Empowerment | Dependency on MCP | Empowered with knowledge |

**Recommendation:** Build the Patterns Skill. It delivers more value with less maintenance burden.
