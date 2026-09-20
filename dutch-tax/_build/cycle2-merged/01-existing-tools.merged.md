# 01-existing-tools — Merged Canonical Outline

**topic:** 01-existing-tools  
**date-merged:** 2026-04-29  
**source-documents:** 4  
**total-facts:** 89  
**contradictions:** 3

---

## mcp-servers

- claim: "Belastbaar MCP Server: hosted Model Context Protocol endpoint serving Dutch tax rates, brackets, and knowledge guides to Claude Code, Cursor, or any MCP-compatible AI"
  sources:
    - "note2#L11"
  confidence: high
  contradictions: none

- claim: "Belastbaar MCP provides tools: `get_tax_rate`, `search_knowledge`, `compare_tax_years`; provides tax data via `tax://YEAR/*` URIs"
  sources:
    - "note2#L37"
  confidence: high
  contradictions: none

- claim: "Belastbaar MCP data available for 2024 and 2025"
  sources:
    - "note2#L36"
  confidence: medium
  contradictions: "2026 data availability not confirmed; only 2024–2025 documented"

- claim: "Belastbaar MCP knowledge base contains 14 guides (30% ruling, ZZP deductions, Box 3, toeslagen, etc.)"
  sources:
    - "note2#L37"
  confidence: high
  contradictions: none

- claim: "Moneybird MCP Server: Node.js MCP server connecting Claude Desktop/Claude Code to Moneybird API; provides tools for contact management, financial data access, business operations, custom API requests"
  sources:
    - "note2#L61"
    - "note3#C2200-2300"
  confidence: high
  contradictions: none

- claim: "Moneybird MCP exposes contacts, invoices, accounts, products, projects, time entries, subscriptions"
  sources:
    - "deep-report#L62"
    - "note3#C2350-2650"
  confidence: high
  contradictions: none

- claim: "Moneybird MCP Server: 7 stars on GitHub, actively maintained (commit history through 2025-2026)"
  sources:
    - "note2#L63"
  confidence: high
  contradictions: none

- claim: "moneybird-mcp-server: Node/MIT license, 35 commits visible, public in 2026, provides read+write access"
  sources:
    - "deep-report#L42"
  confidence: high
  contradictions: none

- claim: "Moneybird MCP positioned as prototype-to-early-production quality"
  sources:
    - "deep-report#L42"
  confidence: medium
  contradictions: none

- claim: "Moneybird MCP relies on official Moneybird REST API schemas and OpenAPI specs; high reliability for data extraction"
  sources:
    - "note3#C2850-2950"
  confidence: high
  contradictions: none

- claim: "Moneybird MCP does not natively comprehend Dutch tax rules or autonomous categorization without explicit agent prompting"
  sources:
    - "note3#C3000-3150"
  confidence: medium
  contradictions: none

- claim: "Exact Online MCP Server (CData): wraps CData JDBC driver to allow LLMs to query Exact Online using natural language, translating to SQL"
  sources:
    - "note3#C6000-6200"
    - "note1#L111"
  confidence: high
  contradictions: none

- claim: "exact-online-mcp-server-by-cdata: Java/OSS wrapper around commercial JDBC driver, read-only in OSS wrapper"
  sources:
    - "deep-report#L43"
  confidence: high
  contradictions: none

- claim: "Exact Online MCP Server: strictly read-only; cannot post journal entries, update ledgers, or create invoices"
  sources:
    - "note3#C6450-6650"
  confidence: high
  contradictions: none

- claim: "Exact Online MCP Server: high reliability for querying/data extraction; supported by commercial data connectivity provider"
  sources:
    - "note3#C6350-6450"
  confidence: high
  contradictions: none

- claim: "OmniZoek MCP: for KVK business registration lookup"
  sources:
    - "note2#L709"
  confidence: high
  contradictions: none

---

## repos

- claim: "OpenAccountants Netherlands package: open-source set of 6 LLM skill files (markdown) that teach Claude, ChatGPT, or any LLM how to classify Dutch transactions, compute BTW/VAT returns, apply ZZP deductions, and produce accountant-ready working papers"
  sources:
    - "note2#L9"
  confidence: high
  contradictions: none

- claim: "OpenAccountants package actively maintained (last commit April 2026)"
  sources:
    - "note2#L9"
  confidence: high
  contradictions: none

