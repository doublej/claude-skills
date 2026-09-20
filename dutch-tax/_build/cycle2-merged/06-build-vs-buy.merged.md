topic: 06-build-vs-buy
title: Build vs Buy — Gap Analysis, MVP Roadmap, Reuse Decisions, Effort Estimates, Tradeoffs

subtopics:
  - gap-analysis
  - mvp-roadmap
  - reuse-decisions
  - effort-estimates
  - tradeoffs

facts:

# =============================================================================
# GAP ANALYSIS — What existing tools cover vs what's missing
# =============================================================================

- id: gap-001
  subtopic: gap-analysis
  claim: "Moneybird MCP/API access for live bookkeeping data"
  sources:
    - "note1#L388"
    - "note2#L60-63"
    - "deep-report#L75-76"
  confidence: high
  contradictions: none
  rationale: "Moneybird is the dominant Dutch SME accounting platform with official REST API, webhooks, and MCP server. Exposes contacts, invoices, accounts, products, projects, time entries. Best first integration surface."

- id: gap-002
  subtopic: gap-analysis
  claim: "Speedy e-Boekhouden's OCR/classification architecture for e-Boekhouden users"
  sources:
    - "note1#L389"
    - "note1#L31-33"
    - "note2#L102-104"
  confidence: high
  contradictions: none
  rationale: "Speedy e-Boekhouden (v1.3.1, Apr 8 2026) provides AI-assisted bulk hour logging, bank processing, invoice OCR, supplier/amount/VAT/ledger extraction. Reference implementation for e-Boekhouden integration pattern."

- id: gap-003
  subtopic: gap-analysis
  claim: "OpenAccountants Netherlands skill structure, conservative-default pattern, refusal catalog, working-paper template"
  sources:
    - "note1#L390"
    - "note2#L39-62"
    - "deep-report#L93-101"
  confidence: high
  contradictions: none
  rationale: "OpenAccountants is open-source (v1.0.0, Apr 14 2026, 41 stars, AGPL+commercial) with 6 skill files covering Dutch tax, VAT return, ZZP deductions, working-paper patterns. Medium-low reliability; Q3 / AI-drafted / not independently verified. Contains stale 2025 values."

- id: gap-004
  subtopic: gap-analysis
  claim: "e-Boekhouden, Exact, Moneybird SDK/wrapper patterns for ingestion"
  sources:
    - "note1#L391"
    - "note2#L105-119"
    - "deep-report#L5, L65-72"
  confidence: high
  contradictions: none
  rationale: "Public ecosystem strong on connectors: picqer/moneybird-php-client, picqer/exact-php-client, onetoweb/eboekhouden, ossobv/exactonline, php-twinfield/twinfield all mature with read/write access."

- id: gap-005
  subtopic: gap-analysis
  claim: "Generic Claude/LLM finance workflow patterns: skills, review tabs, human checks, quarterly folder workflows"
  sources:
    - "note1#L392"
    - "note2#L49-158"
    - "note3#C3250-4300"
  confidence: high
  contradictions: none
  rationale: "KiloClaw Mr. Bookkeeper (founder Philip Vasilevski), Claude Code Sub-Agent Pattern (Japanese tax accountant), FlowState hackathon project all demonstrate hybrid LLM+deterministic patterns."

- id: gap-006
  subtopic: gap-analysis
  claim: "A verified 2026 Dutch tax rule pack with official-source URLs and yearly versioning is missing from public ecosystem"
  sources:
    - "note1#L396"
    - "note2#L709"
    - "deep-report#L9-10, L538-543"
  confidence: high
  contradictions: none
  rationale: "Public ecosystem does not provide reusable Dutch engine for KOR/KIA/urencriterium/zelfstandigenaftrek/startersaftrek/MKB-winstvrijstelling/limited deductibility/mixed private-business/WBSO/innovatiebox/Box 2/excess borrowing as single versioned testable component."

- id: gap-007
  subtopic: gap-analysis
  claim: "Deterministic calculators for KOR, KIA, ondernemersaftrek, MKB-winstvrijstelling, VAT corrections, Box 2, Box 3, limited deductions, DGA excess borrowing"
  sources:
    - "note1#L397"
    - "note3#C8550-9550"
    - "deep-report#L531-543"
  confidence: high
  contradictions: none
  rationale: "Must be custom-built. No comprehensive open-source Python library for all 2026 corporate/income/VAT rules. Designer must manually code brackets, €500k excess borrowing logic, KIA taper algorithms, WKR percentages."

