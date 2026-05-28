"""Unit tests for text_parser module.

Covers Happy Path, Error Path, and Edge Cases as specified
in Task 3 test criteria.
"""

import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from src.parser.text_parser import (
    _build_message,
    _detect_encoding,
    _extract_attachments,
    _validate_file_path,
    parse_chat_file,
)


# --- Fixtures ---


@pytest.fixture
def sample_chat_path():
    """Path to the sample_chat.txt fixture."""
    return str(
        Path(__file__).parent.parent
        / "fixtures"
        / "sample_chat.txt"
    )


@pytest.fixture
def empty_file(tmp_path):
    """Create an empty chat file."""
    f = tmp_path / "empty.txt"
    f.write_text("", encoding="utf-8")
    return str(f)


@pytest.fixture
def single_message_file(tmp_path):
    """Create a file with one message."""
    content = "[2024/01/15, 10:00:00] Alice: Hello World\n"
    f = tmp_path / "single.txt"
    f.write_text(content, encoding="utf-8")
    return str(f)


@pytest.fixture
def multiline_file(tmp_path):
    """Create a file with multi-line messages."""
    content = (
        "[2024/01/15, 10:00:00] Alice: Line one\n"
        "Line two\n"
        "Line three\n"
        "[2024/01/15, 10:01:00] Bob: Reply\n"
    )
    f = tmp_path / "multiline.txt"
    f.write_text(content, encoding="utf-8")
    return str(f)


@pytest.fixture
def system_message_file(tmp_path):
    """Create a file with system messages."""
    content = (
        "[2024/01/15, 09:00:00] Messages and calls are "
        "end-to-end encrypted. No one outside of this chat, "
        "not even WhatsApp, can read or listen to them.\n"
        "[2024/01/15, 09:01:00] Alice: Hi\n"
        "[2024/01/15, 09:02:00] Bob joined using this "
        "group's invite link\n"
    )
    f = tmp_path / "system.txt"
    f.write_text(content, encoding="utf-8")
    return str(f)


@pytest.fixture
def attachment_file(tmp_path):
    """Create a file with attachment messages."""
    content = (
        "[2024/01/15, 10:00:00] Alice: "
        "<attached: photo.jpg>\n"
        "[2024/01/15, 10:01:00] Bob: Nice pic!\n"
    )
    f = tmp_path / "attach.txt"
    f.write_text(content, encoding="utf-8")
    return str(f)


@pytest.fixture
def latin1_file(tmp_path):
    """Create a file encoded in latin-1."""
    content = "[2024/01/15, 10:00:00] Alice: caf\xe9\n"
    f = tmp_path / "latin1.txt"
    f.write_bytes(content.encode("latin-1"))
    return str(f)


@pytest.fixture
def utf8_sig_file(tmp_path):
    """Create a file with UTF-8 BOM."""
    content = "[2024/01/15, 10:00:00] Alice: Hello\n"
    f = tmp_path / "bom.txt"
    f.write_bytes(b"\xef\xbb\xbf" + content.encode("utf-8"))
    return str(f)


# --- Happy Path Tests ---


