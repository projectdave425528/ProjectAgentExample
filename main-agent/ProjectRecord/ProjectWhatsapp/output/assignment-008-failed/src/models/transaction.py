"""TransactionRecord model for transaction records."""
import uuid
from datetime import date as DateType
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, field_validator


def _generate_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid.uuid4())


class TransactionRecord(BaseModel):
    """Represents a complete transaction record."""

    id: str = Field(
        default_factory=_generate_uuid,
        description="UUID 唯一識別碼",
    )
    transaction_date: DateType = Field(
        ..., description="交易日期"
    )
    customer_name: str = Field(
        ..., min_length=1, description="客戶名稱"
    )
    repair_item: str | None = Field(
        default=None, description="維修項目"
    )
    quoted_amount: Decimal | None = Field(
        default=None, description="報價金額"
    )
    received_amount: Decimal | None = Field(
        default=None, description="實收金額"
    )
    payment_method: Literal[
        "payme", "fps", "bank_transfer", "cash", "unknown"
    ] | None = Field(
        default=None, description="付款方式"
    )
    payment_status: Literal["paid", "unpaid", "partial"] = Field(
        ..., description="付款狀態"
    )
    source_messages: list[int] = Field(
        default_factory=list, description="來源訊息 indices"
    )
    source_images: list[str] = Field(
        default_factory=list, description="來源圖片文件名"
    )
    notes: str = Field(
        default="", description="備註"
    )
    confidence: float = Field(
        ..., description="整體信心度 (0.0 - 1.0)"
    )
    needs_review: bool = Field(
        default=False, description="需要人工確認"
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
