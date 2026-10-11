"""Quickstart: generate users, names, emails, IDs and dates.

Run with: python examples/quickstart.py
"""

from __future__ import annotations

from testseed import TestSeed


def main() -> None:
    seed = TestSeed(locale="es_CR", seed=123)

    usuario = seed.user()
    print(usuario.full_name, "-", usuario.email)

    for u in seed.users(count=3):
        print(u.id, u.full_name, u.birth_date.isoformat())

    print(seed.first_name(), "|", seed.last_name(), "|", seed.full_name())
    print(seed.email(), "|", seed.fake_id("ORD"))
    print(seed.date_between("2024-01-01", "2024-12-31"))


if __name__ == "__main__":
    main()
