---
name: aeo-geo
description: Audit and optimize websites for AI-engine citation in ChatGPT, Perplexity, Claude, Gemini, Google AI Overviews. Generates llms.txt, robots.txt allowlists, JSON-LD schema, and applies Princeton GEO content methods. Triggers on "AEO", "GEO", "answer engine optimization", "generative engine optimization", "make my site visible to ChatGPT/Perplexity", "llms.txt", "AI search", "AI citations", "LLM SEO".
---

# AEO/GEO — Answer & Generative Engine Optimization

## Overview

Make a website cited by AI engines. Three planes: discoverability (crawlers can reach it), structure (JSON-LD + llms.txt), citability (content evidence Princeton/AutoGEO research shows AI engines reward).

Wrap [`geo-optimizer-skill`](https://github.com/Auriti-Labs/geo-optimizer-skill) (305⭐, Princeton/AutoGEO-backed) for the heavy lifting. Add Princeton method table, framework patterns, and codebase-fix prompts inline.

## When to use

- User wants their site to appear in ChatGPT Search / Perplexity / Claude / Gemini answers
- Adding `llms.txt`, `robots.txt` AI-bot rules, or JSON-LD to a project
- Auditing why a site isn't being cited
- Writing or rewriting content to maximize LLM citation odds

## When NOT to use

- Pure traditional Google SEO without AI angle → use `prompt-crafter` + standard meta/sitemap
- Personal projects with no real audience to capture → skip; not worth the maintenance
- Multi-LLM brand monitoring → see `references/citation-monitoring.md` (separate concern, costs money)

## Step 1 — Detect environment

```bash
# Required
which geo || pip install geo-optimizer-skill
geo --version

# Optional (skip cleanly if missing)
which searchstack 2>/dev/null  # citation monitoring
```

If `geo` install fails: fall back to inline checks in `references/inline-fallback.md`.

## Step 2 — Audit

```bash
geo audit --url https://SITE.com --format text          # human read
geo audit --url https://SITE.com --format json > audit.json
geo audit --sitemap https://SITE.com/sitemap.xml --max-urls 25  # batch
```

Score bands: 0-35 critical · 36-67 foundation · 68-85 good · 86-100 excellent.

Read scoring rubric: `references/princeton-methods.md`.

## Step 3 — Fix discoverability (robots.txt)

The four bots that **must never be blocked** for citation:

| Bot | Engine |
|-----|--------|
| `OAI-SearchBot` | ChatGPT Search citations |
| `PerplexityBot` | Perplexity answer citations |
| `ClaudeBot` | Claude web citations |
| `Google-Extended` | Gemini AI Overviews |

To allow citations but block training data, see `references/robots-patterns.md` (full bot table, 27 AI bots across 3 tiers).

## Step 4 — Generate llms.txt

```bash
geo llms --base-url https://SITE.com \
  --site-name "Site" --description "One sentence." \
  --output ./public/llms.txt
```

Spec: H1 (site name) → blockquote (description) → H2 sections → links. Keep <200 lines. Spec at https://llmstxt.org. Also generate `llms-full.txt` (longer).

## Step 5 — Inject JSON-LD

```bash
geo schema --type website     --url https://SITE.com           > schema.json
geo schema --type organization --url https://SITE.com           >> schema.json
geo schema --type faq         --url https://SITE.com/faq        >> schema.json
geo schema --type article     --url https://SITE.com/post/x     >> schema.json
```

Types: `website`, `webapp`, `faq`, `article`, `organization`, `breadcrumb`. Place in `<head>` or page-specific layouts. Framework patterns: `references/framework-integration.md`.

## Step 6 — Optimize content (Princeton 8-method table)

Apply in priority order. Source: Princeton KDD 2024 (10k Perplexity queries) + AutoGEO ICLR 2026.

| Pri | Method | Lift | Action |
|-----|--------|------|--------|
| 🔴 1 | Cite Sources | +30-115% | Add authoritative external links (gov, edu, journals) |
| 🔴 2 | Add Statistics | +40% | Concrete numbers, percentages, dates |
| 🟠 3 | Quotation Addition | +30-40% | `"Text" — Name, Role, Org, Year` |
| 🟠 4 | Authoritative Tone | +6-12% | Confident expert framing |
| 🟡 5 | Fluency | +15-30% | Clear, direct prose |
| 🟡 6 | Easy-to-Understand | +8-15% | Define terms, analogies |
| 🟢 7 | Technical Terms | +5-10% | Correct industry vocab |
| 🟢 8 | Unique Words | +5-8% | Vary vocabulary |
| ❌ 9 | Keyword Stuffing | ~0% | Do NOT — neutral-to-negative |

Full method matrix + examples: `references/princeton-methods.md`.

## Step 7 — Auto-apply fixes

```bash
geo fix --url https://SITE.com --apply
geo fix --url https://SITE.com --only robots,llms,schema
```

Generates missing files (robots.txt entries, llms.txt, JSON-LD, meta tags, AI discovery endpoints).

## Step 8 — Audit content quality (pre-publish)

Before shipping new content, run a truth pass — AI engines aggressively penalize fabricated stats. Checklist: `references/content-audit.md`.

- Verify every statistic against its cited source
- Check every external link returns 2xx
- Confirm quotes are real (search the exact string)
- Flag uncited claims of fact

## Step 9 — Track over time (optional)

```bash
geo audit --url https://SITE.com --save-history --regression
geo history --url https://SITE.com
geo track --url https://SITE.com --report --output ./report.html
```

## Step 10 — Citation monitoring (optional, costs money)

Only when actively tracking a live brand. Requires API keys. See `references/citation-monitoring.md`.

```bash
pip install searchstack
searchstack ai      # ChatGPT/Perplexity/Claude citation polling
searchstack geo     # Google AI Overview tracking
```

## Framework integration

Pick the entry-point file for the stack:

- **Astro**: `astro.config.mjs` integration
- **Next.js**: `next.config.mjs` + postbuild script
- **SvelteKit**: `+page.server.ts` for JSON-LD; `static/llms.txt`
- **Vite/Nuxt**: plugin or `nuxt.config.ts`
- **Static**: drop files in `public/` or `static/`

Snippets for each: `references/framework-integration.md`.

## Output convention

When asked to "improve AEO/GEO" on a codebase, produce a fix list ordered by impact:

```
1. [CRITICAL] robots.txt blocks ClaudeBot — remove line 12
2. [HIGH]     no llms.txt at /llms.txt — generated, write to public/
3. [MEDIUM]   missing FAQPage JSON-LD on /faq — patch added
4. [LOW]      no <html lang> on layout — set "en"
```

Ship as a PR-style diff list, not prose.

## References

- `references/princeton-methods.md` — 47-method scoring rubric, examples, evidence
- `references/robots-patterns.md` — 27 AI bots, allow/block patterns, CDN gotchas
- `references/framework-integration.md` — Astro/Next/SvelteKit/Vite/Nuxt snippets
- `references/content-audit.md` — pre-publish truth checklist
- `references/citation-monitoring.md` — searchstack-aeo + cost notes
- `references/inline-fallback.md` — manual checks if `geo` CLI unavailable
- `references/awesome-geo.md` — curated index of platforms, papers, related tools

## Install

```bash
./scripts/install_cli.sh
```

Idempotent: installs `geo-optimizer-skill`, optionally `searchstack`.
