---
name: dutch-tax
description: Dutch ZZP/BV bookkeeping and tax-optimization expertise (2026). Routes questions on KIA, KOR, BTW, urencriterium, WBSO, excessief lenen, WKR, RGS, Moneybird/Exact MCP, accountant handoff, deterministic-engine architecture, year-end iXBRL. Trigger on Dutch tax/bookkeeping/BTW/ZZP/BV/DGA/belastingdienst questions.
---

# Dutch Tax Skill

Opinionated for **ZZP (eenmanszaak)** and **BV / DGA** scenarios. VOF mentioned only where relevant.

**All numeric thresholds are 2026** unless explicitly tagged otherwise. Verify against `references/05-rules-2026/` before applying.

## Hard rules (read before answering anything tax-numerical)

1. **Never invent numbers.** If a 2026 threshold is not in `references/05-rules-2026/`, say "not in skill — verify against Belastingdienst.nl" and stop.
2. **Calculations are deterministic.** LLM may classify, extract, explain — never compute final tax. See `references/03-architecture/deterministic-engine.md`.
3. **Accountant-in-loop is mandatory** for: BTW filing, IB/VPB filing, KOR switch, KIA on ambiguous assets, WBSO/Innovatiebox, all DGA salary/dividend/loan decisions, structural choices (BV vs ZZP). See `references/06-risks-sources/liability.md`.
4. **Output disclaimer** on any tax position: "Review by qualified accountant required before filing."

## Routing table — load on demand

Pick the smallest set of references that answer the question. Most questions need 1–2 files.

### "What's the X threshold/rate for 2026?"
→ `references/05-rules-2026/thresholds.md` (KIA, KOR, zelfstandigenaftrek, startersaftrek, MKB-winstvrijstelling, urencriterium, representatiekosten cap, excessief lenen €500k)
→ `references/05-rules-2026/btw-rates.md` (0/9/21%, KOR, logies)
→ `references/05-rules-2026/ib-brackets.md` (Box 1/2/3)
→ Plus the matching topic file in `references/02-tax-opportunities/` if asking about HOW to use it

### "How does {KIA, MKB, zelfstandigenaftrek, WBSO, excessief lenen, representatie, WKR, BTW mixed-use, DGA salary} work?"
→ `references/02-tax-opportunities/<topic>.md`
→ Cross-link to `references/05-rules-2026/thresholds.md` for the number

### "Which MCP server / tool / repo / platform connects to {Moneybird, Exact, e-Boekhouden, Jortt}?"
→ `references/01-existing-tools/mcp-servers.md` (MCPs)
→ `references/01-existing-tools/platforms.md` (platforms + their APIs)
→ `references/01-existing-tools/repos.md` (open-source builds: OpenAccountants, Speedy, TaxHacker, Claude Did My Taxes, income-tax-optimizer)

### "How should I architect / build / structure the AI tax pipeline?"
→ `references/03-architecture/deterministic-engine.md` (Python tax math, hardcoded 2026 tables)
→ `references/03-architecture/rgs-normalization.md` (chart-of-accounts mapping)
→ `references/03-architecture/mcp-layer.md` (Moneybird/Exact ingestion)
→ `references/03-architecture/exception-handling.md` (classified/assumed/needs-review)
→ `references/03-architecture/evidence-logging.md` (7-year retention, calc traces)
→ `references/03-architecture/roadmap.md` (gap analysis, MVP phases, build-vs-buy)

### "What prompt do I use for {categorization, quarterly scan, accountant questions, year-end close}?"
→ `references/04-prompts/<workflow>.md`

### "What are the BTW deadlines / filing requirements?"
→ `references/05-rules-2026/deadlines.md`

### "Can the AI file my BTW return / make tax decisions / approve writeback?"
→ `references/06-risks-sources/liability.md` (NO without accountant)
→ `references/06-risks-sources/compliance.md` (Belastingdienst posture, retention)

### "Where does this rule come from?" / source verification
→ `references/06-risks-sources/source-table.md`

### Acronym lookup (RGS, BTW, WKR, DGA, KOR, KIA, IB, VPB, Vpb, MKB, WBSO, FOR, ICP, KVK, RVO, SBR, XAF)
→ `_glossary.md`

## Personal scope

- Entity defaults: ZZP (eenmanszaak) + BV (DGA scenarios)
- Deep coverage: WBSO/Innovatiebox, excessief lenen, DGA gebruikelijk loon, zelfstandigenaftrek + urencriterium
- Skip: VOF-only edge cases (mention but don't deep-doc)
- Currency: EUR. Dates: NL format (DD-MM-YYYY) unless asking US-style date.

## Files in this skill

- `SKILL.md` — this router
- `INDEX.md` — visible navigable tree (open this for human-readable layout)
- `_glossary.md` — NL fiscal acronyms
- `references/01-existing-tools/` — MCPs, repos, platforms
- `references/02-tax-opportunities/` — 9 opportunity docs
- `references/03-architecture/` — 6 architectural docs
- `references/04-prompts/` — 4 workflow prompts
- `references/05-rules-2026/` — 4 numeric reference docs
- `references/06-risks-sources/` — compliance, liability, source-table
- `_build/` — auditable extraction + merge artifacts (do not load by default)
