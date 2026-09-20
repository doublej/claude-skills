# note3.md Structured Outline

## 01-existing-tools

```yaml
- id: 01-existing-tools
  subtopic: claude-did-my-taxes-architecture
  facts:
    - claim: "Claude Code workflow for Dutch BV entities with holding structures, WBSO, Innovatiebox, shareholder loan accounts"
      source_offset: "C1200-1400"
      confidence: high
    - claim: "System ingests bank API transactions, scrapes email receipts, executes matching algorithms, calculates VAT, generates quarterly reports for Belastingdienst"
      source_offset: "C1440-1700"
      confidence: high
    - claim: "Uses deterministic Python code for math; LLM reserved for semantic expense categorization"
      source_offset: "C1880-2050"
      confidence: high
    - claim: "Maintains localized knowledge base of Dutch tax strategies, flags edge cases for accountant review"
      source_offset: "C1750-1880"
      confidence: high
    - claim: "Saves thousands of euros through proactive diligence"
      source_offset: "C1750-1800"
      confidence: medium

- id: 01-existing-tools
  subtopic: moneybird-mcp-server
  facts:
    - claim: "Repository: moneybird-mcp-server (by vanderheijden86 and Klavis-AI)"
      source_offset: "C2200-2300"
      confidence: high
    - claim: "Exposes Moneybird API via Model Context Protocol, allows AI to list contacts, retrieve sales invoices, check accounts, access product/project data, make custom API requests"
      source_offset: "C2350-2650"
      confidence: high
    - claim: "Provides essential read/write access for data extraction and categorized entry injection"
      source_offset: "C2700-2800"
      confidence: high
    - claim: "Relies on official Moneybird REST API schemas and OpenAPI specs; high reliability for data extraction"
      source_offset: "C2850-2950"
      confidence: high
    - claim: "Does not natively comprehend Dutch tax rules or autonomous categorization without explicit agent prompting"
      source_offset: "C3000-3150"
      confidence: medium

- id: 01-existing-tools
  subtopic: agents-md-skill-md-modularity
  facts:
    - claim: "Claude Skills Architecture documented by Lovely Mcinerney and Solmaz.io"
      source_offset: "C3250-3380"
      confidence: high
    - claim: "Outlines modular directory structure (.claude/skills/) using SKILL.md files and AGENTS.md paradigm"
      source_offset: "C3420-3550"
      confidence: high
    - claim: "Prevents LLM hallucination by loading domain-specific instructions only when triggered"
      source_offset: "C3600-3750"
      confidence: high
    - claim: "Can create compartmentalized skills like dutch-vat-checker, dga-salary-compliance, kia-investment-tracker"
      source_offset: "C3900-4100"
      confidence: high
    - claim: "Forces LLM to rely on constrained, injected context files rather than base-model training data, reducing US/UK tax logic misapplication"
      source_offset: "C4100-4300"
      confidence: high

- id: 01-existing-tools
  subtopic: dutch-income-tax-optimizer
  facts:
    - claim: "Repository: income-tax-optimizer (by Sikerdebaard)"
      source_offset: "C4550-4650"
      confidence: high
    - claim: "Dedicated to Dutch Box 1 and Box 3 income tax optimization"
      source_offset: "C4700-4800"
      confidence: high
    - claim: "Uses gradient descent and random permutations to optimize asset/income division between fiscal partners to minimize tax liability"
      source_offset: "C4900-5150"
      confidence: high
    - claim: "Author notes algorithm may find local minima rather than global minima, requires parameter updates for annual bracket changes"
      source_offset: "C5300-5500"
      confidence: high
    - claim: "Raw algorithmic script not integrated to ledger; requires manual parameter input"
      source_offset: "C5550-5650"
      confidence: medium

- id: 01-existing-tools
  subtopic: exact-online-mcp-server
  facts:
    - claim: "Repository: exact-online-mcp-server-by-cdata (by CDataSoftware)"
      source_offset: "C5800-5950"
      confidence: high
    - claim: "Wraps CData JDBC driver to allow LLMs to query Exact Online using natural language, translating to SQL"
      source_offset: "C6000-6200"
      confidence: high
    - claim: "Open-source version is strictly read-only; cannot post journal entries, update ledgers, or create invoices"
      source_offset: "C6450-6650"
      confidence: high
    - claim: "High reliability for querying/data extraction; supported by commercial data connectivity provider"
      source_offset: "C6350-6450"
      confidence: high

- id: 01-existing-tools
  subtopic: xtroverso-year-end-framework
  facts:
    - claim: "XTROVERSO Dutch Year-End Tax Risk Checklist for Small Business"
      source_offset: "C6800-6900"
      confidence: high
    - claim: "Professional-grade procedural checklist covering ZZP and DGA structures"
      source_offset: "C6950-7050"
      confidence: high
    - claim: "Covers WKR free space, mixed-use asset depreciation, company car VAT adjustments, iXBRL filing mandates for 2026"
      source_offset: "C7100-7350"
      confidence: high
    - claim: "Sourced from specialized Dutch business clinic focused on transition and reconstruction"
      source_offset: "C7550-7650"
      confidence: medium
    - claim: "Prevents standard Belastingdienst corrections, mitigates fines, ensures all final allowable deductions captured before fiscal window closes"
      source_offset: "C7400-7550"
      confidence: medium

- id: 01-existing-tools
  subtopic: referentie-grootboekschema-rgs
  facts:
    - claim: "Referentie Grootboekschema (RGS) is universal chart of accounts taxonomy used by Belastingdienst and CBS"
      source_offset: "C10100-10300"
      confidence: high
    - claim: "Standard document available via 1truth.nl"
      source_offset: "C36500-36700"
      confidence: high
```