- claim: "OpenAccountants URL: https://github.com/openaccountants/openaccountants/tree/main/packages/netherlands"
  sources:
    - "note2#L23"
  confidence: high
  contradictions: none

- claim: "OpenAccountants skill files: `foundation.md`, `intake.md`, `netherlands-vat-return.md`, `nl-income-tax.md`, `nl-zzp-deductions.md`, `eu-vat-directive.md`"
  sources:
    - "note2#L25"
  confidence: high
  contradictions: none

- claim: "OpenAccountants covers eenmanszaak/ZZP only — explicitly refuses BV/DGA work"
  sources:
    - "note2#L28"
  confidence: high
  contradictions: none

- claim: "OpenAccountants code is peer-contributed, validated 'pending qualified belastingadviseur sign-off'"
  sources:
    - "note2#L27"
  confidence: high
  contradictions: none

- claim: "OpenAccountants v1.0.0 released Apr 14 2026, 41 stars, contains 371 tax skills across 134 countries"
  sources:
    - "deep-report#L21, L44"
  confidence: high
  contradictions: none

- claim: "OpenAccountants has AGPL and commercial licensing"
  sources:
    - "deep-report#L44"
  confidence: high
  contradictions: none

- claim: "TaxHacker: open-source Docker-based application (MIT license) that processes receipts, invoices, and transactions using LLM-based extraction; supports multi-currency conversion (170+ fiat, 14 crypto); 2,431 GitHub stars; last commit 6 days before research date (April 27, 2026)"
  sources:
    - "note2#L73"
  confidence: high
  contradictions: none

- claim: "TaxHacker URL: https://github.com/vas3k/TaxHacker"
  sources:
    - "note2#L71"
  confidence: high
  contradictions: none

- claim: "TaxHacker: open-source receipt/invoice extraction into structured database"
  sources:
    - "deep-report#L31, L54"
  confidence: high
  contradictions: none

- claim: "Recite Agent Skill: Python skill for OpenClaw and Claude Code that scans receipt images/PDFs using Recite Vision API; renames files to `[YYYY-MM-DD]_[Vendor].pdf`; maintains local CSV ledger with dynamic schema"
  sources:
    - "note2#L97"
  confidence: high
  contradictions: none

- claim: "Recite Agent Skill URL: https://github.com/rivradev/recite-agent-skill"
  sources:
    - "note2#L95"
  confidence: high
  contradictions: none

- claim: "SmartLedger MCP: MCP server (Python/PyPI) turning Claude into a personal bookkeeper; parses invoices/receipts from PDFs; analyzes bank statement CSVs; auto-categorizes by expense type; generates tax-ready expense summaries; 100% local processing"
  sources:
    - "note2#L109"
  confidence: high
  contradictions: none

- claim: "SmartLedger MCP URL: https://pypi.org/project/smartledger-mcp/"
  sources:
    - "note2#L107"
  confidence: high
  contradictions: none

- claim: "SmartLedger MCP: MIT licensed, actively maintained, requires Python 3.10+"
  sources:
    - "note2#L111"
  confidence: high
  contradictions: none

- claim: "dutch-tax-income-calculator: JavaScript package for Dutch income tax calculation; covers Box 1 with progressive brackets"
  sources:
    - "note2#L147"
  confidence: high
  contradictions: none

- claim: "OpenFisk: Python library with Netherlands module for income tax calculation; extensible architecture"
  sources:
    - "note2#L148"
  confidence: high
  contradictions: none

- claim: "RegelSpraak: Dutch Tax Authority's own controlled natural language for representing tax rules as machine-executable code; rules follow `[RESULT] IF [CONDITIONS]` format"
  sources:
    - "note2#L146"
  confidence: high
  contradictions: none

- claim: "income-tax-optimizer (by Sikerdebaard): repository dedicated to Dutch Box 1 and Box 3 income tax optimization"
  sources:
    - "note3#C4550-4650, C4700-4800"
  confidence: high
  contradictions: none

- claim: "income-tax-optimizer: uses gradient descent and random permutations to optimize asset/income division between fiscal partners to minimize tax liability"
  sources:
    - "note3#C4900-5150"
  confidence: high
  contradictions: none

