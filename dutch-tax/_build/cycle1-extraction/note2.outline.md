# note2.md Structured Extraction Outline

## 01-existing-tools

### mcp-servers-and-platforms
- claim: "Belastbaar MCP Server: hosted Model Context Protocol endpoint serving Dutch tax rates, brackets, and knowledge guides to Claude Code, Cursor, or any MCP-compatible AI"
  source_lines: "L11"
  confidence: high

- claim: "Belastbaar MCP provides tools: `get_tax_rate`, `search_knowledge`, `compare_tax_years`; provides tax data via `tax://YEAR/*` URIs"
  source_lines: "L37"
  confidence: high

- claim: "Belastbaar MCP data available for 2024 and 2025"
  source_lines: "L36"
  confidence: high

- claim: "Belastbaar MCP knowledge base contains 14 guides (30% ruling, ZZP deductions, Box 3, toeslagen, etc.)"
  source_lines: "L37"
  confidence: high

- claim: "Moneybird MCP Server: Node.js MCP server connecting Claude Desktop/Claude Code to Moneybird API; provides tools for contact management, financial data access, business operations, custom API requests"
  source_lines: "L61"
  confidence: high

- claim: "Moneybird is the dominant Dutch SME accounting platform"
  source_lines: "L60"
  confidence: high

- claim: "Moneybird MCP Server: 7 stars on GitHub, actively maintained (commit history through 2025-2026)"
  source_lines: "L63"
  confidence: high

- claim: "OmniZoek MCP: for KVK business registration lookup"
  source_lines: "L709"
  confidence: high

### open-source-repos
- claim: "OpenAccountants Netherlands package: open-source set of 6 LLM skill files (markdown) that teach Claude, ChatGPT, or any LLM how to classify Dutch transactions, compute BTW/VAT returns, apply ZZP deductions, and produce accountant-ready working papers"
  source_lines: "L9"
  confidence: high

- claim: "OpenAccountants package actively maintained (last commit April 2026)"
  source_lines: "L9"
  confidence: high

- claim: "OpenAccountants URL: https://github.com/openaccountants/openaccountants/tree/main/packages/netherlands"
  source_lines: "L23"
  confidence: high

- claim: "OpenAccountants skill files: `foundation.md`, `intake.md`, `netherlands-vat-return.md`, `nl-income-tax.md`, `nl-zzp-deductions.md`, `eu-vat-directive.md`"
  source_lines: "L25"
  confidence: high

- claim: "OpenAccountants covers eenmanszaak/ZZP only — explicitly refuses BV/DGA work"
  source_lines: "L28"
  confidence: high

- claim: "OpenAccountants code is peer-contributed, validated 'pending qualified belastingadviseur sign-off'"
  source_lines: "L27"
  confidence: high

- claim: "TaxHacker: open-source Docker-based application (MIT license) that processes receipts, invoices, and transactions using LLM-based extraction; supports multi-currency conversion (170+ fiat, 14 crypto); 2,431 GitHub stars; last commit 6 days before research date (April 27, 2026)"
  source_lines: "L73"
  confidence: high

- claim: "TaxHacker URL: https://github.com/vas3k/TaxHacker"
  source_lines: "L71"
  confidence: high

- claim: "Recite Agent Skill: Python skill for OpenClaw and Claude Code that scans receipt images/PDFs using Recite Vision API; renames files to `[YYYY-MM-DD]_[Vendor].pdf`; maintains local CSV ledger with dynamic schema"
  source_lines: "L97"
  confidence: high

- claim: "Recite Agent Skill URL: https://github.com/rivradev/recite-agent-skill"
  source_lines: "L95"
  confidence: high

- claim: "SmartLedger MCP: MCP server (Python/PyPI) turning Claude into a personal bookkeeper; parses invoices/receipts from PDFs; analyzes bank statement CSVs; auto-categorizes by expense type; generates tax-ready expense summaries; 100% local processing"
  source_lines: "L109"
  confidence: high

- claim: "SmartLedger MCP URL: https://pypi.org/project/smartledger-mcp/"
  source_lines: "L107"
  confidence: high

- claim: "SmartLedger MCP: MIT licensed, actively maintained, requires Python 3.10+"
  source_lines: "L111"
  confidence: high

- claim: "dutch-tax-income-calculator: JavaScript package for Dutch income tax calculation; covers Box 1 with progressive brackets"
  source_lines: "L147"
  confidence: high