## 02-tax-opportunities

```yaml
- id: 02-tax-opportunities
  subtopic: kia-small-scale-investment-deduction
  facts:
    - claim: "KIA target entities: ZZP, VOF, BV"
      source_offset: "C9100-9200"
      confidence: high
    - claim: "KIA 2026: investment €2,901 to €71,683 → 28% deduction"
      source_offset: "C13150-13350"
      confidence: high
    - claim: "If investments > €71,684, apply fixed €20,072 deduction, tapering off thereafter"
      source_offset: "C13350-13550"
      confidence: high
    - claim: "Detection: summation of qualifying asset purchases with individual value > €450 within fiscal year"
      source_offset: "C9350-9500"
      confidence: high
    - claim: "Low calculation risk, moderate classification risk (must exclude goodwill, passenger cars)"
      source_offset: "C13650-13800"
      confidence: high
    - claim: "End-of-Q4 tax opportunity scan should check: sum all capital assets exceeding €450, evaluate if cumulative total approaching €2,901 threshold"
      source_offset: "C23100-23350"
      confidence: high

- id: 02-tax-opportunities
  subtopic: mkb-winstvrijstelling-sme-profit-exemption
  facts:
    - claim: "MKB-winstvrijstelling target entities: ZZP, VOF, Eenmanszaak"
      source_offset: "C14000-14150"
      confidence: high
    - claim: "Automatically deduct 12.7% of remaining profit to arrive at final taxable income"
      source_offset: "C14300-14450"
      confidence: high
    - claim: "Zero risk; purely mathematical execution"
      source_offset: "C14500-14600"
      confidence: high
    - claim: "Applies after zelfstandigenaftrek and startersaftrek deductions"
      source_offset: "C14150-14300"
      confidence: high

- id: 02-tax-opportunities
  subtopic: zelfstandigenaftrek-startersaftrek
  facts:
    - claim: "Zelfstandigenaftrek 2026: €1,200 annual allowance if urencriterium met (>= 1,225 hours annually)"
      source_offset: "C14800-15000"
      confidence: high
    - claim: "Startersaftrek 2026: additional €2,123 if within first 3 years of business"
      source_offset: "C15050-15200"
      confidence: high
    - claim: "Requires time-tracking logs and KVK registration date evidence"
      source_offset: "C14700-14800"
      confidence: high
    - claim: "Moderate risk: AI must intelligently defend inclusion of non-billable hours during audit"
      source_offset: "C15250-15450"
      confidence: medium

- id: 02-tax-opportunities
  subtopic: innovatiebox-wbso
  facts:
    - claim: "Innovatiebox/WBSO target entities: BV, VPB Entities"
      source_offset: "C15550-15700"
      confidence: high
    - claim: "Identifies software development/engineering expenses linked to approved R&D project"
      source_offset: "C15800-15950"
      confidence: high
    - claim: "If WBSO declaration active, prepare allocation proposal to attribute profits to IP, triggering 9% effective corporate tax rate"
      source_offset: "C16050-16300"
      confidence: high
    - claim: "High risk of misclassification; strict accountant review mandatory"
      source_offset: "C16350-16500"
      confidence: medium

- id: 02-tax-opportunities
  subtopic: excessief-lenen-excess-borrowing
  facts:
    - claim: "Excess Borrowing target entity: DGA (Director/Shareholder)"
      source_offset: "C16650-16800"
      confidence: high
    - claim: "If total debt exceeds €500,000 (excluding qualifying mortgages), excess taxed as Box 2 fictitious dividend"
      source_offset: "C17050-17300"
      confidence: high
    - claim: "Detection: continuous monitoring of total DGA debt and connected persons to BV"
      source_offset: "C16900-17050"
      confidence: high
    - claim: "Low calculation risk; system must generate urgent alert if balance nears €500,000 threshold before year-end"
      source_offset: "C17350-17550"
      confidence: high

- id: 02-tax-opportunities
  subtopic: representatiekosten-representation-costs
  facts:
    - claim: "Representatiekosten 2026: €5,700 non-deductible threshold OR deduct 80% of costs (income tax) / 73.5% (VPB), select most favorable"
      source_offset: "C17800-18050"
      confidence: high
    - claim: "All entities can claim; aggregate mixed-use promotional and relational expenses"
      source_offset: "C17650-17800"
      confidence: high
    - claim: "Moderate risk: AI must accurately distinguish between pure private expenses and valid representation costs"
      source_offset: "C18100-18300"
      confidence: medium

- id: 02-tax-opportunities
  subtopic: wkr-work-related-costs-scheme
  facts:
    - claim: "WKR applies to employers and DGA holdings"
      source_offset: "C18400-18550"
      confidence: high
    - claim: "Free space 2026: 2.00% on first €400,000 of wage sum; 1.18% above that"
      source_offset: "C18750-18950"
      confidence: high
    - claim: "Exceeding space triggers 80% final levy; system must halt non-essential allowances if approaching limit"
      source_offset: "C19000-19200"
      confidence: high
    - claim: "Data required: fiscal wage sum, general ledger for employee benefits and untaxed allowances"
      source_offset: "C18550-18750"
      confidence: high

- id: 02-tax-opportunities
  subtopic: vat-mixed-use-assets-company-cars
  facts:
    - claim: "Applies to all entities using assets for both business and private purposes"
      source_offset: "C19300-19450"
      confidence: high
    - claim: "Requires asset registry, mileage logs, private-use declarations"
      source_offset: "C19450-19600"
      confidence: high
    - claim: "Must calculate mandatory VAT correction for private use in final VAT return of year"
      source_offset: "C19700-19900"
      confidence: high
    - claim: "High risk; requires accurate mileage logs or application of standard Belastingdienst percentage correction"
      source_offset: "C19950-20150"
      confidence: medium
    - claim: "Belastingdienst rule: BTW on food/drink consumed on-premises NOT deductible as input tax"
      source_offset: "C22100-22350"
      confidence: high
```

