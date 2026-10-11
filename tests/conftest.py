from __future__ import annotations

import pytest

from testseed import TestSeed


@pytest.fixture
def cr() -> TestSeed:
    """A Costa Rican generator with a fixed seed."""
    return TestSeed(locale="es_CR", seed=123)


@pytest.fixture
def en() -> TestSeed:
    """A neutral English generator with a fixed seed."""
    return TestSeed(locale="en", seed=123)
