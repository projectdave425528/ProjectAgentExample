"""Transaction information extraction from matched pairs.

Extracts customer name, repair item, quantity, and quoted amount
from MatchedPair message content. Supports Cantonese expressions.
"""
import re
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# --- Constants ---

REPAIR_KEYWORDS: list[str] = [
    "換屏", "換芒", "換mon", "換MON",
    "換電池", "換電",
    "換殼", "換背蓋",
    "維修", "整機",
    "貼膜", "貼玻璃貼",
    "換鏡頭", "換cam",
    "換充電口", "換尾插",
]

CHINESE_DIGITS: dict[str, int] = {
    "零": 0, "一": 1, "二": 2, "兩": 2,
    "三": 3, "四": 4, "五": 5,
    "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
}

CHINESE_AMOUNTS: dict[str, int] = {
    "一百": 100, "二百": 200, "兩百": 200,
    "三百": 300, "四百": 400, "五百": 500,
    "六百": 600, "七百": 700, "八百": 800,
    "九百": 900, "一千": 1000, "兩千": 2000,
    "三千": 3000, "四千": 4000, "五千": 5000,
}

# Regex patterns for amount extraction
AMOUNT_PATTERNS: list[re.Pattern] = [
    re.compile(r"HK\$\s*([\d,]+(?:\.\d{1,2})?)"),
    re.compile(r"\$\s*([\d,]+(?:\.\d{1,2})?)"),
    re.compile(r"([\d,]+(?:\.\d{1,2})?)\s*蚊"),
    re.compile(r"([\d,]+(?:\.\d{1,2})?)\s*元"),
]

# Regex patterns for quantity extraction
QUANTITY_PATTERNS: list[re.Pattern] = [
    re.compile(r"[xX×]\s*(\d+)"),
    re.compile(r"(\d+)\s*[部台隻個]"),
]

DEFAULT_TIME_WINDOW_HOURS: int = 2


# --- Models ---

class ExtractionResult(BaseModel):
    """Intermediate extraction result with quantity."""

    customer_name: str = Field(
        ..., description="客戶名稱"
    )
    repair_item: Optional[str] = Field(
        default=None, description="維修項目"
    )
    quoted_amount: Optional[Decimal] = Field(
        default=None, description="報價金額（單價）"
    )
    quantity: int = Field(
        default=1, description="數量"
    )
    timestamp: datetime = Field(
        ..., description="交易時間"
    )
    confidence: float = Field(
        default=0.5, description="提取信心度"
    )


# --- Public Functions ---

def extract_customer_name(sender: str) -> str:
    """Extract customer name from message sender.

    Returns 'Unknown' if sender is empty or whitespace.
    """
    name = sender.strip() if sender else ""
    return name if name else "Unknown"


def extract_repair_item(content: str) -> Optional[str]:
    """Extract repair item from message content using keywords.

    Returns the first matching keyword found, or None.
    """
    for keyword in REPAIR_KEYWORDS:
        if keyword.lower() in content.lower():
            return keyword
    return None


def extract_quantity(content: str) -> int:
    """Extract quantity from message content.

    Supports formats: '3部', 'x2', '×3', '2台', '兩部', '三部'.
    Returns 1 as default if no quantity found.
    """
    # Check Chinese digit + unit patterns first
    chinese_qty = _extract_chinese_quantity(content)
    if chinese_qty is not None:
        return chinese_qty

    # Check numeric patterns
    for pattern in QUANTITY_PATTERNS:
        match = pattern.search(content)
        if match:
            return int(match.group(1))

    return 1


def extract_quoted_amount(content: str) -> Optional[Decimal]:
    """Extract quoted amount from message content.

    Supports: $xxx, HK$xxx, xxx蚊, xxx元, and Cantonese amounts.
    Returns the unit price as Decimal, or None if not found.
    """
    # Try numeric patterns first
    for pattern in AMOUNT_PATTERNS:
        match = pattern.search(content)
        if match:
            raw = match.group(1).replace(",", "")
            return Decimal(raw)

    # Try Cantonese amount expressions
    return _extract_chinese_amount(content)


def extract_from_matched_pair(pair) -> ExtractionResult:
    """Extract transaction info from a single MatchedPair.

    Args:
        pair: A MatchedPair instance with message and image_result.

    Returns:
        ExtractionResult with extracted fields.
    """
    content = pair.message.content
    sender = pair.message.sender

    customer_name = extract_customer_name(sender)
    repair_item = extract_repair_item(content)
    quantity = extract_quantity(content)
    quoted_amount = extract_quoted_amount(content)
    confidence = _calculate_confidence(
        repair_item, quoted_amount
    )

    return ExtractionResult(
        customer_name=customer_name,
        repair_item=repair_item,
        quoted_amount=quoted_amount,
        quantity=quantity,
        timestamp=pair.message.timestamp,
        confidence=confidence,
    )


def group_by_time_window(
    results: list[ExtractionResult],
    window_hours: int = DEFAULT_TIME_WINDOW_HOURS,
) -> list[list[ExtractionResult]]:
    """Group extraction results by customer and time window.

    Same customer within the time window but with different
    quoted amounts are treated as separate transactions.

    Args:
        results: List of ExtractionResult to group.
        window_hours: Time window in hours (default 2).

    Returns:
        List of groups, each group is a list of ExtractionResult.
    """
    if not results:
        return []

    sorted_results = sorted(
        results, key=lambda r: (r.customer_name, r.timestamp)
    )
    groups: list[list[ExtractionResult]] = []
    current_group: list[ExtractionResult] = [sorted_results[0]]

    for result in sorted_results[1:]:
        prev = current_group[-1]
        same_customer = (
            result.customer_name == prev.customer_name
        )
        within_window = _is_within_window(
            prev.timestamp, result.timestamp, window_hours
        )
        same_amount = (
            result.quoted_amount == prev.quoted_amount
        )

        if same_customer and within_window and same_amount:
            current_group.append(result)
        else:
            groups.append(current_group)
            current_group = [result]

    groups.append(current_group)
    return groups


# --- Private Helpers ---

def _extract_chinese_quantity(content: str) -> Optional[int]:
    """Extract quantity from Chinese digit expressions."""
    for char, value in CHINESE_DIGITS.items():
        if value == 0:
            continue
        for unit in ["部", "台", "隻", "個"]:
            if f"{char}{unit}" in content:
                return value
    return None


def _extract_chinese_amount(content: str) -> Optional[Decimal]:
    """Extract amount from Cantonese expressions."""
    for text, value in CHINESE_AMOUNTS.items():
        # Match with or without trailing unit (蚊/元)
        if text in content:
            return Decimal(value)
        if f"{text}蚊" in content:
            return Decimal(value)
    return None


def _calculate_confidence(
    repair_item: Optional[str],
    quoted_amount: Optional[Decimal],
) -> float:
    """Calculate extraction confidence score."""
    score = 0.3  # base score for having a customer name
    if repair_item is not None:
        score += 0.35
    if quoted_amount is not None:
        score += 0.35
    return round(score, 2)


def _is_within_window(
    ts1: datetime, ts2: datetime, hours: int
) -> bool:
    """Check if two timestamps are within the time window."""
    delta = timedelta(hours=hours)
    return abs(ts2 - ts1) <= delta
