"""Unit tests for payment status resolver."""
import pytest
from decimal import Decimal

from src.builder.status_resolver import (
    resolve_payment_status,
    _calculate_total,
    _compare_amounts,
)


class TestResolvePaymentStatus:
    """Tests for resolve_payment_status."""

    # --- Happy Path ---

    def test_exact_match_paid(self):
        """Happy path: quoted×quantity == received → paid."""
        status = resolve_payment_status(
            quoted_amount=Decimal("500"),
            quantity=2,
            received_amount=Decimal("1000"),
        )
        assert status == "paid"

    def test_single_item_paid(self):
        """Happy path: single item exact match → paid."""
        status = resolve_payment_status(
            quoted_amount=Decimal("500"),
            quantity=1,
            received_amount=Decimal("500"),
        )
        assert status == "paid"

    def test_within_tolerance_paid(self):
        """Happy path: within 1% tolerance → paid."""
        # 500 × 2 = 1000, tolerance = ±10
        status = resolve_payment_status(
            quoted_amount=Decimal("500"),
            quantity=2,
            received_amount=Decimal("995"),
        )
        assert status == "paid"

    # --- Partial Payment ---

    def test_partial_payment(self):
        """Happy path: received < total → partial."""
        status = resolve_payment_status(
            quoted_amount=Decimal("500"),
            quantity=2,
            received_amount=Decimal("700"),
        )
        assert status == "partial"

    def test_partial_small_amount(self):
        """Happy path: received much less than total → partial."""
        status = resolve_payment_status(
            quoted_amount=Decimal("1000"),
            quantity=1,
            received_amount=Decimal("100"),
        )
        assert status == "partial"

    # --- Unpaid ---

    def test_no_received_amount_unpaid(self):
        """Happy path: no received amount → unpaid."""
        status = resolve_payment_status(
            quoted_amount=Decimal("500"),
            quantity=1,
            received_amount=None,
        )
        assert status == "unpaid"

    def test_zero_received_unpaid(self):
        """Happy path: received = 0 → unpaid."""
        status = resolve_payment_status(
            quoted_amount=Decimal("500"),
            quantity=1,
            received_amount=Decimal("0"),
        )
        assert status == "unpaid"

    # --- Error Path ---

    def test_no_quoted_but_has_received_paid(self):
        """Error path: no quoted amount but received → paid."""
        status = resolve_payment_status(
            quoted_amount=None,
            quantity=1,
            received_amount=Decimal("500"),
        )
        assert status == "paid"

    def test_no_quoted_no_received_unpaid(self):
        """Error path: no quoted, no received → unpaid."""
        status = resolve_payment_status(
            quoted_amount=None,
            quantity=1,
            received_amount=None,
        )
        assert status == "unpaid"

    # --- Edge Cases ---

    def test_overpaid_is_paid(self):
        """Edge case: overpaid → still paid."""
        status = resolve_payment_status(
            quoted_amount=Decimal("500"),
            quantity=1,
            received_amount=Decimal("600"),
        )
        assert status == "paid"

    def test_tolerance_boundary_lower(self):
        """Edge case: exactly at lower tolerance boundary → paid."""
        # 1000 - 1% = 990
        status = resolve_payment_status(
            quoted_amount=Decimal("500"),
            quantity=2,
            received_amount=Decimal("990"),
        )
        assert status == "paid"

    def test_just_below_tolerance_partial(self):
        """Edge case: just below tolerance → partial."""
        # 1000 - 1% = 990, so 989 is partial
        status = resolve_payment_status(
            quoted_amount=Decimal("500"),
            quantity=2,
            received_amount=Decimal("989"),
        )
        assert status == "partial"

    def test_negative_received_unpaid(self):
        """Edge case: negative received → unpaid."""
        status = resolve_payment_status(
            quoted_amount=Decimal("500"),
            quantity=1,
            received_amount=Decimal("-100"),
        )
        assert status == "unpaid"

    def test_large_quantity(self):
        """Edge case: large quantity calculation correct."""
        # 200 × 10 = 2000
        status = resolve_payment_status(
            quoted_amount=Decimal("200"),
            quantity=10,
            received_amount=Decimal("2000"),
        )
        assert status == "paid"


class TestCalculateTotal:
    """Tests for _calculate_total helper."""

    def test_basic_multiplication(self):
        """Basic multiplication works."""
        assert _calculate_total(Decimal("500"), 2) == Decimal("1000")

    def test_quantity_one(self):
        """Quantity 1 returns same amount."""
        assert _calculate_total(Decimal("300"), 1) == Decimal("300")

    def test_decimal_amount(self):
        """Decimal amounts multiply correctly."""
        assert _calculate_total(
            Decimal("99.50"), 3
        ) == Decimal("298.50")


class TestCompareAmounts:
    """Tests for _compare_amounts helper."""

    def test_exact_match(self):
        """Exact match → paid."""
        assert _compare_amounts(
            Decimal("1000"), Decimal("1000")
        ) == "paid"

    def test_within_tolerance(self):
        """Within 1% → paid."""
        assert _compare_amounts(
            Decimal("1000"), Decimal("992")
        ) == "paid"

    def test_below_tolerance(self):
        """Below tolerance → partial."""
        assert _compare_amounts(
            Decimal("1000"), Decimal("500")
        ) == "partial"

    def test_zero_expected_with_received(self):
        """Zero expected but received → paid."""
        assert _compare_amounts(
            Decimal("0"), Decimal("100")
        ) == "paid"

    def test_zero_expected_zero_received(self):
        """Zero expected, zero received → unpaid."""
        assert _compare_amounts(
            Decimal("0"), Decimal("0")
        ) == "unpaid"
