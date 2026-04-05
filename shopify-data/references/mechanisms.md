# Shopify Product Organization Mechanisms

Detailed reference for each native mechanism. Use the decision framework in SKILL.md first; consult this file for specifics.

## Structure Layer

### Product Record

The base product object: title, description, media, category, variants, metafields, status, publishing, organization fields, SEO listing.

- **Scope**: Product
- **Best for**: Core sellable entity, human-facing content, anchoring variants/collections/metafields
- **Avoid**: Putting variant-specific data (price, SKU, inventory) at product level
- **Storefront**: Title, description, media, status, publishing all affect presence
- **Search**: Base unit returned in search/collection browsing

### Options

Shopper-selectable dimensions (Size, Color, Material). Option values combine into variants.

- **Scope**: Product structure → generates variant combinations
- **Limit**: 3 options per product, up to 2,048 variants
- **Best for**: Real purchasable dimensions shoppers choose between
- **Avoid**: Non-sellable descriptive attributes that don't need distinct SKUs
- **Filtering**: Can be storefront filter sources; if migrated to category metafields, use those instead
- **Alternatives**: Category metafields (standardized attrs), custom metafields (descriptive data)

### Variants

Specific purchasable combinations of option values (e.g., "Blue / Large"). Each variant carries its own price, SKU, barcode, inventory, weight, and media.

- **Scope**: Variant (child of product)
- **Limit**: 2,048 per product; Liquid `product.variants` caps at 250; theme/app/channel compat varies
- **Best for**: True sellable permutations with separate inventory/pricing
- **Avoid**: Purely descriptive data that doesn't need separate SKU/inventory
- **Collections**: Include whole products, not individual variants
- **Smart collections**: Can match on variant metafields, but pull in the whole product
- **Alternatives**: Combined listings (group separate products); metafields (add data without creating SKUs)

## Classification Layer

### Product Category (Shopify Standard Taxonomy)

Standardized category from Shopify's predefined taxonomy. Enables category metafields, channel alignment, tax calculations, analytics.

- **Scope**: Product classification
- **Limit**: 1 per product; must come from Shopify taxonomy; uncategorized if not set
- **Best for**: Normalized classification for taxonomy-driven features, channels, taxes
- **Avoid**: Freeform internal labels (use product type instead)
- **Filtering**: Standard storefront filter source; unlocks category-specific attributes as additional filter sources
- **Guidance**: Shopify recommends assigning category first, before product type

### Category Metafields (Standard Product Attributes)

Standardized attributes tied to the assigned product category (color, size, material, etc.).

- **Scope**: Product attribute layer linked to taxonomy
- **Best for**: Standardized filterable attributes recognized across Shopify ecosystem
- **Avoid**: Attributes not relevant to the category
- **Dependencies**: Require product category assignment
- **Filtering**: Can be filter sources; when present, preferred over product-option filters
- **Swatches**: Color entries can render as swatches
- **Category change**: Shopify tries to retain values and variant connections when category changes

### Product Type

Merchant-defined custom classification field. Lighter weight than category.

- **Scope**: Product classification
- **Limit**: 1 per product; freeform text
- **Best for**: Internal segmentation, reporting, merchant-specific categorization
- **Avoid**: When you need taxonomy/tax/channel alignment (use category)
- **Filtering**: Standard filter source; indexed by search
- **Guidance**: Shopify says use standard categories first; type only when taxonomy doesn't fit

### Vendor

Product vendor/manufacturer/brand field.

- **Scope**: Product classification
- **Limit**: 1 per product; defaults to store name if unset
- **Best for**: Brand pages, supplier reporting, vendor filtering
- **Avoid**: Multi-value brand tagging; general grouping (use collections)
- **Filtering**: Standard filter source; values based on store's default language

### Tags

Flat text labels on products and other resources.

- **Scope**: Resource-level labels
- **Limit**: 250 per product (standard); not case-sensitive
- **Best for**: Loose internal grouping, temporary labels, smart-collection criteria, search assistance
- **Avoid**: Structured attribute systems, durable integrations, precise storefront faceting
- **Filtering**: Can be filter source if explicitly enabled; values display in default language only
- **Search**: Indexed for storefront search matching; no typo tolerance on tags; invisible to external search engines
- **Guidance**: Shopify recommends storefront filters over tag-based filtering UX

