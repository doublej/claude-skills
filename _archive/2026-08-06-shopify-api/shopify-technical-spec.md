# Shopify MCP Technical Specification
## Implementation Guide for Claude Code Skill

---

## Architecture Decision Record (ADR)

### Decision
**Use GeLi2001/shopify-mcp as the foundation MCP server for Shopify Claude Code skill.**

### Context
Three candidate implementations evaluated:
1. **GeLi2001/shopify-mcp** (120 stars, GraphQL, TypeScript, npx)
2. **amir-bengherbi/shopify-mcp-server** (16 stars, REST, JavaScript)
3. **Official Shopify SDKs** (1000+ stars, language-specific, no MCP wrapper)

### Decision Rationale
1. **Popularity (75% weight):** 120 stars vs 16 stars = 7.5x adoption signal
2. **Modern Architecture:** GraphQL queries are forward-compatible; Shopify deprecating REST
3. **TypeScript:** Type safety reduces integration errors in Claude Code context
4. **Installation:** npx standard reduces user friction
5. **Extensibility:** GraphQL mutations support future feature additions

### Alternatives Considered & Rejected
- **REST-based approach (amir-bengherbi):** 7.5x fewer deployments, API sunset risk
- **Direct SDK usage:** Requires custom MCP wrapper (reinventing wheel)
- **Building from scratch:** >3 months engineering time vs 0 with established MCP

### Implications
- Commits to GraphQL-first architecture for v1.0 and v2.0
- Phase 2 enhancement sourced from amir-bengherbi's feature list, not direct code adoption
- Shopify API 2025+ lock-in (strategic commitment, automatic sunset after 2 years)

### Status
**ACCEPTED** - Implementation begins with skill-creator skill

---

## Technical Architecture

### MCP Server Layer

```
┌─────────────────────────────────────────┐
│   Claude Code / User Chat Interface     │
└─────────────────┬───────────────────────┘
                  │
                  ↓
          ┌───────────────────┐
          │   Shopify Skill   │
          │   (SKILL.md)      │
          └─────────┬─────────┘
                    │
                    ↓
      ┌─────────────────────────────┐
      │  GeLi2001/shopify-mcp       │
      │  (MCP Server)               │
      │  ├─ get-products            │
      │  ├─ get-customers           │
      │  ├─ get-orders              │
      │  ├─ createProduct           │
      │  ├─ updateCustomer          │
      │  └─ updateOrder             │
      └─────────────┬───────────────┘
                    │
                    ↓
      ┌──────────────────────────────┐
      │  Shopify GraphQL Admin API   │
      │  (2025-01 API version)       │
      │  ├─ Products                 │
      │  ├─ Customers                │
      │  ├─ Orders                   │
      │  ├─ Collections              │
      │  ├─ Discounts                │
      │  └─ Fulfillments             │
      └──────────────────────────────┘
```

### Installation Flow

```bash
# 1. User installs Shopify skill
install-skill.sh shopify

# 2. Skill setup prompts for:
#    - Store URL (e.g., mystore.myshopify.com)
#    - Access Token (from Shopify admin)

# 3. Internally:
#    npm install shopify-mcp  (or npx shopify-mcp)
#    Verify GraphQL endpoint connectivity

# 4. Claude Code registers tool handlers
#    ✓ /shopify get-products
#    ✓ /shopify get-customers
#    ... etc
```

---

## API Authentication

### Shopify Access Token Model

**How It Works:**
1. Shopify store admin creates "Custom App" in Admin settings
2. Generates Access Token with specific scopes
3. Token stored in Claude Code environment (e.g., `SHOPIFY_ACCESS_TOKEN`)
4. All GraphQL queries include header: `X-Shopify-Access-Token: {TOKEN}`

**Scopes Required for v1.0:**
```
read_products        # Get product data
write_products       # Create/update products
read_customers       # Get customer data
write_customers      # Update customer info
read_orders          # Get order data
write_orders         # Update order status
```

**Scopes for Phase 2:**
```
read_discounts       # Get discount codes
write_discounts      # Create discount codes
read_draft_orders    # Create draft orders
write_draft_orders
read_fulfillments
write_fulfillments
read_webhooks
write_webhooks
```

### Token Storage & Refresh

**Storage:** `~/.claude/shopify-config.json` (or equivalent)
```json
{
  "store_url": "mystore.myshopify.com",
  "access_token": "shpat_...",
  "api_version": "2025-01",
  "created_at": "2026-01-29",
  "expires_at": "2027-01-29"
}
```

**Refresh Strategy:**
- Shopify tokens don't expire naturally (unlike OAuth)
- Tokens rotated annually by admin recommendation
- Skill checks token validity before operations
- Clear error message if token invalid/revoked

**Security:**
- Token stored locally, never transmitted to Anthropic
- Used only for direct Shopify API calls
- Scoped to minimum required permissions
- Rotate tokens if compromise suspected

---