class TestHappyPath:
    """Tests for normal, expected usage."""

    def test_parse_sample_chat_message_count(self, sample_chat_path):
        """Sample chat with 12 lines produces correct message count."""
        messages = parse_chat_file(sample_chat_path)
        # 12 timestamped lines in sample_chat.txt
        assert len(messages) == 12

    def test_parse_sample_chat_first_message_is_system(
        self, sample_chat_path
    ):
        """First message (encryption notice) is system message."""
        messages = parse_chat_file(sample_chat_path)
        assert messages[0].is_system_message is True

    def test_parse_sample_chat_regular_message(self, sample_chat_path):
        """Regular message has correct sender and content."""
        messages = parse_chat_file(sample_chat_path)
        msg = messages[1]
        assert msg.sender == "陳大文"
        assert "換屏幾錢" in msg.content
        assert msg.is_system_message is False

    def test_parse_sample_chat_multiline_message(
        self, sample_chat_path
    ):
        """Multi-line message content includes continuation lines."""
        messages = parse_chat_file(sample_chat_path)
        # Third message (index 2) has 3 lines
        msg = messages[2]
        assert "iPhone 15 換屏 $500" in msg.content
        assert "Pro Max" in msg.content
        assert "保護貼" in msg.content

    def test_parse_sample_chat_attachment(self, sample_chat_path):
        """Attachment message has filename in attachments list."""
        messages = parse_chat_file(sample_chat_path)
        # Message at index 8 has attachment
        msg = messages[8]
        assert "payment_receipt.jpg" in msg.attachments

    def test_parse_sample_chat_timestamps(self, sample_chat_path):
        """All messages have valid datetime timestamps."""
        messages = parse_chat_file(sample_chat_path)
        for msg in messages:
            assert isinstance(msg.timestamp, datetime)

    def test_parse_single_message(self, single_message_file):
        """Single message file produces one ParsedMessage."""
        messages = parse_chat_file(single_message_file)
        assert len(messages) == 1
        assert messages[0].sender == "Alice"
        assert messages[0].content == "Hello World"

    def test_parse_attachment_extraction(self, attachment_file):
        """Attachment filename is correctly extracted."""
        messages = parse_chat_file(attachment_file)
        assert messages[0].attachments == ["photo.jpg"]
        assert messages[1].attachments == []

    def test_raw_text_preserved(self, single_message_file):
        """Raw text field contains original line."""
        messages = parse_chat_file(single_message_file)
        assert "[2024/01/15, 10:00:00]" in messages[0].raw_text

    def test_multiline_raw_text(self, multiline_file):
        """Multi-line message raw_text contains all lines."""
        messages = parse_chat_file(multiline_file)
        raw = messages[0].raw_text
        assert "Line one" in raw
        assert "Line two" in raw
        assert "Line three" in raw


# --- Error Path Tests ---


class TestErrorPath:
    """Tests for error conditions."""

    def test_file_not_found_raises(self):
        """Non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError) as exc_info:
            parse_chat_file("/nonexistent/path/chat.txt")
        assert "not found" in str(exc_info.value)

    def test_file_not_found_message_contains_path(self):
        """Error message includes the file path."""
        path = "/some/missing/file.txt"
        with pytest.raises(FileNotFoundError) as exc_info:
            parse_chat_file(path)
        assert path in str(exc_info.value)

    def test_latin1_encoding_fallback(self, latin1_file):
        """File with latin-1 encoding is read successfully."""
        messages = parse_chat_file(latin1_file)
        assert len(messages) == 1
        assert "caf" in messages[0].content

    def test_utf8_sig_encoding(self, utf8_sig_file):
        """File with UTF-8 BOM is read successfully."""
        messages = parse_chat_file(utf8_sig_file)
        assert len(messages) == 1
        assert messages[0].sender == "Alice"

    def test_unparseable_lines_logged_as_warning(
        self, tmp_path, caplog
    ):
        """Lines that don't match any pattern log a warning."""
        content = (
            "This is not a valid message line\n"
            "[2024/01/15, 10:00:00] Alice: Hello\n"
        )
        f = tmp_path / "bad.txt"
        f.write_text(content, encoding="utf-8")
        with caplog.at_level(logging.WARNING):
            messages = parse_chat_file(str(f))
        assert len(messages) == 1
        assert any("unparseable" in r.message.lower() or
                   "Skipping" in r.message
                   for r in caplog.records)


# --- Edge Case Tests ---


