# Tax Opportunities 2026

Reference guide to Dutch tax deductions and exemptions for ZZP, VOF, BV, and DGA entities. Each file covers a single opportunity with detection logic, pitfalls, and optimization tactics.

## Files

| File | Opportunity | Type | Who | Confidence |
|------|-------------|------|-----|-----------|
| `kia.md` | Investment allowance (28% or fixed + taper) | Deterministic | ZZP/VOF/BV | High |
| `mkb-winstvrijstelling.md` | MKB profit exemption (12.7%) | Deterministic | ZZP/VOF | High |
| `zelfstandigenaftrek.md` | Self-employment deduction + startersaftrek + hours test | Deterministic | ZZP | High |
| `wbso-innovatiebox.md` | R&D wage credit (WBSO) + 9% IP tax rate (Innovatiebox) | Heuristic | ZZP/BV | Medium |
| `excessief-lenen.md` | DGA loan cap (€500k) and Box 2 deemed dividend | Deterministic | BV/DGA | High |
| `representatiekosten.md` | Business gifts/meals (€5,700 or 73.5%–80% deduction) | Deterministic | All | High |
| `wkr.md` | Employee benefits free space (2.00% / 1.18%) | Deterministic | Employer | High |
| `btw-mixed-use.md` | VAT mixed-use (car 2.7% or 1.5%, phone, home office) | Heuristic | All | Medium |
| `dga-salary.md` | DGA reasonable salary (gebruikelijk loon) | Judgment | BV/DGA | Medium |

## When to load

**Quarterly bookkeeping scan:** Load all files. Use detection logic to flag candidates.  
**DGA salary determination:** Load `dga-salary.md` + `liability.md` for risk context.  
**Year-end planning:** Check `excessief-lenen.md` for loan threshold, `kia.md` for qualifying asset purchases, `wkr.md` for allowance limit.  
**Onboarding new client:** Read all files to understand tax landscape; use as checklist.

## Entry points

- **Start here if...** you need 2026 thresholds → read `thresholds.md` in `../05-rules-2026/`
- **Risk assessment** → cross-link to `../06-risks-sources/liability.md`
- **Automation strategy** → see `../03-architecture/deterministic-engine.md`
