# Changelog

Todas las versiones siguen [Semantic Versioning](https://semver.org/lang/es/) y este
archivo sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

Cada versión que cambie los datos generados para una misma semilla lo anota en
**Reproducibility changes**.

## [Unreleased]

## [0.1.0] - 2026-10-10

Primera versión pública (MVP).

### Added

- `TestSeed(locale, seed, *, reference_date, email_domains)`, el punto de entrada.
- `user()` y `users(count)` que devuelven la dataclass inmutable `User`, con `to_dict()`.
- `first_name()`, `last_name()`, `full_name()`, `email()`, `fake_id()`.
- `date_between()` y `datetime_between()` (UTC).
- `reset()` para repetir la secuencia.
- Locales `en` (por defecto) y `es_CR` (dos apellidos).
- Generador determinista basado en SHA-256, independiente de la versión de Python
  (algoritmo v1).
- Validación de dominios de correo reservados (`UnsafeEmailDomainError`).
- Errores `TestSeedError`, `UnsupportedLocaleError`.
- Pruebas de snapshot para el contrato de reproducibilidad.

### Reproducibility changes

- Línea base: algoritmo v1.

[Unreleased]: https://github.com/javzdev/TestSeed/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/javzdev/TestSeed/releases/tag/v0.1.0
