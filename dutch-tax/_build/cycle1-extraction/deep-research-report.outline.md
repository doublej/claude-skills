# Structured Factual Outline: deep-research-report (6).md

## 01-existing-tools

### Moneybird
- id: 01-existing-tools
  subtopic: moneybird
  facts:
    - claim: "Moneybird offers official REST API with webhook events and idempotency keys"
      source_lines: "L17, L40, L62"
      confidence: high
    - claim: "Moneybird has official MCP launch and official CLI help page"
      source_lines: "L17, L40"
      confidence: high
    - claim: "Moneybird is described as the best first Dutch SMB integration surface for an AI copilot"
      source_lines: "L17"
      confidence: high
    - claim: "Moneybird has strong webhooks with retries and idempotency; invoice import/export patterns available"
      source_lines: "L62"
      confidence: high
    - claim: "Moneybird exposes contacts, invoices, accounts, products, projects, time entries, subscriptions"
      source_lines: "L62"
      confidence: high
    - claim: "Moneybird has VAT tax rates and ledger IDs in API flows"
      source_lines: "L62"
      confidence: high
    - claim: "Moneybird is recommended as the best first integration if goal is fast but defensible Dutch MVP"
      source_lines: "L75-76"
      confidence: high

### Jortt
- id: 01-existing-tools
  subtopic: jortt
  facts:
    - claim: "Jortt integrates AI but states bookings follow fixed rules with 99%+ rule-driven certainty"
      source_lines: "L20"
      confidence: medium
    - claim: "Jortt exposes API for bookkeeping operations"
      source_lines: "L20"
      confidence: medium
    - claim: "Jortt Boekhoudbot demonstrates AI is integrated but deterministic-first pattern should dominate"
      source_lines: "L20"
      confidence: medium
    - claim: "Jortt is positioned as reference for deterministic booking policy architecture"
      source_lines: "L20"
      confidence: medium
    - claim: "Jortt explicitly states that bookkeeping should follow fixed hard rules and AI is helpful for advice/explanation"
      source_lines: "L8-9"
      confidence: high

### Other Platforms
- id: 01-existing-tools
  subtopic: other_platforms
  facts:
    - claim: "AFAS Software is a Dutch ERP vendor with REST and SOAP APIs"
      source_lines: "L5"
      confidence: high
    - claim: "Yuki is accounting software available in Netherlands"
      source_lines: "L5"
      confidence: high
    - claim: "Exact Online is an enterprise integration platform available in Netherlands"
      source_lines: "L5"
      confidence: high
    - claim: "e-Boekhouden is Dutch bookkeeping platform with official API and community client"
      source_lines: "L25, L65"
      confidence: high
    - claim: "SnelStart is a Dutch bookkeeping platform with official developer surface"
      source_lines: "L69"
      confidence: high
    - claim: "Twinfield is an enterprise bookkeeping platform with SOAP-heavy integration style"
      source_lines: "L70"
      confidence: high
    - claim: "Rompslomp is a Dutch bookkeeping platform with public API support pages"
      source_lines: "L71"
      confidence: high

### MCP Servers and Open-Source Connectors
- id: 01-existing-tools
  subtopic: mcp_and_open_source
  facts:
    - claim: "moneybird-mcp-server: Node/MIT license, 35 commits visible, public in 2026, provides read+write access"
      source_lines: "L42"
      confidence: high
    - claim: "moneybird-mcp-server exposes contacts, invoices, accounts, products, projects, time entries"
      source_lines: "L42"
      confidence: high
    - claim: "moneybird-mcp-server is positioned as prototype-to-early-production quality"
      source_lines: "L42"
      confidence: medium
    - claim: "exact-online-mcp-server-by-cdata: Java/OSS wrapper around commercial JDBC driver, read-only in OSS wrapper"
      source_lines: "L43"
      confidence: high
    - claim: "OpenAccountants: v1.0.0 released Apr 14 2026, 41 stars, contains 371 tax skills across 134 countries"
      source_lines: "L21, L44"
      confidence: high
    - claim: "OpenAccountants includes EU VAT and reverse-charge skills"
      source_lines: "L21"
      confidence: high
    - claim: "OpenAccountants has AGPL and commercial licensing"
      source_lines: "L44"
      confidence: high
    - claim: "speedy-eboekhouden: TypeScript/self-hosted, updated Apr 23 2026, provides e-Boekhouden overlay with OCR, refund matching, hours"
      source_lines: "L45"
      confidence: high
    - claim: "picqer/moneybird-php-client: PHP client with release Apr 14 2025, read+write access, mature status"
      source_lines: "L48"
      confidence: high
    - claim: "picqer/exact-php-client: PHP client with release Dec 19 2025, read+write access, mature status"
      source_lines: "L49"
      confidence: high
    - claim: "onetoweb/eboekhouden: PHP e-Boekhouden API client"
      source_lines: "L46"
      confidence: high
    - claim: "ossobv/exactonline: Python/LGPL Exact Online REST client, mostly read with some adapters"
      source_lines: "L51"
      confidence: high
    - claim: "php-twinfield/twinfield: PHP Twinfield SOAP client, release Jan 5 2026, read+write, mature status"
      source_lines: "L50"
      confidence: high
    - claim: "TaxHacker: open-source receipt/invoice extraction into structured database"
      source_lines: "L31, L54"
      confidence: high

### Standards and Platforms
- id: 01-existing-tools
  subtopic: standards_and_platforms
  facts:
    - claim: "RGS Taxonomy links chart of accounts to SBR (Dutch accounting standard)"
      source_lines: "L19"
      confidence: high
    - claim: "SBR is the Dutch normalized accounting standard"
      source_lines: "L5, L9"
      confidence: high
    - claim: "Digipoort is the filing transport standard for Netherlands"
      source_lines: "L19"
      confidence: high
    - claim: "XAF 4.0 is the current audit/exchange standard used by Belastingdienst ODB"
      source_lines: "L18, L19"
      confidence: high
    - claim: "RegelSpraak is a Belastingdienst-developed controlled natural language used operationally to specify executable tax rules"
      source_lines: "L22"
      confidence: high
    - claim: "RegelSpraak signals that executable tax-law formalisation is the correct pattern for Dutch tax logic"
      source_lines: "L22"
      confidence: high

### Inventory Summary
- id: 01-existing-tools
  subtopic: ecosystem_pattern
  facts:
    - claim: "Public code is strong on connectors, MCP wrappers, OCR/document extraction and prompt-skill packaging"
      source_lines: "L57"
      confidence: high
    - claim: "Public code is weak on Dutch tax-rule determinism and accountant-grade audit traceability"
      source_lines: "L57"
      confidence: high
    - claim: "The public ecosystem is fragment-rich but solution-poor"
      source_lines: "L6"
      confidence: high
    - claim: "Moneybird is recommended as best first integration, Exact Online as best second integration after rule infrastructure is robust"
      source_lines: "L76-77"
      confidence: high

---

## 02-tax-opportunities

