# BTW Mixed-Use (VAT Repayment for Private-Use Assets) — 2026

**Definition:** When business assets (car, phone, home office, devices) are used for private purposes, the VAT attributable to private use cannot be deducted as input VAT and must be repaid. Applies to all entities. Company car has simplified 2.7% (or 1.5%) forfait option if no mileage logs.

## 2026 Numbers (high confidence)

| Asset | Private-Use Handling | VAT Correction |
|-------|----------------------|----------------|
| Company car | 2.7% forfait OR actual km logs | If forfait: 2.7% of catalog value × 21% VAT |
| | (1.5% if conditions met: B2B only, closed tracking) | Or: 1.5% of catalog value if strict conditions |
| Phone | Proportional allocation (est. 30–50%) | Pro-rata VAT repayment |
| Home office | Proportional by square footage | Pro-rata VAT repayment |
| Devices (laptop, tablet) | Proportional by usage (estimate 20–40%) | Pro-rata VAT repayment |

**VAT rate applied:** 21% on most assets (standard rate).

## Eligibility & Scope

- **Who:** All entities with mixed business/private asset use
- **What:** Any asset purchased with VAT deduction that is later used partially for private purposes
- **What NOT:** Exclusively business assets (100% deductible) do not trigger repayment
- **Timing:** VAT correction applies in the tax period when private use occurs or is detected

## Detection Logic

1. **Asset registry:** Identify all capitalized assets (car, equipment, devices, property)
2. **Usage classification:** Determine if each asset is 100% business or mixed (business + private)
3. **For company car:**
   - If mileage logs exist: calculate private km % and apply VAT correction
   - If NO logs: apply 2.7% (or 1.5%) forfait of catalog value (Belastingdienst standard)
4. **For other assets:** Estimate private-use percentage (phone 30–50%, home office pro-rata, devices 20–40%)
5. **Calculate VAT correction:** Private-use percentage × VAT × asset purchase price
6. **Flag if no documentation:** Missing mileage logs, usage logs → apply forfait (higher repayment risk)

**Data required:** Asset registry with purchase price, VAT-paid, catalog value (car), mileage logs (if available), usage estimates, dates of acquisition and private-use start.

## Pitfalls

- **Delayed recognition:** Purchasing car/device for 100% business, later using privately → VAT correction owed retroactively from first private use
- **Km-log weakness:** Informal tracking (hand-written notes) is less defensible than digital logs; Belastingdienst may impose higher estimate
- **Car catalog value inflation:** Private-use forfait is based on catalog value (list price), not purchase price. Imported/used cars with low purchase price but high catalog value = higher repayment
- **Home-office complexity:** Allocating office VAT by square footage requires accurate space measurements; missing floor-plan = audit risk
- **Period of use:** If car purchased in June, private use begins in August → VAT correction is partial (not full year)
- **Cumulative error:** Multiple mixed-use assets (car + phone + office) in same year = complex aggregate calculation; errors compound

## Examples

**Example 1: Company car (2.7% forfait, no km logs)**
- Catalog value: €40,000
- VAT-paid (21%): €8,400
- Private-use forfait: 2.7% × €40,000 = €1,080
- VAT repayment: €1,080 × 21% = €227
- (Note: This is simplified; actual calculation may differ)

**Example 2: Company car (actual km logs)**
- Annual km: 20,000 total, 5,000 private (25%)
- VAT-paid: €8,400
- VAT repayment: €8,400 × 25% = €2,100

**Example 3: Home office (proportional)**
- Total office space: 50 m² out of 100 m² home
- VAT-paid on office furniture/fixtures: €2,000
- Private-use %: 50%
- VAT repayment: €2,000 × 50% = €1,000

## Optimization Tactic

**Mileage logging discipline:** Maintain detailed km logs from day of car purchase (even if fully business initially). If private use becomes unavoidable later, logs support lower forfait or actual % claim. Missing logs force Belastingdienst 2.7% forfait (or higher estimate).

**Asset purchase timing:** If planning private-use asset, purchase it in name of DGA personally (not BV) to avoid VAT correction burden. Or, delay VAT recovery until business use is confirmed ≥80%.

**Documentation:** For phone/device/home office, photograph space plan, maintain usage logs (even informal), and note on asset register the estimated private % at purchase. Year-end review and adjustment beats surprise audit correction.

---

## VAT Return Integration

**Correction method:**
- Correction ≤€1,000: Include in next VAT return (box for corrections)
- Correction >€1,000: File separate suppletie form (request form) with detailed justification and asset list

---

## Cross-links

- `../05-rules-2026/vat-rates.md` — VAT rate (21% standard)
- `../06-risks-sources/liability.md` — Audit risk for mixed-use allocation and km-log quality
- `representatiekosten.md` — Related: business entertainment VAT (also non-deductible)

## Sources

- note1 (L182, L183): VAT mixed-use scope and company-car forfait
- note3 (C19300–19450, C19450–19600, C19700–19900, C19950–20150): Mixed-use rules, asset registry, mileage-log standards, forfait percentages
- deep-report (L95–96): Risk assessment and automation fit
