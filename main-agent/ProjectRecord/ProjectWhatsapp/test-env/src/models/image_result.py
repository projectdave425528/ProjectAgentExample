"""ImageAnalysisResult model for image analysis output."""
from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ImageAnalysisResult(BaseModel):
    """Represents the result of analyzing a payment image."""

    filename: str = Field(
        ..., min_length=1, description="圖片文件名"
    )
    image_date: date | None = Field(
        default=None, description="從文件名提取嘅日期"
    )
    analysis_mode: Literal["ocr", "ai_vision"] = Field(
        ..., description="分析模式"
    )
    payment_method: Literal[
        "payme", "fps", "bank_transfer", "unknown"
    ] | None = Field(
        default=None, description="付款方式"
    )
    amount: Decimal | None = Field(
        default=None, description="金額"
    )
    transaction_date: date | None = Field(
        default=None, description="交易日期"
    )
    transaction_id: str | None = Field(
        default=None, description="交易編號"
    )
    confidence: float = Field(
        ..., description="信心度 (0.0 - 1.0)"
    )
    raw_text: str | None = Field(
        default=None, description="OCR 提取嘅原始文字"
    )
    needs_review: bool = Field(
        default=False, description="信心度低時標記"
    )
    error: str | None = Field(
        default=None, description="分析失敗時記錄原因"
    )

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Validate confidence is between 0.0 and 1.0."""
        if v < 0.0 or v > 1.0:
            raise ValueError(
                "confidence 必須介於 0.0 到 1.0 之間"
            )
        return v
