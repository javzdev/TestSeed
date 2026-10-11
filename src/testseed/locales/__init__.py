"""Locale registry.

To add a locale, create ``testseed/locales/<code>.py`` exposing a ``LOCALE``
constant and register it in ``_REGISTRY``.
"""

from __future__ import annotations

from typing import Final

from testseed.errors import UnsupportedLocaleError
from testseed.locales import en, es_CR
from testseed.locales._base import LocaleData

DEFAULT_LOCALE: Final = "en"

_REGISTRY: Final[dict[str, LocaleData]] = {
    en.LOCALE.code: en.LOCALE,
    es_CR.LOCALE.code: es_CR.LOCALE,
}

__all__ = ["DEFAULT_LOCALE", "LocaleData", "available_locales", "get_locale", "normalize_locale"]


def normalize_locale(code: str) -> str:
    """Normalize ``"es-cr"``, ``"ES_CR"`` or ``" es_CR "`` to ``"es_CR"``."""
    if not isinstance(code, str):
        raise TypeError(f"locale must be a str, got {type(code).__name__}")
    language, _, region = code.strip().replace("-", "_").partition("_")
    return f"{language.lower()}_{region.upper()}" if region else language.lower()


def get_locale(code: str) -> LocaleData:
    """Return the data for ``code`` or raise :class:`UnsupportedLocaleError`.

    There is no silent fallback: asking for ``"es_MX"`` fails loudly instead of
    quietly producing Costa Rican or English data.
    """
    normalized = normalize_locale(code)
    try:
        return _REGISTRY[normalized]
    except KeyError:
        supported = ", ".join(available_locales())
        raise UnsupportedLocaleError(
            f"locale {code!r} is not supported. Available locales: {supported}"
        ) from None


def available_locales() -> tuple[str, ...]:
    """Return the supported locale codes, sorted."""
    return tuple(sorted(_REGISTRY))