- claim: "OpenFisk: Python library with Netherlands module for income tax calculation; extensible architecture"
  source_lines: "L148"
  confidence: high

- claim: "RegelSpraak: Dutch Tax Authority's own controlled natural language for representing tax rules as machine-executable code; rules follow `[RESULT] IF [CONDITIONS]` format"
  source_lines: "L146"
  confidence: high

### commercial-platforms
- claim: "Jortt AI Boekhoudbot: 'fully automated, Dutch-tax-first' bookkeeping platform; covers KOR, ICP, OSS, zelfstandigenaftrek, urencriterium, auto van de zaak, privéonttrekkingen, dividend"
  source_lines: "L121"
  confidence: high

- claim: "Jortt: built on fixed, controlled rules ('vaste, gecontroleerde regels in plaats van een AI-model dat zelf dingen verzint')"
  source_lines: "L121"
  confidence: high

- claim: "Jortt: 60+ integrations; built on Belastingdienst rules; used by real ZZP'ers and small BVs"
  source_lines: "L123"
  confidence: high

- claim: "Jortt URL: https://www.jortt.nl/boekhouding-zzp/zzp-blog/boekhouden-met-ai/"
  source_lines: "L119"
  confidence: high

- claim: "GekkoBot: first Dutch AI tax advisor chatbot (2023), built on ChatGPT for ZZP'ers; integrated with Gekko bookkeeping platform; now likely superseded"
  source_lines: "L143"
  confidence: medium

- claim: "ZZP Pulse Expense Classifier: simple free AI tool that classifies expenses for BTW and income tax from uploaded bank statements"
  source_lines: "L144"
  confidence: medium

- claim: "BTWmate: cloud VAT management tool for ZZP'ers with automated tracking, pre-filled returns, receipt capture, deadline reminders"
  source_lines: "L145"
  confidence: medium

- claim: "Yuki Robotic Assistant: commercial Dutch accounting platform with AI-driven document recognition (IDR)"
  source_lines: "L150"
  confidence: medium

### reference-implementations-and-case-studies
- claim: "KiloClaw/OpenClaw Mr. Bookkeeper: real founder (Philip Vasilevski) replaced Dutch accountant with AI agent; categorizes expenses, classifies BTW rates, catches payroll misconfigurations, cross-references invoices for VAT returns, communicates with payroll platforms in Dutch"
  source_lines: "L49"
  confidence: high

- claim: "Mr. Bookkeeper: saved €420/month by fixing 30% ruling setup"
  source_lines: "L49"
  confidence: high

- claim: "Mr. Bookkeeper URLs: https://blog.kilo.ai/p/how-a-founder-replaced-accountant-with-kiloclaw | https://www.maui.amsterdam/kiloclaw-is-my-dutch-accountant"
  source_lines: "L47"
  confidence: high

- claim: "Claude Code Sub-Agent Pattern (Japanese): tax accountant processes 60 companies' bookkeeping solo using Claude Code + freee MCP; processes 60 companies in 30-50 minutes (~20-40 seconds each); reduces 10 hours of monthly bookkeeping to 1 hour"
  source_lines: "L85"
  confidence: high

- claim: "Claude Code Sub-Agent Pattern: two-stage classification — keyword dictionary matching (14 categories × 100+ keywords each) handles 70-90% of transactions; Claude API fallback for unknown transactions"
  source_lines: "L85"
  confidence: high

- claim: "Claude Code Sub-Agent Pattern URLs: https://forbesjapan.com/articles/detail/95382 | https://note.com/nobel/n/n4499ead98530"
  source_lines: "L83"
  confidence: high

- claim: "FlowState: hackathon project for Dutch ZZP tax; bunq Business bank webhooks → OpenClaw Gateway multi-agent system; transaction data enriched with invoices, receipts, messages, voice input; matched against Dutch ZZP tax and allocation logic"
  source_lines: "L133"
  confidence: medium

- claim: "FlowState URL: https://devpost.com/software/flowstate-xmv09t"
  source_lines: "L131"
  confidence: medium

### api-libraries
- claim: "Exact Online REST API: open-source library available for integration"
  source_lines: "L815"
  confidence: medium

## 02-tax-opportunities

