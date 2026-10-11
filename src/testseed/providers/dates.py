"""Date and datetime providers."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

from testseed._random import Stream

DateLike = date | str
DateTimeLike = datetime | date | str


def parse_date(value: DateLike, *, name: str = "value") -> date:
    """Convert an ISO string (``"2024-01-31"``), ``date`` or ``datetime`` to ``date``."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            raise ValueError(f"{name} must be an ISO date (YYYY-MM-DD), got {value!r}") from None
    raise TypeError(f"{name} must be a date or an ISO date string, got {type(value).__name__}")


def parse_datetime(value: DateTimeLike, *, name: str = "value") -> datetime:
    """Convert a value to an aware UTC ``datetime``.

    Naive datetimes and plain dates are interpreted as UTC.
    """
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            raise ValueError(f"{name} must be an ISO datetime, got {value!r}") from None
    if isinstance(value, datetime):
        return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day, tzinfo=UTC)
    raise TypeError(f"{name} must be a datetime, date or ISO string, got {type(value).__name__}")


def subtract_years(day: date, years: int) -> date:
    """Return ``day`` moved back ``years`` years; 29 Feb becomes 28 Feb when needed."""
    try:
        return day.replace(year=day.year - years)
    except ValueError:
        return day.replace(year=day.year - years, day=28)


def date_between(stream: Stream, start: date, end: date) -> date:
    """Return a date in ``[start, end]`` (both inclusive)."""
    if start > end:
        raise ValueError(f"start ({start}) must be on or before end ({end})")
    return start + timedelta(days=stream.randbelow((end - start).days + 1))


def datetime_between(stream: Stream, start: datetime, end: datetime) -> datetime:
    """Return an aware UTC datetime in ``[start, end]`` with second precision."""
    if start > end:
        raise ValueError(f"start ({start}) must be on or before end ({end})")
    span = int((end - start).total_seconds())
    return start + timedelta(seconds=stream.randbelow(span + 1))
