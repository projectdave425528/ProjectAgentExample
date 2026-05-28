"""Utility functions for WhatsApp timestamp parsing.

Handles multiple date/time formats:
- 24-hour: 14:30:00, 14:30
- 12-hour: 2:30 PM, 2:30:00 PM
- Date orders: YYYY/MM/DD, DD/MM/YYYY, MM/DD/YYYY
- Date separators: / - .
- 2-digit and 4-digit years
"""

import re
from datetime import datetime
from typing import Optional

# Pattern to split date string into components
_DATE_SPLIT = re.compile(r"[/\-.]")

# Pattern to detect AM/PM
_AMPM_PATTERN = re.compile(r"(\d{1,2}:\d{2}(?::\d{2})?)\s*([AaPp][Mm])")

# Known date format orders to try
_DATE_FORMATS = [
    # (year_index, month_index, day_index)
    (0, 1, 2),  # YYYY/MM/DD
    (2, 1, 0),  # DD/MM/YYYY
    (2, 0, 1),  # MM/DD/YYYY
]


def parse_timestamp(timestamp_str: str) -> Optional[datetime]:
    """Parse a WhatsApp timestamp string into a datetime object.

    Supports multiple formats including 12/24 hour time,
    various date orders, and different separators.

    Args:
        timestamp_str: Raw timestamp string from the chat export.

    Returns:
        datetime object if parsing succeeds, None otherwise.
    """
    if not timestamp_str:
        return None
    timestamp_str = timestamp_str.strip()
    date_str, time_str = _split_date_time(timestamp_str)
    if date_str is None or time_str is None:
        return None
    time_parts = _parse_time(time_str)
    if time_parts is None:
        return None
    hour, minute, second = time_parts
    return _resolve_date(date_str, hour, minute, second)


def _split_date_time(timestamp_str: str) -> tuple:
    """Split timestamp into date and time portions.

    Args:
        timestamp_str: e.g. '2024/01/15, 14:30:00'

    Returns:
        Tuple of (date_str, time_str) or (None, None).
    """
    comma_idx = timestamp_str.find(",")
    if comma_idx == -1:
        return (None, None)
    date_str = timestamp_str[:comma_idx].strip()
    time_str = timestamp_str[comma_idx + 1:].strip()
    return (date_str, time_str)


def _parse_time(time_str: str) -> Optional[tuple]:
    """Parse time string into (hour, minute, second).

    Handles both 12-hour (with AM/PM) and 24-hour formats.

    Args:
        time_str: e.g. '14:30:00' or '2:30 PM'

    Returns:
        Tuple of (hour, minute, second) or None.
    """
    if not time_str:
        return None
    ampm_match = _AMPM_PATTERN.search(time_str)
    if ampm_match:
        return _parse_12h_time(ampm_match)
    return _parse_24h_time(time_str)


def _parse_12h_time(ampm_match: re.Match) -> Optional[tuple]:
    """Parse 12-hour time from regex match.

    Args:
        ampm_match: Regex match with time and AM/PM groups.

    Returns:
        Tuple of (hour, minute, second) or None.
    """
    time_part = ampm_match.group(1)
    period = ampm_match.group(2).upper()
    parts = time_part.split(":")
    try:
        hour = int(parts[0])
        minute = int(parts[1])
        second = int(parts[2]) if len(parts) > 2 else 0
    except (ValueError, IndexError):
        return None
    hour = _convert_12h_to_24h(hour, period)
    if hour is None:
        return None
    return (hour, minute, second)


def _convert_12h_to_24h(hour: int, period: str) -> Optional[int]:
    """Convert 12-hour format to 24-hour.

    Args:
        hour: Hour value (1-12).
        period: 'AM' or 'PM'.

    Returns:
        24-hour format hour (0-23) or None if invalid.
    """
    if hour < 1 or hour > 12:
        return None
    if period == "AM":
        return 0 if hour == 12 else hour
    return hour if hour == 12 else hour + 12


def _parse_24h_time(time_str: str) -> Optional[tuple]:
    """Parse 24-hour time string.

    Args:
        time_str: e.g. '14:30:00' or '14:30'

    Returns:
        Tuple of (hour, minute, second) or None.
    """
    parts = time_str.strip().split(":")
    try:
        hour = int(parts[0])
        minute = int(parts[1])
        second = int(parts[2]) if len(parts) > 2 else 0
    except (ValueError, IndexError):
        return None
    if hour > 23 or minute > 59 or second > 59:
        return None
    return (hour, minute, second)


def _resolve_date(date_str: str, hour: int, minute: int, second: int) -> Optional[datetime]:
    """Try multiple date format orders to resolve a date string.

    Args:
        date_str: Date portion, e.g. '2024/01/15'.
        hour: Parsed hour (0-23).
        minute: Parsed minute (0-59).
        second: Parsed second (0-59).

    Returns:
        datetime object if any format succeeds, None otherwise.
    """
    parts = _DATE_SPLIT.split(date_str)
    if len(parts) != 3:
        return None
    for year_idx, month_idx, day_idx in _DATE_FORMATS:
        result = _try_date_format(
            parts, year_idx, month_idx, day_idx,
            hour, minute, second
        )
        if result is not None:
            return result
    return None


def _try_date_format(
    parts: list, year_idx: int, month_idx: int, day_idx: int,
    hour: int, minute: int, second: int
) -> Optional[datetime]:
    """Attempt to construct a datetime with a specific date order.

    Args:
        parts: List of 3 date component strings.
        year_idx: Index of year in parts.
        month_idx: Index of month in parts.
        day_idx: Index of day in parts.
        hour: Hour value.
        minute: Minute value.
        second: Second value.

    Returns:
        datetime if valid, None otherwise.
    """
    try:
        year = int(parts[year_idx])
        month = int(parts[month_idx])
        day = int(parts[day_idx])
    except ValueError:
        return None
    year = _normalize_year(year)
    if not _is_valid_date_range(year, month, day):
        return None
    try:
        return datetime(year, month, day, hour, minute, second)
    except ValueError:
        return None


def _normalize_year(year: int) -> int:
    """Normalize 2-digit year to 4-digit.

    Args:
        year: Year value (2 or 4 digits).

    Returns:
        4-digit year value.
    """
    if year < 100:
        return year + 2000
    return year


def _is_valid_date_range(year: int, month: int, day: int) -> bool:
    """Quick check if date components are in valid ranges.

    Args:
        year: 4-digit year.
        month: Month (1-12).
        day: Day (1-31).

    Returns:
        True if ranges are plausible.
    """
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False
    if year < 1900 or year > 2100:
        return False
    return True


def normalize_date_string(date_str: str) -> Optional[str]:
    """Normalize a date string to YYYY-MM-DD format.

    Args:
        date_str: Raw date string with any separator.

    Returns:
        Normalized date string or None if invalid.
    """
    if not date_str:
        return None
    parts = _DATE_SPLIT.split(date_str.strip())
    if len(parts) != 3:
        return None
    for year_idx, month_idx, day_idx in _DATE_FORMATS:
        try:
            year = int(parts[year_idx])
            month = int(parts[month_idx])
            day = int(parts[day_idx])
            year = _normalize_year(year)
            if _is_valid_date_range(year, month, day):
                datetime(year, month, day)
                return f"{year:04d}-{month:02d}-{day:02d}"
        except ValueError:
            continue
    return None


def split_sender_content(rest: str) -> Optional[tuple]:
    """Split the rest part into sender and content.

    Uses the first ': ' as delimiter so senders with colons
    in their names are handled correctly.

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
