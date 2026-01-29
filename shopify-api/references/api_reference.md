# Shopify API Reference

## GraphQL Mutations

### Product Mutations

```graphql
# Create product
mutation productCreate($input: ProductInput!) {
  productCreate(input: $input) {
    product { id title handle }
    userErrors { field message }
  }
}

# Variables
{
  "input": {
    "title": "Product Name",
    "descriptionHtml": "<p>Description</p>",
    "vendor": "Vendor",
    "productType": "Type",
    "status": "DRAFT",
    "variants": [{ "price": "29.99", "sku": "SKU-001" }]
  }
}
```

```graphql
# Update product
mutation productUpdate($input: ProductInput!) {
  productUpdate(input: $input) {
    product { id title }
    userErrors { field message }
  }
}

# Variables
{ "input": { "id": "gid://shopify/Product/123", "title": "New Title" } }
```

```graphql
# Delete product
mutation productDelete($input: ProductDeleteInput!) {
  productDelete(input: $input) {
    deletedProductId
    userErrors { field message }
  }
}

# Variables
{ "input": { "id": "gid://shopify/Product/123" } }
```

### Inventory Mutations

```graphql
# Adjust inventory
mutation inventoryAdjustQuantity($input: InventoryAdjustQuantityInput!) {
  inventoryAdjustQuantity(input: $input) {
    inventoryLevel { available }
    userErrors { field message }
  }
}

# Variables
{
  "input": {
    "inventoryLevelId": "gid://shopify/InventoryLevel/123",
    "availableDelta": 10
  }
}
```

### Order Mutations

```graphql
# Update order
mutation orderUpdate($input: OrderInput!) {
  orderUpdate(input: $input) {
    order { id tags }
    userErrors { field message }
  }
}

# Variables
{ "input": { "id": "gid://shopify/Order/123", "tags": ["vip", "priority"] } }
```

```graphql
# Cancel order
mutation orderCancel($orderId: ID!, $reason: OrderCancelReason!, $refund: Boolean!, $restock: Boolean!) {
  orderCancel(orderId: $orderId, reason: $reason, refund: $refund, restock: $restock) {
    orderCancelUserErrors { field message }
    job { id }
  }
}

# Variables
{
  "orderId": "gid://shopify/Order/123",
  "reason": "CUSTOMER",
  "refund": true,
  "restock": true
}
```

### Customer Mutations

```graphql
# Create customer
mutation customerCreate($input: CustomerInput!) {
  customerCreate(input: $input) {
    customer { id email }
    userErrors { field message }
  }
}

# Variables
{
  "input": {
    "email": "customer@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "tags": ["newsletter"]
  }
}
```

```graphql
# Update customer
mutation customerUpdate($input: CustomerInput!) {
  customerUpdate(input: $input) {
    customer { id tags }
    userErrors { field message }
  }
}

# Variables
{ "input": { "id": "gid://shopify/Customer/123", "tags": ["vip", "loyalty"] } }
```

### Discount Mutations

```graphql
# Create discount code
mutation discountCodeBasicCreate($basicCodeDiscount: DiscountCodeBasicInput!) {
  discountCodeBasicCreate(basicCodeDiscount: $basicCodeDiscount) {
    codeDiscountNode { id }
    userErrors { field message }
  }
}

# Variables
{
  "basicCodeDiscount": {
    "title": "Summer Sale",
    "code": "SUMMER20",
    "startsAt": "2024-06-01T00:00:00Z",
    "endsAt": "2024-08-31T23:59:59Z",
    "customerGets": {
      "value": { "percentage": 0.20 },
      "items": { "all": true }
    },
    "customerSelection": { "all": true },
    "appliesOncePerCustomer": true
  }
}
```

### Webhook Mutations

```graphql
# Subscribe to webhook
mutation webhookSubscriptionCreate($topic: WebhookSubscriptionTopic!, $webhookSubscription: WebhookSubscriptionInput!) {
  webhookSubscriptionCreate(topic: $topic, webhookSubscription: $webhookSubscription) {
    webhookSubscription { id }
    userErrors { field message }
  }
}

# Variables
{
  "topic": "ORDERS_CREATE",
  "webhookSubscription": {
    "callbackUrl": "https://your-app.com/webhooks/orders",
    "format": "JSON"
  }
}
```

## Common Queries

### Shop Info

```graphql
query {
  shop {
    name
    email
    primaryDomain { url }
    plan { displayName }
    currencyCode
    timezoneAbbreviation
  }
}
```

### Products with Metafields

```graphql
query products($first: Int!, $query: String) {
  products(first: $first, query: $query) {
    edges {
      node {
        id
        title
        handle
        status
        totalInventory
        metafields(first: 5) {
          edges {
            node {
              namespace
              key
              value
            }
          }
        }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
```

### Orders with Line Items

```graphql
query orders($first: Int!, $query: String) {
  orders(first: $first, query: $query) {
    edges {
      node {
        id
        name
        createdAt
        totalPriceSet { shopMoney { amount currencyCode } }
        customer { id email }
        lineItems(first: 10) {
          edges {
            node {
              title
              quantity
              variant { id sku }
            }
          }
        }
        shippingAddress {
          address1
          city
          country
        }
      }
    }
  }
}
```

### Inventory Levels by Location

```graphql
query inventoryLevels($locationId: ID!) {
  location(id: $locationId) {
    name
    inventoryLevels(first: 50) {
      edges {
        node {
          available
          item {
            id
            sku
            variant { product { title } }
          }
        }
      }
    }
  }
}
```

## Query Filters (Search Syntax)

### Product Filters

```
status:active                    # Active products only
vendor:"Brand Name"              # By vendor
product_type:Shoes               # By type
tag:sale                         # By tag
created_at:>2024-01-01           # Created after date
inventory_total:<10              # Low stock
title:*shirt*                    # Title contains
```

### Order Filters

```
financial_status:paid            # Paid orders
fulfillment_status:unfulfilled   # Unfulfilled orders
status:open                      # Open orders
created_at:>=2024-01-01          # Date range
customer_id:123                  # By customer
tag:priority                     # By tag
```

### Customer Filters

```
email:*@example.com              # Email domain
orders_count:>5                  # Repeat customers
total_spent:>100                 # High value
accepts_marketing:true           # Marketing subscribers
tag:vip                          # By tag
```

## Webhook Topics (GraphQL Enum)

| REST Topic | GraphQL Enum |
|------------|--------------|
| orders/create | ORDERS_CREATE |
| orders/updated | ORDERS_UPDATED |
| orders/paid | ORDERS_PAID |
| orders/fulfilled | ORDERS_FULFILLED |
| orders/cancelled | ORDERS_CANCELLED |
| products/create | PRODUCTS_CREATE |
| products/update | PRODUCTS_UPDATE |
| products/delete | PRODUCTS_DELETE |
| customers/create | CUSTOMERS_CREATE |
| customers/update | CUSTOMERS_UPDATE |
| inventory_levels/update | INVENTORY_LEVELS_UPDATE |
| fulfillments/create | FULFILLMENTS_CREATE |
| refunds/create | REFUNDS_CREATE |

## Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 400 | Bad Request | Fix request syntax |
| 401 | Unauthorized | Check access token |
| 402 | Payment Required | Store billing issue |
| 403 | Forbidden | Check API scopes |
| 404 | Not Found | Verify resource ID |
| 422 | Unprocessable | Check userErrors array |
| 423 | Locked | Store is frozen |
| 429 | Too Many Requests | Implement backoff |
| 500 | Server Error | Retry with backoff |
| 503 | Service Unavailable | Retry later |