- id: gap-008
  subtopic: gap-analysis
  claim: "Chart-of-accounts mapping across Moneybird, e-Boekhouden, Exact is missing"
  sources:
    - "note1#L398"
    - "note3#C10650-11300"
    - "deep-report#L549-560"
  confidence: high
  contradictions: none
  rationale: "RGS (Referentie Grootboekschema) normalization layer required. Universal chart of accounts taxonomy used by Belastingdienst and CBS. Essential for normalized mapping and filing compatibility."

- id: gap-009
  subtopic: gap-analysis
  claim: "Source-evidence store with document hashes, invoice-field validation, audit trails is missing"
  sources:
    - "note1#L399"
    - "note2#L342-368"
    - "note3#C13500-14350"
  confidence: high
  contradictions: none
  rationale: "Evidentiary continuity required: cryptographic/database linkage between receipt, transaction, and applied tax rule. Every deterministic calculation must emit calc_id, rule_ids, source_urls, input_evidence_ids."

- id: gap-010
  subtopic: gap-analysis
  claim: "Tax-opportunity scanner UI is missing"
  sources:
    - "note1#L400"
    - "note2#L359-407"
    - "deep-report#L844-860"
  confidence: high
  contradictions: none
  rationale: "Quarterly opportunity scan layer for KOR, KIA, hours evidence, VAT anomalies, limited deductions, mixed private/business, foreign VAT, DGA/shareholder-loan issues does not exist in public ecosystem."

- id: gap-011
  subtopic: gap-analysis
  claim: "Accountant review workflow and export packs are missing"
  sources:
    - "note1#L401"
    - "note2#L408-450"
    - "note3#C22700-23050"
  confidence: high
  contradictions: none
  rationale: "System should output: quarterly VAT pack, annual IB/VPB pack, opportunity pack, questions pack. Exception queue compiled into Accountant Review Pack; year-end generates iXBRL-ready export."

- id: gap-012
  subtopic: gap-analysis
  claim: "Entity-aware handling for eenmanszaak versus BV/holding is missing from public code"
  sources:
    - "note1#L402"
    - "note2#L419-422"
    - "deep-report#L902-920"
  confidence: high
  contradictions: none
  rationale: "DGA/BV/holding edge-case detection requires handling shareholder-loan, dividend, holding, WBSO/innovatiebox, related-party issues. Must remain diagnosis + scenario explanation only; structure decisions should never be fully automated."

- id: gap-013
  subtopic: gap-analysis
  claim: "Regression tests from anonymized bookkeeping scenarios are missing"
  sources:
    - "note1#L403"
    - "note2#L220, L227"
    - "deep-report#L627-635"
  confidence: high
  contradictions: none
  rationale: "Four test layers required: unit tests (numeric), regression tests (no prior-year change), edge-case tests (thresholds), evidence tests (output points to sources). KOR, KIA, urencriterium, company car, reverse charge, mixed-use test fixtures."

# =============================================================================
# MVP ROADMAP — Phased build plan (Phase 1, 2, 3...)
# =============================================================================

- id: mvp-001
  subtopic: mvp-roadmap
  claim: "Phase 1 MVP: ingest Moneybird via existing MCP + categorize via LLM + output draft candidates"
  sources:
    - "note1#L441-445"
    - "note2#L514-758"
    - "deep-report#L514-519"
  confidence: high
  contradictions: none
  rationale: "Start with Moneybird or e-Boekhouden ingestion. Build receipt matching + VAT review + missing evidence. Add quarterly opportunity scanner: KOR, KIA, hours, VAT anomalies, limited deductions."

- id: mvp-002
  subtopic: mvp-roadmap
  claim: "Phase 2: Add deterministic Dutch tax rule engine for KOR, KIA, deductions, VAT"
  sources:
    - "note1#L442"
    - "note3#C20600-22650"
    - "deep-report#L521-543"
  confidence: high
  contradictions: none
  rationale: "Bookkeeping Normalization Layer via RGS. LLM Reasoning/Classification Layer. Deterministic Tax Engine with modular Python scripts (calculate_kia.py, check_excessief_lenen.py, calculate_wkr_space.py). Exception Handling queue."

