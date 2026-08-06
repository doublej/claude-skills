# Content Audit Checklist

Run before publishing or shipping content updates. AI engines downrank or skip pages with detectable hallucinations + dead links.

## Pre-publish gates

### 1. Statistics
For every number on the page:
- [ ] Cite the source inline (link or footnote)
- [ ] Verify the number matches the source (not paraphrased into a new number)
- [ ] Check the source date — flag stats older than 24 months as stale
- [ ] Reject "studies show" / "research suggests" without a specific citation

### 2. Quotes
For every block quote:
- [ ] Search the exact string — does it appear at the cited source?
- [ ] Verify attribution: name spelling, role, organization, year
- [ ] If from a podcast/video, link to timestamp
- [ ] Flag composite quotes (multiple sentences stitched into one) — separate them

### 3. External links
- [ ] Every link returns 2xx (use `geo audit` or `lychee`)
- [ ] Domains are not parked / squatters
- [ ] Links open the relevant section, not just a homepage redirect
- [ ] No tracking links that decay (utm-only URLs)

### 4. Names + entities
- [ ] Person names: spelled correctly, current title, current org
- [ ] Company names: legal name vs. brand name consistent on the page
- [ ] Product names: capitalization consistent (`GitHub` not `Github`)
- [ ] Tool versions: pin version where behavior depends on it

### 5. Claims of fact
For each factual claim:
- [ ] Tagged as `claim`, `opinion`, or `forecast`
- [ ] Claims have a citation; opinions are clearly first-person
- [ ] No "everyone knows" / "obviously" framing without backing

### 6. Author + dateline
- [ ] Author name with link to bio / sameAs profile
- [ ] `datePublished` and `dateModified` in JSON-LD
- [ ] Editor / reviewer credit if applicable
- [ ] About page reachable in ≤2 clicks

### 7. AI-discovery affordances
- [ ] H1 reads as a complete claim, not a teaser
- [ ] First paragraph contains the answer (front-loading)
- [ ] Headings are full questions or statements, not labels
- [ ] Tables for any comparison; lists for any enumeration

## Quick CLI helpers

```bash
# Dead-link check
npx -y lychee --no-progress https://SITE.com/post/x

# Geo audit on a single page
geo audit --url https://SITE.com/post/x

# Diff before/after a content edit
geo diff --before https://SITE.com/post/x --after http://localhost:3000/post/x
```

## Failure modes to catch

| Symptom | Cause | Fix |
|---------|-------|-----|
| GPT cites a competitor for our exact stat | We paraphrased; competitor quoted verbatim | Use the verbatim phrasing from the source |
| Page never appears in Perplexity citations | All claims are uncited | Add 3-5 authoritative sources |
| AI Overview pulls our headline but wrong fact | Stat in body contradicts headline | Reconcile; LLMs prefer the headline |
| ChatGPT replies with an outdated number | dateModified missing | Add `datePublished` + `dateModified` JSON-LD |

## Don't

- Don't add fake quotes / synthetic stats to pad authority — modern rerankers detect hallucinated provenance and downrank.
- Don't bulk-add citations that lead to LLM-generated articles — secondary fabrications.
- Don't trust your own draft's stats — re-verify after each edit pass.