## 03-architecture

```yaml
- id: 03-architecture
  subtopic: deterministic-calculator-llm-classifier-split
  facts:
    - claim: "Most critical failure mode: arithmetic hallucination and misapplication of multi-step tax formulas"
      source_offset: "C8550-8750"
      confidence: high
    - claim: "Solution: strictly separate semantic duties from mathematical duties"
      source_offset: "C8800-8900"
      confidence: high
    - claim: "LLM functions exclusively as semantic classifier; deterministic Python engine performs all calculations"
      source_offset: "C8950-9100"
      confidence: high
    - claim: "Python script contains hardcoded, verified 2026 tax tables (e.g., 35.75% Box 1 Bracket 1 rate, 21% VAT)"
      source_offset: "C9200-9400"
      confidence: high
    - claim: "Python applies 12.7% MKB-winstvrijstelling and returns mathematically infallible tax liability"
      source_offset: "C9400-9550"
      confidence: high

- id: 03-architecture
  subtopic: accountant-in-loop-exception-detection
  facts:
    - claim: "Systems employ 'Ask Accountant' extraction and quarantine workflow for ambiguous tax scenarios"
      source_offset: "C9750-9900"
      confidence: high
    - claim: "When LLM confidence drops below threshold, transaction quarantined; system does not guess"
      source_offset: "C9950-10100"
      confidence: high
    - claim: "Example: determining precise private-use percentage of mixed-use asset triggers quarantine"
      source_offset: "C10050-10200"
      confidence: high
    - claim: "At month-end, system generates formatted dossier with transaction details, OCR receipt, technical question for accountant"
      source_offset: "C10200-10450"
      confidence: high
    - claim: "Ensures legal ambiguities resolved by certified professionals while AI handles bulk routine processing"
      source_offset: "C10450-10600"
      confidence: high

- id: 03-architecture
  subtopic: rgs-normalization-standardized-bookkeeping
  facts:
    - claim: "Ledger data must be normalized via Referentie Grootboekschema (RGS), universal chart of accounts"
      source_offset: "C10650-10850"
      confidence: high
    - claim: "Standard used by both Belastingdienst and CBS"
      source_offset: "C10750-10850"
      confidence: high
    - claim: "AI agent maps proprietary user-generated ledger accounts to RGS taxonomy upon ingestion"
      source_offset: "C10900-11050"
      confidence: high
    - claim: "Deterministic tax engine queries specific RGS codes independent of user's idiosyncratic naming conventions"
      source_offset: "C11100-11300"
      confidence: high

- id: 03-architecture
  subtopic: continuous-auditing-tax-opportunity-scanners
  facts:
    - claim: "Cron-triggered batch processing performs continuous auditing; inverts traditional retroactive accounting"
      source_offset: "C11450-11650"
      confidence: high
    - claim: "End of each quarter: optimization agent scans cumulative ledger account totals"
      source_offset: "C11700-11850"
      confidence: high
    - claim: "Example: if business accumulated €2,500 in KIA-qualifying investments by November, system generates alert that additional €401 before Dec 31 triggers 28% deduction"
      source_offset: "C11950-12250"
      confidence: high

- id: 03-architecture
  subtopic: retrieval-augmented-generation-rag
  facts:
    - claim: "Maintains localized, curated knowledge base with latest Belastingdienst PDFs, tax treaties, KVK regulations"
      source_offset: "C12500-12700"
      confidence: high
    - claim: "LLM uses RAG instead of base training weights to answer complex strategy questions"
      source_offset: "C12750-12900"
      confidence: high
    - claim: "Tax regulations update annually with Prinsjesdag announcements"
      source_offset: "C12400-12500"
      confidence: high
    - claim: "RAG approach sharply reduces risk of outdated or jurisdictionally incorrect advice"
      source_offset: "C12950-13100"
      confidence: high

- id: 03-architecture
  subtopic: evidentiary-continuity-receipt-extraction
  facts:
    - claim: "Belastingdienst mandates business records retention minimum 7 years; burden of proof on entrepreneur"
      source_offset: "C13250-13450"
      confidence: high
    - claim: "Automated extraction pipeline: scrape designated email inboxes, extract PDF/image attachments"
      source_offset: "C13500-13700"
      confidence: high
    - claim: "Vision model (Claude 3.5 Sonnet) processes document via OCR, extracting line items, dates, VAT amounts"
      source_offset: "C13750-13950"
      confidence: high
    - claim: "System creates cryptographic/database link between receipt, bank transaction, and applied tax rule"
      source_offset: "C14000-14200"
      confidence: high
    - claim: "Ensures every ledger entry perpetually defensible during tax audit"
      source_offset: "C14200-14350"
      confidence: high

- id: 03-architecture
  subtopic: build-blueprint-multi-agent-pipeline
  facts:
    - claim: "Data Inputs/Ingestion Layer: bank feeds via API (JSON), receipt extraction via email scraping/cloud storage"
      source_offset: "C20600-20900"
      confidence: high
    - claim: "MCP Server connected to core accounting platform (Moneybird/Exact Online) for bidirectional ledger interface"
      source_offset: "C20950-21200"
      confidence: high
    - claim: "Bookkeeping Normalization Layer: AI immediately maps extracted metadata to Dutch RGS"
      source_offset: "C21250-21500"
      confidence: high
    - claim: "LLM Reasoning/Classification Layer: semantic matching of transactions to receipts, VAT review, agentic judgment on deductibility"
      source_offset: "C21600-21900"
      confidence: high
    - claim: "Deterministic Tax Engine: data passed as structured JSON to local Python environment with modular scripts (calculate_kia.py, check_excessief_lenen.py, calculate_wkr_space.py)"
      source_offset: "C22000-22300"
      confidence: high
    - claim: "Exception Handling: items below LLM confidence threshold routed to Exception Queue; every action logged with cryptographic linkage"
      source_offset: "C22400-22650"
      confidence: high
    - claim: "Accountant Handoff: Exception Queue compiled into Accountant Review Pack; year-end generates iXBRL-ready export for human signature and KVK deposit"
      source_offset: "C22700-23050"
      confidence: high

- id: 03-architecture
  subtopic: expense-categorization-pipeline-prompt
  facts:
    - claim: "Daily trigger upon ingestion of new bank feeds and email receipts"
      source_offset: "C23500-23650"
      confidence: high
    - claim: "Inputs: raw bank transaction description, OCR-extracted receipt text, historical vendor categorization list, user business entity type (ZZP vs BV)"
      source_offset: "C23700-23950"
      confidence: high
    - claim: "Prompt enforces chain-of-thought: map to RGS code, evaluate deductibility, extract exact VAT/rate"
      source_offset: "C24050-24300"
      confidence: high
    - claim: "Prompt explicitly includes Belastingdienst rule: BTW on food/drink consumed on-premises NOT deductible as input tax; classify under representatiekosten"
      source_offset: "C24400-24700"
      confidence: high
    - claim: "Output strictly as JSON object matching provided schema"
      source_offset: "C24750-24900"
      confidence: high

- id: 03-architecture
  subtopic: end-of-quarter-opportunity-scan-prompt
  facts:
    - claim: "Runs automatically Oct 1 and monthly thereafter until Dec 31"
      source_offset: "C25150-25300"
      confidence: high
    - claim: "Inputs: YTD trial balance mapped to RGS, active asset registry, DGA current account balance"
      source_offset: "C25300-25550"
      confidence: high
    - claim: "Prompt executes: KIA check (sum assets > €450, approaching €2,901?); Excess Borrowing check (DGA balance > €450,000?); WKR Free Space calculation"
      source_offset: "C25650-26000"
      confidence: high
    - claim: "Generates actionable executive summary of tax-saving recommendations"
      source_offset: "C26050-26200"
      confidence: high

- id: 03-architecture
  subtopic: accountant-question-generation-prompt
  facts:
    - claim: "Runs prior to quarterly BTW filing deadline or during annual close"
      source_offset: "C26450-26650"
      confidence: high
    - claim: "Formats algorithmic anomalies into professional, actionable accountant queries"
      source_offset: "C26350-26450"
      confidence: high
    - claim: "For each quarantined item: provide date, vendor, exact amount, proposed fiscal treatment, specific uncertainty"
      source_offset: "C26850-27100"
      confidence: high
    - claim: "Explicitly request accountant binding legal determination; do not invent rules or estimate percentages"
      source_offset: "C27100-27300"
      confidence: high

- id: 03-architecture
  subtopic: recommended-implementation-stack
  facts:
    - claim: "Reasoning/Agent Environment: Claude 3.5 Sonnet via Claude Desktop or LangGraph"
      source_offset: "C27900-28100"
      confidence: high
    - claim: "Instruction Architecture: Adopt open AGENTS.md paradigm with compartmentalized instruction sets for specific domains"
      source_offset: "C28150-28400"
      confidence: high
    - claim: "Store official 2026 Belastingdienst rules as markdown files in agent reference directory"
      source_offset: "C28400-28600"
      confidence: high
    - claim: "Connectivity Layer: Deploy moneybird-mcp-server locally for standardized authenticated interface"
      source_offset: "C28700-28900"
      confidence: high
    - claim: "Mathematical Core: Construct Local Python Execution Environment; absolute imperative that LLM never calculates final VAT or KIA deductions"
      source_offset: "C29000-29300"
      confidence: high
    - claim: "LLM extracts raw numerical data, passes as structured arguments to Python scripts; script applies deterministic math, returns exact liability"
      source_offset: "C29300-29550"
      confidence: high
    - claim: "Governance Protocol: Strict Accountant-in-loop for year-end reporting and ambiguous categorizations; optimize for cleanest possible trial balance"
      source_offset: "C29600-29850"
      confidence: high
```

