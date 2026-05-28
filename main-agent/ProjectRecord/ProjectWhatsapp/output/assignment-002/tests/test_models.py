"""Unit tests for all Pydantic data models.

Covers: Happy Path, Error Path, Edge Cases.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from src.models.message import ParsedMessage
from src.models.image_result import ImageAnalysisResult
from src.models.transaction import TransactionRecord
from src.models.config import AppConfig


# ============================================================
# ParsedMessage Tests
# ============================================================

class TestParsedMessageHappyPath:
    """Happy path tests for ParsedMessage."""

    def test_create_with_all_fields(self):
        """All fields correctly assigned and serializable."""
        msg = ParsedMessage(
            timestamp=datetime(2024, 1, 15, 14, 30, 0),
            sender="John",
            content="Hello",
            is_system_message=False,
            attachments=["image.jpg"],
            raw_text="[2024/01/15, 14:30:00] John: Hello",
        )
        assert msg.timestamp == datetime(2024, 1, 15, 14, 30, 0)
        assert msg.sender == "John"
        assert msg.content == "Hello"
        assert msg.is_system_message is False
        assert msg.attachments == ["image.jpg"]
        assert msg.raw_text == "[2024/01/15, 14:30:00] John: Hello"

    def test_serialize_to_json(self):
        """Model can serialize to JSON string."""
        msg = ParsedMessage(
            timestamp=datetime(2024, 1, 15, 14, 30, 0),
            sender="陳大文",
            content="你好",
            raw_text="[2024/01/15, 14:30:00] 陳大文: 你好",
        )
        json_str = msg.model_dump_json()
        assert "陳大文" in json_str
        assert "你好" in json_str

    def test_defaults_applied(self):
        """Default values for optional fields."""
        msg = ParsedMessage(
            timestamp=datetime(2024, 1, 15, 14, 30, 0),
            sender="John",
            content="Hi",
            raw_text="[2024/01/15, 14:30:00] John: Hi",
        )
        assert msg.is_system_message is False
        assert msg.attachments == []


class TestParsedMessageErrorPath:
    """Error path tests for ParsedMessage."""

    def test_missing_timestamp_raises_error(self):
        """Missing required field raises ValidationError."""
        with pytest.raises(ValidationError):
            ParsedMessage(
                sender="John",
                content="Hello",
                raw_text="raw",
            )

    def test_missing_sender_raises_error(self):
        """Missing sender raises ValidationError."""
        with pytest.raises(ValidationError):
            ParsedMessage(
                timestamp=datetime(2024, 1, 15, 14, 30, 0),
                content="Hello",
                raw_text="raw",
            )

    def test_missing_raw_text_raises_error(self):
        """Missing raw_text raises ValidationError."""
        with pytest.raises(ValidationError):
            ParsedMessage(
                timestamp=datetime(2024, 1, 15, 14, 30, 0),
                sender="John",
                content="Hello",
            )

    def test_empty_sender_raises_error(self):
        """Empty sender string raises ValidationError."""
        with pytest.raises(ValidationError):
            ParsedMessage(
                timestamp=datetime(2024, 1, 15, 14, 30, 0),
                sender="",
                content="Hello",
                raw_text="raw",
            )

    def test_empty_raw_text_raises_error(self):
        """Empty raw_text string raises ValidationError."""
        with pytest.raises(ValidationError):
            ParsedMessage(
                timestamp=datetime(2024, 1, 15, 14, 30, 0),
                sender="John",
                content="Hello",
                raw_text="",
            )


class TestParsedMessageEdgeCases:
    """Edge case tests for ParsedMessage."""

    def test_sender_with_emoji(self):
        """Sender with emoji characters preserved correctly."""
        msg = ParsedMessage(
            timestamp=datetime(2024, 1, 15, 14, 30, 0),
            sender="John 😀🎉",
            content="Hello",
            raw_text="[2024/01/15, 14:30:00] John 😀🎉: Hello",
        )
        assert msg.sender == "John 😀🎉"

    def test_sender_with_special_characters(self):
        """Sender with special characters preserved."""
        msg = ParsedMessage(
            timestamp=datetime(2024, 1, 15, 14, 30, 0),
            sender="Dr. Wong: 醫生",
            content="Hello",
            raw_text="raw text here",
        )
        assert msg.sender == "Dr. Wong: 醫生"

    def test_empty_content_allowed(self):
        """Empty content string is allowed."""
        msg = ParsedMessage(
            timestamp=datetime(2024, 1, 15, 14, 30, 0),
            sender="John",
            content="",
            raw_text="raw",
        )
        assert msg.content == ""


# ============================================================
# ImageAnalysisResult Tests
# ============================================================

class TestImageAnalysisResultHappyPath:
    """Happy path tests for ImageAnalysisResult."""

    def test_create_full_result(self):
        """Create with all fields populated."""
        result = ImageAnalysisResult(
            filename="payment_001.jpg",
            image_date=date(2024, 1, 15),
            analysis_mode="ocr",
            payment_method="payme",
            amount=Decimal("500.00"),
            transaction_date=date(2024, 1, 15),
            transaction_id="TXN123",
            confidence=0.95,
            raw_text="HK$500.00 PayMe",
            needs_review=False,
            error=None,
        )
        assert result.filename == "payment_001.jpg"
        assert result.amount == Decimal("500.00")
        assert result.confidence == 0.95

    def test_minimal_result(self):
        """Create with only required fields."""
        result = ImageAnalysisResult(
            filename="img.png",
            analysis_mode="ai_vision",
            confidence=0.5,
        )
        assert result.payment_method is None
        assert result.amount is None
        assert result.needs_review is False


class TestImageAnalysisResultErrorPath:
    """Error path tests for ImageAnalysisResult."""

    def test_confidence_above_1_raises_error(self):
        """Confidence > 1.0 raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ImageAnalysisResult(
                filename="img.png",
                analysis_mode="ocr",
                confidence=1.5,
            )
        assert "confidence" in str(exc_info.value)

    def test_confidence_below_0_raises_error(self):
        """Confidence < 0.0 raises ValidationError."""
        with pytest.raises(ValidationError):
            ImageAnalysisResult(
                filename="img.png",
                analysis_mode="ocr",
                confidence=-0.1,
            )

    def test_empty_filename_raises_error(self):
        """Empty filename raises ValidationError."""
        with pytest.raises(ValidationError):
            ImageAnalysisResult(
                filename="",
                analysis_mode="ocr",
                confidence=0.5,
            )

    def test_invalid_analysis_mode_raises_error(self):
        """Invalid analysis_mode raises ValidationError."""
        with pytest.raises(ValidationError):
            ImageAnalysisResult(
                filename="img.png",
                analysis_mode="invalid_mode",
                confidence=0.5,
            )

    def test_invalid_payment_method_raises_error(self):
        """Invalid payment_method raises ValidationError."""
        with pytest.raises(ValidationError):
            ImageAnalysisResult(
                filename="img.png",
                analysis_mode="ocr",
                confidence=0.5,
                payment_method="credit_card",
            )


