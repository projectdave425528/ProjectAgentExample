"""Tests for parser module (patterns + text_parser)."""
from datetime import datetime
from pathlib import Path
import logging
import pytest

from src.parser.patterns import match_message_line, is_system_message, extract_attachment
from src.parser.utils import parse_timestamp
from src.parser.text_parser import parse_chat_file


class TestPatterns:
    def test_standard_24h(self):
        result = match_message_line("[2024/01/15, 14:30:00] John: Hello")
        assert result == ("2024/01/15, 14:30:00", "John", "Hello")

    def test_12h_format(self):
        result = match_message_line("[1/15/24, 2:30 PM] John: Hi")
        assert result is not None
        assert result[1] == "John"

    def test_sender_with_colon(self):
        result = match_message_line("[2024/01/15, 14:30:00] Dr. Wong: 醫生: 你好")
        assert result[1] == "Dr. Wong"
        assert result[2] == "醫生: 你好"

    def test_continuation_line_returns_none(self):
        assert match_message_line("This is continuation") is None

    def test_empty_returns_none(self):
        assert match_message_line("") is None


class TestSystemMessage:
    def test_joined_group(self):
        assert is_system_message("陳大文 加入了群組") is True

    def test_normal_message(self):
        assert is_system_message("你好嗎") is False

    def test_empty(self):
        assert is_system_message("") is False


class TestAttachment:
    def test_extract(self):
        assert extract_attachment("<attached: photo.jpg>") == "photo.jpg"

    def test_no_attachment(self):
        assert extract_attachment("normal text") is None


class TestParseTimestamp:
    def test_24h(self):
        assert parse_timestamp("2024/01/15, 14:30:00") == datetime(2024, 1, 15, 14, 30, 0)

    def test_12h_pm(self):
        assert parse_timestamp("1/15/24, 2:30 PM") == datetime(2024, 1, 15, 14, 30, 0)

    def test_invalid_returns_none(self):
        assert parse_timestamp("not a timestamp") is None

    def test_feb_31_invalid(self):
        assert parse_timestamp("2024/02/31, 14:30:00") is None


class TestTextParser:
    def test_parse_sample_chat(self):
        fixture = Path(__file__).parent / "fixtures" / "sample_chat.txt"
        messages = parse_chat_file(str(fixture))
        assert len(messages) == 12

    def test_first_is_system(self):
        fixture = Path(__file__).parent / "fixtures" / "sample_chat.txt"
        messages = parse_chat_file(str(fixture))
        assert messages[0].is_system_message is True
        assert "encrypted" in messages[0].content

    def test_multiline_message(self):
        fixture = Path(__file__).parent / "fixtures" / "sample_chat.txt"
        messages = parse_chat_file(str(fixture))
        # Find the message with "Pro Max" (multi-line from 維修師傅)
        found = any("Pro Max" in m.content for m in messages)
        assert found

    def test_attachment_extracted(self):
        fixture = Path(__file__).parent / "fixtures" / "sample_chat.txt"
        messages = parse_chat_file(str(fixture))
        # Find message with attachment
        attach_msgs = [m for m in messages if m.attachments]
        assert len(attach_msgs) >= 1
        assert "payment_receipt.jpg" in attach_msgs[0].attachments

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            parse_chat_file("/nonexistent/file.txt")

    def test_empty_file(self, tmp_path, caplog):
        f = tmp_path / "empty.txt"
        f.write_text("", encoding="utf-8")
        with caplog.at_level(logging.WARNING):
            result = parse_chat_file(str(f))
        assert result == []
