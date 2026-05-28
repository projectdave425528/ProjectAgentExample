"""WhatsApp .txt chat file parser.

Reads a WhatsApp chat export file line by line,
parses messages using regex patterns, handles multi-line
messages, system messages, and media attachments.
"""

import logging
from pathlib import Path
from typing import Optional

from src.models.message import ParsedMessage
from src.parser.patterns import (
    extract_attachment,
    is_system_message,
    match_message_line,
)
from src.parser.utils import parse_timestamp

logger = logging.getLogger(__name__)


def parse_chat_file(file_path: str) -> list[ParsedMessage]:
    """Parse a WhatsApp chat export .txt file.

    Reads the file line by line to handle large files
    without loading everything into memory.

    Args:
        file_path: Path to the .txt chat export file.

    Returns:
        List of ParsedMessage objects.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(
            f"搵唔到文件：{file_path}，請確認路徑是否正確"
        )
    if path.stat().st_size == 0:
        logger.warning("文件為空：%s", file_path)
        return []
    return _read_and_parse(path)


def _read_and_parse(path: Path) -> list[ParsedMessage]:
    """Read file line by line and parse into messages.

    Args:
        path: Validated Path object.

    Returns:
        List of ParsedMessage objects.
    """
    messages: list[ParsedMessage] = []
    pending: Optional[dict] = None

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            matched = match_message_line(line)
            if matched:
                if pending:
                    _finalize_message(pending, messages)
                pending = _create_pending(matched, line)
            else:
                pending = _append_continuation(
                    pending, line, messages
                )

    if pending:
        _finalize_message(pending, messages)
    return messages


def _create_pending(matched: tuple, raw_line: str) -> dict:
    """Create a pending message dict from a matched line.

    Args:
        matched: Tuple of (timestamp_str, sender, content).
        raw_line: The original raw line text.

    Returns:
        Dict with message fields for later finalization.
    """
    timestamp_str, sender, content = matched
    return {
        "timestamp_str": timestamp_str,
        "sender": sender,
        "content": content,
        "raw_lines": [raw_line],
    }


def _append_continuation(
    pending: Optional[dict], line: str, messages: list
) -> Optional[dict]:
    """Append a continuation line to the pending message.

    If no pending message exists, logs a warning and skips.

    Args:
        pending: Current pending message dict or None.
        line: The continuation line text.
        messages: Messages list (unused, for signature).

    Returns:
        Updated pending dict or None.
    """
    if not line.strip():
        if pending:
            pending["content"] += "\n"
            pending["raw_lines"].append(line)
        return pending
    if pending is None:
        logger.warning("無法解析嘅行（無前置訊息）：%s", line)
        return None
    pending["content"] += "\n" + line
    pending["raw_lines"].append(line)
    return pending


def _finalize_message(
    pending: dict, messages: list[ParsedMessage]
) -> None:
    """Convert pending dict to ParsedMessage and append.

    Handles timestamp parsing, system message detection,
    and attachment extraction.

    Args:
        pending: Pending message dict.
        messages: List to append the finalized message to.
    """
    timestamp = parse_timestamp(pending["timestamp_str"])
    if timestamp is None:
        logger.warning(
            "無法解析時間戳：%s", pending["timestamp_str"]
        )
        return
    content = pending["content"]
    attachments = _extract_attachments(content)
    system_flag = is_system_message(content)
    raw_text = "\n".join(pending["raw_lines"])

    msg = ParsedMessage(
        timestamp=timestamp,
        sender=pending["sender"],
        content=content,
        is_system_message=system_flag,
        attachments=attachments,
        raw_text=raw_text,
    )
    messages.append(msg)


def _extract_attachments(content: str) -> list[str]:
    """Extract all attachment filenames from content.

    Args:
        content: Message content string.

    Returns:
        List of attachment filenames (may be empty).
    """
    attachment = extract_attachment(content)
    if attachment:
        return [attachment]
    return []
