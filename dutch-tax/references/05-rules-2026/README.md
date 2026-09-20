# 2026 Tax Rules Reference

This folder contains the authoritative 2026 Dutch tax thresholds, rates, and deadlines used throughout the skill.

## Purpose

**Numbers in this folder are the single source of truth for the skill.** When a leaf document (e.g., `02-tax-opportunities/kia.md`) needs to state a 2026 threshold, it references these files. When you update the skill for 2027, start here.

## Files

1. **`btw-rates.md`** — VAT rates (0%, 9%, 21%), logies move to 21%, KOR threshold, input tax rules, suppletie requirement.
2. **`ib-brackets.md`** — Income tax (Box 1–3) rates, allowances, innovatiebox effective rates.
3. **`thresholds.md`** — Master lookup table: KIA bands, KOR, MKB winstvrijstelling, zelfstandigenaftrek, startersaftrek, urencriterium, representatiekosten, relatiegeschenken, WKR percentages, excessief lenen, DGA salary, bonnetjesplicht, factuurplicht.
4. **`deadlines.md`** — BTW filing, suppletie window, Prinsjesdag, KVK iXBRL, annual accounting closure, 7-year retention.

## How to use this folder

- **Leaf documents reference these files** with hard links: `[KIA rules](../05-rules-2026/thresholds.md)`
- **When a user asks a 2026 tax question**, route to the specific file (e.g., "What's the KIA investment range?" → `thresholds.md`, search "KIA")
- **When you verify a number against live data**, update the confidence tag and leave a dated note in the file
- **Before final filing**, users MUST verify these values against [Belastingdienst.nl](https://www.belastingdienst.nl) — rules may change between Prinsjesdag and tax-year start

## Critical verification notes

- **Box 1 Bracket 1 (35.75%)** — one source only; verify against Belastingdienst before relying
- **DGA gebruikelijk loon (€56,000)** — 2025 baseline; 2026 equivalent not yet confirmed from official sources
- **Logies rate change to 21%** — confirmed from 2026 announcements
- **Excessief lenen €500,000** — stepped down from €700,000 in 2023; this is 2026 correct value

## Sources

These numbers are synthesized from:
- Belastingdienst official guidance
- Dutch tax administration publicly available rates
- 2026 budget announcements and legislative changes
- MCP server tax data (Belastbaar for 2024–2025; 2026 pending)

## When rules change

Prinsjesdag (Budget Day, mid-September) is when the Dutch government announces rule changes for the coming fiscal year. **Update this folder immediately after Prinsjesdag when 2027 rules are announced.** Do not wait for the calendar year to turn.

---

**Last reviewed:** 29 April 2026 | **Confidence:** High for most 2026 rates; medium for derived values (DGA, Box 1 detailed brackets) — always double-check before filing.
