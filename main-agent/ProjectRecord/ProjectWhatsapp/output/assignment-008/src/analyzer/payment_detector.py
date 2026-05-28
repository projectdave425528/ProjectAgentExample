"""Detect payment method from OCR text."""
from typing import Literal


PaymentMethod = Literal["payme", "fps", "bank_transfer", "unknown"]

_PAYME_KEYWORDS = ["payme", "pay me"]
_FPS_KEYWORDS = ["fps", "轉數快", "faster payment"]
_BANK_KEYWORDS = ["銀行", "bank transfer", "匯款", "轉帳"]


class PaymentDetector:
    """Detects payment method from OCR text using keyword matching."""

    def detect(self, text: str) -> PaymentMethod | None:
        """Detect payment method from text.

        Args:
            text: OCR-extracted text to analyze.

        Returns:
            Payment method literal or None if text is empty.
        """
        if not text:
            return None
        lower_text = text.lower()
        if self._matches(lower_text, _PAYME_KEYWORDS):
            return "payme"
        if self._matches(lower_text, _FPS_KEYWORDS):
            return "fps"
        if self._matches(lower_text, _BANK_KEYWORDS):
            return "bank_transfer"
        return "unknown"

    def _matches(self, text: str, keywords: list[str]) -> bool:
        """Check if any keyword exists in text."""
        return any(kw in text for kw in keywords)
