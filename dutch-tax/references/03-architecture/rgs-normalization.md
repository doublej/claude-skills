# Referentie Grootboekschema (RGS) Normalization

## One-line definition

Universal Dutch chart-of-accounts taxonomy (Referentie Grootboekschema) used by Belastingdienst and CBS; maps proprietary ledger categories to standard RGS codes for filing compatibility.

## Why RGS matters

- **Belastingdienst requirement.** All Dutch VAT/income filings reference RGS codes. Filing systems (iXBRL, SBR) expect RGS mapping.
- **Accountant acceptance.** Professional accountants expect ledger data normalized to standard chart-of-accounts, not bespoke vendor categories.
- **Filing compatibility.** Moneybird, e-Boekhouden, Exact expose proprietary account names. RGS normalization decouples bookkeeping platform from tax logic.
- **Multi-platform reuse.** Same normalized RGS codes work across Moneybird, Exact, e-Boekhouden, or any future connector.

## RGS structure overview

RGS groups accounts into hierarchical categories:

| Category | RGS Code Range | Example | Purpose |
|----------|----------------|---------|---------|
| **Assets** | 1000–1999 | 1100 (current assets), 1500 (fixed assets) | Balance-sheet assets |
| **Liabilities** | 2000–2999 | 2000 (debt), 2100 (payables) | Balance-sheet liabilities |
| **Equity** | 3000–3999 | 3000 (capital), 3200 (retained earnings) | Balance-sheet equity |
| **Revenue** | 4000–4999 | 4000 (product sales), 4100 (services) | P&L revenue lines |
| **COGS** | 5000–5999 | 5000 (materials), 5100 (subcontract) | P&L cost of goods sold |
| **Operating Expenses** | 6000–6999 | 6100 (salaries), 6200 (rent), 6300 (marketing) | P&L opex |
| **Financial** | 7000–7999 | 7000 (interest), 7100 (foreign exchange) | P&L financing costs |
| **Other** | 8000–8999 | 8000 (extraordinary), 8100 (tax) | P&L non-recurring |

## Implementation pattern

1. **Ingestion:** User's bookkeeping data (Moneybird contacts, invoice line items, ledger account names) arrives with proprietary account codes.
2. **Mapping:** AI agent maps each proprietary account to RGS code using:
   - **Deterministic keyword matching** (e.g., "Rent" → 6200 Operating Expense / Rent)
   - **LLM fallback** (classify ambiguous accounts via context + confidence scoring)
   - **Manual override** (user confirms/corrects mapping; stored for future transactions)
3. **Query:** Deterministic tax engine queries ledger by RGS code, not proprietary account name.
4. **Output:** All evidence logs reference RGS codes; filing systems use RGS codes.

## Mapping table (subset example)

| Proprietary Account (Moneybird) | RGS Code | RGS Category | Confidence |
|---------|----------|-------------|------------|
| Huishouding | 6200 | Operating Expenses / Rent | high |
| Kantoor benodigdheden | 6300 | Operating Expenses / Office | high |
| Diensten van derden | 5100 | COGS / Subcontract | medium |
| Reizen & onkosten | 6400 | Operating Expenses / Travel | high |
| Auto kosten | 6500 | Operating Expenses / Vehicle | high |
| Representatie | 6600 | Operating Expenses / Representation | high |
| Onbekend | [QUARANTINE] | Needs User Input | low |

## Authoritative source

**Download standard RGS:** Official document available at [1truth.nl](https://www.1truth.nl/):
- Full RGS taxonomy in CSV/Excel format.
- Code definitions and hierarchies.
- Linked to SBR (Standaard Bedrijfsrapportage) for annual filings.

## Detection & risk

- **Stability:** RGS taxonomy changes rarely (announced in advance via official updates). Low risk if mapped consistently.
- **Mapping drift:** High risk if user changes account names mid-year without updating RGS mapping.
- **Missing mappings:** Medium risk if new proprietary accounts are added without RGS assignment (will quarantine in exception queue).

## Cross-links

- **Ingestion layer:** `mcp-layer.md` — MCP surfaces proprietary ledger data; RGS mapping is the first normalization step.
- **Exception handling:** `exception-handling.md` — unmapped or ambiguous accounts trigger `needs_user_input` state.
- **Evidence logging:** `evidence-logging.md` — all findings cite RGS codes, not proprietary account names.
- **Tax rules:** `../05-rules-2026/*` — deterministic engine queries by RGS code + profit band.

---

**Sources:** note1, note3, deep-report
