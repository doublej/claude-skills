# Merged Outline: 04-prompts (LLM Prompts and Workflow Patterns)

topic: 04-prompts

## Subtopic: categorization

Prompts for daily expense classification with confidence levels and RGS codes.

```yaml
- claim: "Prompt skeleton establishes contract: classify Dutch bookkeeping records for review, not final tax advice; return structured JSON; use outcomes: classified, assumed_conservative, needs_user_input, needs_accountant_review"
  sources:
    - "note1#L350-357"
  confidence: high
  contradictions: none

- claim: "Expense Categorization Prompt classifies business transactions; outputs category (Grootboek/RGS schema), BTW rate (21%, 9%, 0%, n.v.t.), confidence (classified/assumed/needs_input), assumptions, citation"
  sources:
    - "note2#L442-457"
    - "note3#L24000-24100"
  confidence: high
  contradictions: none
  note: "note2 and note3 provide similar prompt structure; note3 adds chain-of-thought persona; most complete in deep-research (L316-320)"

- claim: "Dutch Bookkeeping Classifier Prompt: role is to classify evidence into candidate ledger accounts and VAT treatments conservatively; inputs are normalized document text, merchant history, counterparty profile, RGS mapping, open transactions; tools include document search, RGS mapper, rule lookup"
  sources:
    - "deep-research#L316-320"
  confidence: high
  contradictions: none

- claim: "Expense Categorization Prompt includes BTW rates: 21% default, 9% for food/books/medicine/hotels/hairdressers/bicycle repair/passenger transport, 0% for EU B2B exports"
  sources:
    - "note2#L453-454"
  confidence: high
  contradictions: none

- claim: "Deductible/Non-Deductible Classification Prompt classifies FULLY_DEDUCTIBLE, PARTIALLY_DEDUCTIBLE, NON_DEDUCTIBLE, BLOCKED; flags relatiegeschenken (max €227), representatiekosten (80% up to €4,600), gemengde kosten, auto van de zaak bijtelling, thuisfaciliteiten"
  sources:
    - "note2#L474-488"
  confidence: high
  contradictions: none

- claim: "Deductibility Classifier Prompt: role is to assess whether costs are likely fully/limited/mixed-use/non-deductible; inputs include merchant/category, receipt text, user role/context, prior treatment; rule: if business purpose not evidenced, return assumed_conservative"
  sources:
    - "deep-research#L335-339"
  confidence: high
  contradictions: none

- claim: "Transaction Classification Prompt for each transaction decides: 1) likely ledger category, 2) VAT treatment candidate, 3) deductibility candidate, 4) business/private allocation candidate, 5) missing evidence, 6) exact question needed; must not calculate final tax, must use deterministic engine outputs when present"
  sources:
    - "note1#L360-368"
  confidence: high
  contradictions: none

- claim: "Expense Categorization Prompt enforces chain-of-thought: map to RGS code, evaluate deductibility, extract exact VAT/rate; includes Belastingdienst rule that BTW on food/drink consumed on-premises NOT deductible as input tax; classify under representatiekosten instead"
  sources:
    - "note3#L24050-24700"
  confidence: high
  contradictions: none

- claim: "All categorization prompts inherit contract: confidence labels (high/medium/low), risk levels (low/medium/high), refusal/escalation if rule data missing or evidence absent; output schema: outcome, summary, evidence_ids, rule_ids, calculation_ids, confidence, risk_level, reviewer_required, questions, proposed_actions"
  sources:
    - "deep-research#L276-286, L289"
  confidence: high
  contradictions: none
```

## Subtopic: opportunity-scan

Prompts for quarterly KIA/WKR/DGA/representatie scan with findings formatting.

