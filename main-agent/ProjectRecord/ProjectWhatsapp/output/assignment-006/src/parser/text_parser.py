"""WhatsApp chat file parser.

Reads a .txt chat export line by line, parses each message
using regex patterns from Task 2, handles multi-line messages,
system messages, and media attachments.
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
    """Parse a WhatsApp .txt chat export into ParsedMessage list.

    Reads the file line by line to handle large files without
    loading everything into memory. Supports UTF-8, UTF-8-sig,
    and latin-1 encodings.

    Args:
        file_path: Path to the .txt chat export file.

    Returns:
        List of ParsedMessage objects.

    Raises:
        FileNotFoundError: If file_path does not exist.
    """
    path = _validate_file_path(file_path)
    encoding = _detect_encoding(path)
    return _parse_lines(path, encoding)


def _validate_file_path(file_path: str) -> Path:
    """Validate that the file exists and return Path object.

    Args:
        file_path: Path string to validate.

    Returns:
        Path object for the file.

    Raises:
        FileNotFoundError: If file does not exist.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Chat file not found: {file_path}"
        )
    return path


def _detect_encoding(path: Path) -> str:
    """Detect file encoding by trying UTF-8 first, then fallbacks.

    Args:
        path: Path to the file.

    Returns:
        Encoding string that successfully reads the file.
    """
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        if _can_read_with_encoding(path, encoding):
            return encoding
    return "latin-1"


def _can_read_with_encoding(path: Path, encoding: str) -> bool:
    """Test if a file can be read with the given encoding.

    Args:
        path: Path to the file.
        encoding: Encoding to test.

    Returns:
        True if file reads without error.
    """
    try:
        with open(path, "r", encoding=encoding) as f:
            f.read(1024)
        return True
    except (UnicodeDecodeError, ValueError):
        return False


def _parse_lines(path: Path, encoding: str) -> list[ParsedMessage]:
    """Read file line by line and build ParsedMessage list.

    Args:
        path: Path to the chat file.
        encoding: File encoding to use.

    Returns:
        List of ParsedMessage objects.
    """
    if path.stat().st_size == 0:
        logger.warning("Empty chat file: %s", path)
        return []

    messages: list[ParsedMessage] = []
    pending = _new_pending_state()

    with open(path, "r", encoding=encoding) as f:
        for line in f:
            pending = _process_line(line, pending, messages)

    _flush_pending(pending, messages)
    return messages


def _process_line(
    line: str, pending: dict, messages: list[ParsedMessage]
) -> dict:
    """Process a single line from the chat file.

    Args:
        line: Current line text.
        pending: Current pending message state.
        messages: Accumulated messages list (mutated).

    Returns:
        Updated pending state.
    """
    stripped = line.rstrip("\n\r")
    match_result = match_message_line(stripped)

    if match_result is not None:
        _flush_pending(pending, messages)
        return _start_new_message(match_result, stripped)

    _append_continuation(pending, stripped)
    return pending


def _start_new_message(match_result: tuple, raw: str) -> dict:
    """Create a new pending message state from a match result.

    Args:
        match_result: Tuple of (timestamp_str, sender, content).
        raw: The raw line text.

    Returns:
        New pending state dict.
    """
    timestamp_str, sender, content = match_result
    return {
        "timestamp_str": timestamp_str,
        "sender": sender,
        "content": content,
        "raw_lines": [raw],
        "active": True,
    }


def _append_continuation(pending: dict, line: str) -> None:
    """Append a continuation line to the pending message.

    Args:
        pending: Current pending state (mutated).
        line: Continuation line text.
    """
    if not pending["active"]:
        if line.strip():
            logger.warning("Skipping unparseable line: %s", line)
        return
    pending["content"] += "\n" + line
    pending["raw_lines"].append(line)


def _flush_pending(
    pending: dict, messages: list[ParsedMessage]
) -> None:
    """Convert pending state to ParsedMessage and append.

    Args:
        pending: Current pending state.
        messages: Messages list to append to (mutated).
    """
    if not pending["active"]:
        return
    msg = _build_message(pending)
    if msg is not None:
        messages.append(msg)
    pending["active"] = False


def _build_message(pending: dict) -> Optional[ParsedMessage]:
    """Build a ParsedMessage from pending state.

    Args:
        pending: Pending message state dict.

    Returns:
        ParsedMessage or None if timestamp parsing fails.
    """
    timestamp = parse_timestamp(pending["timestamp_str"])
    if timestamp is None:
        logger.warning(
            "Failed to parse timestamp: %s",
            pending["timestamp_str"],
        )
        return None

    content = pending["content"]
    raw_text = "\n".join(pending["raw_lines"])
    attachments = _extract_attachments(content)
    system_flag = is_system_message(content)

    return ParsedMessage(
        timestamp=timestamp,
        sender=pending["sender"],
        content=content,
        is_system_message=system_flag,
        attachments=attachments,
        raw_text=raw_text,
    )


def _extract_attachments(content: str) -> list[str]:
    """Extract all attachment filenames from content.

    Args:
        content: Message content string.

    Returns:
        List of attachment filenames found.
    """
    attachment = extract_attachment(content)
    if attachment is not None:
        return [attachment]
    return []


def _new_pending_state() -> dict:
    """Create an empty pending message state.

    Returns:
        Dict with active=False.
    """
    return {"active": False}
