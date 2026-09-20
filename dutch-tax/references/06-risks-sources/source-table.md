# Source Trust Matrix

Master reference table of all sources used in the Dutch tax skill. Grouped by trust level.

---

## HIGH: Official & authoritative

| URL | Name | Trust | Used for | Caveats |
|-----|------|-------|----------|---------|
| https://www.belastingdienst.nl | Belastingdienst (Dutch Tax Authority) | HIGH | 2026 tax rates, KIA thresholds, KOR rules, VAT rates, Box brackets, excess-borrowing limits, zelfstandigenaftrek, startersaftrek | HTML/PDF subject to change; capture hashes + versioning metadata |
| https://www.belastingdienst.nl/zakelijk/btw_tarief/btw_tarief | Belastingdienst BTW Rates | HIGH | VAT rate definitions (0%, 9%, 21%); rate exceptions | Annual updates; requires version pinning |
| https://www.belastingdienst.nl/zakelijk/kleineondernemersregeling | Belastingdienst KOR (Small Business Exemption) | HIGH | KOR €20k threshold, eligibility, VAT exemption consequences | Year-specific threshold; monitor for changes |
| https://www.belastingdienst.nl/zakelijk/kleinschaligheidsinvesteringsaftrek | Belastingdienst KIA | HIGH | KIA 2026 thresholds (€2,901–€398,236), tiered %, asset rules | Tables change annually; verify per year |
| https://www.belastingdienst.nl/zakelijk/excessief-lenen-van-bv-beperkt | Belastingdienst Excessief Lenen | HIGH | DGA excess borrowing threshold €500k, Box 2 treatment | Threshold changed €700k→€500k in 2023; verify current |
| https://www.belastingdienst.nl/zakelijk/box_2 | Belastingdienst Box 2 | HIGH | Box 2 rates 2026, dividend/loan taxation | Annual rate changes; sensitive audit area |
| https://www.belastingdienst.nl/zakelijk/box_3 | Belastingdienst Box 3 | HIGH | Box 3 2026 rules, asset categories, tax-free allowance | Year-versioned; requires accountant for planning |
| https://www.belastingdienst.nl/zakelijk/mkb_winstvrijstelling | Belastingdienst MKB-Winstvrijstelling | HIGH | 12.7% SMB profit exemption, ZZP/eenmanszaak eligibility | % and cap change annually |
| https://www.belastingdienst.nl/zakelijk/zelfstandigenaftrek | Belastingdienst Zelfstandigenaftrek | HIGH | Self-employed deduction €1,200 (2026), eligibility, carryforward | Amount changes annually; verify per year |
| https://www.rvo.nl | RVO (Netherlands Enterprise Agency) | HIGH | WBSO R&D credit, Innovatiebox rules, EIA/MIA/Vamil schemes | Complex; professional review mandatory |
| https://www.kvk.nl | KVK (Dutch Chamber of Commerce) | HIGH | Business registration, entity types, entrepreneur status, VAT ID verification | Real-time API available; use for DGA/holding fact-check |
| https://1truth.nl | 1Truth.nl (RGS — Referentie Grootboekschema) | HIGH | Dutch chart of accounts standard (Belastingdienst + CBS) | Essential for ledger mapping + filing compatibility |
| https://www.cbs.nl | CBS (Central Bureau of Statistics) | HIGH | Economic indices, provisional percentages (Box 3) | Official annual data; use for fact-checking |
| https://www.digipoort.nl | Digipoort | HIGH | iXBRL filing gateway, submission validation | Required for year-end close |
| https://www.sbr-nl.nl | SBR / XAF 4.0 | HIGH | Audit file export format standard; XAF 4.0 schema | Essential for accountant workpapers |
| https://www.regelspraak.nl | RegelSpraak (Belastingdienst AI-developed rules) | HIGH | Community-validated tax rule language | Official rules in structured form |

---

## MEDIUM-HIGH: Established & widely trusted

| URL | Name | Trust | Used for | Caveats |
|-----|------|-------|----------|---------|
| https://www.jortt.nl | Jortt AI Boekhoudbot | MEDIUM-HIGH | Reference for deterministic-first architecture, fixed rule patterns, Belastingdienst integration | Closed-source; claims high automation but logic not publicly verifiable |
| https://github.com/vas3k/TaxHacker | TaxHacker (OSS receipt extraction) | MEDIUM-HIGH | OCR + document extraction patterns; multi-currency support | 1,327 stars/month; "very early stage" — not production-hardened |
| https://github.com/picqer/moneybird-php-client | picqer/moneybird-php-client | MEDIUM-HIGH | PHP SDK for Moneybird API (read+write) | Last release Apr 14 2025; well-maintained, mature |
| https://github.com/picqer/exact-php-client | picqer/exact-php-client | MEDIUM-HIGH | PHP SDK for Exact Online (read+write) | Last release Dec 19 2025; mature, widely used |
| https://github.com/php-twinfield/twinfield | php-twinfield (SOAP client) | MEDIUM-HIGH | Twinfield enterprise bookkeeping integration | Last release Jan 5 2026; enterprise-grade, SOAP-heavy |

---

## MEDIUM: Community-maintained, require local validation

