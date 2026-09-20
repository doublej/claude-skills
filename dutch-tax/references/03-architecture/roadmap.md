# Build vs Buy: Gap Analysis, MVP Roadmap, Reuse Decisions

## Gap analysis: what's missing from public ecosystem

| Gap | Why it matters | Effort | Status |
|-----|-------|--------|--------|
| **Verified 2026 Dutch tax rule pack** | No open-source library covers all rules (KOR, KIA, KIA taper, excess borrowing, MKB 12.7%, limited deductibility, Box 2/3, WKR) with official sources and yearly versioning | Hard (annual) | Missing |
| **Deterministic tax engine** | Math must be testable and auditable; LLM cannot be trusted for arithmetic; requires hard-coded brackets, thresholds, taper algorithms | Hard | Missing |
| **RGS normalization layer** | Universal chart of accounts (Referentie Grootboekschema) is Belastingdienst standard; must map proprietary Moneybird/Exact accounts to RGS codes for filing compatibility | Moderate | Missing |
| **Source-evidence store** | 7-year Belastingdienst retention mandate; cryptographic linkage between receipt, transaction, and tax rule; finding_id → rule_version → source_url → evidence_ids | Hard | Missing |
| **Quarterly opportunity scanner** | Automated detection of KOR eligibility, KIA near-threshold, hours evidence gaps, limited-deduction risks, WBSO candidates, DGA excess-borrowing, related-party, foreign VAT | Hard (proprietary logic) | Missing |
| **Accountant review pack generator** | Four-pack export (VAT, IB/VPB, opportunity, questions) with evidence links and accountant-ready formatting | Moderate | Missing |
| **Entity-aware BV/DGA handling** | Shareholder-loan monitoring, DGA useelijk-loon risk flags, dividend timing, intercompany detection | Hard (expertise) | Missing |
| **Regression test suite** | Anonymized prior-year bookkeeping scenarios; test KOR, KIA, urencriterium, company car, reverse charge, mixed-use | Moderate (data) | Missing |

## MVP Roadmap: 5 phases

### Phase 1: Moneybird ingestion + LLM categorization + draft candidates
**Effort:** Easy–Moderate | **Timeline:** 2–4 weeks | **Outcome:** Demo with live Moneybird data

- Use moneybird-mcp-server (Node, MIT, 35 commits) for OAuth + API access.
- Ingest contacts, invoices, time entries; normalize proprietary account names to RGS codes.
- LLM classify transactions with confidence scoring (high/medium/low).
- Emit classified transaction candidates + exception queue (missing receipt, low confidence, foreign supplier, mixed use).
- No writeback; all proposals staged for accountant review.

**First-hour deliverables:**
- Feature 1: Document/receipt ingestion with OCR (Claude 3.5 Sonnet vision).
- Feature 2: Transaction classification with VAT candidate (LLM fallback on deterministic keyword dict).
- Feature 3: Missing-receipt and mixed-use detector (simple rules).
- Feature 4: Quarterly VAT prep packet (totals, source invoices, reverse-charge list, missing receipts).
- Feature 5: KOR, KIA, urencriterium scan (thresholds + alert).

### Phase 2: Deterministic engine for KOR, KIA, MKB, VAT
**Effort:** Hard | **Timeline:** 4–8 weeks | **Outcome:** Testable Python service with 2026 rules

- Build deterministic engine (calculate_kia.py, check_excessief_lenen.py, calculate_wkr_space.py, vat_correction.py).
- Hard-code verified 2026 tables: Box 1 bracket 35.75%, VAT rates 21%, KIA tiers, MKB 12.7%, WKR 2.00%/1.18%.
- Implement RGS normalization: LLM + deterministic mapping from proprietary Moneybird accounts to RGS codes.
- Define exception handling: outcome states (classified, assumed_conservative, needs_input, needs_review, blocked).
- Emit per-calculation metadata: calc_id, rule_ids, source_urls, input_snapshot, intermediate_steps, output_values.