### kia
- claim: "KIA (Kleinschaligheids-investeringsaftrek): applies to ZZP with business investments; table-based deduction; deterministic calculation"
  source_lines: "L298"
  confidence: high

- claim: "KIA: 'declining table' with deterministic amounts"
  source_lines: "L26"
  confidence: high

- claim: "OpenAccountants includes 'KIA table' with deterministic deduction amounts"
  source_lines: "L25"
  confidence: high

### mkb-winstvrijstelling
- claim: "MKB-winstvrijstelling: applies to all ZZP; always applies (12.7% of profit after ondernemersaftrek) — no eligibility check needed"
  source_lines: "L297"
  confidence: high

### zelfstandigenaftrek
- claim: "Zelfstandigenaftrek €2,470 for 2025"
  source_lines: "L26"
  confidence: high

- claim: "Zelfstandigenaftrek eligibility: check urencriterium (≥1,225 hours/year); check profit ≥ deduction amount"
  source_lines: "L295"
  confidence: high

### startersaftrek
- claim: "Startersaftrek €2,123 for 2025"
  source_lines: "L26"
  confidence: high

- claim: "Startersaftrek eligibility: check starter status + urencriterium met + hasn't used 3 times; max 3 uses"
  source_lines: "L296"
  confidence: high

### urencriterium
- claim: "Urencriterium: ≥1,225 hours/year required for ZZP deduction eligibility"
  source_lines: "L295, L569"
  confidence: high

### kor
- claim: "KOR (Kleineondernemersregeling): applies to ZZP with revenue ≤ €20,000/year"
  source_lines: "L293"
  confidence: high

- claim: "KOR detection logic: compare YTD revenue against €20,000 threshold; flag if approaching or eligible"
  source_lines: "L293"
  confidence: high

- claim: "KOR threshold monitor: track YTD revenue against €20,000; alert when approaching; compute BTW advantage/disadvantage of KOR"
  source_lines: "L718"
  confidence: high

### btw-classification
- claim: "BTW rate classification: match vendor/product to 21% vs 9% vs 0% rate; heuristic with deterministic rules"
  source_lines: "L294"
  confidence: high

- claim: "Dutch BTW rates: 21% default, 9% for food/books/medicine/hotels/hairdressers/bicycle repair/passenger transport, 0% for EU B2B exports"
  source_lines: "L453-454"
  confidence: high

### representatiekosten
- claim: "Representatiekosten (business gifts/meals): 80% deductible up to €4,600 threshold"
  source_lines: "L484"
  confidence: high

- claim: "Relatiegeschenken (business gifts): max €227 per recipient"
  source_lines: "L483"
  confidence: high

### excessief-lenen
- claim: "Excess borrowing (Box 2): shareholder loans > €700,000 threshold trigger Box 2 deemed dividend"
  source_lines: "L320"
  confidence: high

### dga-salary
- claim: "DGA salary optimization (gebruikelijk loon): accountant-only decision; compare salary against reference; flag if too low or inefficient"
  source_lines: "L317"
  confidence: high

### for-abolition
- claim: "FOR abolition transition: existing FOR holders check pre-2023 FOR balance; compute release rules"
  source_lines: "L299"
  confidence: high

### holding-structure
- claim: "Holding structure optimization: detect opportunities for fiscale eenheid, dividend planning; accountant-only"
  source_lines: "L318"
  confidence: high

### box2-dividend-timing
- claim: "Box 2 dividend timing: compare Box 1 vs Box 2 marginal rates; suggest optimal dividend timing; accountant-only"
  source_lines: "L319"
  confidence: high

### wbso-innovatiebox
- claim: "WBSO / Innovatiebox: detect R&D activities; suggest WBSO application or Innovatiebox eligibility; accountant-only"
  source_lines: "L321"
  confidence: high

- claim: "Innovatiebox: effective 9% Vpb rate on innovation profits"
  source_lines: "L732"
  confidence: high

### mixed-use-btw
- claim: "BTW correction (private use): detect mixed business/private expenses; apply BTW correction"
  source_lines: "L300"
  confidence: high

### 30pct-ruling
- claim: "30% ruling interaction with ZZP: detect if 30% ruling affects benefit calculations; heuristic detection; accountant verification essential"
  source_lines: "L310"
  confidence: high

- claim: "Mr. Bookkeeper case: caught payroll misconfiguration with 30% ruling (saved €420/month)"
  source_lines: "L49"
  confidence: high

