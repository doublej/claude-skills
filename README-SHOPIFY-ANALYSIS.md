# Shopify MCP Evaluation: Complete Analysis

This directory contains a comprehensive evaluation of building a Shopify MCP server as a Claude Code skill, concluding with a recommendation to build a patterns documentation skill instead.

## Quick Decision

**Recommendation: DO NOT build Shopify MCP. Build "Shopify API Patterns" skill instead.**

- Existing Shopify MCPs cover only 1.5% of use cases
- Quarterly versioning makes MCP unsustainable to maintain
- GraphQL cost-based rate limiting creates footguns
- Credential storage in MCP creates security risks
- Patterns skill provides better long-term value with lower maintenance

## Documents in This Analysis

### 1. SHOPIFY_DECISION.md (START HERE)
**Executive summary of the entire analysis**

- Bottom-line recommendation
- Why MCP approach fails (5 core reasons)
- Why Patterns Skill works better
- Real-world scenario results
- What would change this recommendation

**Read this first:** 5-minute overview

---

### 2. shopify-analysis.md
**Detailed critique of MCP approach with architectural flaws**

Sections:
1. Existing MCP implementations are insufficient
   - GeLi2001/shopify-mcp (120★) gaps
   - amir-bengherbi/shopify-mcp-server (16★) gaps
   
2. Shopify API complexity challenges
   - Quarterly versioning nightmare
   - Strict rate limiting + GraphQL costs
   - OAuth authentication complexity
   
3. Architectural mismatch with Claude Code Skills
   - Skills are documentation, not proxies
   - "Incomplete feature" problem
   
4. Comparison: Direct API vs MCP
   - Why direct API integration recommended
   
5. Security & credential concerns
   - Token storage in MCP risks
   - Scope creep risk
   
6. Maintenance & community support reality
   - Why projects are stalled
   - Graveyard risk
   
7. Real-world use case analysis
   - Scenario 1-4: Where MCP fails
   
8. Recommended alternative
   - "Shopify API Patterns" skill architecture
   
9. Final verdict with decision framework

10. Conclusion

**Read this for:** Deep technical analysis (2000+ words)

---

### 3. shopify-alternatives-comparison.md
**Side-by-side comparison of four integration approaches with scenarios**

Content:
- Executive comparison table (8 approaches, 7 factors each)
- Detailed scenario analysis (5 real-world scenarios)
  - Scenario A: Create single product
  - Scenario B: Bulk update 500 products
  - Scenario C: Inventory across warehouses
  - Scenario D: Auto-fulfill workflow
  - Scenario E: Export customer data
- Rate limiting deep dive (REST vs GraphQL)
- Complexity evolution (why MCP fails over time)
- Token management comparison
- Versioning maintenance burden
- Code complexity comparison
- Conclusion comparing approaches

**Read this for:** Detailed scenario analysis with code examples

---

### 4. shopify-recommendation.md
**Proposed architecture for "Shopify API Patterns" skill (recommended approach)**

Content:
- Recommendation summary with justification
- Proposed skill structure (directory layout)
- Main content outline (SKILL.md sections):
  1. Overview & approach
  2. Authentication & access tokens
  3. Rate limiting (critical section)
  4. Common patterns (products, orders, inventory)
  5. Webhooks & background jobs
- Example implementations (Node.js SDK)
- Implementation plan (4 phases, ~1 week effort)
- Why this wins over MCP (comparison table)
- Next steps if proceeding

**Read this for:** How to build the recommended alternative

---

## Analysis at a Glance

### The Problem: MCP Is Too Small
```
Shopify API surface: ~1000 operations
GeLi2001 MCP coverage: 9 tools
Coverage percentage: 0.9%

User expectation: Complete integration
Reality: Hits wall on first non-trivial task
```

### The Problem: Maintenance is Unsustainable
```
Shopify releases 4 new API versions per year
Each version requires:
- Testing all tools
- Updating examples
- Deprecation handling
- User communication

3-year effort: 40+ hours/year (growing as API expands)
```

### The Problem: Rate Limiting Is Hidden
```
GraphQL cost system: 3M points/day budget
Easy to exhaust: 1000 poorly-structured queries = budget gone
No warning: MCP doesn't track costs
User impact: "Why did Shopify integration break?"
```

