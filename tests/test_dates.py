from __future__ import annotations

from datetime import UTC, date, datetime, timedelta, timezone

import pytest

from testseed import TestSeed


def test_date_between_inclusive_bounds(cr: TestSeed) -> None:
    values = {cr.date_between("2024-01-01", "2024-01-03") for _ in range(300)}
    assert values == {date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 3)}


def test_date_between_single_day(cr: TestSeed) -> None:
    assert cr.date_between("2024-02-29", "2024-02-29") == date(2024, 2, 29)


def test_date_between_accepts_date_and_datetime(cr: TestSeed) -> None:
    value = cr.date_between(date(2024, 1, 1), datetime(2024, 12, 31, 23, 59))
    assert date(2024, 1, 1) <= value <= date(2024, 12, 31)
    assert type(value) is date


def test_date_between_wide_range(cr: TestSeed) -> None:
    value = cr.date_between("0001-01-01", "9999-12-31")
    assert date(1, 1, 1) <= value <= date(9999, 12, 31)


def test_date_between_reversed(cr: TestSeed) -> None:
    with pytest.raises(ValueError, match="before"):
        cr.date_between("2024-12-31", "2024-01-01")


@pytest.mark.parametrize("bad", ["2024-13-01", "31/12/2024", "", "mañana"])
def test_date_between_bad_string(cr: TestSeed, bad: str) -> None:
    with pytest.raises(ValueError, match="ISO"):
        cr.date_between(bad, "2024-12-31")


def test_date_between_bad_type(cr: TestSeed) -> None:
    with pytest.raises(TypeError, match="end"):
        cr.date_between("2024-01-01", 20241231)  # type: ignore[arg-type]


def test_datetime_between_is_aware_utc(cr: TestSeed) -> None:
    value = cr.datetime_between("2024-01-01T00:00:00", "2024-01-02T00:00:00")
    assert value.tzinfo is UTC
    assert datetime(2024, 1, 1, tzinfo=UTC) <= value <= datetime(2024, 1, 2, tzinfo=UTC)


def test_datetime_between_converts_offsets(cr: TestSeed) -> None:
    cst = timezone(timedelta(hours=-6))
    start = datetime(2024, 1, 1, 0, 0, tzinfo=cst)
    value = cr.datetime_between(start, start)
    assert value == datetime(2024, 1, 1, 6, 0, tzinfo=UTC)


def test_datetime_between_accepts_dates(cr: TestSeed) -> None:
    value = cr.datetime_between(date(2024, 1, 1), date(2024, 1, 1))
    assert value == datetime(2024, 1, 1, tzinfo=UTC)


def test_datetime_between_errors(cr: TestSeed) -> None:
    with pytest.raises(ValueError, match="before"):
        cr.datetime_between("2024-01-02", "2024-01-01")
    with pytest.raises(ValueError, match="ISO"):
        cr.datetime_between("not-a-date", "2024-01-01")
    with pytest.raises(TypeError, match="start"):
        cr.datetime_between(1.0, "2024-01-01")  # type: ignore[arg-type]


def test_reference_date_validation() -> None:
    assert TestSeed(reference_date="2030-06-15").reference_date == date(2030, 6, 15)
    with pytest.raises(ValueError, match="reference_date"):
        TestSeed(reference_date="15-06-2030")
