---
name: code-glossary
description: "Curate a project's ubiquitous language — the shared vocabulary that humans, code, and AI agents all use for the same concepts. Builds and maintains a domain glossary (GLOSSARY.md) so 'wallpaper' vs 'wall decoration' vs 'product' stop drifting across docs, code, and prompts. Use when starting a new project, when agents keep using wrong words, when team/docs/code diverge on naming, or when onboarding a new agent into a project. Triggers on 'ubiquitous language', 'domain glossary', 'project vocabulary', 'name things consistently', 'we keep calling this different things', 'agent uses wrong word'."
---

# Ubiquitous Language

Curate the **ubiquitous language** of a project — the single shared vocabulary used by domain experts, code, docs, and AI agents. The artifact is a `GLOSSARY.md` at the project root, referenced from `CLAUDE.md` so every agent session loads it.

This is Domain-Driven Design's most practical idea: if the team calls it a "Wall Decoration" but the code calls it `Product` and the design doc calls it "Wallpaper", everyone wastes cycles translating. Agents amplify the cost — they will happily invent a fourth word.

<core_principle>
One concept → one canonical term. Used everywhere: spoken, docs, code identifiers, commit messages, PR titles, agent prompts.
</core_principle>

<when_to_use>
- New project — seed the glossary before code accumulates conflicting names
- Existing project where naming has drifted — agent or contributor used "user" / "customer" / "account" interchangeably
- Cross-project ecosystem (e.g. `pimpelmees/`, `remotevr/`, `project-atlas/`) where shared concepts need shared names
- Before a large refactor — lock vocabulary so the refactor doesn't introduce new synonyms
- Onboarding a new agent or person — glossary IS the onboarding doc
</when_to_use>

<pipeline>
```
Phase 1: SCOPE       detect target, locate existing CLAUDE.md / GLOSSARY.md
Phase 2: HARVEST     extract candidate terms from code, docs, CLAUDE.md, recent commits
Phase 3: CLUSTER     group synonyms; surface conflicts to user
Phase 4: DEFINE      user picks canonical term per cluster; write definition + rejected synonyms
Phase 5: WIRE        write GLOSSARY.md, link from CLAUDE.md, optionally add per-subfolder pointers
Phase 6: ENFORCE     (optional) flag remaining occurrences of rejected synonyms in code/docs
```
</pipeline>

<phase_1_scope>

1. Resolve target project root from `$ARGUMENTS` or current working directory.
2. Read `CLAUDE.md` at project root if present. Note any vocabulary already declared.
3. Check for existing `GLOSSARY.md`, `glossary.md`, `docs/glossary.md`, or `.claude/glossary.md`.
4. If glossary exists → switch to **update mode** (skip to Phase 2 in update-only form). Otherwise → **bootstrap mode**.
5. Detect project ecosystem context. If inside a known multi-project tree (e.g. `multi-stack/pimpelmees/`), check parent CLAUDE.md for ecosystem-level vocabulary.
</phase_1_scope>

<phase_2_harvest>

Extract candidate domain terms. Mechanical pass — Claude judges later.

**Sources, in priority order:**

1. **Existing CLAUDE.md / README.md** — proper nouns, capitalised concepts, anything in `<ecosystems>` / `<folders>` tags.
2. **Top-level directory names** — often domain nouns (`auth/`, `billing/`, `decorations/`).
3. **Exported type names / class names / DB tables** — use Grep:
   ```
   Grep: pattern="^(export )?(class|interface|type|struct|model) ([A-Z]\w+)" type="ts,py,rs,go,swift"
   Grep: pattern="^(CREATE TABLE|class .* Base)" type="sql,py"
   ```
4. **Recent commit messages** — `git log --oneline -100` for living vocabulary.
5. **User-facing strings** (i18n keys, UI labels) if present.

Collect terms with frequency. Skip generic/framework names (`Component`, `Controller`, `Manager`, `Util`).

**Output:** flat list of candidate terms, each with:
- term (as found)
- frequency (occurrences across sources)
- example contexts (file path + line where seen)
</phase_2_harvest>

<phase_3_cluster>

Group candidate terms into **concept clusters**. Each cluster = one real-world thing called multiple names.

Claude does semantic grouping using domain knowledge + context. Examples of typical clusters:

| Concept | Candidate terms found |
|---------|----------------------|
| The end-customer | `User`, `Customer`, `Account`, `Buyer`, `Shopper` |
| A purchasable wall art SKU | `Product`, `Wallpaper`, `WallDecoration`, `Decoration`, `Item`, `SKU` |
| The generation request | `Job`, `Task`, `Generation`, `Render`, `WallgenRequest` |

**Heuristics for clustering:**
- Singular + plural variants → same cluster.
- Abbreviations of the same noun (`Decoration` / `Decor`) → same cluster.
- Words that show up in the same code paths or DB foreign keys → likely same concept.
- When unsure → keep separate, let user decide.

**Conflict surface.** For each cluster with 2+ terms, prepare a snippet showing where each term lives:

```
Cluster: "the purchasable wall art SKU"
  - "Product" (47 uses)         → src/db/models.py, src/api/products.py, README.md
  - "WallDecoration" (12 uses)  → src/decorations/*.py, CLAUDE.md
  - "Wallpaper" (8 uses)        → marketing/site/*, old docs
```

Skip clusters with only one term (no conflict to resolve) — they're already canonical.
</phase_3_cluster>

<phase_4_define>

For each conflicting cluster, ask the user via consult-user-mcp `form`. Batch up to 10 clusters per form (mode `accordion`) — don't ask one at a time.

For each cluster:

```json
{
  "id": "cluster-{slug}",
  "question": "Concept: '{description}'. Found terms: {list}. Pick canonical:",
  "options": ["{term1}", "{term2}", "{term3}"],
  "other": true
}
```

If only one cluster, use single `pick`. If 2-10, use `form` with one choice question per cluster.

**After choices collected**, for each canonical term gather a definition. One short follow-up `text` question per term, OR Claude drafts definitions from context and shows them in one final `form` for confirmation:

```
{canonical_term} — {one-sentence definition}.
Rejected synonyms: {term1}, {term2} (do not use)
Related: [[OtherTerm]]
```

**Definition rules:**
- One sentence. Plain language. No code references in the definition itself.
- State what it IS, not what it does.
- List rejected synonyms explicitly so future contributors (human or agent) know what NOT to use.
- Cross-link related terms with `[[TermName]]` for navigability.
</phase_4_define>

<phase_5_wire>

Write `GLOSSARY.md` at project root. Format defined in `references/glossary-template.md`.

**Structure:**

```markdown
# {Project} Glossary

The vocabulary of this project. One concept → one canonical term. Use these words in code, commits, docs, and conversations.

## Core Concepts

### Product
A purchasable wall art SKU in the catalogue.
- **Rejected synonyms:** WallDecoration, Wallpaper, Decoration, Item, SKU
- **Related:** [[Variant]], [[Order]]

### Generation
A single async render request from prompt to finished image.
- **Rejected synonyms:** Job, Task, Render, WallgenRequest
- **Related:** [[Product]], [[Prompt]]

## Process Vocabulary
(verbs and workflow names)

## Out of Scope
Terms intentionally NOT used by this project and why.
```

**Then wire it in:**

1. **Update CLAUDE.md** — add a `<vocabulary>` section near the top:
   ```xml
   <vocabulary>
   Canonical terms defined in GLOSSARY.md. Use these names exactly — they are the project's ubiquitous language.
   Top 10 most-used: Product, Generation, Variant, Order, Customer, ...
   Full glossary: ./GLOSSARY.md
   </vocabulary>
   ```

2. **For ecosystems** (parent project with sub-projects), write the glossary at the ecosystem root, then add a one-line breadcrumb in each child CLAUDE.md:
   ```
   Vocabulary: see ../GLOSSARY.md
   ```

3. **Commit** as its own atomic commit:
   ```
   docs: add GLOSSARY.md — ubiquitous language for {project}
   ```
</phase_5_wire>

<phase_6_enforce>

Optional. Only if user opted in.

Flag remaining occurrences of **rejected synonyms** in code + docs. Does NOT auto-rename (that's a separate, heavier operation — out of scope for this skill).

1. For each rejected synonym, Grep across project:
   ```
   Grep: pattern="\b{rejected_synonym}\b" exclude="GLOSSARY.md,**/.git/**"
   ```
2. Produce a markdown report `GLOSSARY-violations.md` (or print to stdout):
   ```
   ## Violations

   ### "WallDecoration" → use "Product"
   - src/decorations/models.py:14
   - src/decorations/api.py:8 (3 occurrences)
   - CLAUDE.md:42
   ```
3. Ask user: fix now (route to a separate refactor), defer, or accept.

**Do not auto-rename.** Renaming touches behaviour and requires test gates. Surface the list; let the user decide whether to schedule a refactor.
</phase_6_enforce>

<update_mode>

When `GLOSSARY.md` already exists, run a lighter loop:

1. Read existing glossary.
2. Re-harvest (Phase 2).
3. Identify **new terms** not in glossary AND **uses of rejected synonyms** that appeared since last update.
4. Show the diff to user: "X new terms found, Y rejected-synonym occurrences appeared." Ask which to address.
5. Add only the deltas. Don't rewrite the whole file.
</update_mode>

<reference_files>
- [DDD Primer](references/ddd-primer.md) — what ubiquitous language is, where it came from, how it differs from glossary/taxonomy/ontology
- [Glossary Template](references/glossary-template.md) — canonical GLOSSARY.md structure with examples
</reference_files>

<anti_patterns>
- **Don't define framework terms.** `Component`, `Controller`, `Service`, `Repository` — those are stack vocabulary, not domain vocabulary.
- **Don't pluralise.** Define `Product`, not `Products`. Plurals are derivable.
- **Don't allow two canonical terms for the same concept** "because both feel right." Pick one. The whole point is to stop the drift.
- **Don't let the glossary grow past ~50 core terms.** If it's bigger, split by sub-domain (separate glossary per bounded context).
- **Don't skip rejected-synonyms.** A definition without rejected synonyms is half the value — agents need to know what NOT to say.
</anti_patterns>
