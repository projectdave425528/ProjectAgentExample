"""Unit tests for OcrAnalyzer (mocking pytesseract and Pillow)."""
from decimal import Decimal
from unittest.mock import patch, MagicMock

import pytest

from src.analyzer.ocr_analyzer import OcrAnalyzer
from src.models.config import AppConfig


@pytest.fixture
def analyzer():
    """Create OcrAnalyzer instance."""
    return OcrAnalyzer()


@pytest.fixture
def config():
    """Create default AppConfig."""
    return AppConfig()


class TestOcrAnalyzerHappyPath:
    """Happy path tests for OcrAnalyzer."""

    @patch("src.analyzer.ocr_analyzer.pytesseract")
    @patch("src.analyzer.ocr_analyzer.Image")
    def test_extract_payme_amount(
        self, mock_image, mock_tesseract, analyzer, config
    ):
        """Mock Tesseract returns 'HK$500.00 PayMe' → correct extraction."""
        mock_image.open.return_value = MagicMock()
        mock_tesseract.image_to_string.return_value = (
            "HK$500.00 PayMe"
        )

        with patch("os.path.isfile", return_value=True):
            result = analyzer.analyze("test.jpg", config)

        assert result.amount == Decimal("500.00")
        assert result.payment_method == "payme"
        assert result.confidence > 0.5
        assert result.error is None
        assert result.analysis_mode == "ocr"

    @patch("src.analyzer.ocr_analyzer.pytesseract")
    @patch("src.analyzer.ocr_analyzer.Image")
    def test_extract_fps(
        self, mock_image, mock_tesseract, analyzer, config
    ):
        """Mock Tesseract returns FPS keyword → detected as fps."""
        mock_image.open.return_value = MagicMock()
        mock_tesseract.image_to_string.return_value = (
            "轉數快 $1,000.50 已收"
        )

        with patch("os.path.isfile", return_value=True):
            result = analyzer.analyze("receipt.png", config)

        assert result.amount == Decimal("1000.50")
        assert result.payment_method == "fps"
        assert result.confidence == 1.0

    @patch("src.analyzer.ocr_analyzer.pytesseract")
    @patch("src.analyzer.ocr_analyzer.Image")
    def test_extract_bank_transfer(
        self, mock_image, mock_tesseract, analyzer, config
    ):
        """Mock Tesseract returns bank transfer keywords."""
        mock_image.open.return_value = MagicMock()
        mock_tesseract.image_to_string.return_value = (
            "銀行轉帳 $800"
        )

        with patch("os.path.isfile", return_value=True):
            result = analyzer.analyze("bank.jpg", config)

        assert result.amount == Decimal("800")
        assert result.payment_method == "bank_transfer"

    @patch("src.analyzer.ocr_analyzer.pytesseract")
    @patch("src.analyzer.ocr_analyzer.Image")
    def test_webp_format_supported(
        self, mock_image, mock_tesseract, analyzer, config
    ):
        """WEBP format image is accepted and processed."""
        mock_image.open.return_value = MagicMock()
        mock_tesseract.image_to_string.return_value = "$300"

        with patch("os.path.isfile", return_value=True):
            result = analyzer.analyze("photo.webp", config)

        assert result.amount == Decimal("300")
        assert result.error is None


class TestOcrAnalyzerErrorPath:
    """Error path tests for OcrAnalyzer."""

    def test_file_not_found(self, analyzer, config):
        """Non-existent file returns error result (no exception)."""
        result = analyzer.analyze(
            "/nonexistent/image.jpg", config
        )

        assert result.error == "無法讀取文件"
        assert result.confidence == 0.0
        assert result.needs_review is True
        assert result.filename == "image.jpg"

    def test_unsupported_format(self, analyzer, config):
        """Unsupported file format returns error result."""
        with patch("os.path.isfile", return_value=True):
            result = analyzer.analyze("file.bmp", config)

        assert "唔支援" in result.error
        assert result.confidence == 0.0

    @patch("src.analyzer.ocr_analyzer.pytesseract")
    @patch("src.analyzer.ocr_analyzer.Image")
    def test_tesseract_failure(
        self, mock_image, mock_tesseract, analyzer, config
    ):
        """Tesseract raises exception → error result returned."""
        mock_image.open.side_effect = Exception(
            "Tesseract not found"
        )

        with patch("os.path.isfile", return_value=True):
            result = analyzer.analyze("test.jpg", config)

        assert result.error == "Tesseract OCR 執行失敗"
        assert result.confidence == 0.0
        assert result.needs_review is True


class TestOcrAnalyzerEdgeCases:
    """Edge case tests for OcrAnalyzer."""

    @patch("src.analyzer.ocr_analyzer.pytesseract")
    @patch("src.analyzer.ocr_analyzer.Image")
    def test_empty_ocr_text(
        self, mock_image, mock_tesseract, analyzer, config
    ):
        """OCR returns empty string → confidence=0.0, needs_review=True."""
        mock_image.open.return_value = MagicMock()
        mock_tesseract.image_to_string.return_value = ""

        with patch("os.path.isfile", return_value=True):
            result = analyzer.analyze("blank.jpg", config)

        assert result.confidence == 0.0
        assert result.needs_review is True
        assert result.amount is None
        assert result.payment_method is None

    @patch("src.analyzer.ocr_analyzer.pytesseract")
    @patch("src.analyzer.ocr_analyzer.Image")
    def test_text_without_amount_or_payment(
        self, mock_image, mock_tesseract, analyzer, config
    ):
        """OCR text has no amounts or payment keywords."""
        mock_image.open.return_value = MagicMock()
        mock_tesseract.image_to_string.return_value = (
            "Hello World 你好"
        )

        with patch("os.path.isfile", return_value=True):
            result = analyzer.analyze("random.png", config)

        assert result.confidence == 0.3
        assert result.amount is None
        assert result.payment_method is None
        assert result.needs_review is True

    @patch("src.analyzer.ocr_analyzer.pytesseract")
    @patch("src.analyzer.ocr_analyzer.Image")
    def test_custom_tesseract_path(
        self, mock_image, mock_tesseract, analyzer
    ):
        """Custom tesseract_path in config is applied."""
        config = AppConfig(
            tesseract_path="/usr/local/bin/tesseract"
        )
        mock_image.open.return_value = MagicMock()
        mock_tesseract.image_to_string.return_value = "$100"

        with patch("os.path.isfile", return_value=True):
            analyzer.analyze("test.jpg", config)

        assert (
            mock_tesseract.pytesseract.tesseract_cmd
            == "/usr/local/bin/tesseract"
        )

    @patch("src.analyzer.ocr_analyzer.pytesseract")
    @patch("src.analyzer.ocr_analyzer.Image")
    def test_filename_extracted_from_path(
        self, mock_image, mock_tesseract, analyzer, config
    ):
        """Filename is correctly extracted from full path."""
        mock_image.open.return_value = MagicMock()
        mock_tesseract.image_to_string.return_value = "$500"

        with patch("os.path.isfile", return_value=True):
            result = analyzer.analyze(
                "/path/to/receipt.jpg", config
            )

        assert result.filename == "receipt.jpg"
