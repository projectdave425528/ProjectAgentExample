"""Quick smoke tests for all models."""
import uuid
from datetime import date, datetime
from decimal import Decimal
import pytest
from pydantic import ValidationError
from src.models.message import ParsedMessage
from src.models.image_result import ImageAnalysisResult
from src.models.transaction import TransactionRecord
from src.models.config import AppConfig


class TestParsedMessage:
    def test_create_valid(self):
        msg = ParsedMessage(
            timestamp=datetime(2024, 1, 15, 14, 30),
            sender="陳大文", content="你好",
            raw_text="[2024/01/15, 14:30:00] 陳大文: 你好",
        )
        assert msg.sender == "陳大文"

    def test_missing_sender_raises(self):
        with pytest.raises(ValidationError):
            ParsedMessage(timestamp=datetime(2024, 1, 15), content="Hi", raw_text="raw")

    def test_emoji_sender(self):
        msg = ParsedMessage(
            timestamp=datetime(2024, 1, 15), sender="🔧師傅",
            content="Hi", raw_text="raw text",
        )
        assert "🔧" in msg.sender


class TestImageAnalysisResult:
    def test_confidence_valid(self):
        r = ImageAnalysisResult(filename="img.jpg", analysis_mode="ocr", confidence=0.95)
        assert r.confidence == 0.95

    def test_confidence_above_1_raises(self):
        with pytest.raises(ValidationError):
            ImageAnalysisResult(filename="img.jpg", analysis_mode="ocr", confidence=1.5)

    def test_amount_decimal(self):
        r = ImageAnalysisResult(
            filename="img.jpg", analysis_mode="ocr",
            confidence=0.9, amount=Decimal("500.00"),
        )
        assert r.amount == Decimal("500.00")


class TestTransactionRecord:
    def test_uuid_auto_generated(self):
        r = TransactionRecord(
            transaction_date=date(2024, 1, 15),
            customer_name="陳大文", payment_status="paid", confidence=0.9,
        )
        uuid.UUID(r.id)  # validates format

    def test_uuid_unique(self):
        r1 = TransactionRecord(transaction_date=date(2024, 1, 15), customer_name="A", payment_status="paid", confidence=0.9)
        r2 = TransactionRecord(transaction_date=date(2024, 1, 15), customer_name="A", payment_status="paid", confidence=0.9)
        assert r1.id != r2.id


class TestAppConfig:
    def test_defaults(self):
        c = AppConfig()
        assert c.analysis_mode == "ocr"
        assert c.confidence_threshold == 0.7

    def test_invalid_mode_raises(self):
        with pytest.raises(ValidationError):
            AppConfig(analysis_mode="invalid")