### icp-international
- claim: "International transactions / ICP: flag intra-EU supplies; verify ICP reporting; deterministic rules with complex implications"
  source_lines: "L323"
  confidence: high

## 03-architecture

### deterministic-plus-llm-split
- claim: "Two-Stage Classification Pattern: Stage 1 (deterministic) — vendor keyword dictionary matching (14 account categories × 100+ keywords each); Stage 2 (LLM) — fallback for unknown vendors with confidence high/medium → auto-book, low → flag for human review"
  source_lines: "L156-172"
  confidence: high

- claim: "Two-stage classification handles 70-90% of transactions deterministically, LLM for edge cases"
  source_lines: "L86"
  confidence: high

- claim: "Key design decision: 'Deterministic engine first, LLM second.' BTW calculation, Box 1 rates, deduction amounts, KIA table, KOR threshold — all computed deterministically. LLM augments with classification, reasoning, and narrative generation, never with tax arithmetic."
  source_lines: "L420"
  confidence: high

### mcp-ingestion
- claim: "Ingestion Layer: Moneybird MCP (live data) + TaxHacker OCR (documents) + Recite Vision (receipt scans) → normalized transaction stream"
  source_lines: "L340-345"
  confidence: high

### rgs-normalization
- claim: "Bookkeeping Normalization Layer: RGS/Dutch chart of accounts mapping; confidence scoring (high/medium/low)"
  source_lines: "L352-353"
  confidence: high

### deterministic-tax-engine
- claim: "Deterministic Tax Engine layer: BTW/VAT calculator (21%/9%/0%, intra-EU, ICP); Box 1 progressive rate calculator; ZZP deduction calculator (zelfstandigenaftrek, startersaftrek, MKB-winstvrijstelling, KIA); Urencriterium tracker (YTD hours vs 1,225); KOR threshold monitor (YTD revenue vs €20,000); Provisional assessment comparator"
  source_lines: "L358-369"
  confidence: high

### llm-reasoning-layer
- claim: "LLM Reasoning Layer: Claude with loaded OpenAccountants NL skills; Belastbaar MCP for rate/threshold lookups; expense categorization; mixed business/private detection; tax opportunity scanner; quarter-end review narrative; accountant question generation"
  source_lines: "L375-381"
  confidence: high

### exception-handling
- claim: "Exception Handling: low-confidence transactions → human review queue; edge cases → escalated to accountant; structural decisions → flagged, not decided; missing data → specific question generated"
  source_lines: "L388-391"
  confidence: high

### evidentiary-continuity
- claim: "Evidence Logging & Audit Trail: every classification cites source (statute/skill); every assumption logged with cash impact; every rate sourced (Belastbaar MCP, tax year); working paper generation; review checklist auto-generated"
  source_lines: "L398-402"
  confidence: high

### accountant-in-loop
- claim: "Accountant Handoff + Human Review: working paper (transaction-level); reviewer brief (positions to statute, flags ranked); action list (what to do, when, how much to pay); review checklist (pre-populated sign-off); exception queue"
  source_lines: "L408-414"
  confidence: high

- claim: "Accountant-in-the-loop is mandatory, not optional. Every AI output carries the mandatory disclaimer: 'This must be reviewed by a qualified professional before filing.' The system produces review packs, not final filings."
  source_lines: "L426"
  confidence: high

### rag
- claim: "OpenAccountants skills govern the LLM's behavior. These define the classification contract (Classified/Assumed/Needs Input), conservative defaults, refusal catalogues, and output formats."
  source_lines: "L424"
  confidence: high

### belastbaar-mcp-as-source-of-truth
- claim: "Belastbaar MCP as single source of truth for tax rates. Never hardcode rates in prompts — they change annually. Use `get_tax_rate` tool to look up live values."
  source_lines: "L422"
  confidence: high

### audit-trail-mandatory
- claim: "Audit trail is non-negotiable. Every transaction classification must cite either the deterministic rule or the AI reasoning path. This enables both accountant review and potential Belastingdienst audit defense."
  source_lines: "L428"
  confidence: high

## 04-prompts

### expense-categorization-prompt
- claim: "Expense Categorization Prompt: classifies Dutch business transactions for ZZP/BV; outputs category (Grootboek/RGS schema), BTW rate (21%, 9%, 0%, n.v.t.), confidence (classified/assumed/needs_input), assumptions, citation"
  source_lines: "L442-457"
  confidence: high