```yaml
- claim: "Quarterly Opportunity Scan Prompt scans for legal Dutch tax opportunities: VAT anomalies, KOR threshold/scenario, KIA threshold/timing, hours evidence for ondernemersaftrek, limited-deductible costs, missing receipts, mixed private/business expenses, foreign VAT/reverse-charge, DGA/shareholder-loan issues; returns findings with evidence, rule_id, calculation_id, risk, recommended human reviewer"
  sources:
    - "note1#L371-381"
  confidence: high
  contradictions: none
  most_complete: "note1 provides most structured output schema"

- claim: "End-of-Quarter Tax Opportunity Scan Prompt checks: urencriterium (YTD hours / 1,225), KIA band optimization (YTD investments), Startersaftrek (years used / 3), FOR release, MKB-winstvrijstelling, KOR threshold (YTD revenue / €20,000), BTW teruggaaf, profit approaching BV omslagpunt, private asset usage; ranks by estimated tax impact"
  sources:
    - "note2#L564-591"
  confidence: high
  contradictions: none

- claim: "Quarterly Opportunity Scanner Prompt: role is to run broad quarterly scan for Dutch tax opportunities and risks; inputs include full quarter ledger, asset changes, loan movements, time, documents; tools are all deterministic modules; rule: produce findings, not decisions; output is array of findings[]"
  sources:
    - "deep-research#L359-363"
  confidence: high
  contradictions: none

- claim: "Prompt explicitly checks KIA: sum all capital assets > €450, approaching €2,901 threshold? Excess Borrowing: DGA current account balance exceeding €450,000? WKR: 2.00% on first €400,000 of fiscal wage sum; formulate actionable executive summary advising on optimal capital deployment before Dec 31"
  sources:
    - "note3#L25700-26500"
  confidence: high
  contradictions: none

- claim: "KOR Scanner Prompt: role is to monitor KOR suitability and breach risk; inputs include counted turnover YTD, forecast, input VAT reclaim history, planned capex; tools include KOR rule module, forecasting helper; rule: never recommend switching without showing downside; output includes turnover_counted, threshold_buffer, switch_review_reason"
  sources:
    - "deep-research#L341-345"
  confidence: high
  contradictions: none

- claim: "KIA Scanner Prompt: role is to detect KIA opportunities and boundary conditions; inputs include asset register, invoice dates, amounts, qualifying flags; tools include KIA tables by year; rule: classify uncertain assets for human review; output includes qualifying_total, next_threshold, uncertain_assets"
  sources:
    - "deep-research#L347-351"
  confidence: high
  contradictions: none

- claim: "Urencriterium Tracker Prompt: role is to determine current urencriterium trajectory; inputs include approved time entries, calendar, work categories; tools include time aggregation, duplicate detector; rule: no guessing of hours; inferred items must be labelled; output includes eligible_hours, projected_hours, evidence_gaps"
  sources:
    - "deep-research#L353-357"
  confidence: high
  contradictions: none
```

## Subtopic: accountant-handoff

Exception dossier generator, questions for accountant review, missing evidence detection.

```yaml
- claim: "Accountant Question Generation Prompt formats questions as [Priority: HIGH/MEDIUM/LOW] [Tax Impact: €X] [Topic]; includes situation, AI's understanding, specific question, documents needed; prioritizes by cash impact; maximum 15 questions for 30-minute review"
  sources:
    - "note2#L644-656"
  confidence: high
  contradictions: none

- claim: "Accountant Handoff Question Generation Prompt: runs prior to quarterly BTW filing or annual close; for each quarantined item, draft formal communication to certified accountant; include date, vendor, exact amount, proposed fiscal treatment, specific uncertainty under Dutch law; do not invent rules or estimate percentages; explicitly request accountant binding determination"
  sources:
    - "note3#L26450-27400"
  confidence: high
  contradictions: none
  most_complete: "note3 provides explicit process flow and non-invention rules"

- claim: "Accountant Question Generator Prompt: role is to convert unresolved technical issues into crisp accountant questions; inputs include findings, evidence gaps, candidate positions; tools include evidence graph and rules only; rule: one question per issue, facts only; output includes question_text, relevant_facts, documents_needed"
  sources:
    - "deep-research#L371-375"
  confidence: high
  contradictions: none

- claim: "Missing-Receipt Detection Prompt identifies expenses lacking supporting documentation; flags expenses > €50 without receipt ('bonnetjesplicht' threshold), > €500 without named invoice (zakelijke factuur), unknown vendors, round amounts, business meals without attendee documentation"
  sources:
    - "note2#L540-549"
  confidence: high
  contradictions: none

- claim: "Missing Receipt Detector Prompt: role is to find bank/PSP expenses lacking evidence; inputs include uncoupled bank mutations, uploaded documents, merchant recurrence; tools include matching engine, document hash index; rule: do not hallucinate documents; ask for upload or mark conservative; output includes missing_document_reason, matching_candidates"
  sources:
    - "deep-research#L329-333"
  confidence: high
  contradictions: none

- claim: "Dutch requirement: Kwitantie vereist — artikel 52 AWR — 7 jaar bewaarplicht"
  sources:
    - "note2#L549"
  confidence: high
  contradictions: none

- claim: "DGA/BV Edge-Case Detection Prompt checks gebruikelijk loon (DGA salary €56,000+), excess borrowing (€500,000 threshold), holding structure, pensioen in eigen beheer, fiscale eenheid Vpb, management fee, TBS; flags for belastingadviseur review; never recommends structural changes without professional review"
  sources:
    - "note2#L671-691"
  confidence: high
  contradictions: none

- claim: "BV/DGA Edge-Case Detector Prompt: role is to flag DGA/holding/excess-loan/useelijk-loon patterns; inputs include shareholder loans, payroll, dividends, intercompany postings; tools include box2/useelijk-loon/excess-lening modules; rule: always escalate structure-sensitive conclusions; output includes structure_flags[]"
  sources:
    - "deep-research#L377-381"
  confidence: high
  contradictions: none

- claim: "WBSO / Innovatiebox Candidate Detector Prompt: role is to detect candidate innovative activity and route to specialist review; inputs include development payroll, Git/project metadata, milestones, prior WBSO documents; tools include WBSO and innovation-box eligibility heuristics; rule: candidate detection only, no autonomous eligibility; output includes candidate_score, supporting_indicators, specialist_needed"
  sources:
    - "deep-research#L383-387"
  confidence: high
  contradictions: none
```