### KOR (Small Business Exemption)
- id: 02-tax-opportunities
  subtopic: kor
  facts:
    - claim: "KOR threshold is currently €20,000"
      source_lines: "L112, L85"
      confidence: high
    - claim: "KOR threshold is year-specific"
      source_lines: "L85"
      confidence: high
    - claim: "KOR strategic choice: no VAT charged, no input VAT reclaim"
      source_lines: "L85"
      confidence: high
    - claim: "KOR eligibility requires Dutch establishment status and annual turnover counted for KOR"
      source_lines: "L85"
      confidence: high
    - claim: "KOR opportunity scanning is high automation fit for detection, medium for recommendation"
      source_lines: "L85"
      confidence: high
    - claim: "KOR is monitored by monitoring KOR suitability and breach risk as a quarterly/ongoing workflow"
      source_lines: "L112"
      confidence: high

### KIA (Small-Scale Investment Deduction)
- id: 02-tax-opportunities
  subtopic: kia
  facts:
    - claim: "KIA has year-versioned tables and thresholds"
      source_lines: "L87"
      confidence: high
    - claim: "KIA calculation inputs: asset dates, amounts, asset qualification, book-year total, per-asset threshold"
      source_lines: "L87"
      confidence: high
    - claim: "KIA has exclusions, low-value assets, instalment timing, desinvestment considerations"
      source_lines: "L87"
      confidence: high
    - claim: "KIA is high automation fit for opportunities and boundary conditions"
      source_lines: "L87"
      confidence: high
    - claim: "KIA detection is part of first five MVP features"
      source_lines: "L520"
      confidence: high
    - claim: "KIA qualifying investments detected as fifth feature in MVP"
      source_lines: "L5"
      confidence: high
    - claim: "KIA opportunity mentioned as ZZP/VOF/BV segment with rolling aggregate of qualifying investments"
      source_lines: "L116"
      confidence: high

### Urencriterium (Hours Threshold)
- id: 02-tax-opportunities
  subtopic: urencriterium
  facts:
    - claim: "Urencriterium is a stable concept with year-specific examples"
      source_lines: "L90"
      confidence: high
    - claim: "Urencriterium threshold includes time entries, planning/admin hours, startup work, interruptions"
      source_lines: "L90"
      confidence: high
    - claim: "Urencriterium evidence quality is crucial, pregnancy/disability rules matter"
      source_lines: "L90"
      confidence: high
    - claim: "Urencriterium is medium-high automation fit if time-tracking exists"
      source_lines: "L90"
      confidence: high
    - claim: "Urencriterium tracker is a required LLM agent role"
      source_lines: "L360"
      confidence: high
    - claim: "Urencriterium test fixture: threshold check at 1,224 vs 1,225 hours"
      source_lines: "L227"
      confidence: high
    - claim: "Urencriterium is detected via approved time entries, calendar, work categories"
      source_lines: "L360"
      confidence: high

### Zelfstandigenaftrek (Self-Employed Deduction)
- id: 02-tax-opportunities
  subtopic: zelfstandigenaftrek
  facts:
    - claim: "Zelfstandigenaftrek is a fixed amount by year"
      source_lines: "L91"
      confidence: high
    - claim: "Zelfstandigenaftrek eligibility: entrepreneur status, urencriterium, AOW status, profit, carryforward"
      source_lines: "L91"
      confidence: high
    - claim: "Zelfstandigenaftrek carryforward of unrealised amount complicates history"
      source_lines: "L91"
      confidence: high
    - claim: "Zelfstandigenaftrek is high automation fit once eligibility is fixed by rules/evidence"
      source_lines: "L91"
      confidence: high
    - claim: "Zelfstandigenaftrek is year-versioned and fixed amount changes by year"
      source_lines: "L41"
      confidence: high

### Startersaftrek (Starter Deduction)
- id: 02-tax-opportunities
  subtopic: startersaftrek
  facts:
    - claim: "Startersaftrek is year-versioned and history-sensitive"
      source_lines: "L92"
      confidence: high
    - claim: "Startersaftrek requires tracking entrepreneur years in prior 5 years, use count, urencriterium"
      source_lines: "L92"
      confidence: high
    - claim: "Startersaftrek is an add-on deduction"
      source_lines: "L92"
      confidence: high
    - claim: "Startersaftrek is high automation fit"
      source_lines: "L92"
      confidence: high
    - claim: "Startersaftrek requires history and startup-year tracking"
      source_lines: "L92"
      confidence: high

### MKB-Winstvrijstelling (SMB Profit Exemption)
- id: 02-tax-opportunities
  subtopic: mkb_winstvrijstelling
  facts:
    - claim: "MKB-winstvrijstelling percentage and benefit cap change by year"
      source_lines: "L93"
      confidence: high
    - claim: "MKB-winstvrijstelling applies to profit after ondernemersaftrek"
      source_lines: "L93"
      confidence: high
    - claim: "MKB-winstvrijstelling has negative-profit and benefit-cap interaction considerations"
      source_lines: "L93"
      confidence: high
    - claim: "MKB-winstvrijstelling is high automation fit"
      source_lines: "L93"
      confidence: high

### WBSO (R&D Tax Credit)
- id: 02-tax-opportunities
  subtopic: wbso
  facts:
    - claim: "WBSO is strongly year-versioned"
      source_lines: "L101"
      confidence: high
    - claim: "WBSO inputs: S&O wages or hours, starter status, chosen method, approved project"
      source_lines: "L101"
      confidence: high
    - claim: "WBSO has percentage, bracket, and optional forfait benefit"
      source_lines: "L101"
      confidence: high
    - claim: "WBSO qualification is not bookkeeping-only; approval workflow matters"
      source_lines: "L101"
      confidence: high
    - claim: "WBSO is medium automation fit for candidate scanning, low for final claim decision"
      source_lines: "L101"
      confidence: high
    - claim: "WBSO/innovatiebox module should start with candidate detection and document completeness"
      source_lines: "L553"
      confidence: high

### Innovatiebox (Innovation Deduction)
- id: 02-tax-opportunities
  subtopic: innovatiebox
  facts:
    - claim: "Innovatiebox is year-versioned and fact-intensive"
      source_lines: "L102"
      confidence: high
    - claim: "Innovatiebox inputs: Vpb taxpayer status, S&O declaration, asset classification, thresholds, development costs, attributable profit"
      source_lines: "L102"
      confidence: high
    - claim: "Innovatiebox has small/large taxpayer distinctions and threshold mechanics"
      source_lines: "L102"
      confidence: high
    - claim: "Innovatiebox has high judgment content; qualification requires specialist review"
      source_lines: "L102"
      confidence: high
    - claim: "Innovatiebox is medium automation fit for candidate detection, low for autonomous conclusion"
      source_lines: "L102"
      confidence: high
    - claim: "Innovatiebox should be postponed in MVP roadmap"
      source_lines: "L529"
      confidence: high
    - claim: "WBSO/innovatiebox candidate detector is a required LLM agent"
      source_lines: "L394"
      confidence: high

### Limited Deductible Costs (Beperkt aftrekbare kosten)
- id: 02-tax-opportunities
  subtopic: limited_deductibility
  facts:
    - claim: "Limited deductible costs threshold changes by year"
      source_lines: "L94"
      confidence: high
    - claim: "Limited deductibility applies to spend categories, annual totals, chosen method"
      source_lines: "L94"
      confidence: high
    - claim: "Representatiekosten/relationship gifts are classified within limited deductibility"
      source_lines: "L94"
      confidence: high
    - claim: "Limited deductibility is high automation fit if expense taxonomy is strong"
      source_lines: "L94"
      confidence: high