| URL | Name | Trust | Used for | Caveats |
|-----|------|-------|----------|---------|
| https://github.com/openaccountants/openaccountants | OpenAccountants Netherlands | MEDIUM | Dutch tax classification rules, VAT patterns, conservative defaults, skill templates | Q3 / AI-drafted / not independently verified; 2025 values stale; use structure only, replace all numeric values |
| https://github.com/vanderheijden86/moneybird-mcp-server | moneybird-mcp-server | MEDIUM | Moneybird API ingestion via MCP (read+write contacts, invoices, accounts) | Prototype→early-production; v35 commits; use for connector only, not tax logic |
| https://github.com/cdata/exact-online-mcp-server | exact-online-mcp-server-by-cdata | MEDIUM | Exact Online API ingestion via MCP (read-only JDBC) | OSS is read-only; production would need write extensions |
| https://github.com/rivradev/recite-agent-skill | Recite Agent Skill | MEDIUM | Receipt scanning via Recite Vision API | Single-author; relies on external Recite API |
| https://pypi.org/project/smartledger-mcp | SmartLedger MCP | MEDIUM | Offline bookkeeping categorization + tax-ready summaries | MIT licensed, active; requires Python 3.10+; deterministic reference |
| https://www.belastaar.nl | Belastbaar MCP Server | MEDIUM | Tax rates, brackets, knowledge guides for 2024–2025 | 2026 data not available; closed-source; not independently audited |
| https://blog.kilo.ai/p/how-a-founder-replaced-accountant-with-kiloclaw | KiloClaw writeup | MEDIUM | Proof-of-concept: AI-assisted Dutch bookkeeping, expense categorization | Single-user anecdotal; not independently verifiable; saved €420/month |
| https://github.com/Sikerdebaard/income-tax-optimizer | Dutch Income Tax Optimizer | MEDIUM | Gradient-descent patterns for Box 1 + Box 3 optimization | Requires annual parameter updates; local minima risk; not integrated to ledger |
| https://github.com/ossobv/exactonline | ossobv/exactonline (Python/LGPL) | MEDIUM | Python REST client for Exact Online | Community-maintained, not official; mostly read with some adapters |
| https://github.com/onetoweb/eboekhouden | onetoweb/eboekhouden (PHP) | MEDIUM | e-Boekhouden API client | Community-maintained; check currency vs API changes |

---

## MEDIUM-LOWER: Emerging & experimental

| URL | Name | Trust | Used for | Caveats |
|-----|------|-------|----------|---------|
| https://speedy-eboekhouden.vercel.app | Speedy e-Boekhouden | MEDIUM-LOWER | Receipt OCR, refund matching, hours tracking patterns for e-Boekhouden | v1.3.1 (Apr 8 2026); explicitly "use at own risk"; young, not production-hardened |
| https://github.com/openaccountants/openaccountants/tree/main/packages/netherlands | OpenAccountants Netherlands package | MEDIUM-LOWER | Skill files for tax classification, VAT, ZZP deductions | Last commit Apr 2026; 41 stars; structure OK, values stale |
| https://forbesjapan.com/articles/detail/95382 | Claude Code Sub-Agent Pattern (Japanese) | MEDIUM-LOWER | Two-stage classification (deterministic + LLM fallback) | Japanese context; published by licensed professional; pattern highly relevant |
| https://www.xtroverso.nl | XTROVERSO Year-End Checklist | MEDIUM-LOWER | Procedural checklist for ZZP/DGA structures, WKR, mixed-use, iXBRL | Specialized Dutch accounting firm; prevents standard Belastingdienst corrections |

---

## LOWER: Historical or proof-of-concept only

| URL | Name | Trust | Used for | Caveats |
|-----|------|-------|----------|---------|
| https://devpost.com/software/flowstate-xmv09t | FlowState (hackathon) | LOWER | Proof-of-concept: multi-agent transaction matching (bunq + OpenClaw) | Hackathon project only; not production-proven |
| https://github.com/Lovely-mcinerney/claude-md-docs | Claude Skills Architecture | LOWER | Reference for modular instruction structure, hallucination prevention | General pattern; not Dutch-specific |

---

## Usage notes

### When citing a source

- For all Belastingdienst pages: Capture HTML hash + access date (subject to change)
- For all rates/thresholds: Check quarterly against live Belastingdienst pages
- For OpenAccountants: Use structure/patterns only; replace all numeric values
- For community MCP servers: Test connectors thoroughly before production use
- For writeups/case studies: Use as reference patterns, not authoritative proof

### Confidence in numbers

Mark confidence level when citing year-specific values:

- **HIGH**: Belastingdienst official page with date captured
- **MEDIUM**: Multiple sources agree; one version-pinned
- **MEDIUM (flag)**: Only one source found; not independently verified
- **LOW**: Anecdotal or single case study

### Missing sources for 2026

- **DGA gebruikelijk loon norm**: Only 2025 value (€56k) available; verify with Belastingdienst before use
- **Box 1 Bracket 1 rate**: 35.75% recorded with confidence MEDIUM; verify against live Belastingdienst

---

## Cross-links

- See `compliance.md` for audit-readiness contract (how to cite sources in outputs)
- See `liability.md` for hard "no" rules on autonomous filings (always escalate to accountant)
- See `../05-rules-2026/` for all numeric rules with source citations
- See `../04-prompts/accountant-handoff.md` for escalation templates

---

## Sources

note1#L23, L452 (OpenAccountants reliability); note2#L709 (KVK API); deep-report#L8-9, L48-51, L554, L562, L564, L568, L572, L576, L579 (all Belastingdienst + connectors); note3#C23000-23150 (empowerment); decisions.md#L28-31 (DGA 2026 unknown).
