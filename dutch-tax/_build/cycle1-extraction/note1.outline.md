# note1.outline.md – Structured Topic-Keyed Outline

## 01-existing-tools

- id: 01-existing-tools
  subtopic: openaccountants_netherlands_skill
  facts:
    - claim: "OpenAccountants Netherlands skill covers Dutch IB, VAT-adjacent bookkeeping, entrepreneur deductions, conservative defaults, bank-statement patterns, working-paper output"
      source_lines: "L20"
      confidence: high
    - claim: "Netherlands skill is tagged Q3 / AI-drafted / not independently verified"
      source_lines: "L7, L23"
      confidence: high
    - claim: "Netherlands skill covers zelfstandigenaftrek, startersaftrek, MKB-winstvrijstelling, KIA flagging, hours log review, KOR/VAT revenue warning, non-deductible items"
      source_lines: "L22"
      confidence: high
    - claim: "Netherlands skill lists BV/DGA, Box 2, complex auto, WBSO, international, 30%-ruling as gaps/out of scope"
      source_lines: "L24"
      confidence: high

- id: 01-existing-tools
  subtopic: speedy_eboekhouden
  facts:
    - claim: "Speedy e-Boekhouden v1.3.1 released April 8, 2026"
      source_lines: "L33"
      confidence: high
    - claim: "Speedy integrates AI-assisted bulk hour logging, bank processing, invoice OCR, supplier/amount/VAT/ledger extraction, ledger-account and BTW-code classification"
      source_lines: "L31"
      confidence: high
    - claim: "Speedy does not implement KIA/KOR/Box/DGA/WBSO optimization"
      source_lines: "L32"
      confidence: high
    - claim: "Speedy has visible Go/React/Postgres/Redis/Claude architecture"
      source_lines: "L8"
      confidence: high

- id: 01-existing-tools
  subtopic: moneybird_mcp_connector
  facts:
    - claim: "Moneybird official AI-koppeling says ChatGPT, Cursor, Mistral, Claude can connect with read-only or read-write modes"
      source_lines: "L41"
      confidence: high
    - claim: "Moneybird API exposes financial accounts, purchase transactions, ledger accounts, tax rates, time entries, webhooks"
      source_lines: "L40"
      confidence: high
    - claim: "Moneybird MCP exposes contacts, invoices, accounts, payments, products, projects, custom API requests"
      source_lines: "L9"
      confidence: high
    - claim: "Moneybird read-write excludes delete actions; production should start read-only"
      source_lines: "L146"
      confidence: medium

- id: 01-existing-tools
  subtopic: jortt_boekhoudbot
  facts:
    - claim: "Jortt's bookkeeping bot runs bank to VAT return, annual accounts, income tax return path using fixed controlled rules"
      source_lines: "L61"
      confidence: high
    - claim: "Jortt implements bank mutation categorization, invoice/payment matching, VAT placement, automatic controls, annual accounts, IB reporting, KIA reporting, year-close checklists"
      source_lines: "L61"
      confidence: high

- id: 01-existing-tools
  subtopic: other_bookkeeping_platforms
  facts:
    - claim: "e-Boekhouden has strong public wrapper/API patterns and REST API wrapper exposure of invoices, ledgers, mutations, relations, cost centers, VAT codes"
      source_lines: "L121"
      confidence: high
    - claim: "Exact Online can be accessed through Exact APIs or CData read-only MCP"
      source_lines: "L111"
      confidence: medium
    - claim: "Boekie AI claims Exact Online and e-Boekhouden integrations, bank transaction processing, purchase/sales invoice OCR, automatic VAT calculation, ledger mapping, learning from corrections, confidence scoring"
      source_lines: "L71"
      confidence: medium

- id: 01-existing-tools
  subtopic: commercial_products
  facts:
    - claim: "Paperdork advertises dashboards with KIA threshold, urencriterium, zelfstandigenaftrek, startersaftrek tax-benefit insights"
      source_lines: "L81"
      confidence: medium
    - claim: "BTW Vriend describes Dutch ZZP/VOF bookkeeping with invoices, receipts, VAT, KIA benefit calculation, zelfstandigenaftrek, startersaftrek, MKB-winstvrijstelling"
      source_lines: "L91"
      confidence: medium
    - claim: "Fiscaal Agent / Virtual Outcomes offers VAT calculators, urencriterium tracking, belastingdruk calculators, scenario planning, ZZP-versus-BV considerations"
      source_lines: "L101"
      confidence: medium

