from __future__ import annotations

from collections import Counter

import pytest

from testseed._random import Stream, derive_key


def test_keys_distinguish_types_and_order() -> None:
    assert derive_key(1, 1) != derive_key(1, "1")
    assert derive_key(1, "a", "b") != derive_key(1, "b", "a")
    assert derive_key(1, "a") != derive_key(2, "a")


def test_randbelow_bounds_and_spread() -> None:
    stream = Stream.from_seed(0, "spread")
    counts = Counter(stream.randbelow(6) for _ in range(6000))
    assert set(counts) == set(range(6))
    assert all(800 < c < 1200 for c in counts.values())


def test_randbelow_large_n() -> None:
    stream = Stream.from_seed(0, "large")
    assert 0 <= stream.randbelow(1 << 64) < 1 << 64
    assert stream.randbelow(1) == 0


@pytest.mark.parametrize("n", [0, -5, (1 << 64) + 1])
def test_randbelow_invalid(n: int) -> None:
    with pytest.raises(ValueError, match="n must"):
        Stream.from_seed(0).randbelow(n)


def test_randint() -> None:
    stream = Stream.from_seed(0)
    assert {stream.randint(-1, 1) for _ in range(200)} == {-1, 0, 1}
    with pytest.raises(ValueError, match="low"):
        stream.randint(2, 1)


def test_choice() -> None:
    stream = Stream.from_seed(0)
    assert stream.choice("abc") in "abc"
    with pytest.raises(IndexError):
        stream.choice([])


def test_random_float_range() -> None:
    stream = Stream.from_seed(0)
    values = [stream.random() for _ in range(1000)]
    assert all(0.0 <= v < 1.0 for v in values)
    assert 0.4 < sum(values) / len(values) < 0.6
