"""Unit tests for payment_detector module."""
import pytest

from src.analyzer.payment_detector import detect_payment_method


class TestDetectPaymentMethod:
    """Tests for detect_payment_method function."""

    # --- Happy Path: PayMe ---

    def test_payme_lowercase(self):
        """Detect 'payme' keyword."""
        assert detect_payment_method("payme 收款") == "payme"

    def test_payme_mixed_case(self):
        """Detect 'PayMe' mixed case."""
        assert detect_payment_method("PayMe 已收") == "payme"

    def test_pay_me_with_space(self):
        """Detect 'Pay Me' with space."""
        assert detect_payment_method("用 Pay Me 轉") == "payme"

    # --- Happy Path: FPS ---

    def test_fps_uppercase(self):
        """Detect 'FPS' keyword."""
        assert detect_payment_method("FPS 轉帳") == "fps"

    def test_fps_lowercase(self):
        """Detect 'fps' lowercase."""
        assert detect_payment_method("用 fps 過數") == "fps"

    def test_faster_payment(self):
        """Detect 'Faster Payment' keyword."""
        result = detect_payment_method("Faster Payment System")
        assert result == "fps"

    def test_zhuan_shu_kuai(self):
        """Detect '轉數快' Chinese keyword."""
        assert detect_payment_method("轉數快收款") == "fps"

    # --- Happy Path: Bank Transfer ---

    def test_bank_transfer_english(self):
        """Detect 'bank transfer' keyword."""
        result = detect_payment_method("via bank transfer")
        assert result == "bank_transfer"

    def test_bank_chinese(self):
        """Detect '銀行' keyword."""
        assert detect_payment_method("銀行轉帳") == "bank_transfer"

    def test_hui_kuan(self):
        """Detect '匯款' keyword."""
        assert detect_payment_method("已匯款") == "bank_transfer"

    def test_zhuan_zhang(self):
        """Detect '轉帳' keyword."""
        assert detect_payment_method("已轉帳") == "bank_transfer"

    # --- Priority Order ---

    def test_payme_takes_priority_over_fps(self):
        """PayMe detected first when both present."""
        text = "PayMe FPS 轉帳"
        assert detect_payment_method(text) == "payme"

    def test_fps_takes_priority_over_bank(self):
        """FPS detected first when FPS and bank present."""
        text = "FPS 銀行轉帳"
        assert detect_payment_method(text) == "fps"

    # --- Error / Edge Cases ---

    def test_empty_string(self):
        """Empty string returns 'unknown'."""
        assert detect_payment_method("") == "unknown"

    def test_none_input(self):
        """None input returns 'unknown'."""
        assert detect_payment_method(None) == "unknown"

    def test_whitespace_only(self):
        """Whitespace-only returns 'unknown'."""
        assert detect_payment_method("   ") == "unknown"

    def test_no_keywords(self):
        """Text without payment keywords returns 'unknown'."""
        result = detect_payment_method("今日天氣好好")
        assert result == "unknown"

    def test_partial_keyword_no_match(self):
        """Partial keyword should not match (e.g. 'pay' alone)."""
        # 'pay' alone should not match 'payme'
        assert detect_payment_method("pay now") == "unknown"