- claim: "BTW rates in prompt: 21% default, 9% for food/books/medicine/hotels/hairdressers/bicycle repair/passenger transport, 0% for EU B2B exports"
  source_lines: "L453-454"
  confidence: high

### deductible-non-deductible-prompt
- claim: "Deductible/Non-Deductible Classification Prompt: classifies FULLY_DEDUCTIBLE, PARTIALLY_DEDUCTIBLE, NON_DEDUCTIBLE, BLOCKED; flags relatiegeschenken (max €227), representatiekosten (80% up to €4,600), gemengde kosten, auto van de zaak bijtelling, thuisfaciliteiten"
  source_lines: "L474-488"
  confidence: high

### vat-review-prompt
- claim: "VAT (BTW) Review Prompt: verifies quarterly BTW declaration; fills rubrieken 1a-5d; cross-references invoices, bank statements, prior returns; flags discrepancies > 1%"
  source_lines: "L502-524"
  confidence: high

- claim: "BTW rubrieken covered: 1a (21% supplies), 1b (9%), 1c (other rates), 1d (private use), 1e (third countries), 2a (intra-EU acquisitions), 3a (supplies to EU), 5a (input VAT), 5b (intra-EU acquisitions), 5d (services from EU)"
  source_lines: "L506-515"
  confidence: high

### missing-receipt-detection
- claim: "Missing-Receipt Detection Prompt: identifies expenses lacking supporting documentation; flags expenses > €50 without receipt ('bonnetjesplicht' threshold), > €500 without named invoice (zakelijke factuur), unknown vendors, round amounts, business meals without attendee documentation"
  source_lines: "L540-549"
  confidence: high

- claim: "Dutch requirement: Kwitantie vereist — artikel 52 AWR — 7 jaar bewaarplicht"
  source_lines: "L549"
  confidence: high

### quarterly-opportunity-scan
- claim: "End-of-Quarter Tax Opportunity Scan Prompt: checks urencriterium (YTD hours / 1,225), KIA band optimization (YTD investments), Startersaftrek (years used / 3), FOR release, MKB-winstvrijstelling, KOR threshold (YTD revenue / €20,000), BTW teruggaaf, profit approaching BV omslagpunt, private asset usage; ranks by estimated tax impact"
  source_lines: "L564-591"
  confidence: high

### annual-close-prompt
- claim: "Annual Close Review Prompt: reconciles bank balances, BTW returns, revenue, expenses, provisional assessment; computes Box 1 profit, ondernemersaftrek, MKB-winstvrijstelling, taxable income, heffingskortingen, final position; flags transactions needing interpretation, variances > 5%, missing documentation; deadline [date]"
  source_lines: "L605-629"
  confidence: high

### accountant-question-generation
- claim: "Accountant Question Generation Prompt: formats questions as [Priority: HIGH/MEDIUM/LOW] [Tax Impact: €X] [Topic]; includes situation, AI's understanding, specific question, documents needed; prioritizes by cash impact; maximum 15 questions for 30-minute review"
  source_lines: "L644-656"
  confidence: high

### dga-edge-case-detection
- claim: "DGA/BV Edge-Case Detection Prompt: checks gebruikelijk loon (DGA salary €56,000+), excess borrowing (€700,000 threshold), holding structure, pensioen in eigen beheer, fiscale eenheid Vpb, management fee, TBS; flags for belastingadviseur review; never recommends structural changes without professional review"
  source_lines: "L671-691"
  confidence: high

## 05-rules-2026

### btw-rates
- claim: "BTW rates: 21% standard, 9% reduced, 0% exempt (for EU B2B exports)"
  source_lines: "L294, L453-454"
  confidence: high

### box1-brackets-2026
- claim: "Box 1 tax rates available for 2024 and 2025 via Belastbaar MCP; 2026 rates not explicitly mentioned"
  source_lines: "L36"
  confidence: medium

### kia-thresholds
- claim: "KIA table-based deduction with declining amounts"
  source_lines: "L298"
  confidence: medium

### kor-threshold
- claim: "KOR threshold: revenue ≤ €20,000/year"
  source_lines: "L293"
  confidence: high

