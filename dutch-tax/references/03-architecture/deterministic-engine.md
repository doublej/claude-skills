# Deterministic Tax Calculation Engine

## One-line definition

Custom Python service that executes verified 2026 tax rules (VAT, KIA, KOR, deductions, Box brackets) with hard-coded tables, rule versioning, and audit traces.

## Why deterministic, not LLM

- **Tax math must be correct, not hallucinated.** LLM reasoning is useful for extraction and classification; for arithmetic, deterministic code guarantees repeatability and auditability.
- **No comprehensive open-source library exists.** Every rule (KOR threshold, KIA taper logic, excess-borrowing €500k check, MKB-winstvrijstelling 12.7%, Box 1 bracket 35.75%) must be hand-coded.
- **Annual maintenance required.** Prinsjesdag (September) announces next-year rules. System must version every rule with effective dates and official sources.
- **Calculation traces are mandatory.** Each output must cite rule_id, rule_version, source_url, input_snapshot, intermediate_steps. LLM cannot provide this level of accountability.

## 2026 hardcoded values (high confidence unless noted)

| Concept | 2026 Value | Entity | Notes |
|---------|-----------|--------|-------|
| VAT standard rate | 21% | All | EU harmonized |
| VAT reduced | 9%, 0% | All | Tiered by good/service |
| Box 1 Bracket 1 | 35.75% | ZZP / BV | (medium: verify vs Belastingdienst) |
| KIA threshold (28% band) | €2,901–€71,683 | ZZP / eenmanszaak | High confidence |
| KIA fixed-deduction band | €71,684–€398,236 | ZZP / eenmanszaak | Fixed €20,072 + taper |
| KIA taper rate | 4.43% | ZZP / eenmanszaak | Above €71,683 |
| KOR threshold | €20,000 turnover | All | Reverse-charge eligibility below €20k |
| MKB-winstvrijstelling | 12.7% | BV (payroll <€750k) | High confidence |
| Zelfstandigenaftrek | €1,200 | ZZP / eenmanszaak | On step-down toward 2027 abolition |
| Startersaftrek | €1,200 | First 5 years | High confidence |
| DGA excess-borrowing threshold | €500,000 | DGA/shareholder | (was €700k in 2023; 2026 is €500k) |
| Box 2 rate | 24.5% (income) / 31% (profit) | DGA / shareholder | High confidence |
| Box 3 rates | 1.28%, 6%, 2.70% | All | Wealth tax; tiered by asset band |
| WKR (werknemersvoordeel) | 2.00%, 1.18% | Payroll benefit | Tiered |
| Beperkt aftrekbare kosten threshold | €5,700 representatiekosten | All | 80% above €5,700; some capped at €5k |

## Engine modules (suggested structure)

```
deterministic_engine/
  ├── rules/
  │   ├── kia.yaml          # KIA thresholds, bands, taper
  │   ├── kor.yaml          # KOR reverse-charge logic
  │   ├── deductions.yaml    # Zelfstandigenaftrek, startersaftrek, MKB, etc.
  │   ├── vat.yaml          # VAT rates, correction logic
  │   ├── boxes.yaml        # Box 1, 2, 3 rates, thresholds
  │   ├── wkr.yaml          # WKR percentages
  │   └── limited_deductibility.yaml  # Representatiekosten, meals, etc.
  ├── calculate_kia.py       # KIA percentage + taper logic
  ├── check_excessief_lenen.py  # DGA €500k excess-borrowing check
  ├── calculate_wkr_space.py # WKR free space remaining
  ├── vat_correction.py      # VAT return adjustments, reverse-charge
  ├── box_calculator.py      # Box 1, 2, 3 rates and income mapping
  └── output_trace.py        # Emit calc_id, rule_ids, evidence_ids, etc.
```

## Rule format (YAML/JSON)

Every rule must carry:

```yaml
rule_id: "KIA-001"
rule_name: "KIA percentage deduction for small business"
entity_type: ["ZZP", "eenmanszaak"]
tax_year: 2026
effective_date: "2026-01-01"
official_source_url: "https://www.belastingdienst.nl/..."  # Exact statute link
rule_text: "Percentage deduction KIA: 28% on profits between €2,901–€71,683; €20,072 fixed + taper above €71,683"

eligibility_predicates:
  - entity_type in ["ZZP", "eenmanszaak"]
  - profit > €0

calculation:
  if: profit_capped in [2901, 71683]
    then: kia_deduction = profit_capped * 0.28
  elif: profit_capped in [71684, 398236]
    then: kia_deduction = 20072 + (profit_capped - 71683) * 0.0443
  else: kia_deduction = 0

numeric_parameters:
  threshold_lower: 2901
  threshold_28pct: 71683
  fixed_deduction: 20072
  taper_rate: 0.0443
  threshold_upper: 398236

maintenance_notes: "Updated annually with Belastingdienst published rates. Last audit: 2026-04-29."
```

## Eligibility & scope

- **Covers**: VAT rates, VAT return (aangifte) corrections, KIA, KOR, zelfstandigenaftrek, startersaftrek, MKB-winstvrijstelling, beperkt aftrekbare kosten, Box 2 excess-borrowing check, Box 3 tiering, WKR free space, limited-deductibility caps.
- **Does NOT cover**: Innovatiebox logic (complex asset tracking), WBSO eligibility (requires narrative R&D proof), intercompany pricing, multi-jurisdiction consolidation.

## Annual maintenance burden

1. **Monitor Belastingdienst** `veranderingen` page monthly; RVO year-end rate releases.
2. **Prinsjesdag (mid-September):** Track announced rule changes for next year.
3. **Q4 update cycle:** Patch numeric parameters, test with anonymized prior-year data, commit with issue reference.
4. **No silent mutations.** Every rule change opens a review ticket; changes go through pull request with test evidence before merge.

## Risk classification

| Risk | Condition |
|------|-----------|
| Low | Engine is properly versioned, every rule cites official source, unit + regression tests pass quarterly, changes go through review |
| Medium | Numeric parameters updated ad-hoc without test suite, or rules lack official source URLs |
| High | Rules are stale (older than 1 year), live-edited without regression tests, source URLs are broken/missing, multiple rules per rule_id |

## Output contract

Every calculation must emit:

```json
{
  "calc_id": "calc_2026_04_29_uuid",
  "module": "calculate_kia",
  "rule_ids": ["KIA-001"],
  "source_urls": ["https://www.belastingdienst.nl/..."],
  "input_snapshot": {
    "entity_type": "ZZP",
    "profit_before_kia": 150000,
    "tax_year": 2026
  },
  "intermediate_steps": [
    {"step": "check eligibility", "result": true},
    {"step": "profit >= €2,901", "result": true},
    {"step": "select band", "result": "28% band (€2,901–€71,683)"},
    {"step": "apply rate", "result": "€150,000 * 0.28 = €42,000"}
  ],
  "output_values": {
    "kia_deduction": 42000,
    "currency": "EUR",
    "rounding_policy": "round_half_up"
  },
  "evidence_ids": ["ev_income_ledger_2026", "ev_balance_sheet_2026"],
  "generated_at": "2026-04-29T14:32:00Z",
  "engine_version": "2026.04.01"
}
```

---

**Sources:** note1, note3, deep-report
