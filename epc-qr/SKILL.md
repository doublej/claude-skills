---
name: epc-qr
description: Generate EPC QR codes for European banking payments (SEPA) as ASCII art. Auto-detects IBAN, amount, recipient name, and payment reference from conversation context. Use when user mentions SEPA payment, bank transfer, IBAN, or requests a payment QR code.
---

# EPC QR Code Generator

Generate EPC (European Payments Council) QR codes for SEPA banking payments. Output scannable ASCII QR codes directly in terminal.

## Quick Start

When user provides payment details, extract and validate fields, then generate QR code:

```
User: "Pay John Doe €50.00 to IBAN NL02ABNA0123456789 for invoice 2024-001"

→ Extract: IBAN=NL02ABNA0123456789, name="John Doe", amount=50.00, ref="invoice 2024-001"
→ Call script: echo '{"context": "Pay John Doe €50.00..."}' | python3 scripts/generate_epc_qr.py
→ Display ASCII QR code with confirmation message
```

## Field Detection

Auto-extract these fields from conversation context:

| Field | Required | Format | Max Length | Example |
|-------|----------|--------|------------|---------|
| IBAN | Yes | 2 letters + 2 digits + alphanumerics | 34 chars | DE89370400440532013000 |
| Beneficiary | Yes | Capitalized name | 70 chars | John Doe |
| Amount | No | Numeric (EUR only) | 999999999.99 | 50.00 |
| Reference | No | Text in quotes or after keywords | 140 chars | invoice 2024-001 |
| BIC | No | Bank identifier | 11 chars | DEUTDEFF |

### Detection Patterns

**IBAN**: Looks for pattern `[A-Z]{2}[0-9]{2}[A-Z0-9]+` with or without spaces

**Amount**: Matches `€50`, `50 EUR`, `50.00`, `50,00` (European comma decimal)

**Beneficiary**: Finds capitalized words near payment keywords (pay, to, for, beneficiary, recipient)

**Reference**: Extracts text in quotes or after keywords (reference, for, regarding, invoice)

## Validation Rules

### Format Checks
- IBAN: 15-34 chars, starts with 2 letters + 2 digits
- Amount: Positive, max 999999999.99 EUR
- Beneficiary: Required, max 70 chars
- Reference: Optional, max 140 chars

### Business Rules
- Currency: EUR only (EPC spec requirement)
- IBAN spaces: Stripped before validation
- Special characters: Sanitized to Latin-1 subset
- Single IBAN: If multiple IBANs found, ask user to clarify

## Usage Workflow

1. **Detect payment intent** from user message (keywords: pay, transfer, SEPA, IBAN, QR code)
2. **Extract fields** using patterns or explicit values from user
3. **Validate** required fields (IBAN, beneficiary)
4. **Generate** QR code via script
5. **Display** ASCII QR with confirmation message

### Confirmation Message Format

```
Scan this QR code with your banking app to pay [€AMOUNT] to [BENEFICIARY]
[for REFERENCE]

[ASCII QR CODE]

IBAN: [IBAN]
```

If amount is missing: "to pay [BENEFICIARY]" (no amount shown)

## Error Handling

### Missing Required Fields

**No IBAN**:
```
I found the amount (€100.00) and recipient (Maria Garcia), but I need an IBAN.
Please provide the recipient's IBAN (e.g., ES91 2100 0418 4502 0005 1332).
```

**No Beneficiary**:
```
I found the IBAN (DE89370400440532013000), but I need the recipient's name.
Who should receive this payment?
```

### Invalid Format

**Bad IBAN**:
```
Invalid IBAN format: XY123. IBANs start with 2 letters and 2 digits.
Example: DE89 3704 0044 0532 0130 00
```

**Bad Amount**:
```
Invalid amount: -50. Amount must be positive.
Use format like: 123.45 EUR or €123.45
```

### Ambiguity

**Multiple IBANs**:
```
Found multiple IBANs: DE89370400440532013000, NL02ABNA0123456789
Please specify which account to use.
```

## Script Reference

Execute `scripts/generate_epc_qr.py` with JSON input via stdin:

```json
{
  "context": "Full user message for auto-extraction",
  "iban": "Optional explicit IBAN",
  "beneficiary": "Optional explicit name",
  "amount": 50.00,
  "reference": "Optional reference text",
  "bic": "Optional BIC code"
}
```

**Output**: ASCII QR code to stdout OR error message to stderr

**Dependency**: `segno` library (`pip install segno`)

## Edge Cases

- **No amount**: Generate QR without amount (valid per EPC spec)
- **IBAN with spaces**: Spaces stripped automatically
- **European decimals**: Handle both `50.00` and `50,00` formats
- **Special characters**: Auto-sanitize to Latin-1 for EPC compatibility
- **Hidden IBANs**: Extract from formatted text or tables

## EPC Specification Notes

- Service tag: "BCD"
- Version: "002"
- Character set: UTF-8 with Latin-1 fallback
- Error correction: Level M (15%)
- Currency: EUR only (EPC spec requirement)