## 04-prompts

```yaml
- id: 04-prompts
  subtopic: expense-categorization-deductibility
  facts:
    - claim: "Prompt pattern: enforce chain-of-thought reasoning for Dutch tax accountant persona"
      source_offset: "C24000-24100"
      confidence: high
    - claim: "First: map expense to RGS standard code"
      source_offset: "C24150-24250"
      confidence: high
    - claim: "Second: evaluate deductibility (fully/partially/non-deductible)"
      source_offset: "C24250-24400"
      confidence: high
    - claim: "Third: extract exact VAT and applied rate"
      source_offset: "C24400-24500"
      confidence: high
    - claim: "Critical inclusion: Belastingdienst rule on restaurant/food VAT non-deductibility"
      source_offset: "C24600-24800"
      confidence: high
    - claim: "Output schema: strict JSON object matching provided format"
      source_offset: "C24800-24950"
      confidence: high

- id: 04-prompts
  subtopic: quarterly-opportunity-scan
  facts:
    - claim: "Prompt frames system as 'automated fiscal strategist'"
      source_offset: "C25500-25650"
      confidence: high
    - claim: "Three continuous auditing checks: KIA check, Excess Borrowing check, WKR Free Space calculation"
      source_offset: "C25700-26050"
      confidence: high
    - claim: "KIA check specifics: sum all capital assets > €450, approaching €2,901 threshold?"
      source_offset: "C25800-26000"
      confidence: high
    - claim: "Excess Borrowing check: DGA current account balance exceeding €450,000?"
      source_offset: "C26000-26150"
      confidence: high
    - claim: "WKR calculation: 2.00% on first €400,000 of fiscal wage sum"
      source_offset: "C26150-26300"
      confidence: high
    - claim: "Formulate actionable executive summary advising on optimal capital deployment before Dec 31"
      source_offset: "C26350-26500"
      confidence: high

- id: 04-prompts
  subtopic: accountant-handoff-question-generation
  facts:
    - claim: "Purpose: format anomalies into professional accountant queries"
      source_offset: "C26350-26500"
      confidence: high
    - claim: "Runs prior to quarterly BTW filing or annual close"
      source_offset: "C26550-26700"
      confidence: high
    - claim: "For each quarantined item, draft formal communication to certified accountant"
      source_offset: "C26750-26950"
      confidence: high
    - claim: "Include: date, vendor, exact amount, proposed fiscal treatment, specific uncertainty under Dutch law"
      source_offset: "C26950-27200"
      confidence: high
    - claim: "Do not invent rules or estimate percentages; explicitly request accountant binding determination"
      source_offset: "C27200-27400"
      confidence: high

- id: 04-prompts
  subtopic: year-end-ixbrl-prep
  facts:
    - claim: "At year-end, system generates iXBRL-ready export file requiring human signature and KVK deposit"
      source_offset: "C22800-23050"
      confidence: high
    - claim: "Year-end checklist covers iXBRL filing mandates for 2026"
      source_offset: "C7200-7350"
      confidence: high
```