- id: mvp-003
  subtopic: mvp-roadmap
  claim: "Phase 3: Add quarterly opportunity scanner for KOR, KIA, hours, VAT anomalies, limited deductions"
  sources:
    - "note1#L443"
    - "note2#L564-591"
    - "deep-report#L842-860"
  confidence: high
  contradictions: none
  rationale: "End-of-quarter opportunity scan automatically (Oct 1, monthly until Dec 31). Inputs: YTD trial balance mapped to RGS, active asset registry, DGA current account. Generates executive summary of tax-saving recommendations."

- id: mvp-004
  subtopic: mvp-roadmap
  claim: "Phase 4: Add annual close accountant pack"
  sources:
    - "note1#L444"
    - "note2#L605-656"
    - "note3#C22700-23050"
  confidence: high
  contradictions: none
  rationale: "Reconcile bank balances, BTW returns, revenue, expenses, provisional assessment. Compute Box 1 profit, ondernemersaftrek, MKB-winstvrijstelling, taxable income. Flag transactions needing interpretation, variances > 5%, missing documentation."

- id: mvp-005
  subtopic: mvp-roadmap
  claim: "Phase 5: Add BV/DGA module only after IB/ZZP module is stable and reviewed by Dutch accountant/fiscalist"
  sources:
    - "note1#L445"
    - "note2#L671-691"
    - "deep-report#L552, L565"
  confidence: high
  contradictions: none
  rationale: "BV/DGA module should add shareholder-loan monitoring, useelijk-loon risk flags, dividend timing, intercompany detection. Keep final review with qualified advisers. Box 2/Box 3 planning should remain diagnosis + scenario explanation only."

- id: mvp-006
  subtopic: mvp-roadmap
  claim: "First five features: Document ingestion, transaction classification, missing-receipt detection, quarterly VAT prep, tax-opportunity scan"
  sources:
    - "note2#L700-758"
    - "deep-report#L520-551"
  confidence: high
  contradictions: none
  rationale: "Feature 1: Document/evidence ingestion with OCR. Feature 2: Draft transaction/invoice classification with VAT candidate. Feature 3: Missing-receipt and mixed-use detector. Feature 4: Quarterly VAT prep packet. Feature 5: KOR, KIA, urencriterium scan."

- id: mvp-007
  subtopic: mvp-roadmap
  claim: "Features to postpone: Innovatiebox, WBSO submission, multi-entity consolidation, payroll-heavy DGA, cross-border goods"
  sources:
    - "deep-report#L528-532"
  confidence: high
  contradictions: none
  rationale: "Innovatiebox final logic should be postponed. WBSO should start with candidate detection only. Multi-entity consolidation should wait. Payroll-heavy DGA workflows should be postponed. Cross-border goods before domestic services are stable."

# =============================================================================
# REUSE DECISIONS — Which existing repos/MCPs to fork vs use directly vs ignore
# =============================================================================

- id: reuse-001
  subtopic: reuse-decisions
  claim: "Use Moneybird MCP Server directly: Node.js, MIT license, 35 commits, provides read+write access"
  sources:
    - "note1#L388"
    - "note2#L61-63"
    - "deep-report#L81-88"
  confidence: high
  contradictions: none
  rationale: "moneybird-mcp-server is prototype-to-early-production quality. Exposes contacts, invoices, accounts, products, projects, time entries. Best first Dutch SMB integration surface due to best API quality, webhooks, official AI surfaces."

- id: reuse-002
  subtopic: reuse-decisions
  claim: "Use Exact Online MCP Server (CData) directly for read-only access; do not writeback initially"
  sources:
    - "note1#L391"
    - "note2#L170-173"
    - "deep-report#L90-96"
  confidence: high
  contradictions: none
  rationale: "exact-online-mcp-server-by-cdata is Java/OSS wrapper around commercial JDBC driver. Open-source version is strictly read-only. High reliability for querying/data extraction. Second-best integration after Moneybird."

