# Evidence Logging & Audit Defense

## One-line definition

Comprehensive 7-year retention system with cryptographic linking between receipts, transactions, and applied tax rules; mandatory per Belastingdienst art. 52 AWR.

## Belastingdienst retention mandate

- **7-year retention rule (art. 52 AWR):** All business records (invoices, receipts, bank statements, ledger entries, tax calculations) must be retained for 7 years from tax filing date.
- **Burden of proof:** Entrepreneur must demonstrate how deductions, thresholds, and tax positions are supported by documentary evidence.
- **Digital audit trails:** If audited, Belastingdienst expects to trace:
  - Receipt → bank transaction → ledger entry → tax rule applied → calculation output → filing position.

## Per-finding metadata (required)

Every tax conclusion (KIA deduction, KOR reverse-charge, VAT correction, limited deduction) must emit:

```json
{
  "finding_id": "finding_2026_04_29_uuid",
  "tax_year": 2026,
  "entity_id": "zzp_001_company_abc",
  "entity_type": "ZZP",
  
  "tax_concept": "KIA_deduction",
  "input_records": [
    {
      "record_type": "ledger_entry",
      "record_id": "le_2026_04_001",
      "description": "Equipment purchase: computer",
      "amount": 1500,
      "date": "2026-02-15",
      "rgs_code": "1500"
    },
    {
      "record_type": "invoice",
      "record_id": "inv_vendor_xyz_2026_02",
      "supplier": "Tech Vendor XYZ",
      "amount": 1500,
      "vat": 315,
      "date": "2026-02-15"
    }
  ],
  
  "rule_version": "KIA-001-2026.04.01",
  "official_source_url": "https://www.belastingdienst.nl/zakelijk/...",
  
  "calculation_trace": {
    "module": "calculate_kia",
    "input_snapshot": {
      "profit_before_kia": 150000,
      "kia_eligible_assets": 85000,
      "entity_type": "ZZP"
    },
    "intermediate_steps": [
      {"step": "identify KIA-eligible assets", "value": 85000},
      {"step": "check profit threshold (€0)", "result": true},
      {"step": "apply 28% band (€2,901–€71,683)", "result": "€71,683 < €85,000"},
      {"step": "apply fixed + taper band", "kia_deduction": 20072, "taper": 625, "total": 20697}
    ]
  },
  
  "llm_extraction_trace": {
    "ocr_confidence": 0.95,
    "vendor_recognition": "high",
    "category_confidence": "high",
    "extracted_fields": {
      "supplier": "Tech Vendor XYZ",
      "amount": "€1.500",
      "vat_rate": "21%",
      "invoice_type": "equipment"
    }
  },
  
  "confidence": "high",
  "confidence_score": 0.93,
  
  "review_status": "approved",
  "reviewer_name": "Accountant Jan Jansen",
  "reviewer_email": "jan.jansen@firm.nl",
  "review_date": "2026-04-25",
  "reviewer_notes": "Equipment purchase confirmed. Asset register updated. KIA deduction eligible.",
  
  "final_action": "applied_to_filing",
  "filing_reference": "IB2026_entity_001",
  
  "created_at": "2026-04-29T14:32:00Z",
  "updated_at": "2026-04-25T09:00:00Z"
}
```

## Per-calculation metadata (required)

Every deterministic calculation (e.g., VAT return, KIA computation, Box 1 bracket) emits:

```json
{
  "calc_id": "calc_2026_q1_vat_001",
  "tax_concept": "VAT_return_aangifte",
  "tax_year": 2026,
  "period": "Q1_2026",
  
  "module": "vat_correction",
  "rule_ids": ["VAT-001", "VAT-002-reverse-charge"],
  "source_urls": [
    "https://www.belastingdienst.nl/btw/",
    "https://www.belastingdienst.nl/btw/omgekeerde-heffing/"
  ],
  
  "input_snapshot": {
    "revenue_gross": 45000,
    "revenue_vat": 9450,
    "expenses_gross": 15000,
    "expenses_vat": 3150,
    "reverse_charge_eu": 5000,
    "reverse_charge_vat": 0
  },
  
  "evidence_ids": [
    "ev_invoice_batch_q1_2026",
    "ev_bank_statement_q1_2026",
    "ev_supplier_list_eu"
  ],
  
  "intermediate_steps": [
    {"step": "collect Q1 invoices", "count": 32, "gross_revenue": 45000},
    {"step": "identify reverse-charge EU services", "count": 2, "amount": 5000},
    {"step": "calculate VAT on revenue (21%)", "vat": 9450},
    {"step": "calculate VAT on expenses (21%)", "vat_credit": 3150},
    {"step": "apply reverse-charge adjustment (0% on EU services)", "adjustment": 0},
    {"step": "compute net VAT owed", "net": 6300}
  ],
  
  "output_values": {
    "vat_owed": 6300,
    "currency": "EUR",
    "rounding_policy": "round_half_up",
    "due_date": "2026-05-20"
  },
  
  "generated_at": "2026-04-29T14:32:00Z",
  "engine_version": "2026.04.01"
}
```

## Cryptographic linking (future: hash anchoring)

For maximum audit defensibility, link evidence using content hashes:

```json
{
  "evidence_hash_chain": [
    {
      "evidence_id": "ev_receipt_vendor_xyz_2026_02_15",
      "evidence_type": "receipt_image_pdf",
      "content_hash_sha256": "a1b2c3d4...",
      "linked_to": ["txn_bank_2026_02_15_xyz", "ledger_entry_2026_02"]
    },
    {
      "evidence_id": "txn_bank_2026_02_15_xyz",
      "evidence_type": "bank_transaction",
      "content_hash_sha256": "b2c3d4e5...",
      "linked_to": ["ledger_entry_2026_02", "finding_kia_2026_04"]
    },
    {
      "evidence_id": "ledger_entry_2026_02",
      "evidence_type": "ledger_debit",
      "content_hash_sha256": "c3d4e5f6...",
      "linked_to": ["finding_kia_2026_04", "calc_kia_2026"]
    }
  ]
}
```

## Receipt OCR & vision extraction

- **Technology:** Claude 3.5 Sonnet vision model for OCR and field extraction.
- **Process:** Email or cloud storage ingestion → PDF/image upload → Claude vision → structured JSON extraction.
- **Extracted fields (mandatory):**
  - Supplier name, date, amount (gross), VAT amount, VAT %, ledger category suggestion.
- **Fallback:** If OCR confidence < 0.75, quarantine for manual review.
- **Storage:** Original receipt + OCR transcript both retained for 7 years.

## Evidence retention storage (7 years)

Choose one:

1. **Database + blob storage:** PostgreSQL for metadata (finding_id, calc_id, review_status), S3/Azure Blob for receipt images and PDFs.
2. **Document management system (DMS):** Moneybird integrates with DMS partners; consider third-party document archival.
3. **Flat-file archive (lower-tech):** ZIP containing findings JSON, receipts, and a manifest. Versioned per year; backed up off-site.

**Retention policy:** Minimum 7 years from end of tax year (Dutch law). Recommend 10 years for audit safety.

## Audit scenario: Belastingdienst request

If audited, system provides:

1. **Finding audit trail:** find_id → rule_id → rule_version → official source → calculation_trace → evidence_ids.
2. **Receipt trail:** transaction_id → bank posting → receipt OCR transcript → ledger entry.
3. **Calculation defensibility:** calc_id → input snapshot → step-by-step intermediate outputs → final output.

Example request: "Why did you claim €20,697 KIA deduction in 2026?"
Response: Finding_2026_04_uuid → rule KIA-001-2026.04.01 (source: belastingdienst.nl) → input profit €150k → intermediate steps (28% band calculation + taper logic) → output €20,697.

## Cross-links

- **Exception handling:** `exception-handling.md` — items in needs_accountant_review queue must have complete evidence logging before escalation.
- **Deterministic engine:** `deterministic-engine.md` — every calculation emits calc_id and rule_ids.
- **Accountant review:** `../01-existing-tools/*` — review pack export includes evidence_ids for accountant cross-reference.

---

**Sources:** note1, note3, deep-report
