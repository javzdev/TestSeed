# TestSeed

**Datos sintéticos realistas, seguros y reproducibles para pruebas de software.**

[English version → README.en.md](README.en.md)

TestSeed genera usuarios, nombres, correos, identificadores y fechas ficticios para
tests, demos, desarrollo local y cursos. Hace tres promesas concretas:

- **Reproducible:** la misma versión + la misma configuración + la misma semilla
  devuelven exactamente los mismos datos, en cualquier sistema operativo y versión de Python.
- **Seguro por defecto:** los correos solo usan dominios reservados para pruebas (`.test`),
  y los identificadores llevan el prefijo `TS-` para que no se confundan con documentos reales.
- **Sin dependencias:** solo la biblioteca estándar de Python, sin llamadas de red.

> Estado: **alpha (0.1.0)**. La API puede cambiar antes de 1.0; los cambios se anotan en el
> [CHANGELOG](CHANGELOG.md).

## Instalación

Requiere Python 3.11 o superior.

```bash
# Desde el código fuente (modo desarrollo)
git clone https://github.com/javzdev/TestSeed.git
cd TestSeed
python -m venv .venv
# Windows: .venv\Scripts\activate    |    Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"
```

> Todavía no está publicado en PyPI. Cuando lo esté: `pip install testseed`.

## Uso rápido

```python
from testseed import TestSeed

seed = TestSeed(locale="es_CR", seed=123)

usuario = seed.user()
print(usuario.full_name)  # Carolina Porras Herrera
print(usuario.email)  # carolina.porras25@pruebas.test
print(usuario.id)  # TS-USR-TV0JJ5C14J

usuarios = seed.users(count=100)

fecha = seed.date_between("2024-01-01", "2024-12-31")
```

### Como diccionario o JSON

```python
import json

datos = [u.to_dict() for u in seed.users(count=3)]
print(json.dumps(datos, ensure_ascii=False, indent=2))
```

`to_dict()` devuelve fechas en ISO 8601 y siempre las mismas claves, en este orden:
`id, first_name, last_name, full_name, email, username, birth_date, created_at, locale`.

### En tus pruebas con pytest

```python
import pytest
from testseed import TestSeed


@pytest.fixture
def datos() -> TestSeed:
    return TestSeed(locale="es_CR", seed=2024)


def test_registro(datos: TestSeed) -> None:
    for usuario in datos.users(count=50):
        assert usuario.email.endswith(".test")
```

Más ejemplos en [`examples/`](examples/).

## API

| Llamada | Devuelve |
|---|---|
| `TestSeed(locale="en", seed=None, *, reference_date=None, email_domains=None)` | Generador |
| `seed.user(*, min_age=18, max_age=80)` | `User` |
| `seed.users(count, *, min_age=18, max_age=80)` | `list[User]` |
| `seed.first_name()` / `seed.last_name()` / `seed.full_name()` | `str` |
| `seed.email(first_name=None, last_name=None)` | `str`, p. ej. `ana.mora07@correo.test` |
| `seed.fake_id(prefix="ID")` | `str`, p. ej. `TS-ID-7K3M9QX2AB` |
| `seed.date_between(start, end)` | `datetime.date` (límites incluidos) |
| `seed.datetime_between(start, end)` | `datetime.datetime` en UTC |
| `seed.reset()` | Reinicia la secuencia desde el principio |
| `seed.seed`, `seed.locale`, `seed.reference_date`, `seed.email_domains` | Configuración en uso |
| `available_locales()` | `("en", "es_CR")` |

`User` es una dataclass inmutable con `id`, `first_name`, `last_name`, `full_name`,
`email`, `username`, `birth_date`, `created_at` (UTC) y `locale`.

Las fechas aceptan `datetime.date` o texto `"AAAA-MM-DD"`.

### Locales

| Código | Descripción |
|---|---|
| `en` (por defecto) | Inglés neutro, un apellido |
| `es_CR` | Español de Costa Rica, dos apellidos (`Mora Vargas`), dominios `correo.test`, `ejemplo.test`, `pruebas.test` |

Se aceptan variantes como `"es-CR"`. Un locale no soportado lanza
`UnsupportedLocaleError`: TestSeed nunca cambia de locale en silencio.

## Reproducibilidad

```python
a = TestSeed(locale="es_CR", seed=42).users(count=10)
b = TestSeed(locale="es_CR", seed=42).users(count=10)
assert a == b
```

Garantías:

1. Igual versión de TestSeed + igual `locale`, `seed`, `reference_date`, `email_domains` +
   igual secuencia de llamadas ⇒ mismos datos, en cualquier SO y Python ≥ 3.11.
2. `users(10)` es siempre el prefijo de `users(100)`.
3. Cada método tiene su propia secuencia: llamar a `first_name()` no cambia el siguiente `user()`.
4. Las edades se calculan contra una **fecha de referencia fija** (2025-01-01 por defecto),
   no contra la fecha de hoy. Así los datos no cambian según el día en que corran tus tests.
5. Si no indicas `seed`, se elige una al azar; léela con `seed.seed` para repetir la ejecución.

Las versiones de parche (`0.1.x`) **nunca** cambian los datos generados. Antes de 1.0, una
versión menor puede cambiarlos, siempre anotado en el CHANGELOG bajo
*Reproducibility changes*.

## Privacidad y seguridad

- **Correos:** solo dominios reservados por la IETF (`*.test`, `*.example`, `*.invalid`,
  `*.localhost`, `example.com/.net/.org`). Si pasas otro dominio en `email_domains` se lanza
  `UnsafeEmailDomainError`.
- **Identificadores:** formato `TS-<PREFIJO>-<10 caracteres>` con letras y números. No
  generamos cédulas, pasaportes, números fiscales ni tarjetas de pago, ni siquiera con formato válido.
- **Nombres:** se combinan al azar a partir de listas de nombres comunes. **Una combinación
  puede coincidir con una persona real**; no la trates como dato de nadie.
- **Sin red:** todo se genera localmente.
- **No es criptografía:** no uses TestSeed para generar contraseñas, tokens ni secretos.
- **Unicidad:** los correos e IDs son únicos *dentro de una instancia*. Entre instancias o
  semillas distintas no hay garantía.

Detalles en [docs/PRIVACY.md](docs/PRIVACY.md).

## Limitaciones (MVP)

- Solo dos locales: `en` y `es_CR`.
- Solo usuarios, nombres, correos, IDs y fechas. Sin direcciones, teléfonos, productos ni pedidos.
- Sin relaciones entre entidades, sin CLI y sin exportadores (usa `to_dict()` + `json`/`csv`).
- Las listas de nombres son cortas (≈40–50 por locale).

Lo que viene está en [docs/ROADMAP.md](docs/ROADMAP.md).

## Desarrollo

```bash
pip install -e ".[dev]"
ruff check .            # lint
ruff format .           # formato
mypy                    # tipos (modo estricto)
pytest --cov            # pruebas + cobertura
./scripts/check.sh      # todo lo anterior (Windows: .\scripts\check.ps1)
python -m build         # construir wheel y sdist en dist/
```

Lee [CONTRIBUTING.md](CONTRIBUTING.md) antes de abrir un PR. Diseño técnico:
[docs/DESIGN.md](docs/DESIGN.md). Publicación: [docs/RELEASING.md](docs/RELEASING.md).

## Licencia

[MIT](LICENSE).
