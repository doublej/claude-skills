# Representatiekosten (Business Gifts & Meals) — 2026

**Definition:** Mixed-use entertainment/gift expenses capped at €5,700 annual deduction, OR deductible at 80% (income tax) / 73.5% (VPB), whichever is most favorable. Relatiegeschenken (business gifts) capped at €227 per recipient per year.

## 2026 Numbers (high confidence)

| Category | Limit | Deductibility |
|----------|-------|---------------|
| Representatiekosten total | €5,700/year | 100% OR 80% (IB) / 73.5% (VPB) — pick favorable |
| Relatiegeschenken per recipient | €227/year | Included in representatiekosten ceiling |
| On-premises food/drink (no clients present) | Not deductible | Disallowed as input VAT + representatiekosten |

## Eligibility & Scope

- **Who:** All entities (ZZP, VOF, BV, DGA)
- **What:** Client entertainment (meals, drinks, theater, gifts), business meals with business partners, promotional gifts under €227
- **What NOT:** Private staff parties (unless justified as business-necessity entertainment), personal gift-giving, entertainment without business purpose
- **VAT treatment:** Input VAT on representatiekosten is NOT recoverable (see pitfall below)

## Detection Logic

1. **Classify expenses** into representatiekosten (entertainment/gifts) vs. other business costs
2. **Filter for business purpose:** Must evidence relationship to client/business development
3. **Cap individual gifts:** Flag any single gift >€227 per recipient per year
4. **Aggregate annual:** Sum all representatiekosten expenses for fiscal year
5. **Choose deduction method:**
   - If total ≤ €5,700: deduct 100% (IB) or 73.5% (VPB)
   - If total > €5,700: deduct only €5,700 (IB) or calculate 80%/73.5% of €5,700, then compare to full 80%/73.5% of actual amount
6. **Flag if approaching ceiling:** Warn if Q4 spending suggests year-end overage

**Decision rule:** For BV (VPB), deduct 73.5% of €5,700 = €4,195.50. For ZZP/VOF (IB), deduct 80% of €5,700 = €4,560 OR 100% if under €5,700. Compare and pick maximum.

**Data required:** Receipt register with business purpose, attendee names, date, amount, VAT-per-item indicator.

## Pitfalls

- **Input VAT non-deductibility:** VAT paid on representatiekosten (meal VAT, gift VAT) CANNOT be deducted as input VAT. Mark as non-deductible on VAT return.
- **On-premises food trap:** Meals/drinks consumed on business premises (office, home office) without external clients present are NOT representatiekosten; they are private expenses or staff costs.
- **Gift over-cap:** Single gift >€227 per recipient in one year cannot be split across multiple years; full excess is non-deductible.
- **Client presence requirement:** Entertainment must involve actual or prospective client/business contact. Internal-only events (staff outing) are not representatiekosten.
- **Lack of documentation:** Missing receipts, unclear business purpose → Belastingdienst disallows entire category. Require itemized receipts with attendee names.
- **Currency mix:** If paying in foreign currency (e.g., meal abroad), convert to EUR at transaction date; apply cap in EUR.

## Examples

**Example 1 (ZZP, IB):**
- Client dinner: €300 (includes €50 VAT)
- Year-end gifts (5 clients × €150 each): €750
- Total representatiekosten: €1,050
- Deduction: min(€1,050, €5,700) × 80% = €840
- (VAT on meals is not deducted separately; already excluded from input VAT claim)

**Example 2 (BV, VPB):**
- Client entertainment + gifts: €6,500
- Over-cap by €800
- Best deduction: 73.5% × €5,700 = €4,190.50
- Excess €800: not deductible

**Example 3 (Single gift overage):**
- Client gift €300 to one recipient
- €227 deductible, €73 non-deductible (not gift-able to another person)

## Optimization Tactic

**Stay under €5,700:** Plan Q4 entertainment spending to remain below threshold, ensuring 100% deduction for ZZP or maximum percentage for BV. Example: If YTD is €5,400, cap Q4 to €300 to avoid overage penalties.

**Separate meal categories:** Distinguish representatiekosten from staff meals and private entertainment in bookkeeping to prevent mixing.

**Document business purpose:** For each expense, note attendee name, relationship to business, and business outcome (prospective client, existing client, partnership discussion).

---

## Cross-links

- `../05-rules-2026/thresholds.md` — Representatiekosten cap and relatiegeschenken limit
- `../06-risks-sources/liability.md` — Audit risk for business-purpose classification and VAT mishandling
- `btw-mixed-use.md` — Input VAT treatment for representatiekosten (non-deductible)

## Sources

- note1 (L181): €5,700 cap and deduction percentage
- note2 (L484): Relatiegeschenken €227 limit (confirmed for 2026)
- note3 (C17650–17800, C17800–18050, C18100–18300, C24650–24850): Eligibility, classification risk, Belastingdienst input-VAT rule
