"""Exceptions raised by TestSeed."""

from __future__ import annotations


class TestSeedError(Exception):
    """Base class for every TestSeed-specific error."""

    __test__ = False  # Keep pytest from collecting this class.


class UnsupportedLocaleError(TestSeedError, ValueError):
    """The requested locale is not available."""


class UnsafeEmailDomainError(TestSeedError, ValueError):
    """An email domain is not reserved for testing and could reach real people."""