- id: 01-existing-tools
  subtopic: connectors_and_sdks
  facts:
    - claim: "CData Exact Online MCP is a local read-only MCP server exposing Exact Online through JDBC relational model"
      source_lines: "L111"
      confidence: high
    - claim: "moneysnake Moneybird SDK latest release Apr. 2, 2026"
      source_lines: "L462"
      confidence: high
    - claim: "MoneybirdPaypalFetcher imports PayPal transactions and splits PayPal fees into cost transactions"
      source_lines: "L121"
      confidence: high

## 02-tax-opportunities

- id: 02-tax-opportunities
  subtopic: kia
  facts:
    - claim: "2026 KIA applies from €2,901 to €398,236 with tiered percentages/amounts"
      source_lines: "L175, L161"
      confidence: high
    - claim: "KIA applies to entrepreneurs investing in business assets; asset purchases over threshold, combined annual investment, timing before/after year-end, excluded assets"
      source_lines: "L175"
      confidence: high
    - claim: "System should detect KIA thresholds and timing; rule type is Deterministic + review"
      source_lines: "L175"
      confidence: high

- id: 02-tax-opportunities
  subtopic: kor_klein_ondernemers_regeling
  facts:
    - claim: "KOR applies at ≤ €20,000 turnover; participants do not charge VAT, file no VAT return, cannot deduct input VAT"
      source_lines: "L174"
      confidence: high
    - claim: "System should detect: Turnover near/under €20,000; whether VAT exemption helps or hurts because input VAT cannot be reclaimed"
      source_lines: "L174"
      confidence: high

- id: 02-tax-opportunities
  subtopic: urencriterium
  facts:
    - claim: "Belastingdienst requires at least 1,225 hours and generally more time in the business than other work, with evidence"
      source_lines: "L177, L161"
      confidence: high
    - claim: "System should detect whether logged hours plausibly meet 1,225; missing evidence; employee-time comparison"
      source_lines: "L177"
      confidence: high

- id: 02-tax-opportunities
  subtopic: zelfstandigenaftrek
  facts:
    - claim: "2026 zelfstandigenaftrek is €1,200 under listed conditions"
      source_lines: "L178, L161"
      confidence: high
    - claim: "System should detect: Eligibility and 2026 amount; AOW adjustment; unused carry-forward if low profit"
      source_lines: "L178"
      confidence: high

- id: 02-tax-opportunities
  subtopic: startersaftrek
  facts:
    - claim: "2026 startersaftrek is €2,123 when conditions are met"
      source_lines: "L179"
      confidence: high
    - claim: "System should detect: Whether eligible for starter increase; prior-year usage count"
      source_lines: "L179"
      confidence: high

- id: 02-tax-opportunities
  subtopic: mkb_winstvrijstelling
  facts:
    - claim: "2026 MKB-winstvrijstelling is 12.7% of profit after ondernemersaftrek"
      source_lines: "L180"
      confidence: high
    - claim: "Rule type is Deterministic"
      source_lines: "L180"
      confidence: high

- id: 02-tax-opportunities
  subtopic: beperkt_aftrekbare_kosten
  facts:
    - claim: "2026 threshold is €5,700; IB alternative is 80%; VPB alternative is 73.5%"
      source_lines: "L181"
      confidence: high
    - claim: "Applies to meals, representation, gifts, conferences; rule type is Deterministic + classification"
      source_lines: "L181"
      confidence: high

- id: 02-tax-opportunities
  subtopic: vat_rates_and_compliance
  facts:
    - claim: "Essential. Official rates are 21%, 9%, 0%, exempt categories with different VAT deduction consequences"
      source_lines: "L170"
      confidence: high
    - claim: "System should detect: 21%, 9%, 0%, exempt, reverse-charge, mixed-rate invoices"
      source_lines: "L170"
      confidence: high
    - claim: "VAT invoice compliance requires: legal name/address, VAT ID, KVK, date, unique invoice number, supply date, amount excl. VAT, VAT rate/amount"
      source_lines: "L171"
      confidence: high

- id: 02-tax-opportunities
  subtopic: vat_correction_suppletie
  facts:
    - claim: "Corrections over €1,000 require a suppletie form; smaller corrections can be processed in next VAT return"
      source_lines: "L172"
      confidence: high

