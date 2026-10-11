"""Locale data model."""

from __future__ import annotations

from dataclasses import dataclass

from testseed.privacy import validate_email_domain


@dataclass(frozen=True, slots=True)
class LocaleData:
    """Static data used to generate values for one locale.

    Locales contain only data (no logic) so that new ones can be contributed
    without touching the generators.
    """

    code: str
    name: str
    first_names: tuple[str, ...]
    last_names: tuple[str, ...]
    #: How many surnames a full name carries (Costa Rica uses two).
    surnames_per_person: int
    email_domains: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.first_names or not self.last_names or not self.email_domains:
            raise ValueError(f"locale {self.code!r} has an empty data table")
        if self.surnames_per_person not in (1, 2):
            raise ValueError("surnames_per_person must be 1 or 2")
        if self.surnames_per_person > len(set(self.last_names)):
            raise ValueError("not enough distinct last names")
        for domain in self.email_domains:
            validate_email_domain(domain)
