"""Deterministic, Python-version-independent pseudo-random streams.

TestSeed does not use :mod:`random` to generate data. CPython only guarantees
that ``Random.random()`` keeps producing the same sequence across versions;
``choice``, ``randrange`` and friends may change. To keep the reproducibility
contract under TestSeed's control, every value is drawn from a :class:`Stream`:
a SHA-256 counter-mode generator keyed by the instance seed plus a *path*
(for example ``("user", 7, "first_name")``).

Deriving one independent stream per path means that:

* record ``n`` does not depend on how many values were drawn for record ``n - 1``;
* adding a new field to a model does not shift the values of existing fields;
* the same seed and path produce the same values on any platform.

This module is **not** cryptographically secure for secrets generation and must
never be used for tokens, passwords or keys.
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from typing import Final, TypeVar

_T = TypeVar("_T")

#: Bump only together with a CHANGELOG entry: it changes every generated value.
ALGORITHM_VERSION: Final = 1

_U64: Final = 1 << 64


def derive_key(seed: int, *path: str | int) -> bytes:
    """Return the 32-byte key for ``seed`` and ``path``.

    ``repr`` is used for each component so that ``1`` and ``"1"`` differ.
    """
    material = "\x1f".join(
        [f"testseed-v{ALGORITHM_VERSION}", repr(seed), *(repr(part) for part in path)]
    )
    return hashlib.sha256(material.encode("utf-8")).digest()


class Stream:
    """A deterministic stream of pseudo-random numbers."""

    __slots__ = ("_block", "_buffer", "_key")

    def __init__(self, key: bytes) -> None:
        self._key = key
        self._block = 0
        self._buffer: list[int] = []

    @classmethod
    def from_seed(cls, seed: int, *path: str | int) -> Stream:
        """Create the stream identified by ``seed`` and ``path``."""
        return cls(derive_key(seed, *path))

    def next_u64(self) -> int:
        """Return the next unsigned 64-bit integer."""
        if not self._buffer:
            digest = hashlib.sha256(self._key + self._block.to_bytes(8, "big")).digest()
            self._block += 1
            # Reversed so that ``pop()`` yields the first 8 bytes first.
            self._buffer = [int.from_bytes(digest[i : i + 8], "big") for i in range(24, -1, -8)]
        return self._buffer.pop()

    def randbelow(self, n: int) -> int:
        """Return an unbiased integer in ``[0, n)`` using rejection sampling."""
        if n <= 0:
            raise ValueError(f"n must be positive, got {n}")
        if n > _U64:
            raise ValueError(f"n must be at most 2**64, got {n}")
        limit = _U64 - (_U64 % n)
        while True:
            value = self.next_u64()
            if value < limit:
                return value % n

    def randint(self, low: int, high: int) -> int:
        """Return an integer in ``[low, high]`` (both inclusive)."""
        if low > high:
            raise ValueError(f"low ({low}) must be <= high ({high})")
        return low + self.randbelow(high - low + 1)

    def choice(self, options: Sequence[_T]) -> _T:
        """Return one element of a non-empty sequence."""
        if not options:
            raise IndexError("cannot choose from an empty sequence")
        return options[self.randbelow(len(options))]

    def random(self) -> float:
        """Return a float in ``[0.0, 1.0)`` with 53 bits of precision."""
        return (self.next_u64() >> 11) * (1.0 / (1 << 53))