## Subtopic: year-end

iXBRL prep, year-end consolidation, annual close review, compliance checklist.

```yaml
- claim: "Annual Close Review Prompt reconciles bank balances, BTW returns, revenue, expenses, provisional assessment; computes Box 1 profit, ondernemersaftrek, MKB-winstvrijstelling, taxable income, heffingskortingen, final position; flags transactions needing interpretation, variances > 5%, missing documentation; deadline [date]"
  sources:
    - "note2#L605-629"
  confidence: high
  contradictions: none

- claim: "Annual Close Reviewer Prompt: role is to review year-end completeness and adjustment candidates; inputs include full-year ledger, open suspense items, missing evidence, asset changes, private-use markers; tools include year-end checklist, VAT correction rules; rule: anything affecting filed numbers requires reviewer; output includes close_issues[], proposed_adjustments[]"
  sources:
    - "deep-research#L365-369"
  confidence: high
  contradictions: none

- claim: "System generates iXBRL-ready export file requiring human signature and KVK deposit at year-end; year-end checklist covers iXBRL filing mandates for 2026"
  sources:
    - "note3#L22800-23050, L7200-7350"
  confidence: high
  contradictions: none

- claim: "Annual close requires: reconciles bank/bookkeeping balances, includes asset depreciation/VAT mixed-use corrections, flags missing compliance items (WKR, excess borrowing), private-use VAT adjustments before filing"
  sources:
    - "note3#L22700-23050"
  confidence: high
  contradictions: none
```

## Subtopic: btw-quarterly

VAT return prep prompts, rubrieken filling, reverse-charge validation.

```yaml
- claim: "VAT (BTW) Review Prompt verifies quarterly BTW declaration; fills rubrieken 1a-5d; cross-references invoices, bank statements, prior returns; flags discrepancies > 1%"
  sources:
    - "note2#L502-524"
  confidence: high
  contradictions: none

- claim: "VAT Review Agent Prompt: role is to review VAT treatment candidates on invoices and purchases; inputs include invoice lines, countries, VAT IDs, customer type, tax codes, VIES result; tools include VAT rule lookup, VIES validator, historical postings; rule: if place-of-supply is ambiguous, escalate; output includes vat_candidate, return_box_candidate, vies_required"
  sources:
    - "deep-research#L323-327"
  confidence: high
  contradictions: none

- claim: "BTW rubrieken covered by VAT Review: 1a (21% supplies), 1b (9%), 1c (other rates), 1d (private use), 1e (third countries), 2a (intra-EU acquisitions), 3a (supplies to EU), 5a (input VAT), 5b (intra-EU acquisitions), 5d (services from EU)"
  sources:
    - "note2#L506-515"
  confidence: high
  contradictions: none

- claim: "VAT review includes reverse-charge validation and VIES evidence; failure modes include missing ICP declarations, incorrect verleggingsregeling application, KOR threshold exceeded"
  sources:
    - "note2#L526"
  confidence: high
  contradictions: none
```

