# Synthesis Decisions & Contradiction Resolutions

Generated during Cycle 3 (Opus synthesis). Records every non-trivial choice that shaped the skill tree.

## Tree shape decisions

- **6 numbered top-level reference folders** instead of 7. Cycle-2 topic 06 (build-vs-buy) folded into `references/03-architecture/roadmap.md`, since gap-analysis and MVP phases are architectural concerns, not user-facing tax questions. The Cycle-2 topic 07 (risks-sources) becomes folder `06-risks-sources/`.
- **`dga-salary.md` promoted to its own leaf** in `02-tax-opportunities/`. The plan's tree didn't list it explicitly, but the merged outline gave it enough mass and the topic is too sensitive to fold into representatie/excessief.
- **Build-vs-buy NOT a separate folder.** All consumer questions about "what should I use vs build?" route through `03-architecture/roadmap.md` plus `01-existing-tools/*` for tool inventory.

## Contradictions resolved

### KIA threshold (note1 vs note3 differed)
- note1: "€2,901 to €398,236"
- note3: "€2,901 to €71,683 → 28% deduction"
- **Resolution**: BOTH correct, different bands. €2,901–€71,683 is the **28% percentage band**. €71,684–€398,236 is the **fixed €20,072 + taper** band. Both documented in `references/02-tax-opportunities/kia.md`. Source: note3 explicit + note1 confirms upper bound of €398,236.

### Excessief lenen threshold (€500k vs €700k)
- note2: €700,000
- note1, note3, deep-report: €500,000
- **Resolution**: €500,000 for 2026. €700k was the 2023 value before the 2024 step-down. note2's value is stale. All references use €500,000; note2 contradiction is recorded for audit but not surfaced to users.

### Zelfstandigenaftrek amount (€1,200 vs €2,470)
- note2: €2,470 for **2025**
- note1, note3: €1,200 for **2026**
- **Resolution**: No contradiction — different years. The amount is on a multi-year step-down toward 2027 abolition. 2026 = €1,200. 2026 is the canonical value used everywhere.

### DGA gebruikelijk loon norm (€56k 2025; 2026 unknown)
- note2: €56,000 (2025)
- No source provides 2026 value
- **Resolution**: Document the 2025 baseline AND explicitly flag in `references/02-tax-opportunities/dga-salary.md` and `references/06-risks-sources/liability.md` that the 2026 value must be verified against Belastingdienst before any DGA salary determination. Confidence: medium.

### Box 1 Bracket 1 rate 35.75% (note3 only)
- note3 explicit
- note2 says Belastbaar MCP only has 2024–2025 data
- **Resolution**: 35.75% recorded with `confidence: medium` flag in `references/05-rules-2026/ib-brackets.md`. Reader directed to verify against Belastingdienst before relying on it.

### Representatiekosten threshold (€5,700 vs €4,600)
- note2: 80% up to €4,600 (older threshold)
- note1, note3: €5,700 for 2026
- **Resolution**: €5,700 is 2026 canonical. €4,600 was older; treat as stale.

## Authoritative ranking of sources

When sources disagree on a 2026 number, prefer in this order:

1. **deep-research-report (6).md** — most polished, explicit sourcing, latest revision
2. **note1.md** — exec summary with ranked findings, often most current
3. **note3.md** — same content as deep-report (single-line variant)
4. **note2.md** — synthesis with stale 2025/2023 values mixed in

## Style guide for leaf documents

- **Length**: 80–250 lines per leaf. Single concept per file.
- **Structure** (when applicable):
  1. One-line definition
  2. **2026 numbers** (verbatim, with currency/unit)
  3. **Eligibility** / who it applies to (ZZP / VOF / BV / DGA)
  4. **Detection logic** — how the AI spots the opportunity / risk in bookkeeping data
  5. **Pitfalls** — non-obvious caveats
  6. **Action / optimization tactic** — what the user should do
  7. **Cross-links** — `references/...` paths to related leaves
  8. **Sources** — citations to source files (note1, note2, note3, deep-report)
- **Currency**: EUR with `€` symbol, no thousand-separator inconsistency (use comma per NL: €71,683 in prose, €71683 in code).
- **Confidence**: Mark `(high)` / `(medium)` / `(low)` when stating year-specific numbers.
- **No comments in numbers**: never inline-justify a number with parenthetical explanations the user didn't ask for.

## What got cut

- **Audit anomaly detection prompts** beyond what's in `04-prompts/opportunity-scan.md` — too speculative across sources.
- **VOF-specific rules** — mentioned briefly in glossary, not deep-doc'd per user scope.
- **Implementation code** for the deterministic engine — architecture documents how, user implements separately. Per plan's "out of scope".
- **Translation to Dutch** — kept English per plan; multilingual users can translate on demand.

## Smoke-test queries (Cycle 5 will validate these)

1. "What's the KIA threshold for 2026?" → `02-tax-opportunities/kia.md` + `05-rules-2026/thresholds.md`
2. "Which MCP server connects Moneybird?" → `01-existing-tools/mcp-servers.md`
3. "How should I structure the deterministic tax engine?" → `03-architecture/deterministic-engine.md`
4. "What prompt do I use for quarterly scanning?" → `04-prompts/opportunity-scan.md`
5. "Can the AI file my BTW return directly?" → `06-risks-sources/liability.md`