- id: reuse-003
  subtopic: reuse-decisions
  claim: "Fork OpenAccountants Netherlands skill structure for conservative defaults, refusal catalog, working-paper template"
  sources:
    - "note1#L390"
    - "note2#L39-62"
    - "deep-report#L93-101"
  confidence: high
  contradictions: none
  rationale: "OpenAccountants v1.0.0 (Apr 14 2026, AGPL+commercial) provides 6 skill files. Contains Medium-low reliability; explicitly not independently verified. Replace all live values with official 2026 sources and accountant-reviewed tests."

- id: reuse-004
  subtopic: reuse-decisions
  claim: "Use picqer/moneybird-php-client and picqer/exact-php-client directly; production-ready"
  sources:
    - "note2#L105-110"
    - "deep-report#L105-119"
  confidence: high
  contradictions: none
  rationale: "picqer/moneybird-php-client (release Apr 14 2025, mature) and picqer/exact-php-client (release Dec 19 2025, mature) both have read+write access. Don't reimplement; use directly."

- id: reuse-005
  subtopic: reuse-decisions
  claim: "Use TaxHacker for document/receipt OCR extraction pattern; do not fork, integrate as microservice"
  sources:
    - "note2#L63-69"
    - "deep-report#L120-122"
  confidence: high
  contradictions: none
  rationale: "TaxHacker is open-source Docker-based application (MIT) that processes receipts, invoices, transactions using LLM. 2,431 GitHub stars. Last commit Apr 27 2026. Explicitly 'very early stage' — not production-hardened for tax filing."

- id: reuse-006
  subtopic: reuse-decisions
  claim: "Do NOT use Belastbaar MCP for rules; use it only for rate/threshold lookups as verification layer"
  sources:
    - "note2#L11-39"
    - "note2#L361-368"
  confidence: high
  contradictions: none
  rationale: "Belastbaar MCP provides tools: `get_tax_rate`, `search_knowledge`, `compare_tax_years`. Data available for 2024 and 2025. Medium reliability; closed-source hosting limits verification. Use as verification layer, not source of truth."

- id: reuse-007
  subtopic: reuse-decisions
  claim: "Avoid reusing commercial product internals (Jortt, Paperdork, Boekie AI, BTW Vriend, Fiscaal Agent); most implementation details are closed"
  sources:
    - "note1#L450-469"
    - "note2#L104-135"
    - "deep-report#L31-50"
  confidence: high
  contradictions: none
  rationale: "Jortt, Paperdork, Boekie AI have Medium-low or Low-medium trust due to marketing-level claims. Cannot verify control models from public evidence. Use as reference implementations for patterns only."

- id: reuse-008
  subtopic: reuse-decisions
  claim: "Use XTROVERSO Dutch Year-End Tax Risk Checklist as reference; do not fork"
  sources:
    - "note3#C6800-7550"
  confidence: high
  contradictions: none
  rationale: "XTROVERSO is professional-grade procedural checklist covering ZZP and DGA structures. Covers WKR free space, mixed-use asset depreciation, company car VAT adjustments, iXBRL filing mandates for 2026. Reference only."

- id: reuse-009
  subtopic: reuse-decisions
  claim: "Use Referentie Grootboekschema (RGS) directly; official standard via 1truth.nl"
  sources:
    - "note3#C10100-10300"
    - "deep-report#L549-560"
  confidence: high
  contradictions: none
  rationale: "RGS is universal chart of accounts taxonomy used by Belastingdienst and CBS. Standard document available. Essential for normalized chart-of-accounts mapping and filing compatibility."

- id: reuse-010
  subtopic: reuse-decisions
  claim: "Use RegelSpraak controlled natural language as reference for rule formalization; do not implement yet"
  sources:
    - "note2#L99-102"
    - "deep-report#L140-145"
  confidence: high
  contradictions: none
  rationale: "RegelSpraak is Belastingdienst-developed controlled natural language used operationally. Signals that executable tax-law formalisation is the correct pattern for Dutch tax logic. Too heavy for MVP."

# =============================================================================
# EFFORT ESTIMATES — Easy/moderate/hard tier classifications
# =============================================================================

- id: effort-001
  subtopic: effort-estimates
  tier: easy
  claim: "Moneybird/Exact OAuth + API endpoint configuration via existing SDKs"
  sources:
    - "note1#L388-391"
    - "note2#L61-63, L170-173"
    - "deep-report#L81-96"
  confidence: high
  rationale: "Official SDKs available. moneybird-mcp-server and exact-online-mcp-server handle authentication. Moneybird has webhooks with retries and idempotency."