class TestImageAnalysisResultEdgeCases:
    """Edge case tests for ImageAnalysisResult."""

    def test_confidence_exactly_0(self):
        """Confidence of exactly 0.0 is valid."""
        result = ImageAnalysisResult(
            filename="img.png",
            analysis_mode="ocr",
            confidence=0.0,
        )
        assert result.confidence == 0.0

    def test_confidence_exactly_1(self):
        """Confidence of exactly 1.0 is valid."""
        result = ImageAnalysisResult(
            filename="img.png",
            analysis_mode="ocr",
            confidence=1.0,
        )
        assert result.confidence == 1.0

    def test_amount_zero_decimal(self):
        """Amount of Decimal('0.00') is valid."""
        result = ImageAnalysisResult(
            filename="img.png",
            analysis_mode="ocr",
            confidence=0.5,
            amount=Decimal("0.00"),
        )
        assert result.amount == Decimal("0.00")


# ============================================================
# TransactionRecord Tests
# ============================================================

class TestTransactionRecordHappyPath:
    """Happy path tests for TransactionRecord."""

    def test_uuid_auto_generated(self):
        """UUID is automatically generated."""
        record = TransactionRecord(
            transaction_date=date(2024, 1, 15),
            customer_name="陳大文",
            payment_status="paid",
            confidence=0.9,
        )
        assert record.id is not None
        # Validate it's a valid UUID format
        uuid.UUID(record.id)

    def test_uuid_unique(self):
        """Each record gets a unique UUID."""
        record1 = TransactionRecord(
            transaction_date=date(2024, 1, 15),
            customer_name="陳大文",
            payment_status="paid",
            confidence=0.9,
        )
        record2 = TransactionRecord(
            transaction_date=date(2024, 1, 15),
            customer_name="陳大文",
            payment_status="paid",
            confidence=0.9,
        )
        assert record1.id != record2.id

    def test_create_full_record(self):
        """Create with all fields populated."""
        record = TransactionRecord(
            transaction_date=date(2024, 1, 15),
            customer_name="陳大文",
            repair_item="換屏",
            quoted_amount=Decimal("500.00"),
            received_amount=Decimal("500.00"),
            payment_method="payme",
            payment_status="paid",
            source_messages=[0, 1, 2],
            source_images=["img1.jpg"],
            notes="已確認",
            confidence=0.95,
            needs_review=False,
        )
        assert record.customer_name == "陳大文"
        assert record.repair_item == "換屏"
        assert record.payment_status == "paid"


