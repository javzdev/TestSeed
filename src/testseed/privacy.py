"""Safety rules that keep generated data clearly fictitious.

Email domains are restricted to names reserved by the IETF so that generated
addresses can never be delivered to a real mailbox:

* RFC 2606 / RFC 6761 top-level domains: ``.test``, ``.example``, ``.invalid``,
  ``.localhost``.
* RFC 2606 second-level domains: ``example.com``, ``example.net``, ``example.org``.
"""

from __future__ import annotations

import re
from typing import Final

from testseed.errors import UnsafeEmailDomainError

RESERVED_TLDS: Final = ("test", "example", "invalid", "localhost")
RESERVED_DOMAINS: Final = ("example.com", "example.net", "example.org")

#: Prefix of every identifier produced by :meth:`TestSeed.fake_id`.
FAKE_ID_PREFIX: Final = "TS"

_LABEL = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")


def is_reserved_email_domain(domain: str) -> bool:
    """Return ``True`` if ``domain`` is syntactically valid and reserved for testing."""
    normalized = domain.strip().lower()
    labels = normalized.split(".")
    if len(labels) < 2 or not all(_LABEL.match(label) for label in labels):
        return False
    if normalized in RESERVED_DOMAINS or any(
        normalized.endswith("." + reserved) for reserved in RESERVED_DOMAINS
    ):
        return True
    return labels[-1] in RESERVED_TLDS


def validate_email_domain(domain: str) -> str:
    """Return the normalized domain or raise :class:`UnsafeEmailDomainError`."""
    if not isinstance(domain, str):
        raise TypeError(f"email domain must be a str, got {type(domain).__name__}")
    if not is_reserved_email_domain(domain):
        allowed = ", ".join([*(f"*.{tld}" for tld in RESERVED_TLDS), *RESERVED_DOMAINS])
        raise UnsafeEmailDomainError(
            f"{domain!r} is not a domain reserved for testing. Use one of: {allowed}"
        )
    return domain.strip().lower()
