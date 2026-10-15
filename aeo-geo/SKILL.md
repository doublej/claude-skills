---
name: aeo-geo
description: Audit and optimize websites for AI-engine citation in ChatGPT, Perplexity, Claude, Gemini, Google AI Overviews. Generates llms.txt, robots.txt allowlists, JSON-LD schema, and applies Princeton GEO content methods. Triggers on "AEO", "GEO", "answer engine optimization", "generative engine optimization", "make my site visible to ChatGPT/Perplexity", "llms.txt", "AI search", "AI citations", "LLM SEO".
---

# AEO/GEO — Answer & Generative Engine Optimization

## Overview

Make a website cited by AI engines. Three planes: discoverability (crawlers can reach it), structure (JSON-LD + llms.txt), citability (content evidence Princeton/AutoGEO research shows AI engines reward).

Wrap [`geo-optimizer-skill`](https://github.com/Auriti-Labs/geo-optimizer-skill) (305⭐, Princeton/AutoGEO-backed) for the heavy lifting. Add Princeton method table, framework patterns, and codebase-fix prompts inline.

## Presentation

Print once, as the first thing in the response:

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   AEO GEO                                                    ║
║   Answer and generative engine optimization                  ║
║   github.com/doublej                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

Close with the report under Output convention. Generated files (llms.txt, robots.txt, JSON-LD, rewritten content) stay free of box art and signature.

## When to use

- User wants their site to appear in ChatGPT Search / Perplexity / Claude / Gemini answers
- Adding `llms.txt`, `robots.txt` AI-bot rules, or JSON-LD to a project
- Auditing why a site isn't being cited
- Writing or rewriting content to maximize LLM citation odds

## When NOT to use

- Pure traditional Google SEO without AI angle → use `prompt-crafter` + standard meta/sitemap
- Personal projects with no real audience to capture → skip; not worth the maintenance
- Multi-LLM brand monitoring → see `references/citation-monitoring.md` (separate concern, costs money)

## Step 1 — Detect environment and pick a mode

Run this; do not skip it or assume the result:

```bash
command -v geo || uv tool install geo-optimizer-skill   # never pip
geo --version                                           # 4.x expected
command -v searchstack 2>/dev/null                      # optional, citation monitoring
```

Pick the mode, then state it in the report header (Output convention):

| Mode | When | What runs |
|------|------|-----------|
| `cli` | `geo --version` works AND the target is a public URL | Steps 2–9 as written |
| `local` | Target is `localhost`, `127.*`, `10.*`, `192.168.*`, `*.local` | `geo` refuses these (`Unsafe URL: Host not allowed`). Run the curl checks in `references/inline-fallback.md` against the dev server, `geo schema --file <built.html> --analyze` on built HTML, and write llms.txt/robots.txt/JSON-LD into source from the inline templates. No score — write `score: —` |
| `fallback` | `geo` install fails (offline, sandbox) | `references/inline-fallback.md` manual rubric |

Falling back is fine; falling back silently is a bug. In `local`/`fallback` mode, put the reason in the header and list what the CLI would have added (CDN bot checks, 47-method content score, history) as `—` rows.

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
uv tool install searchstack
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
AEO GEO  ──  <site>   mode: <cli|local|fallback (reason)>   score: <before> → <after|—>   band: <critical|foundation|good|excellent|—>

PRI        FINDING                            FIX                              STATUS
────────────────────────────────────────────────────────────────────────────────────
CRITICAL   robots.txt blocks ClaudeBot        remove line 12                   ✓
HIGH       no llms.txt at /llms.txt           generated, write to public/      ✓
MEDIUM     missing FAQPage JSON-LD on /faq    patch added                      ✓
LOW        no <html lang> on layout           set "en"                         —

github.com/doublej
```

Ship as a PR-style diff list, not prose. Marks: `✓` applied, `✗` failed (cause under the table), `—` not applied.

Running as a subagent (result goes back to an orchestrator): return only the header and ≤20 table rows with `file:line` in FIX. No full llms.txt, JSON-LD or rewritten-content blocks — write them to disk and name the path, or offer them on request.

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
