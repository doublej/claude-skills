# Skill Research: Documentation Creation & Framework Suggestions

**Date**: 2026-02-03
**Query**: Documentation creation, concept management, modern framework suggestions

---

## 🎯 Top Recommendations

### 1. **Context7 MCP** - ⭐ Already installed | **HIGH CONFIDENCE**
- **Source**: MCP Plugin (already in your environment)
- **Why**: Purpose-built for querying up-to-date framework/library documentation with version-specific support
- **Strengths**:
  - Zero setup - already available via `mcp__plugin_context7_context7__resolve-library-id` and `query-docs`
  - Solves "which version's docs?" problem
  - Perfect for framework suggestion skills
- **Concerns**:
  - Requires 2-step lookup (resolve-library-id → query-docs)
  - 3-call limit per question suggests backend costs
  - No concept management features
- **Install**: Already installed
- **Best for**: "What's the current best practice for X in framework Y?"

---

### 2. **[DevDocs](https://github.com/cyberagiinc/DevDocs)** - ⭐ 2021 stars | **HIGH CONFIDENCE**
- **Source**: GitHub
- **Why**: Smart crawling (depth 1-5) of ANY tech docs, UI-based config, free forever
- **Strengths**:
  - Broad coverage - can crawl custom/internal docs
  - Active development (2K+ stars)
  - MCP integration ready
  - Export to MD/JSON for fine-tuning
  - Crawl4AI-powered with parallel processing
- **Concerns**:
  - UI dependency may add friction for CLI workflows
  - Depth-5 crawling could pull excessive content
  - Another dependency to maintain
  - Latency vs local search