- id: 02-tax-opportunities
  subtopic: reverse_charge_foreign_vat
  facts:
    - claim: "Foreign entrepreneur transactions can trigger reverse-charge treatment (btw verlegd)"
      source_lines: "L173"
      confidence: high
    - claim: "Rule type is Deterministic + review; risk is High"
      source_lines: "L173"
      confidence: high

- id: 02-tax-opportunities
  subtopic: mixed_business_private_expenses
  facts:
    - claim: "VAT cannot be deducted for private use; if deducted initially, private-use VAT must be repaid"
      source_lines: "L182"
      confidence: high
    - claim: "Applies to phone, car, travel, home office, subscriptions, devices with private use; rule type is Heuristic + accountant review"
      source_lines: "L182"
      confidence: high

- id: 02-tax-opportunities
  subtopic: company_car_vat_private_use
  facts:
    - claim: "Belastingdienst gives rules for private-use VAT and forfaits (2.7% or 1.5%) where no private-use km administration exists"
      source_lines: "L183"
      confidence: high

- id: 02-tax-opportunities
  subtopic: wbso
  facts:
    - claim: "RVO states WBSO reduces R&D costs through tax credit and applies to future R&D projects"
      source_lines: "L184"
      confidence: high
    - claim: "System should detect: Candidate R&D projects, future-only applications, required project admin"
      source_lines: "L184"
      confidence: high
    - claim: "Risk is Very high; rule type is Heuristic + RVO/accountant review"
      source_lines: "L184"
      confidence: high

- id: 02-tax-opportunities
  subtopic: innovatiebox
  facts:
    - claim: "Belastingdienst describes innovatiebox conditions and 9% effective rate for qualifying innovation profits"
      source_lines: "L185"
      confidence: high
    - claim: "Applies to BV/VPB companies with qualifying IP/R&D; requires S&O statement and admin"
      source_lines: "L185"
      confidence: high

- id: 02-tax-opportunities
  subtopic: box_2_dividend_timing
  facts:
    - claim: "2026 Box 2 rates are 24.5% up to €68,843 and 31% above"
      source_lines: "L186"
      confidence: high
    - claim: "System should detect: Dividend amount split across brackets; partner allocation"
      source_lines: "L186"
      confidence: high

- id: 02-tax-opportunities
  subtopic: box_3_balance_timing
  facts:
    - claim: "2026 provisional percentages are 1.28% bank, 6% investments/other assets, 2.70% debts"
      source_lines: "L187"
      confidence: high
    - claim: "2026 tax-free allowance is €59,357 single and €118,714 with partner"
      source_lines: "L187"
      confidence: high

- id: 02-tax-opportunities
  subtopic: dga_excess_borrowing
  facts:
    - claim: "Belastingdienst says borrowing above €500,000 from own BV can be taxed as Box 2 income, with aggregation rules"
      source_lines: "L188, L161"
      confidence: high
    - claim: "System should detect: Debt near/over €500,000; connected persons; home-loan exceptions"
      source_lines: "L188"
      confidence: high
    - claim: "Risk is Very high; rule type is Deterministic + legal/accountant review"
      source_lines: "L188"
      confidence: high

- id: 02-tax-opportunities
  subtopic: bv_holding_versus_eenmanszaak
  facts:
    - claim: "Needs accountant/fiscalist. Public products discuss this as scenario-planning area, not DIY answer"
      source_lines: "L189"
      confidence: medium

## 03-architecture

- id: 03-architecture
  subtopic: deterministic_plus_llm_split
  facts:
    - claim: "Let LLM extract facts, classify transactions, propose tags; let deterministic code calculate VAT, KIA, KOR eligibility, deduction limits, Box thresholds, shareholder-loan thresholds"
      source_lines: "L139-140"
      confidence: high
    - claim: "Pattern appears in OpenAccountants conservative rules, Speedy AI classification paired with structured bookkeeping APIs, Dutch Claude Code writeup's insistence on Python/YAML verification scripts"
      source_lines: "L140"
      confidence: high

- id: 03-architecture
  subtopic: classified_assumed_needs_input_model
  facts:
    - claim: "OpenAccountants uses three-outcome transaction pattern: classify when clear, assume conservatively when needed, route ambiguous items to review"
      source_lines: "L142-143"
      confidence: high
    - claim: "This pattern is ideal for Dutch tax because private/business mixed expenses, VAT reverse charge, DGA items, home-office issues are high-risk"
      source_lines: "L143"
      confidence: high

