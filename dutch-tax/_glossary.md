# Glossary — NL Fiscal Acronyms

Quick lookup. For deeper context, follow the cross-link.

## Tax bodies / standards

| Term | Meaning | Where used |
|---|---|---|
| **Belastingdienst** | Dutch Tax Authority. Source of truth for rates, brackets, audits. | `06-risks-sources/source-table.md` |
| **KVK** | Kamer van Koophandel — Chamber of Commerce. Business registration. | `01-existing-tools/platforms.md` |
| **RVO** | Rijksdienst voor Ondernemend Nederland — manages WBSO/Innovatiebox/EIA/MIA. | `02-tax-opportunities/wbso-innovatiebox.md` |
| **CBS** | Centraal Bureau voor de Statistiek. Co-owner of RGS taxonomy. | `03-architecture/rgs-normalization.md` |
| **RGS** | Referentie Grootboekschema — universal Dutch chart of accounts (linked to SBR). | `03-architecture/rgs-normalization.md` |
| **SBR** | Standard Business Reporting — Dutch normalized accounting/filing standard. | `03-architecture/rgs-normalization.md` |
| **XAF** | XML Auditfile Financieel (currently 4.0) — Belastingdienst audit/exchange file format. | `01-existing-tools/repos.md` |
| **Digipoort** | Filing transport gateway — used to submit BTW/IB/VPB to Belastingdienst. | `04-prompts/year-end.md` |
| **iXBRL** | Inline XBRL — KVK annual deposit format. | `04-prompts/year-end.md`, `05-rules-2026/deadlines.md` |
| **RegelSpraak** | Belastingdienst's controlled natural language for executable tax rules. | `01-existing-tools/repos.md` |
| **Prinsjesdag** | Dutch Budget Day — annual tax-rule update event. Triggers rule re-versioning. | `05-rules-2026/deadlines.md` |

## Entity types

| Term | Meaning |
|---|---|
| **ZZP** | Zelfstandige Zonder Personeel — sole proprietor without employees. |
| **Eenmanszaak** | Sole proprietorship (legal entity). Most ZZP'ers operate as eenmanszaak. |
| **VOF** | Vennootschap Onder Firma — general partnership. |
| **BV** | Besloten Vennootschap — Dutch private limited company. |
| **Holding** | BV that holds shares in operating BV(s). Common DGA tax structure. |
| **DGA** | Directeur-Grootaandeelhouder — director-major-shareholder of a BV. |
| **Fiscale eenheid** | Fiscal unity — multi-BV consolidation for VPB. |

## Tax types / boxes

| Term | Meaning |
|---|---|
| **IB** | Inkomstenbelasting — personal income tax. |
| **VPB / Vpb** | Vennootschapsbelasting — corporate income tax (BV). |
| **BTW** | Belasting Toegevoegde Waarde — VAT. Rates: 0%, 9%, 21%. |
| **Box 1** | IB on labor + entrepreneur income. Progressive (35.75% bracket 1 in 2026). |
| **Box 2** | IB on substantial-interest (DGA) income. 24.5% / 31% in 2026. |
| **Box 3** | IB on savings/investments. Deemed-return: 1.28% / 6% / 2.70% (2026). |

## Deductions / regimes