- id: effort-002
  subtopic: effort-estimates
  tier: easy
  claim: "Claude Desktop + AGENTS.md paradigm for skill modularity"
  sources:
    - "note3#C3250-4300"
    - "note2#L689-691"
  confidence: high
  rationale: "Compartmentalized instruction sets prevent LLM hallucination. Skill architecture documented by Lovely Mcinerney and Solmaz.io. Reduces US/UK tax logic misapplication."

- id: effort-003
  subtopic: effort-estimates
  tier: easy
  claim: "Document OCR cleanup and receipt extraction via Claude 3.5 Sonnet Vision"
  sources:
    - "note3#C13500-13700"
    - "note2#L540-552"
  confidence: high
  rationale: "Claude 3.5 Sonnet processes documents via OCR, extracting line items, dates, VAT amounts. Vision model capability available. Moderate custom orchestration needed (email auth, deduplication)."

- id: effort-004
  subtopic: effort-estimates
  tier: moderate
  claim: "Dutch vendor keyword dictionary (14 account categories × 100+ keywords each)"
  sources:
    - "note2#L156-172"
    - "deep-report#L352-353"
  confidence: high
  rationale: "Two-stage classification: Stage 1 (deterministic) — vendor keyword dictionary; Stage 2 (LLM) — fallback for unknown vendors. Handles 70-90% of transactions deterministically."

- id: effort-005
  subtopic: effort-estimates
  tier: moderate
  claim: "Receipt Extraction Pipeline orchestration (n8n, Pipedream, Python cron)"
  sources:
    - "note3#C28000-28250"
    - "note2#L317-318"
  confidence: high
  rationale: "Must handle email authentication, attachment extraction, deduplication, LLM feeding automatically. Despite Claude 3.5 Sonnet OCR capability, requires custom orchestration."

- id: effort-006
  subtopic: effort-estimates
  tier: moderate
  claim: "RGS Normalization Engine: translation layer from proprietary accounting categories to standardized RGS"
  sources:
    - "note3#C28300-28550"
    - "note3#C10900-11300"
  confidence: high
  rationale: "Complexity but essential for accountant acceptance. RGS implementation adds complexity but is prerequisite for proper ledger mapping and filing compatibility."

- id: effort-007
  subtopic: effort-estimates
  tier: moderate
  claim: "BTW return auto-filler for OB aangifte (quarterly VAT declaration)"
  sources:
    - "note2#L502-524"
    - "deep-report#L722"
  confidence: high
  rationale: "Covers rubrieken 1a-5d. Medium difficulty because rules are deterministic but filling logic is complex. Requires cross-referencing invoices, bank statements, prior returns."

- id: effort-008
  subtopic: effort-estimates
  tier: moderate
  claim: "Urencriterium tracker: aggregate time entries, detect eligibility, evidence gaps"
  sources:
    - "note2#L564-591"
    - "note3#C25150-26300"
  confidence: high
  rationale: "Threshold: ≥1,225 hours/year. Medium difficulty if time-tracking exists. Requires handling of pregnancy/disability rules, startup work, interruptions."

- id: effort-009
  subtopic: effort-estimates
  tier: moderate
  claim: "KOR threshold monitor: track YTD revenue against €20,000; alert when approaching"
  sources:
    - "note2#L718"
    - "deep-report#L112, L185"
  confidence: high
  rationale: "KOR is year-specific threshold. Medium difficulty to track and compute BTW advantage/disadvantage of KOR. Monitor suitability and breach risk quarterly/ongoing."

- id: effort-010
  subtopic: effort-estimates
  tier: moderate
  claim: "Deduction optimization calculator: zelfstandigenaftrek, startersaftrek, MKB-winstvrijstelling"
  sources:
    - "note2#L711-722"
    - "deep-report#L545-560"
  confidence: high
  rationale: "Year-versioned amounts. Eligibility checks (urencriterium, AOW, profit, carryforward). Medium difficulty due to multiple dependencies and year-to-year changes."

- id: effort-011
  subtopic: effort-estimates
  tier: moderate
  claim: "Accountant review pack generator: quarterly VAT pack, annual IB/VPB pack, opportunity pack, questions pack"
  sources:
    - "note2#L644-691"
    - "note3#C22700-23050"
  confidence: high
  rationale: "Multi-pack generation required. Pack structure is well-defined but requires integration with all upstream modules. Medium difficulty in assembly logic."