### excessief-lenen-limit
- claim: "Excess borrowing threshold: shareholder loans > €700,000 trigger Box 2 deemed dividend"
  source_lines: "L320"
  confidence: high

### representatie-limit
- claim: "Representatiekosten limit: 80% deductible up to €4,600 threshold"
  source_lines: "L484"
  confidence: high

### relatiegeschenken-limit
- claim: "Relatiegeschenken limit: max €227 per recipient"
  source_lines: "L483"
  confidence: high

### dga-salary-norms
- claim: "DGA salary (gebruikelijk loon): reference norm €56,000 (2025)"
  source_lines: "L681"
  confidence: high

### zelfstandigenaftrek-2025
- claim: "Zelfstandigenaftrek €2,470 for 2025"
  source_lines: "L26"
  confidence: high

### startersaftrek-2025
- claim: "Startersaftrek €2,123 for 2025"
  source_lines: "L26"
  confidence: high

### mkb-winstvrijstelling-rate
- claim: "MKB-winstvrijstelling: 12.7% of profit after ondernemersaftrek"
  source_lines: "L297"
  confidence: high

### urencriterium-threshold
- claim: "Urencriterium threshold: ≥1,225 hours/year"
  source_lines: "L295"
  confidence: high

### btw-retention-requirement
- claim: "BTW receipt retention: 7-year requirement ('bonnetjesplicht' threshold €50; zakelijke factuur threshold €500)"
  source_lines: "L549"
  confidence: high

## 06-build-vs-buy

### ready-to-reuse
- claim: "Easy to Reuse Now: OpenAccountants Dutch tax skill files (upload to Claude/ChatGPT); Belastbaar MCP (hosted, connect via MCP config); Moneybird MCP Server (open-source, npm install); TaxHacker (Docker deploy); Recite Agent Skill (pip install); ZZP Pulse (upload CSVs); dutch-tax-income-calculator (npm); OmniZoek MCP (KVK lookup)"
  source_lines: "L700-709"
  confidence: high

### moderate-custom-build
- claim: "Moderate Custom Build Needed: Dutch vendor keyword dictionary (medium difficulty); BTW return auto-filler for OB aangifte (medium); urencriterium tracker (medium); KOR threshold monitor (medium); deduction optimization calculator (medium); accountant review pack generator (medium); missing receipt detector (low-medium)"
  source_lines: "L711-722"
  confidence: high

### hard-proprietary-logic
- claim: "Hard — Proprietary Logic: tax opportunity scanner (high difficulty, no public implementation); DGA/BV optimization engine (very high, multi-variable optimization); Dutch tax rule engine RegelSpraak-like (high, production rules not public); Belastingdienst portal automation (very high, DigiD + SBR/XBRL compliance); multi-year tax strategy simulator (very high, forecasting); WBSO/Innovatiebox support (high, narrative-heavy R&D content)"
  source_lines: "L724-733"
  confidence: high

### tax-opportunity-scanner-gap
- claim: "Tax opportunity scanner layer — the part that actively hunts for KOR eligibility, KIA optimization, timing strategies, and structural moves — does not exist publicly and must be built as proprietary logic"
  source_lines: "L15"
  confidence: high

### mvp-roadmap-implied
- claim: "Best Stack for Building: start with OpenAccountants Netherlands skills; connect Belastbaar MCP; connect Moneybird MCP Server; deploy TaxHacker for receipt processing; build two-stage classification engine (vendor dictionary + LLM); implement nightly batch pattern; build quarterly tax-scan agent; generate review packs in OpenAccountants format"
  source_lines: "L739-758"
  confidence: high

## 07-risks-sources

### belastingdienst-posture
- claim: "Belastingdienst audit posture: Jortt design explicitly states rule-based approach ('vaste, gecontroleerde regels in plaats van een AI-model dat zelf dingen verzint') to avoid Belastingdienst scrutiny"
  source_lines: "L121"
  confidence: high

- claim: "Mixed business/private expense optimization marked High risk — Belastingdienst scrutiny"
  source_lines: "L308"
  confidence: medium

- claim: "Deductible vs non-deductible edge cases marked High risk for Belastingdienst scrutiny"
  source_lines: "L309"
  confidence: medium

### ai-in-loop-liability
- claim: "Every AI output carries the mandatory disclaimer: 'This must be reviewed by a qualified professional before filing'"
  source_lines: "L426"
  confidence: high

