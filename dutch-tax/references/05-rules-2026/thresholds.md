# 2026 Tax Thresholds & Deduction Limits

Master lookup table for all major Dutch tax thresholds, organized by topic.

---

## KIA: Kleinschaligheids-investeringsaftrek (Small-scale investment deduction)

| Investment range | Deduction |
|---|---|
| €2,901 – €71,683 | 28% of amount |
| €71,684 – €398,236 | Fixed €20,072 + taper (gradually reduces above €71,683) |
| Above €398,236 | Not eligible |

**Eligibility:** ZZP, VOF, sole traders with business investments in tangible assets.

**Individual asset minimum:** Each asset must cost > €450 to count. Total of qualifying assets summed within fiscal year.

**Asset types:** Machinery, vehicles, furniture, fixtures (depreciation-eligible items). Not: land, buildings, intangible assets.

**Confidence:** High

**Cross-link:** `02-tax-opportunities/kia.md`

---

## KOR: Kleineondernemersregeling (Small business exemption)

| Metric | Threshold |
|---|---|
| Annual turnover | ≤ €20,000 |

**If below:** VAT-exempt. No VAT registration, no quarterly returns, no input VAT deduction.

**If exceeded:** Must register and start charging VAT (even retroactively if discovered).

**Applies to:** ZZP, VOF, eenmanszaak.

**Confidence:** High

**Cross-link:** `05-rules-2026/btw-rates.md` (KOR sits in the BTW rules doc — no separate opportunity leaf)

---

## Zelfstandigenaftrek (Self-employed deduction)

| Year | Annual allowance |
|---|---|
| 2026 | €1,200 |

**Eligibility:** 
- You must meet the **urencriterium** (see below)
- You must have substantial expectation of profit (reasonable business plan)

**Effect:** Reduces taxable profit by this amount. Applied automatically if conditions met.

**Confidence:** High

**Note:** This deduction is scheduled to phase out; 2027 value TBD.

---

## Startersaftrek (New business deduction)

| Year | Annual allowance | Duration |
|---|---|---|
| 2026 | €2,123 | First 3 years of business |

**Eligibility:**
- Business active for ≤ 3 years (inclusive of current year)
- Urencriterium met
- Not a restart of previous failed business (within 3 years)

**Effect:** Additional deduction on top of zelfstandigenaftrek.

**Confidence:** High

---

## Urencriterium (Hours requirement)

| Metric | Threshold |
|---|---|
| Minimum hours per year | 1,225 hours |

**Calculation:** Time spent on business activities, including:
- Direct work (billable hours)
- Admin, planning, bookkeeping
- Professional development
- Startup/setup activities (first year)

**If not met:** Zelfstandigenaftrek and startersaftrek are disallowed; lower tax deductions apply.

**Confidence:** High

**Note:** 1,225 hours ≈ 23.5 hours/week over 52 weeks. Not a hard quota per month; annual total counts.

---

## MKB-winstvrijstelling (SME profit exemption)

| Metric | Rate |
|---|---|
| % of profit exempted | 12.7% |

**Basis:** Calculated on profit **after** zelfstandigenaftrek and startersaftrek applied.

**Eligibility:** All ZZP, VOF, eenmanszaak (automatic).

**Effect:** 12.7% of remaining profit is tax-free.

**Example:** Profit €50,000 → zelfstandigenaftrek €1,200 → taxable €48,800 → MKB exemption €6,197 → net taxable €42,603.

**Confidence:** High

**Cross-link:** `02-tax-opportunities/mkb-winstvrijstelling.md`

---

## Representatiekosten (Business entertaining costs)

| Threshold / Option |  Amount |
|---|---|
| Non-deductible cap | €5,700 |
| Alternative: % deduction (IB) | 80% of actual costs |
| Alternative: % deduction (VPB) | 73.5% of actual costs |

**How to use:** Choose the method most favorable to your tax situation. If entertainment costs < €7,125, the 80% rule is likely best.

**Includes:** Client meals, business gifts (up to limits), entertainment events, travel/accommodation for clients.

**Relatiegeschenken (Business gifts) sub-limit:** Maximum €227 per recipient per year.

**Confidence:** High