class TestEdgeCases:
    """Tests for boundary and unusual conditions."""

    def test_empty_file_returns_empty_list(self, empty_file, caplog):
        """Empty file returns empty list and logs warning."""
        with caplog.at_level(logging.WARNING):
            messages = parse_chat_file(empty_file)
        assert messages == []
        assert any("empty" in r.message.lower()
                   for r in caplog.records)

    def test_long_message_content(self, tmp_path):
        """Message with >10000 characters is handled correctly."""
        long_text = "A" * 12000
        content = f"[2024/01/15, 10:00:00] Alice: {long_text}\n"
        f = tmp_path / "long.txt"
        f.write_text(content, encoding="utf-8")
        messages = parse_chat_file(str(f))
        assert len(messages) == 1
        assert len(messages[0].content) == 12000

    def test_consecutive_continuation_lines(self, tmp_path):
        """Multiple continuation lines all belong to previous msg."""
        lines = ["[2024/01/15, 10:00:00] Alice: Start\n"]
        for i in range(5):
            lines.append(f"Continuation line {i}\n")
        lines.append("[2024/01/15, 10:01:00] Bob: End\n")
        f = tmp_path / "multi.txt"
        f.write_text("".join(lines), encoding="utf-8")
        messages = parse_chat_file(str(f))
        assert len(messages) == 2
        assert "Continuation line 4" in messages[0].content

    def test_system_message_detection(self, system_message_file):
        """System messages are correctly flagged."""
        messages = parse_chat_file(system_message_file)
        # First is encryption notice (system)
        assert messages[0].is_system_message is True
        # Second is regular
        assert messages[1].is_system_message is False
        # Third is join notice (system)
        assert messages[2].is_system_message is True

    def test_message_with_no_content_after_sender(self, tmp_path):
        """Message with empty content after sender is handled."""
        content = "[2024/01/15, 10:00:00] Alice: \n"
        f = tmp_path / "empty_content.txt"
        f.write_text(content, encoding="utf-8")
        messages = parse_chat_file(str(f))
        assert len(messages) == 1
        assert messages[0].content == ""

    def test_sender_with_special_characters(self, tmp_path):
        """Sender with emoji/special chars is preserved."""
        content = "[2024/01/15, 10:00:00] 🔧維修師傅: Hello\n"
        f = tmp_path / "emoji.txt"
        f.write_text(content, encoding="utf-8")
        messages = parse_chat_file(str(f))
        assert len(messages) == 1
        assert "🔧維修師傅" == messages[0].sender

    def test_twelve_hour_format(self, tmp_path):
        """12-hour time format with AM/PM is parsed."""
        content = "[1/15/24, 2:30 PM] Alice: Afternoon\n"
        f = tmp_path / "12h.txt"
        f.write_text(content, encoding="utf-8")
        messages = parse_chat_file(str(f))
        assert len(messages) == 1
        assert messages[0].timestamp.hour == 14

    def test_only_continuation_lines_no_header(self, tmp_path, caplog):
        """File with only continuation lines returns empty list."""
        content = "Just some text\nAnother line\n"
        f = tmp_path / "noheader.txt"
        f.write_text(content, encoding="utf-8")
        with caplog.at_level(logging.WARNING):
            messages = parse_chat_file(str(f))
        assert messages == []


# --- Internal Function Tests ---


class TestInternalFunctions:
    """Tests for internal helper functions."""

    def test_validate_file_path_exists(self, tmp_path):
        """Valid path returns Path object."""
        f = tmp_path / "test.txt"
        f.write_text("hello", encoding="utf-8")
        result = _validate_file_path(str(f))
        assert isinstance(result, Path)

    def test_validate_file_path_not_exists(self):
        """Invalid path raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            _validate_file_path("/no/such/file.txt")

    def test_detect_encoding_utf8(self, tmp_path):
        """UTF-8 file detected as utf-8."""
        f = tmp_path / "utf8.txt"
        f.write_text("Hello 你好", encoding="utf-8")
        result = _detect_encoding(f)
        assert result == "utf-8"

    def test_extract_attachments_with_file(self):
        """Content with attachment returns filename list."""
        result = _extract_attachments("<attached: doc.pdf>")
        assert result == ["doc.pdf"]

    def test_extract_attachments_without_file(self):
        """Content without attachment returns empty list."""
        result = _extract_attachments("Just a message")
        assert result == []
