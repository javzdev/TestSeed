# Análisis previo y plan del MVP

*Product Manager + Arquitectura · versión 0.1.0*

## 1. Resumen del problema

Los equipos necesitan datos de prueba que:

1. **parezcan reales** (nombres y formatos locales, sobre todo en Latinoamérica);
2. **sean seguros**: que un correo de prueba no le llegue nunca a una persona y que un "número
   de cédula" no pase por un documento real;
3. **sean reproducibles**: que un test que falla hoy falle igual mañana, en CI y en la
   laptop de otra persona.

Muchas veces se usan copias de producción (riesgo legal y de privacidad) o datos
inventados a mano (pobres, repetitivos y que no cubren casos límite).

## 2. Comparación con Faker y Polyfactory

| | **Faker** | **Polyfactory** | **TestSeed (MVP)** |
|---|---|---|---|
| Enfoque | Biblioteca de *proveedores* de valores sueltos | *Factories* que construyen instancias a partir de type hints | Registros completos y coherentes con un contrato de reproducibilidad |
| Alcance | Muy amplio: cientos de proveedores, decenas de locales | Dataclasses, TypedDict, Pydantic, attrs, msgspec, SQLAlchemy… | Pequeño: usuarios, nombres, correos, IDs, fechas |
| Datos realistas | Sí, depende de Faker | Delegado en Faker | Sí, para `en` y `es_CR` |
| Seeds | `Faker.seed()` / `seed_instance()`. La documentación advierte que los valores pueden cambiar entre versiones de Faker | `__random_seed__` / `seed_random()`, hereda la variabilidad de Faker | Mismos datos en la misma versión, **en cualquier SO y Python**, comprobado con snapshots en CI |
| Correos | Mezcla dominios reales de correo gratuito con `safe_email()` (dominios example.*) | Lo que genere Faker | **Solo** dominios reservados por la IETF, validados |
| Identificadores | Varios locales generan números con formato válido (SSN, CURP, RFC…) y tarjetas que pasan Luhn | Ídem | Prefijo `TS-` obligatorio; nunca formatos de documentos reales |
| Dependencias | 1 (`tzdata` en algunas plataformas) | Faker + `typing-extensions` | **0** |
| Costa Rica | No encontramos un locale `es_CR` dedicado (verificar antes de comunicarlo públicamente) | — | Primer locale, con dos apellidos |

**Conclusión honesta:** Faker gana en amplitud y Polyfactory en integración con modelos.
TestSeed **no** compite en cantidad de proveedores.

## 3. Diferenciación de TestSeed

1. **Seguro por defecto, no por elección.** El camino fácil (`seed.user()`) ya es seguro;
   salirse de él (un dominio real) da error.
2. **Contrato de reproducibilidad explícito y comprobado:** PRNG propio sobre SHA-256
   (no depende del módulo `random`), un stream por campo y snapshots en CI sobre 3 SO y 3
   versiones de Python.
3. **Registros coherentes:** el correo se deriva del nombre, la edad respeta el rango y la
   cuenta se crea después del nacimiento.
4. **Latinoamérica de primera clase,** empezando por Costa Rica, respetando convenciones
   locales como los dos apellidos.
5. **Cero dependencias,** apto para aulas y entornos restringidos.

A futuro, TestSeed puede *convivir* con Polyfactory (por ejemplo, un proveedor de TestSeed
que alimente sus factories). Es post-MVP.

## 4. Riesgos y suposiciones

| Riesgo | Mitigación |
|---|---|
| El diferenciador no basta para que lo adopten | Validar con 5–10 equipos antes de crecer (ver ROADMAP) |
| Faker añade `es_CR` | El valor central es seguridad + reproducibilidad, no solo el locale |
| Listas de nombres cortas → poca variedad | Documentado; ampliarlas es fácil (solo datos) |
| Un nombre generado coincide con una persona real | Inevitable con nombres comunes; documentado sin promesas absolutas |
| Romper la reproducibilidad sin querer | Snapshots + regla en CONTRIBUTING + sección en CHANGELOG |
| El nombre `testseed` ya existe en PyPI | **Verificar antes de publicar**; alternativa: `testseed-data` |

Suposiciones: los usuarios son desarrolladores Python ≥ 3.11; basta con estructuras Python
simples; el español de Costa Rica es el primer mercado de validación.

## 5. Plan del MVP

### Objetivos

- API de una línea para crear usuarios realistas y seguros.
- Reproducibilidad garantizada y comprobada.
- Paquete listo para PyPI, con CI y documentación bilingüe.

### Fuera de alcance (post-MVP)

Direcciones, teléfonos, productos, pedidos, relaciones entre entidades, exportadores
JSON/CSV/SQL, CLI, plugin de pytest, esquemas personalizados, plugins de terceros,
integración con bases de datos, más locales, generación de documentos de identidad
(**nunca**, ni post-MVP).

### Historias de usuario y criterios de aceptación

| # | Historia | Criterios de aceptación | Prioridad |
|---|---|---|---|
| H1 | Como dev quiero `seed.user()` para tener un usuario realista sin configurar nada | Devuelve `User` con todos los campos; sin argumentos obligatorios | **MVP – P0** |
| H2 | Como QA quiero `seed.users(count=n)` | Devuelve `n` usuarios; `0 ≤ n ≤ 1 000 000`; error claro si el tipo o el rango son inválidos | **MVP – P0** |
| H3 | Como QA quiero la misma salida con la misma semilla | Snapshot idéntico en Linux/Windows/macOS y Python 3.11–3.13 | **MVP – P0** |
| H4 | Como responsable de seguridad quiero que ningún correo sea entregable | Todos los correos terminan en un dominio reservado; un dominio real lanza `UnsafeEmailDomainError` | **MVP – P0** |
| H5 | Como dev costarricense quiero nombres locales | `es_CR` produce dos apellidos distintos de una lista local | **MVP – P0** |
| H6 | Como dev quiero fechas en un rango | `date_between` incluye ambos límites y valida orden y formato | **MVP – P0** |
| H7 | Como dev quiero IDs que no se confundan con reales | Formato `TS-<PREFIJO>-<10>`, únicos por instancia | **MVP – P1** |
| H8 | Como QA quiero edades controladas | `min_age`/`max_age` respetados según una `reference_date` fija | **MVP – P1** |
| H9 | Como dev quiero serializar a JSON | `to_dict()` serializable, con orden de claves estable | **MVP – P1** |
| H10 | Como mantenedor quiero CI y release reproducibles | CI verde; `python -m build` + `twine check` pasan | **MVP – P1** |
| H11 | `datetime_between`, `reset()`, `email_domains` personalizados | Pruebas incluidas | *Opcional (incluido)* |
