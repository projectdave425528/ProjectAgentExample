"""Unit tests for text_parser module."""

import logging
from pathlib import Path
from unittest.mock import patch, mock_open

import pytest

from src.parser.text_parser import (
    parse_chat_file,
    _create_pending,
    _append_continuation,
    _extract_attachments,
)


# --- Fixtures ---

@pytest.fixture
def sample_chat_path():
    """Path to the sample chat fixture file."""
    return str(
        Path(__file__).parent.parent / "fixtures" / "sample_chat.txt"
    )


@pytest.fixture
def empty_file(tmp_path):
    """Create an empty file for testing."""
    f = tmp_path / "empty.txt"
    f.write_text("")
    return str(f)


@pytest.fixture
def standard_chat(tmp_path):
    """Create a standard 10-message chat file."""
    content = "\n".join([
        "[2024/01/15, 14:30:00] Alice: Message 1",
        "[2024/01/15, 14:30:01] Bob: Message 2",
        "[2024/01/15, 14:30:02] Alice: Message 3",
        "[2024/01/15, 14:30:03] Bob: Message 4",
        "[2024/01/15, 14:30:04] Alice: Message 5",
        "[2024/01/15, 14:30:05] Bob: Message 6",
        "[2024/01/15, 14:30:06] Alice: Message 7",
        "[2024/01/15, 14:30:07] Bob: Message 8",
        "[2024/01/15, 14:30:08] Alice: Message 9",
        "[2024/01/15, 14:30:09] Bob: Message 10",
    ])
    f = tmp_path / "standard.txt"
    f.write_text(content, encoding="utf-8")
    return str(f)


@pytest.fixture
def multiline_chat(tmp_path):
    """Create a chat with multi-line messages."""
    content = "\n".join([
        "[2024/01/15, 14:30:00] Alice: First line",
        "Second line",
        "Third line",
        "[2024/01/15, 14:31:00] Bob: Reply",
    ])
    f = tmp_path / "multiline.txt"
    f.write_text(content, encoding="utf-8")
    return str(f)


@pytest.fixture
def system_msg_chat(tmp_path):
    """Create a chat with system messages."""
    content = "\n".join([
        "[2024/01/15, 14:30:00] System: John 加入了群組",
        "[2024/01/15, 14:31:00] Alice: Hello!",
        "[2024/01/15, 14:32:00] System: Messages and calls are end-to-end encrypted",
    ])
    f = tmp_path / "system.txt"
    f.write_text(content, encoding="utf-8")
    return str(f)


@pytest.fixture
def attachment_chat(tmp_path):
    """Create a chat with attachment messages."""
    content = "\n".join([
        "[2024/01/15, 14:30:00] Alice: Check this out",
        "[2024/01/15, 14:31:00] Alice: <attached: photo.jpg>",
        "[2024/01/15, 14:32:00] Bob: Nice!",
        "[2024/01/15, 14:33:00] Bob: <attached: document.pdf>",
    ])
    f = tmp_path / "attachment.txt"
    f.write_text(content, encoding="utf-8")
    return str(f)


# --- Happy Path Tests ---

