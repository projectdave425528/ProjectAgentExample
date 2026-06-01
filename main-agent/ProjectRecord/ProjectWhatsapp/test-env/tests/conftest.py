"""Shared fixtures for E2E tests."""
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from src.models.image_result import ImageAnalysisResult


FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_chat_path() -> Path:
    """Return path to sample_chat.txt fixture file."""
    path = FIXTURES_DIR / "sample_chat.txt"
    assert path.exists(), f"Fixture not found: {path}"
    return path


@pytest.fixture
def mock_image_results() -> list[ImageAnalysisResult]:
    """Return 5 ImageAnalysisResult for img001-005.jpg.

    Amounts: 500, 600, 800, 300, 1200
    Payment methods: payme, fps, bank_transfer, payme, fps
    """
    return [
        ImageAnalysisResult(
            filename="img001.jpg",
            analysis_mode="ocr",
            payment_method="payme",
            amount=Decimal("500"),
            transaction_date=date(2024, 1, 15),
            confidence=0.95,
        ),
        ImageAnalysisResult(
            filename="img002.jpg",
            analysis_mode="ocr",
            payment_method="fps",
            amount=Decimal("600"),
            transaction_date=date(2024, 1, 15),
            confidence=0.90,
        ),
        ImageAnalysisResult(
            filename="img003.jpg",
            analysis_mode="ocr",
            payment_method="bank_transfer",
            amount=Decimal("800"),
            transaction_date=date(2024, 1, 15),
            confidence=0.88,
        ),
        ImageAnalysisResult(
            filename="img004.jpg",
            analysis_mode="ocr",
            payment_method="payme",
            amount=Decimal("300"),
            transaction_date=date(2024, 1, 15),
            confidence=0.92,
        ),
        ImageAnalysisResult(
            filename="img005.jpg",
            analysis_mode="ocr",
            payment_method="fps",
            amount=Decimal("1200"),
            transaction_date=date(2024, 1, 15),
            confidence=0.85,
        ),
    ]


@pytest.fixture
def tmp_output_path(tmp_path) -> Path:
    """Return a temporary output.xlsx path under tmp_path."""
    return tmp_path / "output.xlsx"
