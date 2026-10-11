# Diseño técnico

*Arquitecto de Software · versión 0.1.0*

## Arquitectura

```
          ┌──────────────────────────────────────────┐
 usuario →│ TestSeed (core.py)                        │  API pública, estado:
          │  · contadores por namespace               │  contadores y conjuntos
          │  · unicidad de emails / IDs               │  de unicidad
          └──────┬──────────────┬─────────────────────┘
                 │ Stream       │ LocaleData
                 ▼              ▼
   providers/ (funciones puras)  locales/ (solo datos)
   person · internet ·           en · es_CR
   identifiers · dates
                 │
                 ▼
   _random.Stream (SHA-256 counter mode)    privacy.py (reglas de dominios e IDs)
                 │
                 ▼
   models.User (dataclass inmutable) → to_dict()
```

Capas:

1. **API (`core.TestSeed`)**: validación de argumentos, contadores, unicidad. Es el único
   lugar con estado.
2. **Providers**: funciones puras `f(stream, …) -> valor`. Fáciles de probar y de reutilizar
   para modelos futuros (productos, pedidos).
3. **Locales**: dataclasses de solo datos. Contribuir un locale no requiere tocar lógica.
4. **Núcleo aleatorio (`_random`)**: PRNG determinista propio.
5. **Privacidad (`privacy`)**: reglas centralizadas de lo que se considera seguro.

## Estructura de carpetas

```
testseed/
├── src/testseed/
│   ├── __init__.py          # API pública y __version__
│   ├── core.py              # TestSeed
│   ├── models.py            # User
│   ├── errors.py
│   ├── privacy.py           # dominios reservados, prefijo TS
│   ├── _random.py           # Stream (privado)
│   ├── py.typed
│   ├── locales/  (__init__.py registro, _base.py, en.py, es_CR.py)
│   └── providers/ (person.py, internet.py, identifiers.py, dates.py)
├── tests/                   # pytest; snapshots en test_reproducibility.py
├── examples/                # scripts copiables, ejecutados por la suite
├── docs/
├── scripts/check.{sh,ps1}
├── .github/ (workflows, plantillas de issues y PR, dependabot)
└── pyproject.toml           # hatchling, ruff, mypy, pytest, coverage
```

Se usa *src layout* para que las pruebas corran contra el paquete instalado y no contra
el árbol de fuentes.

## Modelos

```python
@dataclass(frozen=True, slots=True)
class User:
    id: str  # "TS-USR-TV0JJ5C14J"
    first_name: str
    last_name: str  # "Porras Herrera" en es_CR
    email: str  # "carolina.porras25@pruebas.test"
    username: str  # parte local del email
    birth_date: date
    created_at: datetime  # UTC, >= birth_date, <= fin del reference_date
    locale: str
    full_name: str  # propiedad

    def to_dict(self) -> dict[str, Any]: ...
```

Decisión: **dataclass inmutable + `to_dict()`** en lugar de solo diccionarios. Da
autocompletado, tipado y comparación por valor; el diccionario sigue a una llamada de
distancia. `frozen` evita mutaciones accidentales entre tests.

## API pública

Ver la tabla del [README](../README.md#api). Lo que se considera API estable está fijado en
`tests/test_integration.py::test_public_api_surface`.

## Estrategia de seeds y reproducibilidad

- **PRNG propio:** `Stream` = SHA-256(clave ‖ contador), 4 enteros de 64 bits por bloque.
  `randbelow` usa muestreo por rechazo (sin sesgo). No se usa `random` porque CPython solo
  garantiza la secuencia de `random()` entre versiones, no la de `choice`/`randrange`.
- **Un stream por ruta:** `clave = SHA-256("testseed-v1" | seed | locale | namespace | índice | campo)`.
  Consecuencias:
  - el usuario *n* no depende de cuántos números consumió el *n-1* → `users(10)` es
    prefijo de `users(100)`;
  - añadir un campo nuevo a `User` no cambia los campos existentes;
  - cada método (`first_name`, `date_between`…) tiene su propio contador y no interfiere
    con los demás.
- **Fecha de referencia fija** (`2025-01-01` por defecto): las edades no dependen del día
  en que corren los tests.
- **Semilla aleatoria opcional:** `secrets.randbits(63)`, expuesta en `seed.seed`.
- **Versionado del algoritmo:** `ALGORITHM_VERSION` forma parte de la clave; cambiarlo
  invalida todos los snapshots y exige una entrada en el CHANGELOG.
- **Unicidad:** emails e IDs únicos por instancia mediante reintentos deterministas
  (`attempt` en la ruta) y un fallback con sufijo numérico.
- Coste: unos pocos µs por campo; 20 000 usuarios tardan unos 2 s en un portátil.
  Suficiente para el MVP.

### Qué no debe cambiar entre versiones menores (contrato)

| Comportamiento | Parche `0.1.x` | Menor `0.x` (pre-1.0) | Post-1.0 |
|---|---|---|---|
| Datos generados para la misma configuración | No cambia | Solo con nota en *Reproducibility changes* | Solo en versión mayor |
| Nombres y firmas públicas de `__all__` | No cambia | Deprecación previa con aviso | Solo en versión mayor |
| Claves y orden de `to_dict()` | No cambia | Se pueden *añadir* claves al final | Ídem |
| Correos solo en dominios reservados | **Nunca cambia** | **Nunca cambia** | **Nunca cambia** |
| Prefijo `TS-` en los IDs | **Nunca cambia** | **Nunca cambia** | **Nunca cambia** |

## Estrategia de localización

- `LocaleData` describe un locale con datos puros: nombres, apellidos, número de
  apellidos (1 o 2) y dominios.
- Registro explícito en `locales/__init__.py`; códigos normalizados (`es-cr` → `es_CR`).
- Sin *fallback* silencioso: un locale desconocido es un error. Así se evita que alguien
  crea que prueba con datos mexicanos cuando en realidad recibe costarricenses.
- Por defecto `en`, como base neutral e internacional. `es_CR` es el primer locale regional.
- Post-MVP: herencia entre locales (`es_MX` hereda de `es` y sobrescribe solo lo que
  cambia), formatos de teléfono y dirección por locale.

## Extensibilidad

- **Hoy:** un generador nuevo es una función pura en `providers/` más un método en
  `TestSeed` que reserva su namespace (`self._stream("product", index, "name")`). Un
  modelo nuevo sigue el patrón de `_build_user`.
- **Base para datos relacionados:** como cada entidad se identifica por
  `(namespace, índice)`, un futuro `seed.orders()` podrá referenciar al usuario *k* de
  forma determinista (`self._build_user(k, …)`) sin generar los anteriores.
- **Post-MVP:** registro público de providers y plugins vía *entry points*
  (`[project.entry-points."testseed.locales"]`), una vez que la API interna se estabilice.

## Dependencias

**Ninguna en runtime.** Usar Faker habría acelerado el arranque, pero:

1. su salida puede cambiar entre versiones, lo que rompe nuestra promesa central;
2. su `email()` puede devolver dominios reales;
3. arrastraríamos cientos de proveedores que no usamos.

Para el alcance del MVP, unas pocas listas de datos y ~400 líneas de código son más simples
de auditar que una dependencia. Herramientas de desarrollo: pytest, pytest-cov, ruff, mypy,
build y twine. Backend de build: hatchling (solo en tiempo de build).
