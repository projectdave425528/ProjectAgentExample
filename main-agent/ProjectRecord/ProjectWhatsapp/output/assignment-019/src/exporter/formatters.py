"""欄位格式化工具 — 將 TransactionRecord 欄位轉換為 Excel 顯示格式。"""
import re
from datetime import date
from decimal import Decimal


PAYMENT_METHOD_MAP: dict[str, str] = {
    "payme": "PayMe",
    "fps": "轉數快",
    "bank_transfer": "銀行轉帳",
    "cash": "現金",
    "unknown": "未知",
}

PAYMENT_STATUS_MAP: dict[str, str] = {
    "paid": "已付",
    "unpaid": "未付",
    "partial": "部分付款",
}

_QUANTITY_PATTERN = re.compile(r"數量:\s*(\d+)")


def format_date(d: date) -> str:
    """格式化日期為 YYYY-MM-DD。"""
    return d.strftime("%Y-%m-%d")


def format_amount(amount: Decimal | None) -> str:
    """格式化金額，None 返回空字串，有值保留 2 位小數。"""
    if amount is None:
        return ""
    return f"{amount:.2f}"


def format_payment_method(method: str | None) -> str:
    """格式化付款方式為中文顯示名稱。"""
    if method is None:
        return "未知"
    return PAYMENT_METHOD_MAP.get(method, "未知")


def format_payment_status(status: str) -> str:
    """格式化付款狀態為中文顯示名稱。"""
    return PAYMENT_STATUS_MAP.get(status, status)


def extract_quantity_from_notes(notes: str) -> int:
    """從 notes 提取 '數量: X' 中嘅 X，搵唔到返回 1。"""
    match = _QUANTITY_PATTERN.search(notes)
    if match:
        return int(match.group(1))
    return 1
