# Inline Fallback — When `geo` CLI Is Unavailable

If `pip install geo-optimizer-skill` fails (offline, sandbox, no Python), do these checks by hand. ~80% of value, 0% dependencies.

## Quick audit (manual, ~5 min)

```bash
SITE=https://example.com

# 1. robots.txt has citation bots allowed?
curl -s $SITE/robots.txt | grep -iE "OAI-SearchBot|PerplexityBot|ClaudeBot"

# 2. llms.txt exists?
curl -sI $SITE/llms.txt | head -1

# 3. JSON-LD on homepage?
curl -s $SITE | grep -oE '<script type="application/ld\+json"[^>]*>[^<]*</script>' | head -3

# 4. <html lang> set?
curl -s $SITE | grep -oE '<html[^>]*lang="[^"]*"' | head -1

# 5. Sitemap reachable?
curl -sI $SITE/sitemap.xml | head -1

# 6. Can a citation bot reach the site?
curl -A "PerplexityBot/1.0" -sI $SITE | head -1
curl -A "ClaudeBot/1.0" -sI $SITE | head -1
curl -A "OAI-SearchBot/1.0" -sI $SITE | head -1
```

## Inline llms.txt template

Save as `public/llms.txt` (or `static/llms.txt`):

```markdown
# Site Name

> One-sentence factual description of what this site is and who it's for.

## Documentation
- [Getting Started](https://site.com/docs/start): brief description
- [API Reference](https://site.com/docs/api): brief description

## Blog
- [Latest Post Title](https://site.com/blog/latest): one-line summary

## About
- [About the Author / Team](https://site.com/about)
- [Contact](https://site.com/contact)
```

Rules: H1 (site name) → blockquote (description) → H2 sections → bullet links with descriptions. ≤200 lines. Spec: <https://llmstxt.org>.

## Inline JSON-LD templates

### Organization (homepage)
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Site Name",
  "url": "https://site.com",
  "logo": "https://site.com/logo.png",
  "sameAs": [
    "https://en.wikipedia.org/wiki/Site_Name",
    "https://www.linkedin.com/company/site-name",
    "https://github.com/site-name"
  ]
}
```

### Article (blog post)
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Post Title",
  "datePublished": "2026-04-01",
  "dateModified": "2026-04-15",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://site.com/about"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Site Name",
    "logo": { "@type": "ImageObject", "url": "https://site.com/logo.png" }
  }
}
```

### FAQPage
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is X?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "X is a concise factual answer with a number."
    }
  }]
}
```

## Manual scoring rubric (rough)

Tally points; aim for 80+:

- robots.txt allows OAI-SearchBot/PerplexityBot/ClaudeBot: **+18**
- llms.txt present, well-structured: **+18**
- JSON-LD on homepage (Organization + WebSite): **+8**
- JSON-LD on key pages (Article/FAQ as relevant): **+8**
- `<title>`, `<meta description>`, `<link canonical>` complete: **+10**
- Open Graph tags: **+4**
- H1 + heading hierarchy + lists/tables: **+8**
- Statistics + external citations in body: **+6**
- `<html lang>` set: **+3**
- RSS/Atom feed: **+3**
- `dateModified` ≤90 days: **+3**
- About page reachable in ≤2 clicks: **+5**
- Wikipedia / Wikidata / LinkedIn `sameAs` linked: **+5**

## When to upgrade to the real CLI

The fallback covers structure. The CLI adds:
- 47-method content scoring
- CDN crawler-access detection (edge bot blocks)
- Negative-signal detection (CTA overload, popups, thin content)
- Prompt-injection detection
- Trust Stack composite grade
- Coherence audit across a sitemap
- Saved-history regression detection

Run `pip install geo-optimizer-skill` once it's available.
