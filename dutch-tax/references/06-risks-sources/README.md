# Risks & Sources Reference

This folder contains critical risk mitigation strategies, liability boundaries, and source trust levels.

## When to load this folder

Load these documents **before any autonomous action** in these scenarios:

- User asks "can the AI do X autonomously?" or "should I automate this?"
- Any final-filing action (BTW return, IB return, VPB return)
- Year-end close and KVK deposit
- Structural changes (DGA salary, dividend distribution, entity restructuring)
- Audit-readiness questions ("are we compliant?", "what would Belastingdienst ask?")
- "Is this safe?" or "where does this number come from?"

## Three sibling documents

### 1. **compliance.md** (120 lines)
Belastingdienst audit posture and defensive practices.

**Topics**: 7-year retention, audit triggers, mixed-use risk, VAT correction 8-week deadline, BTW on food, conservative-default principle, mitigations (hashing, immutable stores, suppletie queue), audit-readiness contract.

**When**: Before any ledger filing, quarterly scanning, or when user asks about Belastingdienst risk.

---

### 2. **liability.md** (140 lines)
Hard boundaries: what the AI must NOT do alone.

**Rules**: Never file BTW/IB/VPB, never apply KOR unilaterally, never claim KIA without review, never recommend DGA salary, never decide dividends, never restructure entities, always include "qualified accountant" disclaimer, always block writeback until accountant approval, always escalate structural decisions.

**Special flag**: DGA salary 2026 norm unknown (only €56k for 2025 available); treat as accountant-only.

**When**: Before any output that could influence a filing or structural decision.

---

### 3. **source-table.md** (180 lines)
Master source trust matrix: 25+ sources grouped by trust level.

**Groups**: HIGH (Belastingdienst, RVO, KVK, 1truth, CBS, moneybird-mcp, exact-online-mcp), HIGH-COMMUNITY (RegelSpraak), MEDIUM-HIGH (Jortt, TaxHacker, picqer SDKs), MEDIUM (OpenAccountants, KiloClaw, SmartLedger), LOWER (GekkoBot, forums).

**For each**: URL, trust level, use case, caveats.

**When**: Before referencing any external source; use to justify or reject evidence.

---

## Cross-links

- **Tax opportunities**: `../02-tax-opportunities/dga-salary.md` (sensitive DGA rules)
- **Prompts**: `../04-prompts/accountant-handoff.md` (escalation template)
- **Rules 2026**: `../05-rules-2026/` (all numeric rules with source citations)

## Summary

**Compliance**: audit defense via documentation and deterministic rules.
**Liability**: hard "no" rules that keep humans in control.
**Sources**: evidence trust matrix to validate every claim.

Load together for complete risk posture before filing or automating.
