topic: 07-risks-sources
title: "Merged Risk & Source Analysis"
subtopics:
  - compliance
  - liability
  - source-table
  - model-risk
  - data-residency
  - audit-readiness

---

## compliance

- claim: "Belastingdienst requires 7-year document retention for VAT and IB"
  sources:
    - "note1#L500-510"
    - "note3#L13300-13450"
  confidence: high
  contradictions: none
  mitigation: "Implement document hash storage and cryptographic linking; maintain immutable evidence store with 7-year minimum retention"

- claim: "Belastingdienst audit posture: rule-based deterministic approach preferred over AI-invented positions to avoid scrutiny"
  sources:
    - "note2#L121"
    - "deep-report#L8-9"
  confidence: high
  contradictions: none
  mitigation: "Lock all tax calculations into deterministic, versioned rule engines; never allow LLM to invent rates or thresholds"

- claim: "Mixed business/private expense optimization marked High risk for Belastingdienst scrutiny"
  sources:
    - "note2#L308"
  confidence: medium
  contradictions: none
  mitigation: "Conservative default: when uncertain, classify at higher cost (21% VAT if ambiguous); require accountant review for >50% private-use claims"

- claim: "VAT correction deadline: 8-week timing after discovery of error; penalties if late"
  sources:
    - "deep-report#L84, L141-143"
  confidence: high
  contradictions: none
  mitigation: "Flag correction candidates within 8 weeks; maintain suppletie form queue for >€1,000 corrections"

- claim: "BTW on food/drink consumed on-premises NOT deductible as input tax (Belastingdienst rule 2026)"
  sources:
    - "note3#C24650-24850"
  confidence: high
  contradictions: none
  mitigation: "Classify restaurant/food VAT under representatiekosten only; reject input-VAT claims on on-premises consumption"

---

## liability

- claim: "Every AI output carries mandatory disclaimer: 'This must be reviewed by a qualified professional before filing'"
  sources:
    - "note2#L426"
  confidence: high
  contradictions: none
  mitigation: "Enforce disclaimer on all user-facing outputs; block writeback until accountant/user explicitly approves"

- claim: "DGA salary determination marked 'too much legal risk' for AI to decide alone"
  sources:
    - "note2#L771"
  confidence: high
  contradictions: none
  mitigation: "Escalate all DGA salary, dividend, and shareholder-loan decisions to accountant/fiscalist; never output autonomous recommendations"

- claim: "Structural decisions (BV vs eenmanszaak, holding restructuring) should never be left to LLM alone"
  sources:
    - "note2#L770"
  confidence: high
  contradictions: none
  mitigation: "Flag structure-sensitive findings (DGA, excess-borrowing, holding) as mandatory accountant review; output questions only, no recommendations"

- claim: "System must ensure AI remains empowerment tool rather than autonomous liability"
  sources:
    - "note3#C23000-23150"
  confidence: high
  contradictions: none
  mitigation: "Separate 'candidate detection' from 'approved calculation'; require human approval for writebacks and filings"

- claim: "Accountant Handoff protocol ensures system is not forced to resolve highly ambiguous tax scenarios autonomously"
  sources:
    - "note3#C9900-10150"
  confidence: high
  contradictions: none
  mitigation: "Create explicit exception queue for low-confidence items; escalate to accountant with prepared dossier (transaction, OCR, question)"

- claim: "Year-end close requires human accountant signature and KVK deposit"
  sources:
    - "note3#C22950-23100"
  confidence: high
  contradictions: none
  mitigation: "Block export/filing until accountant explicitly signs off; maintain immutable signature record"

---

## source-table

- url: "https://www.belastingdienst.nl"
  name: "Belastingdienst (Dutch Tax Authority) official website"
  trust: high
  used_for: "Official 2026 tax rates, KIA thresholds, KOR rules, VAT rates, Box brackets, excess-borrowing limits, zelfstandigenaftrek/startersaftrek amounts"
  cited_by: ["note1", "note2", "note3", "deep-report"]
  caveat: "HTML/PDF subject to change; capture hashes and versioning metadata"