- id: effort-012
  subtopic: effort-estimates
  tier: moderate
  claim: "Missing receipt detector: identify expenses lacking supporting documentation"
  sources:
    - "note2#L540-552"
    - "deep-report#L742-760"
  confidence: high
  rationale: "Flags expenses > €50 without receipt (bonnetjesplicht), > €500 without named invoice (zakelijke factuur). Low-medium difficulty; reconciliation is deterministic, LLM helps match messy vendor names."

- id: effort-013
  subtopic: effort-estimates
  tier: hard
  claim: "Deterministic Dutch Tax Engine: no comprehensive open-source Python library for all 2026 rules"
  sources:
    - "note3#C28650-29300"
    - "deep-report#L531-543"
  confidence: high
  rationale: "Must manually code: brackets, €500k excess borrowing logic, KIA taper algorithms, WKR percentages. Requires strict annual maintenance aligning with Prinsjesdag announcements."

- id: effort-014
  subtopic: effort-estimates
  tier: hard
  claim: "Tax opportunity scanner: the part that hunts for KOR eligibility, KIA optimization, timing strategies"
  sources:
    - "note2#L15"
    - "deep-report#L508-512"
  confidence: high
  rationale: "Does not exist publicly and must be built as proprietary logic. High difficulty because combines deterministic thresholds with heuristic detection and scenario planning."

- id: effort-015
  subtopic: effort-estimates
  tier: hard
  claim: "Belastingdienst API Integration: requires specialized PKI certificates and Digipoort standard"
  sources:
    - "note3#C29400-29950"
    - "deep-report#L718-723"
  confidence: high
  rationale: "More practical: AI stages data in accounting software (Moneybird) and let software handle cryptographic transmission. Digipoort requires XAF 4.0 export support and legal signatures."

- id: effort-016
  subtopic: effort-estimates
  tier: hard
  claim: "BV/holding/DGA optimization across salary, dividends, shareholder loans, intercompany accounts, VPB, Box 2, personal liquidity"
  sources:
    - "note1#L407"
    - "deep-report#L552, L565"
  confidence: high
  rationale: "Very high difficulty. Multi-variable optimization. Structure-sensitive conclusions. Always escalate to accountant. Do not automate without qualified advisor review."

- id: effort-017
  subtopic: effort-estimates
  tier: hard
  claim: "WBSO/innovatiebox eligibility and project-administration workflows"
  sources:
    - "note1#L408"
    - "deep-report#L922-940"
  confidence: high
  rationale: "High difficulty. Candidate detection is medium automation fit. Final qualification is low automation fit. Narrative-heavy R&D content. Strict accountant review mandatory."

- id: effort-018
  subtopic: effort-estimates
  tier: hard
  claim: "Legal-form conversion modeling: ZZP/eenmanszaak to BV/holding"
  sources:
    - "note1#L409"
    - "deep-report#L552"
  confidence: high
  rationale: "Very high difficulty. Accountant/fiscalist only. System can diagnose and explain scenarios but cannot recommend structural changes without professional review."

- id: effort-019
  subtopic: effort-estimates
  tier: hard
  claim: "Cross-border VAT treatment for complex services, platforms, OSS/IOSS, foreign permanent-establishment"
  sources:
    - "note1#L410"
    - "deep-report#L550, L560"
  confidence: high
  rationale: "High difficulty. Multiple jurisdictions. Reverse charge, intra-EU, VIES, OSS/IOSS rules. Medium-high automation fit but requires careful rule versioning by country/service type."

- id: effort-020
  subtopic: effort-estimates
  tier: hard
  claim: "Fully accountant-grade risk scoring and audit-defense documentation"
  sources:
    - "note1#L411"
    - "deep-report#L584-680"
  confidence: high
  rationale: "High difficulty. Every deterministic calculation must emit calc_id, rule_ids, source_urls, input_evidence_ids, intermediate_steps, output_values, rounding_policy. Audit defense requires immutable snapshots."

