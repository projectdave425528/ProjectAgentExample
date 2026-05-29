"""WhatsApp chat file parser."""
import logging
from pathlib import Path
from typing import Optional

from src.models.message import ParsedMessage
from src.parser.patterns import extract_attachment, is_system_message, match_message_line
from src.parser.utils import parse_timestamp

logger = logging.getLogger(__name__)


def parse_chat_file(file_path: str) -> list[ParsedMessage]:
    """Parse a WhatsApp .txt chat export into ParsedMessage list."""
    path = _validate_file_path(file_path)
    encoding = _detect_encoding(path)
    return _parse_lines(path, encoding)


def _validate_file_path(file_path: str) -> Path:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Chat file not found: {file_path}")
    return path


def _detect_encoding(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        if _can_read_with_encoding(path, encoding):
            return encoding
    return "latin-1"


def _can_read_with_encoding(path: Path, encoding: str) -> bool:
    try:
        with open(path, "r", encoding=encoding) as f:
            f.read(1024)
        return True
    except (UnicodeDecodeError, ValueError):
        return False


def _parse_lines(path: Path, encoding: str) -> list[ParsedMessage]:
    if path.stat().st_size == 0:
        logger.warning("Empty chat file: %s", path)
        return []
    messages: list[ParsedMessage] = []
    pending = {"active": False}
    with open(path, "r", encoding=encoding) as f:
        for line in f:
            pending = _process_line(line, pending, messages)
    _flush_pending(pending, messages)
    return messages


def _process_line(line: str, pending: dict, messages: list) -> dict:
    stripped = line.rstrip("\n\r")
    match_result = match_message_line(stripped)
    if match_result is not None:
        _flush_pending(pending, messages)
        timestamp_str, sender, content = match_result
        # System messages have empty sender
        if not sender:
            sender = content  # Use content as sender for system msgs
        return {"timestamp_str": timestamp_str, "sender": sender, "content": content, "raw_lines": [stripped], "active": True}
    if not pending["active"]:
        if stripped.strip():
            logger.warning("Skipping unparseable line: %s", stripped)
        return pending
    pending["content"] += "\n" + stripped
    pending["raw_lines"].append(stripped)
    return pending


def _flush_pending(pending: dict, messages: list) -> None:
    if not pending["active"]:
        return
    msg = _build_message(pending)
    if msg is not None:
        messages.append(msg)
    pending["active"] = False


def _build_message(pending: dict) -> Optional[ParsedMessage]:
    timestamp = parse_timestamp(pending["timestamp_str"])
    if timestamp is None:
        logger.warning("Failed to parse timestamp: %s", pending["timestamp_str"])
        return None
    content = pending["content"]
    raw_text = "\n".join(pending["raw_lines"])
    attachment = extract_attachment(content)
    attachments = [attachment] if attachment else []
    system_flag = is_system_message(content)
    return ParsedMessage(
        timestamp=timestamp, sender=pending["sender"], content=content,
        is_system_message=system_flag, attachments=attachments, raw_text=raw_text,
    )
