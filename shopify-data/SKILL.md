---
name: shopify-data
description: "Product data architecture: variants, metafields, collections, filters, catalog"
---

# Shopify Data Architecture

Architect product data models using Shopify's native mechanisms correctly.

## Four Layers

| Layer | Mechanisms | Answers |
|-------|-----------|---------|
| **Structure** | Products, options, variants | What is sold? What combinations are purchasable? |
| **Classification** | Category, product type, vendor, tags, collections | What kind of thing is this? How is it grouped? |
| **Discovery** | Filters, search controls, visibility, SEO | How do shoppers find it? |
| **Extensibility** | Metafields, category metafields, metaobjects | What custom data is needed beyond defaults? |

## Decision Framework

### "Where should this attribute live?"

```
Is this a purchasable dimension (size, color, storage)?
  YES → Option + Variant
  NO ↓

Does Shopify's taxonomy standardize it for this category?
  YES → Category metafield
  NO ↓

Is it a single typed value on the product/variant?
  YES → Custom metafield (with definition)
  NO ↓

Is it a reusable entity with multiple fields (ingredient, material spec)?
  YES → Metaobject + reference metafield
  NO ↓

Is it a loose internal label or temporary grouping?
  YES → Tag
  NO → Reconsider; likely one of the above
```

### "How should I group products?"

```
Curated, hand-picked assortment?
  → Manual collection

Rule-based, auto-updating group?
  → Smart collection (up to 60 conditions, 5000 max)

Separate products that should browse as one listing?
  → Combined listings (Plus/enterprise only)
```

### "How do shoppers filter?"

```
Storefront faceted browsing needs Search & Discovery app + compatible theme.
Max 25 filters per store. Each source used once.

Standard sources: availability, price, vendor, product type, category
Custom sources: options, category metafields, product/variant metafields, metaobject refs

Tags CAN be a filter source but Shopify recommends structured alternatives.
Filters unavailable on collections >5000 products or searches >100K results.
```

## Critical Distinctions

| Confusion | Reality |
|-----------|---------|
| Tags = structured data | Tags are flat, untyped labels. Use metafields for structured data. |
| Collections = filters | Collections define product sets. Filters refine within them. |
| Product type = category | Category is Shopify-standardized (taxonomy). Type is merchant-defined. |
| Options = attributes | Options create purchasable variant combos. Metafields for non-sellable attrs. |
| "Not in collection" = hidden | Use status/publishing/unlisted/seo.hidden for real visibility control. |

## Key Constraints

| Mechanism | Limit |
|-----------|-------|
| Options per product | 3 |
| Variants per product | 2,048 (theme/app compat varies; Liquid caps at 250) |
| Tags per product | 250 (standard), more on Plus |
| Smart collection conditions | 60 per collection |
| Smart collections total | 5,000 |
| Storefront filters | 25 per store |
| Product category | 1 per product (Shopify taxonomy) |
| Product type | 1 per product (merchant-defined) |
| Vendor | 1 per product (defaults to store name) |

## Workflow

1. **Classify** — Assign product category from Shopify taxonomy first
2. **Structure** — Model purchasable dimensions as options/variants
3. **Extend** — Category metafields for standardized attrs, custom metafields for the rest
4. **Group** — Collections for merchandising (manual or smart)
5. **Filter** — Configure Search & Discovery filters from structured sources
6. **Tune** — Synonyms, boosts, predictive search settings
7. **Control** — Visibility via status, publishing, unlisted, seo.hidden

## References

For detailed mechanism descriptions, see `references/mechanisms.md`.
For common catalog patterns and comparison matrix, see `references/patterns.md`.

Grep patterns:
- Mechanism details: `grep -n "^### " references/mechanisms.md`
- Specific mechanism: `grep -n "Product category\|Category metafield\|Metaobject\|Smart collection" references/mechanisms.md`
- Patterns: `grep -n "^###" references/patterns.md`