### VAT Mixed-Use (Gemengd Gebruik)
- id: 02-tax-opportunities
  subtopic: vat_mixed_use
  facts:
    - claim: "VAT mixed-use has stable pattern, year-end adjustment"
      source_lines: "L95"
      confidence: high
    - claim: "VAT mixed-use calculation: purchase VAT, intended use, actual use, asset/service class"
      source_lines: "L95"
      confidence: high
    - claim: "VAT mixed-use applies to goods vs services vs immovable property"
      source_lines: "L95"
      confidence: high
    - claim: "VAT mixed-use is high automation fit"
      source_lines: "L95"
      confidence: high
    - claim: "Mixed private/business expense cleanup is quarterly opportunity detection"
      source_lines: "L121"
      confidence: high

### Excessief Lenen (Excess Borrowing)
- id: 02-tax-opportunities
  subtopic: excess_borrowing
  facts:
    - claim: "Excessief lenen is an official rule source at belastingdienst.nl"
      source_lines: "L105"
      confidence: high
    - claim: "Excessief lenen planning is kept human-led and not autonomous"
      source_lines: "L497"
      confidence: high
    - claim: "Excessief lenen is detected via BV/DGA edge-case detector"
      source_lines: "L388"
      confidence: high

### Company Car / Private Use
- id: 02-tax-opportunities
  subtopic: company_car
  facts:
    - claim: "Company car rules are highly year-versioned"
      source_lines: "L96"
      confidence: high
    - claim: "Company car calculation: car type, first registration, catalog value, mileage evidence, ownership treatment"
      source_lines: "L96"
      confidence: high
    - claim: "Company car VAT correction uses 2.7% or 1.5% absent detailed records; IB bijtelling has separate logic"
      source_lines: "L96"
      confidence: high
    - claim: "Company car is medium-high automation fit"
      source_lines: "L96"
      confidence: high
    - claim: "No-mileage-log vs full-mileage-log company car is a required test fixture"
      source_lines: "L227"
      confidence: high

### Reverse Charge / EU VAT
- id: 02-tax-opportunities
  subtopic: reverse_charge
  facts:
    - claim: "Reverse charge/intra-EU/VIES/OSS rules apply across EU+Dutch official sources"
      source_lines: "L97"
      confidence: high
    - claim: "Reverse charge calculation: supplier/customer country, VAT IDs, B2B/B2C, service type, goods flow"
      source_lines: "L97"
      confidence: high
    - claim: "Reverse charge considers property-related services, event admission, non-EU services"
      source_lines: "L97"
      confidence: high
    - claim: "Reverse charge is medium-high automation fit"
      source_lines: "L97"
      confidence: high
    - claim: "Missing EC Sales List/VIES evidence is a quarterly opportunity detection"
      source_lines: "L115"
      confidence: high
    - claim: "EU goods/services matrix is a recommended cross-border VAT module"
      source_lines: "L550"
      confidence: high

### Box 2 (Substantial Interest)
- id: 02-tax-opportunities
  subtopic: box_2
  facts:
    - claim: "Box 2 rates change by year"
      source_lines: "L100"
      confidence: high
    - claim: "Box 2 calculation: AB income, dividend/loan events, brackets, partner split"
      source_lines: "L100"
      confidence: high
    - claim: "Box 2 integrates with excess borrowing and DGA actions"
      source_lines: "L100"
      confidence: high
    - claim: "Box 2 is high automation fit once inputs are known"
      source_lines: "L100"
      confidence: high
    - claim: "Box 2 module planning should remain diagnosis + scenario explanation only"
      source_lines: "L549"
      confidence: high

### DGA Salary (Useelijk Loon)
- id: 02-tax-opportunities
  subtopic: dga_salary
  facts:
    - claim: "DGA salary norms exist and are monitored monthly"
      source_lines: "L5, L5"
      confidence: high
    - claim: "DGA salary test fixture: DGA loans just below/above threshold"
      source_lines: "L227"
      confidence: high
    - claim: "DGA/holding/excess-loan/useelijk-loon patterns are detected by BV/DGA edge-case detector"
      source_lines: "L388"
      confidence: high
    - claim: "DGA monthly risk scan includes loans, payroll floor, dividend patterns"
      source_lines: "L467"
      confidence: high

### Representatiekosten (Representation Costs)
- id: 02-tax-opportunities
  subtopic: representatiekosten
  facts:
    - claim: "Representatiekosten falls under limited deductibility rules"
      source_lines: "L94"
      confidence: high
    - claim: "Representatiekosten test fixture: relationship gift/classification examples"
      source_lines: "L227"
      confidence: high

### BTW (VAT) Rates
- id: 02-tax-opportunities
  subtopic: vat_rates
  facts:
    - claim: "BTW rates include 0%, 9%, and 21% for 2026"
      source_lines: "L5"
      confidence: high
    - claim: "BTW 2026: logies (accommodation) moved to 21%"
      source_lines: "L83"
      confidence: high
    - claim: "BTW rates are version by tax year and category"
      source_lines: "L83"
      confidence: high

---

## 03-architecture

### Hybrid System Pattern
- id: 03-architecture
  subtopic: hybrid_system
  facts:
    - claim: "Most defensible architecture is hybrid: API ingestion from source ledger, OCR/document ingestion, deterministic Dutch tax engine, LLM layer for extraction/classification/question-generation only, evidence store, opportunity scanner, exception queue, accountant review before writeback/filing"
      source_lines: "L7"
      confidence: high
    - claim: "Hybrid architecture direction is implied by strongest public evidence from Jortt, Moneybird, AFAS, Exact, KVK, SBR and XAF"
      source_lines: "L8"
      confidence: high

### Deterministic + LLM Split
- id: 03-architecture
  subtopic: deterministic_llm_split
  facts:
    - claim: "Deterministic for numbers and guards, LLM-driven for interpretation and interaction is the only pattern that scales without creating unmanageable liability"
      source_lines: "L450"
      confidence: high
    - claim: "Workflows are intentionally bimodal: deterministic for numbers and guards, LLM-driven for interpretation and interaction"
      source_lines: "L450"
      confidence: high

### Deterministic Calculation Engine
- id: 03-architecture
  subtopic: deterministic_engine
  facts:
    - claim: "Must be custom-built: Dutch year-versioned rule engine, normalized accounting evidence model, calculation traces, opportunity heuristics tied to official citations, safe-writeback approval flows, review packet accountant can sign off on"
      source_lines: "L9"
      confidence: high
    - claim: "Public ecosystem does not provide reusable Dutch engine for KOR/KIA/urencriterium/zelfstandigenaftrek/startersaftrek/MKB-winstvrijstelling/limited deductibility/mixed private-business use/WBSO/innovatiebox/Box 2/excess borrowing/BV-transition logic as single versioned testable component"
      source_lines: "L9-10"
      confidence: high
    - claim: "Dutch deterministic engine is the core IP that should create defensibility"
      source_lines: "L11"
      confidence: high

### RGS Normalization and Ledger Mapping
- id: 03-architecture
  subtopic: rgs_normalization
  facts:
    - claim: "RGS Taxonomy links chart of accounts to SBR"
      source_lines: "L19"
      confidence: high
    - claim: "RGS is essential for normalized chart-of-accounts mapping and filing compatibility"
      source_lines: "L19"
      confidence: high
    - claim: "RGS implementation adds complexity but essential for accountant acceptance"
      source_lines: "L19"
      confidence: high
    - claim: "RGS/XAF should be used for canonical ledger mapping and downstream filing architecture"
      source_lines: "L19"
      confidence: high

