"""Detect payment method from OCR text."""
from typing import Literal

PaymentMethod = Literal["payme", "fps", "bank_transfer", "unknown"]

_PAYME_KEYWORDS = ["payme", "pay me"]
_FPS_KEYWORDS = ["fps", "轉數快", "faster payment"]
_BANK_KEYWORDS = ["銀行", "bank transfer", "匯款", "轉帳"]


class PaymentDetector:
    def detect(self, text: str) -> PaymentMethod | None:
        if not text:
            return None
        lower_text = text.lower()
        if any(kw in lower_text for kw in _PAYME_KEYWORDS):
            return "payme"
        if any(kw in lower_text for kw in _FPS_KEYWORDS):
            return "fps"
        if any(kw in lower_text for kw in _BANK_KEYWORDS):
            return "bank_transfer"
        return "unknown"


def detect_payment_method(text: str) -> str:
    """Module-level convenience function."""
    if not text or not text.strip():
        return "unknown"
    result = PaymentDetector().detect(text)
    return result if result is not None else "unknown"
