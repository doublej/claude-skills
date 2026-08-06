# robots.txt Patterns for AI Engines

## The 4 critical citation bots

Never block these — blocking them = invisible in AI answers.

| User-agent | Engine | Purpose |
|------------|--------|---------|
| `OAI-SearchBot` | ChatGPT Search | Real-time citation crawl |
| `PerplexityBot` | Perplexity | Answer citations |
| `ClaudeBot` | Claude | Web citations |
| `Google-Extended` | Gemini / AI Overviews | AI training-aware crawl |

## The training bots (block these to opt out of training, keep citations)

| User-agent | Engine | What it does |
|------------|--------|--------------|
| `GPTBot` | OpenAI | Trains GPT models (NOT search) |
| `anthropic-ai` | Anthropic | Legacy training crawler |
| `CCBot` | Common Crawl | Indirect training data |
| `Google-Extended` | Google | Training opt-out (also gates Gemini AI Overviews) |
| `FacebookBot` | Meta | Llama training |
| `Applebot-Extended` | Apple | Apple Intelligence training |
| `Bytespider` | ByteDance | Training |
| `Diffbot` | Diffbot | Training data resale |
| `cohere-ai` | Cohere | Training |
| `Omgilibot` | Webz.io | Training data resale |

## Recommended template

```
# robots.txt — allow citation bots, block training-only bots

# Citation bots — REQUIRED for AI search visibility
User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

# Block training crawlers (keeps your content out of model weights)
User-agent: GPTBot
Disallow: /

User-agent: anthropic-ai
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: FacebookBot
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: Applebot-Extended
Disallow: /

# Conventional search bots
User-agent: *
Allow: /

Sitemap: https://SITE.com/sitemap.xml
```

## Google-Extended caveat

`Google-Extended` is dual-purpose: it gates both Gemini training **and** AI Overview eligibility. If you `Disallow: /` on Google-Extended you opt out of AI Overviews entirely. For most sites: `Allow: /`.

## CDN gotchas

robots.txt at the origin is moot if your CDN blocks the bot at the edge. Check:

- **Cloudflare**: Settings → Bots → "AI Scrapers and Crawlers" toggle. Default-on blocks ALL listed bots — including citation ones. Disable if you want AI search visibility.
- **Vercel**: `vercel.json` may have `headers` with `X-Robots-Tag: noai` — strip it.
- **Akamai/AWS WAF**: managed bot rules may block Claude/Perplexity user-agents. Whitelist by name.

Verify with: `curl -A "PerplexityBot/1.0" -I https://SITE.com/`. Expect 200, not 403/451.

## Per-path policy

Allow citation crawl on public content but lock private areas:

```
User-agent: OAI-SearchBot
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /draft/
```

## Verify

```bash
geo audit --url https://SITE.com --format json | jq '.checks.robots'
```

Manual cross-check: <https://www.darkvisitors.com/agents> for the latest user-agent registry.
