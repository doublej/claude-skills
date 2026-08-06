# Citation Monitoring (Optional)

Track whether ChatGPT / Perplexity / Claude / Grok / Gemini cite your site for target queries. Costs real money via API keys.

## When this is worth it

- Active brand with a marketing budget
- Specific queries you need to win (e.g. "best X for Y")
- You ship content monthly and need a feedback loop

## When to skip

- Personal projects, hobby sites, dev portfolios
- Brand-new domains (citations take 3-6 months to register)
- No budget for $20-100/month in API spend

## Tool: searchstack-aeo

```bash
pip install searchstack
searchstack init                                    # config wizard
searchstack ai --queries queries.yaml               # poll all engines
searchstack geo --keywords "best gpu for ml"        # AI Overview tracking
searchstack monitor --site https://SITE.com         # per-page perf
searchstack report --output ./report.md             # markdown digest
```

## Required keys (set in `~/.searchstack/config.yaml`)

| Key | Required for | Cost (est.) |
|-----|--------------|-------------|
| `OPENAI_API_KEY` | ChatGPT citation polling | ~$0.50/100 queries (gpt-4o-mini) |
| `ANTHROPIC_API_KEY` | Claude citation polling | ~$0.30/100 queries (haiku) |
| `PERPLEXITY_API_KEY` | Perplexity polling | ~$1/100 queries |
| `XAI_API_KEY` | Grok citation polling | ~$0.50/100 queries |
| `GOOGLE_GSC_KEY` | rankings + indexing | free |
| `DATAFORSEO_API_KEY` | keyword volumes | $0.50/1k SERPs |
| `PLAUSIBLE_API_KEY` | AI referral traffic | free if self-hosted |

## Free tier — Ollama local

```bash
ollama pull qwen2.5:7b
searchstack ai --provider ollama --model qwen2.5:7b
```

Tests how open-source models represent your brand. Zero API cost.

## Recommended cron

```cron
# Weekly Monday 8am citation check + diff
0 8 * * 1 cd ~/work/site && searchstack report --output ./reports/$(date +\%F).md
```

## Output sample

```
$ searchstack ai

  Checking AI citations for example.com...

  ChatGPT (gpt-4o-mini):
    "What is the best tool for X?"  ✅ CITED
    "How to solve Y?"                ❌ not cited
    "Top Z software in 2026"         ✅ CITED

  Perplexity (sonar):
    "What is the best tool for X?"  ✅ CITED  → https://example.com/guide
    "Top Z software in 2026"         ❌ not cited

  Summary: ChatGPT 2/3 | Perplexity 1/3 | Claude 0/3
```

## Alternative platforms (paid)

If running this manually is too noisy, the curated list:
- AthenaHQ, Bluefish, Profound, Otterly.ai, Ahrefs Brand Radar, SEMrush AI Visibility Toolkit
- See `references/awesome-geo.md` for the full table

## Pitfalls

- **Sample size**: 3 queries × 1 day = noise. Need 50+ queries × 30 days for signal.
- **Drift**: queries that worked in Q1 get rephrased by Q3 — refresh `queries.yaml` quarterly.
- **Hallucinated citations**: LLMs sometimes "cite" you when they actually don't include the URL. Pair text-match check with citation extraction.
- **Rate limits**: Anthropic's free tier is tight. Use a paid key or rate-limit the poller.
