"""Tests for analyzer module (amount_extractor + payment_detector + ocr_analyzer)."""
from decimal import Decimal
from unittest.mock import patch, MagicMock
import pytest

from src.analyzer.amount_extractor import extract_amounts
from src.analyzer.payment_detector import detect_payment_method
from src.analyzer.ocr_analyzer import OcrAnalyzer
from src.models.config import AppConfig


class TestExtractAmounts:
    def test_simple_dollar(self):
        assert extract_amounts("$500") == [Decimal("500")]

    def test_hk_dollar(self):
        assert extract_amounts("HK$1,000.50") == [Decimal("1000.50")]

    def test_chinese_mun(self):
        assert extract_amounts("500蚊") == [Decimal("500")]

    def test_multiple(self):
        result = extract_amounts("報價 $500 實收 HK$450")
        assert Decimal("500") in result
        assert Decimal("450") in result

    def test_dedup(self):
        result = extract_amounts("$500 同 500蚊")
        assert result == [Decimal("500")]

    def test_empty(self):
        assert extract_amounts("") == []

    def test_none(self):
        assert extract_amounts(None) == []


class TestDetectPaymentMethod:
    def test_payme(self):
        assert detect_payment_method("PayMe 轉帳") == "payme"

    def test_fps(self):
        assert detect_payment_method("轉數快 已收") == "fps"

    def test_bank(self):
        assert detect_payment_method("銀行轉帳") == "bank_transfer"

    def test_unknown(self):
        assert detect_payment_method("你好") == "unknown"

    def test_empty(self):
        assert detect_payment_method("") == "unknown"


class TestOcrAnalyzer:
    @patch("src.analyzer.ocr_analyzer.pytesseract")
    @patch("src.analyzer.ocr_analyzer.Image")
    def test_payme_extraction(self, mock_image, mock_tesseract):
        mock_image.open.return_value = MagicMock()
        mock_tesseract.image_to_string.return_value = "HK$500.00 PayMe"
        analyzer = OcrAnalyzer()
        config = AppConfig()
        with patch("os.path.isfile", return_value=True):
            result = analyzer.analyze("test.jpg", config)
        assert result.amount == Decimal("500.00")
        assert result.payment_method == "payme"
        assert result.confidence == 1.0

    def test_file_not_found(self):
        analyzer = OcrAnalyzer()
        config = AppConfig()
        result = analyzer.analyze("/nonexistent.jpg", config)
        assert result.error == "無法讀取文件"
        assert result.confidence == 0.0
        assert result.needs_review is True

    @patch("src.analyzer.ocr_analyzer.pytesseract")
    @patch("src.analyzer.ocr_analyzer.Image")
    def test_empty_ocr_text(self, mock_image, mock_tesseract):
        mock_image.open.return_value = MagicMock()
        mock_tesseract.image_to_string.return_value = ""
        analyzer = OcrAnalyzer()
        config = AppConfig()
        with patch("os.path.isfile", return_value=True):
            result = analyzer.analyze("blank.jpg", config)
        assert result.confidence == 0.0
        assert result.needs_review is True