## 05-rules-2026

```yaml
- id: 05-rules-2026
  subtopic: vat-rates-btw
  facts:
    - claim: "Dutch VAT rates: 0%, 9%, 21% standard"
      source_offset: "C22050-22150"
      confidence: high
    - claim: "Deterministic engine contains hardcoded 21% standard VAT rate"
      source_offset: "C9250-9350"
      confidence: high

- id: 05-rules-2026
  subtopic: income-box-brackets-2026
  facts:
    - claim: "Box 1 Bracket 1 rate 2026: 35.75%"
      source_offset: "C9200-9350"
      confidence: high

- id: 05-rules-2026
  subtopic: kia-thresholds-deduction
  facts:
    - claim: "KIA 2026: investment €2,901 to €71,683 → 28% deduction"
      source_offset: "C13200-13400"
      confidence: high
    - claim: "KIA individual asset purchase threshold: > €450"
      source_offset: "C9350-9450"
      confidence: high
    - claim: "If investments > €71,684: apply fixed €20,072, tapering off thereafter"
      source_offset: "C13400-13550"
      confidence: high

- id: 05-rules-2026
  subtopic: mkb-winstvrijstelling-rate
  facts:
    - claim: "MKB-winstvrijstelling rate: 12.7% deduction of remaining profit"
      source_offset: "C14300-14450"
      confidence: high

- id: 05-rules-2026
  subtopic: zelfstandigenaftrek-startersaftrek-amounts
  facts:
    - claim: "Zelfstandigenaftrek 2026: €1,200 annual allowance"
      source_offset: "C14900-15050"
      confidence: high
    - claim: "Startersaftrek 2026: €2,123 additional allowance if within first 3 years"
      source_offset: "C15050-15200"
      confidence: high
    - claim: "Urencriterium: minimum 1,225 hours annually to qualify"
      source_offset: "C14900-15050"
      confidence: high

- id: 05-rules-2026
  subtopic: excessief-lenen-limit
  facts:
    - claim: "Excess Borrowing threshold: €500,000 (excluding qualifying mortgages)"
      source_offset: "C17100-17300"
      confidence: high
    - claim: "Excess beyond €500,000 taxed as Box 2 fictitious dividend"
      source_offset: "C17250-17350"
      confidence: high

- id: 05-rules-2026
  subtopic: representatiekosten-threshold
  facts:
    - claim: "Representatiekosten 2026: €5,700 non-deductible threshold"
      source_offset: "C17850-18000"
      confidence: high
    - claim: "Alternative: deduct 80% (income tax) / 73.5% (VPB); select most favorable"
      source_offset: "C17950-18100"
      confidence: high

- id: 05-rules-2026
  subtopic: wkr-free-space-percentages
  facts:
    - claim: "WKR Free Space 2026: 2.00% on first €400,000 of wage sum"
      source_offset: "C18800-18950"
      confidence: high
    - claim: "WKR above €400,000: 1.18%"
      source_offset: "C18950-19100"
      confidence: high
    - claim: "Exceeding free space triggers 80% final levy"
      source_offset: "C19050-19200"
      confidence: high

- id: 05-rules-2026
  subtopic: innovatiebox-effective-rate
  facts:
    - claim: "Innovatiebox/WBSO: 9% effective corporate tax rate on qualifying IP profits"
      source_offset: "C16200-16350"
      confidence: high

- id: 05-rules-2026
  subtopic: belastingdienst-food-vat-rule
  facts:
    - claim: "Belastingdienst rule 2026: BTW on food/drink consumed on-premises NOT deductible as input tax"
      source_offset: "C24650-24850"
      confidence: high
    - claim: "Classify restaurant/food VAT under representatiekosten instead"
      source_offset: "C24850-25000"
      confidence: high

- id: 05-rules-2026
  subtopic: record-retention-deadline
  facts:
    - claim: "Belastingdienst mandates minimum 7-year business records retention"
      source_offset: "C13300-13450"
      confidence: high

- id: 05-rules-2026
  subtopic: annual-deadlines-events
  facts:
    - claim: "Quarterly VAT filing deadline"
      source_offset: "C26500-26650"
      confidence: medium
    - claim: "Prinsjesdag announcements trigger annual tax bracket/threshold updates"
      source_offset: "C12400-12550"
      confidence: high
    - claim: "Year-end iXBRL filing mandates for 2026"
      source_offset: "C7200-7350"
      confidence: high
    - claim: "KVK deposit requirement for year-end iXBRL export"
      source_offset: "C22950-23100"
      confidence: high
```

