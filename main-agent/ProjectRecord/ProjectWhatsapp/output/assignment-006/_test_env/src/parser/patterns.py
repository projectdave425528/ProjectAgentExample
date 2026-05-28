"""Regex patterns for WhatsApp chat export parsing.

Supports multiple timestamp formats:
- 24-hour: [2024/01/15, 14:30:00]
- 12-hour: [1/15/24, 2:30 PM]
- Date separators: / - .
- Date orders: YYYY/MM/DD, DD/MM/YYYY, MM/DD/YYYY
"""

import re
from typing import Optional

# --- Date component patterns ---
# Matches 1-4 digit date components (day, month, year)
_DATE_PART = r"\d{1,4}"
# Date separators: / - .
_DATE_SEP = r"[/\-.]"
# Full date: e.g. 2024/01/15, 15-01-2024, 1.15.24
_DATE = rf"{_DATE_PART}{_DATE_SEP}{_DATE_PART}{_DATE_SEP}{_DATE_PART}"

# --- Time component patterns ---
# 24-hour time: HH:MM or HH:MM:SS
_TIME_24 = r"\d{1,2}:\d{2}(?::\d{2})?"
# 12-hour time: H:MM AM/PM or H:MM:SS AM/PM
_TIME_12 = r"\d{1,2}:\d{2}(?::\d{2})?\s*[AaPp][Mm]"
# Combined time pattern (12-hour first for greedy match)
_TIME = rf"(?:{_TIME_12}|{_TIME_24})"

# --- Main message pattern ---
# Matches: [timestamp] sender: content
# Group 1: timestamp (date + time)
# Group 2: rest (sender: content)
MESSAGE_PATTERN = re.compile(
    rf"^\[({_DATE},\s*{_TIME})\]\s(.+)$"
)

# --- Attachment pattern ---
# Matches: <attached: filename> or <attached:filename>
ATTACHMENT_PATTERN = re.compile(
    r"<attached:\s*([^>]+)>"
)

# --- System message keywords ---
SYSTEM_MESSAGE_KEYWORDS = [
    "加入了群組",
    "已加入",
    "離開了",
    "已離開",
    "更改了群組名稱",
    "更改了群組圖片",
    "更改了群組描述",
    "你已被移除",
    "已被移除",
    "訊息已刪除",
    "此訊息已刪除",
    "Messages and calls are end-to-end encrypted",
    "joined using this group",
    "left",
    "changed the group",
    "removed",
    "deleted this message",
    "created group",
    "added",
    "changed the subject",
    "changed this group's icon",
]


def is_system_message(content: str) -> bool:
    """Check if message content is a system message.

    Args:
        content: The message content string.

    Returns:
        True if content matches any system message keyword.
    """
    if not content:
        return False
    for keyword in SYSTEM_MESSAGE_KEYWORDS:
        if keyword in content:
            return True
    return False


def extract_attachment(content: str) -> Optional[str]:
    """Extract attachment filename from message content.

    Args:
        content: The message content string.

    Returns:
        Filename string if found, None otherwise.
    """
    if not content:
        return None
    match = ATTACHMENT_PATTERN.search(content)
    if match:
        return match.group(1).strip()
    return None


def match_message_line(line: str) -> Optional[tuple]:
    """Match a line against the WhatsApp message pattern.

    Args:
        line: A single line from the chat export.

    Returns:
        Tuple of (timestamp_str, sender, content) if matched,
        None if the line doesn't match the message pattern.
    """
    if not line:
        return None
    match = MESSAGE_PATTERN.match(line.strip())
    if not match:
        return None
    timestamp_str = match.group(1)
    rest = match.group(2)
    parts = split_sender_content(rest)
    if parts is None:
        return None
    sender, content = parts
    return (timestamp_str, sender, content)


def split_sender_content(rest: str) -> Optional[tuple]:
    """Split the rest part into sender and content.

    Uses the first ': ' as delimiter so senders with colons
    in their names (e.g. 'Dr. Wong: 醫生') are handled correctly.

    Args:
        rest: The string after timestamp, e.g. 'John: Hello'.

    Returns:
        Tuple of (sender, content) or None if no delimiter found.
    """
    if not rest:
        return None
    delimiter_idx = rest.find(": ")
    if delimiter_idx == -1:
        return None
    sender = rest[:delimiter_idx]
    content = rest[delimiter_idx + 2:]
    return (sender, content)
