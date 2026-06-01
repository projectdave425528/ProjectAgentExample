"""Unit tests for transaction information extractor."""
import pytest
from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock

from src.builder.extractor import (
    extract_customer_name,
    extract_repair_item,
    extract_quantity,
    extract_quoted_amount,
    extract_from_matched_pair,
    group_by_time_window,
    ExtractionResult,
)


# === extract_customer_name ===

class TestExtractCustomerName:
    """Tests for extract_customer_name."""

    def test_normal_name(self):
        """Happy path: normal sender name."""
        assert extract_customer_name("陳大文") == "陳大文"

    def test_english_name(self):
        """Happy path: English name."""
        assert extract_customer_name("John Wong") == "John Wong"

    def test_empty_string_returns_unknown(self):
        """Error path: empty sender returns Unknown."""
        assert extract_customer_name("") == "Unknown"

    def test_whitespace_only_returns_unknown(self):
        """Error path: whitespace-only returns Unknown."""
        assert extract_customer_name("   ") == "Unknown"

    def test_name_with_emoji(self):
        """Edge case: name with emoji preserved."""
        assert extract_customer_name("陳大文🔥") == "陳大文🔥"

    def test_name_with_leading_trailing_spaces(self):
        """Edge case: strips leading/trailing spaces."""
        assert extract_customer_name("  陳大文  ") == "陳大文"


# === extract_repair_item ===

class TestExtractRepairItem:
    """Tests for extract_repair_item."""

    def test_swap_screen(self):
        """Happy path: 換屏 keyword."""
        assert extract_repair_item("幫我換屏") == "換屏"

    def test_swap_battery(self):
        """Happy path: 換電池 keyword."""
        assert extract_repair_item("要換電池") == "換電池"

    def test_repair(self):
        """Happy path: 維修 keyword."""
        assert extract_repair_item("部機要維修") == "維修"

    def test_swap_mon(self):
        """Happy path: 換mon keyword."""
        assert extract_repair_item("換mon幾錢") == "換mon"

    def test_film(self):
        """Happy path: 貼膜 keyword."""
        assert extract_repair_item("想貼膜") == "貼膜"

    def test_full_repair(self):
        """Happy path: 整機 keyword."""
        assert extract_repair_item("整機要幾耐") == "整機"

    def test_no_keyword_returns_none(self):
        """Error path: no repair keyword found."""
        assert extract_repair_item("你好") is None

    def test_empty_content_returns_none(self):
        """Error path: empty content."""
        assert extract_repair_item("") is None

    def test_case_insensitive_mon(self):
        """Edge case: case-insensitive matching for 換MON."""
        assert extract_repair_item("換MON") == "換mon"


# === extract_quantity ===

class TestExtractQuantity:
    """Tests for extract_quantity."""

    def test_numeric_with_unit_bu(self):
        """Happy path: '3部' format."""
        assert extract_quantity("換屏 3部") == 3

    def test_x_format_lowercase(self):
        """Happy path: 'x2' format."""
        assert extract_quantity("換屏 x2 $500") == 2

    def test_x_format_uppercase(self):
        """Happy path: 'X3' format."""
        assert extract_quantity("換屏 X3") == 3

    def test_multiply_sign(self):
        """Happy path: '×3' format."""
        assert extract_quantity("換屏 ×3") == 3

    def test_numeric_with_unit_tai(self):
        """Happy path: '2台' format."""
        assert extract_quantity("2台機") == 2

    def test_chinese_two_bu(self):
        """Edge case: '兩部' Cantonese."""
        assert extract_quantity("兩部機換屏") == 2

    def test_chinese_three_bu(self):
        """Edge case: '三部' Cantonese."""
        assert extract_quantity("三部都要換") == 3

    def test_no_quantity_returns_one(self):
        """Default: no quantity found returns 1."""
        assert extract_quantity("換屏 $500") == 1

    def test_empty_content_returns_one(self):
        """Default: empty content returns 1."""
        assert extract_quantity("") == 1


# === extract_quoted_amount ===

class TestExtractQuotedAmount:
    """Tests for extract_quoted_amount."""

    def test_dollar_sign(self):
        """Happy path: $500 format."""
        assert extract_quoted_amount("換屏 $500") == Decimal("500")

    def test_hk_dollar(self):
        """Happy path: HK$800 format."""
        assert extract_quoted_amount("HK$800") == Decimal("800")

    def test_man_suffix(self):
        """Happy path: 500蚊 format."""
        assert extract_quoted_amount("收你500蚊") == Decimal("500")

    def test_yuan_suffix(self):
        """Happy path: 300元 format."""
        assert extract_quoted_amount("300元") == Decimal("300")

    def test_amount_with_comma(self):
        """Happy path: $1,000 with comma."""
        assert extract_quoted_amount("$1,000") == Decimal("1000")

    def test_amount_with_decimal(self):
        """Happy path: $500.50 with decimal."""
        assert extract_quoted_amount("$500.50") == Decimal("500.50")

    def test_chinese_three_hundred(self):
        """Edge case: Cantonese '三百' = 300."""
        assert extract_quoted_amount("三百蚊") == Decimal("300")

    def test_chinese_five_hundred(self):
        """Edge case: Cantonese '五百' = 500."""
        assert extract_quoted_amount("五百") == Decimal("500")

    def test_chinese_one_thousand(self):
        """Edge case: Cantonese '一千' = 1000."""
        assert extract_quoted_amount("一千蚊") == Decimal("1000")

    def test_no_amount_returns_none(self):
        """Error path: no amount in content."""
        assert extract_quoted_amount("你好") is None

    def test_empty_content_returns_none(self):
        """Error path: empty content."""
        assert extract_quoted_amount("") is None


