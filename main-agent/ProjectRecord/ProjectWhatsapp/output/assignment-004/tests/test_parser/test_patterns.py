"""Unit tests for WhatsApp parser patterns and utilities.

Covers:
- MESSAGE_PATTERN matching (24h, 12h, various date formats)
- ATTACHMENT_PATTERN extraction
- System message detection
- Sender/content splitting (including colons in sender names)
- Timestamp parsing (multiple formats, edge cases)
- Error paths (empty input, invalid formats)
"""

import pytest
from datetime import datetime

from src.parser.patterns import (
    MESSAGE_PATTERN,
    ATTACHMENT_PATTERN,
    SYSTEM_MESSAGE_KEYWORDS,
    is_system_message,
    extract_attachment,
    match_message_line,
    split_sender_content,
)
from src.parser.utils import (
    parse_timestamp,
    normalize_date_string,
    _parse_time,
    _convert_12h_to_24h,
    _normalize_year,
    _is_valid_date_range,
    _split_date_time,
)


# ============================================================
# MESSAGE_PATTERN Tests
# ============================================================

class TestMessagePattern:
    """Tests for the main MESSAGE_PATTERN regex."""

    # --- Happy Path ---

    def test_standard_24h_format(self):
        """Standard format: [YYYY/MM/DD, HH:MM:SS] Sender: Message"""
        line = "[2024/01/15, 14:30:00] John: Hello"
        match = MESSAGE_PATTERN.match(line)
        assert match is not None
        assert match.group(1) == "2024/01/15, 14:30:00"
        assert match.group(2) == "John: Hello"

    def test_12h_format_pm(self):
        """12-hour format with PM."""
        line = "[1/15/24, 2:30 PM] John: Hi there"
        match = MESSAGE_PATTERN.match(line)
        assert match is not None
        assert match.group(1) == "1/15/24, 2:30 PM"

    def test_12h_format_am(self):
        """12-hour format with AM."""
        line = "[1/15/24, 9:05 AM] Alice: Good morning"
        match = MESSAGE_PATTERN.match(line)
        assert match is not None
        assert match.group(1) == "1/15/24, 9:05 AM"

    def test_dd_mm_yyyy_format(self):
        """DD/MM/YYYY date order."""
        line = "[15/01/2024, 14:30:00] John: Hello"
        match = MESSAGE_PATTERN.match(line)
        assert match is not None
        assert match.group(1) == "15/01/2024, 14:30:00"

    def test_dash_separator(self):
        """Date with dash separator."""
        line = "[2024-01-15, 14:30:00] John: Hello"
        match = MESSAGE_PATTERN.match(line)
        assert match is not None
        assert match.group(1) == "2024-01-15, 14:30:00"

    def test_dot_separator(self):
        """Date with dot separator."""
        line = "[2024.01.15, 14:30:00] John: Hello"
        match = MESSAGE_PATTERN.match(line)
        assert match is not None
        assert match.group(1) == "2024.01.15, 14:30:00"

    def test_time_without_seconds(self):
        """Time without seconds component."""
        line = "[2024/01/15, 14:30] John: Hello"
        match = MESSAGE_PATTERN.match(line)
        assert match is not None
        assert match.group(1) == "2024/01/15, 14:30"

    def test_chinese_sender(self):
        """Chinese characters in sender name."""
        line = "[2024/01/15, 14:30:00] 陳大文: 你好"
        match = MESSAGE_PATTERN.match(line)
        assert match is not None
        assert match.group(2) == "陳大文: 你好"

    def test_12h_with_seconds(self):
        """12-hour format with seconds."""
        line = "[1/15/24, 2:30:45 PM] John: Hi"
        match = MESSAGE_PATTERN.match(line)
        assert match is not None

    def test_lowercase_ampm(self):
        """Lowercase am/pm."""
        line = "[1/15/24, 2:30 pm] John: Hi"
        match = MESSAGE_PATTERN.match(line)
        assert match is not None

    # --- Error Path ---

    def test_no_brackets(self):
        """Line without brackets should not match."""
        line = "2024/01/15, 14:30:00 John: Hello"
        match = MESSAGE_PATTERN.match(line)
        assert match is None

    def test_empty_string(self):
        """Empty string should not match."""
        match = MESSAGE_PATTERN.match("")
        assert match is None

    def test_plain_text(self):
        """Plain text without timestamp should not match."""
        line = "This is just a continuation line"
        match = MESSAGE_PATTERN.match(line)
        assert match is None

    def test_incomplete_timestamp(self):
        """Incomplete timestamp should not match."""
        line = "[2024/01, 14:30:00] John: Hello"
        match = MESSAGE_PATTERN.match(line)
        assert match is None

    # --- Edge Case ---

    def test_sender_with_colon_in_name(self):
        """Sender name containing colon (e.g. Dr. Wong: 醫生)."""
        line = "[2024/01/15, 14:30:00] Dr. Wong: 醫生: 你好"
        match = MESSAGE_PATTERN.match(line)
        assert match is not None
        assert match.group(2) == "Dr. Wong: 醫生: 你好"

    def test_single_digit_date_parts(self):
        """Single digit month and day."""
        line = "[1/5/24, 2:30 PM] John: Hi"
        match = MESSAGE_PATTERN.match(line)
        assert match is not None