- url: "https://www.belastingdienst.nl/zakelijk/btw_tarief/btw_tarief"
  name: "Belastingdienst BTW Rates page"
  trust: high
  used_for: "VAT rate definitions 0%, 9%, 21%; rate exceptions and special categories"
  cited_by: ["deep-report#L554"]
  caveat: "Annual updates; requires version pinning"

- url: "https://www.belastingdienst.nl/zakelijk/kleineondernemersregeling"
  name: "Belastingdienst KOR (Small Business Exemption) page"
  trust: high
  used_for: "KOR €20,000 threshold, eligibility rules, VAT exemption consequences"
  cited_by: ["deep-report#L562"]
  caveat: "Threshold year-specific; monitor for changes"

- url: "https://www.belastingdienst.nl/zakelijk/kleinschaligheidsinvesteringsaftrek"
  name: "Belastingdienst KIA (Small-Scale Investment Deduction) page"
  trust: high
  used_for: "KIA 2026 thresholds (€2,901–€398,236), tiered percentages, asset qualification rules"
  cited_by: ["deep-report#L564"]
  caveat: "Tables change annually; verify per tax year"

- url: "https://www.belastingdienst.nl/zakelijk/excessief-lenen-van-bv-beperkt"
  name: "Belastingdienst Excessief Lenen (Excess Borrowing) page"
  trust: high
  used_for: "DGA excess borrowing threshold €500,000, Box 2 treatment"
  cited_by: ["deep-report#L572"]
  caveat: "Threshold changed from €700,000 in 2023; verify current rules"

- url: "https://www.belastingdienst.nl/zakelijk/box_2"
  name: "Belastingdienst Box 2 (Substantial Interest) page"
  trust: high
  used_for: "Box 2 rates 2026, dividend/loan taxation, rate brackets"
  cited_by: ["deep-report#L576"]
  caveat: "Rates change annually; sensitive area for audit"

- url: "https://www.belastingdienst.nl/zakelijk/box_3"
  name: "Belastingdienst Box 3 (Wealth Tax) page"
  trust: high
  used_for: "Box 3 2026 rules, asset categories, provisional percentages, tax-free allowance"
  cited_by: ["deep-report#L579"]
  caveat: "Box 3 year-versioned and sensitive; requires accountant involvement for planning"

- url: "https://www.belastingdienst.nl/zakelijk/mkb_winstvrijstelling"
  name: "Belastingdienst MKB-Winstvrijstelling (SMB Profit Exemption) page"
  trust: high
  used_for: "MKB-winstvrijstelling 12.7% deduction, eligibility for ZZP/eenmanszaak"
  cited_by: ["deep-report#L568"]
  caveat: "Percentage and cap change annually"

- url: "https://www.belastingdienst.nl/zakelijk/zelfstandigenaftrek"
  name: "Belastingdienst Zelfstandigenaftrek (Self-Employed Deduction) page"
  trust: high
  used_for: "Zelfstandigenaftrek €1,200 (2026), eligibility conditions, carryforward rules"
  cited_by: ["note1", "note3"]
  caveat: "Amount changes annually; verify per tax year"

- url: "https://www.rvo.nl"
  name: "RVO (Netherlands Enterprise Agency)"
  trust: high
  used_for: "WBSO R&D tax credit, Innovatiebox rules, EIA/MIA/Vamil investment schemes"
  cited_by: ["note1", "deep-report"]
  caveat: "WBSO and Innovatiebox rules complex and year-versioned; professional review mandatory"

- url: "https://www.kvk.nl"
  name: "KVK (Dutch Chamber of Commerce) API and registry"
  trust: high
  used_for: "Business registration validation, entity types, entrepreneur status, VAT ID verification"
  cited_by: ["note2#L709", "deep-report"]
  caveat: "Real-time API available; use for fact-checking DGA/holding status"

