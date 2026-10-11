"""Reproducibility contract.

The snapshot tests in this module pin exact output. If one fails, the change
breaks reproducibility for every user: it must not ship in a patch release and
needs a "Reproducibility changes" entry in CHANGELOG.md. Do not just update the
expected values.
"""

from __future__ import annotations

from datetime import date

from testseed import TestSeed
from testseed._random import Stream

# --------------------------------------------------------------- snapshots

EXPECTED_CR_USERS = [
    {
        "id": "TS-USR-TV0JJ5C14J",
        "first_name": "Carolina",
        "last_name": "Porras Herrera",
        "full_name": "Carolina Porras Herrera",
        "email": "carolina.porras25@pruebas.test",
        "username": "carolina.porras25",
        "birth_date": "1972-12-20",
        "created_at": "2020-10-15T16:51:32+00:00",
        "locale": "es_CR",
    },
    {
        "id": "TS-USR-J9HFT1H4WV",
        "first_name": "Jorge",
        "last_name": "Alvarado Cordero",
        "full_name": "Jorge Alvarado Cordero",
        "email": "jorge.alvarado49@ejemplo.test",
        "username": "jorge.alvarado49",
        "birth_date": "1964-08-18",
        "created_at": "2022-08-07T05:01:10+00:00",
        "locale": "es_CR",
    },
    {
        "id": "TS-USR-ZY6KA0EVJZ",
        "first_name": "Fabián",
        "last_name": "Rodríguez Alvarado",
        "full_name": "Fabián Rodríguez Alvarado",
        "email": "fabian.rodriguez37@pruebas.test",
        "username": "fabian.rodriguez37",
        "birth_date": "2002-05-03",
        "created_at": "2023-11-19T06:31:54+00:00",
        "locale": "es_CR",
    },
]


def test_snapshot_es_cr_users() -> None:
    users = TestSeed(locale="es_CR", seed=123).users(count=3)
    assert [u.to_dict() for u in users] == EXPECTED_CR_USERS


def test_snapshot_en_user() -> None:
    assert TestSeed(locale="en", seed=123).user().to_dict() == {
        "id": "TS-USR-RR63XR79EE",
        "first_name": "Harper",
        "last_name": "Davis",
        "full_name": "Harper Davis",
        "email": "harper.davis04@inbox.test",
        "username": "harper.davis04",
        "birth_date": "1952-08-10",
        "created_at": "2024-11-26T18:05:18+00:00",
        "locale": "en",
    }


def test_snapshot_scalar_methods() -> None:
    seed = TestSeed(locale="es_CR", seed=123)
    assert seed.date_between("2024-01-01", "2024-12-31") == date(2024, 3, 8)
    assert seed.fake_id() == "TS-ID-JCSDRAPG8R"
    assert seed.email() == "mauricio.badilla24@ejemplo.test"
    assert seed.first_name() == "Sebastián"
    assert seed.last_name() == "Valverde Mora"
    assert seed.full_name() == "Andrés Ramírez Sánchez"


def test_snapshot_stream_algorithm() -> None:
    stream = Stream.from_seed(123, "x")
    assert [stream.next_u64() for _ in range(5)] == [
        13751569804191075194,
        13402632383112614610,
        10640231059731807848,
        11902962755991409241,
        3486630192701245004,
    ]


# -------------------------------------------------------------- properties


def test_same_seed_same_data() -> None:
    a = TestSeed(locale="es_CR", seed=42)
    b = TestSeed(locale="es_CR", seed=42)
    assert a.users(count=50) == b.users(count=50)
    assert a.date_between("2000-01-01", "2030-12-31") == b.date_between("2000-01-01", "2030-12-31")


def test_different_seed_different_data() -> None:
    a = TestSeed(locale="es_CR", seed=1).users(count=20)
    b = TestSeed(locale="es_CR", seed=2).users(count=20)
    assert a != b


def test_different_locale_independent_data() -> None:
    a = TestSeed(locale="es_CR", seed=1).user()
    b = TestSeed(locale="en", seed=1).user()
    assert a.id != b.id


def test_users_is_prefix_stable() -> None:
    small = TestSeed(seed=7).users(count=10)
    large = TestSeed(seed=7).users(count=100)
    assert large[:10] == small


def test_users_equals_repeated_user_calls() -> None:
    batch = TestSeed(seed=7).users(count=25)
    seed = TestSeed(seed=7)
    assert [seed.user() for _ in range(25)] == batch


def test_methods_use_independent_namespaces() -> None:
    plain = TestSeed(seed=9)
    noisy = TestSeed(seed=9)
    noisy.first_name()
    noisy.date_between("2024-01-01", "2024-12-31")
    noisy.fake_id("ORD")
    assert noisy.user() == plain.user()


def test_reset_replays_sequence() -> None:
    seed = TestSeed(seed=5)
    first = seed.users(count=10)
    seed.reset()
    assert seed.users(count=10) == first


def test_consecutive_calls_advance() -> None:
    seed = TestSeed(seed=5)
    assert seed.user() != seed.user()


def test_random_seed_is_exposed_and_replayable() -> None:
    original = TestSeed(locale="es_CR")
    replay = TestSeed(locale="es_CR", seed=original.seed)
    assert original.users(count=5) == replay.users(count=5)


def test_reference_date_changes_dates_only_where_expected() -> None:
    a = TestSeed(seed=3, reference_date="2025-01-01").user()
    b = TestSeed(seed=3, reference_date="2030-01-01").user()
    assert (a.first_name, a.last_name, a.id) == (b.first_name, b.last_name, b.id)
    assert a.birth_date != b.birth_date
