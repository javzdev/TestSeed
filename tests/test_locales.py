from __future__ import annotations

import pytest

from testseed import (
    DEFAULT_LOCALE,
    TestSeed,
    TestSeedError,
    UnsupportedLocaleError,
    available_locales,
)
from testseed.locales import LocaleData, get_locale, normalize_locale


def test_available_locales() -> None:
    assert available_locales() == ("en", "es_CR")
    assert DEFAULT_LOCALE in available_locales()


def test_default_locale() -> None:
    assert TestSeed(seed=1).locale == "en"


@pytest.mark.parametrize("code", ["es_CR", "es-CR", "ES_cr", " es-cr "])
def test_locale_normalization(code: str) -> None:
    assert normalize_locale(code) == "es_CR"
    assert TestSeed(locale=code, seed=1).locale == "es_CR"


def test_unsupported_locale_lists_alternatives() -> None:
    with pytest.raises(UnsupportedLocaleError, match="es_CR") as info:
        TestSeed(locale="es_MX")
    assert isinstance(info.value, TestSeedError)
    assert isinstance(info.value, ValueError)


def test_locale_type() -> None:
    with pytest.raises(TypeError):
        get_locale(None)  # type: ignore[arg-type]


@pytest.mark.parametrize("code", available_locales())
def test_locale_data_is_sane(code: str) -> None:
    data = get_locale(code)
    assert len(set(data.first_names)) == len(data.first_names)
    assert len(set(data.last_names)) == len(data.last_names)
    assert all(name.strip() == name and name for name in (*data.first_names, *data.last_names))


def test_locale_data_validation() -> None:
    base = get_locale("en")
    with pytest.raises(ValueError, match="empty"):
        LocaleData("xx", "x", (), base.last_names, 1, base.email_domains)
    with pytest.raises(ValueError, match="surnames_per_person"):
        LocaleData("xx", "x", base.first_names, base.last_names, 3, base.email_domains)
    with pytest.raises(ValueError, match="distinct"):
        LocaleData("xx", "x", base.first_names, ("Solo",), 2, base.email_domains)
    with pytest.raises(ValueError, match="reserved"):
        LocaleData("xx", "x", base.first_names, base.last_names, 1, ("gmail.com",))


def test_es_cr_names_are_local() -> None:
    names = {u.last_name.split()[0] for u in TestSeed(locale="es_CR", seed=1).users(count=300)}
    assert names <= set(get_locale("es_CR").last_names)