### MCP Ingestion Layer
- id: 03-architecture
  subtopic: mcp_ingestion
  facts:
    - claim: "MCP surfaces should be used as developer/operator tooling, not as legal brain"
      source_lines: "L560"
      confidence: high
    - claim: "Moneybird official MCP/CLI are access surfaces, not tax reasoning"
      source_lines: "L17"
      confidence: high

### Exception Handling and Quarantine
- id: 03-architecture
  subtopic: exception_handling
  facts:
    - claim: "System should have exception queue for escalation"
      source_lines: "L7"
      confidence: high
    - claim: "High-risk findings should be escalated to accountant/user review"
      source_lines: "L7"
      confidence: high

### Evidentiary Continuity and Audit Traces
- id: 03-architecture
  subtopic: audit_traces
  facts:
    - claim: "Every deterministic calculation should emit: calc_id, module, rule_ids, source_urls, input_snapshot, input_evidence_ids, intermediate_steps[], output_values, rounding_policy, generated_at, engine_version"
      source_lines: "L236"
      confidence: high
    - claim: "Calculation trace format is critical for audit defense and reproducibility"
      source_lines: "L236"
      confidence: high
    - claim: "Every agent conclusion should include: evidence_ids, rule_ids, calculation_ids if applicable, confidence, risk_level, reviewer_required"
      source_lines: "L310"
      confidence: high

### Evidentiary Store
- id: 03-architecture
  subtopic: evidence_store
  facts:
    - claim: "Accountant-grade evidence retention is required"
      source_lines: "L5"
      confidence: high
    - claim: "Evidence store should link documents to transactions and calculations"
      source_lines: "L7"
      confidence: high
    - claim: "Every output should be traceable to evidence and deterministic rules"
      source_lines: "L470"
      confidence: high

### Rule Versioning
- id: 03-architecture
  subtopic: rule_versioning
  facts:
    - claim: "Each rule module should be stored with: rule_id, tax_year, effective_from, effective_to, jurisdiction, source_urls, source_hashes, numeric_parameters, eligibility_predicates, review_policy"
      source_lines: "L212"
      confidence: high
    - claim: "Source hashes should capture HTML/PDF/text slice used"
      source_lines: "L212"
      confidence: high
    - claim: "Rule-versioning strategy is lightweight analogue of RegelSpraak formalisation"
      source_lines: "L217"
      confidence: high

### Testing Architecture
- id: 03-architecture
  subtopic: testing
  facts:
    - claim: "Four test layers required: unit tests (exact numeric output), regression tests (no change in prior-year outputs), edge-case tests (threshold-edge and exception-case coverage), evidence tests (output points to evidence and official sources)"
      source_lines: "L220"
      confidence: high
    - claim: "KOR, KIA, urencriterium at boundaries, company car, reverse charge, mixed-use, DGA loans, WBSO, innovatiebox test fixtures required"
      source_lines: "L227"
      confidence: high

### Stale-Rule Detection and Monitoring
- id: 03-architecture
  subtopic: stale_rule_detection
  facts:
    - claim: "Must monitor: Belastingdienst 'veranderingen' pages by tax year, RVO yearly pages for WBSO/EIA/MIA/Vamil, ODB/XAF and SBR taxonomy release notes, KVK API release notes, accounting-platform changelogs"
      source_lines: "L244"
      confidence: high
    - claim: "No silent rule mutation in production; open review ticket on changes"
      source_lines: "L421"
      confidence: high

### LLM Bounded Inference Layer
- id: 03-architecture
  subtopic: llm_layer
  facts:
    - claim: "LLM should be treated as bounded inference layer"
      source_lines: "L252"
      confidence: high
    - claim: "Allowed LLM tasks: OCR cleanup, field extraction, receipt/invoice classification candidates, ledger treatment suggestions, missing-evidence detection, anomaly detection, accountant-question generation, user-friendly explanations with citations"
      source_lines: "L252-265"
      confidence: high
    - claim: "Not allowed LLM tasks: inventing rates/thresholds/legal tests, final eligibility decisions, filing tax returns, aggressive legal positions, overriding deterministic outputs, autonomous structure decisions, treating marketing pages as authoritative law"
      source_lines: "L252-265"
      confidence: high

### Outcome States
- id: 03-architecture
  subtopic: outcome_states
  facts:
    - claim: "Allowed outcome states: classified, assumed_conservative, needs_user_input, needs_accountant_review, blocked_out_of_scope"
      source_lines: "L268"
      confidence: high

### Mandatory Output Envelope
- id: 03-architecture
  subtopic: output_envelope
  facts:
    - claim: "Every agent conclusion must include: evidence_ids, rule_ids, calculation_ids if applicable, confidence, risk_level, reviewer_required"
      source_lines: "L310"
      confidence: high
    - claim: "Output envelope turns chat output into auditable work product"
      source_lines: "L315"
      confidence: high

### Accountant-in-Loop Pattern
- id: 03-architecture
  subtopic: accountant_in_loop
  facts:
    - claim: "Safe-writeback approval flows require accountant review before material changes"
      source_lines: "L7"
      confidence: high
    - claim: "Accountant question generator converts unresolved technical issues into crisp questions"
      source_lines: "L370"
      confidence: high
    - claim: "Quarterly VAT preparation requires mandatory accountant/user review before filing"
      source_lines: "L461"
      confidence: high
    - claim: "Annual close requires mandatory accountant approval"
      source_lines: "L463"
      confidence: high

---

## 04-prompts

### Dutch Bookkeeping Classifier Prompt
- id: 04-prompts
  subtopic: dutch_bookkeeping_classifier
  facts:
    - claim: "Role: classify bookkeeping evidence into candidate ledger accounts and VAT treatments, conservatively"
      source_lines: "L316"
      confidence: high
    - claim: "Inputs: normalized document text, merchant history, counterparty profile, existing chart/RGS mapping, open transactions"
      source_lines: "L317"
      confidence: high
    - claim: "Tools: document search, source-ledger lookup, RGS mapper, rule lookup"
      source_lines: "L318"
      confidence: high
    - claim: "Rule: never final-post; if multiple plausible ledgers exist, prefer needs_user_input"
      source_lines: "L319"
      confidence: high
    - claim: "Special evidence requirement: cite source document fields and prior-linked transactions"
      source_lines: "L320"
      confidence: high

### VAT Review Agent Prompt
- id: 04-prompts
  subtopic: vat_review_agent
  facts:
    - claim: "Role: review VAT treatment candidates on invoices and purchases"
      source_lines: "L323"
      confidence: high
    - claim: "Inputs: invoice lines, countries, VAT IDs, customer type, tax codes, VIES result"
      source_lines: "L324"
      confidence: high
    - claim: "Tools: VAT rule lookup, VIES validator, historical postings"
      source_lines: "L325"
      confidence: high
    - claim: "Rule: if place-of-supply is ambiguous, escalate"
      source_lines: "L326"
      confidence: high
    - claim: "JSON focus: include vat_candidate, return_box_candidate, vies_required"
      source_lines: "L327"
      confidence: high