- url: "https://github.com/openaccountants/openaccountants"
  name: "OpenAccountants Netherlands skill package"
  trust: medium
  used_for: "Dutch tax classification rules, VAT return patterns, conservative defaults, skill structure templates"
  cited_by: ["note1", "note2"]
  caveat: "Q3 / AI-drafted / not independently verified; 2025 values stale for 2026; use structure only, replace all numeric values"

- url: "https://github.com/vanderheijden86/moneybird-mcp-server"
  name: "moneybird-mcp-server (MCP connector for Moneybird API)"
  trust: high
  used_for: "Moneybird API ingestion, read+write access to contacts, invoices, accounts, ledger entries"
  cited_by: ["note3", "deep-report"]
  caveat: "Prototype-to-early-production quality; v35 commits as of 2026; use for connector only, not tax logic"

- url: "https://github.com/cdata/exact-online-mcp-server"
  name: "exact-online-mcp-server-by-cdata (MCP connector for Exact Online)"
  trust: high
  used_for: "Exact Online API ingestion via read-only JDBC wrapper"
  cited_by: ["note3", "deep-report"]
  caveat: "OSS version is read-only; production would need write extensions"

- url: "https://www.jortt.nl"
  name: "Jortt AI Boekhoudbot (commercial Dutch bookkeeping platform)"
  trust: medium-high
  used_for: "Reference for deterministic-first architecture, fixed rule patterns, integration with Belastingdienst rules"
  cited_by: ["note1", "note2", "deep-report"]
  caveat: "Closed-source implementation details; claims high automation but logic not publicly verifiable"

- url: "https://github.com/vas3k/TaxHacker"
  name: "TaxHacker (open-source receipt/invoice extraction)"
  trust: medium-high
  used_for: "OCR and document extraction patterns; multi-currency support; early-stage but active community"
  cited_by: ["note2"]
  caveat: "1,327 stars/month growth; explicitly 'very early stage' — not production-hardened for tax filing"

- url: "https://github.com/rivradev/recite-agent-skill"
  name: "Recite Agent Skill (receipt image OCR via Recite Vision API)"
  trust: medium
  used_for: "Receipt scanning and document processing pattern for OpenClaw/Claude Code workflows"
  cited_by: ["note2"]
  caveat: "Single-author project; relies on external Recite Vision API"

- url: "https://pypi.org/project/smartledger-mcp/"
  name: "SmartLedger MCP (Python MCP for invoice/receipt processing)"
  trust: medium
  used_for: "Local, 100% offline bookkeeping categorization and tax-ready summaries"
  cited_by: ["note2"]
  caveat: "MIT licensed, active, requires Python 3.10+; useful reference for deterministic classification"

- url: "https://www.belastaar.nl"
  name: "Belastbaar MCP Server (hosted tax knowledge and rate lookups)"
  trust: medium
  used_for: "Tax rates, brackets, and knowledge guides for 2024-2025; provides tax_rate, search_knowledge tools"
  cited_by: ["note2"]
  caveat: "2026 data not yet available; closed-source hosting limits verification; structured but not independently audited"

- url: "https://1truth.nl"
  name: "1Truth.nl (RGS Referentie Grootboekschema / Dutch chart of accounts standard)"
  trust: high
  used_for: "Canonical chart-of-accounts taxonomy used by Belastingdienst and CBS for normalization"
  cited_by: ["note3"]
  caveat: "Essential for ledger mapping and filing compatibility; use for account code standardization"

- url: "https://blog.kilo.ai/p/how-a-founder-replaced-accountant-with-kiloclaw"
  name: "KiloClaw Mr. Bookkeeper writeup (anecdotal case study)"
  trust: medium
  used_for: "Proof-of-concept for AI-assisted Dutch bookkeeping; demonstrates expense categorization and 30% ruling edge-case detection"
  cited_by: ["note2"]
  caveat: "Single-user anecdotal result; not independently verifiable; saved €420/month through proactive diligence"

- url: "https://forbesjapan.com/articles/detail/95382"
  name: "Claude Code Sub-Agent Pattern (Japanese accounting, 60 companies in 30–50 minutes)"
  trust: medium-high
  used_for: "Real-world licensed tax accountant (zeirishi) demonstrating two-stage classification (deterministic + LLM fallback)"
  cited_by: ["note2"]
  caveat: "Japanese context, not Dutch; but pattern highly relevant; published by licensed professional"

