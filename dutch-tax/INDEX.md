# Dutch Tax Skill — Navigation Index

Personal scope: **ZZP (eenmanszaak)** + **BV / DGA**. Tax year **2026**.

```
~/.claude/skills/dutch-tax/
│
├── SKILL.md                           ← Router. Loads first. Read for routing rules.
├── INDEX.md                           ← This file.
├── _glossary.md                       ← NL acronyms (RGS, BTW, WKR, DGA, KOR, KIA…)
│
├── references/
│   │
│   ├── 01-existing-tools/             ← What's already built / reusable
│   │   ├── README.md
│   │   ├── mcp-servers.md             ── Moneybird MCP, Exact Online MCP, Belastbaar MCP, OmniZoek
│   │   ├── repos.md                   ── OpenAccountants, Speedy, TaxHacker, Claude Did My Taxes,
│   │   │                                 income-tax-optimizer, SmartLedger, Recite, RegelSpraak
│   │   └── platforms.md               ── Moneybird, Exact Online, e-Boekhouden, Jortt, Yuki, AFAS,
│   │                                     SnelStart, Twinfield, Rompslomp, KVK
│   │
│   ├── 02-tax-opportunities/          ← One concept per file. Cross-links to 05-rules-2026.
│   │   ├── README.md
│   │   ├── kia.md                     ── Kleinschaligheidsinvesteringsaftrek (€2,901–€71,683 = 28%)
│   │   ├── mkb-winstvrijstelling.md   ── 12.7% profit exemption (ZZP/VOF)
│   │   ├── zelfstandigenaftrek.md     ── €1,200 + startersaftrek €2,123, urencriterium 1,225h
│   │   ├── wbso-innovatiebox.md       ── R&D wage credit + 9% Innovatiebox VPB rate
│   │   ├── excessief-lenen.md         ── DGA loan cap €500,000
│   │   ├── representatiekosten.md     ── €5,700 cap or 80% IB / 73.5% VPB
│   │   ├── wkr.md                     ── Werkkostenregeling 2.00% / 1.18% free space
│   │   ├── btw-mixed-use.md           ── Private-use VAT correction, company car 2.7%/1.5%
│   │   └── dga-salary.md              ── Gebruikelijk loon (€56k 2025; verify 2026)
│   │
│   ├── 03-architecture/               ← How to build the AI bookkeeping system
│   │   ├── README.md
│   │   ├── deterministic-engine.md    ── Python tax math with hardcoded 2026 tables
│   │   ├── rgs-normalization.md       ── Referentie Grootboekschema mapping layer
│   │   ├── mcp-layer.md               ── Read-only-first ingestion via MCP
│   │   ├── exception-handling.md      ── classified / assumed_conservative / needs_input /
│   │   │                                 needs_accountant_review / blocked_out_of_scope
│   │   ├── evidence-logging.md        ── 7-year retention, calc_id trace, hash anchoring
│   │   └── roadmap.md                 ── Gap analysis, MVP phases, build-vs-buy decisions
│   │
│   ├── 04-prompts/                    ← LLM workflow prompts
│   │   ├── README.md
│   │   ├── categorization.md          ── Daily expense classifier with RGS + BTW
│   │   ├── opportunity-scan.md        ── Quarterly KIA/KOR/urencriterium/WKR/excessief scan
│   │   ├── accountant-handoff.md      ── Question generator for review pack
│   │   └── year-end.md                ── Annual close + iXBRL prep
│   │
│   ├── 05-rules-2026/                 ← The numbers. Source of truth for thresholds.
│   │   ├── README.md
│   │   ├── btw-rates.md               ── 0% / 9% / 21%, logies → 21% in 2026
│   │   ├── ib-brackets.md             ── Box 1 / Box 2 (24.5% / 31%) / Box 3 (1.28% / 6% / 2.70%)
│   │   ├── thresholds.md              ── KIA, KOR, zelfstandigenaftrek, startersaftrek, MKB,
│   │   │                                 urencriterium, representatiekosten, excessief lenen, WKR
│   │   └── deadlines.md               ── BTW Q, suppletie 8w, Prinsjesdag, KVK deposit, iXBRL
│   │
│   └── 06-risks-sources/              ← Compliance, liability, citations
│       ├── README.md
│       ├── compliance.md              ── 7-year retention, audit posture, mixed-use risk
│       ├── liability.md               ── AI cannot file alone; DGA = accountant-only
│       └── source-table.md            ── 25+ external sources with trust levels
│
└── _build/                            ← Auditable artifacts (DO NOT load on routine queries)
    ├── cycle1-extraction/             ── Per-file Haiku outlines
    ├── cycle2-merged/                 ── Per-topic merged outlines (7 files)
    └── decisions.md                   ── Synthesis decisions + contradiction resolutions
```

## Quick-fire routing examples

| Question | Files to load |
|---|---|
| "What's the 2026 KIA threshold?" | `02-tax-opportunities/kia.md` + `05-rules-2026/thresholds.md` |
| "Which MCP connects Moneybird?" | `01-existing-tools/mcp-servers.md` |
| "How do I detect a WKR breach?" | `02-tax-opportunities/wkr.md` + `04-prompts/opportunity-scan.md` |
| "Structure the deterministic engine?" | `03-architecture/deterministic-engine.md` |
| "Quarterly scan prompt?" | `04-prompts/opportunity-scan.md` |
| "Can the AI file my BTW?" | `06-risks-sources/liability.md` |
| "What's RGS?" | `_glossary.md` (then `03-architecture/rgs-normalization.md` if going deeper) |
| "Excessief lenen rules?" | `02-tax-opportunities/excessief-lenen.md` + `05-rules-2026/thresholds.md` |
| "Year-end iXBRL flow?" | `04-prompts/year-end.md` + `05-rules-2026/deadlines.md` |

## Reading order for first-time use

1. `SKILL.md` — routing rules, hard guardrails
2. `_glossary.md` — acronym crash course
3. `references/03-architecture/README.md` — system shape
4. `references/05-rules-2026/thresholds.md` — the 2026 numbers
5. `references/06-risks-sources/liability.md` — what AI MUST NOT do alone

After this, load files on-demand per the SKILL.md routing table.