### Missing Receipt Detector Prompt
- id: 04-prompts
  subtopic: missing_receipt_detector
  facts:
    - claim: "Role: find bank/PSP expenses lacking evidence"
      source_lines: "L329"
      confidence: high
    - claim: "Inputs: uncoupled bank mutations, uploaded documents, merchant recurrence"
      source_lines: "L330"
      confidence: high
    - claim: "Tools: matching engine, document hash index"
      source_lines: "L331"
      confidence: high
    - claim: "Rule: do not hallucinate documents; ask for upload or mark conservative"
      source_lines: "L332"
      confidence: high
    - claim: "JSON focus: include missing_document_reason, matching_candidates"
      source_lines: "L333"
      confidence: high

### Deductibility Classifier Prompt
- id: 04-prompts
  subtopic: deductibility_classifier
  facts:
    - claim: "Role: assess whether costs are likely fully deductible, limited, mixed-use or non-deductible"
      source_lines: "L335"
      confidence: high
    - claim: "Inputs: merchant/category, receipt text, user role/context, prior treatment"
      source_lines: "L336"
      confidence: high
    - claim: "Tools: deductibility rules, historical learnings"
      source_lines: "L337"
      confidence: high
    - claim: "Rule: if business purpose is not evidenced, return assumed_conservative"
      source_lines: "L338"
      confidence: high
    - claim: "JSON focus: include deductibility_class, business_purpose_gap"
      source_lines: "L339"
      confidence: high

### KOR Scanner Prompt
- id: 04-prompts
  subtopic: kor_scanner
  facts:
    - claim: "Role: monitor KOR suitability and breach risk"
      source_lines: "L341"
      confidence: high
    - claim: "Inputs: counted turnover YTD, forecast, input VAT reclaim history, planned capex"
      source_lines: "L342"
      confidence: high
    - claim: "Tools: KOR rule module, forecasting helper"
      source_lines: "L343"
      confidence: high
    - claim: "Rule: never recommend switching without showing downside"
      source_lines: "L344"
      confidence: high
    - claim: "JSON focus: include turnover_counted, threshold_buffer, switch_review_reason"
      source_lines: "L345"
      confidence: high

### KIA Scanner Prompt
- id: 04-prompts
  subtopic: kia_scanner
  facts:
    - claim: "Role: detect KIA opportunities and boundary conditions"
      source_lines: "L347"
      confidence: high
    - claim: "Inputs: asset register, invoice dates, amounts, qualifying flags"
      source_lines: "L348"
      confidence: high
    - claim: "Tools: KIA tables by year"
      source_lines: "L349"
      confidence: high
    - claim: "Rule: classify uncertain assets for human review"
      source_lines: "L350"
      confidence: high
    - claim: "JSON focus: include qualifying_total, next_threshold, uncertain_assets"
      source_lines: "L351"
      confidence: high

### Urencriterium Tracker Prompt
- id: 04-prompts
  subtopic: urencriterium_tracker
  facts:
    - claim: "Role: determine current urencriterium trajectory"
      source_lines: "L353"
      confidence: high
    - claim: "Inputs: approved time entries, calendar, work categories"
      source_lines: "L354"
      confidence: high
    - claim: "Tools: time aggregation, duplicate detector"
      source_lines: "L355"
      confidence: high
    - claim: "Rule: no guessing of hours; inferred items must be labelled"
      source_lines: "L356"
      confidence: high
    - claim: "JSON focus: include eligible_hours, projected_hours, evidence_gaps"
      source_lines: "L357"
      confidence: high

### Quarterly Opportunity Scanner Prompt
- id: 04-prompts
  subtopic: quarterly_opportunity_scanner
  facts:
    - claim: "Role: run a broad quarterly scan for Dutch tax opportunities and risks"
      source_lines: "L359"
      confidence: high
    - claim: "Inputs: full quarter ledger, asset changes, loan movements, time, documents"
      source_lines: "L360"
      confidence: high
    - claim: "Tools: all deterministic modules"
      source_lines: "L361"
      confidence: high
    - claim: "Rule: produce findings, not decisions"
      source_lines: "L362"
      confidence: high
    - claim: "JSON focus: array of findings[]"
      source_lines: "L363"
      confidence: high

### Annual Close Reviewer Prompt
- id: 04-prompts
  subtopic: annual_close_reviewer
  facts:
    - claim: "Role: review year-end completeness and adjustment candidates"
      source_lines: "L365"
      confidence: high
    - claim: "Inputs: full-year ledger, open suspense items, missing evidence, asset changes, private-use markers"
      source_lines: "L366"
      confidence: high
    - claim: "Tools: year-end checklist, VAT correction rules"
      source_lines: "L367"
      confidence: high
    - claim: "Rule: anything affecting filed numbers requires reviewer"
      source_lines: "L368"
      confidence: high
    - claim: "JSON focus: close_issues[], proposed_adjustments[]"
      source_lines: "L369"
      confidence: high

### Accountant Question Generator Prompt
- id: 04-prompts
  subtopic: accountant_question_generator
  facts:
    - claim: "Role: convert unresolved technical issues into crisp accountant questions"
      source_lines: "L371"
      confidence: high
    - claim: "Inputs: findings, evidence gaps, candidate positions"
      source_lines: "L372"
      confidence: high
    - claim: "Tools: none beyond evidence graph and rules"
      source_lines: "L373"
      confidence: high
    - claim: "Rule: one question per issue; include facts only"
      source_lines: "L374"
      confidence: high
    - claim: "JSON focus: question_text, relevant_facts, documents_needed"
      source_lines: "L375"
      confidence: high

### BV/DGA Edge-Case Detector Prompt
- id: 04-prompts
  subtopic: bv_dga_detector
  facts:
    - claim: "Role: flag DGA/holding/excess-loan/useelijk-loon patterns"
      source_lines: "L377"
      confidence: high
    - claim: "Inputs: shareholder loans, payroll, dividends, intercompany postings"
      source_lines: "L378"
      confidence: high
    - claim: "Tools: box2/useelijk-loon/excess-lening modules"
      source_lines: "L379"
      confidence: high
    - claim: "Rule: always escalate structure-sensitive conclusions"
      source_lines: "L380"
      confidence: high
    - claim: "JSON focus: structure_flags[]"
      source_lines: "L381"
      confidence: high

### WBSO / Innovatiebox Candidate Detector Prompt
- id: 04-prompts
  subtopic: wbso_innovatiebox_detector
  facts:
    - claim: "Role: detect candidate innovative activity and route to specialist review"
      source_lines: "L383"
      confidence: high
    - claim: "Inputs: development payroll, Git/project metadata, milestones, prior WBSO documents"
      source_lines: "L384"
      confidence: high
    - claim: "Tools: WBSO and innovation-box eligibility heuristics"
      source_lines: "L385"
      confidence: high
    - claim: "Rule: candidate detection only, no autonomous eligibility"
      source_lines: "L386"
      confidence: high
    - claim: "JSON focus: candidate_score, supporting_indicators, specialist_needed"
      source_lines: "L387"
      confidence: high