**Pitfall:** Don't exceed the annual relatiegeschenken limit or costs become fully non-deductible.

**Cross-link:** `02-tax-opportunities/representatiekosten.md`

---

## WKR: Werkkostenregeling (work-cost scheme)

| Wage sum band | Free-space percentage |
|---|---|
| First €400,000 | 2.00% |
| Above €400,000 | 1.18% |

**Applies to:** Any employer (including a BV with a DGA on payroll). Governs untaxed staff allowances/benefits ("vrije ruimte").

**Free space:** Percentages above represent the *vrije ruimte* — the portion of the wage sum that can be paid out as untaxed benefits/allowances/staff perks without triggering payroll tax.

**Exceeding free space:** Excess over the free-space cap triggers an 80% **eindheffing** (final levy) on the overage, paid by the employer.

**Confidence:** High

**Example:** Total fiscal wage sum €500,000 → free space = (€400k × 2.00%) + (€100k × 1.18%) = €8,000 + €1,180 = **€9,180 untaxed benefits allowed**. If €12,000 of benefits are paid, the €2,820 overage incurs 80% eindheffing = €2,256 owed.

**Cross-link:** `02-tax-opportunities/wkr.md`

---

## Excessief lenen (Excessive borrowing from own company)

| Debt threshold | Status |
|---|---|
| ≤ €500,000 | No issue; normal business loan |
| > €500,000 | Excess treated as Box 2 income |

**Applies to:** DGA loans from own BV/NV.

**Exclusion:** Mortgages on business premises do not count toward this limit.

**Calculation:** Total debt to company minus qualifying mortgages → if > €500,000, excess is deemed dividend (taxed Box 2).

**Example:** You owe your BV €600,000. No qualifying mortgage. Excess = €100,000 → taxed as Box 2 dividend at 24.5% (up to €68,843) or 31%.

**Confidence:** High

**Note:** This changed from €700,000 in 2023 to €500,000 in 2024/2026.

**Cross-link:** `02-tax-opportunities/excessief-lenen.md`

---

## DGA gebruikelijk loon (Customary salary for shareholder-director)

| Year | Reference norm |
|---|---|
| 2025 | €56,000 |
| 2026 | Not yet officially announced |

**Purpose:** If a DGA takes salary below "customary," the difference may be recharacterized as profit and taxed accordingly.

**Status:** The 2026 norm has NOT been confirmed from official sources. Use 2025 value (€56,000) as guidance, but verify with Belastingdienst or accountant before finalizing salary.

**Confidence:** Low — flag as requiring verification.

**Cross-link:** `02-tax-opportunities/dga-salary.md` | `06-risks-sources/liability.md`

---

## Document-retention thresholds

| Document type | Retention period |
|---|---|
| Invoices, receipts, contracts | 7 years (art. 52 AWR) |
| VAT records | 7 years |
| Payroll, social security | 7 years |
| Corporate records (BV/NV) | 7 years minimum |

**Confidence:** High

---

## Bonnetjesplicht (receipt obligation)

| Transaction amount | Rule |
|---|---|
| < €50 | Receipt optional (but recommended) |
| ≥ €50 | Receipt required for deductibility |

**Applies to:** Expenses claimed as business deductions.

**Confidence:** High (practical rule; always keep receipts anyway).

---

## Factuurplicht (Invoice obligation)

| Threshold | Rule |
|---|---|
| < €500 | Invoice optional (receipt/proof sufficient) |
| ≥ €500 | Invoice with full details required |

**For B2B transactions:** Invoices always required regardless of amount.

**For B2C (consumer):** €500 threshold applies.

**Confidence:** High

---

## Sources

- Belastingdienst.nl: Official thresholds and deduction rules
- 2026 budget announcements (Prinsjesdag 2025)
- Dutch tax code (Inkomstenbelastingwet, Vpb)
- Regulatory guidance on WKR, KIA, KOR, DGA salary

**Last reviewed:** 29 April 2026

**Key verification reminders:**
- DGA salary 2026 norm: Not confirmed — verify before filing
- Box 1 Bracket 1 rate (35.75%): One source only — cross-check
- All threshold values: Subject to change at Prinsjesdag (September) — re-verify before year-end filing
