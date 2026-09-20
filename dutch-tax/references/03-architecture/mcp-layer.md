# MCP-Based Ingestion Layer

## One-line definition

Read-only-first data transport using Moneybird MCP (Node, MIT, read+write) and Exact Online MCP (CData, read-only); MCP surfaces bookkeeping platform APIs, never acts as tax reasoning engine.

## Connector inventory

### Moneybird MCP Server

- **Status:** Prototype-to-early-production (35 commits, MIT license)
- **Language:** Node.js
- **Access mode:** Read + write (read-only recommended for production start)
- **Capabilities:**
  - Contacts, invoices, purchase orders, accounts, products, projects, time entries
  - Webhooks with retry logic; idempotency support
  - Official Moneybird AI docs distinguish read-only from read-write modes
  - Read-write excludes delete actions (safe writeback design)
- **Ingestion contract:** Fetches list of transactions, invoices, time entries; normalizes to RGS codes
- **Reliability:** High API quality, official AI surfaces, best Dutch SMB integration point

### Exact Online MCP Server (CData)

- **Status:** Open-source wrapper around commercial JDBC driver (Java)
- **Language:** Java
- **Access mode:** Read-only (OSS version is strictly read-only)
- **Capabilities:**
  - Contacts, invoices, purchase orders, G/L accounts, transactions
  - No webhook support; batch polling recommended
- **Ingestion contract:** Fetches accounts and transactions; normalizes to RGS codes
- **Reliability:** High reliability for extraction-only use; second-best integration after Moneybird

## Read-only-first principle

1. **Production starts read-only.** Initial deployment fetches bookkeeping data only; never writes back.
2. **Generate proposed entries.** LLM categorizes transactions, deterministic engine calculates tax impacts, system emits proposed journal entries.
3. **Human approval required.** Accountant reviews proposed entries in staging area (e.g., Moneybird "Draft" or "Pending Review" state).
4. **Only then writeback.** Once approved, system posts to Moneybird. Writeback excluded delete actions (safe pattern per Moneybird docs).

## Data transport contract

| Stage | Input | Processing | Output |
|-------|-------|-----------|--------|
| **Raw ingestion** | Moneybird / Exact API calls | MCP surfaces contacts, invoices, transactions | JSON transaction stream |
| **Deduplication** | Raw stream | Detect duplicate invoice records, bank transactions | Canonical transaction list |
| **RGS normalization** | Canonical transactions + proprietary account names | Deterministic + LLM mapping | RGS-coded ledger |
| **Classification** | RGS-coded ledger + vendor context | Stage 1: keyword dict (70–90%); Stage 2: LLM fallback | Classified transaction + confidence |
| **Tax engine input** | Classified ledger + asset registry | Exception handling (quarantine low-confidence) | Deterministic calc queries |

## Webhook & idempotency

- **Moneybird webhooks:** Supports event-driven updates (invoice created, payment posted, etc.) with retry logic.
- **Idempotency keys:** Prevent duplicate postings if webhook fires multiple times. Include `idempotency_key` in API payload.
- **Deduplication:** Hash (transaction amount + date + counterparty) to detect if transaction already ingested.

## MCP is NOT tax logic

- **MCP surfaces data only.** Moneybird MCP exposes contacts/invoices/accounts; does not perform tax calculations.
- **Tax reasoning is separate.** Deterministic engine (VAT, KIA, KOR, deductions) is decoupled from MCP transport.
- **LLM is for classification, not filing.** LLM extracts and categorizes; system does not ask MCP to "calculate my tax" or "file my return."

## Other ingestion sources

| Source | Transport | Format | Reliability |
|--------|-----------|--------|-------------|
| **Bank feeds** | Bank API (JSON) or CSV upload | Transaction list (date, amount, counterparty, reference) | Medium (requires bank credentials) |
| **Receipt extraction** | Email scraping + OCR | PDF/image → LLM vision → structured JSON (supplier, amount, VAT, date) | Medium (OCR accuracy varies) |
| **Manual entry** | Web form or bulk CSV | User-typed ledger rows | Low (high error rate; needs validation) |

## Exception handling in MCP layer

- **Duplicate detection:** If transaction hash matches prior 30 days, flag and skip (avoid double-booking).
- **Missing required fields:** If invoice lacks supplier name or amount, quarantine in exception queue.
- **Webhook failure:** Retry with exponential backoff; log retry count.
- **API rate limit:** Respect Moneybird rate limits (implement queue + delay).

## Cross-links

- **Architecture overview:** `README.md` — MCP is ingestion stage in broader pipeline.
- **RGS normalization:** `rgs-normalization.md` — MCP surfaces proprietary accounts; RGS mapping follows.
- **Exception handling:** `exception-handling.md` — unclassifiable or missing transactions route to accountant queue.
- **Evidence logging:** `evidence-logging.md` — every ingested transaction assigned transaction_id for cryptographic linking.
- **Tool inventory:** `../01-existing-tools/mcp-servers.md` — full Moneybird/Exact MCP documentation.

---

**Sources:** note1, note2, note3, deep-report
