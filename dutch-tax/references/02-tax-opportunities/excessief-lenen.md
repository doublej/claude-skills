# Excessief Lenen (Excess DGA Loans) — 2026

**Definition:** Shareholder loans to DGA exceeding €500,000 (excluding mortgages on primary residence) trigger Box 2 deemed dividend, taxed at 24.5%–31%. Continuous monitoring required; year-end alert essential.

## 2026 Number (high confidence)

**DGA loan cap:** €500,000 per shareholder (excluding mortgage on primary residence)  
**Above-cap consequence:** Excess treated as Box 2 deemed dividend  
**Tax rate:** 24.5% up to €68,843; 31% above (2026 brackets)

**History:** €500k is the 2026 threshold. €700k was the 2023 amount (stale). Step-down occurred in 2024; 2026 remains at €500k.

## Eligibility & Scope

- **Who:** Director-Shareholders (DGA) with personal loans from BV
- **What included:** All loans to DGA, loans to spouse, loans to connected persons
- **What excluded:** Qualifying mortgages on primary residence (owner-occupied)
- **Entity type:** BV (corporate); not applicable to ZZP/VOF/Eenmanszaak
- **Trigger:** Continuous balance monitoring; measured on each day of fiscal year

## Detection Logic

1. **Identify DGA & related parties:** Director-shareholder, spouse, children, connected-person entities
2. **Collect all outstanding loans** from BV to DGA + spouse + related persons
3. **Deduct qualifying mortgages** on primary residences (with valid documentation)
4. **Sum remaining balance** at year-end (or continuous monitoring intra-year)
5. **Flag if sum > €500,000** or approaching threshold by Q4
6. **Calculate excess:** (Total outstanding – €500,000) = Box 2 deemed dividend
7. **Cross-check DGA continuous status:** If DGA status changes mid-year, threshold may shift proportionally

**Data required:** Loan register with counterparty (DGA/spouse/related entity), outstanding balance, mortgage documentation, dates.

## Pitfalls

- **Connected persons trap:** Loans to spouse or adult children count toward cap. Spouse loans to separate "spousal BV" still count.
- **Mortgage complexity:** Only mortgages on **primary residence** (owner-occupied) are excluded. Investment properties, vacation homes, rental properties do NOT qualify for exclusion.
- **Currency risk:** If loans denominated in foreign currency, track EUR equivalent at year-end rate.
- **Partial-year DGA:** If DGA status acquired mid-year (e.g., share transfer), loan thresholds apply pro-rata.
- **Deemed dividend vs. real dividend:** Box 2 deemed dividend is calculated automatically; cannot be offset by actual retained earnings or losses.
- **Spouse status:** If spouse is also DGA, separate loan cap may apply to spouse's loans (dual threshold scenario); clarify with accountant.

## Optimization Tactic

**Year-end alert:** By November 30, calculate total DGA + spouse + related-person loan balance. If approaching €500k:
1. Forgive portion of loan (becomes dividend; taxed same but clears the excessief-lenen trap)
2. Repay portion of loan from DGA personal funds (reduces Box 2 exposure)
3. Restructure mortgage to increase qualified exclusion (if primary residence refinancing is feasible)
4. Obtain accountant opinion on deemed dividend impact and timing

**Example:** DGA loan balance €450k, spouse loan €60k = €510k total.
- Excess: €10k
- Box 2 deemed dividend: €10k × 24.5% = €2,450 Box 2 tax
- Option: Forgive €10k loan before Dec 31 to avoid Box 2 trigger

## Risk Assessment

**Risk level:** Very High.  
- Automatic trigger if threshold breached; no discretion
- Box 2 rate (24.5%–31%) is higher than standard income tax
- Belastingdienst monitors DGA loan registers routinely
- Audit focus on loan-vs.-dividend structures and primary-residence mortgage eligibility

---

## Cross-links

- `../05-rules-2026/box-2-rates.md` — Box 2 tax rates and brackets
- `../06-risks-sources/liability.md` — Excessief-lenen audit risk and DGA loan documentation standards
- `dga-salary.md` — Complementary DGA tax planning (salary vs. dividend vs. loan)

## Sources

- note1 (L188, L161): €500k cap and Box 2 consequence
- note3 (C17050–17300, C16650–16800, C16900–17050, C17350–17550): Threshold definition, connected-persons scope, monitoring requirements
- deep-report (L105): Risk assessment
- note2 (L320): Stale €700k reference (2023 value, not 2026)