## GraphQL Query Patterns

### Example 1: Get Products (with Pagination)

**Query:**
```graphql
query GetProducts($first: Int!, $after: String) {
  products(first: $first, after: $after) {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        id
        title
        description
        handle
        status
        variants(first: 5) {
          edges {
            node {
              id
              title
              price
              inventoryQuantity
            }
          }
        }
      }
    }
  }
}
```

**Variables:**
```json
{
  "first": 25,
  "after": "eyJkaXJlY3Rpb24iOiJuZXh0In0="
}
```

**Response Shape (Relevant to Tool Output):**
```typescript
interface Product {
  id: string;
  title: string;
  description: string;
  handle: string;
  status: "ACTIVE" | "ARCHIVED" | "DRAFT";
  variants: Array<{
    id: string;
    title: string;
    price: string;
    inventoryQuantity: number;
  }>;
}
```

### Example 2: Create Product

**Query:**
```graphql
mutation CreateProduct($input: ProductInput!) {
  productCreate(input: $input) {
    product {
      id
      title
      handle
      status
    }
    userErrors {
      field
      message
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "title": "New Awesome Product",
    "productType": "T-Shirt",
    "vendor": "My Brand",
    "status": "DRAFT"
  }
}
```

### Example 3: Get Orders with Customer Info

**Query:**
```graphql
query GetOrders($first: Int!) {
  orders(first: $first) {
    edges {
      node {
        id
        orderNumber
        createdAt
        totalPriceSet {
          shopMoney {
            amount
            currencyCode
          }
        }
        customer {
          id
          email
          firstName
          lastName
        }
        lineItems(first: 5) {
          edges {
            node {
              id
              title
              quantity
              originalTotalSet {
                shopMoney {
                  amount
                }
              }
            }
          }
        }
        fulfillmentOrders {
          id
          status
          lineItems(first: 10) {
            edges {
              node {
                id
                quantity
              }
            }
          }
        }
      }
    }
  }
}
```

---

## Rate Limiting Strategy

### Shopify Rate Limit Model

**API Query Cost System:**
- Each GraphQL query has an associated cost (1-100)
- Cumulative cost per second limited to ~4/sec
- More complex queries (multiple resources) cost more

**Monitoring:**
```
Query Cost: 2/4.0 (50% capacity)
Reset Time: 0.5s
```

### Implementation in MCP

**Error Response (Rate Limited):**
```json
{
  "errors": [
    {
      "message": "Throttled: Please retry after 1 second",
      "extensions": {
        "code": "THROTTLED"
      }
    }
  ]
}
```

**Handling Strategy:**
```typescript
// Exponential backoff
async function executeGraphQL(query, variables, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await shopifyGraphQL(query, variables);
    } catch (error) {
      if (error.code === 'THROTTLED') {
        const delayMs = Math.pow(2, attempt) * 1000; // 1s, 2s, 4s
        await sleep(delayMs);
        continue;
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}
```

### Cost Estimation for Common Operations

| Operation | Query Cost | Estimated Time |
|-----------|-----------|----------|
| Get 25 products | ~8 | < 100ms |
| Get 10 customers | ~5 | < 100ms |
| Get 5 orders (with items) | ~12 | < 200ms |
| Create product | ~15 | < 300ms |
| Update customer | ~3 | < 100ms |
| Get collections | ~6 | < 100ms |

**Claude Code Integration:**
- Log query cost in debug output
- Warn if approaching rate limit (>80% capacity)
- Automatically batch requests when possible

---

## Error Handling

### GraphQL Error Types

**1. Validation Errors (4xx equivalent)**
```json
{
  "errors": [
    {
      "message": "Field 'xyz' doesn't exist on type 'Product'",
      "extensions": {
        "code": "INVALID_QUERY"
      }
    }
  ]
}
```

**Claude Code Translation:**
```
❌ Validation error: Field 'xyz' doesn't exist
   (Check field name spelling and available fields)
```

**2. Authentication Errors**
```json
{
  "errors": [
    {
      "message": "Invalid API access token",
      "extensions": {
        "code": "UNAUTHENTICATED"
      }
    }
  ]
}
```

**Claude Code Translation:**
```
❌ Authentication failed
   Check SHOPIFY_ACCESS_TOKEN is set correctly
   Verify token hasn't been revoked in Shopify admin
```

**3. Rate Limit Errors (429 equivalent)**
```json
{
  "errors": [
    {
      "message": "Throttled: Please retry after 1 second",
      "extensions": {
        "code": "THROTTLED"
      }
    }
  ]
}
```

**Claude Code Translation:**
```
⚠️  Rate limited - retrying in 2 seconds...
```

**4. User Permission Errors**
```json
{
  "errors": [
    {
      "message": "You don't have access to this resource",
      "extensions": {
        "code": "ACCESS_DENIED"
      }
    }
  ]
}
```

