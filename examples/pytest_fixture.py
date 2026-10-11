"""Using TestSeed inside your own pytest suite.

Copy the fixture into your ``conftest.py``. A fixed seed keeps failures
reproducible; print ``seed.seed`` when you use a random one.

Run with: python examples/pytest_fixture.py
"""

from __future__ import annotations

import pytest

from testseed import TestSeed, User


@pytest.fixture
def data() -> TestSeed:
    return TestSeed(locale="es_CR", seed=2024)


def register(user: User, registry: dict[str, User]) -> None:
    """Toy system under test."""
    if user.email in registry:
        raise ValueError("duplicate email")
    registry[user.email] = user


def test_register_many(data: TestSeed) -> None:
    registry: dict[str, User] = {}
    for user in data.users(count=100):
        register(user, registry)
    assert len(registry) == 100


if __name__ == "__main__":
    test_register_many(TestSeed(locale="es_CR", seed=2024))
    print("ok: 100 users registered")
