"""Payment status resolution logic.

Compares quoted_amount × quantity vs received_amount to determine
payment status: paid, partial, or unpaid.
Uses ±1% tolerance to avoid floating point issues.
"""
import logging
from decimal import Decimal
from typing import Literal, Optional

logger = logging.getLogger(__name__)

PaymentStatus = Literal["paid", "unpaid", "partial"]

TOLERANCE_PERCENT: Decimal = Decimal("0.01")


def resolve_payment_status(
    quoted_amount: Optional[Decimal],
    quantity: int,
    received_amount: Optional[Decimal],
) -> PaymentStatus:
    """Determine payment status by comparing expected vs received.

    Rules:
    - No received amount → "unpaid"
    - received ≈ quoted × quantity (±1%) → "paid"
    - 0 < received < total → "partial"
    - No quoted amount but has received → "paid" (assume correct)

    Args:
        quoted_amount: Unit price from message extraction.
        quantity: Number of items (default 1).
        received_amount: Actual received from image analysis.

    Returns:
        Payment status string: "paid", "unpaid", or "partial".
    """
    if received_amount is None or received_amount <= 0:
        return "unpaid"

    if quoted_amount is None:
        return "paid"

    total = _calculate_total(quoted_amount, quantity)
    return _compare_amounts(total, received_amount)


def _calculate_total(
    quoted_amount: Decimal, quantity: int
) -> Decimal:
    """Calculate total expected amount."""
    return quoted_amount * quantity


def _compare_amounts(
    expected: Decimal, received: Decimal
) -> PaymentStatus:
    """Compare expected and received with tolerance.

    Tolerance is ±1% of expected amount.
    """
    if expected <= 0:
        return "paid" if received > 0 else "unpaid"

    tolerance = expected * TOLERANCE_PERCENT
    lower_bound = expected - tolerance
    upper_bound = expected + tolerance

    if lower_bound <= received <= upper_bound:
        return "paid"

    if received > 0 and received < lower_bound:
        return "partial"

    # Overpaid — still consider as paid
    if received > upper_bound:
        return "paid"

    return "unpaid"
