# Prompts: LLM Workflows for Daily Classification & Quarterly Scans

This folder contains complete, executable AI prompts for the Dutch tax skill. Each prompt is a usable template that can be invoked by an LLM agent (Claude or other) to classify transactions, scan for opportunities, generate accountant questions, and prepare year-end filings.

## Files

1. **categorization.md** (200 lines)
   - Daily expense classification for every imported bank transaction or invoice.
   - Outputs: classified expense category (RGS code), VAT rate, deductibility status, confidence, and required evidence.
   - When to load: On every new bookkeeping entry; before user review of suspicious transactions.
   - Typical runtime: <10 seconds per transaction.

2. **opportunity-scan.md** (220 lines)
   - Quarterly (Oct 1) and monthly (Nov–Dec) scan for Dutch tax planning opportunities.
   - Detects KIA/KOR/urencriterium/startersaftrek/WKR thresholds, MKB-winstvrijstelling, excessief lenen, WBSO candidates.
   - Outputs: ranked findings with tax impact estimate, evidence, and recommended reviewer.
   - When to load: Monthly Nov–Dec; after Q3 closes (before Q4 filings); whenever user requests opportunity review.
   - Typical runtime: 2–5 minutes for full quarter ledger.

3. **accountant-handoff.md** (200 lines)
   - Before quarterly VAT filing or annual close: generate crisp accountant questions, detect missing receipts, review proposed writeback changes.
   - Sub-prompts: Accountant Question Generator, Missing Receipt Detector, Safe Writeback Reviewer, Source Verification Agent, Rule-Update Monitor.
   - Outputs: prioritized questions [HIGH/MEDIUM/LOW] with documents needed; missing-receipt alerts with bonnetjesplicht/zakelijke factuur thresholds.
   - When to load: 2 weeks before accountant review; before VAT return filing; after year-end close.
   - Typical runtime: 3–10 minutes depending on queue size.

4. **year-end.md** (150 lines)
   - Annual year-end close and iXBRL export preparation.
   - Reconciles bank balances, VAT returns, revenue, expenses; computes Box 1 profit, ondernemersaftrek, MKB-winstvrijstelling, taxable income, heffingskortingen.
   - Flags variances >5%, missing documentation, private-use corrections, WKR/excessief breaches.
   - Outputs: iXBRL-ready export (requires human signature) + compliance checklist.
   - When to load: After year-end (Dec 31); before accountant deposit to KVK (Jan 31).
   - Typical runtime: 5–10 minutes; mandatory accountant signoff before filing.

5. **btw-quarterly.md** [Not included in this batch; reference in opportunity-scan and accountant-handoff as needed.]
   - VAT return prep: fills rubrieken 1a–5d, validates reverse-charge, cross-references invoices and VIES.

## Loading guidance

**Daily workflow:**
- Use `categorization.md` on every bank import and invoice upload.
- Link results to deterministic ledger engine in `references/03-architecture/deterministic-engine.md`.

**Quarterly workflow (Nov–Dec):**
- Oct 1: Run `opportunity-scan.md` for Q3 closing.
- Nov 1, Dec 1: Re-run `opportunity-scan.md` to catch threshold changes.
- 2 weeks before accountant review: Run `accountant-handoff.md`.

**Year-end workflow:**
- Dec 31 or Jan 5: Run `year-end.md` for final consolidation.
- Jan 15–20: Accountant signoff + KVK deposit.

## Integration points

- **Inputs**: All prompts consume outputs from the deterministic tax rules engine (`references/03-architecture/deterministic-engine.md`).
- **Outputs**: All prompts feed into `references/03-architecture/exception-handling.md` quarantine queues.
- **Risk flags**: Cross-link to `references/06-risks-sources/liability.md` for escalation criteria.
- **Rules & thresholds**: Reference `references/05-rules-2026/` for current-year numbers.

## Confidence & escalation

All prompts use a common outcome schema:
- **classified** / **assumed_conservative** / **needs_user_input** / **needs_accountant_review**
- Confidence level: high / medium / low
- Risk level: low / medium / high
- Mandatory reviewer flags for structural changes, innovation claims, and DGA decisions.

---

**Sources:** note1, note2, note3, deep-research-report