- id: 03-architecture
  subtopic: read_only_first_connector
  facts:
    - claim: "Moneybird's official AI docs distinguish read-only from read-write; read-write excludes delete actions"
      source_lines: "L146"
      confidence: high
    - claim: "Production should start read-only, generate proposed journal entries/corrections, then require human approval before writeback"
      source_lines: "L146"
      confidence: high

- id: 03-architecture
  subtopic: receipt_extraction_pipeline
  facts:
    - claim: "Speedy extracts supplier, amounts, VAT, ledger suggestions from invoices and connects to bookkeeping actions"
      source_lines: "L149"
      confidence: high
    - claim: "LinkedIn VAT workflow pattern organizes quarter folders and asks model to extract amounts, VAT, categories, missing items, source references"
      source_lines: "L149"
      confidence: high

- id: 03-architecture
  subtopic: bank_feed_reconciliation_before_tax_reasoning
  facts:
    - claim: "Jortt publicly emphasizes automatic controls: bank balance versus bookkeeping, invoices linked to payments, VAT codes, opening/ending balances"
      source_lines: "L152"
      confidence: high
    - claim: "This should happen before tax-opportunity scanning"
      source_lines: "L152"
      confidence: high

- id: 03-architecture
  subtopic: tax_opportunity_scanner_not_autonomous_planner
  facts:
    - claim: "Strongest practical system should surface opportunities: KIA threshold nearly reached, KOR may be beneficial, hours evidence insufficient, DGA loan near excess-borrowing threshold, WBSO candidate"
      source_lines: "L155"
      confidence: high
    - claim: "Should not present aggressive positions as advice"
      source_lines: "L155"
      confidence: high

- id: 03-architecture
  subtopic: accountant_in_loop_exception_queue
  facts:
    - claim: "Boekie claims confidence thresholds and human escalation"
      source_lines: "L158"
      confidence: medium
    - claim: "Reddit workflow kept accountants for corporate tax, R&D credits, annual accounts"
      source_lines: "L158"
      confidence: medium
    - claim: "OpenAccountants generates working papers and flags reviewer judgment areas"
      source_lines: "L158"
      confidence: high

- id: 03-architecture
  subtopic: official_rule_grounding_versioned
  facts:
    - claim: "Official 2026 Dutch thresholds already differ from stale community examples: zelfstandigenaftrek €1,200, KIA thresholds start €2,901, excess-borrowing threshold €500,000 (vs 2023 €700,000)"
      source_lines: "L161"
      confidence: high

- id: 03-architecture
  subtopic: accountant_review_pack_generation
  facts:
    - claim: "OpenAccountants includes working-paper templates; Jortt has annual-close and IB reporting flows; Reddit workflow generated accountant-ready reports"
      source_lines: "L164"
      confidence: high
    - claim: "System should output: what changed, evidence, rule applied, uncertainty, questions"
      source_lines: "L164"
      confidence: high

- id: 03-architecture
  subtopic: ingestion_layer_objects
  facts:
    - claim: "Core ingestion objects: source_document, transaction, invoice, receipt, counterparty, bank_mutation, ledger_entry, vat_line, asset, loan, time_entry, tax_rule_version, human_review_item"
      source_lines: "L207-221"
      confidence: high
    - claim: "Every object should carry: source ID, file hash, connector name, import timestamp, tax year, confidence, reviewer, evidence links"
      source_lines: "L223"
      confidence: high

- id: 03-architecture
  subtopic: bookkeeping_normalization_layer
  facts:
    - claim: "Normalize everything to stable ledger schema before tax reasoning: Amount ex VAT, VAT amount, gross amount"
      source_lines: "L228-230"
      confidence: high
    - claim: "Include: VAT code, VAT rate, reverse-charge flag, exempt flag, counterparty country/VAT ID, ledger account, fiscal category, business/private allocation %, asset vs expense, related-party flag, evidence completeness"
      source_lines: "L230-236"
      confidence: high

