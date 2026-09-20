# Architecture Reference

This folder documents the deterministic-engine-first pattern for Dutch tax calculation, evidence logging, and accountant collaboration.

## Six sibling documents

1. **deterministic-engine.md** (180 lines)
   - Python engine for verified 2026 tax calculations (VAT, KIA, KOR, deductions, Box 2/3).
   - Why deterministic > LLM for math; hard-coded 2026 tables; maintenance burden.

2. **rgs-normalization.md** (100 lines)
   - Referentie Grootboekschema mapping layer; universal Dutch chart of accounts.
   - Required for accountant acceptance and filing compatibility.

3. **mcp-layer.md** (140 lines)
   - Moneybird MCP (Node, MIT, read+write) and Exact Online MCP (CData, read-only).
   - Read-only-first principle; MCP for transport only, not tax reasoning.

4. **exception-handling.md** (140 lines)
   - Outcome states: classified, assumed_conservative, needs_user_input, needs_accountant_review, blocked_out_of_scope.
   - Exception queues (missing receipt, low-confidence VAT, foreign supplier, DGA, etc.).

5. **evidence-logging.md** (140 lines)
   - 7-year retention (Belastingdienst art. 52 AWR); cryptographic linking.
   - Per-finding and per-calculation metadata; vision OCR for receipt extraction.

6. **roadmap.md** (200 lines)
   - Build vs buy; gap analysis; MVP phases (1-5); reuse decisions; effort tiers.
   - Phase 1: Moneybird ingestion + LLM categorization. Phase 2: Deterministic engine.

## When to load

- **Choosing architecture**: Read README (this file), then deterministic-engine.md and rgs-normalization.md.
- **Setting up ingestion**: Read mcp-layer.md for Moneybird/Exact connector patterns.
- **Handling ambiguous transactions**: Read exception-handling.md for outcome-state decisions.
- **Audit defense**: Read evidence-logging.md for what metadata every finding must emit.
- **Planning build/buy decisions**: Read roadmap.md for gap analysis, phases, and effort tiers.

## Across the skill

- **Tax rules reference**: See `../05-rules-2026/` for KOR, KIA, KOR-KIA interaction, brackets, VAT rates.
- **Opportunity detection**: See `../02-tax-opportunities/` for KIA, KOR, zelfstandigenaftrek, DGA patterns.
- **Prompts and templates**: See `../04-prompts/` for system instructions, classification contracts, quarterly scans.
- **Risk/liability**: See `../06-risks-sources/liability.md` for what system can and cannot do.
- **Tool inventory**: See `../01-existing-tools/` for Moneybird, Exact, OpenAccountants, TaxHacker references.

---

**Sources:** note1, note3, deep-report
