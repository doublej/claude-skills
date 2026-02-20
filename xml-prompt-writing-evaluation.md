# EVALUATION: XML Prompt Writing Tools/Skills for Claude

## Overview

Evaluating 6 resources for teaching XML prompt engineering with Claude. Goal: help users write better structured prompts using XML tags.

---

## FINDINGS

### 1. Anthropic Official Documentation (platform.claude.com)

**URL**: https://platform.claude.com/docs/build-a-system-prompt/prompt-engineering
**Stars/Adoption**: Official (authoritative)
**Maintenance**: Anthropic-maintained

#### PROS
- **Authoritative**: Direct from Anthropic - no guessing about best practices
- **Up-to-date**: Follows current Claude capabilities and training
- **Free**: No cost or infrastructure overhead
- **Non-opinionated**: Documents what works, not what one team prefers
- **Concise**: 8 techniques with clear examples - no bloat
- **Integrated**: Seamless with official Claude ecosystem

#### CONS
- **Static reference**: Not interactive or tutorial-style
- **Limited depth**: Surface-level; doesn't teach philosophy behind techniques
- **No templates**: Examples are illustrative, not copy-paste ready
- **No validation**: Doesn't help users verify their XML is correct

#### Risk Assessment
- **Maintenance**: Low (Anthropic's responsibility)
- **Complexity**: Minimal (just read docs)
- **Vendor lock-in**: None; pure knowledge

#### When to Use
✓ As a baseline reference for correct syntax
✓ When you need Anthropic's official stance
✗ If you need interactive learning
✗ If you want pre-built templates

---

### 2. ThamJiaHe/claude-prompt-engineering-guide (GitHub, 38 stars)

**URL**: https://github.com/ThamJiaHe/claude-prompt-engineering-guide
**Stars**: 38 (low adoption)
**Maintenance**: Community-driven

#### PROS
- **Comprehensive**: 190+ sources cited; deep coverage
- **Curated**: Someone spent time synthesizing many sources
- **Free**: Open-source, no cost
- **Detailed examples**: More fleshed out than official docs
- **Community view**: Shows what practitioners use, not just Anthropic

#### CONS
- **Author credibility**: Unknown author; no track record visible
- **Outdated potential**: 38 stars suggests low visibility/validation
- **No automation**: Just a guide; requires manual application
- **Maintenance risk**: No clear update schedule
- **Bias risk**: Personal interpretation of best practices
- **Contradictions possible**: With 190+ sources, may contain conflicting advice

#### Risk Assessment
- **Maintenance**: MEDIUM-HIGH (community volunteer)
- **Complexity**: Low (reading only)
- **Trust**: Medium (unvetted author)

#### When to Use
✓ For broader context beyond official docs
✗ As primary reference (trust too low)
✗ For production guidance (credibility unclear)

---

### 3. claude-prompts MCP Server (minipuft/claude-prompts, 136 stars)

**URL**: https://github.com/minipuft/claude-prompts
**Stars**: 136
**Type**: MCP (Model Context Protocol) server

#### PROS
- **Integrated**: Works within Claude Code/Cursor workflows
- **Template library**: Provides ready-to-use prompt chains
- **Advanced**: Gates and hooks for complex workflows
- **Discovery**: Browse available prompts without remembering names

#### CONS
- **Setup overhead**: Requires MCP server configuration and launch
- **Learning curve**: Gates/hooks/plugins model unfamiliar to most
- **Maintenance burden**: Another service to maintain/troubleshoot
- **Opaque chains**: Hard to debug when templates fail
- **Limited scope**: Useful for chains, not for teaching XML fundamentals
- **Dependency**: Couples your workflow to a third-party service

#### Risk Assessment
- **Complexity**: HIGH (setup, config, mental model)
- **Maintenance**: MEDIUM (external dependency)
- **Brittleness**: Chains can fail in subtle ways
- **Lock-in**: Switching tools = relearning UI

#### When to Use
✓ If you already use Claude Code + MCP ecosystem
✓ For building complex multi-turn prompt chains
✗ For learning XML fundamentals (adds noise)
✗ For simple one-off prompts (overcomplicated)
✗ For teams without MCP infrastructure

---

### 4. Anthropic's Interactive Tutorial (Jupyter, 30K stars)

**URL**: Claude interactive notebooks (official)
**Stars**: 30K (high adoption)
**Type**: Educational Jupyter notebook

#### PROS
- **Official**: From Anthropic
- **Highly visible**: 30K stars = community validation
- **Interactive**: Learn by doing, not just reading
- **Safe**: Notebook sandboxing; can't break anything
- **Free**: Open-source

#### CONS
- **Educational, not production**: Teaches concepts, not best practices for real work
- **Static content**: Prompts are examples, not patterns
- **Not XML-focused**: Broader prompt engineering, not XML specifically
- **Dated patterns**: Some examples may be outdated
- **No templates**: Still need to extract and adapt examples

#### Risk Assessment
- **Complexity**: Low (notebook interface is familiar)
- **Maintenance**: Low (Anthropic maintains)
- **Relevance**: Medium (educational; not prescriptive)

#### When to Use
✓ For learning prompt fundamentals
✗ For XML-specific techniques (it's broader)
✗ For copy-paste templates

---

### 5. BAML Framework (7.5K stars)

**URL**: https://github.com/BoundaryML/baml
**Stars**: 7.5K (moderate adoption)
**Type**: Domain-specific language (DSL) for prompt engineering

#### PROS
- **Structured approach**: Forces good prompt design via schema
- **Type-safe**: Validates outputs against defined schemas
- **Reusable**: Build libraries of prompt templates
- **Well-maintained**: Active development and community
- **Ecosystem**: Integrations with LangChain, TypeScript, Python

#### CONS
- **Own DSL, not XML**: BAML is proprietary syntax, not XML
- **Steep learning curve**: New language on top of existing stack
- **Schema overkill**: For simple prompts, schemas add friction
- **Vendor dependency**: Tied to Boundary's ecosystem
- **Distraction**: Teaches BAML, not XML writing
- **Overhead**: Compilation/validation steps for simple prompts

#### Risk Assessment
- **Complexity**: VERY HIGH (new language to learn)
- **Maintenance**: MEDIUM (active project, but external)
- **Learning curve**: HIGH (paradigm shift)
- **Payoff**: Medium (best for large teams/complex prompts)

#### When to Use
✓ If you're building a DSL-based prompt system
✓ For teams needing type-safe templates
✗ For learning XML fundamentals (different paradigm)
✗ For simple, one-off prompts (overhead)
✗ If you want to stay close to vanilla Claude

---

### 6. AWS claude-prompt-generator (1.3K stars)

**URL**: https://github.com/aws-samples/claude-prompt-generator
**Stars**: 1.3K
**Type**: Web UI tool

#### PROS
- **Visual workflow**: GUI for building prompts
- **AWS integration**: Works with Bedrock if you're in AWS ecosystem
- **Discovery**: Browse and learn from existing prompts
- **Some templating**: Can save/load prompt configs

#### CONS
- **Dated**: Claude 3 era; may not reflect current best practices
- **AWS-locked**: Requires Bedrock API (cost + infrastructure)
- **Limited scope**: Not specifically about XML
- **Maintenance risk**: Relatively low stars; volunteer-maintained
- **UI friction**: Web UI slower than editing locally/in IDE
- **Export problems**: May not preserve XML structure when saving/loading

#### Risk Assessment
- **Complexity**: Medium (UI-dependent, AWS setup required)
- **Cost**: YES (Bedrock API charges)
- **Maintenance**: MEDIUM-LOW (appears inactive)
- **Portability**: Low (AWS Bedrock-specific)

#### When to Use
✗ Not recommended (outdated, AWS-specific, no clear XML focus)

---

## SUMMARY TABLE

| Tool | Authoritative | Learning | Templates | Setup | Maintenance | Risk |
|------|---------------|----------|-----------|-------|-------------|------|
| **Official Docs** | ✓✓✓ | ✗ | ✗ | ✗ | LOW | MINIMAL |
| **ThamJiaHe guide** | ✗ | ✓✓ | ✗ | ✗ | MEDIUM | MEDIUM |
| **claude-prompts MCP** | ✗ | ✗ | ✓✓ | ✓ | MEDIUM | HIGH |
| **Interactive Tutorial** | ✓✓ | ✓✓ | ✗ | ✗ | LOW | LOW |
| **BAML Framework** | ✗ | ✗ | ✓✓ | ✓✓ | MEDIUM | VERY HIGH |
| **AWS Tool** | ✗ | ✗ | ✓ | ✓ | MEDIUM | HIGH |

---

## RECOMMENDATION MATRIX

### For Learning XML Fundamentals
1. **Start**: Anthropic Official Docs (free, authoritative)
2. **Deepen**: Anthropic Interactive Tutorial (learn by doing)
3. **Context**: ThamJiaHe guide (for broader patterns)

**Skip**: BAML, MCP server, AWS tool (not focused on XML basics)

---

### For Building a Claude Code Skill

**Option A: Lightweight Reference Skill** (RECOMMENDED)
- **What**: Skill that wraps official Anthropic docs + adds practical examples
- **Why**: Low maintenance, high authority, no external dependencies
- **Effort**: ~1-2 hours to create
- **Example template includes**:
  - When to use XML vs. prose
  - Common tag patterns (`<system>`, `<task>`, `<context>`, etc.)
  - Validation checklist
  - Examples: error handling, persona definitions, output formats

**Option B: Template Library Skill**
- **What**: Curated collection of XML prompt templates for common tasks
- **Why**: Copy-paste ready, patterns distilled from best practices
- **Effort**: ~3-4 hours to curate examples
- **Content**: 20-30 reusable templates organized by use case

**Option C: Interactive Learning Skill**
- **What**: Step-by-step tutorial that generates and tests your XML prompts
- **Why**: Hands-on; validates structure as you write
- **Effort**: ~6-8 hours (requires testing harness)
- **Risk**: Maintenance burden if Claude API changes

---

## ARGUMENTS AGAINST ADOPTION

### Against claude-prompts MCP
- **Over-engineered**: Gates/hooks model teaches prompt patterns, not XML syntax
- **Setup friction**: Requires MCP configuration; slows learning
- **Opaque chains**: Hard to debug template failures
- **Better alternative**: Build a simpler skill or use official docs directly

### Against BAML Framework
- **Wrong abstraction level**: BAML ≠ XML; teaches schema design, not prompt structure
- **Learning tax**: Another language to learn; distracts from XML fundamentals
- **Overkill for most users**: 90% of use cases don't need type-safe templates
- **Better alternative**: Official docs + lightweight skill covers 80% of needs

### Against AWS Tool
- **Outdated**: Claude 3 era; patterns likely stale
- **Unnecessary costs**: Bedrock API charges; official Claude API is cheaper
- **Vendor lock-in**: Works only with AWS; not portable
- **Ignored by community**: Only 1.3K stars; low validation
- **Better alternative**: Official docs + any modern Claude client

### Against ThamJiaHe Guide
- **Unvetted author**: Unknown credibility; 38 stars suggests low adoption
- **Possible contradictions**: 190+ sources may conflict with each other
- **Maintenance uncertainty**: No clear update schedule
- **Better use**: Supplement official docs, not replace them

---

## FINAL RECOMMENDATION

### BEST APPROACH: Build a Lightweight Claude Code Skill

**Rationale:**
1. **Start with authority**: Base on Anthropic official docs (cite clearly)
2. **Minimize complexity**: No MCP, no new DSLs, no AWS setup
3. **Add practical value**: Templates + validation checklist that official docs lack
4. **Low maintenance**: No external dependencies, no servers to manage
5. **Fits Claude ecosystem**: Integrates naturally with Claude Code workflow

**Skill Structure:**
```
xml-prompt-writer/
├── SKILL.md (this file)
├── templates/
│   ├── system-prompts.md
│   ├── task-definitions.md
│   ├── error-handling.md
│   └── output-formats.md
├── checklist.md (validation guide)
└── examples/ (3-5 complete, annotated prompts)
```

**Usage:**
- User: "Generate an XML system prompt for a code reviewer"
- Skill: Loads template, fills in blanks, shows structure, runs validation
- Result: Production-ready XML + explanation of design choices

**Estimated effort**: 4-6 hours to initial release
**Maintenance**: Minimal (update quarterly with Anthropic docs)

---

## CONCLUSION

**Adopt:** Anthropic Official Docs + Interactive Tutorial (free, authoritative)
**Build:** Lightweight skill wrapping official docs with templates + validation
**Skip:** MCP server, BAML, AWS tool, unvetted GitHub guides (not worth the overhead)

The best tool is the one that doesn't exist yet: a simple, opinionated skill that teaches XML patterns without the distraction of complex frameworks or external dependencies.