- id: 03-architecture
  subtopic: deterministic_tax_engine_rules
  facts:
    - claim: "Implement as versioned code and YAML/JSON rules, not prompt text"
      source_lines: "L240"
      confidence: high
    - claim: "Must be deterministic: VAT rates, VAT return calculations, suppletie thresholds, KOR turnover, KIA threshold/tier, MKB-winstvrijstelling, zelfstandigenaftrek/startersaftrek, beperkt aftrekbare kosten, Box 2, Box 3, DGA excess-borrowing, reconciliation checks, audit totals"
      source_lines: "L242-253"
      confidence: high

- id: 03-architecture
  subtopic: llm_reasoning_layer_scope
  facts:
    - claim: "Use LLM for: OCR cleanup, invoice-field extraction, ledger-category suggestion, deductibility explanation drafts, needs-accountant detection, accountant-question generation, research against official sources, user-facing explanations"
      source_lines: "L259-268"
      confidence: high
    - claim: "Do not let LLM decide final eligibility, compute tax, invent thresholds, file returns"
      source_lines: "L270"
      confidence: high

- id: 03-architecture
  subtopic: exception_handling_queues
  facts:
    - claim: "Create explicit queues: Missing receipt, Missing invoice field, Low-confidence VAT treatment, Foreign supplier/customer, Mixed private/business use, Home-office claim, Vehicle/private-use issue, Asset purchase near KIA threshold, KOR decision, DGA/shareholder-loan, WBSO/innovatiebox candidate, Related-party/holding/BV transaction, Large manual journal entry, Mismatch bank/invoice/ledger"
      source_lines: "L274-289"
      confidence: high

- id: 03-architecture
  subtopic: evidence_logging_structure
  facts:
    - claim: "Each tax conclusion should produce: finding_id, tax_year, entity_id, tax_concept, input_records, rule_version, official_source_url, calculation_trace, llm_extraction_trace, confidence, review_status, reviewer_notes, final_action"
      source_lines: "L295-309"
      confidence: high
    - claim: "This makes system accountant-reviewable and defensible"
      source_lines: "L311"
      confidence: high

- id: 03-architecture
  subtopic: accountant_handoff_packs
  facts:
    - claim: "Generate four packs: 1) Quarterly VAT pack: VAT return totals, source invoices, reverse-charge list, missing receipts, correction candidates"
      source_lines: "L315-317"
      confidence: high
    - claim: "2) Annual IB/VPB pack: P&L, balance sheet, asset register, deductions, non-deductible expenses, private-use corrections"
      source_lines: "L318"
      confidence: high
    - claim: "3) Opportunity pack: KIA/KOR/hours/WBSO/Box/DGA warnings and missing data"
      source_lines: "L319"
      confidence: high
    - claim: "4) Questions pack: concise accountant questions with evidence links and model uncertainty"
      source_lines: "L320"
      confidence: high

- id: 03-architecture
  subtopic: mandatory_human_review_points
  facts:
    - claim: "Mandatory review before: Filing VAT/IB/VPB, Applying KOR, Claiming KIA for ambiguous assets, Claiming home-office/car/mixed expenses, Claiming WBSO/innovatiebox, BV/holding/DGA salary/dividend decisions, Moving money between BV/holding/DGA, Writing back ledger corrections above materiality threshold"
      source_lines: "L324-333"
      confidence: high

## 04-prompts

- id: 04-prompts
  subtopic: prompt_skeleton_general
  facts:
    - claim: "Prompt skeleton: You are classifying Dutch bookkeeping records for review, not giving final tax advice. Return only structured JSON. Use outcomes: classified, assumed_conservative, needs_user_input, needs_accountant_review. Never invent rates, thresholds, eligibility rules. If rule not supplied, mark needs_accountant_review. Attach evidence_ids for every conclusion."
      source_lines: "L350-357"
      confidence: high

- id: 04-prompts
  subtopic: transaction_classification_prompt
  facts:
    - claim: "For each transaction, decide: 1) likely ledger category, 2) VAT treatment candidate, 3) deductibility candidate, 4) business/private allocation candidate, 5) missing evidence, 6) exact question needed. Do not calculate final tax. Use deterministic engine outputs when present."
      source_lines: "L360-368"
      confidence: high

- id: 04-prompts
  subtopic: quarterly_opportunity_scan_prompt
  facts:
    - claim: "Scan for legal Dutch tax opportunities: VAT anomalies, KOR threshold/scenario, KIA threshold/timing, hours evidence for ondernemersaftrek, limited-deductible costs, missing receipts, mixed private/business expenses, foreign VAT/reverse-charge, DGA/shareholder-loan issues"
      source_lines: "L371-381"
      confidence: high
    - claim: "For each finding, return: evidence, rule_id, calculation_id, risk, recommended human reviewer"
      source_lines: "L381"
      confidence: high