class TestTransactionRecordErrorPath:
    """Error path tests for TransactionRecord."""

    def test_missing_date_raises_error(self):
        """Missing transaction_date raises ValidationError."""
        with pytest.raises(ValidationError):
            TransactionRecord(
                customer_name="陳大文",
                payment_status="paid",
                confidence=0.9,
            )

    def test_missing_customer_name_raises_error(self):
        """Missing customer_name raises ValidationError."""
        with pytest.raises(ValidationError):
            TransactionRecord(
                transaction_date=date(2024, 1, 15),
                payment_status="paid",
                confidence=0.9,
            )

    def test_empty_customer_name_raises_error(self):
        """Empty customer_name raises ValidationError."""
        with pytest.raises(ValidationError):
            TransactionRecord(
                transaction_date=date(2024, 1, 15),
                customer_name="",
                payment_status="paid",
                confidence=0.9,
            )

    def test_invalid_payment_status_raises_error(self):
        """Invalid payment_status raises ValidationError."""
        with pytest.raises(ValidationError):
            TransactionRecord(
                transaction_date=date(2024, 1, 15),
                customer_name="陳大文",
                payment_status="refunded",
                confidence=0.9,
            )

    def test_confidence_out_of_range_raises_error(self):
        """Confidence > 1.0 raises ValidationError."""
        with pytest.raises(ValidationError):
            TransactionRecord(
                transaction_date=date(2024, 1, 15),
                customer_name="陳大文",
                payment_status="paid",
                confidence=2.0,
            )


class TestTransactionRecordEdgeCases:
    """Edge case tests for TransactionRecord."""

    def test_quoted_amount_zero(self):
        """Quoted amount of Decimal('0.00') is valid."""
        record = TransactionRecord(
            transaction_date=date(2024, 1, 15),
            customer_name="陳大文",
            payment_status="unpaid",
            confidence=0.5,
            quoted_amount=Decimal("0.00"),
        )
        assert record.quoted_amount == Decimal("0.00")

    def test_customer_name_with_emoji(self):
        """Customer name with emoji preserved."""
        record = TransactionRecord(
            transaction_date=date(2024, 1, 15),
            customer_name="陳大文 🏠",
            payment_status="paid",
            confidence=0.9,
        )
        assert record.customer_name == "陳大文 🏠"

    def test_defaults_applied(self):
        """Default values correctly applied."""
        record = TransactionRecord(
            transaction_date=date(2024, 1, 15),
            customer_name="陳大文",
            payment_status="paid",
            confidence=0.9,
        )
        assert record.source_messages == []
        assert record.source_images == []
        assert record.notes == ""
        assert record.needs_review is False
        assert record.repair_item is None


# ============================================================
# AppConfig Tests
# ============================================================

class TestAppConfigHappyPath:
    """Happy path tests for AppConfig."""

    def test_defaults(self):
        """All defaults are correctly applied."""
        config = AppConfig()
        assert config.analysis_mode == "ocr"
        assert config.ai_vision_api_key is None
        assert config.tesseract_path is None
        assert config.output_dir == "./output"
        assert config.confidence_threshold == 0.7
        assert config.language == "chi_tra+eng"

    def test_create_with_all_fields(self):
        """Create with all fields specified."""
        config = AppConfig(
            analysis_mode="ai_vision",
            ai_vision_api_key="sk-test-key",
            tesseract_path="C:\\Tesseract\\tesseract.exe",
            output_dir="./results",
            confidence_threshold=0.8,
            language="eng",
        )
        assert config.analysis_mode == "ai_vision"
        assert config.ai_vision_api_key == "sk-test-key"
        assert config.tesseract_path == "C:\\Tesseract\\tesseract.exe"


class TestAppConfigErrorPath:
    """Error path tests for AppConfig."""

    def test_invalid_analysis_mode_raises_error(self):
        """Invalid analysis_mode raises ValidationError."""
        with pytest.raises(ValidationError):
            AppConfig(analysis_mode="invalid")

    def test_confidence_threshold_above_1_raises_error(self):
        """Threshold > 1.0 raises ValidationError."""
        with pytest.raises(ValidationError):
            AppConfig(confidence_threshold=1.5)

    def test_confidence_threshold_below_0_raises_error(self):
        """Threshold < 0.0 raises ValidationError."""
        with pytest.raises(ValidationError):
            AppConfig(confidence_threshold=-0.1)


class TestAppConfigEdgeCases:
    """Edge case tests for AppConfig."""

    def test_tesseract_path_none(self):
        """tesseract_path as None works correctly."""
        config = AppConfig(tesseract_path=None)
        assert config.tesseract_path is None

    def test_threshold_boundary_0(self):
        """Threshold of exactly 0.0 is valid."""
        config = AppConfig(confidence_threshold=0.0)
        assert config.confidence_threshold == 0.0

    def test_threshold_boundary_1(self):
        """Threshold of exactly 1.0 is valid."""
        config = AppConfig(confidence_threshold=1.0)
        assert config.confidence_threshold == 1.0