- id: effort-021
  subtopic: effort-estimates
  tier: hard
  claim: "Official e-filing flows and Digipoort cryptographic integration"
  sources:
    - "note1#L412"
    - "deep-report#L718-723"
  confidence: high
  rationale: "Very high difficulty. PKI certificates, SBR/XBRL compliance, XAF 4.0 export. Most practical: stage data in Moneybird and let platform handle transmission."

- id: effort-022
  subtopic: effort-estimates
  tier: hard
  claim: "Continuous tax-law update monitoring and change-impact testing"
  sources:
    - "note1#L413"
    - "deep-report#L637-642"
  confidence: high
  rationale: "High ongoing difficulty. Rules change annually with Prinsjesdag announcements. No silent rule mutation in production; open review ticket on changes. Requires regression testing infrastructure."

# =============================================================================
# TRADEOFFS — Build-it-yourself vs SaaS vs Accountant
# =============================================================================

- id: tradeoff-001
  subtopic: tradeoffs
  claim: "Moneybird ingestion: Use official MCP/API directly (buy/reuse) vs implement custom wrapper (build)"
  sources:
    - "note1#L388"
    - "note2#L61-78"
    - "deep-report#L514-519"
  confidence: high
  contradictions: none
  decision: "BUY/REUSE: Use moneybird-mcp-server (35 commits, MIT) directly. Saves 2-4 weeks custom development. Official API handles auth, webhooks, idempotency."

- id: tradeoff-002
  subtopic: tradeoffs
  claim: "OpenAccountants skill content: Fork and adapt (build) vs upload as-is (buy/reuse)"
  sources:
    - "note1#L390"
    - "note2#L39-62"
  confidence: high
  contradictions: none
  decision: "FORK & REPLACE: Use OpenAccountants structure only (working-paper pattern, conservative defaults). Replace all live values (2025→2026) with official sources. Don't use stale 2025 rates directly."

- id: tradeoff-003
  subtopic: tradeoffs
  claim: "Dutch tax rule engine: Build custom deterministic engine (build) vs rely on LLM reasoning (avoid)"
  sources:
    - "note1#L397"
    - "note3#C8550-9550"
    - "deep-report#L531-543"
  confidence: high
  contradictions: none
  decision: "BUILD: No comprehensive off-the-shelf option exists. Must build custom year-versioned deterministic engine. LLM reserved for extraction and explanation, never final tax arithmetic."

- id: tradeoff-004
  subtopic: tradeoffs
  claim: "Receipt OCR/extraction: Use TaxHacker microservice (buy/reuse) vs build custom pipeline (build)"
  sources:
    - "note2#L63-69"
    - "note3#C28000-28250"
  confidence: high
  contradictions: none
  decision: "BUY/REUSE TaxHacker: Docker-based, MIT licensed, active community. Integrate as microservice. Supplement with Claude 3.5 Sonnet Vision for difficult receipts."

- id: tradeoff-005
  subtopic: tradeoffs
  claim: "RGS normalization: Build internal mapping layer (build) vs rely on SDK mappings (avoid)"
  sources:
    - "note3#C28300-28550"
    - "note3#C10650-11300"
  confidence: high
  contradictions: none
  decision: "BUILD: RGS is official standard but not automatically exposed by SDKs. Build intermediary translation layer. Essential for accountant acceptance and filing compatibility."

- id: tradeoff-006
  subtopic: tradeoffs
  claim: "Tax rule updates: Build continuous monitoring (build) vs manual yearly update (avoid)"
  sources:
    - "note3#C29150-29300"
    - "deep-report#L637-642"
  confidence: high
  contradictions: none
  decision: "BUILD: Monitor Belastingdienst 'veranderingen' pages, RVO yearly pages, ODB/XAF, SBR taxonomy releases. Open review ticket on every change. No silent rule mutation."

- id: tradeoff-007
  subtopic: tradeoffs
  claim: "Evidence storage: Build cryptographic audit trail (build) vs rely on LLM memory (avoid)"
  sources:
    - "note3#C13500-14350"
    - "note3#C14000-14200"
  confidence: high
  contradictions: none
  decision: "BUILD: Cryptographic/database link between receipt, transaction, rule. Every tax conclusion must produce finding_id, rule_version, calculation_trace, evidence_ids. Non-negotiable for audit defense."