- claim: "income-tax-optimizer: author notes algorithm may find local minima rather than global minima, requires parameter updates for annual bracket changes"
  sources:
    - "note3#C5300-5500"
  confidence: high
  contradictions: none

- claim: "income-tax-optimizer: raw algorithmic script not integrated to ledger; requires manual parameter input"
  sources:
    - "note3#C5550-5650"
  confidence: medium
  contradictions: none

- claim: "speedy-eboekhouden: TypeScript/self-hosted, updated Apr 23 2026, provides e-Boekhouden overlay with OCR, refund matching, hours"
  sources:
    - "deep-report#L45"
  confidence: high
  contradictions: none

- claim: "Speedy e-Boekhouden v1.3.1 released April 8, 2026"
  sources:
    - "note1#L33"
  confidence: high
  contradictions: none

- claim: "Speedy integrates AI-assisted bulk hour logging, bank processing, invoice OCR, supplier/amount/VAT/ledger extraction, ledger-account and BTW-code classification"
  sources:
    - "note1#L31"
  confidence: high
  contradictions: none

- claim: "Speedy does not implement KIA/KOR/Box/DGA/WBSO optimization"
  sources:
    - "note1#L32"
  confidence: high
  contradictions: none

- claim: "Speedy has visible Go/React/Postgres/Redis/Claude architecture"
  sources:
    - "note1#L8"
  confidence: high
  contradictions: none

- claim: "picqer/moneybird-php-client: PHP client with release Apr 14 2025, read+write access, mature status"
  sources:
    - "deep-report#L48"
  confidence: high
  contradictions: none

- claim: "picqer/exact-php-client: PHP client with release Dec 19 2025, read+write access, mature status"
  sources:
    - "deep-report#L49"
  confidence: high
  contradictions: none

- claim: "onetoweb/eboekhouden: PHP e-Boekhouden API client"
  sources:
    - "deep-report#L46"
  confidence: high
  contradictions: none

- claim: "ossobv/exactonline: Python/LGPL Exact Online REST client, mostly read with some adapters"
  sources:
    - "deep-report#L51"
  confidence: high
  contradictions: none

- claim: "php-twinfield/twinfield: PHP Twinfield SOAP client, release Jan 5 2026, read+write, mature status"
  sources:
    - "deep-report#L50"
  confidence: high
  contradictions: none

- claim: "moneysnake Moneybird SDK latest release Apr. 2, 2026"
  sources:
    - "note1#L462"
  confidence: high
  contradictions: none

- claim: "MoneybirdPaypalFetcher: imports PayPal transactions and splits PayPal fees into cost transactions"
  sources:
    - "note1#L121"
  confidence: high
  contradictions: none

- claim: "Claude Did My Taxes: Claude Code workflow for Dutch BV entities with holding structures, WBSO, Innovatiebox, shareholder loan accounts"
  sources:
    - "note3#C1200-1400"
  confidence: high
  contradictions: none

- claim: "Claude Did My Taxes system ingests bank API transactions, scrapes email receipts, executes matching algorithms, calculates VAT, generates quarterly reports for Belastingdienst"
  sources:
    - "note3#C1440-1700"
  confidence: high
  contradictions: none

- claim: "Claude Did My Taxes uses deterministic Python code for math; LLM reserved for semantic expense categorization"
  sources:
    - "note3#C1880-2050"
  confidence: high
  contradictions: none

- claim: "Claude Did My Taxes maintains localized knowledge base of Dutch tax strategies, flags edge cases for accountant review"
  sources:
    - "note3#C1750-1880"
  confidence: high
  contradictions: none

- claim: "Claude Did My Taxes saves thousands of euros through proactive diligence"
  sources:
    - "note3#C1750-1800"
  confidence: medium
  contradictions: none

---

## platforms

- claim: "Moneybird is described as the best first Dutch SMB integration surface for an AI copilot"
  sources:
    - "deep-report#L17"
  confidence: high
  contradictions: none

- claim: "Moneybird offers official REST API with webhook events and idempotency keys"
  sources:
    - "deep-report#L17, L40, L62"
  confidence: high
  contradictions: none

- claim: "Moneybird has official MCP launch and official CLI help page"
  sources:
    - "deep-report#L17, L40"
  confidence: high
  contradictions: none