**Deliverables:**
- Deterministic KIA calculator (28% band, fixed+taper band logic).
- Deterministic KOR reverse-charge checker (€20k threshold).
- Deterministic MKB-winstvrijstelling eligibility (payroll < €750k).
- Deterministic VAT return calc (aangifte rubrieken 1a–5d).
- RGS mapping layer: AI agent + deterministic dictionary.

### Phase 3: Quarterly opportunity scanner
**Effort:** Hard (proprietary) | **Timeline:** 4–6 weeks | **Outcome:** Automated detection + alert dashboard

- Cron-triggered batch processing (Oct 1, monthly until Dec 31).
- Scan YTD trial balance (mapped to RGS) + asset registry + DGA current account.
- Alert on: KIA sum near €2,901, €71,683, or €398,236; KOR approaching €20k; urencriterium < 1,225 hours; limited-deduction capped; DGA loan > €450k (excess-borrowing risk).
- Generate executive summary for accountant.
- Never present aggressive positions as advice; always frame as diagnostic + explanation.

**Deliverables:**
- KIA threshold monitor (YTD sum vs tiers).
- KOR eligibility checker (if turnover < €20k, can apply for reverse-charge exemption).
- Urencriterium tracker (aggregate time entries, flag if < 1,225 hours by Nov 15).
- Limited-deduction scanner (representatiekosten, meals, etc.).
- DGA excess-borrowing alert (shareholder loan > €500k).

### Phase 4: Annual close + accountant pack
**Effort:** Moderate | **Timeline:** 3–4 weeks | **Outcome:** Four-pack PDF/CSV export

- Reconcile bank balances, VAT returns, revenue, expenses against provisional assessment.
- Compute Box 1 profit: gross revenue − all allowed deductions − KIA/zelfstandigenaftrek − MKB − WKR.
- Flag transactions needing interpretation, variances > 5%, missing documentation.
- Generate four packs:
  1. **Quarterly VAT pack** (totals, source invoices, reverse-charge list, missing receipts).
  2. **Annual IB/VPB pack** (P&L, balance sheet, asset register, deductions claimed).
  3. **Opportunity pack** (KIA/KOR/hours/WBSO/Box/DGA warnings).
  4. **Questions pack** (accountant queries with evidence links).
- Export iXBRL-ready data; stage in Moneybird for accountant writeback.

**Deliverables:**
- Quarterly VAT reconciliation.
- P&L statement (revenue − COGS − opex).
- Balance sheet (assets, liabilities, equity).
- Deduction summary (KIA, KOR, zelfstandigenaftrek, MKB, WKR, limited deductions).
- Accountant-ready question list with evidence IDs.

### Phase 5: BV/DGA edge handling (with accountant gate)
**Effort:** Hard (expertise) | **Timeline:** 6–8 weeks | **Outcome:** Diagnostic tool + specialist referral

- Add shareholder-loan monitoring, DGA useelijk-loon risk flags, dividend timing, intercompany detection.
- Diagnose DGA salary vs dividend trade-offs; Box 2 / Box 3 planning.
- Always escalate final decision to accountant / fiscalist. System explains scenarios, never recommends structural changes.
- Keep WBSO eligibility as candidate detection only; require specialist review for final claim.
- Keep innovatiebox logic as diagnosis only; too complex for automation.

**Deliverables:**
- DGA salary vs dividend comparison calculator.
- Shareholder-loan accumulation tracker.
- Related-party transaction detector.
- WBSO candidate identification (R&D payroll, Git metadata, milestones).
- Innovatiebox asset eligibility checker (diagnostic only).

---

## Reuse decisions: buy vs build vs fork

