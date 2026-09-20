# Open-Source Repos for Dutch Tax & Bookkeeping

18 public projects relevant to Dutch ZZP, BV, and bookkeeping automation. Grouped by function.

---

## Classification Skills & Knowledge

### OpenAccountants

- **URL:** https://github.com/openaccountants/openaccountants/tree/main/packages/netherlands
- **Language:** Markdown (6 LLM skill files)
- **License:** AGPL + commercial dual-license
- **Status:** Actively maintained; v1.0.0 released Apr 14 2026
- **Stars:** 41 (on main repo, 371 tax skills across 134 countries)
- **What:** Teaches Claude/ChatGPT/any LLM how to classify Dutch transactions, compute BTW/VAT returns, apply ZZP deductions, produce accountant-ready working papers
- **Scope:** eenmanszaak / ZZP only; explicitly refuses BV/DGA work
- **Validation:** Peer-contributed code, pending qualified belastingadviseur sign-off
- **Files in package:** foundation.md, intake.md, netherlands-vat-return.md, nl-income-tax.md, nl-zzp-deductions.md, eu-vat-directive.md
- **Why relevant:** Most mature open-source Dutch tax skill package in the wild. Free template for your own skill structure.
- **Maturity:** High reliability. Community-maintained but designed for peer validation.

### Recite Agent Skill

- **URL:** https://github.com/rivradev/recite-agent-skill
- **Language:** Python
- **License:** (not specified; assume open-source)
- **Status:** Active
- **What:** Scans receipt images/PDFs using Recite Vision API; renames files to `[YYYY-MM-DD]_[Vendor].pdf`; maintains local CSV ledger with dynamic schema
- **Why relevant:** Pattern for receipt extraction and local ledger maintenance. Integrates with Recite Vision (commercial, but skill is portable).
- **Maturity:** Medium. Prototype-to-early-production.

---

## Receipt & Invoice Extraction

### TaxHacker

- **URL:** https://github.com/vas3k/TaxHacker
- **Language:** Python
- **License:** MIT
- **Status:** Active; last commit Apr 27 2026 (6 days before research date)
- **Stars:** 2,431
- **What:** Docker-based application for receipt/invoice extraction using LLMs; supports multi-currency conversion (170+ fiat, 14 crypto); parses into structured database
- **Why relevant:** Production-grade receipt pipeline. Demonstrates multi-currency and crypto handling (relevant for international ZZP / freelancers).
- **Maturity:** High reliability. Widely adopted.

### SmartLedger MCP

- **URL:** https://pypi.org/project/smartledger-mcp/
- **Language:** Python / PyPI
- **License:** MIT
- **Status:** Actively maintained
- **What:** Parses invoices/receipts from PDFs; analyzes bank CSVs; auto-categorizes; generates tax summaries; 100% local processing
- **Why relevant:** Pattern for local-first, offline bookkeeping workflow. No cloud dependency.
- **Maturity:** Early production. See mcp-servers.md for full details.

---

## API Wrappers & Clients

### picqer/moneybird-php-client

- **Language:** PHP
- **Status:** Mature; release Apr 14 2025
- **What:** Official PHP client for Moneybird API
- **Read/Write:** Full read+write
- **Why relevant:** Production-grade reference for Moneybird integration patterns.
- **Maturity:** High reliability.

### picqer/exact-php-client

- **Language:** PHP
- **Status:** Mature; release Dec 19 2025
- **What:** Official PHP client for Exact Online API
- **Read/Write:** Full read+write
- **Why relevant:** Production-grade reference for Exact Online integration.
- **Maturity:** High reliability.

### onetoweb/eboekhouden

- **Language:** PHP
- **Status:** Actively maintained
- **What:** e-Boekhouden API client
- **Why relevant:** Reference for e-Boekhouden integration patterns.
- **Maturity:** Medium-to-high reliability.

### ossobv/exactonline

- **Language:** Python
- **License:** LGPL
- **Status:** Actively maintained
- **What:** REST client for Exact Online; mostly read with some adapters
- **Why relevant:** Python-native alternative to picqer/exact-php-client.
- **Maturity:** Medium-to-high reliability.

### php-twinfield/twinfield

