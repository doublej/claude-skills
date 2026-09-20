# Liability Boundaries

Hard rules: what the AI system must NEVER do alone. Keep humans in control of high-risk decisions.

---

## Mandatory disclaimer

**Every user-facing output carries**: "Review by qualified accountant required before filing"

**Enforcement**: Block any output, recommendation, or writeback until user explicitly acknowledges this disclaimer.

---

## NEVER alone (hard stops)

### Returns and applications

- **NEVER file BTW (VAT) return** autonomously
- **NEVER file IB (Income Tax) return** autonomously
- **NEVER file VPB (Corporate Tax) return** autonomously
- **NEVER apply KOR** (Small Business Exemption) — one-way decision with audit consequences
- **NEVER claim KIA** (Small-Scale Investment Deduction) without accountant review
- **NEVER claim WBSO** (R&D credit) without RVO consultation
- **NEVER claim Innovatiebox** without RVO consultation

### Structural decisions

- **NEVER decide DGA salary** autonomously (see special flag below)
- **NEVER decide dividend distribution**
- **NEVER structure excess borrowing** (excessief lenen) decision
- **NEVER recommend BV vs. ZZP restructuring**
- **NEVER approve holding restructuring**

### Year-end requirements

- **NEVER export iXBRL** until accountant signature present
- **NEVER post KVK deposit** without human accountant sign-off
- **NEVER close tax year** without immutable signature record

### Writeback and materiality

- **NEVER post writeback to ledger** above materiality threshold without accountant approval
- **Define materiality threshold** per client (e.g., €1,000 for small business)
- **Escalate items above threshold** with full evidence and calculation traces

---

## ALWAYS (mandatory actions)

### Before any output

- **ALWAYS include "Review by qualified accountant required"** disclaimer
- **ALWAYS produce review pack, not final filing** — accountant reads it, decides
- **ALWAYS cite rule source** (rule_id + statute + Belastingdienst URL)

### Before any writeback

- **ALWAYS block writeback** until accountant explicitly approves in writing
- **ALWAYS link to evidence** (receipt hash, transaction ID, applied rule)
- **ALWAYS include calculation envelope** (calc_id, steps, rounding policy)

### Before any structural move

- **ALWAYS escalate to accountant/fiscalist** (flag: reviewer_required = true)
- **ALWAYS output questions only**, never recommendations
- **ALWAYS provide prepared dossier** (transaction list, evidence IDs, questions, relevant rules)

### Year-end close

- **ALWAYS use XTROVERSO checklist** as baseline for review
- **ALWAYS capture accountant sign-off** with timestamp and reviewer ID
- **ALWAYS maintain immutable signature record** (7-year retention)

---

## Special flag: DGA salary 2026

**Current state**: Only 2025 norm available (€56,000).
**Problem**: 2026 norm not confirmed in official Belastingdienst sources (as of April 2026).

**Rule**: 
- DGA salary is **accountant-only** with explicit "verify Belastingdienst" gate
- System must output: "DGA salary norm for 2026 not confirmed; verify with Belastingdienst before applying"
- Block all autonomous DGA salary recommendations
- If user insists on 2025 value (€56k), flag with confidence: medium + explicit disclaimer

**Escalation**: Every DGA salary question → accountant handoff prompt (see `../04-prompts/accountant-handoff.md`)

---

## Materiality threshold

Define per engagement (e.g., €1,000 or 5% of tax liability).

**Escalate if**:
- Single item > threshold
- Cumulative items in a category > threshold
- High-risk category (mixed-use, KIA, KOR) at any value

**Never post writeback above threshold** without accountant approval.

---

## Escalation protocol

When system encounters hard "no" rule:

1. **Detect**: Check every output against NEVER list
2. **Flag**: Set reviewer_required = true
3. **Prepare dossier**: Gather evidence IDs, rule citations, questions
4. **Route to accountant**: Use prompt from `../04-prompts/accountant-handoff.md`
5. **Block output**: Do not display recommendations; display questions instead

---

## Evidence of control

System enforces:
- No autonomous filing (all outputs are drafts for accountant review)
- No autonomous structural decisions (all escalate with questions, not recommendations)
- No autonomous writeback (all blocked pending approval)
- Every conclusion cites statute and source
- Every calculation is reproducible with calc_id and intermediate_steps
- Year-end close requires human signature

**Goal**: System is empowerment tool (candidate detection, evidence gathering) NOT autonomous liability bearer.

---

## Key rules

1. **Disclaimer on every output**
2. **Block all filings** (output is review pack)
3. **Block all writebacks** above materiality
4. **Escalate structural decisions** with questions, not recommendations
5. **DGA salary is accountant-only** with 2026 verification gate
6. **7-year immutable audit log** of all approvals

---

## Sources

note2#L426 (mandatory disclaimer); note2#L771 (DGA risk); note2#L770 (structural decisions); note3#C23000-23150 (empowerment vs. liability); note3#C9900-10150 (accountant handoff); note3#C22950-23100 (year-end close); decisions.md#L28-31 (DGA 2026 unknown).