class TestParseHappyPath:
    """Tests for normal/expected usage."""

    def test_parse_standard_10_messages(self, standard_chat):
        """10 standard messages should produce 10 ParsedMessage."""
        result = parse_chat_file(standard_chat)
        assert len(result) == 10

    def test_parse_message_fields_correct(self, standard_chat):
        """First message should have correct fields."""
        result = parse_chat_file(standard_chat)
        msg = result[0]
        assert msg.sender == "Alice"
        assert msg.content == "Message 1"
        assert msg.is_system_message is False
        assert msg.attachments == []
        assert msg.timestamp.year == 2024
        assert msg.timestamp.month == 1
        assert msg.timestamp.day == 15

    def test_parse_attachment_messages(self, attachment_chat):
        """Attachment messages should populate attachments list."""
        result = parse_chat_file(attachment_chat)
        assert result[1].attachments == ["photo.jpg"]
        assert result[3].attachments == ["document.pdf"]

    def test_parse_sample_chat_fixture(self, sample_chat_path):
        """Sample chat fixture should parse without errors."""
        result = parse_chat_file(sample_chat_path)
        assert len(result) > 0

    def test_parse_12h_format(self, tmp_path):
        """12-hour time format should parse correctly."""
        content = "[1/15/24, 2:30 PM] Alice: Hello"
        f = tmp_path / "12h.txt"
        f.write_text(content, encoding="utf-8")
        result = parse_chat_file(str(f))
        assert len(result) == 1
        assert result[0].timestamp.hour == 14
        assert result[0].timestamp.minute == 30

    def test_parse_sender_with_colon(self, tmp_path):
        """Sender with colon should be handled correctly."""
        content = "[2024/01/15, 14:30:00] Dr. Wong: 醫生話冇問題"
        f = tmp_path / "colon.txt"
        f.write_text(content, encoding="utf-8")
        result = parse_chat_file(str(f))
        assert len(result) == 1
        assert result[0].sender == "Dr. Wong"
        assert result[0].content == "醫生話冇問題"


# --- Multi-line Message Tests ---

class TestMultilineMessages:
    """Tests for multi-line message handling."""

    def test_multiline_content_joined(self, multiline_chat):
        """Continuation lines should be appended to previous message."""
        result = parse_chat_file(multiline_chat)
        assert len(result) == 2
        assert "First line\nSecond line\nThird line" == result[0].content

    def test_multiline_raw_text_preserved(self, multiline_chat):
        """Raw text should include all original lines."""
        result = parse_chat_file(multiline_chat)
        assert "Second line" in result[0].raw_text
        assert "Third line" in result[0].raw_text

    def test_consecutive_continuation_lines(self, tmp_path):
        """Multiple continuation lines all belong to same message."""
        content = "\n".join([
            "[2024/01/15, 14:30:00] Alice: Line 1",
            "Line 2",
            "Line 3",
            "Line 4",
            "Line 5",
        ])
        f = tmp_path / "multi.txt"
        f.write_text(content, encoding="utf-8")
        result = parse_chat_file(str(f))
        assert len(result) == 1
        assert result[0].content.count("\n") == 4


# --- System Message Tests ---

class TestSystemMessages:
    """Tests for system message detection."""

    def test_system_message_flagged(self, system_msg_chat):
        """System messages should have is_system_message=True."""
        result = parse_chat_file(system_msg_chat)
        assert result[0].is_system_message is True
        assert result[2].is_system_message is True

    def test_normal_message_not_flagged(self, system_msg_chat):
        """Normal messages should have is_system_message=False."""
        result = parse_chat_file(system_msg_chat)
        assert result[1].is_system_message is False


# --- Error Path Tests ---

