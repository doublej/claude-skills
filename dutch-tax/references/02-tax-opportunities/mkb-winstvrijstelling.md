# MKB-Winstvrijstelling (SME Profit Exemption) — 2026

**Definition:** Automatic 12.7% of qualifying profit is exempt from income tax, applied after zelfstandigenaftrek. Deterministic calculation, zero risk.

## 2026 Number (high confidence)

**Exemption rate:** 12.7% of remaining profit (after zelfstandigenaftrek)  
**Maximum exemption:** €250,000 cumulative over lifetime (aggregate cap, reset if conditions not met)

## Eligibility

- **Who:** ZZP (sole proprietor), VOF (partnership), Eenmanszaak (single-person company)
- **What entities excluded:** BV (corporate tax, different rules; see Innovatiebox instead)
- **Profit threshold:** Any positive profit qualifies
- **Conditions:** No special circumstances disqualifying standard calculation

## Detection Logic

1. Confirm entity type is ZZP, VOF, or Eenmanszaak (not BV)
2. Calculate net profit after zelfstandigenaftrek deduction
3. Apply 12.7% exemption to remaining profit
4. Track cumulative exemption balance against €250,000 lifetime cap
5. No further conditions; purely mathematical

**Data required:** Profit & loss statement, zelfstandigenaftrek amount for the year.

## Calculation Example

```
Gross profit:                 €50,000
Zelfstandigenaftrek:          -€1,200
Profit after deduction:       €48,800
MKB exemption (12.7%):        -€6,197
Taxable profit:               €42,603
```

## Pitfalls

- **Cumulative cap:** Once €250,000 lifetime exemption is used, no further exemption applies
- **Entity type drift:** If ZZP converts to BV, MKB exemption ceases; Innovatiebox becomes relevant instead
- **No discretion:** The 12.7% is automatic; cannot be claimed or declined

## Cross-links

- `zelfstandigenaftrek.md` — Sequencing of zelfstandigenaftrek and MKB exemption
- `../05-rules-2026/ib-brackets.md` — Income tax rates on taxable profit after exemption
- `../06-risks-sources/liability.md` — Entity type verification for audit

## Sources

- note1 (L180): 12.7% rate
- note3 (C14300–14450, C14000–14150, C14500–14600): Eligibility and calculation
- note2 (L297): ZZP/VOF/Eenmanszaak scope
