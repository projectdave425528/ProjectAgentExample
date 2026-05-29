"""Utility functions for WhatsApp timestamp parsing."""
import re
from datetime import datetime
from typing import Optional

_DATE_SPLIT = re.compile(r"[/\-.]")
_AMPM_PATTERN = re.compile(r"(\d{1,2}:\d{2}(?::\d{2})?)\s*([AaPp][Mm])")
_DATE_FORMATS = [(0, 1, 2), (2, 1, 0), (2, 0, 1)]


def parse_timestamp(timestamp_str: str) -> Optional[datetime]:
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
    comma_idx = timestamp_str.find(",")
    if comma_idx == -1:
        return (None, None)
    return (timestamp_str[:comma_idx].strip(), timestamp_str[comma_idx + 1:].strip())


def _parse_time(time_str: str) -> Optional[tuple]:
    if not time_str:
        return None
    ampm_match = _AMPM_PATTERN.search(time_str)
    if ampm_match:
        return _parse_12h_time(ampm_match)
    return _parse_24h_time(time_str)


def _parse_12h_time(ampm_match: re.Match) -> Optional[tuple]:
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
    if hour < 1 or hour > 12:
        return None
    if period == "AM":
        return 0 if hour == 12 else hour
    return hour if hour == 12 else hour + 12


def _parse_24h_time(time_str: str) -> Optional[tuple]:
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
    parts = _DATE_SPLIT.split(date_str)
    if len(parts) != 3:
        return None
    for year_idx, month_idx, day_idx in _DATE_FORMATS:
        result = _try_date_format(parts, year_idx, month_idx, day_idx, hour, minute, second)
        if result is not None:
            return result
    return None


def _try_date_format(parts, year_idx, month_idx, day_idx, hour, minute, second) -> Optional[datetime]:
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
    return year + 2000 if year < 100 else year


def _is_valid_date_range(year: int, month: int, day: int) -> bool:
    return 1 <= month <= 12 and 1 <= day <= 31 and 1900 <= year <= 2100


def normalize_date_string(date_str: str) -> Optional[str]:
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
    if not rest:
        return None
    delimiter_idx = rest.find(": ")
    if delimiter_idx == -1:
        return None
    return (rest[:delimiter_idx], rest[delimiter_idx + 2:])
