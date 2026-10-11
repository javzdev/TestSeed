# Privacidad y seguridad de los datos generados

*Especialista en Seguridad y Privacidad · versión 0.1.0*

TestSeed genera **datos ficticios para pruebas**. No anonimiza datos reales, no garantiza
privacidad absoluta y no es una fuente de aleatoriedad criptográfica.

## Políticas por tipo de dato

| Dato | Política | Estado |
|---|---|---|
| **Correos** | Solo dominios reservados por la IETF: TLD `.test`, `.example`, `.invalid`, `.localhost` (RFC 2606/6761) y `example.com/.net/.org`. Cualquier otro se rechaza con `UnsafeEmailDomainError`. Por defecto, siempre `.test` | **MVP** |
| **Identificadores** | `TS-<PREFIJO>-<10 caracteres Crockford Base32>`, siempre con letras. Nunca se imitan cédulas, DIMEX, pasaportes, números fiscales ni de seguridad social | **MVP** |
| **Nombres** | Combinaciones aleatorias de nombres y apellidos comunes. Pueden coincidir con personas reales; nunca se usan listas de personas concretas ni de figuras públicas | **MVP** |
| **Fechas** | Rango acotado, relativo a una fecha de referencia fija | **MVP** |
| **Teléfonos** | Cuando se añadan: solo rangos reservados para ficción o documentación cuando existan (p. ej. 555-01XX en NANP). Si un país no tiene rango reservado, usar un formato visiblemente inválido o un prefijo marcado | *Post-MVP* |
| **Direcciones** | Calles y números ficticios; ciudades y provincias reales están permitidas, pero nunca direcciones completas reales | *Post-MVP* |
| **Datos financieros** | Nunca números que pasen la validación de Luhn ni IBAN válidos. Montos y monedas sí. Tarjetas solo con prefijo `TS-CARD-` o con los números de prueba documentados por cada pasarela | *Post-MVP* |
| **Documentos de identidad** | **No se generarán**, ni siquiera post-MVP | Nunca |

## Comprobaciones automáticas

`tests/test_privacy.py` verifica, para cada locale:

- que todos los correos terminen en `.test`;
- que los IDs cumplan el patrón `TS-USR-…`;
- que ningún valor textual coincida con el patrón de la cédula costarricense
  (`#-####-####`) ni con secuencias de 13–19 dígitos (tarjetas);
- que los dominios reales se rechacen;
- que la generación funcione sin acceso a la red.

## Buenas prácticas para quien usa TestSeed

1. No mezcles datos de TestSeed con datos reales en la misma tabla sin marcarlos.
2. Si cargas datos en un entorno compartido (staging), usa un `email_domains` propio
   (`staging.acme.test`) para identificarlos y borrarlos con facilidad.
3. No uses TestSeed para generar contraseñas, tokens ni claves. Para eso existe el módulo `secrets`.
4. No presentes datos de TestSeed como si fueran de personas reales en demos públicas sin aclararlo.
5. La unicidad de correos e IDs es **por instancia**. Si combinas varias instancias, valida
   la unicidad tú mismo.

## Sin promesas absolutas

- No se puede garantizar que ningún nombre generado pertenezca a alguien.
- La unicidad solo se garantiza dentro de una instancia.
- Los dominios reservados no son entregables según los estándares de la IETF, pero un
  servidor de correo mal configurado en tu red podría aceptarlos. Úsalos solo en entornos de prueba.