### Source-Verification Agent Prompt
- id: 04-prompts
  subtopic: source_verification_agent
  facts:
    - claim: "Role: verify that a claimed rule or threshold is backed by an official source"
      source_lines: "L389"
      confidence: high
    - claim: "Inputs: claim text, candidate source URLs, tax year"
      source_lines: "L390"
      confidence: high
    - claim: "Tools: official-source registry only"
      source_lines: "L391"
      confidence: high
    - claim: "Rule: if only non-official sources exist, mark low confidence"
      source_lines: "L392"
      confidence: high
    - claim: "JSON focus: verified_claim, official_source_urls, version_date"
      source_lines: "L393"
      confidence: high

### Rule-Update Monitor Prompt
- id: 04-prompts
  subtopic: rule_update_monitor
  facts:
    - claim: "Role: detect changes in official rules and downstream code impact"
      source_lines: "L395"
      confidence: high
    - claim: "Inputs: monitored URL registry, prior hashes, rule metadata"
      source_lines: "L396"
      confidence: high
    - claim: "Tools: diff engine, release feed parser"
      source_lines: "L397"
      confidence: high
    - claim: "Rule: no silent rule mutation in production; open review ticket"
      source_lines: "L398"
      confidence: high
    - claim: "JSON focus: changed_rules[], impact_modules[]"
      source_lines: "L399"
      confidence: high

### Safe Writeback Reviewer Prompt
- id: 04-prompts
  subtopic: safe_writeback_reviewer
  facts:
    - claim: "Role: approve or block proposed writeback operations"
      source_lines: "L401"
      confidence: high
    - claim: "Inputs: draft ledger changes, evidence IDs, calc traces, reviewer identity"
      source_lines: "L402"
      confidence: high
    - claim: "Tools: deterministic validator, permission checker"
      source_lines: "L403"
      confidence: high
    - claim: "Rule: block if no evidence, no trace, or high-risk tax treatment unresolved"
      source_lines: "L404"
      confidence: high
    - claim: "JSON focus: writeback_decision, blocking_reasons, required_approvals"
      source_lines: "L405"
      confidence: high

### Prompt Pack Inheritance
- id: 04-prompts
  subtopic: prompt_pack_contract
  facts:
    - claim: "All prompts inherit same contract: confidence labels (high/medium/low), risk levels (low/medium/high), refusal/escalation if rule data missing or evidence absent"
      source_lines: "L276-286"
      confidence: high
    - claim: "Output schema inherited by all prompts: outcome, summary, evidence_ids, rule_ids, calculation_ids, confidence, risk_level, reviewer_required, questions, proposed_actions"
      source_lines: "L289"
      confidence: high

---

## 05-rules-2026

### VAT Rates 2026
- id: 05-rules-2026
  subtopic: vat_rates_2026
  facts:
    - claim: "VAT rates include 0%, 9%, 21% in 2026"
      source_lines: "L5, L83"
      confidence: high
    - claim: "VAT 2026: logies (accommodation) moved to 21%"
      source_lines: "L83"
      confidence: high
    - claim: "VAT rates are versioned by tax year and category"
      source_lines: "L83"
      confidence: high
    - claim: "Official source: belastingdienst.nl/.../btw_tarief/btw_tarief"
      source_lines: "L554"
      confidence: high

### KOR Threshold 2026
- id: 05-rules-2026
  subtopic: kor_threshold
  facts:
    - claim: "KOR threshold is €20,000"
      source_lines: "L85, L112"
      confidence: high
    - claim: "KOR is year-specific threshold that changes"
      source_lines: "L85"
      confidence: high
    - claim: "Official source: belastingdienst.nl/.../kleineondernemersregeling"
      source_lines: "L562"
      confidence: high

### KIA 2026 Thresholds
- id: 05-rules-2026
  subtopic: kia_thresholds
  facts:
    - claim: "KIA has year-versioned tables for 2026"
      source_lines: "L87"
      confidence: high
    - claim: "KIA qualification depends on asset dates, amounts, and per-asset thresholds"
      source_lines: "L87"
      confidence: high
    - claim: "Official source: belastingdienst.nl/.../kleinschaligheidsinvesteringsaftrek"
      source_lines: "L564"
      confidence: high

### Excessief Lenen Limit 2026
- id: 05-rules-2026
  subtopic: excess_borrowing
  facts:
    - claim: "Excessief lenen has numeric limits and year-specific calculations"
      source_lines: "L5"
      confidence: high
    - claim: "Official source: belastingdienst.nl/.../excessief-lenen-van-bv-beperkt"
      source_lines: "L572"
      confidence: high

### Representatiekosten 2026
- id: 05-rules-2026
  subtopic: representatiekosten
  facts:
    - claim: "Representatiekosten limit is €5,700"
      source_lines: "L5"
      confidence: high
    - claim: "Representatiekosten are limited deductible costs"
      source_lines: "L94"
      confidence: high

### DGA Salary Norms 2026
- id: 05-rules-2026
  subtopic: dga_salary_norms
  facts:
    - claim: "DGA salary norms exist and are monitored"
      source_lines: "L5"
      confidence: high
    - claim: "DGA salary is part of useelijk-loon compliance"
      source_lines: "L5"
      confidence: high

### Box 1 2026 Brackets
- id: 05-rules-2026
  subtopic: box_1_brackets
  facts:
    - claim: "Box 1 brackets are year-versioned and change for 2026"
      source_lines: "L5"
      confidence: high

### Box 2 2026
- id: 05-rules-2026
  subtopic: box_2_rates
  facts:
    - claim: "Box 2 rates change by year"
      source_lines: "L100"
      confidence: high
    - claim: "Box 2 2026 rates visible in official sources"
      source_lines: "L576"
      confidence: high
    - claim: "Official source: belastingdienst.nl/.../box_2"
      source_lines: "L576"
      confidence: high

### Box 3 2026
- id: 05-rules-2026
  subtopic: box_3
  facts:
    - claim: "Box 3 2026 pages are visible in official sources"
      source_lines: "L579"
      confidence: high
    - claim: "Box 3 is versioned by year and sensitive area"
      source_lines: "L5, L549"
      confidence: high

### Deadlines 2026
- id: 05-rules-2026
  subtopic: deadlines
  facts:
    - claim: "VAT quarterly deadline applies to quarterly filers"
      source_lines: "L5"
      confidence: high
    - claim: "Prinsjesdag (Budget Day) is a key annual deadline"
      source_lines: "L5"
      confidence: high
    - claim: "KVK registration deadlines apply"
      source_lines: "L5"
      confidence: high
    - claim: "VAT correction deadline: 8-week timing after discovery of error; penalties if late"
      source_lines: "L84"
      confidence: high

### Zelfstandigenaftrek 2026
- id: 05-rules-2026
  subtopic: zelfstandigenaftrek_2026
  facts:
    - claim: "Zelfstandigenaftrek is fixed amount by year and changes for 2026"
      source_lines: "L91, L41"
      confidence: high
    - claim: "Zelfstandigenaftrek has carryforward mechanics"
      source_lines: "L91"
      confidence: high

### Startersaftrek 2026
- id: 05-rules-2026
  subtopic: startersaftrek_2026
  facts:
    - claim: "Startersaftrek is year-versioned for 2026"
      source_lines: "L92"
      confidence: high
    - claim: "Startersaftrek requires 5-year prior history tracking"
      source_lines: "L92"
      confidence: high