# ============================================================
# split_sender_content Tests
# ============================================================

class TestSplitSenderContent:
    """Tests for sender/content splitting logic."""

    def test_simple_split(self):
        """Simple sender: content split."""
        result = split_sender_content("John: Hello")
        assert result == ("John", "Hello")

    def test_sender_with_colon(self):
        """Sender with colon in name - first ': ' is delimiter."""
        result = split_sender_content("Dr. Wong: 醫生: 你好")
        assert result == ("Dr. Wong", "醫生: 你好")

    def test_chinese_sender(self):
        """Chinese sender name."""
        result = split_sender_content("陳大文: 你好嗎")
        assert result == ("陳大文", "你好嗎")

    def test_empty_content(self):
        """Empty content after delimiter."""
        result = split_sender_content("John: ")
        assert result == ("John", "")

    def test_no_delimiter(self):
        """No ': ' delimiter returns None."""
        result = split_sender_content("System message without colon")
        assert result is None

    def test_empty_string(self):
        """Empty string returns None."""
        result = split_sender_content("")
        assert result is None

    def test_none_input(self):
        """None input returns None."""
        result = split_sender_content(None)
        assert result is None

    def test_colon_without_space(self):
        """Colon without space is not a delimiter."""
        result = split_sender_content("http://example.com: content")
        assert result == ("http://example.com", "content")

    def test_multiple_colons(self):
        """Multiple ': ' - only first one is used."""
        result = split_sender_content("A: B: C: D")
        assert result == ("A", "B: C: D")


# ============================================================
# ATTACHMENT_PATTERN Tests
# ============================================================

class TestAttachmentPattern:
    """Tests for attachment filename extraction."""

    def test_standard_attachment(self):
        """Standard attachment format."""
        content = "<attached: IMG-20240115-WA0001.jpg>"
        match = ATTACHMENT_PATTERN.search(content)
        assert match is not None
        assert match.group(1).strip() == "IMG-20240115-WA0001.jpg"

    def test_attachment_no_space(self):
        """Attachment without space after colon."""
        content = "<attached:document.pdf>"
        match = ATTACHMENT_PATTERN.search(content)
        assert match is not None
        assert match.group(1).strip() == "document.pdf"

    def test_attachment_in_message(self):
        """Attachment embedded in message text."""
        content = "Here is the file <attached: report.xlsx> please check"
        match = ATTACHMENT_PATTERN.search(content)
        assert match is not None
        assert match.group(1).strip() == "report.xlsx"

    def test_no_attachment(self):
        """No attachment in content."""
        content = "Just a normal message"
        match = ATTACHMENT_PATTERN.search(content)
        assert match is None

    def test_empty_string(self):
        """Empty string has no attachment."""
        match = ATTACHMENT_PATTERN.search("")
        assert match is None


# ============================================================
# extract_attachment Tests
# ============================================================

