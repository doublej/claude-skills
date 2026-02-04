#!/usr/bin/env python3
"""
EPC QR Code Generator
Generates EPC (European Payments Council) QR codes for SEPA banking payments.
"""

import sys
import json
import re
from typing import Optional


def extract_iban(text: str) -> Optional[str]:
    """Extract IBAN from text. Handles IBANs with or without spaces."""
    # Pattern: 2 letters + 2 digits + alphanumerics (15-34 total chars)
    patterns = [
        r'\b([A-Z]{2}[0-9]{2}[A-Z0-9\s]{11,30})\b',  # With optional spaces
        r'\b([A-Z]{2}[0-9]{2}[A-Z0-9]{11,30})\b',    # Without spaces
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text.upper())
        if matches:
            # Remove spaces and return first match
            return matches[0].replace(' ', '')
    return None


def extract_amount(text: str) -> Optional[float]:
    """Extract amount from text. Handles various European formats."""
    patterns = [
        r'€\s*(\d+[.,]\d{2})',           # €50.00 or €50,00
        r'EUR\s*(\d+[.,]\d{2})',         # EUR 50.00
        r'(\d+[.,]\d{2})\s*EUR',         # 50.00 EUR
        r'€\s*(\d+)',                    # €50
        r'(\d+)\s*EUR',                  # 50 EUR
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            amount_str = matches[0].replace(',', '.')
            try:
                return float(amount_str)
            except ValueError:
                continue
    return None


def extract_beneficiary(text: str) -> Optional[str]:
    """Extract beneficiary name from text using heuristics."""
    # Look for capitalized words near payment keywords
    payment_keywords = ['pay', 'to', 'for', 'beneficiary', 'recipient', 'transfer']

    # Pattern: capitalized words (likely names)
    name_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b'
    names = re.findall(name_pattern, text)

    if not names:
        return None

    # Find names near payment keywords
    for name in names:
        name_pos = text.find(name)
        context_start = max(0, name_pos - 50)
        context_end = min(len(text), name_pos + len(name) + 50)
        context = text[context_start:context_end].lower()

        for keyword in payment_keywords:
            if keyword in context:
                return name

    # Fallback: return first capitalized name found
    return names[0] if names else None


def extract_reference(text: str) -> Optional[str]:
    """Extract payment reference from text."""
    patterns = [
        r'reference[:\s]+(["\']?)([^"\']+)\1',
        r'for[:\s]+(["\']?)([^"\']+)\1',
        r'regarding[:\s]+(["\']?)([^"\']+)\1',
        r'invoice[:\s]+(["\']?)([^"\']+)\1',
        r'"([^"]+)"',
        r"'([^']+)'",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Extract the reference text (second group for most patterns)
            ref = matches[0][1] if isinstance(matches[0], tuple) and len(matches[0]) > 1 else matches[0]
            if ref and len(ref) > 3:  # Minimum length to avoid noise
                return ref.strip()
    return None


def validate_iban(iban: str) -> tuple[bool, Optional[str]]:
    """Validate IBAN format."""
    if not iban:
        return False, "IBAN is required"

    # Remove spaces
    iban = iban.replace(' ', '')

    # Check length
    if len(iban) < 15 or len(iban) > 34:
        return False, f"Invalid IBAN length: {len(iban)} (must be 15-34 characters)"

    # Check format: 2 letters + 2 digits + alphanumerics
    if not re.match(r'^[A-Z]{2}[0-9]{2}[A-Z0-9]+$', iban):
        return False, f"Invalid IBAN format: {iban}. IBANs start with 2 letters and 2 digits."

    return True, None


def validate_amount(amount: Optional[float]) -> tuple[bool, Optional[str]]:
    """Validate amount if provided."""
    if amount is None:
        return True, None  # Amount is optional

    if amount <= 0:
        return False, f"Invalid amount: {amount}. Amount must be positive."

    if amount > 999999999.99:
        return False, f"Invalid amount: {amount}. Maximum amount is 999999999.99 EUR."

    return True, None


def sanitize_text(text: str) -> str:
    """Sanitize text to Latin-1 subset for EPC compatibility."""
    # Remove or replace characters not in Latin-1
    try:
        return text.encode('latin-1').decode('latin-1')
    except UnicodeEncodeError:
        # Replace non-Latin-1 chars with closest ASCII equivalent
        import unicodedata
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        ).encode('latin-1', errors='ignore').decode('latin-1')


def generate_epc_qr(
    iban: str,
    beneficiary: str,
    amount: Optional[float] = None,
    reference: Optional[str] = None,
    bic: Optional[str] = None
) -> str:
    """Generate EPC QR code as ASCII art."""
    try:
        from segno import helpers
    except ImportError:
        return "Error: segno library not installed. Run: pip install segno"

    # Sanitize inputs
    iban = iban.replace(' ', '').upper()
    beneficiary = sanitize_text(beneficiary)
    if reference:
        reference = sanitize_text(reference)

    try:
        # Generate EPC QR code
        qr = helpers.make_epc_qr(
            name=beneficiary,
            iban=iban,
            amount=amount,
            text=reference,
            bic=bic,
        )

        # Return ASCII art
        return qr.terminal(compact=True)
    except Exception as e:
        return f"Error generating QR code: {str(e)}"


def main():
    """Main entry point."""
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())

        context = input_data.get('context', '')

        # Extract fields from context or use explicit fields
        iban = input_data.get('iban') or extract_iban(context)
        beneficiary = input_data.get('beneficiary') or extract_beneficiary(context)
        amount = input_data.get('amount') or extract_amount(context)
        reference = input_data.get('reference') or extract_reference(context)
        bic = input_data.get('bic')

        # Validate required fields
        if not iban:
            print("Error: No IBAN found. Please provide IBAN (e.g., DE89370400440532013000)", file=sys.stderr)
            sys.exit(1)

        valid, error = validate_iban(iban)
        if not valid:
            print(f"Error: {error}", file=sys.stderr)
            sys.exit(1)

        if not beneficiary:
            print("Error: No recipient name found. Please specify who receives the payment.", file=sys.stderr)
            sys.exit(1)

        valid, error = validate_amount(amount)
        if not valid:
            print(f"Error: {error}", file=sys.stderr)
            sys.exit(1)

        # Generate QR code
        qr_code = generate_epc_qr(iban, beneficiary, amount, reference, bic)

        # Output result
        print(qr_code)

    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
