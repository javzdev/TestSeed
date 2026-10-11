"""TestSeed: realistic, safe and reproducible synthetic data for software testing.

>>> from testseed import TestSeed
>>> seed = TestSeed(locale="es_CR", seed=123)
>>> len(seed.users(count=3))
3
"""

from __future__ import annotations

from testseed.core import DEFAULT_REFERENCE_DATE, MAX_BATCH_SIZE, TestSeed
from testseed.errors import TestSeedError, UnsafeEmailDomainError, UnsupportedLocaleError
from testseed.locales import DEFAULT_LOCALE, available_locales
from testseed.models import User

__version__ = "0.1.0"

__all__ = [
    "DEFAULT_LOCALE",
    "DEFAULT_REFERENCE_DATE",
    "MAX_BATCH_SIZE",
    "TestSeed",
    "TestSeedError",
    "UnsafeEmailDomainError",
    "UnsupportedLocaleError",
    "User",
    "__version__",
    "available_locales",
]