class TestExtractAttachment:
    """Tests for extract_attachment function."""

    def test_extract_jpg(self):
        """Extract JPG filename."""
        result = extract_attachment("<attached: photo.jpg>")
        assert result == "photo.jpg"

    def test_extract_with_path(self):
        """Extract filename with complex name."""
        result = extract_attachment("<attached: IMG-20240115-WA0001.jpg>")
        assert result == "IMG-20240115-WA0001.jpg"

    def test_no_attachment_returns_none(self):
        """No attachment returns None."""
        result = extract_attachment("Hello world")
        assert result is None

    def test_empty_returns_none(self):
        """Empty string returns None."""
        result = extract_attachment("")
        assert result is None

    def test_none_returns_none(self):
        """None input returns None."""
        result = extract_attachment(None)
        assert result is None

    def test_webp_format(self):
        """WEBP format attachment."""
        result = extract_attachment("<attached: sticker.webp>")
        assert result == "sticker.webp"


# ============================================================
# is_system_message Tests
# ============================================================

class TestIsSystemMessage:
    """Tests for system message detection."""

    def test_joined_group_chinese(self):
        """Chinese 'joined group' message."""
        assert is_system_message("陳大文 加入了群組") is True

    def test_left_group_chinese(self):
        """Chinese 'left group' message."""
        assert is_system_message("陳大文 已離開") is True

    def test_changed_name_chinese(self):
        """Chinese 'changed group name' message."""
        assert is_system_message("陳大文 更改了群組名稱") is True

    def test_removed_chinese(self):
        """Chinese 'removed' message."""
        assert is_system_message("你已被移除") is True

    def test_deleted_message_chinese(self):
        """Chinese 'deleted message'."""
        assert is_system_message("訊息已刪除") is True

    def test_english_left(self):
        """English 'left' keyword."""
        assert is_system_message("John left") is True

    def test_encryption_notice(self):
        """End-to-end encryption notice."""
        msg = "Messages and calls are end-to-end encrypted"
        assert is_system_message(msg) is True

    def test_normal_message(self):
        """Normal message is not system message."""
        assert is_system_message("你好嗎？今日天氣好好") is False

    def test_empty_string(self):
        """Empty string is not system message."""
        assert is_system_message("") is False

    def test_none_input(self):
        """None input is not system message."""
        assert is_system_message(None) is False

    def test_partial_keyword_not_match(self):
        """Partial keyword that doesn't contain full keyword."""
        assert is_system_message("我加入了") is False


# ============================================================
# match_message_line Tests
# ============================================================

class TestMatchMessageLine:
    """Tests for the match_message_line function."""

    def test_standard_message(self):
        """Standard message line returns correct tuple."""
        result = match_message_line(
            "[2024/01/15, 14:30:00] John: Hello"
        )
        assert result is not None
        timestamp_str, sender, content = result
        assert timestamp_str == "2024/01/15, 14:30:00"
        assert sender == "John"
        assert content == "Hello"

    def test_chinese_message(self):
        """Chinese sender and content."""
        result = match_message_line(
            "[2024/01/15, 14:30:05] 陳大文: 你好"
        )
        assert result is not None
        _, sender, content = result
        assert sender == "陳大文"
        assert content == "你好"

    def test_sender_with_colon(self):
        """Sender with colon in name."""
        result = match_message_line(
            "[2024/01/15, 14:30:00] Dr. Wong: 醫生: 你好"
        )
        assert result is not None
        _, sender, content = result
        assert sender == "Dr. Wong"
        assert content == "醫生: 你好"

    def test_12h_format(self):
        """12-hour format message."""
        result = match_message_line(
            "[1/15/24, 2:30 PM] John: Hi there"
        )
        assert result is not None
        timestamp_str, sender, content = result
        assert timestamp_str == "1/15/24, 2:30 PM"
        assert sender == "John"
        assert content == "Hi there"

    def test_continuation_line(self):
        """Continuation line (no timestamp) returns None."""
        result = match_message_line("This is a continuation")
        assert result is None

    def test_empty_string(self):
        """Empty string returns None."""
        result = match_message_line("")
        assert result is None

    def test_none_input(self):
        """None input returns None."""
        result = match_message_line(None)
        assert result is None

    def test_system_message_no_colon_space(self):
        """System message without ': ' delimiter returns None."""
        line = "[2024/01/15, 14:30:00] 陳大文 加入了群組"
        result = match_message_line(line)
        # This line has no ': ' so split_sender_content returns None
        assert result is None

    def test_whitespace_line(self):
        """Whitespace-only line returns None."""
        result = match_message_line("   ")
        assert result is None