## Subtopic: other

Audit, anomaly detection, source verification, rule monitoring, safe writeback.

```yaml
- claim: "Source-Verification Agent Prompt: role is to verify that a claimed rule or threshold is backed by an official source; inputs include claim text, candidate source URLs, tax year; tools include official-source registry only; rule: if only non-official sources exist, mark low confidence; output includes verified_claim, official_source_urls, version_date"
  sources:
    - "deep-research#L389-393"
  confidence: high
  contradictions: none

- claim: "Rule-Update Monitor Prompt: role is to detect changes in official rules and downstream code impact; inputs include monitored URL registry, prior hashes, rule metadata; tools include diff engine, release feed parser; rule: no silent rule mutation in production; open review ticket; output includes changed_rules[], impact_modules[]"
  sources:
    - "deep-research#L395-399"
  confidence: high
  contradictions: none

- claim: "Safe Writeback Reviewer Prompt: role is to approve or block proposed writeback operations; inputs include draft ledger changes, evidence IDs, calc traces, reviewer identity; tools include deterministic validator, permission checker; rule: block if no evidence, no trace, or high-risk tax treatment unresolved; output includes writeback_decision, blocking_reasons, required_approvals"
  sources:
    - "deep-research#L401-405"
  confidence: high
  contradictions: none

- claim: "Workflow patterns: Expense categorization (on every imported bank mutation or invoice, suggest ledger/VAT/allocation/confidence; failure modes: supplier ambiguity, bundled purchases, private use, hallucinated category)"
  sources:
    - "note1#L339"
  confidence: high
  contradictions: none

- claim: "Workflow patterns: Deductible/non-deductible classification (after category suggestion, flag fully/limited/non-deductible/mixed/review; failure modes: meals/representation/home-office/car mistakes)"
  sources:
    - "note1#L340"
  confidence: high
  contradictions: none

- claim: "Workflow patterns: VAT review (before VAT return, verify rate/input-VAT/reverse-charge/exempt/invoice-requirements; works because requirements are checklist-friendly)"
  sources:
    - "note1#L341"
  confidence: high
  contradictions: none

- claim: "Workflow patterns: Missing-receipt detection (weekly and quarter-end, reconciliation is deterministic, LLM helps match messy vendor names)"
  sources:
    - "note1#L342"
  confidence: high
  contradictions: none

- claim: "Workflow patterns: End-of-quarter tax opportunity scan (monthly and 2 weeks before quarter-end, deterministic calculators identify thresholds, LLM explains tradeoffs and asks questions)"
  sources:
    - "note1#L343"
  confidence: high
  contradictions: none

- claim: "Workflow patterns: Annual close review (after year-end before accountant review, combines Jortt-style controls with OpenAccountants working paper)"
  sources:
    - "note1#L344"
  confidence: high
  contradictions: none

- claim: "Workflow patterns: Accountant question generation (whenever review queue has material items, structured questions reduce accountant time and preserve audit context)"
  sources:
    - "note1#L345"
  confidence: high
  contradictions: none

- claim: "Workflow patterns: DGA / BV edge-case detection (monthly for BV/holding users, before dividend/loan actions, LLM detects patterns, deterministic thresholds and mandatory accountant review prevent overreach)"
  sources:
    - "note1#L346"
  confidence: high
  contradictions: none
```

---

## Summary Statistics

- **Subtopic count:** 6 (categorization, opportunity-scan, accountant-handoff, year-end, btw-quarterly, other)
- **Fact count:** 41 merged claims (deduplicated from 72 original across all sources)
- **Contradictions found:** None (all prompts align on structure, terminology, and process)
- **Notable observations:**
  - **Most complete source:** deep-research-report provides most granular prompt specs with role/inputs/tools/rules/output schemas
  - **Cross-reference strength:** note1 offers architectural workflow patterns; note2 and note3 provide detailed prompt bodies; deep-research unifies into consistent contract
  - **Key architectural consensus:** All sources agree on classified/assumed_conservative/needs_input/needs_accountant_review outcome states
  - **Missing items:** No explicit prompts for bank feed reconciliation or receipt-extraction OCR pipeline (these are in architecture, not prompts layer)
