# Compliance & Audit Defense

Belastingdienst compliance posture and defensive practices to minimize audit risk.

## Document retention (legal requirement)

**7-year minimum retention** for VAT (BTW) and Income Tax (IB) evidence per Article 52 AWR.

**Mitigation**: Implement document hash storage with cryptographic linking. Maintain immutable evidence store indexed by:
- Receipt/invoice document ID
- Transaction ID (bank statement)
- Applied tax rule (rule_id + version)
- Timestamp of entry + person who entered it

Verify retention at year-end close and flag any documents approaching 7-year expiry.

---

## Audit triggers

**High-risk signals** that attract Belastingdienst scrutiny:

1. **Mixed business/private expenses** (e.g., home office, vehicle, meals)
   - Mixed-use optimization marked HIGH RISK
   - Mitigation: Conservative default — when ambiguous, classify at higher cost (21% VAT if uncertain)
   - Require accountant review for >50% private-use claims

2. **Deterministic vs. AI-invented positions**
   - Belastingdienst prefers rule-based, deterministic tax positions over novel LLM interpretations
   - Mitigation: Lock all calculations into versioned rule engines; never allow LLM to invent rates or thresholds

3. **VAT compliance gaps**
   - VAT correction deadline: 8 weeks after error discovery; penalties if late
   - Mitigation: Flag correction candidates within 8-week window; maintain suppletie form queue for corrections >€1,000

4. **Restaurant and on-premises food**
   - BTW on food/drink consumed on-premises NOT deductible as input tax (Belastingdienst rule 2026)
   - Mitigation: Classify restaurant/food VAT under representatiekosten only; reject input-VAT claims on on-premises consumption

---

## Conservative-default principle

When ambiguous, classify at higher cost (higher VAT rate, lower deduction).

**Examples**:
- Ambiguous vendor type → assume 21% VAT rather than 9% or 0%
- Ambiguous personal vs. business expense → exclude from deduction
- Ambiguous KIA asset → don't claim until accountant confirms

**Rationale**: Overly aggressive positions trigger audits; conservative positions rarely questioned.

---

## Audit-readiness contract

Every system output must satisfy:

### Calculation envelope (all numeric results)

Every deterministic calculation emits:
- **calc_id**: Unique identifier
- **module**: Which rule engine produced it
- **rule_ids**: Rule(s) applied (e.g., "KIA_28_percent_band")
- **source_urls**: Links to official sources (Belastingdienst URLs with version dates)
- **input_snapshot**: Values used (ledger amounts, asset cost, etc.)
- **input_evidence_ids**: Document hashes linked to input
- **intermediate_steps[]**: All substeps in the calculation
- **output_values**: Final result with rounding policy applied
- **rounding_policy**: Explanation of rounding (standard, floor, ceiling)
- **generated_at**: ISO timestamp
- **engine_version**: Rule engine version for reproducibility

**Rationale**: Accountant can reconstruct and defend to Belastingdienst auditor.

### Conclusion envelope (all agent outputs)

Every conclusion includes:
- **evidence_ids**: Which receipts, invoices, or transactions support this finding
- **rule_ids**: Which tax rules were consulted
- **calculation_ids**: If applicable, links to calculation envelopes
- **confidence**: high / medium / low
- **risk_level**: low / medium / high / extreme
- **reviewer_required**: boolean (true if human accountant must approve before any action)

**Rationale**: Enables audit trail reconstruction and escalation.

---

## Mitigations per risk type

### Document evidence

- Hash all receipts/invoices at upload; store hash + metadata in immutable ledger
- Link every transaction to original document via document_id and hash
- Flag any discrepancies (hash mismatch, metadata edits) for manual review
- Export evidence graph (transaction → document → applied rule) for accountant workpapers

### Never invent rates

- All rates (VAT, KIA percentages, Box brackets, thresholds) sourced from official Belastingdienst pages
- Version-pin every source; capture HTML/PDF hash
- Block any LLM-generated rate that doesn't cite official source
- Quarterly audit of rate values against live Belastingdienst pages; flag any drift

### Suppletie queue (corrections > €1,000)

- Flag VAT corrections >€1,000 within 8 weeks of discovery
- Queue for accountant review before submission
- Maintain immutable record of correction reason, amount, timeline, and approver

### Year-end close: KVK deposit

- KVK deposit requires:
  - Human accountant signature (pen-and-paper or digital signature with key escrow)
  - Year-end review checklist completed (XTROVERSO framework)
  - iXBRL export signed off by accountant
- System blocks export until both conditions met
- Capture signature timestamp and reviewer ID in immutable log

---

## Key rules

1. **Every conclusion cites statute + source URL** with version date
2. **Every calculation has calc_id** for traceability
3. **Every receipt links to transaction + applied rule** via evidence graph
4. **Never hardcode rates**; always source from official pages
5. **Conservative default wins ties** (ambiguous = higher cost)
6. **7-year minimum retention** enforced at close

---

## Sources

note1#L500-510 (7-year retention); note3#L13300-13450 (retention detail); note2#L121 (deterministic preference); deep-report#L8-9 (audit posture); note2#L308 (mixed-use risk); deep-report#L84, L141-143 (VAT correction deadline); note3#C24650-24850 (BTW on food); note3#C236 (calculation envelope); note3#C310 (conclusion envelope); note3#C14000-14250 (evidentiary continuity); note3#C7400-7550 (XTROVERSO framework); note3#C491-494 (XAF, evidence IDs, rule snapshots, review records).