- url: "https://github.com/Sikerdebaard/income-tax-optimizer"
  name: "Dutch Income Tax Optimizer (Python script for Box 1 and Box 3 optimization)"
  trust: medium
  used_for: "Reference for gradient-descent optimization patterns; demonstrates algorithmic multi-variable bracket tuning"
  cited_by: ["note3"]
  caveat: "Requires annual parameter updates for bracket changes; local minima risk; not integrated to ledger"

- url: "https://github.com/picqer/moneybird-php-client"
  name: "picqer/moneybird-php-client (PHP SDK for Moneybird, mature status)"
  trust: high
  used_for: "Production-grade PHP connector for Moneybird API with read+write access"
  cited_by: ["deep-report#L48"]
  caveat: "Last release Apr 14 2025; well-maintained; mature status"

- url: "https://github.com/picqer/exact-php-client"
  name: "picqer/exact-php-client (PHP SDK for Exact Online)"
  trust: high
  used_for: "Production-grade PHP connector for Exact Online with read+write access"
  cited_by: ["deep-report#L49"]
  caveat: "Last release Dec 19 2025; mature status; widely used"

- url: "https://github.com/php-twinfield/twinfield"
  name: "php-twinfield/twinfield (PHP SOAP client for Twinfield)"
  trust: high
  used_for: "Enterprise bookkeeping connector; mature SOAP client for Twinfield integration"
  cited_by: ["deep-report#L50"]
  caveat: "Last release Jan 5 2026; enterprise-grade but SOAP-heavy integration style"

- url: "https://github.com/ossobv/exactonline"
  name: "ossobv/exactonline (Python/LGPL Exact Online REST client)"
  trust: medium-high
  used_for: "Open-source Python alternative for Exact Online; mostly read with some adapters"
  cited_by: ["deep-report#L51"]
  caveat: "Community-maintained; not official Exact support"

- url: "https://github.com/onetoweb/eboekhouden"
  name: "onetoweb/eboekhouden (PHP e-Boekhouden API client)"
  trust: medium
  used_for: "Community PHP client for e-Boekhouden integration"
  cited_by: ["deep-report"]
  caveat: "Community-maintained; check currency vs e-Boekhouden API changes"

- url: "https://speedy-eboekhouden.vercel.app/"
  name: "Speedy e-Boekhouden (TypeScript/self-hosted OCR overlay)"
  trust: medium
  used_for: "Reference for receipt OCR, refund matching, hours tracking patterns for e-Boekhouden users"
  cited_by: ["note1", "deep-report"]
  caveat: "v1.3.1 released Apr 8 2026; young, labels self 'use at own risk'; medium for architecture, low-medium for maturity"

- url: "https://github.com/openaccountants/openaccountants/tree/main/packages/netherlands"
  name: "OpenAccountants Netherlands package repository"
  trust: medium
  used_for: "Skill files for Dutch tax classification, VAT, ZZP deductions, conservative defaults"
  cited_by: ["note2#L23"]
  caveat: "Actively maintained (last commit Apr 2026); 371 tax skills across 134 countries; 41 stars"

- url: "https://devpost.com/software/flowstate-xmv09t"
  name: "FlowState (hackathon Dutch ZZP tax project with bunq + OpenClaw)"
  trust: low-medium
  used_for: "Proof-of-concept for multi-agent transaction matching against Dutch tax rules"
  cited_by: ["note2#L131-133"]
  caveat: "Hackathon project only; not production-proven"

- url: "https://github.com/Lovely-mcinerney/claude-md-docs"
  name: "Claude Skills Architecture (AGENTS.md and SKILL.md modularity pattern)"
  trust: high
  used_for: "Reference for modular instruction structure and LLM hallucination prevention via compartmentalized skills"
  cited_by: ["note3"]
  caveat: "General architecture pattern; not Dutch-specific"

