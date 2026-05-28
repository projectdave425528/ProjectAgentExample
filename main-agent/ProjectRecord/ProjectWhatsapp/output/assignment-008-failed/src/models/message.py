"""ParsedMessage model for WhatsApp chat messages."""
from datetime import datetime
from pydantic import BaseModel, Field


class ParsedMessage(BaseModel):
    """Represents a single parsed WhatsApp message."""

    timestamp: datetime = Field(
        ..., description="訊息時間戳"
    )
    sender: str = Field(
        ..., min_length=1, description="發送者名稱"
    )
    content: str = Field(
        ..., description="訊息內容"
    )
    is_system_message: bool = Field(
        default=False, description="是否系統訊息"
    )
    attachments: list[str] = Field(
        default_factory=list, description="附件文件名列表"
    )
    raw_text: str = Field(
        ..., min_length=1, description="原始文字（debug 用）"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "timestamp": "2024-01-15T14:30:00",
                    "sender": "John",
                    "content": "Hello",
                    "is_system_message": False,
                    "attachments": [],
                    "raw_text": "[2024/01/15, 14:30:00] John: Hello",
                }
            ]
        }
    }