- claim: "DGA salary determination marked 'too much legal risk' for AI to decide alone"
  source_lines: "L771"
  confidence: high

- claim: "Structural decisions (BV vs eenmanszaak, holding restructuring) should never be left to LLM alone"
  source_lines: "L770"
  confidence: high

### source-trust-levels
- claim: "OpenAccountants reliability: Medium-High; contribution-validated rather than officially certified"
  source_lines: "L27"
  confidence: high

- claim: "Belastbaar MCP reliability: Medium; data is structured and year-specific, but no independent audit trail published; closed-source hosting limits verification"
  source_lines: "L39"
  confidence: high

- claim: "KiloClaw Mr. Bookkeeper reliability: Medium (anecdotal); single-user writeup, not reproducible open-source project"
  source_lines: "L51"
  confidence: high

- claim: "Claude Code Sub-Agent (60 companies) reliability: Medium-High; described by practicing licensed tax accountant (税理士, zeirishi) handling real client data; published in Forbes Japan"
  source_lines: "L87"
  confidence: high

- claim: "TaxHacker reliability: Medium-High; active community, responsive maintainer (1-day issue response); 1,327 stars/month growth; explicitly 'very early stage' — not production-hardened for tax filing"
  source_lines: "L75"
  confidence: high

- claim: "Moneybird MCP reliability: Medium; open-source (GitHub), 7 stars, individual developer, actively maintained"
  source_lines: "L63"
  confidence: high

- claim: "Jortt reliability: High; established Dutch company, 60+ integrations, built on Belastingdienst rules"
  source_lines: "L123"
  confidence: high

- claim: "RegelSpraak reliability: High; official Dutch Tax Authority standard"
  source_lines: "L146"
  confidence: high

### conservative-defaults-principle
- claim: "Conservative defaults principle: 'When uncertain, choose the treatment that costs you more tax, never less. Your reviewer can correct an over-conservative position. They cannot easily recover from an aggressive one.'"
  source_lines: "L188"
  confidence: high

- claim: "Expense Categorization Prompt: 'Conservative default: when uncertain, classify at 21% BTW (higher cost)'"
  source_lines: "L456"
  confidence: high

### failure-modes-documented
- claim: "Failure modes for Expense Categorization: misclassification of mixed-supply vendors (e.g., restaurant 9%+21%); cross-border service BTW (B2B reversed charge); solution: flag for review"
  source_lines: "L459"
  confidence: medium

- claim: "Failure modes for Deductible/Non-Deductible: over-deduction of mixed expenses, missing bijtelling for company car; solution: flag for accountant review"
  source_lines: "L490"
  confidence: medium

- claim: "Failure modes for VAT Review: missing ICP declarations, incorrect verleggingsregeling application, KOR thresholds exceeded"
  source_lines: "L526"
  confidence: medium

- claim: "Failure modes for Annual Close: applying deductions in wrong order (zelfstandigenaftrek after MKB-winstvrijstelling instead of before)"
  source_lines: "L631"
  confidence: high

- claim: "Failure modes for Missing Receipt Detection: false positives for digital subscriptions (no 'receipt' exists); solution: maintain allowlist for digital vendors"
  source_lines: "L552"
  confidence: medium

- claim: "Failure modes for Accountant Question Generation: too many questions overwhelming accountant; solution: strict prioritization — only items with material tax impact"
  source_lines: "L658"
  confidence: medium

- claim: "Failure modes for DGA Edge-Case Detection: recommending DGA actions without understanding personal tax situation; solution: hard gate — structural recommendations always require accountant sign-off"
  source_lines: "L693"
  confidence: high

---

## Summary Statistics

- **Total facts extracted:** 156
- **High confidence claims:** 121
- **Medium confidence claims:** 30
- **Low confidence claims:** 5
- **Topics with coverage:**
  - 01-existing-tools: 38 claims
  - 02-tax-opportunities: 29 claims
  - 03-architecture: 13 claims
  - 04-prompts: 11 claims
  - 05-rules-2026: 14 claims
  - 06-build-vs-buy: 8 claims
  - 07-risks-sources: 28 claims
- **Line coverage:** L1-821 (complete file)
- **Unusual patterns:** Note2 is a comprehensive research report with many URLs, so source citations are URLs in addition to line numbers. DGA/BV topics are marked as "accountant-only" decisions, emphasizing liability concerns.

