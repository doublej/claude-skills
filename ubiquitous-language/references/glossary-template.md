# Glossary Template

Canonical structure for `GLOSSARY.md`. Copy, fill, prune.

---

```markdown
# {Project Name} Glossary

The vocabulary of this project. One concept → one canonical term. Use these exact words in code, commits, docs, conversations, and agent prompts.

If you find yourself reaching for a synonym, check the **Rejected synonyms** lists below — your word is probably there with a pointer to the canonical term.

Last updated: YYYY-MM-DD

## Core Concepts

### {CanonicalTerm}
{One-sentence definition. What it IS, not what it does. Plain language, no code refs.}
- **Rejected synonyms:** {Synonym1}, {Synonym2}, {Synonym3} — do not use
- **Related:** [[OtherTerm]], [[AnotherTerm]]
- **Examples:** {optional — one or two real examples from the domain}

### {NextTerm}
...

## Process Vocabulary

Verbs and workflow names. Same rules — pick one, list rejected forms.

### {generate}
The act of producing a {Product} from a {Prompt} through the {Wallgen} pipeline.
- **Rejected synonyms:** render, create, make, produce
- **Related:** [[Generation]], [[Prompt]]

## Roles

People or actors in the system. Even if just one human, name the role.

### Customer
End user who purchases {Product}s through the storefront.
- **Rejected synonyms:** user, buyer, account holder, shopper
- **Related:** [[Order]]

## Out of Scope

Terms intentionally NOT used and why. This prevents the glossary from being asked "where is X?" forever.

- **Wallpaper** — too narrow; we sell more than wallpaper. Use [[Product]].
- **Item** — too generic; SKUs are [[Product]]s, line entries on an order are [[OrderLine]]s.
- **Render** — implies graphics-pipeline meaning. Use [[Generation]] for the async business event.
```

---

## Worked example (pimpelmees/wallgen)

```markdown
# Wallgen Glossary

The vocabulary of the wallpaper generation ecosystem. One concept → one canonical term.

Last updated: 2026-05-16

## Core Concepts

### Product
A purchasable wall art SKU in the Shopify catalogue. Has one or more [[Variant]]s (sizes/materials).
- **Rejected synonyms:** WallDecoration, Wallpaper, Decoration, Item, SKU
- **Related:** [[Variant]], [[Order]], [[Generation]]
- **Examples:** "Mossy Forest Mural", "Bauhaus Geometry 02"

### Generation
A single async render request: from [[Prompt]] to finished image, processed by the wallgen FastAPI service.
- **Rejected synonyms:** Job, Task, Render, WallgenRequest
- **Related:** [[Product]], [[Prompt]]

### Prompt
The text input that drives a [[Generation]]. May include style modifiers and aspect ratio.
- **Rejected synonyms:** Query, Description, Input
- **Related:** [[Generation]]

### Variant
A specific size + material combination of a [[Product]]. Maps to a Shopify Variant.
- **Rejected synonyms:** Size, Option, SKUVariant
- **Related:** [[Product]]

### Order
A customer purchase containing one or more [[OrderLine]]s. Maps to a Shopify Order.
- **Rejected synonyms:** Purchase, Sale, Transaction
- **Related:** [[Customer]], [[OrderLine]]

## Process Vocabulary

### generate
Produce a finished image from a [[Prompt]] via the wallgen pipeline.
- **Rejected synonyms:** render, create, make

### publish
Push a generated image as a new [[Product]] (or [[Variant]]) into Shopify.
- **Rejected synonyms:** upload, sync, deploy

## Roles

### Customer
End-user who purchases [[Product]]s via the Shopify storefront.
- **Rejected synonyms:** user, buyer, shopper

### Operator
Internal user who runs [[Generation]]s and curates [[Product]] launches. (Currently: just JJ.)
- **Rejected synonyms:** admin, user, designer

## Out of Scope

- **Wallpaper** — too narrow; we sell murals, posters, prints too. Use [[Product]].
- **Decoration** — used in product copy for SEO but never in code or process language.
- **Item** — Shopify uses it for line entries; we use [[OrderLine]] to avoid ambiguity.
```

---

## Sizing guidance

| Terms | Treatment |
|-------|-----------|
| < 10 | Inline in CLAUDE.md, no separate file |
| 10-50 | Standalone GLOSSARY.md at project root |
| 50-100 | Split into Core / Process / Roles / Out-of-Scope sections (as above) |
| > 100 | Split per bounded context — separate GLOSSARY.md per sub-project, plus a context-map at ecosystem root |