class TestErrorPaths:
    """Tests for error handling."""

    def test_file_not_found_raises(self):
        """Non-existent file should raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError) as exc_info:
            parse_chat_file("/nonexistent/path/chat.txt")
        assert "搵唔到文件" in str(exc_info.value)

    def test_file_not_found_message_contains_path(self):
        """Error message should contain the file path."""
        path = "/some/missing/file.txt"
        with pytest.raises(FileNotFoundError) as exc_info:
            parse_chat_file(path)
        assert path in str(exc_info.value)

    def test_empty_file_returns_empty_list(self, empty_file, caplog):
        """Empty file should return empty list with warning."""
        with caplog.at_level(logging.WARNING):
            result = parse_chat_file(empty_file)
        assert result == []
        assert "文件為空" in caplog.text


# --- Edge Case Tests ---

class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_very_long_message(self, tmp_path):
        """Message with >10000 characters should parse correctly."""
        long_content = "A" * 10001
        content = f"[2024/01/15, 14:30:00] Alice: {long_content}"
        f = tmp_path / "long.txt"
        f.write_text(content, encoding="utf-8")
        result = parse_chat_file(str(f))
        assert len(result) == 1
        assert len(result[0].content) == 10001

    def test_unparseable_first_line_skipped(self, tmp_path, caplog):
        """Lines before first valid message should be skipped."""
        content = "\n".join([
            "This is not a valid message line",
            "[2024/01/15, 14:30:00] Alice: Hello",
        ])
        f = tmp_path / "skip.txt"
        f.write_text(content, encoding="utf-8")
        with caplog.at_level(logging.WARNING):
            result = parse_chat_file(str(f))
        assert len(result) == 1
        assert "無法解析" in caplog.text

    def test_single_message_file(self, tmp_path):
        """File with only one message should work."""
        content = "[2024/01/15, 14:30:00] Alice: Solo message"
        f = tmp_path / "single.txt"
        f.write_text(content, encoding="utf-8")
        result = parse_chat_file(str(f))
        assert len(result) == 1

    def test_chinese_content(self, tmp_path):
        """Chinese content should be preserved correctly."""
        content = "[2024/01/15, 14:30:00] 陳大文: 今日天氣好好"
        f = tmp_path / "chinese.txt"
        f.write_text(content, encoding="utf-8")
        result = parse_chat_file(str(f))
        assert result[0].sender == "陳大文"
        assert result[0].content == "今日天氣好好"

    def test_emoji_in_content(self, tmp_path):
        """Emoji in content should be preserved."""
        content = "[2024/01/15, 14:30:00] Alice: Hello 😊🎉"
        f = tmp_path / "emoji.txt"
        f.write_text(content, encoding="utf-8")
        result = parse_chat_file(str(f))
        assert "😊🎉" in result[0].content

    def test_dash_date_separator(self, tmp_path):
        """Dash date separator should parse correctly."""
        content = "[15-01-2024, 14:30:00] Alice: Dash format"
        f = tmp_path / "dash.txt"
        f.write_text(content, encoding="utf-8")
        result = parse_chat_file(str(f))
        assert len(result) == 1
        assert result[0].timestamp.day == 15

    def test_dot_date_separator(self, tmp_path):
        """Dot date separator should parse correctly."""
        content = "[2024.01.15, 14:30:00] Alice: Dot format"
        f = tmp_path / "dot.txt"
        f.write_text(content, encoding="utf-8")
        result = parse_chat_file(str(f))
        assert len(result) == 1


# --- Internal Function Tests ---

class TestInternalFunctions:
    """Tests for internal helper functions."""

    def test_create_pending(self):
        """_create_pending should build correct dict."""
        matched = ("2024/01/15, 14:30:00", "Alice", "Hello")
        raw = "[2024/01/15, 14:30:00] Alice: Hello"
        result = _create_pending(matched, raw)
        assert result["timestamp_str"] == "2024/01/15, 14:30:00"
        assert result["sender"] == "Alice"
        assert result["content"] == "Hello"
        assert result["raw_lines"] == [raw]

    def test_append_continuation_with_pending(self):
        """Continuation should append to pending content."""
        pending = {
            "content": "Line 1",
            "raw_lines": ["[...] Alice: Line 1"],
        }
        result = _append_continuation(pending, "Line 2", [])
        assert result["content"] == "Line 1\nLine 2"

    def test_append_continuation_no_pending(self, caplog):
        """No pending message should log warning."""
        with caplog.at_level(logging.WARNING):
            result = _append_continuation(None, "orphan line", [])
        assert result is None
        assert "無法解析" in caplog.text

    def test_extract_attachments_found(self):
        """Should extract attachment filename."""
        result = _extract_attachments("<attached: photo.jpg>")
        assert result == ["photo.jpg"]

    def test_extract_attachments_not_found(self):
        """No attachment should return empty list."""
        result = _extract_attachments("Hello world")
        assert result == []