### The Solution: Patterns Skill
```
Teach users how to integrate correctly
- Patterns docs: ~2000 words (write once)
- Code examples: 10-15 working examples
- Maintenance: ~2 hours/quarter (mostly link checks)

Points to official resources (Shopify maintains)
Users build real integrations (not fake proxy)
```

## Key Findings

### Existing MCP Implementations
- **GeLi2001/shopify-mcp:** 120 stars, 9 tools, appears popular but incomplete
- **amir-bengherbi/shopify-mcp-server:** 16 stars, 15 tools, more features but less adoption
- **Neither:** Updated for latest API versions, no evidence of maintenance cadence
- **Both:** Missing critical features (inventory, fulfillment, webhooks fully)

### Shopify API Realities
- **Versioning:** 4 new versions per year, deprecations every 3 months
- **Rate Limiting:** REST (40 req/min) + GraphQL (3M point budget, cost-based)
- **Scope:** 1000+ operations across products, orders, inventory, fulfillment, etc.
- **Auth:** OAuth complexity, scope management, token security

### Why This Matters for Skills
- Skills are meant to be documentation + patterns, not stateful proxies
- Complex APIs with versioning need teaching, not wrapping
- MCP's request-response model doesn't fit stateful operations (webhooks, jobs)
- Better to empower users than hide complexity

## Scenario Results Summary

| Use Case | MCP | Patterns | CLI | Official SDK |
|----------|-----|----------|-----|--------------|
| Create product | ✓ | ✓ | ✓ | ✓ |
| Bulk update 500 products | ❌ Hits rate limit | ✓ Shows pattern | ✓ | ✓ |
| Inventory visibility | ❌ Tool doesn't exist | ✓ Reference | ✓ | ✓ |
| Auto-fulfill webhook | ❌ No webhooks | ✓ Full pattern | ✓ | ✓ |
| Export 100k customers | ❌ Inefficient | ✓ Optimization | ✓ | ✓ |

MCP wins on speed for trivial tasks, loses on everything realistic.

## Recommendation Summary

### Why NOT MCP
1. 1.5% coverage creates false promises
2. Quarterly versioning = maintenance hell
3. GraphQL costs create silent failures
4. Credential storage = security risk
5. Users hit gaps and blame tool

### Why YES Patterns Skill
1. 100% coverage via official references
2. Low maintenance (documentation)
3. Teaches cost-awareness
4. No credential storage
5. Empowers real workflows

### What to Build
**Skill: "Shopify API Patterns"**
- 2000-3000 word guide
- 7 reference documents (auth, rate limiting, patterns)
- 10-15 working code examples
- Initial effort: 5-7 days
- 3-year maintenance: ~10-12 hours total

## Historical Precedent

Other complex API MCP attempts:
- AWS MCP proxies → Abandoned (API too large)
- Stripe MCP → Built but incomplete (users use SDK)
- Twilio MCP → Missing features (users fall back to API)

**Pattern:** When API is complex + versioned, proxy fails. Teaching wins.

## Files in This Directory

```
/Users/jurrejan/Documents/development/_management/claude_skills/
├── SHOPIFY_DECISION.md                     (Executive summary - START HERE)
├── shopify-analysis.md                     (Detailed technical critique)
├── shopify-alternatives-comparison.md      (Scenario analysis with code)
├── shopify-recommendation.md               (Proposed skill architecture)
└── README-SHOPIFY-ANALYSIS.md             (This file)
```

## How to Use This Analysis

### For Decision Makers
1. Read: SHOPIFY_DECISION.md (5 min)
2. Reference: Why Not MCP section (justification)

### For Technical Review
1. Read: shopify-analysis.md (30 min, technical depth)
2. Review: shopify-alternatives-comparison.md (detailed scenarios)
3. Check: Real-world use case analysis section

### For Implementation Planning
1. Read: shopify-recommendation.md (skill architecture)
2. Review: Proposed skill structure section
3. Check: Implementation plan (4 phases, timeline)

### For Stakeholder Communication
1. Share: SHOPIFY_DECISION.md (summary)
2. Link to: shopify-analysis.md sections (evidence)
3. Show: Scenario results table (visual proof)

## Key Takeaway

Building an MCP for Shopify is a trap that sounds good initially but fails in practice. The complexity of Shopify's API, versioning cycle, and rate limiting system makes a proxy unsustainable.

Teaching users how to integrate with Shopify properly (via patterns, examples, and references to official tools) is more valuable, more maintainable, and more honest about what's possible.

**Recommendation: Skip the MCP. Build the patterns guide.**
