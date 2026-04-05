# Shopify Catalog Patterns & Comparison

## Comparison Matrix

| Mechanism | Scope | Org? | Filter? | Structured? | Best for | Avoid when |
|-----------|-------|------|---------|-------------|----------|------------|
| Product record | Product | Yes | Indirect | Partial | Base sellable entity | Need reusable custom schemas |
| Options | Product structure | Partial | Yes | Partial | Shopper-selectable dimensions | Attr doesn't create real sellable combos |
| Variants | Variant | Yes | Indirect | Yes | Real SKUs / inventory / price diffs | Only need descriptive attributes |
| Product category | Taxonomy | Yes | Yes | Partial | Standard classification, channels, tax | Need freeform merchant labels |
| Category metafields | Attribute layer | Yes | Yes | Yes | Standardized filterable attributes | Attr not category-relevant |
| Product type | Product | Yes | Yes | No | Merchant-defined classification | Need taxonomy-aware classification |
| Vendor | Product | Yes | Yes | No | Brand/supplier grouping | Need multi-value grouping |
| Tags | Resource label | Yes | If surfaced | No | Loose labels | Durable schema or precise faceting |
| Manual collections | Collection | Yes | No | No | Curated merchandising pages | Need auto-updating rules |
| Smart collections | Collection | Yes | No | No | Rule-based grouping | Need per-variant or editorial precision |
| Metafields | Many resources | Yes | Yes | Yes | Typed custom fields | Need reusable multi-field records |
| Metaobjects | Standalone | Yes | Via refs | Yes | Reusable structured entities | One simple attached field is enough |
| Storefront filters | Storefront | No | Yes | No | Faceted browsing UX | Internal organization only |
| Search controls | Storefront search | No | Search only | No | Relevance tuning | Data model itself is wrong |
| Visibility controls | Product/channel | Yes | Indirect | No | Publishing/discoverability control | Only need navigation changes |
| SEO listing | Product SEO | Partial | No | No | External search snippets | Storefront search tuning |
| Combined listings | Storefront grouping | Partial | Indirect | Partial | Group products into one listing | Normal variants are sufficient |

## Common Patterns

### Apparel Catalog (Size/Color Variants)

```
Product Category: Apparel > [specific taxonomy node]
Options: Size, Color (→ variants for all combos)
Category Metafields: Standardized color (with swatch support), material, size system
Collections:
  - Smart: "Women's Tops" (category condition), "Sale" (tag condition)
  - Manual: "New Arrivals", "Editor's Picks"
Filters: Size, Color, Price, Availability, Material (via category metafield)
```

### Electronics Catalog (Technical Specs)

```
Product Category: Electronics > [specific node]
Options: Only real purchasable dimensions (storage, color)
Custom Metafields: Wattage, compatibility, connectivity, dimensions (typed definitions)
Category Metafields: Use where taxonomy provides standard attrs
Collections:
  - Smart: "Laptops" (category), "Under $500" (price + category)
Filters: Brand (vendor), price, specs (via metafield filters)
```

### Furniture / Home (Material + Finish)

```
Product Category: Home > Furniture > [node]
Options: Size, Finish (if truly different SKUs)
Metaobjects: "Material" (name, composition, care instructions, sustainability rating)
  → Referenced via metafield on products
Category Metafields: Standard attrs where available
Metafields: Dimensions, weight capacity, assembly required (boolean)
Collections:
  - Smart: By room ("Living Room"), by material
Filters: Material (metaobject ref), price, dimensions
```

### Food / Supplements (Reusable Ingredients)

```
Product Category: Food > [node]
Metaobjects: "Ingredient" (name, origin, allergen info, nutritional data)
  → List of metaobject references on each product
Metafields: Serving size, calories, certifications
Tags: Dietary labels for quick admin grouping ("vegan", "gluten-free")
  → But use metafields for storefront filtering
Collections:
  - Smart: By dietary need (metafield conditions)
Filters: Dietary (metafield), allergens (metafield), price
```

### B2B / Wholesale (Visibility-Controlled)

```
Standard product modeling for catalog
Visibility: Unlisted products for direct-link-only wholesale items
Publishing: Channel-specific (wholesale channel vs retail storefront)
Metafields: Minimum order quantity, wholesale pricing tiers, lead time
Collections:
  - Manual: Wholesale-specific curated collections
  - Smart: By vendor for supplier-organized catalogs
```

## Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
|-------------|-------------|-----------------|
| Tags as structured data | Untyped, no validation, messy at scale | Metafields with definitions |
| Tags for storefront filters | Shopify recommends against it | Category metafields or custom metafield filters |
| Collections as filters | Collections are product sets, not facets | Search & Discovery filters |
| Options for non-purchasable attrs | Creates phantom variants with no inventory/price diff | Metafields |
| "Not in any collection" = hidden | Product still in search, recommendations, direct URL | Status/publishing/unlisted/seo.hidden |
| Product type instead of category | Loses taxonomy benefits (channels, tax, category attrs) | Use category first, type for supplementary |
| One mega-product with 2048 variants | Theme/app/Liquid compat issues, performance concerns | Split into separate products or combined listings |
| Metafields without definitions | No admin UI, no validation, not filterable | Always create metafield definitions |
| Metaobjects for simple values | Unnecessary complexity | Single metafield with definition |
