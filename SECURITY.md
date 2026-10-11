# Política de seguridad / Security policy

## Versiones soportadas

| Versión | Soporte |
|---|---|
| 0.1.x | ✅ |

## Reportar un problema

**No abras un issue público.** Usa *Security → Report a vulnerability* en GitHub
(GitHub Private Vulnerability Reporting).

Considera un problema de seguridad o privacidad, por ejemplo:

- Un correo generado que use un dominio no reservado (que podría llegar a una persona real).
- Un identificador con el formato válido de un documento real (cédula, pasaporte, tarjeta).
- Cualquier acceso a red, a archivos o a variables de entorno durante la generación.

Responderemos en un plazo de 7 días y coordinaremos la divulgación contigo.

## Lo que TestSeed no es

TestSeed **no** es una herramienta de anonimización de datos reales ni un generador de
secretos. Su generador no es criptográficamente seguro. Ver [docs/PRIVACY.md](docs/PRIVACY.md).
