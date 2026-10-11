"""Privacy and safety guarantees."""

from __future__ import annotations

import re
import socket

import pytest

from testseed import TestSeed, UnsafeEmailDomainError, available_locales
from testseed.privacy import is_reserved_email_domain

#: Costa Rican cédula de identidad (e.g. 1-2345-6789 or 123456789).
CEDULA_CR = re.compile(r"\b\d-?\d{4}-?\d{4}\b")
#: Anything that could pass as a payment card number.
CARD_LIKE = re.compile(r"\d(?:[ -]?\d){12,18}")


@pytest.fixture(params=available_locales())
def any_locale(request: pytest.FixtureRequest) -> TestSeed:
    return TestSeed(locale=request.param, seed=2024)


def test_emails_use_reserved_domains(any_locale: TestSeed) -> None:
    for user in any_locale.users(count=1000):
        assert user.email.rsplit(".", 1)[-1] == "test"
    assert any_locale.email().endswith(".test")


def test_ids_are_clearly_fictitious(any_locale: TestSeed) -> None:
    for user in any_locale.users(count=500):
        assert re.fullmatch(r"TS-USR-[0-9A-HJKMNP-TV-Z]{10}", user.id)


def test_no_real_identifier_patterns(any_locale: TestSeed) -> None:
    for user in any_locale.users(count=1000):
        for key, value in user.to_dict().items():
            if key in {"birth_date", "created_at"}:
                continue
            assert not CEDULA_CR.search(value), (key, value)
            assert not CARD_LIKE.search(value), (key, value)


@pytest.mark.parametrize(
    "domain",
    ["acme.test", "QA.Example", "sub.example.com", "example.org", "x.invalid", "dev.localhost"],
)
def test_reserved_domains_accepted(domain: str) -> None:
    assert is_reserved_email_domain(domain)
    TestSeed(email_domains=[domain])


@pytest.mark.parametrize(
    "domain",
    ["gmail.com", "empresa.cr", "test", "test.com", "example.com.evil.net", "a..test", "-a.test"],
)
def test_real_domains_rejected(domain: str) -> None:
    assert not is_reserved_email_domain(domain)
    with pytest.raises(UnsafeEmailDomainError):
        TestSeed(email_domains=[domain])


def test_email_domains_argument_validation() -> None:
    with pytest.raises(TypeError, match="single str"):
        TestSeed(email_domains="acme.test")
    with pytest.raises(ValueError, match="at least one"):
        TestSeed(email_domains=[])
    with pytest.raises(TypeError):
        TestSeed(email_domains=[123])  # type: ignore[list-item]


def test_generation_needs_no_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def blocked(*args: object, **kwargs: object) -> None:
        raise AssertionError("TestSeed must not open network connections")

    monkeypatch.setattr(socket, "socket", blocked)
    monkeypatch.setattr(socket, "create_connection", blocked)
    seed = TestSeed(locale="es_CR", seed=1)
    seed.users(count=100)
    seed.email()
    seed.date_between("2024-01-01", "2024-12-31")


def test_seed_type_validation() -> None:
    with pytest.raises(TypeError, match="seed"):
        TestSeed(seed="123")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="seed"):
        TestSeed(seed=True)
