# Princeton GEO Methods + AutoGEO 47-Method Matrix

## Sources
- Princeton KDD 2024: ["GEO: Generative Engine Optimization"](https://arxiv.org/abs/2311.09735) — 10,000 queries on Perplexity.ai
- AutoGEO ICLR 2026: ["What Generative Search Engines Like and How to Optimize Web Content Cooperatively"](https://arxiv.org/abs/2510.11438)
- SE Ranking 2025 + Growth Marshal 2026 (extension to 47 methods)

## Top 8 — Apply in this order

| # | Method | Visibility lift | Mechanism | Anti-pattern |
|---|--------|-----------------|-----------|--------------|
| 1 | **Cite Sources** | +30 to +115% | LLMs trust + reproduce content with verifiable external citations | Bare claims, internal-only links |
| 2 | **Add Statistics** | +40% | Concrete numbers anchor LLM extraction; quotable | Vague qualifiers ("many", "most") |
| 3 | **Quotation Addition** | +30 to +40% | Direct quotes get re-quoted by LLMs | Paraphrasing without attribution |
| 4 | **Authoritative Tone** | +6 to +12% | Confident expert framing maps to high-confidence outputs | Hedging, "I think", "maybe" |
| 5 | **Fluency Optimization** | +15 to +30% | Clean prose passes LLM rerankers | Fragmented, run-on, awkward |
| 6 | **Easy-to-Understand** | +8 to +15% | Definitions + analogies → broader query match | Jargon walls, no priming |
| 7 | **Technical Terms** | +5 to +10% | Industry vocab triggers domain matches | Layperson-only phrasing |
| 8 | **Unique Words** | +5 to +8% | Lexical diversity beats repetition | Over-optimized keyword reuse |

## Anti-method
| ❌ | Keyword Stuffing | ~0% / negative | LLM rerankers detect + downrank | Avoid |

## Schema/structural checks (geo-optimizer-skill scoring)

| Area | Pts | Looks for |
|------|-----|-----------|
| robots.txt | 18 | 27 AI bots across 3 tiers (training/search/user). Citation bots explicitly allowed |
| llms.txt | 18 | Present, has H1 + blockquote + sections + links + depth. Companion `llms-full.txt` |
| Schema JSON-LD | 16 | WebSite, Organization, FAQPage, Article. Schema richness (5+ attributes) |
| Meta Tags | 14 | Title, description, canonical, OG complete |
| Content | 12 | H1, statistics, external citations, heading hierarchy, lists/tables, front-loading |
| Brand & Entity | 10 | Brand-name coherence, Knowledge Graph (Wikipedia/Wikidata/LinkedIn/Crunchbase), about page, geo signals, topic authority |
| Signals | 6 | `<html lang>`, RSS/Atom, dateModified freshness |
| AI Discovery | 6 | `.well-known/ai.txt`, `/ai/summary.json`, `/ai/faq.json`, `/ai/service.json` |

**Score bands**: 86-100 Excellent · 68-85 Good · 36-67 Foundation · 0-35 Critical.

## Bonus checks (informational)

- **CDN Crawler Access** — Cloudflare/Akamai/Vercel may block GPTBot/ClaudeBot/PerplexityBot at the edge even if robots.txt allows
- **JS Rendering** — content accessible without JS? SPA framework detection
- **WebMCP Readiness** — Chrome WebMCP: `registerTool()`, `toolname` attrs, `potentialAction` schema
- **Negative Signals** — 8 anti-citation: CTA overload, popups, thin content, keyword stuffing, missing author, boilerplate ratio
- **Prompt Injection** — hidden text, invisible Unicode, LLM instructions, HTML-comment injection, monochrome text, micro-font, data-attr injection, aria-hidden abuse
- **Trust Stack Score** — 5 layers: Technical, Identity, Social, Academic, Consistency → composite A-F
- **RAG Chunk Readiness** — section word counts, definition openings, heading boundaries, anchor sentences
- **Content Decay** — temporal/statistical/version/event/price decay → evergreen score 0-100
- **Platform Citation Profile** — per-platform readiness for ChatGPT, Perplexity, Google AI

## Worked example — boost a flat paragraph

**Before** (bare claim, no anchors):
```
Our pricing model has helped many small businesses scale.
```

**After** (methods 1+2+3 applied):
```
Our pricing model has reduced customer-acquisition cost by 38% on
average across 412 SMB accounts in 2025 (internal data, audited by
[Stripe Atlas](https://stripe.com/atlas)). "We cut paid acquisition
in half within the first quarter." — Lena Park, Head of Growth,
Treadle, Q3 2025.
```

Three methods, ~3-4× citation odds.
