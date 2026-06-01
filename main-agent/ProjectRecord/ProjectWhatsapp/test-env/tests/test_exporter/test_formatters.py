"""Unit tests for src/exporter/formatters.py."""
import pytest
from datetime import date
from decimal import Decimal

from src.exporter.formatters import (
    extract_quantity_from_notes,
    format_amount,
    format_date,
    format_payment_method,
    format_payment_status,
)


class TestFormatDate:
    def test_format_date_normal(self):
        assert format_date(date(2026, 5, 30)) == "2026-05-30"

    def test_format_date_single_digit_month_day(self):
        assert format_date(date(2026, 1, 5)) == "2026-01-05"

    def test_format_date_end_of_year(self):
        assert format_date(date(2026, 12, 31)) == "2026-12-31"


class TestFormatAmount:
    def test_format_amount_none_returns_empty(self):
        assert format_amount(None) == ""

    def test_format_amount_integer_value(self):
        assert format_amount(Decimal("100")) == "100.00"

    def test_format_amount_decimal_value(self):
        assert format_amount(Decimal("99.50")) == "99.50"

    def test_format_amount_zero(self):
        assert format_amount(Decimal("0")) == "0.00"

    def test_format_amount_large_value(self):
        assert format_amount(Decimal("12345.67")) == "12345.67"


class TestFormatPaymentMethod:
    def test_payme(self):
        assert format_payment_method("payme") == "PayMe"

    def test_fps(self):
        assert format_payment_method("fps") == "轉數快"

    def test_bank_transfer(self):
        assert format_payment_method("bank_transfer") == "銀行轉帳"

    def test_cash(self):
        assert format_payment_method("cash") == "現金"

    def test_unknown(self):
        assert format_payment_method("unknown") == "未知"

    def test_none_returns_unknown(self):
        assert format_payment_method(None) == "未知"

    def test_unrecognized_returns_unknown(self):
        assert format_payment_method("bitcoin") == "未知"


class TestFormatPaymentStatus:
    def test_paid(self):
        assert format_payment_status("paid") == "已付"

    def test_unpaid(self):
        assert format_payment_status("unpaid") == "未付"

    def test_partial(self):
        assert format_payment_status("partial") == "部分付款"

    def test_unknown_status_returns_raw(self):
        assert format_payment_status("refunded") == "refunded"


class TestExtractQuantityFromNotes:
    def test_extract_quantity_present(self):
        assert extract_quantity_from_notes("數量: 3") == 3

    def test_extract_quantity_in_longer_text(self):
        assert extract_quantity_from_notes("維修手機，數量: 2，已完成") == 2

    def test_extract_quantity_missing_returns_one(self):
        assert extract_quantity_from_notes("普通備註") == 1

    def test_extract_quantity_empty_string(self):
        assert extract_quantity_from_notes("") == 1

    def test_extract_quantity_large_number(self):
        assert extract_quantity_from_notes("數量: 100") == 100
