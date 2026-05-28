"""Unit tests for amount_extractor module."""
from decimal import Decimal

import pytest

from src.analyzer.amount_extractor import extract_amounts


class TestExtractAmounts:
    """Tests for extract_amounts function."""

    # --- Happy Path ---

    def test_simple_dollar_amount(self):
        """Standard $500 format."""
        result = extract_amounts("收到 $500 多謝")
        assert result == [Decimal("500")]

    def test_dollar_with_cents(self):
        """$500.00 format with cents."""
        result = extract_amounts("金額 $500.50")
        assert result == [Decimal("500.50")]

    def test_hk_dollar_amount(self):
        """HK$ prefix format."""
        result = extract_amounts("HK$500.00 已收")
        assert result == [Decimal("500.00")]

    def test_hk_dollar_with_thousands(self):
        """HK$1,000.50 with thousands separator."""
        result = extract_amounts("轉帳 HK$1,000.50")
        assert result == [Decimal("1000.50")]

    def test_chinese_suffix_mun(self):
        """500蚊 format."""
        result = extract_amounts("收咗500蚊")
        assert result == [Decimal("500")]

    def test_chinese_suffix_yuen(self):
        """500元 format."""
        result = extract_amounts("金額500元")
        assert result == [Decimal("500")]

    def test_multiple_amounts(self):
        """Multiple amounts in one text."""
        text = "報價 $500 實收 HK$450.00"
        result = extract_amounts(text)
        assert Decimal("500") in result
        assert Decimal("450.00") in result

    # --- Edge Cases ---

    def test_thousands_separator(self):
        """$1,000.50 correctly parsed as 1000.50."""
        result = extract_amounts("$1,000.50")
        assert result == [Decimal("1000.50")]

    def test_ten_thousands(self):
        """$10,000 correctly parsed."""
        result = extract_amounts("$10,000")
        assert result == [Decimal("10000")]

    def test_chinese_suffix_with_thousands(self):
        """1,000蚊 with thousands separator."""
        result = extract_amounts("收咗1,000蚊")
        assert result == [Decimal("1000")]

    def test_empty_string(self):
        """Empty string returns empty list."""
        result = extract_amounts("")
        assert result == []

    def test_none_input(self):
        """None input returns empty list."""
        result = extract_amounts(None)
        assert result == []

    def test_whitespace_only(self):
        """Whitespace-only string returns empty list."""
        result = extract_amounts("   ")
        assert result == []

    def test_no_amounts_in_text(self):
        """Text without any amounts returns empty list."""
        result = extract_amounts("你好，今日天氣好好")
        assert result == []

    def test_no_duplicate_amounts(self):
        """Same amount appearing twice is deduplicated."""
        text = "$500 同 500蚊"
        result = extract_amounts(text)
        assert result == [Decimal("500")]

    def test_dollar_with_space(self):
        """Dollar sign with space before amount."""
        result = extract_amounts("$ 500")
        assert result == [Decimal("500")]