# === extract_from_matched_pair ===

class TestExtractFromMatchedPair:
    """Tests for extract_from_matched_pair."""

    def _make_pair(self, sender, content, timestamp=None):
        """Helper to create a mock MatchedPair."""
        if timestamp is None:
            timestamp = datetime(2024, 1, 15, 14, 30, 0)
        pair = MagicMock()
        pair.message.sender = sender
        pair.message.content = content
        pair.message.timestamp = timestamp
        return pair

    def test_full_extraction(self):
        """Happy path: all fields extracted."""
        pair = self._make_pair("陳大文", "換屏 $500")
        result = extract_from_matched_pair(pair)

        assert result.customer_name == "陳大文"
        assert result.repair_item == "換屏"
        assert result.quoted_amount == Decimal("500")
        assert result.quantity == 1

    def test_with_quantity(self):
        """Happy path: quantity extracted."""
        pair = self._make_pair("陳大文", "換屏 x3 $500")
        result = extract_from_matched_pair(pair)

        assert result.quantity == 3
        assert result.quoted_amount == Decimal("500")

    def test_empty_sender(self):
        """Error path: empty sender becomes Unknown."""
        pair = self._make_pair("", "換屏 $500")
        result = extract_from_matched_pair(pair)

        assert result.customer_name == "Unknown"

    def test_no_amount_no_crash(self):
        """Error path: no amount doesn't crash."""
        pair = self._make_pair("陳大文", "你好")
        result = extract_from_matched_pair(pair)

        assert result.quoted_amount is None
        assert result.repair_item is None

    def test_confidence_full(self):
        """Confidence is high when all fields found."""
        pair = self._make_pair("陳大文", "換屏 $500")
        result = extract_from_matched_pair(pair)

        assert result.confidence == 1.0

    def test_confidence_no_fields(self):
        """Confidence is low when no fields found."""
        pair = self._make_pair("陳大文", "你好")
        result = extract_from_matched_pair(pair)

        assert result.confidence == 0.3


# === group_by_time_window ===

class TestGroupByTimeWindow:
    """Tests for group_by_time_window."""

    def _make_result(self, name, amount, ts_hour):
        """Helper to create ExtractionResult."""
        return ExtractionResult(
            customer_name=name,
            repair_item="換屏",
            quoted_amount=Decimal(str(amount)) if amount else None,
            quantity=1,
            timestamp=datetime(2024, 1, 15, ts_hour, 0, 0),
            confidence=0.8,
        )

    def test_single_result(self):
        """Happy path: single result = single group."""
        results = [self._make_result("陳大文", 500, 10)]
        groups = group_by_time_window(results)

        assert len(groups) == 1
        assert len(groups[0]) == 1

    def test_same_customer_same_amount_within_window(self):
        """Happy path: same customer, same amount, within 2h."""
        results = [
            self._make_result("陳大文", 500, 10),
            self._make_result("陳大文", 500, 11),
        ]
        groups = group_by_time_window(results)

        assert len(groups) == 1
        assert len(groups[0]) == 2

    def test_same_customer_different_amount_splits(self):
        """Edge case: same customer, different amounts = 2 groups."""
        results = [
            self._make_result("陳大文", 500, 10),
            self._make_result("陳大文", 800, 11),
        ]
        groups = group_by_time_window(results)

        assert len(groups) == 2

    def test_same_customer_outside_window_splits(self):
        """Edge case: same customer, outside 2h window = 2 groups."""
        results = [
            self._make_result("陳大文", 500, 10),
            self._make_result("陳大文", 500, 13),
        ]
        groups = group_by_time_window(results)

        assert len(groups) == 2

    def test_different_customers_split(self):
        """Happy path: different customers = separate groups."""
        results = [
            self._make_result("陳大文", 500, 10),
            self._make_result("李小明", 500, 10),
        ]
        groups = group_by_time_window(results)

        assert len(groups) == 2

    def test_empty_list_returns_empty(self):
        """Edge case: empty input returns empty."""
        groups = group_by_time_window([])

        assert groups == []
