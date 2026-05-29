"""Regex patterns for WhatsApp chat export parsing."""
import re
from typing import Optional

_DATE_PART = r"\d{1,4}"
_DATE_SEP = r"[/\-.]"
_DATE = rf"{_DATE_PART}{_DATE_SEP}{_DATE_PART}{_DATE_SEP}{_DATE_PART}"
_TIME_24 = r"\d{1,2}:\d{2}(?::\d{2})?"
_TIME_12 = r"\d{1,2}:\d{2}(?::\d{2})?\s*[AaPp][Mm]"
_TIME = rf"(?:{_TIME_12}|{_TIME_24})"

MESSAGE_PATTERN = re.compile(rf"^\[({_DATE},\s*{_TIME})\]\s(.+)$")
ATTACHMENT_PATTERN = re.compile(r"<attached:\s*([^>]+)>")

SYSTEM_MESSAGE_KEYWORDS = [
    "加入了群組", "已加入", "離開了", "已離開",
    "更改了群組名稱", "更改了群組圖片", "更改了群組描述",
    "你已被移除", "已被移除", "訊息已刪除", "此訊息已刪除",
    "Messages and calls are end-to-end encrypted",
    "joined using this group", "left", "changed the group",
    "removed", "deleted this message", "created group",
    "added", "changed the subject", "changed this group's icon",
]


def is_system_message(content: str) -> bool:
    if not content:
        return False
    return any(kw in content for kw in SYSTEM_MESSAGE_KEYWORDS)


def extract_attachment(content: str) -> Optional[str]:
    if not content:
        return None
    match = ATTACHMENT_PATTERN.search(content)
    return match.group(1).strip() if match else None


def match_message_line(line: str) -> Optional[tuple]:
    if not line:
        return None
    match = MESSAGE_PATTERN.match(line.strip())
    if not match:
        return None
    timestamp_str = match.group(1)
    rest = match.group(2)
    parts = split_sender_content(rest)
    if parts is None:
        # System message (has timestamp but no ': ' delimiter)
        return (timestamp_str, "", rest)
    return (timestamp_str, parts[0], parts[1])


def split_sender_content(rest: str) -> Optional[tuple]:
    if not rest:
        return None
    delimiter_idx = rest.find(": ")
    if delimiter_idx == -1:
        return None
    return (rest[:delimiter_idx], rest[delimiter_idx + 2:])