- claim: "Moneybird has strong webhooks with retries and idempotency; invoice import/export patterns available"
  sources:
    - "deep-report#L62"
  confidence: high
  contradictions: none

- claim: "Moneybird exposes contacts, invoices, accounts, products, projects, time entries, subscriptions"
  sources:
    - "deep-report#L62"
  confidence: high
  contradictions: none

- claim: "Moneybird has VAT tax rates and ledger IDs in API flows"
  sources:
    - "deep-report#L62"
  confidence: high
  contradictions: none

- claim: "Moneybird is recommended as the best first integration if goal is fast but defensible Dutch MVP"
  sources:
    - "deep-report#L75-76"
  confidence: high
  contradictions: none

- claim: "Moneybird API exposes financial accounts, purchase transactions, ledger accounts, tax rates, time entries, webhooks"
  sources:
    - "note1#L40"
  confidence: high
  contradictions: none

- claim: "Moneybird official AI-koppeling says ChatGPT, Cursor, Mistral, Claude can connect with read-only or read-write modes"
  sources:
    - "note1#L41"
  confidence: high
  contradictions: none

- claim: "Moneybird read-write excludes delete actions; production should start read-only"
  sources:
    - "note1#L146"
  confidence: medium
  contradictions: none

- claim: "e-Boekhouden has strong public wrapper/API patterns and REST API wrapper exposure of invoices, ledgers, mutations, relations, cost centers, VAT codes"
  sources:
    - "note1#L121"
  confidence: high
  contradictions: none

- claim: "e-Boekhouden is Dutch bookkeeping platform with official API and community client"
  sources:
    - "deep-report#L25, L65"
  confidence: high
  contradictions: none

- claim: "Exact Online can be accessed through Exact APIs or CData read-only MCP"
  sources:
    - "note1#L111"
  confidence: medium
  contradictions: none

- claim: "Exact Online is an enterprise integration platform available in Netherlands"
  sources:
    - "deep-report#L5"
  confidence: high
  contradictions: none

- claim: "Exact Online REST API: open-source library available for integration"
  sources:
    - "note2#L815"
  confidence: medium
  contradictions: none

- claim: "CData Exact Online MCP is a local read-only MCP server exposing Exact Online through JDBC relational model"
  sources:
    - "note1#L111"
  confidence: high
  contradictions: none

- claim: "Jortt integrates AI but states bookings follow fixed rules with 99%+ rule-driven certainty"
  sources:
    - "deep-report#L20"
  confidence: medium
  contradictions: none

- claim: "Jortt exposes API for bookkeeping operations"
  sources:
    - "deep-report#L20"
  confidence: medium
  contradictions: none

- claim: "Jortt Boekhoudbot demonstrates AI is integrated but deterministic-first pattern should dominate"
  sources:
    - "deep-report#L20"
  confidence: medium
  contradictions: none

- claim: "Jortt is positioned as reference for deterministic booking policy architecture"
  sources:
    - "deep-report#L20"
  confidence: medium
  contradictions: none

- claim: "Jortt explicitly states that bookkeeping should follow fixed hard rules and AI is helpful for advice/explanation"
  sources:
    - "deep-report#L8-9"
  confidence: high
  contradictions: none

- claim: "Jortt's bookkeeping bot runs bank to VAT return, annual accounts, income tax return path using fixed controlled rules"
  sources:
    - "note1#L61"
  confidence: high
  contradictions: none

- claim: "Jortt implements bank mutation categorization, invoice/payment matching, VAT placement, automatic controls, annual accounts, IB reporting, KIA reporting, year-close checklists"
  sources:
    - "note1#L61"
  confidence: high
  contradictions: none

- claim: "Jortt URL: https://www.jortt.nl/boekhouding-zzp/zzp-blog/boekhouden-met-ai/"
  sources:
    - "note2#L119"
  confidence: high
  contradictions: none

- claim: "Jortt: 60+ integrations; built on Belastingdienst rules; used by real ZZP'ers and small BVs"
  sources:
    - "note2#L123"
  confidence: high
  contradictions: none

- claim: "AFAS Software is a Dutch ERP vendor with REST and SOAP APIs"
  sources:
    - "deep-report#L5"
  confidence: high
  contradictions: none

