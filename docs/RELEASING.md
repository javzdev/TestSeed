# Mantenimiento y publicación

*DevOps / Mantenedor Open Source · versión 0.1.0*

## Licencia: MIT

Se elige **MIT** frente a Apache-2.0 porque:

- es la más corta y conocida, lo que reduce la fricción para estudiantes y empresas pequeñas;
- es la misma licencia que Faker y Polyfactory, así que no hay dudas de compatibilidad
  si algún día se integra con ellas;
- la ventaja principal de Apache-2.0 (la concesión explícita de patentes) es poco relevante
  para una biblioteca de datos de prueba sin algoritmos patentables.

Si en el futuro se aceptan contribuciones corporativas grandes, se puede reevaluar.

## Versionado

- [SemVer](https://semver.org/lang/es/). Versión inicial: **0.1.0** (alpha).
- La versión vive en `src/testseed/__init__.py` (`__version__`) y hatchling la lee de ahí.
- Tags con el formato `vMAJOR.MINOR.PATCH` (por ejemplo `v0.1.0`).
- Reglas de reproducibilidad por tipo de versión: ver [DESIGN.md](DESIGN.md#qué-no-debe-cambiar-entre-versiones-menores-contrato).

## CI (`.github/workflows/ci.yml`)

| Job | Qué hace |
|---|---|
| `lint` | `ruff check`, `ruff format --check`, `mypy` (estricto) |
| `test` | pytest con cobertura ≥ 95 % en Python 3.11/3.12/3.13 (Linux), más Windows y macOS |
| `build` | `python -m build`, `twine check --strict` e instalación del wheel en un entorno limpio |

## Proceso de release

1. Verifica que el nombre `testseed` siga libre en PyPI (si no, cambia `name` en `pyproject.toml`).
2. Mueve las entradas de `Unreleased` a una nueva sección en `CHANGELOG.md`, con fecha.
3. Actualiza `__version__`.
4. `./scripts/check.sh && python -m build && twine check --strict dist/*`
5. Commit `Release vX.Y.Z`, tag `git tag -a vX.Y.Z -m "vX.Y.Z"` y `git push --tags`.
6. `release.yml` vuelve a correr las pruebas, comprueba que el tag coincida con la versión,
   construye y publica primero en **TestPyPI** y después en **PyPI**.

### Configuración única (todavía sin hacer)

El workflow de release **no publica nada** hasta que alguien con permisos:

1. cree el proyecto en PyPI y TestPyPI y configure un
   [Trusted Publisher](https://docs.pypi.org/trusted-publishers/) para este repo y el
   workflow `release.yml` (sin tokens guardados en GitHub);
2. cree los environments `testpypi` y `pypi` en *Settings → Environments*, y añada
   *required reviewers* a `pypi`.

### Prueba local de publicación (sin publicar)

```bash
python -m build
twine check --strict dist/*
python -m venv /tmp/t && /tmp/t/bin/pip install dist/*.whl
/tmp/t/bin/python -c "from testseed import TestSeed; print(TestSeed(seed=1).user())"
```

## Configuración recomendada del repositorio

- Proteger `main`: PR obligatorio, CI verde y una revisión.
- Activar *Private vulnerability reporting* y *Discussions*.
- Crear las etiquetas listadas en CONTRIBUTING.md.
- Dependabot ya está configurado (`.github/dependabot.yml`).