## Grouping Layer

### Manual Collections

Merchant explicitly selects which products belong.

- **Scope**: Product grouping / storefront navigation
- **Plan**: Basic and higher (Starter doesn't support collections)
- **Best for**: Curated assortments, seasonal edits, campaign pages, editor's picks
- **Avoid**: When behavior should be rule-driven and auto-updating
- **Constraints**: Whole products only (not individual variants); cannot convert from smart collections

### Smart Collections (Automatic)

Rule-based collections that auto-include matching products.

- **Scope**: Rule-based merchandising
- **Limit**: 60 conditions per collection; 5,000 smart collections per store
- **Best for**: "All from vendor X", "all red dresses", category-based assortments
- **Avoid**: Precise editorial control; per-variant inclusion
- **Conditions**: Product category, exact tag matches, activated product/variant metafield definitions (including metaobject references)
- **Metafield limits**: Limited number of definitions can be activated for smart collection use

## Extensibility Layer

### Metafields

Typed custom fields on products, variants, collections, orders, and more.

- **Scope**: Custom data on many resource types
- **Best for**: Technical specs, badges, dates, files, compatibility data, filter sources
- **Avoid**: When category metafields already model it; when you need a reusable multi-field entity (use metaobjects)
- **Definitions**: Required for admin editing, validation, type safety, smart collection use, and filter use
- **Filtering**: Product and variant metafields can be filter sources and smart collection conditions (eligible types only)
- **Theme**: Displayed via dynamic sources if theme supports them

### Metaobjects

Reusable standalone structured content objects with multiple fields.

- **Scope**: Custom data model / standalone objects
- **Best for**: Ingredient records, material specs, care instructions, brand stories, reusable swatches
- **Avoid**: When a simple single metafield would do
- **Attachment**: Reference via metafield definition on products/variants/etc.
- **Filtering**: Search & Discovery supports metafield filters based on metaobject references (including visual filters)
- **Storefront**: Surfaced via themes/Storefront API; depends on storefront access settings

## Discovery Layer

### Storefront Filters (Search & Discovery)

Faceted filtering on collection pages and search results.

- **Scope**: Storefront discovery
- **Requirements**: Search & Discovery app + compatible theme
- **Limit**: 25 filters per store; each source used once
- **Standard sources**: Availability, price, vendor, product type, category
- **Custom sources**: Options, category metafields, product/variant metafields, metaobject references
- **Unavailable**: Collections >5,000 products; searches >100K results
- **Price filter**: Default currency only

### Search Controls

Synonyms, product boosts, semantic search, predictive search, result-type settings.

- **Scope**: Storefront search tuning
- **Synonyms**: Online store only
- **Predictive search**: Grow/Advanced/Plus only; requires theme/API support
- **Semantic search**: Plan-limited; excludes predictive search, Japanese; requires <200K products
- **Product boosts**: Sync with metafield; can be bulk-edited or updated via Shopify Flow
- **Guidance**: Complements filters; does not replace proper data modeling

### Visibility Controls

Product status (active/draft/archived), channel publishing, unlisted status, `seo.hidden`.

- **Status**: Controls whether product is available at all
- **Publishing**: Product-level, not variant-level; controls per-channel availability
- **Unlisted**: Direct URL only; excluded from search, collections, recommendations
- **seo.hidden**: Hides from sitemaps, search engines, and storefront search; still appears in collections and recommendations
- **Key difference**: Unlisted is broader exclusion than seo.hidden

### SEO Listing / Handle

Page title, meta description, URL handle for external search engines.

- **Scope**: Product SEO metadata
- **Best for**: External search engine click-through and URL control
- **Avoid**: Expecting it to affect Shopify storefront search
- **Handle**: Auto-generated on creation; avoid changing frequently

### Combined Listings

Combine separate products into one storefront browse experience.

- **Scope**: Advanced storefront merchandising
- **Plan**: Plus and enterprise only; requires compatible theme
- **Best for**: Separate products that should appear as one listing
- **Avoid**: When normal variants are sufficient
- **Caveats**: Online storefront only; child products excluded from filter results for product options; search/recommendation display is configurable
