"""Data models returned by TestSeed."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class User:
    """A synthetic user. Every field is fictitious.

    Instances are immutable; use :func:`dataclasses.replace` to derive variants.
    """

    id: str
    first_name: str
    last_name: str
    email: str
    username: str
    birth_date: date
    created_at: datetime
    locale: str

    @property
    def full_name(self) -> str:
        """First name followed by surname(s)."""
        return f"{self.first_name} {self.last_name}"

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict (dates as ISO 8601 strings).

        Key order is part of the public contract.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "email": self.email,
            "username": self.username,
            "birth_date": self.birth_date.isoformat(),
            "created_at": self.created_at.isoformat(),
            "locale": self.locale,
        }