- id: 04-prompts
  subtopic: workflow_patterns
  facts:
    - claim: "Expense categorization: Suggest ledger account, VAT code, business/private allocation, confidence. On every imported bank mutation or invoice. Inputs: Bank description, receipt/invoice OCR, supplier, amount, prior examples, chart of accounts. Failure modes: Supplier ambiguity, bundled purchases, private use, hallucinated category. Why: LLM handles messy descriptions; deterministic validator checks VAT/account validity"
      source_lines: "L339"
      confidence: high
    - claim: "Deductible/non-deductible classification: Flag fully deductible, limited deductible, non-deductible, mixed, or review. After category suggestion. Failure modes: Meals/representation/home-office/car mistakes. Works if output is only proposal and limited-deduction rules are deterministic"
      source_lines: "L340"
      confidence: high
    - claim: "VAT review: Verify VAT rate, input VAT, reverse charge, exempt/0%, invoice requirements. Before VAT return. Works because Belastingdienst requirements are checklist-friendly; LLM finds anomalies"
      source_lines: "L341"
      confidence: high
    - claim: "Missing-receipt detection: Identify paid expenses lacking evidence. Weekly and quarter-end. Reconciliation is deterministic; LLM helps match messy vendor names"
      source_lines: "L342"
      confidence: high
    - claim: "End-of-quarter tax opportunity scan: Surface near-term actions before quarter close. Monthly and 2 weeks before quarter-end. Deterministic calculators identify thresholds; LLM explains tradeoffs and asks questions"
      source_lines: "L343"
      confidence: high
    - claim: "Annual close review: Produce accountant-ready close pack. After year-end, before accountant review. Combines Jortt-style controls with OpenAccountants-style working paper"
      source_lines: "L344"
      confidence: high
    - claim: "Accountant question generation: Convert uncertainty into concise review questions. Whenever review queue has material items. Structured questions reduce accountant time and preserve audit context"
      source_lines: "L345"
      confidence: high
    - claim: "DGA / BV edge-case detection: Detect shareholder-loan, dividend, holding, WBSO/innovatiebox, related-party issues. Monthly for BV/holding users; before dividend/loan actions. LLM detects patterns; deterministic thresholds and mandatory accountant review prevent overreach"
      source_lines: "L346"
      confidence: high

## 05-rules-2026

- id: 05-rules-2026
  subtopic: vat_rates
  facts:
    - claim: "Official rates are 21%, 9%, 0%, and exempt categories with different VAT deduction consequences"
      source_lines: "L170"
      confidence: high

- id: 05-rules-2026
  subtopic: kia_2026
  facts:
    - claim: "2026 KIA applies from €2,901 to €398,236 with tiered percentages/amounts"
      source_lines: "L175"
      confidence: high

- id: 05-rules-2026
  subtopic: kor_2026
  facts:
    - claim: "KOR applies at ≤ €20,000 turnover"
      source_lines: "L174"
      confidence: high

- id: 05-rules-2026
  subtopic: zelfstandigenaftrek_2026
  facts:
    - claim: "2026 zelfstandigenaftrek is €1,200 under listed conditions"
      source_lines: "L178"
      confidence: high

- id: 05-rules-2026
  subtopic: startersaftrek_2026
  facts:
    - claim: "2026 startersaftrek is €2,123 when conditions are met"
      source_lines: "L179"
      confidence: high

- id: 05-rules-2026
  subtopic: mkb_winstvrijstelling_2026
  facts:
    - claim: "2026 MKB-winstvrijstelling is 12.7% of profit after ondernemersaftrek"
      source_lines: "L180"
      confidence: high

- id: 05-rules-2026
  subtopic: beperkt_aftrekbare_kosten_2026
  facts:
    - claim: "2026 threshold is €5,700; IB alternative is 80%; VPB alternative is 73.5%"
      source_lines: "L181"
      confidence: high

- id: 05-rules-2026
  subtopic: box_2_2026
  facts:
    - claim: "2026 Box 2 rates are 24.5% up to €68,843 and 31% above"
      source_lines: "L186"
      confidence: high