- **Install**: Docker-based setup, see [repo README](https://github.com/cyberagiinc/DevDocs)
- **Best for**: Custom docs, tutorials, guides beyond API references

---

### 3. **[Awesome-docs](https://github.com/testthedocs/awesome-docs)** - ⭐ 827 stars | **MEDIUM CONFIDENCE**
- **Source**: GitHub
- **Why**: Curated list of documentation tools (Sphinx, MkDocs, etc.)
- **Strengths**:
  - Community-vetted resources
  - Good for discovery
- **Concerns**:
  - It's a list, not a tool - requires manual evaluation
  - Curation drift (links may be stale)
  - No direct integration with skills
- **Install**: Just bookmark the repo
- **Best for**: Building documentation systems, not querying them

---

### 4. **[TouchDesigner MCP](https://github.com/bottobot/touchdesigner-mcp-server)** - ⭐ 26 stars | **LOW CONFIDENCE**
- **Source**: GitHub
- **Why**: Complete TouchDesigner operator/Python API documentation
- **Strengths**:
  - 629 operators + 14 tutorials + 69 Python API classes
  - Well-executed for its domain
- **Concerns**:
  - Hyper-niche (visual programming for multimedia)
  - Not relevant for general web/app development
  - Single maintainer risk
- **Install**: See repo for MCP config
- **Best for**: Creative coding/generative art projects only

---

### 5. **[S3-Documentation-MCP-Server](https://github.com/yoanbernabeu/S3-Documentation-MCP-Server)** - ⭐ 7 stars | **LOW CONFIDENCE**
- **Source**: GitHub
- **Why**: RAG over Markdown docs stored on S3
- **Strengths**:
  - Could handle custom concept storage
  - RAG approach enables semantic search
- **Concerns**:
  - Only 7 stars (minimal validation)
  - Requires S3 + infrastructure setup
  - Better solved with local Markdown + grep
  - Vendor lock-in to AWS
- **Install**: Requires S3 bucket setup
- **Best for**: Skip unless you already host docs on S3

---

## 📊 Source Coverage

| Source | Results Found | Top Pick |
|--------|---------------|----------|
| GitHub | 20+ MCP servers | DevDocs (2021⭐) |
| mcp.so | Limited results (404/429 errors) | Filesystem, Jina AI mentioned |
| Smithery | Rate limited | N/A |
| Context7 | Already installed | Context7 MCP (plugin) |

---

## 🎭 Debate Summary

### Advocate Highlights
- **Context7 is already installed** - zero friction to start using immediately
- **DevDocs fills gaps** - smart crawling covers custom docs Context7 doesn't index
- **2021 stars signal trust** - DevDocs has real community adoption
- **Free + UI = accessible** - lowers barrier vs CLI-only tools

### Critic Concerns
- **MCP overhead** - official docs + browser search is often faster
- **Maintenance burden** - each server is another dependency to manage
- **Call limits** - Context7's 3-call limit suggests expensive backend
- **Crawl noise** - depth-5 crawling pulls menus, footers, irrelevant content
- **7-star projects** - S3-Documentation-MCP is too immature to trust

### Synthesizer Verdict
**Install Context7 (if not present) + consider DevDocs as complement**

**Confidence Scores:**
1. Context7: 92/100 (HIGH)
2. DevDocs: 88/100 (HIGH)
3. Awesome-docs: 65/100 (MEDIUM - reference only)
4. TouchDesigner: 45/100 (LOW - niche)
5. S3-Documentation: 42/100 (LOW - immature)

**Gap Identified**: None of these solve "holds concepts" requirement. Consider:
- Obsidian MCP for note-taking
- Custom skill with embedded concept templates
- Separate research for knowledge management tools

---

## 🔧 Recommended Action Plan

### Immediate (Today)
1. **Use Context7** for framework suggestions
   ```
   mcp__plugin_context7_context7__resolve-library-id
   mcp__plugin_context7_context7__query-docs
   ```
2. Test with: "modern React 19 patterns" or "FastAPI async best practices"

### Short-term (This Week)
3. **Evaluate DevDocs** if Context7 coverage is insufficient
   - Install via Docker
   - Configure to crawl frequently-referenced docs

### For Concept Management
4. **Research separately** - this requires note-taking/knowledge base tools:
   - Obsidian MCP
   - Notion MCP
   - Custom Markdown-based solution

### Skip
5. ❌ S3-Documentation-MCP (immature)
6. ❌ TouchDesigner MCP (unless creative coding is your focus)

---

## 📝 Raw Search Data

### GitHub Queries
- `gh search repos "documentation mcp server"` → 20 results (DevDocs leading)
- `gh search repos "framework suggestions skill"` → 0 results
- `gh search repos "awesome documentation tools"` → awesome-docs (827⭐)
- `gh search repos "concept knowledge mcp"` → 0 results
- `gh search repos "technical writing documentation"` → Mostly portfolios (low stars)

### MCP.so Results
- Filesystem, PostgreSQL, Jina AI, Firecrawl, Search1API mentioned
- No dedicated documentation creation servers found
- Many results were 404 or rate-limited

### Smithery Results
- Rate limited (429 error)

---

## 💡 Key Insights

### What Worked
- Context7 is already in the user's environment - immediate win
- DevDocs emerged as clear leader for broad documentation access
- Awesome-docs useful as meta-reference despite not being a tool

### What Didn't Work
- "Framework suggestions" as search term yielded nothing
- mcp.so and Smithery had technical issues (404/429)
- Concept management requires different tool category (knowledge bases)

### Patterns for Future Searches
- Search "documentation mcp" not "documentation creation"
- Concept management = note-taking/knowledge base tools (separate category)
- Framework suggestions = documentation lookup tools (Context7, DevDocs)
- Always check if tool is already installed (Context7 case!)

---

## 🎓 Lessons Learned

1. **Check existing environment first** - Context7 was already available
2. **Documentation ≠ concept management** - different tool categories
3. **High stars matter** - DevDocs (2021⭐) vs S3-Docs (7⭐) quality gap is real
4. **Web search failures happen** - GitHub search more reliable than web directories
5. **Niche tools exist** - TouchDesigner shows MCP ecosystem breadth

---

## ✅ Final Recommendation

**Primary**: Use Context7 MCP (already installed)
**Secondary**: Add DevDocs if you need broader coverage
**For concepts**: Research knowledge base MCPs separately (Obsidian, Notion)

**Confidence**: HIGH for Context7 + DevDocs combo covering documentation/framework needs
**Gap**: Concept management requires different tool class
