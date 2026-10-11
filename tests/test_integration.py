"""End-to-end checks of the public API and the shipped examples."""

from __future__ import annotations

import csv
import io
import json
import runpy
from pathlib import Path

import pytest

import testseed
from testseed import TestSeed

EXAMPLES = sorted((Path(__file__).parent.parent / "examples").glob("*.py"))


def test_public_api_surface() -> None:
    """Removing or renaming any of these is a breaking change."""
    assert set(testseed.__all__) == {
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
    }
    for name in ("user", "users", "first_name", "last_name", "full_name", "email",
                 "fake_id", "date_between", "datetime_between", "reset"):  # fmt: skip
        assert callable(getattr(TestSeed, name))


def test_user_dict_keys_are_stable(cr: TestSeed) -> None:
    assert list(cr.user().to_dict()) == [
        "id",
        "first_name",
        "last_name",
        "full_name",
        "email",
        "username",
        "birth_date",
        "created_at",
        "locale",
    ]


def test_users_serialize_to_json_and_csv(cr: TestSeed) -> None:
    rows = [u.to_dict() for u in cr.users(count=50)]
    assert json.loads(json.dumps(rows, ensure_ascii=False)) == rows

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    assert list(csv.DictReader(io.StringIO(buffer.getvalue()))) == rows


def test_repr(cr: TestSeed) -> None:
    assert repr(cr) == "TestSeed(locale='es_CR', seed=123)"


def test_readme_quickstart() -> None:
    seed = TestSeed(locale="es_CR", seed=123)
    usuario = seed.user()
    usuarios = seed.users(count=100)
    fecha = seed.date_between("2024-01-01", "2024-12-31")
    assert usuario.email.endswith(".test")
    assert len(usuarios) == 100
    assert fecha.year == 2024


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.name)
def test_examples_run(path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    runpy.run_path(str(path), run_name="__main__")
    assert capsys.readouterr().out
