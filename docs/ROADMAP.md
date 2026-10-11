# Validación y roadmap post-MVP

*Product Manager · versión 0.1.0*

## Plan de validación

**Objetivo:** confirmar en 6–8 semanas que "seguro por defecto + reproducible + es_CR"
resuelve un dolor real, antes de ampliar el alcance.

1. **Pruebas guiadas (semanas 1–3):** 5–10 desarrolladores (comunidades Python de Costa
   Rica, cursos universitarios, 2–3 equipos de QA). Tarea: sustituir los datos de prueba
   de una suite existente por TestSeed en 30 minutos. Observar dónde se atascan y qué echan en falta.
2. **Entrevista corta (15 min):** ¿qué usaban antes? ¿Les importa la reproducibilidad o
   la seguridad de los correos? ¿Qué dato necesitan después?
3. **Publicación alpha (semanas 3–8):** publicar en PyPI y anunciarlo en foros y
   comunidades locales. Fijar en GitHub Discussions un issue "¿Qué datos necesitas?".

### Métricas iniciales

| Métrica | Señal mínima a las 8 semanas |
|---|---|
| Descargas en PyPI (pypistats, sin contar CI) | > 300/mes |
| Estrellas en GitHub | > 50 |
| Issues abiertos por terceros | ≥ 10 |
| PRs externos aceptados | ≥ 3 (al menos un locale nuevo) |
| Feedback cualitativo | ≥ 5 entrevistas; ≥ 3 personas que lo usarían en su trabajo |
| Repos públicos que lo usan (GitHub dependency graph) | ≥ 5 |

Las descargas por sí solas son una métrica ruidosa; pesan más los issues y las entrevistas.

### Qué posponer hasta validar la demanda

Todo lo de abajo. En concreto **no** construir CLI, plugin de pytest ni integraciones con
bases de datos hasta tener al menos 3 peticiones independientes de cada uno.

## Roadmap post-MVP

Orden tentativo según el feedback esperado. Cada punto requiere su propio issue de diseño.

| Versión | Funcionalidad | Notas |
|---|---|---|
| 0.2 | **Más locales** (`es_MX`, `es_CO`, `es` neutro) y herencia entre locales | Lo más barato y lo que más amplía la audiencia |
| 0.2 | **Direcciones y teléfonos** | Con las políticas de [PRIVACY.md](PRIVACY.md) |
| 0.3 | **Productos e inventario** (`seed.products()`) | Nombres, SKU `TS-SKU-…`, precios y stock |
| 0.3 | **Pedidos y datos relacionados** (`seed.orders(users=...)`) | Usa la identidad `(namespace, índice)` ya preparada |
| 0.4 | **Exportación JSON y CSV** (`testseed.export`) | Hoy basta con `to_dict()` + stdlib |
| 0.4 | **CLI** (`testseed users --count 100 --locale es_CR --format csv`) | Sin dependencias (argparse) |
| 0.5 | **Plugin de pytest** (fixture `testseed`, `--testseed-seed`, imprimir la semilla al fallar) | Opt-in vía entry point |
| 0.5 | **Fixtures para APIs y bases de datos** (SQL `INSERT`, cargas para SQLite) | Sin ORM obligatorio |
| 0.6 | **Esquemas personalizados** (`seed.records(schema={...})` o desde dataclasses) | Evaluar integración con Polyfactory en vez de duplicarla |
| 1.0 | **Plugins comunitarios** (locales y providers vía entry points) | API interna estable y documentada |

## Definition of Done del MVP

- [x] Se instala localmente en modo desarrollo (`pip install -e ".[dev]"`)
- [x] Genera un usuario (`user()`) y una lista de usuarios (`users(count)`)
- [x] La misma semilla produce los mismos datos en la misma versión (snapshots en CI multiplataforma)
- [x] Los correos usan dominios `.test` por defecto; los dominios reales se rechazan
- [x] Las pruebas pasan (pytest, cobertura ≥ 95 %)
- [x] Ruff y mypy (estricto) sin errores
- [x] El README (ES + EN) explica instalación, uso, limitaciones y privacidad
- [x] Licencia MIT, CONTRIBUTING, CODE_OF_CONDUCT, CHANGELOG, SECURITY y plantillas de issues y PR
- [x] CI básica (lint, tipos, pruebas en 3 SO, build)
- [x] Paquete preparado para PyPI (`python -m build` + `twine check` pasan); publicado en PyPI como 0.1.0
- [x] Repo en GitHub, Trusted Publishing configurado y v0.1.0 publicada
