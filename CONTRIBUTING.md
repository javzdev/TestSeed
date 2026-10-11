# Contribuir a TestSeed / Contributing

¡Gracias por tu interés! Las contribuciones en español o inglés son bienvenidas.
*Contributions in Spanish or English are welcome.*

Al participar aceptas el [Código de Conducta](CODE_OF_CONDUCT.md).

## Preparar el entorno

```bash
git clone https://github.com/javzdev/TestSeed.git
cd TestSeed
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Antes de abrir un PR

```bash
ruff check .
ruff format .
mypy
pytest --cov
```

o simplemente `./scripts/check.sh` (Windows: `.\scripts\check.ps1`). CI corre lo mismo en
Linux, Windows y macOS con Python 3.11–3.13.

## Reglas del proyecto

1. **Reproducibilidad primero.** `tests/test_reproducibility.py` fija valores exactos.
   Si tu cambio los rompe, **no actualices los valores sin más**: explícalo en el PR y
   añade una entrada en *Reproducibility changes* del CHANGELOG. Esos cambios nunca
   entran en una versión de parche.
2. **Usa siempre `Stream`, nunca `random`.** Cada valor nuevo debe salir de un stream con
   una ruta propia (`self._stream("modelo", index, "campo")`), para no desplazar los
   valores existentes.
3. **Privacidad.** Ningún dato puede confundirse con uno real. Lee [docs/PRIVACY.md](docs/PRIVACY.md).
4. **Cero dependencias de runtime.** Las de desarrollo van en `[project.optional-dependencies].dev`.
5. **Tipado estricto.** `mypy --strict` sin errores; nada de `Any` en la API pública.
6. **Alcance.** Revisa [docs/ROADMAP.md](docs/ROADMAP.md); abre un issue antes de
   trabajar en algo grande.

## Añadir un locale

1. Crea `src/testseed/locales/<codigo>.py` con una constante `LOCALE = LocaleData(...)`
   (mira `es_CR.py`). Solo datos, sin lógica.
2. Regístralo en `_REGISTRY` de `src/testseed/locales/__init__.py`.
3. Usa nombres comunes del país, sin duplicados, y dominios `.test`.
4. Actualiza `test_available_locales`, el README y el CHANGELOG.

## Guía de issues

- **Bug:** usa la plantilla e incluye `locale`, `seed` y versión. Un ejemplo
  reproducible vale más que mil palabras.
- **Propuesta:** describe primero el problema y tu caso de uso real, y luego la API.
  Toda propuesta de dato nuevo debe explicar cómo se mantiene claramente ficticio.
- **Vulnerabilidad o fuga de privacidad:** **no** abras un issue público; sigue [SECURITY.md](SECURITY.md).
- **Preguntas:** usa GitHub Discussions.
- **Nunca pegues datos personales reales** en un issue.

Etiquetas: `bug`, `enhancement`, `locale`, `privacy`, `reproducibility`, `good first issue`,
`post-mvp`, `triage`.

## Commits y PRs

- Mensajes en imperativo y cortos (`Add es_MX locale`, `Fix leap-day birth dates`).
  Se recomienda [Conventional Commits](https://www.conventionalcommits.org/) pero no es obligatorio.
- Un PR = un cambio. Anota el cambio en `CHANGELOG.md` bajo `Unreleased`.
