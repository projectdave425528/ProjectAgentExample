"""Extract monetary amounts from OCR text."""
import re
from decimal import Decimal, InvalidOperation


# Patterns ordered from most specific to least specific
_AMOUNT_PATTERNS = [
    # HK$1,000.50 or HK$500
    re.compile(r"HK\$\s*([\d,]+(?:\.\d{1,2})?)"),
    # $1,000.50 or $500
    re.compile(r"\$\s*([\d,]+(?:\.\d{1,2})?)"),
    # 500蚊 or 1,000蚊
    re.compile(r"([\d,]+(?:\.\d{1,2})?)\s*蚊"),
    # 500元 or 1,000元
    re.compile(r"([\d,]+(?:\.\d{1,2})?)\s*元"),
]


class AmountExtractor:
    """Extracts monetary amounts from OCR text."""

    def extract(self, text: str) -> Decimal | None:
        """Extract the first monetary amount found in text.

        Args:
            text: OCR-extracted text to search.

        Returns:
            Decimal amount or None if no amount found.
        """
        if not text:
            return None
        for pattern in _AMOUNT_PATTERNS:
            match = pattern.search(text)
            if match:
                return self._parse_amount(match.group(1))
        return None

    def _parse_amount(self, raw: str) -> Decimal | None:
        """Parse a raw amount string into Decimal.

        Removes thousand separators and converts to Decimal.
        """
        try:
            cleaned = raw.replace(",", "")
            return Decimal(cleaned)
        except (InvalidOperation, ValueError):
            return None


def _parse_amount(raw: str) -> Decimal | None:
    """Module-level helper to parse raw amount string."""
    try:
        cleaned = raw.replace(",", "")
        return Decimal(cleaned)
    except (InvalidOperation, ValueError):
        return None


def extract_amounts(text: str) -> list[Decimal]:
    """Extract all monetary amounts from text (deduplicated).

    Searches for all amount patterns, returns unique amounts
    in order of first appearance.

    Args:
        text: OCR-extracted text to search.

    Returns:
        List of unique Decimal amounts found.
    """
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