# ============================================================
# parse_timestamp Tests
# ============================================================

class TestParseTimestamp:
    """Tests for timestamp parsing utility."""

    # --- Happy Path ---

    def test_standard_24h(self):
        """Standard 24-hour timestamp."""
        result = parse_timestamp("2024/01/15, 14:30:00")
        assert result == datetime(2024, 1, 15, 14, 30, 0)

    def test_24h_without_seconds(self):
        """24-hour without seconds."""
        result = parse_timestamp("2024/01/15, 14:30")
        assert result == datetime(2024, 1, 15, 14, 30, 0)

    def test_12h_pm(self):
        """12-hour PM format."""
        result = parse_timestamp("1/15/24, 2:30 PM")
        assert result == datetime(2024, 1, 15, 14, 30, 0)

    def test_12h_am(self):
        """12-hour AM format."""
        result = parse_timestamp("1/15/24, 9:05 AM")
        assert result == datetime(2024, 1, 15, 9, 5, 0)

    def test_12h_noon(self):
        """12 PM = noon (12:00)."""
        result = parse_timestamp("1/15/24, 12:00 PM")
        assert result == datetime(2024, 1, 15, 12, 0, 0)

    def test_12h_midnight(self):
        """12 AM = midnight (00:00)."""
        result = parse_timestamp("1/15/24, 12:00 AM")
        assert result == datetime(2024, 1, 15, 0, 0, 0)

    def test_dd_mm_yyyy(self):
        """DD/MM/YYYY format."""
        result = parse_timestamp("15/01/2024, 14:30:00")
        assert result == datetime(2024, 1, 15, 14, 30, 0)

    def test_dash_separator(self):
        """Dash date separator."""
        result = parse_timestamp("2024-01-15, 14:30:00")
        assert result == datetime(2024, 1, 15, 14, 30, 0)

    def test_dot_separator(self):
        """Dot date separator."""
        result = parse_timestamp("2024.01.15, 14:30:00")
        assert result == datetime(2024, 1, 15, 14, 30, 0)

    def test_2digit_year(self):
        """2-digit year normalized to 2000s."""
        result = parse_timestamp("1/15/24, 2:30 PM")
        assert result is not None
        assert result.year == 2024

    # --- Error Path ---

    def test_empty_string(self):
        """Empty string returns None."""
        assert parse_timestamp("") is None

    def test_none_input(self):
        """None input returns None."""
        assert parse_timestamp(None) is None

    def test_no_comma(self):
        """No comma separator returns None."""
        assert parse_timestamp("2024/01/15 14:30:00") is None

    def test_invalid_time(self):
        """Invalid time (25:00) returns None."""
        assert parse_timestamp("2024/01/15, 25:00:00") is None

    def test_completely_invalid(self):
        """Completely invalid string returns None."""
        assert parse_timestamp("not a timestamp") is None

    # --- Edge Case ---

    def test_invalid_date_feb_31(self):
        """Feb 31 is invalid - returns None."""
        result = parse_timestamp("2024/02/31, 14:30:00")
        assert result is None

    def test_leap_year_feb_29(self):
        """Feb 29 on leap year is valid."""
        result = parse_timestamp("2024/02/29, 14:30:00")
        assert result == datetime(2024, 2, 29, 14, 30, 0)

    def test_non_leap_year_feb_29(self):
        """Feb 29 on non-leap year is invalid."""
        result = parse_timestamp("2023/02/29, 14:30:00")
        assert result is None

    def test_midnight_24h(self):
        """Midnight in 24-hour format."""
        result = parse_timestamp("2024/01/15, 00:00:00")
        assert result == datetime(2024, 1, 15, 0, 0, 0)

    def test_end_of_day(self):
        """23:59:59 is valid."""
        result = parse_timestamp("2024/01/15, 23:59:59")
        assert result == datetime(2024, 1, 15, 23, 59, 59)

    def test_whitespace_around(self):
        """Whitespace around timestamp is handled."""
        result = parse_timestamp("  2024/01/15, 14:30:00  ")
        assert result == datetime(2024, 1, 15, 14, 30, 0)