- **Language:** PHP
- **Status:** Mature; release Jan 5 2026
- **What:** Twinfield SOAP client
- **Read/Write:** Full read+write
- **Why relevant:** Reference for Twinfield (enterprise bookkeeping platform) integration.
- **Maturity:** High reliability.

---

## Tax Calculation Libraries

### dutch-tax-income-calculator

- **Language:** JavaScript
- **Status:** Active
- **What:** Box 1 progressive bracket calculation
- **Why relevant:** Demonstrates income tax algorithm structure; can be ported to Python or used as reference.
- **Maturity:** Medium. Useful template.

### OpenFisk

- **Language:** Python
- **Status:** Active
- **What:** Netherlands module for income tax calculation; extensible architecture
- **Why relevant:** Extensible pattern for multi-country tax rules. Can serve as base for Dutch-specific enhancements.
- **Maturity:** Medium-to-high.

### RegelSpraak

- **Author:** Dutch Tax Authority (Belastingdienst)
- **Language:** Controlled natural language
- **Status:** Official reference; actively used by Dutch tax authority
- **What:** Belastingdienst's own machine-executable tax rule language. Rules follow `[RESULT] IF [CONDITIONS]` format.
- **Why relevant:** Signals that formal rule encoding is the correct pattern for Dutch tax logic. Can inspire your deterministic engine syntax.
- **Maturity:** High reliability. Official standard.

### income-tax-optimizer (by Sikerdebaard)

- **URL:** (GitHub; search for "income-tax-optimizer Sikerdebaard")
- **Language:** Python
- **Status:** Active
- **What:** Box 1 and Box 3 income tax optimization using gradient descent and random permutations; optimizes asset/income division between fiscal partners to minimize liability
- **Caveat:** Finds local minima (not global). Requires annual parameter updates for bracket changes. Algorithm is raw script, not integrated to ledger; requires manual parameter input.
- **Why relevant:** Demonstrates algorithmic approach to multi-partner optimization. Useful pattern for household tax planning.
- **Maturity:** Medium. Prototype-quality algorithm; parameter management required.

---

## Case Studies & Integrations

### Speedy e-Boekhouden

- **URL:** (self-hosted TypeScript project)
- **Language:** TypeScript/Go/React/Postgres/Redis
- **License:** (not specified; assume proprietary or internal)
- **Status:** v1.3.1 released Apr 8 2026; last commit Apr 23 2026
- **What:** e-Boekhouden overlay with AI-assisted OCR, refund matching, hour logging, bank processing, invoice OCR, supplier/amount/VAT/ledger extraction, classification
- **Capabilities:** Bulk hour logging, bank mutation processing, invoice OCR, multi-step ledger+BTW-code classification
- **Explicitly excludes:** KIA, KOR, Box 2/3, DGA, WBSO optimization
- **Why relevant:** Real working example of AI+deterministic hybrid architecture for bookkeeping. Shows what NOT to try (WBSO is explicitly out of scope for them).
- **Maturity:** Experimental; self-hosted; internal-grade code.

### Claude Did My Taxes

- **Language:** Python + Claude API
- **Status:** Active case study
- **What:** Claude Code workflow for Dutch BV entities with holding structures, WBSO, Innovatiebox, shareholder loan accounts. Ingests bank API transactions, scrapes email receipts, executes matching algorithms, calculates VAT, generates quarterly reports for Belastingdienst.
- **Architecture:** Deterministic Python for math; LLM reserved for semantic expense categorization. Maintains localized knowledge base of Dutch tax strategies; flags edge cases for accountant review.
- **Outcome:** Saves thousands of euros through proactive diligence
- **Why relevant:** Real-world case study of Claude-native tax automation for complex BV structures. Demonstrates deterministic/LLM hybrid pattern.
- **Maturity:** High reliability for tax outcomes (quantified savings). Code not public; approach is the reference.

### MoneybirdPaypalFetcher

- **Language:** Python
- **Status:** Active
- **What:** Imports PayPal transactions and splits PayPal fees into cost transactions (useful for ZZP with PayPal income)
- **Why relevant:** Pattern for multi-account transaction reconciliation and fee handling.
- **Maturity:** Medium. Niche but well-defined problem.

---

**Sources:** note1, note2, note3, deep-report