| Term | Meaning | Cross-link |
|---|---|---|
| **KIA** | Kleinschaligheidsinvesteringsaftrek — small-scale investment deduction. | `02-tax-opportunities/kia.md` |
| **KOR** | Kleineondernemersregeling — VAT exemption ≤ €20,000 turnover. | `05-rules-2026/btw-rates.md` |
| **MKB-winstvrijstelling** | SMB profit exemption — 12.7% of profit (after ondernemersaftrek). | `02-tax-opportunities/mkb-winstvrijstelling.md` |
| **Zelfstandigenaftrek** | Self-employed deduction — €1,200 (2026) if urencriterium met. | `02-tax-opportunities/zelfstandigenaftrek.md` |
| **Startersaftrek** | Starter deduction — €2,123 add-on, max 3 of first 5 years. | `02-tax-opportunities/zelfstandigenaftrek.md` |
| **Urencriterium** | Hours criterion — ≥1,225 h/year required for ZZP deductions. | `02-tax-opportunities/zelfstandigenaftrek.md` |
| **Ondernemersaftrek** | Umbrella term for entrepreneur deductions (incl. zelfstandigenaftrek + startersaftrek). | `02-tax-opportunities/zelfstandigenaftrek.md` |
| **WBSO** | Wet Bevordering Speur- en Ontwikkelingswerk — R&D wage tax credit. | `02-tax-opportunities/wbso-innovatiebox.md` |
| **Innovatiebox** | Effective 9% VPB rate on qualifying IP profits. | `02-tax-opportunities/wbso-innovatiebox.md` |
| **Excessief lenen** | DGA excess-borrowing rule — loans > €500,000 trigger Box 2 deemed dividend. | `02-tax-opportunities/excessief-lenen.md` |
| **WKR** | Werkkostenregeling — work-cost scheme (free space 2.00% / 1.18%). | `02-tax-opportunities/wkr.md` |
| **Representatiekosten** | Entertainment/business gifts — €5,700 cap or 80% IB / 73.5% VPB. | `02-tax-opportunities/representatiekosten.md` |
| **Gebruikelijk loon** | DGA "customary salary" norm. | `02-tax-opportunities/dga-salary.md` |
| **FOR** | Fiscale Oudedagsreserve — old-age reserve. **Abolished new contributions from 2023**; only release rules apply. | `02-tax-opportunities/zelfstandigenaftrek.md` |
| **EIA / MIA / Vamil** | Energy / environment / accelerated-depreciation investment schemes (RVO). | `02-tax-opportunities/kia.md` |
| **Bijtelling** | Private-use addition to income for company car. | `02-tax-opportunities/btw-mixed-use.md` |
| **Suppletie** | VAT correction form. Required for corrections > €1,000. | `05-rules-2026/deadlines.md` |
| **Bonnetjesplicht** | Receipt obligation — receipts mandatory for expenses > €50. | `04-prompts/categorization.md` |
| **TBS-regeling** | Terbeschikkingstellingsregeling — assets/loans made available by DGA to own BV. | `02-tax-opportunities/dga-salary.md` |
| **30%-regeling** | 30% facility for incoming foreign employees. | `01-existing-tools/repos.md` |

## VAT / cross-border

| Term | Meaning |
|---|---|
| **BTW verlegd** | Reverse-charge VAT — supplier doesn't charge, buyer self-accounts. |
| **ICP** | Intracommunautaire Prestaties — intra-EU supplies declaration. |
| **VIES** | EU VAT-ID validation system. |
| **Rubrieken** | Sections of the BTW return (1a, 1b, 1c, 1d, 1e, 2a, 3a, 5a, 5b, 5d). |

## Architecture / pipeline

| Term | Meaning | Cross-link |
|---|---|---|
| **MCP** | Model Context Protocol — Anthropic's tool-use protocol. Used for Moneybird/Exact ingestion. | `03-architecture/mcp-layer.md` |
| **classified** | Outcome state: confident classification, eligible for auto-post after batch review. | `03-architecture/exception-handling.md` |
| **assumed_conservative** | Outcome state: defaulted to safer treatment when uncertain; flagged for accountant. | `03-architecture/exception-handling.md` |
| **needs_user_input** | Outcome state: missing evidence or context; ask user. | `03-architecture/exception-handling.md` |
| **needs_accountant_review** | Outcome state: high-risk treatment; escalate. | `03-architecture/exception-handling.md` |
| **blocked_out_of_scope** | Outcome state: skill explicitly refuses (e.g. structural BV decisions). | `03-architecture/exception-handling.md` |
| **calc_id** | Unique identifier for each deterministic calculation, captured in evidence log. | `03-architecture/evidence-logging.md` |
| **finding_id** | Unique identifier for each tax conclusion produced by the pipeline. | `03-architecture/evidence-logging.md` |