# ============================================================
# normalize_date_string Tests
# ============================================================

class TestNormalizeDateString:
    """Tests for date string normalization."""

    def test_yyyy_mm_dd(self):
        """YYYY/MM/DD normalizes correctly."""
        assert normalize_date_string("2024/01/15") == "2024-01-15"

    def test_dd_mm_yyyy(self):
        """DD/MM/YYYY normalizes correctly."""
        assert normalize_date_string("15/01/2024") == "2024-01-15"

    def test_dash_separator(self):
        """Dash separator normalizes correctly."""
        assert normalize_date_string("2024-01-15") == "2024-01-15"

    def test_dot_separator(self):
        """Dot separator normalizes correctly."""
        assert normalize_date_string("2024.01.15") == "2024-01-15"

    def test_2digit_year(self):
        """2-digit year normalizes to 2000s."""
        result = normalize_date_string("1/15/24")
        assert result is not None
        assert "2024" in result

    def test_empty_string(self):
        """Empty string returns None."""
        assert normalize_date_string("") is None

    def test_none_input(self):
        """None input returns None."""
        assert normalize_date_string(None) is None

    def test_invalid_format(self):
        """Invalid format returns None."""
        assert normalize_date_string("not-a-date") is None

    def test_too_few_parts(self):
        """Too few date parts returns None."""
        assert normalize_date_string("2024/01") is None


# ============================================================
# Internal helper tests
# ============================================================

class TestInternalHelpers:
    """Tests for internal utility functions."""

    def test_convert_12h_to_24h_pm(self):
        """PM conversion."""
        assert _convert_12h_to_24h(2, "PM") == 14

    def test_convert_12h_to_24h_am(self):
        """AM stays same (except 12)."""
        assert _convert_12h_to_24h(9, "AM") == 9

    def test_convert_12h_to_24h_12pm(self):
        """12 PM = 12."""
        assert _convert_12h_to_24h(12, "PM") == 12

    def test_convert_12h_to_24h_12am(self):
        """12 AM = 0."""
        assert _convert_12h_to_24h(12, "AM") == 0

    def test_convert_12h_invalid_hour(self):
        """Hour > 12 returns None."""
        assert _convert_12h_to_24h(13, "PM") is None

    def test_convert_12h_zero_hour(self):
        """Hour 0 is invalid for 12h format."""
        assert _convert_12h_to_24h(0, "AM") is None

    def test_normalize_year_2digit(self):
        """2-digit year adds 2000."""
        assert _normalize_year(24) == 2024

    def test_normalize_year_4digit(self):
        """4-digit year unchanged."""
        assert _normalize_year(2024) == 2024

    def test_is_valid_date_range_valid(self):
        """Valid date range."""
        assert _is_valid_date_range(2024, 1, 15) is True

    def test_is_valid_date_range_month_0(self):
        """Month 0 is invalid."""
        assert _is_valid_date_range(2024, 0, 15) is False

    def test_is_valid_date_range_month_13(self):
        """Month 13 is invalid."""
        assert _is_valid_date_range(2024, 13, 15) is False

    def test_is_valid_date_range_day_0(self):
        """Day 0 is invalid."""
        assert _is_valid_date_range(2024, 1, 0) is False

    def test_is_valid_date_range_day_32(self):
        """Day 32 is invalid."""
        assert _is_valid_date_range(2024, 1, 32) is False

    def test_split_date_time_valid(self):
        """Valid timestamp splits correctly."""
        date_str, time_str = _split_date_time("2024/01/15, 14:30:00")
        assert date_str == "2024/01/15"
        assert time_str == "14:30:00"

    def test_split_date_time_no_comma(self):
        """No comma returns (None, None)."""
        assert _split_date_time("no comma here") == (None, None)

    def test_parse_time_24h(self):
        """Parse 24h time."""
        result = _parse_time("14:30:00")
        assert result == (14, 30, 0)

    def test_parse_time_12h(self):
        """Parse 12h time."""
        result = _parse_time("2:30 PM")
        assert result == (14, 30, 0)

    def test_parse_time_empty(self):
        """Empty time returns None."""
        assert _parse_time("") is None

    def test_parse_time_none(self):
        """None time returns None."""
        assert _parse_time(None) is None
