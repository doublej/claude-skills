---
name: skill-researcher
description: "Research skills/MCP servers from GitHub, mcp.so, Smithery with debate eval"
---

# Skill Researcher

Research and evaluate skills from multiple sources with structured debate-style analysis.

## Workflow

```
1. SEARCH → GitHub is the required source; add web directories only as fallback
2. COLLECT → Gather metadata, deduplicate results
3. DEBATE → 3 parallel agents evaluate findings (skippable — see When to skip debate)
4. SYNTHESIZE → Merge perspectives into recommendations
5. IMPROVE → Update learnings for next run
```

## Sources

| Source | Type | Status | Best For |
|--------|------|--------|----------|
| GitHub | Code repos | **Required** | Skills, custom implementations, awesome lists |
| mcp.so | Directory | Fallback only | Production MCP servers, community ratings |
| Smithery | Registry | Fallback only | Verified MCP servers, installation guides |

**GitHub is the sole required source.** As of 2026, mcp.so and Smithery consistently return 403/429 to WebFetch (auth-gated / anti-bot) — 8+ consecutive runs confirmed this. Only attempt them if GitHub returns **fewer than 3 usable results**, and even then **check `references/learnings.md` first**: if it already records those sources as broken/403 for this kind of query, skip them and note the skip rather than re-hitting a dead endpoint.

## Search Strategy

Run GitHub queries in parallel (below). Query mcp.so / Smithery only under the fallback condition above.

### Source 1: GitHub (gh cli)

```bash
# Primary queries (run all in parallel)
gh search repos "<topic> skill claude" --limit 20 --json name,description,stargazersCount,url --sort stars
gh search repos "<topic> skill codex" --limit 20 --json name,description,stargazersCount,url --sort stars
gh search repos "<topic> mcp server" --limit 20 --json name,description,stargazersCount,url --sort stars
gh search repos "awesome <topic>" --limit 10 --json name,description,stargazersCount,url --sort stars
```

For promising repos (>10 stars):
```bash
gh api repos/<owner>/<repo>/contents --jq '.[].name'
gh api repos/<owner>/<repo>/readme --jq '.content' | base64 -d | head -150
```

### Source 2: mcp.so (WebFetch) — fallback only, usually 403/429; check learnings first

```
URL: https://mcp.so/search?q=<topic>
Prompt: "Extract all MCP servers from search results. For each: name, description, install count, GitHub link if available."
```

Also fetch category pages for broader discovery:
```
URL: https://mcp.so/servers
Prompt: "List MCP servers related to <topic>. Include name, category, and brief description."
```

### Source 3: Smithery (WebFetch) — fallback only, usually 403/429; check learnings first

```
URL: https://smithery.ai/search?q=<topic>
Prompt: "Extract MCP servers matching <topic>. For each: name, description, verification status, install command."
```

Browse registry for related servers:
```
URL: https://smithery.ai/servers
Prompt: "Find servers related to <topic>. Note any verified badges or popularity indicators."
```

## Result Aggregation

After collecting from all sources, deduplicate and merge:

1. **Match by name/repo** - Same server may appear on multiple sources
2. **Prefer GitHub data** for stars/activity metrics
3. **Prefer mcp.so/Smithery** for install counts and community feedback
4. **Flag discrepancies** - Different descriptions or versions across sources

## Debate Evaluation

**When to skip debate.** The 3-agent debate is the default, not a hard requirement. Skip it when any of these hold, and record the skip + reason in the output's **Debate Summary** field and in `references/learnings.md`:

- You directly inspected repo contents + README for the top candidates — direct file inspection is stronger evidence of "legit" than debating metadata.
- Only one viable candidate exists, or findings are unambiguous.
- The user already owns / uses the target skill.

When skipped, synthesize the recommendation inline and write `Debate Summary: replaced by direct file inspection` (or the applicable reason). Otherwise, spawn 3 Task agents in parallel with `subagent_type=general-purpose`:

### Agent 1: Advocate
Prompt: "You are evaluating skills for <topic>. ARGUE FOR adoption. Consider: popularity signals, documentation quality, active maintenance, feature coverage. Be enthusiastic but cite evidence."

### Agent 2: Critic
Prompt: "You are evaluating skills for <topic>. ARGUE AGAINST adoption. Consider: complexity overhead, maintenance burden, vendor lock-in, security concerns, alternatives. Be skeptical but fair."

### Agent 3: Synthesizer
Prompt: "Given advocate and critic perspectives on <topic> skills, synthesize a final recommendation. Weight: 40% popularity, 30% quality, 30% fit-for-purpose. Output ranked list with confidence scores."

## Output Format

```markdown
## Skill Research: <topic>

### Top Recommendations
1. **[name](url)** - ⭐ stars | Source: GitHub/mcp.so/Smithery | Confidence: HIGH/MEDIUM/LOW
   - Why: <1-2 sentences>
   - Concerns: <brief>
   - Install: `<command or link>`

### Source Coverage
| Source | Results Found | Top Pick |
|--------|---------------|----------|
| GitHub | N repos | ... |
| mcp.so | N servers | ... |
| Smithery | N servers | ... |

### Debate Summary
- Advocate highlights: ...
- Critic concerns: ...
- Synthesizer verdict: ...

### Raw Data
<collapsible with full search results per source>
```

## Self-Improvement

After each run, append learnings to `references/learnings.md`:

```markdown
## Run: <date> - <topic>

### What Worked
- Search queries that found good results
- Evaluation criteria that mattered

### What Didn't
- Queries with poor signal-to-noise
- Missed important repos

### Pattern Updates
- New search terms to try
- Filters to add/remove
```

Read `references/learnings.md` at start of each run to apply accumulated knowledge.

## Quick Commands

| Source | Query Type | Command/URL |
|--------|------------|-------------|
| GitHub | Claude skills | `gh search repos "<topic> skill claude" --sort stars` |
| GitHub | Codex skills | `gh search repos "<topic> skill codex" --sort stars` |
| GitHub | MCP servers | `gh search repos "<topic> mcp server" --sort stars` |
| GitHub | Awesome lists | `gh search repos "awesome <topic>" --sort stars` |
| mcp.so | Search | `https://mcp.so/search?q=<topic>` |
| mcp.so | Browse | `https://mcp.so/servers` |
| Smithery | Search | `https://smithery.ai/search?q=<topic>` |
| Smithery | Browse | `https://smithery.ai/servers` |

## Example Run

User: "Research database skills"

1. **GitHub**: `gh search repos "database mcp server"` → found 15 repos
2. **mcp.so**: WebFetch `mcp.so/search?q=database` → found postgres-mcp, sqlite-mcp
3. **Smithery**: WebFetch `smithery.ai/search?q=database` → found verified postgres server
4. **Dedupe**: postgres-mcp appears on all 3 sources, merge metadata
5. **Debate**: Advocate praises postgres-mcp adoption, Critic notes setup complexity
6. **Synthesize**: Recommend postgres-mcp (verified, 500+ installs, active maintenance)
7. **Improve**: Log that "database" yields better results than specific DB names