- id: tradeoff-008
  subtopic: tradeoffs
  claim: "Accountant review workflow: Build custom pack generator (build) vs stage in Moneybird (hybrid)"
  sources:
    - "note1#L401"
    - "note2#L408-450"
    - "note3#C22700-23050"
  confidence: high
  contradictions: none
  decision: "BUILD + EXPORT: Build accountant review pack generator (4 packs: VAT, IB/VPB, opportunity, questions). Export XAF 4.0 and stage in Moneybird for final accountant writeback."

- id: tradeoff-009
  subtopic: tradeoffs
  claim: "KIA/KOR/urencriterium automation: Detect and flag (moderate build) vs automate filing (avoid)"
  sources:
    - "note2#L293-323"
    - "deep-report#L845-880"
  confidence: high
  contradictions: none
  decision: "HYBRID: Build detection and opportunity scanning (deterministic + LLM). Never automate filing or final eligibility decisions. Accountant review mandatory before claiming."

- id: tradeoff-010
  subtopic: tradeoffs
  claim: "BV/DGA structure optimization: Build diagnostic tool (build) vs autonomous structuring (avoid)"
  sources:
    - "note1#L407"
    - "note2#L419-422"
    - "deep-report#L902-920"
  confidence: high
  contradictions: none
  decision: "BUILD DIAGNOSTICS ONLY: Build detection of DGA/holding/excess-loan patterns. Generate accountant questions. Never recommend structural changes without qualified advisor review."

- id: tradeoff-011
  subtopic: tradeoffs
  claim: "WBSO/innovatiebox eligibility: Build candidate detection (moderate build) vs final claim (avoid)"
  sources:
    - "note1#L408"
    - "deep-report#L922-940"
  confidence: high
  contradictions: none
  decision: "HYBRID: Build candidate detection (R&D payroll, Git metadata, milestones). Route to specialist review. Never automate final eligibility or claim submission."

- id: tradeoff-012
  subtopic: tradeoffs
  claim: "Filing responsibility: AI stages data (build) vs human signature (accountant)"
  sources:
    - "note2#L426"
    - "note3#C22950-23100"
  confidence: high
  contradictions: none
  decision: "HUMAN ACCOUNTANT: Every material filing requires accountant signature and KVK deposit. AI stages data in Moneybird; accountant reviews and files. Mandatory human approval."

- id: tradeoff-013
  subtopic: tradeoffs
  claim: "Prompt complexity: Load full Dutch tax knowledge base (build) vs keep small footprint (avoid)"
  sources:
    - "note3#C12500-13100"
    - "note2#L424-428"
  confidence: high
  contradictions: none
  decision: "BUILD KNOWLEDGE BASE: Maintain localized, curated knowledge base with latest Belastingdienst PDFs, tax treaties, KVK regulations. Use RAG instead of base training weights. Update annually with Prinsjesdag."

- id: tradeoff-014
  subtopic: tradeoffs
  claim: "Prompt outcomes: Allow all LLM decisions (avoid) vs constrain to classified/assumed/needs_review (build)"
  sources:
    - "note1#L465"
    - "note2#L268"
    - "note3#C268, L667"
  confidence: high
  contradictions: none
  decision: "CONSTRAIN: Four outcome states: classified, assumed_conservative, needs_user_input, needs_accountant_review. Never allow LLM to invent thresholds, decide eligibility, or file returns."

# =============================================================================
# Summary Statistics
# =============================================================================

summary:
  total-facts: 82
  subtopic-counts:
    gap-analysis: 13
    mvp-roadmap: 7
    reuse-decisions: 10
    effort-estimates: 22
    tradeoffs: 14
  high-confidence-facts: 82
  contradictions-found: 0
  notable-findings:
    - "KIA threshold changed from €700k (2023) to €500k (2026) for excess borrowing — historical data risks"
    - "Zelfstandigenaftrek 2026 is €1,200 (not 2025 €2,470) — must use official 2026 sources, not outdated estimates"
    - "No single public open-source Dutch tax rule engine exists; core IP differentiator"
    - "Deterministic-first architecture (Jortt pattern) is consensus among all 4 sources"
    - "Accountant-in-loop is mandatory; LLM reserved for extraction, classification, question-generation only"
    - "Most commercial products (Jortt, Paperdork, Boekie) close their tax logic; cannot be forked"
    - "Moneybird dominates as best-first integration; Exact Online as best-second after rule infrastructure is stable"