**Claude Code Translation:**
```
❌ Permission denied
   This token lacks scope 'write_products'
   Update app scopes in Shopify admin
```

---

## Phase 2 Feature Integration

### Planned Additions (Post-v1.0)

**From amir-bengherbi/shopify-mcp-server:**

1. **get-collections**
   ```graphql
   query GetCollections($first: Int!) {
     collections(first: $first) {
       edges { node { id, title, handle, description } }
     }
   }
   ```

2. **create-discount**
   ```graphql
   mutation CreateDiscount($input: DiscountCodeBasicInput!) {
     discountCodeBasicCreate(input: $input) {
       discountCodeBasic { id, codeError, codes(first: 1) { nodes } }
     }
   }
   ```

3. **create-draft-order**
   ```graphql
   mutation CreateDraftOrder($input: DraftOrderInput!) {
     draftOrderCreate(input: $input) {
       draftOrder { id, invoiceUrl, statusUrl }
     }
   }
   ```

4. **manage-webhook**
   ```graphql
   mutation CreateWebhook($input: WebhookSubscriptionInput!) {
     webhookSubscriptionCreate(input: $input) {
       webhookSubscription { id, topic, endpoint }
     }
   }
   ```

---

## Testing Strategy

### Unit Tests (Query Validation)
```typescript
describe('Shopify Queries', () => {
  it('should fetch products with correct shape', async () => {
    const result = await getProducts({ first: 5 });
    expect(result).toHaveProperty('edges');
    expect(result.edges[0]).toHaveProperty('node.id');
    expect(result.edges[0].node).toHaveProperty('title');
  });

  it('should handle pagination cursor', async () => {
    const result = await getProducts({
      first: 5,
      after: 'cursor123'
    });
    expect(result.pageInfo).toHaveProperty('endCursor');
  });
});
```

### Integration Tests (Against Shopify Sandbox)
```bash
# Use Shopify development store for testing
export SHOPIFY_STORE=testing-store.myshopify.com
export SHOPIFY_ACCESS_TOKEN=<sandbox-token>

npm test -- --integration
```

### Error Simulation
```typescript
// Test rate limiting retry behavior
const mockThrottledResponse = {
  errors: [{ message: 'Throttled', code: 'THROTTLED' }]
};

// Test authentication failure
const mockAuthError = {
  errors: [{ message: 'Invalid token', code: 'UNAUTHENTICATED' }]
};
```

---

## Performance Targets

### Query Response Times (SLA)

| Operation | p50 | p95 | p99 |
|-----------|-----|-----|-----|
| Get Products (25) | 50ms | 150ms | 500ms |
| Get Customers (10) | 40ms | 120ms | 400ms |
| Get Orders (5) | 60ms | 200ms | 600ms |
| Create Product | 100ms | 300ms | 800ms |
| Update Customer | 30ms | 100ms | 300ms |

**Monitoring in Claude Code:**
```
Query: get-products
├─ Time: 87ms
├─ Cost: 8/4.0
├─ Status: ✓ Success
└─ Result: 25 products fetched
```

---

## Migration Path from Other Solutions

### If using amir-bengherbi/shopify-mcp

**Migration Steps:**
1. Export access token and configuration from old setup
2. Uninstall `amir-bengherbi/shopify-mcp-server`
3. Install `GeLi2001/shopify-mcp` via skill installer
4. Import configuration (store URL, token)
5. Test existing workflows (backward compatible tools)
6. Access new features (Phase 2+)

**Breaking Changes:** None expected (get-products, get-customers, get-orders preserved)

### If using direct SDK

**No migration needed:** Skill wraps the MCP server, existing SDK usage continues independently.

---

## Deployment Checklist

- [ ] GeLi2001/shopify-mcp cloned and tested locally
- [ ] GraphQL endpoint connectivity verified
- [ ] Access token scopes documented
- [ ] Rate limiting behavior tested
- [ ] Error handling covers all GraphQL error types
- [ ] Pagination tested (25+ products)
- [ ] TypeScript types exported from MCP
- [ ] Integration tests passing against sandbox store
- [ ] Documentation complete (SKILL.md)
- [ ] Example usage provided for each tool
- [ ] Security review of token storage
- [ ] Performance baselines established

---

## References

**GeLi2001/shopify-mcp:**
- GitHub: https://github.com/GeLi2001/shopify-mcp
- Installation: `npx shopify-mcp`

**Shopify GraphQL Admin API:**
- Docs: https://shopify.dev/docs/api/admin-graphql
- Scopes: https://shopify.dev/docs/api/admin-rest/2025-01/resources/oauth-scopes
- Rate Limits: https://shopify.dev/docs/api/admin-graphql/2025-01/rate-limits

**amir-bengherbi/shopify-mcp-server (Phase 2 reference):**
- GitHub: https://github.com/amir-bengherbi/shopify-mcp-server

---

**Document Version:** 1.0
**Last Updated:** January 29, 2026
**Status:** Ready for Implementation