### MKB-Winstvrijstelling 2026
- id: 05-rules-2026
  subtopic: mkb_winstvrijstelling_2026
  facts:
    - claim: "MKB-winstvrijstelling percentage and benefit cap change for 2026"
      source_lines: "L93"
      confidence: high
    - claim: "Official source: belastingdienst.nl/.../mkb_winstvrijstelling"
      source_lines: "L568"
      confidence: high

---

## 06-build-vs-buy

### Build-vs-Buy Decision Matrix
- id: 06-build-vs-buy
  subtopic: build_vs_buy_matrix
  facts:
    - claim: "Use existing: Moneybird, Exact SDKs, KVK APIs, Ponto/bunq/Mollie/Stripe discussions, community MCPs"
      source_lines: "L483"
      confidence: high
    - claim: "Build yourself: custom normalization and idempotent connector wrappers"
      source_lines: "L484"
      confidence: high
    - claim: "Build yourself: Dutch invoice/receipt post-processing and evidence linker"
      source_lines: "L486"
      confidence: high
    - claim: "Build yourself: fully custom deterministic engine for tax rules"
      source_lines: "L489"
      confidence: high
    - claim: "Build yourself: custom findings framework for opportunity scanning"
      source_lines: "L490"
      confidence: high
    - claim: "Keep human-led: final acceptance of unusual ledger cases"
      source_lines: "L485"
      confidence: high
    - claim: "Keep human-led: eligibility on fact-heavy regimes (WBSO, innovatiebox)"
      source_lines: "L492"
      confidence: high
    - claim: "Keep human-led: human/accountant handling of filing"
      source_lines: "L491"
      confidence: high
    - claim: "Keep human-led: accountant/fiscalist handling of structure planning"
      source_lines: "L491"
      confidence: high

### Things Not Worth Building Initially
- id: 06-build-vs-buy
  subtopic: things_not_to_build
  facts:
    - claim: "Autonomous filing should not be built"
      source_lines: "L499"
      confidence: high
    - claim: "Full BV/holding/intercompany engine in v1 should not be built"
      source_lines: "L500"
      confidence: high
    - claim: "Box 3 planning beyond basic data preparation should not be built"
      source_lines: "L501"
      confidence: high
    - claim: "Full standalone bookkeeping ledger replacing source system should not be built"
      source_lines: "L502"
      confidence: high
    - claim: "Deep custom OCR stack before validating demand should not be built"
      source_lines: "L503"
      confidence: high

### Things Never to Automate
- id: 06-build-vs-buy
  subtopic: never_automate
  facts:
    - claim: "Structure changes should never be fully automated"
      source_lines: "L507"
      confidence: high
    - claim: "Aggressive tax positions should never be fully automated"
      source_lines: "L508"
      confidence: high
    - claim: "Final eligibility calls for innovation regimes should never be automated"
      source_lines: "L509"
      confidence: high
    - claim: "Material ledger writeback without approval should never be automated"
      source_lines: "L510"
      confidence: high
    - claim: "Communication that sounds like legal advice should never be automated"
      source_lines: "L511"
      confidence: high

### MVP Recommendation
- id: 06-build-vs-buy
  subtopic: mvp_recommendation
  facts:
    - claim: "Most defensible MVP is a Dutch freelancer/consultant/micro-agency copilot on Moneybird"
      source_lines: "L514"
      confidence: high
    - claim: "First user segment: NL ZZP/sole traders and small BV operators with clean digital workflows, services revenue, recurring software spend, moderate foreign-VAT/reverse-charge exposure"
      source_lines: "L516"
      confidence: high
    - claim: "Moneybird is best first integration due to best API quality, webhooks, official AI surfaces, pragmatic SMB scope, community tooling"
      source_lines: "L519"
      confidence: high

### First Five Features
- id: 06-build-vs-buy
  subtopic: first_five_features
  facts:
    - claim: "Feature 1: Document/evidence ingestion with OCR cleanup and source linking"
      source_lines: "L521"
      confidence: high
    - claim: "Feature 2: Draft transaction/invoice classification with VAT candidate selection"
      source_lines: "L522"
      confidence: high
    - claim: "Feature 3: Missing-receipt and mixed-use expense detector"
      source_lines: "L523"
      confidence: high
    - claim: "Feature 4: Quarterly VAT prep packet with anomaly list and reverse-charge checks"
      source_lines: "L524"
      confidence: high
    - claim: "Feature 5: Tax-opportunity scan for KOR, KIA, urencriterium, limited-deductibility, car/mileage, excess-loan red flags"
      source_lines: "L525"
      confidence: high

### Features to Postpone
- id: 06-build-vs-buy
  subtopic: postpone_features
  facts:
    - claim: "Innovatiebox final logic should be postponed"
      source_lines: "L528"
      confidence: high
    - claim: "Full WBSO submission preparation should be postponed"
      source_lines: "L529"
      confidence: high
    - claim: "Multi-entity consolidation should be postponed"
      source_lines: "L530"
      confidence: high
    - claim: "Payroll-heavy DGA workflows should be postponed"
      source_lines: "L531"
      confidence: high
    - claim: "Cross-border goods complexity should be postponed before domestic services are stable"
      source_lines: "L532"
      confidence: high

### Features to Avoid
- id: 06-build-vs-buy
  subtopic: avoid_features
  facts:
    - claim: "Should not promise 'autonomous tax optimisation'"
      source_lines: "L535"
      confidence: high
    - claim: "Should not use AI to generate final return numbers without traceable deterministic modules"
      source_lines: "L536"
      confidence: high
    - claim: "Should not build custom bank connectors where PSD2 aggregators solve the problem"
      source_lines: "L537"
      confidence: high

### Success Metrics
- id: 06-build-vs-buy
  subtopic: success_metrics
  facts:
    - claim: "Share of transactions auto-classified into low-risk draft state"
      source_lines: "L540"
      confidence: high
    - claim: "Percentage of findings accepted by accountant review"
      source_lines: "L541"
      confidence: high
    - claim: "Reduction in missing-doc backlog"
      source_lines: "L542"
      confidence: high
    - claim: "Time to quarterly VAT prep"
      source_lines: "L543"
      confidence: high
    - claim: "False-positive rate on high-risk findings"
      source_lines: "L544"
      confidence: high

### Representative Test Scenarios
- id: 06-build-vs-buy
  subtopic: test_scenarios
  facts:
    - claim: "Test scenario 1: Domestic SaaS freelancer under/near KOR threshold"
      source_lines: "L547"
      confidence: high
    - claim: "Test scenario 2: Consultant with EU B2B reverse-charge invoices"
      source_lines: "L548"
      confidence: high
    - claim: "Test scenario 3: Creative professional with mixed private/business software and telecom spend"
      source_lines: "L549"
      confidence: high
    - claim: "Test scenario 4: Micro-BV with one shareholder current account and no mileage log"
      source_lines: "L550"
      confidence: high
    - claim: "Test scenario 5: Service business buying equipment late in year near KIA thresholds"
      source_lines: "L551"
      confidence: high