- url: "https://www.xtroverso.nl"
  name: "XTROVERSO Dutch Year-End Tax Risk Checklist (professional accounting firm)"
  trust: medium-high
  used_for: "Professional-grade procedural checklist for ZZP and DGA structures; WKR, mixed-use, iXBRL filing"
  cited_by: ["note3#L101-115"]
  caveat: "Sourced from specialized Dutch business clinic; prevents standard Belastingdienst corrections"

---

## model-risk

- claim: "Most critical failure mode: arithmetic hallucination and misapplication of multi-step tax formulas"
  sources:
    - "note3#C8550-8750"
  confidence: high
  contradictions: none
  mitigation: "Never allow LLM to perform final calculations; use deterministic Python/YAML for all numeric operations; all formulas must be versioned and tested"

- claim: "LLM may hallucinate vendor intent if description vague"
  sources:
    - "note3#C24950-25100"
  confidence: medium
  contradictions: none
  mitigation: "Require explicit matching to historical vendors or merchant categories; flag uncertain classifications as needs_user_input; never post to ledger without confidence > threshold"

- claim: "LLM may attempt to deduct restaurant VAT if specific exclusion rule not aggressively weighted in prompt"
  sources:
    - "note3#C25050-25250"
  confidence: medium
  contradictions: none
  mitigation: "Aggressively weight restaurant/food on-premises VAT non-deductibility in prompt; classify under representatiekosten only; flag as review item if LLM suggests input-VAT recovery"

- claim: "OpenAccountants Netherlands skill is explicitly Medium-low reliability; Q3 / AI-drafted / not independently verified"
  sources:
    - "note1#L23, L452"
  confidence: high
  contradictions: none
  mitigation: "Use OpenAccountants structure only; replace all numeric values with official 2026 Belastingdienst sources; do not trust training data values"

- claim: "Project warns about hallucination, changing law, uneven coverage"
  sources:
    - "note1#L23"
  confidence: high
  contradictions: none
  mitigation: "Implement RAG with Belastingdienst official sources; maintain rule-versioning with source hashes; never hardcode rates"

- claim: "Speedy e-Boekhouden is explicitly young, v1.3.1 released Apr. 8, 2026, labels self use at own risk"
  sources:
    - "note1#L33"
  confidence: high
  contradictions: none
  mitigation: "Use as reference architecture only; do not rely on production maturity; test all OCR and classification outputs"

- claim: "Confidence thresholds and human escalation required for edge cases"
  sources:
    - "note1#L158"
  confidence: high
  contradictions: none
  mitigation: "Define confidence levels: high (auto-post), medium (draft, user review), low (escalate to accountant); never auto-post medium/low confidence items"

---

## data-residency

- claim: "Minimise LLM context; send only fields needed"
  sources:
    - "note3#C484"
  confidence: high
  contradictions: none
  mitigation: "Filter document payloads before LLM processing; exclude sensitive PII/financial details not needed for classification task"

- claim: "Keep original evidence in separate encrypted store"
  sources:
    - "note3#C485"
  confidence: high
  contradictions: none
  mitigation: "Maintain separate encrypted vault for original receipts, invoices, bank statements; use cryptographic hashes for LLM context"

- claim: "Maintain per-object provenance and role-based access"
  sources:
    - "note3#C486"
  confidence: high
  contradictions: none
  mitigation: "Log all access to sensitive documents; implement role-based permissions (user, accountant, admin); track who viewed/modified what"

- claim: "Prefer EU storage and processors for documents and audit artefacts"
  sources:
    - "note3#C487"
  confidence: high
  contradictions: none
  mitigation: "Store evidence in EU infrastructure; process audit artefacts in EU data centers; flag cross-border processing with explicit user consent"

- claim: "Log every user-visible explanation and system-side writeback proposal"
  sources:
    - "note3#C488"
  confidence: high
  contradictions: none
  mitigation: "Maintain immutable audit log of all LLM outputs; capture timestamp, model version, prompt, context, output; retention 7 years minimum"

---

## audit-readiness