## 06-build-vs-buy

```yaml
- id: 06-build-vs-buy
  subtopic: gap-analysis-easy-tier
  facts:
    - claim: "Data Transport via MCP: moneybird-mcp-server and exact-online-mcp-server mature and ready for immediate local deployment"
      source_offset: "C27200-27450"
      confidence: high
    - claim: "Moneybird MCP handles complex OAuth authentication and endpoint mapping to read/write ledger data"
      source_offset: "C27450-27650"
      confidence: high
    - claim: "LLM Orchestration: Claude Desktop + AGENTS.md paradigm allow immediate localized workflow execution with high contextual awareness"
      source_offset: "C27700-27950"
      confidence: high

- id: 06-build-vs-buy
  subtopic: gap-analysis-moderate-tier
  facts:
    - claim: "Receipt Extraction Pipeline: requires custom orchestration (n8n, Pipedream, Python cron) despite Claude 3.5 Sonnet OCR capability"
      source_offset: "C28000-28250"
      confidence: high
    - claim: "Must handle email authentication, attachment extraction, deduplication, LLM feeding automatically"
      source_offset: "C28050-28250"
      confidence: high
    - claim: "RGS Normalization Engine: intermediary translation layer required to map proprietary accounting categories to standardized RGS"
      source_offset: "C28300-28550"
      confidence: high

- id: 06-build-vs-buy
  subtopic: gap-analysis-hard-tier
  facts:
    - claim: "Deterministic Dutch Tax Engine: no comprehensive open-source Python library for all 2026 corporate/income/VAT rules"
      source_offset: "C28650-28900"
      confidence: high
    - claim: "System designer must manually code brackets, €500k excess borrowing logic, KIA taper algorithms, WKR percentages"
      source_offset: "C28900-29150"
      confidence: high
    - claim: "Engine requires strict annual maintenance aligning with Prinsjesdag announcements"
      source_offset: "C29150-29300"
      confidence: high
    - claim: "Belastingdienst API Integration: requires specialized PKI certificates and Digipoort standard integration for automated filing"
      source_offset: "C29400-29700"
      confidence: high
    - claim: "More practical: AI stages data in accounting software (Moneybird) and let software handle cryptographic transmission"
      source_offset: "C29700-29950"
      confidence: high

- id: 06-build-vs-buy
  subtopic: implementation-effort-summary
  facts:
    - claim: "Three tiers of difficulty: Easy to Reuse Now, Moderate Custom Build, Hard Proprietary Logic"
      source_offset: "C27100-27200"
      confidence: high
```

