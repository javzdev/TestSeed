## Qué cambia / What changes

<!-- Enlaza el issue: Closes #123 -->

## Checklist

- [ ] `ruff check .`, `ruff format --check .`, `mypy` y `pytest` pasan localmente
- [ ] Añadí o actualicé pruebas
- [ ] Actualicé `CHANGELOG.md` (sección `Unreleased`)
- [ ] **No** modifiqué los valores esperados de `tests/test_reproducibility.py`
      — o, si lo hice, lo documenté en "Reproducibility changes" del CHANGELOG y expliqué el porqué
- [ ] Los datos nuevos no pueden confundirse con datos reales (ver `docs/PRIVACY.md`)
- [ ] No añadí dependencias de runtime
