"""Person name providers."""

from __future__ import annotations

from testseed._random import Stream
from testseed.locales import LocaleData


def first_name(stream: Stream, locale: LocaleData) -> str:
    """Return a first name from the locale."""
    return stream.choice(locale.first_names)


def last_name(stream: Stream, locale: LocaleData) -> str:
    """Return the surname(s) for the locale, e.g. ``"Mora Vargas"`` for ``es_CR``."""
    names = locale.last_names
    first_index = stream.randbelow(len(names))
    surnames = [names[first_index]]
    if locale.surnames_per_person == 2:
        # Pick a different second surname: skip over the first one.
        offset = 1 + stream.randbelow(len(names) - 1)
        surnames.append(names[(first_index + offset) % len(names)])
    return " ".join(surnames)
