"""AppConfig model for application configuration."""
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class AppConfig(BaseModel):
    """Application configuration model."""

    analysis_mode: Literal["ocr", "ai_vision"] = Field(
        default="ocr", description="分析模式"
    )
    ai_vision_api_key: str | None = Field(
        default=None, description="AI Vision API Key"
    )
    tesseract_path: str | None = Field(
        default=None, description="Tesseract OCR 路徑"
    )
    output_dir: str = Field(
        default="./output", description="輸出目錄"
    )
    confidence_threshold: float = Field(
        default=0.7, description="信心度閾值"
    )
    language: str = Field(
        default="chi_tra+eng", description="Tesseract 語言包"
    )

    @field_validator("confidence_threshold")
    @classmethod
    def validate_threshold(cls, v: float) -> float:
        """Validate confidence_threshold is between 0.0 and 1.0."""
        if v < 0.0 or v > 1.0:
            raise ValueError(
                "confidence_threshold 必須介於 0.0 到 1.0 之間"
            )
        return v
