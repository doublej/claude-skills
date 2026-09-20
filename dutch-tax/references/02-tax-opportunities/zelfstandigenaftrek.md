# Zelfstandigenaftrek + Startersaftrek + Urencriterium — 2026

**Definition:** Blanket self-employment deduction (€1,200) + optional starter deduction (€2,123) + mandatory hours test (≥1,225 h/year). Entwined eligibility rules; declining amounts toward 2027 abolition.

## 2026 Numbers (high confidence)

| Deduction | Amount | Condition |
|-----------|--------|-----------|
| Zelfstandigenaftrek | €1,200 | AOW-eligible age (57+) or full year work; urencriterium met |
| Startersaftrek | €2,123 | Starter status; used ≤2 times in prior 5 years; urencriterium met |
| **Urencriterium** | **≥1,225 h/year** | **Required for both deductions** |

**Status decline:** Zelfstandigenaftrek is being phased out. €2,470 (2025) → €1,200 (2026) → €0 (2027).

## Eligibility

- **Who:** ZZP, VOF, Eenmanszaak (not BV)
- **Urencriterium:** Must log ≥1,225 billable/admin/business-development hours per year
- **Age/AOW:** If <57, only eligible if worked entire fiscal year (no part-year deferral)
- **Starter status:** Requires 3 out of preceding 5 fiscal years with no self-employment activity
- **Startersaftrek use:** Can claim maximum 3 times over lifetime, max once per fiscal year
- **Profit floor:** Deductions cannot exceed net profit

## Detection Logic

**Urencriterium verification:**
1. Collect time logs (calendar entries, invoice records, admin hours, startup work)
2. Exclude personal, recreational, overhead hours not tied to business
3. Count approved categories: client work, R&D, admin, business development, training on business skills
4. Sum annual hours; flag if <1,225 or missing evidence

**Startersaftrek history:**
1. Look back 5 fiscal years for self-employment periods
2. If <3 years with activity, qualify as starter
3. Count uses of startersaftrek deduction in prior years
4. Warn if ≥3 uses or >2 uses in last 5 years

**AOW/age check:**
1. If age ≥57: eligible regardless of part-year work
2. If age <57: only eligible if worked full fiscal year (no interruptions)

**Data required:** Time logs, KVK registration date, prior-year zelfstandigenaftrek claims, birth date or AOW record.

## Pitfalls

- **Hours test failure:** Most common audit finding. Insufficient logs = deduction denial. Require contemporaneous time tracking.
- **Overlap with employees:** If you employ staff, their hours cannot count toward urencriterium; must isolate ZZP/self-work hours.
- **Starter definition strictness:** Even 1 month of self-employment in 3 of the prior 5 years disqualifies "starter" status.
- **Multiple uses tracking:** If spouse claims deduction + you claim deduction in same year, both counts are tracked jointly.
- **AOW age border:** Turning 57 mid-year: eligible only from that date onward; pro-rata not standard.
- **Startersaftrek sunset:** Cannot be carried forward to 2027; must claim in 2026 if eligible.

## Optimization Tactic

**For starters (2026):** Claim startersaftrek (€2,123) immediately; you have limited uses (3 total lifetime). Claim before end of fiscal year. Combine with zelfstandigenaftrek (€1,200) for total €3,323 deduction if urencriterium met.

**For age <57:** Confirm full-year work status by Dec 31; part-year work disqualifies deduction.

**Hour-logging strategy:** Establish contemporaneous time-tracking (calendar, invoice ledger, or time-tracking app) by month-end; end-of-year reconstruction is auditable weakness.

## Cross-links

- `../05-rules-2026/thresholds.md` — Urencriterium threshold and AOW age boundary
- `../06-risks-sources/liability.md` — Hours test audit risk and evidence standards
- `mkb-winstvrijstelling.md` — Sequencing: zelfstandigenaftrek applied first, then MKB exemption

## Sources

- note1 (L177, L178, L179, L161): 2026 amounts and urencriterium
- note2 (L26, L208–209, L295–296): Step-down progression and AOW rules
- note3 (C14800–15200): Eligibility and evidence requirements
- deep-report (L90, L92, L227, L360): Detection logic and audit risk
