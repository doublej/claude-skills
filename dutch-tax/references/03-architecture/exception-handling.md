# Exception Handling & Outcome States

## One-line definition

Structured quarantine and action mapping for ambiguous transactions: five outcome states route items to auto-posting, staging, user input, accountant review, or out-of-scope blocking.

## Five outcome states

| State | Meaning | Auto-action | Next Step |
|-------|---------|-------------|-----------|
| **classified** | High confidence (≥90%); categorization is clear | Post to ledger after batch review | Accountant batch-reviews weekly |
| **assumed_conservative** | Medium confidence (70–89%); category is reasonable but not certain; system chose safer interpretation | Flag for accountant review; do not auto-post | Accountant confirms or corrects |
| **needs_user_input** | Low confidence or missing data; system cannot decide without user context | Quarantine; request user confirmation | User provides missing info (supplier name, ledger account, expense type) |
| **needs_accountant_review** | High uncertainty, policy decision, or professional judgment required | Escalate to accountant review pack | Accountant decides and documents rationale |
| **blocked_out_of_scope** | Outside system scope (e.g., WBSO eligibility, intercompany pricing, foreign permanent establishment) | Skip processing; do not queue | Refer user to specialist (WBSO advisor, international tax counsel) |

## State → action mapping

```yaml
classified:
  action: "auto_post_after_batch_review"
  batch_cadence: "weekly"
  confidence_threshold: 0.90
  example: "Invoice from office supply vendor for €150; category is clearly 6300 (Office Expenses)"

assumed_conservative:
  action: "flag_for_accountant_review"
  do_not_auto_post: true
  confidence_range: [0.70, 0.89]
  example: "Travel expense €230 with unclear business purpose; assuming 6400 (Travel) but accountant should verify"

needs_user_input:
  action: "quarantine_and_request_input"
  confidence_threshold: 0.70
  missing_fields:
    - supplier_name
    - expense_category
    - business_purpose
    - receipt_reference
  example: "Bank transaction €500 with reference 'MISC'. Missing supplier name and purpose."

needs_accountant_review:
  action: "escalate_to_accountant_pack"
  triggers:
    - mixed_personal_business
    - foreign_supplier_vat_rule
    - home_office_allocation
    - company_car_depreciation
    - related_party_transaction
  example: "Vehicle expense: personal use 30%, business use 70%. Accountant must confirm depreciation split."

blocked_out_of_scope:
  action: "refer_to_specialist"
  categories:
    - wbso_eligibility
    - innovatiebox_asset_qualification
    - intercompany_pricing
    - foreign_permanent_establishment
    - transfer_pricing
  example: "Transaction appears to be R&D investment; cannot auto-classify WBSO eligibility. Refer to WBSO specialist."
```

## Exception queues (14 categories)

| Queue | Description | Trigger Condition | Example |
|-------|-------------|-------------------|---------|
| **Missing receipt** | Expense > €50 without supporting document | Ledger amount > €50 AND receipt_id = NULL | Bank transfer €125, no invoice attached |
| **Low-confidence VAT** | VAT % cannot be determined from vendor type or invoice | LLM confidence < 0.70 on VAT rate | Imported service; reverse-charge rule ambiguous |
| **Foreign supplier** | Counterparty is outside NL; VAT reverse-charge may apply | Counterparty country != NL | Invoice from German software vendor |
| **Mixed personal/business** | Expense has both private and business components | Detector flags dual use OR user marks partial allocation | Rent: 20% personal apartment, 80% home office |
| **Home office** | Rent or utilities allocated to business use | Expense category in [rent, utilities, insurance] AND allocation % entered | Monthly rent allocation to business |
| **Vehicle** | Car, motorcycle, or delivery vehicle; depreciation or expense | Vendor contains [auto, car, fuel, maintenance] OR asset_class = vehicle | Monthly fuel: €200; or vehicle purchase €25,000 |
| **KIA near threshold** | YTD investments approaching KIA tiers (€2,901, €71,683, €398,236) | Assets in KIA-eligible categories + YTD sum within €5,000 of tier | Invested €69,000 in equipment; €71,683 threshold approaches |
| **DGA/shareholder loan** | Shareholder or DGA personal loan to company; excess-borrowing rule (€500k) applies | Loan_counterparty = shareholder OR dga AND loan > €0 | DGA withdrew €100,000 loan from company; accumulated €420,000 |
| **WBSO candidate** | Potential R&D project; WBSO tax benefit eligibility unclear | Payroll category OR project tag contains [research, development, R&D] AND uncertain scope | Engineering team spent Q1 on new product R&D |
| **Related party** | Transaction with related entity (spouse business, parent/subsidiary, joint venture) | Counterparty = related_party_flag OR company_relationship = related | Invoice from spouse's consulting company |
| **Large manual entry** | High-value transaction entered manually without automatic import | Entry_method = manual AND amount > €2,000 | User manually entered €5,000 office refit; no invoice yet |
| **Bank/invoice/ledger mismatch** | Transaction recorded in multiple places with different amounts or dates | amount_bank != amount_invoice OR date_diff > 3_days | Bank shows €2,100 received; invoice shows €2,000; ledger entry shows €1,900 |
| **Reverse-charge VAT unclear** | EU or third-country services; reverse-charge eligibility ambiguous | Counterparty outside NL AND service_type in [consulting, digital, license] | Digital marketing agency (London) invoice €3,000; VAT treatment unclear |
| **Incomplete transaction** | Required fields missing; system cannot proceed | Missing [amount, date, vendor, or category] AND entry_state = draft | Draft entry created; amount field empty |

## Confidence scoring (LLM layer)

When LLM classifies a transaction, emit confidence score:

```json
{
  "transaction_id": "txn_2026_04_29_001",
  "proposed_category": "6200 Operating Expense / Rent",
  "confidence_score": 0.87,
  "confidence_level": "medium",
  "reasoning": "Invoice from 'Amsterdam Business Centre' clearly indicates office rent; amount €2,500 aligns with typical commercial rent.",
  "alternative_categories": [
    {"category": "6300 Office", "confidence": 0.05, "reason": "Less likely; invoice says 'Rental Agreement' not office supplies"}
  ],
  "exception_queue": "assumed_conservative",
  "next_action": "Flag for accountant batch review"
}
```

## Accountant review pack structure

At month-end, compile exception queue into accountant review pack:

- **By queue:** Items grouped (e.g., "5 items needing receipt", "3 mixed-use decisions", "2 vehicle allocations")
- **Per item:** transaction_id, date, amount, proposed action, confidence score, user notes, evidence links
- **Summary:** Total items queued, distribution by queue type, materiality (sum of affected amounts)
- **Export format:** PDF or CSV for accountant review + spreadsheet with decision columns

## Confidence threshold tuning

- **Too high (≥95%):** Few false positives; risk: too many items escalated to accountant (overwhelms review).
- **Too low (≤60%):** Many false positives; risk: auto-posted errors; audit risk if incorrect assumptions baked in.
- **Recommended:** 90% for auto-post (classified), 70–89% for assumed_conservative, <70% for needs_user_input.

## Policy: never guess

- If LLM confidence drops below threshold → do not assume or invent category → quarantine.
- If receipt is missing → do not estimate amount → flag for user input.
- If foreign supplier VAT rule is ambiguous → do not assume reverse-charge → escalate to accountant.

---

**Sources:** note1, note3, deep-report