- claim: "Every deterministic calculation should emit: calc_id, module, rule_ids, source_urls, input_snapshot, input_evidence_ids, intermediate_steps[], output_values, rounding_policy, generated_at, engine_version"
  sources:
    - "note3#C236"
  confidence: high
  contradictions: none
  mitigation: "Implement structured calculation envelope for all tax engine outputs; make reproducible from input + rule version"

- claim: "Calculation trace format is critical for audit defense and reproducibility"
  sources:
    - "note3#C236"
  confidence: high
  contradictions: none
  mitigation: "Version and test all calculation modules independently; maintain regression tests; export traces in JSON for accountant review"

- claim: "Every agent conclusion should include: evidence_ids, rule_ids, calculation_ids if applicable, confidence, risk_level, reviewer_required"
  sources:
    - "note3#C310"
  confidence: high
  contradictions: none
  mitigation: "Wrap all agent outputs in mandatory envelope; require evidence IDs and rule citations; block outputs without proper linkage"

- claim: "Strict evidentiary continuity required: cryptographic/database linkage between receipt, transaction, and applied tax rule"
  sources:
    - "note3#C14000-14250"
  confidence: high
  contradictions: none
  mitigation: "Implement evidence graph with document hashes, transaction IDs, rule references; ensure every finding points to source evidence"

- claim: "Proper year-end review per XTROVERSO framework prevents standard Belastingdienst corrections and mitigates fines"
  sources:
    - "note3#C7400-7550"
  confidence: high
  contradictions: none
  mitigation: "Use XTROVERSO checklist as baseline; implement year-end close review with accountant sign-off; capture review decisions in audit log"

- claim: "Export XAF 4.0 and accountant workpapers"
  sources:
    - "note3#C491"
  confidence: high
  contradictions: none
  mitigation: "Support XAF 4.0 export format; generate accountant workpapers with evidence IDs and calculation traces"

- claim: "Include evidence IDs and source URLs on findings"
  sources:
    - "note3#C492"
  confidence: high
  contradictions: none
  mitigation: "Every finding must cite evidence document and rule source; include URLs with version dates"

- claim: "Keep immutable snapshots of rule versions used for each period"
  sources:
    - "note3#C493"
  confidence: high
  contradictions: none
  mitigation: "Capture rule snapshots at period start; maintain git-style versioning; never silently mutate rules in production"

- claim: "Preserve human review record for high-risk issues"
  sources:
    - "note3#C494"
  confidence: high
  contradictions: none
  mitigation: "Log all accountant/user approvals with timestamp, reviewer ID, decision rationale; retain 7 years"

---

## contradictions

- note1 states "2026 zelfstandigenaftrek is €1,200" (L178)
- note2 states "2025 zelfstandigenaftrek is €2,470" (L26)
- note3 states "2026 zelfstandigenaftrek is €1,200" (C14900-15050)
- **Resolution**: note2 cites 2025 rates; note1 and note3 cite 2026 rates. Use 2026 value €1,200 for current year.

- note1 states "2026 excess-borrowing threshold €500,000" (L188)
- note2 states "2025 excess-borrowing threshold €700,000" (L320)
- **Resolution**: threshold changed from €700,000 in 2023 to €500,000 in 2026. Use €500,000 for 2026.

---

## summary-statistics

- **subtopic count**: 6 (compliance, liability, source-table, model-risk, data-residency, audit-readiness)
- **fact count**: 47 deduplicated facts across compliance/liability/model-risk/data-residency/audit-readiness
- **source-table entries**: 25+ official and community sources with trust levels assigned
- **contradictions found**: 2 (zelfstandigenaftrek 2025 vs 2026; excess-borrowing threshold change)
- **notable patterns**:
  - Belastingdienst and RVO sources universally HIGH trust
  - OpenAccountants and community projects MEDIUM trust; use for structure/patterns only, not numeric values
  - LLM hallucination on arithmetic is critical risk; all calculations must be deterministic
  - 7-year retention and audit-readiness mandatory by law
  - DGA/structure/filing decisions must remain human-led with accountant sign-off
