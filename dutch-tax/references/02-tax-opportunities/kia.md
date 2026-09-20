# KIA (Kleine Investeringsaftrek) — 2026

**Definition:** Immediate deduction of qualifying business asset purchases, no depreciation. Applies to ZZP, VOF, BV, DGA.

## 2026 Numbers (high confidence)

**Band 1:** €2,901–€71,683 per fiscal year → **28% deduction**  
**Band 2:** €71,684–€398,236 per fiscal year → **fixed €20,072 + tapering deduction** (declining percentage above €71,683)

Minimum asset value: **€450** per item (exclude goodwill, passenger cars).

## Eligibility

- **Who:** ZZP, VOF, Eenmanszaak, BV with business use
- **What:** Tools, machinery, equipment, vehicles (not cars), computers, furniture, software, office supplies
- **What not:** Goodwill, land, passenger cars, real estate, financial assets
- **When:** Asset must be purchased and in use within the same fiscal year to qualify

## Detection Logic

1. Sum all qualifying asset purchases in fiscal year with individual value > €450
2. Exclude goodwill, passenger cars, real estate, financial instruments
3. Apply band 1 (28%) if total ≤ €71,683
4. Apply band 2 formula if total ≥ €71,684
5. Flag if sum approaching €71,683 boundary (consider timing for tax efficiency)

**Data required:** Asset registry with purchase date, cost, classification, fiscal year.

## Pitfalls

- **Passenger car mistake:** Claiming deduction on company car purchases (not eligible; see BTW mixed-use instead)
- **Goodwill exclusion:** Intangible acquisition costs do not qualify
- **Year-end purchases:** Assets must be purchased *and in use* by Dec 31 to count in that year
- **Multi-asset gaming:** Splitting single large asset into multiple €450+ items to claim benefit multiple times (allowed but auditable)
- **Borderline asset class:** Software licenses vs. subscriptions (once-off purchase deductible; recurring SaaS may not be)

## Optimization Tactic

**Year-end tax planning:** If business has profit and KIA deduction is below €71,683, consider purchasing qualifying assets (e.g., software, hardware, office equipment) before Dec 31 to claim 28% deduction in current year. Example: €2,901 purchase yields €812 deduction at 28%.

## Cross-links

- `../05-rules-2026/thresholds.md` — KIA band thresholds
- `../06-risks-sources/liability.md` — Audit risk for borderline asset classification
- `btw-mixed-use.md` — Company car VAT handling (complement to KIA exclusion)

## Sources

- note1 (L175, L161): KIA range and 28% band
- note3 (C13150–13550, C13650–13800): Band definitions, classification rules
- deep-report (L87): Automation fit assessment
