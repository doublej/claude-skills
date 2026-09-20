# MCP Servers for Dutch Tax & Bookkeeping

Model Context Protocol servers that expose Dutch financial data, tax rules, or bookkeeping APIs to Claude Code, Cursor, or other MCP-compatible AI tools.

## Belastbaar MCP

- **Repo:** (closed-source, SaaS endpoint)
- **Language/License:** Proprietary; hosted service
- **What it does:** Exposes Dutch tax rates, brackets, deduction rules, BOXes, and a 14-item knowledge base (30% ruling, ZZP deductions, toeslagen, representatiekosten, etc.) via MCP protocol
- **Data years:** 2024–2025 confirmed; 2026 **not confirmed** (medium confidence flag)
- **Tools exposed:** `get_tax_rate`, `search_knowledge`, `compare_tax_years`
- **Data URIs:** `tax://YEAR/*` namespace
- **Read/Write:** Read-only (reference data)
- **Maturity:** Production. Actively maintained.
- **NL relevance:** High. Authored for Dutch tax domain.
- **Install hint:** Configure MCP endpoint in settings.json; requires API key from Belastbaar
- **When to use:** Quick lookups of 2024–2025 tax brackets, rates, or quick rules without deep algorithmic work. **NOT** for 2026 unless brackets are manually updated.
- **Caveat:** Knowledge base is reference-only; does not know user's specific transactions or filing status.

---

## Moneybird MCP Server

- **Repo:** https://github.com/vanderheijden86/moneybird-mcp-server (Node.js)
- **Language/License:** Node.js / MIT
- **What it does:** Connects Claude to Moneybird REST API; exposes contact management, invoices, ledger accounts, financial data, projects, time entries, subscriptions, custom API pass-through
- **Maturity:** Early production (7 GitHub stars, 35+ commits, actively maintained through 2026)
- **Read/Write split:**
  - **Read:** Full access to contacts, invoices, accounts, products, projects, time entries, subscriptions, financial reports
  - **Write:** Full access (create/update invoices, contacts, projects, entries); **excludes** delete operations
  - **Recommendation:** Start read-only in production; escalate to write after validation
- **Capabilities in detail:**
  - Fetches bank transactions, ledger accounts, VAT tax rates, invoice history
  - Webhooks with retries and idempotency keys available
  - Native support for Moneybird invoice import/export patterns
- **Reliability for data extraction:** High. Backed by official Moneybird OpenAPI specs.
- **Reliability for tax logic:** Medium. Exposes financial data but does **not** natively comprehend Dutch tax rules or auto-categorize without explicit agent prompting.
- **NL relevance:** Very high. Moneybird is the dominant Dutch SMB bookkeeping platform.
- **Install hint:** `npm install @moneybird/mcp-server` or run from source; requires Moneybird API token
- **When to use:** Any project that needs read/write integration with Moneybird: invoice creation, contact sync, transaction fetching, project time tracking, financial report queries.

---

## Exact Online MCP Server (CData)

- **Repo:** https://github.com/cdata/exact-online-mcp-server (Java wrapper)
- **Language/License:** Java / OSS wrapper around commercial JDBC driver
- **What it does:** Wraps CData JDBC connectivity to Exact Online; translates natural language queries to SQL; exposes ledger, contacts, invoices, payments in relational table schema
- **Maturity:** Production-grade (supported by commercial vendor CData)
- **Read/Write split:**
  - **Read:** Full query access to all Exact Online entities (GL accounts, journals, invoices, contacts, payments, tax lines)
  - **Write:** None. Read-only in OSS wrapper.
  - **Note:** Write access via official Exact Online REST API requires separate implementation
- **Reliability:** High for data extraction. Commercial vendor backing.
- **Reliability for tax logic:** Medium. Exposes ledger data but no native Dutch tax rule inference.
- **NL relevance:** High. Exact Online is an enterprise ERP used by mid-market Dutch accounting firms.
- **Install hint:** Deploy locally; requires CData JDBC driver license (separate purchase) and Exact Online REST credentials
- **When to use:** Read-only access to Exact Online ledgers, GL hierarchies, contact lists, invoice queries. Suitable for auditing, compliance scanning, data enrichment. NOT for transaction posting or write-heavy operations.
- **Caveat:** Write operations require custom REST client integration outside the MCP wrapper.

---

## OmniZoek MCP

- **Repo:** (reference only; Dutch business registration lookup)
- **Language/License:** Not specified
- **What it does:** Queries Dutch Chamber of Commerce (KvK) business registration database; returns company legal name, address, UBO (beneficial owners), establishment dates, turnover brackets
- **Maturity:** Production
- **Read/Write:** Read-only (query only)
- **NL relevance:** High. KvK registration is mandatory for all Dutch business structures.
- **Install hint:** Configure via MCP endpoint; may require KvK API credentials
- **When to use:** Verify business legal names, UBO identity, establishment dates during intake or audit. Useful for ZZP-to-BV transition checks.
- **Caveat:** Does not return financial data; KvK is administrative registry only.

---

## SmartLedger MCP

- **Repo:** https://pypi.org/project/smartledger-mcp/ (Python package)
- **Language/License:** Python / MIT
- **What it does:** Turns Claude into a personal bookkeeper. Parses invoices/receipts from PDFs, analyzes bank CSVs, auto-categorizes by expense type, generates tax-ready expense summaries. **100% local processing** (no cloud)
- **Maturity:** Early production. Actively maintained.
- **Read/Write split:**
  - **Read:** Local file system (PDF receipts, CSV bank exports)
  - **Write:** Structured output (categorized expense ledger, tax summary)
  - **Note:** Does NOT integrate with upstream bookkeeping platforms; output is local only
- **Capabilities:**
  - Receipt OCR and PDF parsing
  - Expense categorization (functional, not rule-based)
  - Bank CSV analysis
  - Tax-ready summaries
- **Reliability:** Medium. Local LLM-based extraction; accuracy depends on invoice quality.
- **NL relevance:** Medium. Generic expense categorization; no Dutch-specific tax rules built in.
- **Requirements:** Python 3.10+
- **Install hint:** `pip install smartledger-mcp`
- **When to use:** Offline receipt/invoice processing for small ZZP or hobby income. **NOT** for real-time bookkeeping sync or production filing.
- **Caveat:** No connection to Belastingdienst, banks, or official platforms; entirely local workflow.

---

**Sources:** note2, note3, deep-report