- id: 05-rules-2026
  subtopic: box_3_2026
  facts:
    - claim: "2026 provisional percentages are 1.28% bank, 6% investments/other assets, 2.70% debts"
      source_lines: "L187"
      confidence: high
    - claim: "2026 tax-free allowance is €59,357 single and €118,714 with partner"
      source_lines: "L187"
      confidence: high

- id: 05-rules-2026
  subtopic: dga_excess_borrowing_threshold_2026
  facts:
    - claim: "Borrowing above €500,000 from own BV can be taxed as Box 2 income (changed from €700,000 in 2023)"
      source_lines: "L161, L188"
      confidence: high

- id: 05-rules-2026
  subtopic: urencriterium_threshold
  facts:
    - claim: "At least 1,225 hours required; generally more time in business than other work, with evidence"
      source_lines: "L177"
      confidence: high

## 06-build-vs-buy

- id: 06-build-vs-buy
  subtopic: easy_to_reuse_now
  facts:
    - claim: "Moneybird MCP/API access for live bookkeeping data"
      source_lines: "L388"
      confidence: high
    - claim: "Speedy e-Boekhouden's OCR/classification architecture for e-Boekhouden users"
      source_lines: "L389"
      confidence: high
    - claim: "OpenAccountants Netherlands skill structure, conservative-default pattern, refusal catalog, working-paper template"
      source_lines: "L390"
      confidence: high
    - claim: "e-Boekhouden, Exact, Moneybird SDK/wrapper patterns for ingestion"
      source_lines: "L391"
      confidence: high
    - claim: "Generic Claude/LLM finance workflow patterns: skills, review tabs, human checks, quarterly folder workflows"
      source_lines: "L392"
      confidence: high

- id: 06-build-vs-buy
  subtopic: moderate_custom_build_needed
  facts:
    - claim: "A verified 2026 Dutch tax rule pack with official-source URLs and yearly versioning"
      source_lines: "L396"
      confidence: high
    - claim: "Deterministic calculators for KOR, KIA, ondernemersaftrek, MKB-winstvrijstelling, VAT corrections, Box 2, Box 3, limited deductions, DGA excess borrowing"
      source_lines: "L397"
      confidence: high
    - claim: "Chart-of-accounts mapping across Moneybird, e-Boekhouden, Exact"
      source_lines: "L398"
      confidence: high
    - claim: "Source-evidence store with document hashes, invoice-field validation, audit trails"
      source_lines: "L399"
      confidence: high
    - claim: "Tax-opportunity scanner UI"
      source_lines: "L400"
      confidence: high
    - claim: "Accountant review workflow and export packs"
      source_lines: "L401"
      confidence: high
    - claim: "Entity-aware handling for eenmanszaak versus BV/holding"
      source_lines: "L402"
      confidence: high
    - claim: "Regression tests from anonymized bookkeeping scenarios"
      source_lines: "L403"
      confidence: high

- id: 06-build-vs-buy
  subtopic: hard_proprietary_logic_needing_custom_build
  facts:
    - claim: "BV/holding/DGA optimization across salary, dividends, shareholder loans, intercompany accounts, VPB, Box 2, personal liquidity"
      source_lines: "L407"
      confidence: high
    - claim: "WBSO/innovatiebox eligibility and project-administration workflows"
      source_lines: "L408"
      confidence: high
    - claim: "Legal-form conversion modeling: ZZP/eenmanszaak to BV/holding"
      source_lines: "L409"
      confidence: high
    - claim: "Cross-border VAT treatment for complex services, platforms, OSS/IOSS, foreign permanent-establishment"
      source_lines: "L410"
      confidence: high
    - claim: "Fully accountant-grade risk scoring"
      source_lines: "L411"
      confidence: high
    - claim: "Official e-filing flows"
      source_lines: "L412"
      confidence: high
    - claim: "Continuous tax-law update monitoring and change-impact testing"
      source_lines: "L413"
      confidence: high

