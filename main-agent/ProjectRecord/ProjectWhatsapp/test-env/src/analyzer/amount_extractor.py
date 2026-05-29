"""Extract monetary amounts from OCR text."""
import re
from decimal import Decimal, InvalidOperation

_AMOUNT_PATTERNS = [
    re.compile(r"HK\$\s*([\d,]+(?:\.\d{1,2})?)"),
    re.compile(r"\$\s*([\d,]+(?:\.\d{1,2})?)"),
    re.compile(r"([\d,]+(?:\.\d{1,2})?)\s*蚊"),
    re.compile(r"([\d,]+(?:\.\d{1,2})?)\s*元"),
]


class AmountExtractor:
    def extract(self, text: str) -> Decimal | None:
        if not text:
            return None
        for pattern in _AMOUNT_PATTERNS:
            match = pattern.search(text)
            if match:
                return _parse_amount(match.group(1))
        return None


def _parse_amount(raw: str) -> Decimal | None:
    try:
        return Decimal(raw.replace(",", ""))
    except (InvalidOperation, ValueError):
        return None


def extract_amounts(text: str) -> list[Decimal]:
    """Extract all monetary amounts from text (deduplicated)."""
    if not text or not text.strip():
        return []
    results = []
    seen = set()
    for pattern in _AMOUNT_PATTERNS:
        for match in pattern.finditer(text):
            amount = _parse_amount(match.group(1))
            if amount is not None and amount not in seen:
                results.append(amount)
                seen.add(amount)
    return results