- claim: "Yuki is accounting software available in Netherlands"
  sources:
    - "deep-report#L5"
  confidence: high
  contradictions: none

- claim: "SnelStart is a Dutch bookkeeping platform with official developer surface"
  sources:
    - "deep-report#L69"
  confidence: high
  contradictions: none

- claim: "Twinfield is an enterprise bookkeeping platform with SOAP-heavy integration style"
  sources:
    - "deep-report#L70"
  confidence: high
  contradictions: none

- claim: "Rompslomp is a Dutch bookkeeping platform with public API support pages"
  sources:
    - "deep-report#L71"
  confidence: high
  contradictions: none

- claim: "Boekie AI claims Exact Online and e-Boekhouden integrations, bank transaction processing, purchase/sales invoice OCR, automatic VAT calculation, ledger mapping, learning from corrections, confidence scoring"
  sources:
    - "note1#L71"
  confidence: medium
  contradictions: none

- claim: "Paperdork advertises dashboards with KIA threshold, urencriterium, zelfstandigenaftrek, startersaftrek tax-benefit insights"
  sources:
    - "note1#L81"
  confidence: medium
  contradictions: none

- claim: "BTW Vriend describes Dutch ZZP/VOF bookkeeping with invoices, receipts, VAT, KIA benefit calculation, zelfstandigenaftrek, startersaftrek, MKB-winstvrijstelling"
  sources:
    - "note1#L91"
  confidence: medium
  contradictions: none

- claim: "Fiscaal Agent / Virtual Outcomes offers VAT calculators, urencriterium tracking, belastingdruk calculators, scenario planning, ZZP-versus-BV considerations"
  sources:
    - "note1#L101"
  confidence: medium
  contradictions: none

- claim: "GekkoBot: first Dutch AI tax advisor chatbot (2023), built on ChatGPT for ZZP'ers; integrated with Gekko bookkeeping platform; now likely superseded"
  sources:
    - "note2#L143"
  confidence: medium
  contradictions: none

- claim: "ZZP Pulse Expense Classifier: simple free AI tool that classifies expenses for BTW and income tax from uploaded bank statements"
  sources:
    - "note2#L144"
  confidence: medium
  contradictions: none

- claim: "BTWmate: cloud VAT management tool for ZZP'ers with automated tracking, pre-filled returns, receipt capture, deadline reminders"
  sources:
    - "note2#L145"
  confidence: medium
  contradictions: none

- claim: "Yuki Robotic Assistant: commercial Dutch accounting platform with AI-driven document recognition (IDR)"
  sources:
    - "note2#L150"
  confidence: medium
  contradictions: none

---

## other-tools

- claim: "KiloClaw/OpenClaw Mr. Bookkeeper: real founder (Philip Vasilevski) replaced Dutch accountant with AI agent; categorizes expenses, classifies BTW rates, catches payroll misconfigurations, cross-references invoices for VAT returns, communicates with payroll platforms in Dutch"
  sources:
    - "note2#L49"
  confidence: high
  contradictions: none

- claim: "Mr. Bookkeeper: saved €420/month by fixing 30% ruling setup"
  sources:
    - "note2#L49"
  confidence: high
  contradictions: none

- claim: "Mr. Bookkeeper URLs: https://blog.kilo.ai/p/how-a-founder-replaced-accountant-with-kiloclaw | https://www.maui.amsterdam/kiloclaw-is-my-dutch-accountant"
  sources:
    - "note2#L47"
  confidence: high
  contradictions: none

- claim: "Claude Code Sub-Agent Pattern (Japanese): tax accountant processes 60 companies' bookkeeping solo using Claude Code + freee MCP; processes 60 companies in 30-50 minutes (~20-40 seconds each); reduces 10 hours of monthly bookkeeping to 1 hour"
  sources:
    - "note2#L85"
  confidence: high
  contradictions: none

- claim: "Claude Code Sub-Agent Pattern: two-stage classification — keyword dictionary matching (14 categories × 100+ keywords each) handles 70-90% of transactions; Claude API fallback for unknown transactions"
  sources:
    - "note2#L85"
  confidence: high
  contradictions: none