- id: 06-build-vs-buy
  subtopic: practical_stack_recommendation
  facts:
    - claim: "Ledger connector: Use Moneybird MCP/API where possible; Speedy e-Boekhouden as reference for e-Boekhouden users; Exact Online APIs or CData read-only MCP for Exact"
      source_lines: "L421-422"
      confidence: high
    - claim: "Core backend: Python or TypeScript service with Postgres evidence store, deterministic tax engine, rule-version tables, job queue, structured JSON outputs. Speedy's Go/React/Postgres/Redis architecture is good reference"
      source_lines: "L424-425"
      confidence: high
    - claim: "Rule system: Start from OpenAccountants Netherlands skill for structure only; replace all live values with official 2026 sources and accountant-reviewed tests"
      source_lines: "L427-428"
      confidence: high
    - claim: "Prompting strategy: LLM for extraction, categorization, anomaly detection, question generation. Force JSON output with classified/assumed_conservative/needs_user_input/needs_accountant_review. Require evidence IDs and ban invented thresholds"
      source_lines: "L430-431"
      confidence: high

- id: 06-build-vs-buy
  subtopic: what_must_remain_deterministic
  facts:
    - claim: "VAT calculations, invoice requirements, KOR threshold logic, KIA tiers, zelfstandigenaftrek/startersaftrek/MKB calculations, limited-deduction thresholds, Box 2/Box 3 calculations, DGA excess-borrowing thresholds, reconciliation checks, all final numbers"
      source_lines: "L433-434"
      confidence: high

- id: 06-build-vs-buy
  subtopic: what_should_never_be_left_to_llm
  facts:
    - claim: "Filing VAT/IB/VPB, WBSO/innovatiebox claims, BV/holding restructuring, DGA salary/dividend/loan decisions, private-use corrections, home-office deductions, cross-border VAT, legal-form changes, aggressive optimization positions"
      source_lines: "L436-437"
      confidence: high

- id: 06-build-vs-buy
  subtopic: defensible_product_wedge_mvp
  facts:
    - claim: "1) Start with Moneybird or e-Boekhouden ingestion"
      source_lines: "L441"
      confidence: high
    - claim: "2) Build receipt matching + VAT review + missing evidence"
      source_lines: "L442"
      confidence: high
    - claim: "3) Add quarterly opportunity scanner: KOR, KIA, hours, VAT anomalies, limited deductions"
      source_lines: "L443"
      confidence: high
    - claim: "4) Add annual close accountant pack"
      source_lines: "L444"
      confidence: high
    - claim: "5) Add BV/DGA module only after IB/ZZP module is stable and reviewed by Dutch accountant/fiscalist"
      source_lines: "L445"
      confidence: high

## 07-risks-sources

- id: 07-risks-sources
  subtopic: belastingdienst_audit_posture
  facts:
    - claim: "System should treat Belastingdienst as highest trust official source for all 2026 rates and rules"
      source_lines: "L449"
      confidence: high
    - claim: "All Belastingdienst sources listed in table L473-483 have High trust level"
      source_lines: "L449"
      confidence: high

- id: 07-risks-sources
  subtopic: open_source_skill_reliability
  facts:
    - claim: "OpenAccountants Netherlands skill is explicitly Medium-low reliability; Q3 / AI-drafted / not independently verified"
      source_lines: "L23, L452"
      confidence: high
    - claim: "Project warns about hallucination, changing law, uneven coverage"
      source_lines: "L23"
      confidence: high
    - claim: "Contains stale 2025 values; needs 2026 verification"
      source_lines: "L452"
      confidence: high

- id: 07-risks-sources
  subtopic: speedy_eboekhouden_maturity
  facts:
    - claim: "Speedy e-Boekhouden is explicitly young, v1.3.1 released Apr. 8, 2026, labels self use at own risk"
      source_lines: "L33"
      confidence: high
    - claim: "Medium for architecture reuse, low-medium for maturity"
      source_lines: "L33"
      confidence: high

- id: 07-risks-sources
  subtopic: commercial_products_transparency
  facts:
    - claim: "Jortt, Paperdork, Boekie AI, BTW Vriend, Fiscaal Agent: most implementation details and tax logic are closed or marketing-level"
      source_lines: "L11"
      confidence: high
    - claim: "Paperdork, Boekie AI, BTW Vriend, Fiscaal Agent all have Medium-low or Low-medium trust levels due to marketing-level claims"
      source_lines: "L450-469"
      confidence: high

- id: 07-risks-sources
  subtopic: reddit_anecdote_reliability
  facts:
    - claim: "Dutch Claude Code automated accounting workflow is anecdotal; no repo, no tests, no public code, no independently verifiable result"
      source_lines: "L53-54"
      confidence: high
    - claim: "Claims should be treated as design evidence, not product evidence"
      source_lines: "L54"
      confidence: low

