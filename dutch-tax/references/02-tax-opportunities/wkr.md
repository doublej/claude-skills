# WKR (Werkkostenregeling) — 2026

**Definition:** Employer taxable benefit allowance exempting a portion of untaxed employee benefits and allowances from payroll tax. Exceeding the free space triggers 80% final levy (eindheffing) on the overage.

## 2026 Numbers (high confidence)

| Wage Sum Range | WKR Free Space | Rate |
|----------------|----------------|------|
| €0–€400,000 | 2.00% of wage sum | Untaxed allowances exempt |
| €400,001+ | 1.18% of amount above €400k | Untaxed allowances exempt |
| Exceeding space | 80% eindheffing | Mandatory payroll tax on overage |

**Cumulative example:** Wage sum €500k → Free space = (€400k × 2.00%) + (€100k × 1.18%) = €8,000 + €1,180 = €9,180.

## Eligibility & Scope

- **Who:** Employers with employees (ZZP rarely applies unless has staff); DGA holdings
- **What:** Untaxed allowances (car allowance, phone allowance, home-office allowance, travel reimbursement), taxable benefits, expense reimbursements under €23/day
- **What NOT:** Salary, taxable wages, holiday pay, sick pay above statutory limits
- **Monitoring:** Quarterly or annual calculation; must halt new allowances if approaching limit

## Detection Logic

1. **Calculate fiscal wage sum** for the year (all employee salaries, payroll contributions included)
2. **Identify untaxed allowances & benefits** ledger (car, phone, meals, travel, home office)
3. **Sum untaxed allowances** for all employees combined
4. **Apply WKR percentage** to wage sum based on brackets above
5. **Compare actual allowances to free space:**
   - If allowances ≤ free space: all exempt (no eindheffing)
   - If allowances > free space: excess × 80% must be paid as payroll tax (eindheffing)
6. **Flag near-limit:** When YTD allowances approach free space, halt new benefit issuance or reductions

**Data required:** Payroll ledger with gross salaries, benefit allowances per employee, untaxed reimbursements, wage-sum total by fiscal year.

## Pitfalls

- **Over-estimation trap:** Calculating free space incorrectly (e.g., forgetting 1.18% bracket for amounts >€400k) leads to underpayment and 80% penalty.
- **Benefit salary creep:** Offering new allowances without recalculating free space → overage accrues unnoticed until year-end audit.
- **Threshold timing:** €400k wage-sum boundary mid-year requires recalculation; some systems miss bracket shift.
- **Covered vs. uncovered allowances:** Some allowances are "WKR-covered" (exempt); others are taxable wages disguised as allowances → mixed treatment audit risk.
- **Multi-location employers:** If company operates in multiple branches, wage sum is cumulative across all locations.
- **Rounding:** Eindheffing is calculated on overage amount; rounding errors can trigger audit.

## Optimization Tactic

**Quarterly monitoring:** Calculate WKR free space after each quarter. If Q1–Q3 allowances + expected Q4 allowances would exceed space:
1. Halt new benefit issuance from Q4 onward
2. Or, reduce allowance amounts for remaining employees (proportional reduction acceptable)
3. Or, restructure as taxable wages (subject to income tax, but avoids 80% eindheffing penalty)

**Example:** Wage sum YTD €350k; Q4 projected €475k. Free space at 2.00% = €9,500. If current allowances €8,500, can add €1,000 in Q4; if €9,500, must halt new benefits.

---

## Cross-links

- `../05-rules-2026/thresholds.md` — WKR percentage brackets and wage-sum definition
- `../06-risks-sources/liability.md` — Payroll tax compliance and eindheffing audit risk

## Sources

- note3 (C18400–18550, C18550–18750, C18750–18950, C19000–19200): WKR scope, percentage brackets, allowance-coverage rules