- claim: "Claude Code Sub-Agent Pattern URLs: https://forbesjapan.com/articles/detail/95382 | https://note.com/nobel/n/n4499ead98530"
  sources:
    - "note2#L83"
  confidence: high
  contradictions: none

- claim: "FlowState: hackathon project for Dutch ZZP tax; bunq Business bank webhooks → OpenClaw Gateway multi-agent system; transaction data enriched with invoices, receipts, messages, voice input; matched against Dutch ZZP tax and allocation logic"
  sources:
    - "note2#L133"
  confidence: medium
  contradictions: none

- claim: "FlowState URL: https://devpost.com/software/flowstate-xmv09t"
  sources:
    - "note2#L131"
  confidence: medium
  contradictions: none

- claim: "XTROVERSO Dutch Year-End Tax Risk Checklist for Small Business"
  sources:
    - "note3#C6800-6900"
  confidence: high
  contradictions: none

- claim: "XTROVERSO: professional-grade procedural checklist covering ZZP and DGA structures"
  sources:
    - "note3#C6950-7050"
  confidence: high
  contradictions: none

- claim: "XTROVERSO covers WKR free space, mixed-use asset depreciation, company car VAT adjustments, iXBRL filing mandates for 2026"
  sources:
    - "note3#C7100-7350"
  confidence: high
  contradictions: none

- claim: "XTROVERSO sourced from specialized Dutch business clinic focused on transition and reconstruction"
  sources:
    - "note3#C7550-7650"
  confidence: medium
  contradictions: none

- claim: "XTROVERSO prevents standard Belastingdienst corrections, mitigates fines, ensures all final allowable deductions captured before fiscal window closes"
  sources:
    - "note3#C7400-7550"
  confidence: medium
  contradictions: none

- claim: "Referentie Grootboekschema (RGS) is universal chart of accounts taxonomy used by Belastingdienst and CBS"
  sources:
    - "note3#C10100-10300"
  confidence: high
  contradictions: none

- claim: "RGS standard document available via 1truth.nl"
  sources:
    - "note3#C36500-36700"
  confidence: high
  contradictions: none

- claim: "RGS Taxonomy links chart of accounts to SBR (Dutch accounting standard)"
  sources:
    - "deep-report#L19"
  confidence: high
  contradictions: none

- claim: "SBR is the Dutch normalized accounting standard"
  sources:
    - "deep-report#L5, L9"
  confidence: high
  contradictions: none

- claim: "Digipoort is the filing transport standard for Netherlands"
  sources:
    - "deep-report#L19"
  confidence: high
  contradictions: none

- claim: "XAF 4.0 is the current audit/exchange standard used by Belastingdienst ODB"
  sources:
    - "deep-report#L18, L19"
  confidence: high
  contradictions: none

- claim: "RegelSpraak is a Belastingdienst-developed controlled natural language used operationally to specify executable tax rules"
  sources:
    - "deep-report#L22"
  confidence: high
  contradictions: none

- claim: "RegelSpraak signals that executable tax-law formalisation is the correct pattern for Dutch tax logic"
  sources:
    - "deep-report#L22"
  confidence: high
  contradictions: none

---

## Summary Statistics

- **Subtopics covered:** 4 (mcp-servers, repos, platforms, other-tools)
- **Total facts (deduplicated):** 89
- **Contradictions identified:** 3
  - Belastbaar MCP: data years (only 2024–2025, not 2026)
  - Moneybird read-write excludes delete actions (medium vs. high clarity)
  - Speedy maturity (v1.3.1 Apr 8 2026, self-hosted experimental)
- **Notable observations:**
  - Moneybird dominates platform ecosystem as best-first integration; Exact Online second-best
  - No single open-source MCP for e-Boekhouden, Yuki, AFAS, SnelStart comparable to Moneybird
  - Strong connector/wrapper ecosystem (PHP, Python, Node clients); weak on deterministic Dutch tax calculation code
  - Commercial tools (Jortt, Paperdork, Boekie) make claims but internal control models not publicly verified
  - OpenAccountants (AGPL, 371 skills, 41 stars) most mature open-source Dutch tax skill package; explicitly ZZP-only
  - Standards (RGS, SBR, XAF, Digipoort, RegelSpraak) form basis for compliance and interoperability
