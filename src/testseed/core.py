"""The :class:`TestSeed` entry point."""

from __future__ import annotations

import secrets
from collections.abc import Iterable
from datetime import date, datetime, timedelta
from typing import Final

from testseed._random import Stream
from testseed.locales import DEFAULT_LOCALE, get_locale
from testseed.models import User
from testseed.privacy import validate_email_domain
from testseed.providers import dates, identifiers, internet, person
from testseed.providers.dates import DateLike, DateTimeLike

#: Fixed "today" used for ages and account dates, so output never depends on the
#: day the tests run. Override it with ``reference_date=``.
DEFAULT_REFERENCE_DATE: Final = date(2025, 1, 1)

#: Upper bound for ``users(count=...)``; protects against accidental huge allocations.
MAX_BATCH_SIZE: Final = 1_000_000

#: How far back ``User.created_at`` can go from the reference date.
ACCOUNT_HISTORY_YEARS: Final = 5

MIN_AGE_LIMIT: Final = 0
MAX_AGE_LIMIT: Final = 120

_EMAIL_ATTEMPTS: Final = 10


class TestSeed:
    """Reproducible generator of synthetic test data.

    >>> seed = TestSeed(locale="es_CR", seed=123)
    >>> seed.user().email.endswith(".test")
    True

    Reproducibility contract: the same TestSeed version, constructor arguments
    and sequence of calls always return the same values. Each method draws from
    its own namespace, so calling ``first_name()`` never changes what ``user()``
    returns next.

    Instances are not thread-safe; create one per thread.
    """

    __test__ = False  # Keep pytest from collecting this class.

    def __init__(
        self,
        locale: str = DEFAULT_LOCALE,
        seed: int | None = None,
        *,
        reference_date: DateLike | None = None,
        email_domains: Iterable[str] | None = None,
    ) -> None:
        """Create a generator.

        Args:
            locale: Locale code such as ``"es_CR"`` or ``"en"``.
            seed: Integer seed. When omitted a random one is chosen; read it back
                from :attr:`seed` to reproduce the run.
            reference_date: The "today" used to compute ages and account dates.
                Defaults to :data:`DEFAULT_REFERENCE_DATE`.
            email_domains: Domains for generated emails. Each must be reserved
                for testing (``*.test``, ``*.example``, ``example.com``...).
        """
        self._locale = get_locale(locale)
        if seed is None:
            seed = secrets.randbits(63)
        elif isinstance(seed, bool) or not isinstance(seed, int):
            raise TypeError(f"seed must be an int or None, got {type(seed).__name__}")
        self._seed = seed
        self._reference_date = (
            DEFAULT_REFERENCE_DATE
            if reference_date is None
            else dates.parse_date(reference_date, name="reference_date")
        )
        if email_domains is None:
            self._email_domains = self._locale.email_domains
        else:
            if isinstance(email_domains, str):
                raise TypeError("email_domains must be an iterable of str, not a single str")
            self._email_domains = tuple(validate_email_domain(d) for d in email_domains)
            if not self._email_domains:
                raise ValueError("email_domains must contain at least one domain")
        self._counters: dict[str, int] = {}
        self._issued_emails: set[str] = set()
        self._issued_ids: set[str] = set()

    def __repr__(self) -> str:
        return f"TestSeed(locale={self.locale!r}, seed={self.seed!r})"

    # ------------------------------------------------------------------ config

    @property
    def seed(self) -> int:
        """The seed in use (also when it was chosen randomly)."""
        return self._seed

    @property
    def locale(self) -> str:
        """The normalized locale code."""
        return self._locale.code

    @property
    def reference_date(self) -> date:
        """The fixed "today" used for ages and account dates."""
        return self._reference_date

    @property
    def email_domains(self) -> tuple[str, ...]:
        """The domains used for generated emails."""
        return self._email_domains

    def reset(self) -> None:
        """Rewind the generator: following calls repeat the values from the start."""
        self._counters.clear()
        self._issued_emails.clear()
        self._issued_ids.clear()

    # ---------------------------------------------------------------- internals

    def _next_index(self, namespace: str) -> int:
        index = self._counters.get(namespace, 0)
        self._counters[namespace] = index + 1
        return index

    def _stream(self, *path: str | int) -> Stream:
        # The locale is part of the key so each locale yields an independent dataset.
        return Stream.from_seed(self._seed, self._locale.code, *path)

    def _unique_id(self, prefix: str, *path: str | int) -> str:
        attempt = 0
        while True:
            value = identifiers.fake_id(self._stream(*path, attempt), prefix)
            if value not in self._issued_ids:
                self._issued_ids.add(value)
                return value
            attempt += 1

    def _unique_email(self, first: str, last: str, *path: str | int) -> tuple[str, str]:
        """Return ``(username, email)``, unique within this instance."""
        for attempt in range(_EMAIL_ATTEMPTS):
            stream = self._stream(*path, attempt)
            user = internet.username(stream, first, last)
            address = internet.email(stream, user, self._email_domains)
            if address not in self._issued_emails:
                self._issued_emails.add(address)
                return user, address
        # Deterministic fallback once random attempts are exhausted.
        stream = self._stream(*path, "fallback")
        base = internet.username(stream, first, last)
        domain = stream.choice(self._email_domains)
        counter = 1
        while True:
            user = f"{base}.{counter}"
            address = f"{user}@{domain}"
            if address not in self._issued_emails:
                self._issued_emails.add(address)
                return user, address
            counter += 1

    # ------------------------------------------------------------------ people

    def first_name(self) -> str:
        """Return a first name for the locale."""
        index = self._next_index("first_name")
        return person.first_name(self._stream("first_name", index), self._locale)

    def last_name(self) -> str:
        """Return the surname(s) for the locale (two for ``es_CR``)."""
        index = self._next_index("last_name")
        return person.last_name(self._stream("last_name", index), self._locale)

    def full_name(self) -> str:
        """Return ``"<first name> <surname(s)>"``."""
        index = self._next_index("full_name")
        first = person.first_name(self._stream("full_name", index, "first"), self._locale)
        last = person.last_name(self._stream("full_name", index, "last"), self._locale)
        return f"{first} {last}"

    def email(self, first_name: str | None = None, last_name: str | None = None) -> str:
        """Return an email on a domain reserved for testing, unique within this instance.

        Names are generated when not given; accents are removed (``Zúñiga`` -> ``zuniga``).
        """
        index = self._next_index("email")
        first = first_name or person.first_name(self._stream("email", index, "first"), self._locale)
        last = last_name or person.last_name(self._stream("email", index, "last"), self._locale)
        return self._unique_email(first, last, "email", index, "address")[1]

    def fake_id(self, prefix: str = "ID") -> str:
        """Return a clearly fictitious identifier such as ``"TS-ID-7K3M9QX2AB"``.

        Identifiers are unique within this instance.
        """
        identifiers.validate_prefix(prefix)
        namespace = f"fake_id:{prefix}"
        return self._unique_id(prefix, namespace, self._next_index(namespace))

    # ------------------------------------------------------------------- dates

    def date_between(self, start: DateLike, end: DateLike) -> date:
        """Return a date in ``[start, end]``; accepts ``date`` or ``"YYYY-MM-DD"``."""
        start_date = dates.parse_date(start, name="start")
        end_date = dates.parse_date(end, name="end")
        index = self._next_index("date_between")
        return dates.date_between(self._stream("date_between", index), start_date, end_date)

    def datetime_between(self, start: DateTimeLike, end: DateTimeLike) -> datetime:
        """Return an aware UTC datetime in ``[start, end]`` with second precision.

        Naive inputs and plain dates are interpreted as UTC.
        """
        start_dt = dates.parse_datetime(start, name="start")
        end_dt = dates.parse_datetime(end, name="end")
        index = self._next_index("datetime_between")
        return dates.datetime_between(self._stream("datetime_between", index), start_dt, end_dt)

    # ------------------------------------------------------------------- users

    def user(self, *, min_age: int = 18, max_age: int = 80) -> User:
        """Return one synthetic :class:`User` aged ``min_age``-``max_age`` at the reference date."""
        _validate_age_range(min_age, max_age)
        return self._build_user(self._next_index("user"), min_age, max_age)

    def users(self, count: int, *, min_age: int = 18, max_age: int = 80) -> list[User]:
        """Return ``count`` users.

        ``users(n)`` returns the same users as ``n`` consecutive ``user()`` calls,
        so ``users(10)`` is a prefix of ``users(100)`` for the same seed.
        """
        if isinstance(count, bool) or not isinstance(count, int):
            raise TypeError(f"count must be an int, got {type(count).__name__}")
        if not 0 <= count <= MAX_BATCH_SIZE:
            raise ValueError(f"count must be between 0 and {MAX_BATCH_SIZE}, got {count}")
        _validate_age_range(min_age, max_age)
        return [self._build_user(self._next_index("user"), min_age, max_age) for _ in range(count)]

    def _build_user(self, index: int, min_age: int, max_age: int) -> User:
        ref = self._reference_date
        first = person.first_name(self._stream("user", index, "first_name"), self._locale)
        last = person.last_name(self._stream("user", index, "last_name"), self._locale)
        username, email = self._unique_email(first, last, "user", index, "email")

        # Born so that the age at ``ref`` is within [min_age, max_age].
        latest_birth = dates.subtract_years(ref, min_age)
        earliest_birth = dates.subtract_years(ref, max_age + 1) + timedelta(days=1)
        birth_date = dates.date_between(
            self._stream("user", index, "birth_date"), earliest_birth, latest_birth
        )

        # Account created on or after the birth date, up to the end of the reference day.
        history_start = dates.parse_datetime(
            max(dates.subtract_years(ref, ACCOUNT_HISTORY_YEARS), birth_date)
        )
        created_at = dates.datetime_between(
            self._stream("user", index, "created_at"),
            history_start,
            dates.parse_datetime(ref) + timedelta(days=1, seconds=-1),
        )

        return User(
            id=self._unique_id("USR", "user", index, "id"),
            first_name=first,
            last_name=last,
            email=email,
            username=username,
            birth_date=birth_date,
            created_at=created_at,
            locale=self._locale.code,
        )


def _validate_age_range(min_age: int, max_age: int) -> None:
    for name, value in (("min_age", min_age), ("max_age", max_age)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if not MIN_AGE_LIMIT <= min_age <= max_age <= MAX_AGE_LIMIT:
        raise ValueError(
            f"ages must satisfy {MIN_AGE_LIMIT} <= min_age <= max_age <= {MAX_AGE_LIMIT}, "
            f"got min_age={min_age}, max_age={max_age}"
        )
