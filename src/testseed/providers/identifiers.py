"""Clearly fictitious identifiers.

Identifiers look like ``TS-USR-7K3M9QX2AB``: the ``TS-`` prefix and the mix of
letters and digits make them impossible to confuse with national ID numbers,
tax IDs, passport numbers or payment cards.
"""

from __future__ import annotations

import re
from typing import Final

from testseed._random import Stream
from testseed.privacy import FAKE_ID_PREFIX

#: Crockford's Base32 alphabet (no I, L, O, U) avoids ambiguous characters.
ALPHABET: Final = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
BODY_LENGTH: Final = 10

_PREFIX = re.compile(r"^[A-Z][A-Z0-9]{0,9}$")


def validate_prefix(prefix: str) -> str:
    """Return ``prefix`` if it is 1-10 uppercase ASCII letters/digits, starting with a letter."""
    if not isinstance(prefix, str):
        raise TypeError(f"prefix must be a str, got {type(prefix).__name__}")
    if not _PREFIX.match(prefix):
        raise ValueError(
            f"prefix must be 1-10 uppercase letters or digits starting with a letter, "
            f"got {prefix!r}"
        )
    return prefix


def fake_id(stream: Stream, prefix: str) -> str:
    """Return an identifier such as ``"TS-USR-7K3M9QX2AB"``."""
    body = "".join(stream.choice(ALPHABET) for _ in range(BODY_LENGTH))
    return f"{FAKE_ID_PREFIX}-{prefix}-{body}"