### Advanced Roadmap Modules
- id: 06-build-vs-buy
  subtopic: advanced_roadmap
  facts:
    - claim: "BV/DGA module: add shareholder-loan monitoring, useelijk-loon risk flags, dividend timing, intercompany detection; keep final review with qualified advisers"
      source_lines: "L552"
      confidence: high
    - claim: "Holding/intercompany module: after robust entity-normalization and permissions"
      source_lines: "L554"
      confidence: high
    - claim: "WBSO/innovatiebox module: candidate detection first, then specialist workpapers; do not automate final qualification"
      source_lines: "L556"
      confidence: high
    - claim: "Cross-border VAT module: add EU goods/services matrix, OSS/IOSS, ICP/ESL evidence, foreign marketplace, VIES audit logging"
      source_lines: "L560"
      confidence: high
    - claim: "Box 2/Box 3 planning: keep diagnosis + scenario explanation only; Box 3 must remain year-versioned and review-gated"
      source_lines: "L565"
      confidence: high
    - claim: "Continuous law-update testing: treat rule changes as software changes; every rule diff opens regression test"
      source_lines: "L568"
      confidence: high

---

## 07-risks-sources

### Risk Analysis: Largest Product Risk
- id: 07-risks-sources
  subtopic: hallucination_risk
  facts:
    - claim: "Largest product risk is not classification accuracy; it is users mistaking system for tax adviser"
      source_lines: "L473"
      confidence: high
    - claim: "Safest stance: opinionated about data quality, tracing, opportunity detection; explicitly cautious about legal positions, restructurings, filings"
      source_lines: "L473"
      confidence: high

### Hallucination and Wrong-Filing Risk Management
- id: 07-risks-sources
  subtopic: hallucination_mitigation
  facts:
    - claim: "Never let LLM invent numeric parameters"
      source_lines: "L477"
      confidence: high
    - claim: "Require official source binding for every rule module"
      source_lines: "L478"
      confidence: high
    - claim: "Separate 'candidate detection' from 'approved calculation'"
      source_lines: "L479"
      confidence: high
    - claim: "Make every material output reproducible from evidence and deterministic rules"
      source_lines: "L480"
      confidence: high
    - claim: "Require human approval for writeback and filing"
      source_lines: "L481"
      confidence: high

### GDPR and Security Risk Management
- id: 07-risks-sources
  subtopic: gdpr_security
  facts:
    - claim: "Minimise LLM context; send only fields needed"
      source_lines: "L484"
      confidence: high
    - claim: "Keep original evidence in separate encrypted store"
      source_lines: "L485"
      confidence: high
    - claim: "Maintain per-object provenance and role-based access"
      source_lines: "L486"
      confidence: high
    - claim: "Prefer EU storage and processors for documents and audit artefacts"
      source_lines: "L487"
      confidence: high
    - claim: "Log every user-visible explanation and system-side writeback proposal"
      source_lines: "L488"
      confidence: high

### Accountant-Reliance and Audit-Defence Risk
- id: 07-risks-sources
  subtopic: audit_defence
  facts:
    - claim: "Export XAF 4.0 and accountant workpapers"
      source_lines: "L491"
      confidence: high
    - claim: "Include evidence IDs and source URLs on findings"
      source_lines: "L492"
      confidence: high
    - claim: "Keep immutable snapshots of rule versions used for each period"
      source_lines: "L493"
      confidence: high
    - claim: "Preserve human review record for high-risk issues"
      source_lines: "L494"
      confidence: high

### Source Trust Levels
- id: 07-risks-sources
  subtopic: source_trust_levels
  facts:
    - claim: "Belastingdienst official sources have HIGH trust and are NL-specific, tax-specific"
      source_lines: "L554-579"
      confidence: high
    - claim: "RVO official sources have HIGH trust and are NL-specific, tax-specific"
      source_lines: "L567, L582-587"
      confidence: high
    - claim: "Official standards (RGS, SBR, XAF, Digipoort) have HIGH trust"
      source_lines: "L592-598"
      confidence: high
    - claim: "KVK API has HIGH trust, NL-specific, not tax-specific"
      source_lines: "L599"
      confidence: high
    - claim: "Moneybird developer docs have HIGH trust, NL-specific, indirect tax coverage"
      source_lines: "L602"
      confidence: high
    - claim: "OpenAccountants has MEDIUM trust, limited NL-specific depth"
      source_lines: "L617"
      confidence: medium
    - claim: "Commercial claims (Jortt, Yuki, Boekie) have MEDIUM-HIGH trust; vendor claims not independently proven"
      source_lines: "L606, L610, L31"
      confidence: medium

### Open Questions and Limitations
- id: 07-risks-sources
  subtopic: open_questions
  facts:
    - claim: "No strong public, production-proven MCP surface for e-Boekhouden, Yuki, AFAS, Twinfield, SnelStart comparable to Moneybird"
      source_lines: "L625"
      confidence: high
    - claim: "Public Dutch open-source code for actual Dutch tax calculations is thin; mostly connectors/wrappers"
      source_lines: "L626"
      confidence: high
    - claim: "Commercial AI-bookkeeping products make strong automation claims but internal control models cannot be verified from public evidence"
      source_lines: "L627"
      confidence: high
    - claim: "Box 3, innovation-box, DGA/holding matters require year-versioning and human review"
      source_lines: "L628"
      confidence: high

### Source Table Citation
- id: 07-risks-sources
  subtopic: source_table
  facts:
    - claim: "Comprehensive source table provided with 40+ sources including Belastingdienst, RVO, official standards, commercial tools, open-source projects"
      source_lines: "L553-630"
      confidence: high
    - claim: "Each source rated by NL-specificity, tax-specificity, depth, trust level, last visible date, reusable value, caveat"
      source_lines: "L553-630"
      confidence: high

### Final Recommendation: Best Path
- id: 07-risks-sources
  subtopic: final_recommendation
  facts:
    - claim: "Start on Moneybird"
      source_lines: "L637"
      confidence: high
    - claim: "Build read-mostly copilot first: ingest, classify, detect, explain, package"
      source_lines: "L638"
      confidence: high
    - claim: "Make deterministic Dutch tax engine core IP"
      source_lines: "L639"
      confidence: high
    - claim: "Use LLM only for extraction, candidate classification, anomaly detection, question generation, source-grounded explanations"
      source_lines: "L640"
      confidence: high
    - claim: "Implement findings, calculation traces, evidence IDs, review gates before ambitious automation"
      source_lines: "L641"
      confidence: high
    - claim: "Use official Dutch sources for rules, RGS/XAF for interoperability, KVK/VIES/RVO for enrichment"
      source_lines: "L642"
      confidence: high

### Best Practical Stack
- id: 07-risks-sources
  subtopic: best_practical_stack
  facts:
    - claim: "Source ledger: Moneybird first, Exact second"
      source_lines: "L646"
      confidence: high
    - claim: "Connector model: official APIs + webhooks; MCP/CLI only as developer/operator tooling, not legal brain"
      source_lines: "L647"
      confidence: high
    - claim: "Rules: custom year-versioned deterministic engine backed by Belastingdienst/RVO/EC official sources"
      source_lines: "L648"
      confidence: high
    - claim: "Schema: normalized internal evidence graph with XAF export support and optional RGS mapping"
      source_lines: "L649"
      confidence: high
    - claim: "LLM: bounded reviewer/explainer/extractor, never final calculator"
      source_lines: "L650"
      confidence: high
    - claim: "Human oversight: entrepreneur for facts, accountant/fiscalist for tax positions and structure-sensitive matters"
      source_lines: "L651"
      confidence: high

