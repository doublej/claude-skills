# DDD Primer: What Ubiquitous Language Is

The term **ubiquitous language** comes from Eric Evans' *Domain-Driven Design* (2003). One of the most useful and most ignored ideas in software.

## The idea

One concept → one word. Used by everyone. Everywhere.

- Domain experts (the people who understand the problem) speak it.
- Product managers write it in tickets.
- Designers label it in mockups.
- Engineers name their classes / functions / tables with it.
- The agent reads it from `GLOSSARY.md` and uses the same word back.

When all of these align, translation cost disappears. When they don't, every conversation has hidden ambiguity:

> "Did you add the wallpaper to the product page?"
> "I added the WallDecoration to the catalogue."
> *(...are those the same thing?)*

## Related terms (not the same)

| Term | What it is | Scope |
|------|-----------|-------|
| **Ubiquitous language** | Shared vocabulary across humans + code + agents | Whole project / bounded context |
| **Domain glossary** | The artifact — the written list of terms | A document |
| **Nomenclature** | Formal naming system in a scientific field | Discipline-wide |
| **Lexicon** | Set of words used in a domain | Linguistic |
| **Ontology** | Terms + the relationships between them | Semantic graph (heavier) |
| **Taxonomy** | Hierarchical classification | Categorisation, not vocabulary |
| **Naming conventions** | Rules for *how* to form names (camelCase) | Style, not meaning |
| **Style guide** | Naming + formatting + tone | Broader |

Ubiquitous language is the **practice**. The glossary is the **artifact**. Don't conflate them.

## Bounded contexts

Evans' second key idea: vocabulary is **scoped to a bounded context**. The word `Order` means something different in *Sales* (a customer purchase) vs *Fulfilment* (a warehouse pick-list) vs *Accounting* (a journal entry).

In a small project: one glossary, no bounded contexts to worry about.

In an ecosystem with multiple sub-projects (e.g. `pimpelmees/wallgen`, `pimpelmees/shopify-template`, `pimpelmees/product-model`): each sub-project is a candidate bounded context. Options:

1. **Single shared glossary** at ecosystem root (`pimpelmees/GLOSSARY.md`). Best when concepts are mostly shared.
2. **Per-context glossaries** (`wallgen/GLOSSARY.md`, `shopify-template/GLOSSARY.md`). Best when the same word legitimately means different things in different contexts. The ecosystem root then carries a **context map** explaining the translations.

Default: start with one shared glossary. Split only when you hit real conflicts.

## Why agents make it worse

Agents amplify vocabulary drift in three ways:

1. **They invent synonyms.** Given the prompt "build the wallpaper API", an agent may use `Wallpaper`, `Paper`, `Decor`, `Mural` across different functions in the same session.
2. **They mirror the user's word.** If you said "decoration" in one message and "product" in the next, the agent will use both.
3. **They borrow framework defaults.** "Item", "Resource", "Entity" leak in from training data.

A glossary kills all three at the root. The agent reads the canonical term and rejected synonyms at session start; drift stops.

## When you don't need this

- Solo throwaway scripts.
- Pure infra/devops projects (no domain — vocabulary IS the framework).
- Projects with fewer than ~5 domain nouns.

Otherwise: yes you need it. Even a 10-term glossary pays off.

## Further reading

- Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software* (2003) — chapter on Ubiquitous Language
- Vaughn Vernon, *Implementing Domain-Driven Design* (2013) — practical patterns
- Martin Fowler, [bliki: UbiquitousLanguage](https://martinfowler.com/bliki/UbiquitousLanguage.html)
- Martin Fowler, [bliki: BoundedContext](https://martinfowler.com/bliki/BoundedContext.html)
