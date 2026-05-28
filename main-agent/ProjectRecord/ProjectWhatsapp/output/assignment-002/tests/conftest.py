"""Shared pytest fixtures for WhatsApp accounting tests."""
import pytest
from datetime import datetime, date
from decimal import Decimal

from src.models.message import ParsedMessage
from src.models.image_result import ImageAnalysisResult
from src.models.transaction import TransactionRecord
from src.models.config import AppConfig


@pytest.fixture
def sample_parsed_message():
    """Create a sample ParsedMessage fixture."""
    return ParsedMessage(
        timestamp=datetime(2024, 1, 15, 14, 30, 0),
        sender="陳大文",
        content="換屏，報價五百蚊",
        is_system_message=False,
        attachments=[],
        raw_text="[2024/01/15, 14:30:00] 陳大文: 換屏，報價五百蚊",
    )


@pytest.fixture
def sample_image_result():
    """Create a sample ImageAnalysisResult fixture."""
    return ImageAnalysisResult(
        filename="IMG-20240115-WA0001.jpg",
        image_date=date(2024, 1, 15),
        analysis_mode="ocr",
        payment_method="payme",
        amount=Decimal("500.00"),
        transaction_date=date(2024, 1, 15),
        transaction_id="TXN123456",
        confidence=0.85,
        raw_text="PayMe $500.00",
        needs_review=False,
        error=None,
    )


@pytest.fixture
def sample_transaction_record():
    """Create a sample TransactionRecord fixture."""
    return TransactionRecord(
        transaction_date=date(2024, 1, 15),
        customer_name="陳大文",
        repair_item="換屏",
        quoted_amount=Decimal("500.00"),
        received_amount=Decimal("500.00"),
        payment_method="payme",
        payment_status="paid",
        source_messages=[0, 1, 2],
        source_images=["IMG-20240115-WA0001.jpg"],
        notes="",
        confidence=0.85,
        needs_review=False,
    )


@pytest.fixture
def sample_app_config():
    """Create a sample AppConfig fixture."""
    return AppConfig(
        analysis_mode="ocr",
        ai_vision_api_key=None,
        tesseract_path=None,
        output_dir="./output",
        confidence_threshold=0.7,
        language="chi_tra+eng",
    )
