from __future__ import annotations

import dataclasses
from datetime import UTC, date, datetime, timedelta

import pytest

from testseed import MAX_BATCH_SIZE, TestSeed, User
from testseed.providers.dates import subtract_years


def _age(birth: date, on: date) -> int:
    return on.year - birth.year - ((on.month, on.day) < (birth.month, birth.day))


def test_user_has_expected_types(cr: TestSeed) -> None:
    user = cr.user()
    assert isinstance(user, User)
    assert isinstance(user.birth_date, date)
    assert isinstance(user.created_at, datetime)
    assert user.created_at.tzinfo is UTC
    assert user.locale == "es_CR"
    assert user.full_name == f"{user.first_name} {user.last_name}"
    assert user.email.split("@")[0] == user.username


def test_user_is_immutable(cr: TestSeed) -> None:
    user = cr.user()
    with pytest.raises(dataclasses.FrozenInstanceError):
        user.first_name = "Otro"  # type: ignore[misc]


def test_es_cr_users_have_two_surnames(cr: TestSeed) -> None:
    for user in cr.users(count=200):
        first, second = user.last_name.split(" ")
        assert first != second


def test_en_users_have_one_surname(en: TestSeed) -> None:
    assert all(" " not in u.last_name for u in en.users(count=200))


def test_default_ages_are_adults(cr: TestSeed) -> None:
    for user in cr.users(count=500):
        assert 18 <= _age(user.birth_date, cr.reference_date) <= 80


@pytest.mark.parametrize(("min_age", "max_age"), [(0, 0), (18, 18), (30, 45), (0, 120)])
def test_custom_age_range(min_age: int, max_age: int) -> None:
    seed = TestSeed(seed=11)
    for user in seed.users(count=300, min_age=min_age, max_age=max_age):
        assert min_age <= _age(user.birth_date, seed.reference_date) <= max_age


def test_created_at_window(cr: TestSeed) -> None:
    ref = cr.reference_date
    lower = datetime(ref.year - 5, ref.month, ref.day, tzinfo=UTC)
    upper = datetime(ref.year, ref.month, ref.day, tzinfo=UTC) + timedelta(days=1)
    for user in cr.users(count=300, min_age=0, max_age=3):
        assert lower <= user.created_at < upper
        assert user.created_at.date() >= user.birth_date


def test_leap_day_reference_date() -> None:
    seed = TestSeed(seed=1, reference_date=date(2024, 2, 29))
    assert subtract_years(date(2024, 2, 29), 1) == date(2023, 2, 28)
    assert len(seed.users(count=50)) == 50


def test_users_count(cr: TestSeed) -> None:
    assert len(cr.users(count=100)) == 100
    assert cr.users(count=0) == []


def test_users_count_positional(cr: TestSeed) -> None:
    assert len(cr.users(3)) == 3


def test_emails_and_ids_unique_within_instance() -> None:
    users = TestSeed(locale="es_CR", seed=99).users(count=20_000)
    assert len({u.email for u in users}) == len(users)
    assert len({u.id for u in users}) == len(users)


def test_custom_email_domains() -> None:
    seed = TestSeed(seed=1, email_domains=["acme.test"])
    assert all(u.email.endswith("@acme.test") for u in seed.users(count=50))


@pytest.mark.parametrize("count", [-1, MAX_BATCH_SIZE + 1])
def test_users_count_out_of_range(cr: TestSeed, count: int) -> None:
    with pytest.raises(ValueError, match="count"):
        cr.users(count=count)


@pytest.mark.parametrize("count", [1.5, "10", True, None])
def test_users_count_wrong_type(cr: TestSeed, count: object) -> None:
    with pytest.raises(TypeError, match="count"):
        cr.users(count=count)  # type: ignore[arg-type]


@pytest.mark.parametrize(("min_age", "max_age"), [(-1, 10), (30, 20), (0, 121)])
def test_invalid_age_range(cr: TestSeed, min_age: int, max_age: int) -> None:
    with pytest.raises(ValueError, match="min_age"):
        cr.user(min_age=min_age, max_age=max_age)


def test_invalid_age_type(cr: TestSeed) -> None:
    with pytest.raises(TypeError, match="max_age"):
        cr.users(count=1, max_age="80")  # type: ignore[arg-type]


def test_names(cr: TestSeed) -> None:
    assert cr.first_name()
    assert len(cr.last_name().split()) == 2
    assert len(cr.full_name().split()) >= 3


def test_email_with_given_names(cr: TestSeed) -> None:
    address = cr.email(first_name="María José", last_name="Zúñiga Mora")
    assert address.startswith("mariajose.zuniga")
    assert address.endswith(".test")


def test_email_with_non_latin_name_falls_back(en: TestSeed) -> None:
    assert en.email(first_name="李", last_name="王").startswith("user")


def test_email_unique_when_names_repeat(cr: TestSeed) -> None:
    emails = [cr.email(first_name="Ana", last_name="Mora") for _ in range(400)]
    assert len(set(emails)) == len(emails)


def test_fake_id(cr: TestSeed) -> None:
    assert cr.fake_id().startswith("TS-ID-")
    assert cr.fake_id("ORD").startswith("TS-ORD-")
    assert len({cr.fake_id("X") for _ in range(1000)}) == 1000


@pytest.mark.parametrize("prefix", ["", "usr", "1AB", "TOOLONGPREFIX", "A-B"])
def test_fake_id_invalid_prefix(cr: TestSeed, prefix: str) -> None:
    with pytest.raises(ValueError, match="prefix"):
        cr.fake_id(prefix)


def test_fake_id_prefix_type(cr: TestSeed) -> None:
    with pytest.raises(TypeError):
        cr.fake_id(1)  # type: ignore[arg-type]
