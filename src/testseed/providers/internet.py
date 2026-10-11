"""Username and email providers."""

from __future__ import annotations

import re
import unicodedata

from testseed._random import Stream

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Return an ASCII, lowercase, alphanumeric-only version of ``text``.

    ``"Zúñiga"`` becomes ``"zuniga"``; characters without an ASCII equivalent
    are dropped.
    """
    decomposed = unicodedata.normalize("NFKD", text)
    ascii_only = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return _NON_ALNUM.sub("", ascii_only.lower())


def username(stream: Stream, first_name: str, last_name: str) -> str:
    """Return a username such as ``"maria.mora42"``.

    Only the first surname is used, which matches how people usually build
    addresses in locales with two surnames.
    """
    first = slugify(first_name) or "user"
    surname_parts = last_name.split()
    last = slugify(surname_parts[0]) if surname_parts else ""
    base = f"{first}.{last}" if last else first
    return f"{base}{stream.randbelow(100):02d}"


def email(stream: Stream, user: str, domains: tuple[str, ...]) -> str:
    """Return ``user@domain`` with a domain chosen from ``domains``."""
    return f"{user}@{stream.choice(domains)}"
