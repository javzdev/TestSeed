# TestSeed

**Realistic, safe and reproducible synthetic data for software testing.**

[Versión en español → README.md](README.md)

TestSeed generates fictitious users, names, emails, identifiers and dates for tests,
demos, local development and teaching. It makes three concrete promises:

- **Reproducible:** same version + same settings + same seed return exactly the same
  data, on any OS and Python version.
- **Safe by default:** emails only use domains reserved for testing (`.test`), and
  identifiers carry a `TS-` prefix so they can't be mistaken for real documents.
- **Zero dependencies:** standard library only, no network calls.

> Status: **alpha (0.1.0)**. The API may change before 1.0; changes are listed in the
> [CHANGELOG](CHANGELOG.md).

## Installation

Requires Python 3.11+.

```bash
git clone https://github.com/javzdev/TestSeed.git
cd TestSeed
python -m venv .venv
# Windows: .venv\Scripts\activate    |    Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"
```

> Not on PyPI yet. Once it is: `pip install testseed`.

## Quickstart

```python
from testseed import TestSeed

seed = TestSeed(locale="es_CR", seed=123)

user = seed.user()
print(user.full_name)  # Carolina Porras Herrera
print(user.email)  # carolina.porras25@pruebas.test
print(user.id)  # TS-USR-TV0JJ5C14J

users = seed.users(count=100)
day = seed.date_between("2024-01-01", "2024-12-31")

rows = [u.to_dict() for u in users]  # JSON-serializable dicts
```

## API

| Call | Returns |
|---|---|
| `TestSeed(locale="en", seed=None, *, reference_date=None, email_domains=None)` | Generator |
| `seed.user(*, min_age=18, max_age=80)` | `User` |
| `seed.users(count, *, min_age=18, max_age=80)` | `list[User]` |
| `seed.first_name()` / `seed.last_name()` / `seed.full_name()` | `str` |
| `seed.email(first_name=None, last_name=None)` | `str`, e.g. `ana.mora07@correo.test` |
| `seed.fake_id(prefix="ID")` | `str`, e.g. `TS-ID-7K3M9QX2AB` |
| `seed.date_between(start, end)` | `datetime.date` (inclusive) |
| `seed.datetime_between(start, end)` | UTC `datetime.datetime` |
| `seed.reset()` | Replays the sequence from the start |
| `available_locales()` | `("en", "es_CR")` |

Locales: `en` (default, neutral English, one surname) and `es_CR` (Costa Rican Spanish,
two surnames). Unsupported locales raise `UnsupportedLocaleError`; there is no silent fallback.

## Reproducibility

1. Same TestSeed version + same `locale`, `seed`, `reference_date`, `email_domains` +
   same call sequence ⇒ same data on every OS and Python ≥ 3.11.
2. `users(10)` is always a prefix of `users(100)`.
3. Each method has its own sequence: calling `first_name()` does not change the next `user()`.
4. Ages are computed against a **fixed reference date** (2025-01-01 by default), never "today".
5. Without `seed`, a random one is chosen; read it from `seed.seed` to replay a run.

Patch releases never change generated data. Before 1.0, a minor release may, and it will
be listed under *Reproducibility changes* in the CHANGELOG.

## Privacy and safety

- Emails only use IETF-reserved domains; any other domain raises `UnsafeEmailDomainError`.
- No national IDs, passports, tax numbers or payment cards are generated, not even in a valid format.
- Names are random combinations of common names and **may match a real person**.
- Not cryptographic: never use TestSeed for passwords, tokens or secrets.
- Emails and IDs are unique *within one instance* only.

See [docs/PRIVACY.md](docs/PRIVACY.md).

## Limitations (MVP)

Two locales, users/names/emails/IDs/dates only; no addresses, phones, relations, CLI or
exporters yet. See [docs/ROADMAP.md](docs/ROADMAP.md).

## Development

```bash
pip install -e ".[dev]"
./scripts/check.sh      # ruff + mypy + pytest (Windows: .\scripts\check.ps1)
python -m build
```

See [CONTRIBUTING.md](CONTRIBUTING.md). License: [MIT](LICENSE).
