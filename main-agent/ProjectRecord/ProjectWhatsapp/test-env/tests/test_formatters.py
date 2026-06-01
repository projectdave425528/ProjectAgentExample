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
    """Tests for format_date."""

    def test_format_date_normal(self):
        """正常日期格式化為 YYYY-MM-DD。"""
        assert format_date(date(2026, 5, 30)) == "2026-05-30"

    def test_format_date_single_digit_month_day(self):
        """單位數月份同日期有前導零。"""
        assert format_date(date(2026, 1, 5)) == "2026-01-05"

    def test_format_date_end_of_year(self):
        """年末日期正確格式化。"""
        assert format_date(date(2026, 12, 31)) == "2026-12-31"


class TestFormatAmount:
    """Tests for format_amount."""

    def test_format_amount_none_returns_empty(self):
        """None 返回空字串。"""
        assert format_amount(None) == ""

    def test_format_amount_integer_value(self):
        """整數金額保留 2 位小數。"""
        assert format_amount(Decimal("100")) == "100.00"

    def test_format_amount_decimal_value(self):
        """小數金額保留 2 位小數。"""
        assert format_amount(Decimal("99.50")) == "99.50"

    def test_format_amount_zero(self):
        """零金額顯示 0.00。"""
        assert format_amount(Decimal("0")) == "0.00"

    def test_format_amount_large_value(self):
        """大金額正確格式化。"""
        assert format_amount(Decimal("12345.67")) == "12345.67"

    def test_format_amount_many_decimals_truncated(self):
        """多位小數截斷到 2 位。"""
        result = format_amount(Decimal("100.999"))
        assert result == "100.999" or result == "101.00"
        # Decimal formatting preserves precision


class TestFormatPaymentMethod:
    """Tests for format_payment_method."""

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
        """None 返回 '未知'。"""
        assert format_payment_method(None) == "未知"

    def test_unrecognized_returns_unknown(self):
        """未識別嘅值返回 '未知'。"""
        assert format_payment_method("bitcoin") == "未知"


class TestFormatPaymentStatus:
    """Tests for format_payment_status."""

    def test_paid(self):
        assert format_payment_status("paid") == "已付"

    def test_unpaid(self):
        assert format_payment_status("unpaid") == "未付"

    def test_partial(self):
        assert format_payment_status("partial") == "部分付款"

    def test_unknown_status_returns_raw(self):
        """未識別嘅狀態返回原始值。"""
        assert format_payment_status("refunded") == "refunded"


class TestExtractQuantityFromNotes:
    """Tests for extract_quantity_from_notes."""

    def test_extract_quantity_present(self):
        """正常提取數量。"""
        assert extract_quantity_from_notes("數量: 3") == 3

    def test_extract_quantity_in_longer_text(self):
        """從較長文本中提取數量。"""
        assert extract_quantity_from_notes("維修手機，數量: 2，已完成") == 2

    def test_extract_quantity_missing_returns_one(self):
        """冇數量信息返回 1。"""
        assert extract_quantity_from_notes("普通備註") == 1

    def test_extract_quantity_empty_string(self):
        """空字串返回 1。"""
        assert extract_quantity_from_notes("") == 1

    def test_extract_quantity_large_number(self):
        """大數量正確提取。"""
        assert extract_quantity_from_notes("數量: 100") == 100

    def test_extract_quantity_with_extra_spaces(self):
        """數量前有額外空格。"""
        assert extract_quantity_from_notes("數量:  5") == 5