## 07-risks-sources

```yaml
- id: 07-risks-sources
  subtopic: belastingdienst-audit-posture
  facts:
    - claim: "Belastingdienst mandates 7-year business record retention; burden of proof on entrepreneur if incomplete"
      source_offset: "C13300-13500"
      confidence: high
    - claim: "Strict evidentiary continuity required: cryptographic/database linkage between receipt, transaction, and applied tax rule"
      source_offset: "C14000-14250"
      confidence: high
    - claim: "Proper year-end review per XTROVERSO framework prevents standard Belastingdienst corrections and mitigates fines"
      source_offset: "C7400-7550"
      confidence: high

- id: 07-risks-sources
  subtopic: llm-hallucination-failure-modes
  facts:
    - claim: "Most critical failure: arithmetic hallucination and misapplication of complex multi-step tax formulas"
      source_offset: "C8550-8750"
      confidence: high
    - claim: "LLM may hallucinate vendor intent if description vague"
      source_offset: "C24950-25100"
      confidence: medium
    - claim: "LLM may attempt to deduct restaurant VAT if specific exclusion rule not aggressively weighted in prompt"
      source_offset: "C25050-25250"
      confidence: medium

- id: 07-risks-sources
  subtopic: kia-classification-risk
  facts:
    - claim: "Moderate classification risk for KIA: must exclude goodwill and passenger cars"
      source_offset: "C13650-13800"
      confidence: high

- id: 07-risks-sources
  subtopic: innovatiebox-wbso-misclassification
  facts:
    - claim: "High risk of WBSO/Innovatiebox misclassification; strict accountant review mandatory"
      source_offset: "C16350-16500"
      confidence: high

- id: 07-risks-sources
  subtopic: representatiekosten-distinction-risk
  facts:
    - claim: "Moderate risk: AI must accurately distinguish between pure private expenses and valid representation costs"
      source_offset: "C18100-18300"
      confidence: high

- id: 07-risks-sources
  subtopic: vat-mixed-use-risk
  facts:
    - claim: "High VAT/mixed-use asset risk; requires accurate mileage logs or Belastingdienst standard percentage correction"
      source_offset: "C19950-20150"
      confidence: high

- id: 07-risks-sources
  subtopic: source-trust-levels
  facts:
    - claim: "Trust Level: Highest — Official Government Source (Belastingdienst, RGS standard)"
      source_offset: "C36100-36500"
      confidence: high
    - claim: "Trust Level: High — Anecdotal/proven architecture (Claude Did My Taxes), Open Source Repository (Moneybird MCP, Exact MCP), Technical Writeup (AGENTS.md), Professional Accounting Firm (XTROVERSO)"
      source_offset: "C35400-36100"
      confidence: high
    - claim: "Trust Level: Medium — Requires manual parameter updates (Dutch Income Tax Optimizer)"
      source_offset: "C35100-35400"
      confidence: high

- id: 07-risks-sources
  subtopic: llm-in-loop-liability
  facts:
    - claim: "System must ensure AI remains empowerment tool rather than autonomous liability"
      source_offset: "C23000-23150"
      confidence: high
    - claim: "Accountant Handoff protocol ensures system is not forced to resolve highly ambiguous tax scenarios autonomously"
      source_offset: "C9900-10150"
      confidence: high
    - claim: "Year-end close requires human accountant signature and KVK deposit"
      source_offset: "C22950-23100"
      confidence: high
```