| Component | Decision | Rationale | Risk |
|-----------|----------|-----------|------|
| **Moneybird MCP + API** | BUY/REUSE moneybird-mcp-server | Official, MIT, 35 commits, best Dutch SMB platform | Low (official support) |
| **Exact Online MCP** | BUY/REUSE exact-online-mcp (read-only) | High reliability for extraction; second-best integration | Low (stable, read-only) |
| **OpenAccountants skills** | FORK & REPLACE values | Use structure + working-paper pattern; replace all 2025 → 2026 values with official sources | Medium (requires verification) |
| **Moneybird/Exact PHP clients** | BUY/REUSE picqer/moneybird-php, picqer/exact-php | Production-ready, mature, read+write | Low (well-maintained) |
| **Receipt OCR** | BUY/REUSE TaxHacker + Claude 3.5 Sonnet Vision | Docker-based, MIT, OSS + LLM fallback | Medium (TaxHacker early-stage) |
| **Deterministic tax engine** | BUILD custom | No comprehensive off-the-shelf Python library for all 2026 rules | High (annual maintenance) |
| **RGS normalization** | BUILD intermediary layer | RGS is official standard; not exposed by SDKs; must hand-map | Medium (taxonomy stable) |
| **Evidence store** | BUILD cryptographic linking | 7-year retention mandate; must ensure audit defensibility; no COTS solution fits | High (custom) |
| **Opportunity scanner** | BUILD proprietary logic | Does not exist publicly; combines thresholds + heuristics + scenario planning | High (custom) |
| **Accountant review pack** | BUILD + EXPORT | Multi-pack generation; integration with all upstream modules | Medium (well-scoped) |
| **Belastbaar MCP** | USE FOR VERIFICATION ONLY | Data available for 2024–2025 only; closed-source hosting; use as check-layer, not source of truth | Medium (limited coverage) |
| **Commercial products (Jortt, Paperdork, Boekie)** | AVOID REUSING internals | Most close their tax logic; cannot fork; use as reference patterns only | Low (reference only) |
| **RegelSpraak formalization** | USE AS REFERENCE | Belastingdienst-developed controlled natural language; signals correctness of formalizing tax law; too heavy for MVP | Low (future pattern) |

---

## Effort tier summary

| Tier | Estimate | Example |
|------|----------|---------|
| **Easy** | 1–2 weeks | OAuth config, Claude Desktop paradigm, OCR cleanup |
| **Moderate** | 2–4 weeks | Vendor keyword dict (14 × 100 keywords), RGS mapping, BTW filler, urencriterium tracker |
| **Hard** | 4+ weeks | Deterministic engine, opportunity scanner, evidence store, BV/DGA module, WBSO workflows |

---

## Tradeoffs & decisions

### LLM vs deterministic arithmetic
- **Decision:** DETERMINISTIC for all math (VAT, KIA, KOR, brackets, thresholds).
- **Reason:** Tax calculations must be auditable and reproducible; LLM cannot guarantee correctness.
- **LLM scope:** Classification, extraction, explanation, question generation only.

### Read-only first vs immediate writeback
- **Decision:** Start read-only; generate proposed entries; require accountant approval before writeback.
- **Reason:** Safe-by-default; reduces risk of posting incorrect entries to Moneybird.
- **Writeback:** Read-write excludes delete (Moneybird pattern); blocks on missing evidence.

### Accountant in the loop (mandatory)
- **Decision:** Every material finding requires accountant review before filing.
- **Scope:** System proposes; accountant approves or corrects.
- **Liability:** Accountant signature required for VAT/IB/VPB deposit to KVK.

### RGS normalization (mandatory)
- **Decision:** Build translation layer from proprietary accounts to RGS codes.
- **Reason:** Belastingdienst standard; accountant acceptance; filing compatibility.
- **Implementation:** AI maps on ingestion; deterministic engine queries by RGS code.

### Continuous monitoring (rule updates)
- **Decision:** Monitor Belastingdienst changes; version every rule; no silent mutations.
- **Cadence:** Annual Prinsjesdag (September); review ticket per change.
- **Testing:** Regression tests; no patch without test evidence.

---

## Not in Phase 1–4 (postpone)

- **Innovatiebox final logic** — Too complex; candidate detection only.
- **WBSO submission** — Candidate detection + specialist referral only.
- **Multi-entity consolidation** — Out of scope; single entity per user.
- **Payroll-heavy DGA workflows** — Complexity; post-Phase 4.
- **Cross-border goods/IOSS** — Stabilize domestic rules first; add after Phase 4 proven stable.

---

**Sources:** note1, note2, note3, deep-report
