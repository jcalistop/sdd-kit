# Política de seguridad

## Versiones soportadas

| Versión                    | Soportada |
| -------------------------- | --------- |
| `main`                     | Sí        |
| Tags de release publicados | Sí        |

El kit se distribuye como documentación y scripts de bootstrap. Los proyectos que lo consumen como submodule deben actualizar manualmente.

## Qué reportar

Reporta vulnerabilidades que afecten:

- Scripts de bootstrap (`bootstrap/`) que permitan ejecución arbitraria o fuga de datos
- La CLI (`cli/`) cuando procese rutas o entradas de forma insegura
- Instrucciones para agentes que induzcan a prácticas peligrosas de forma sistemática

No es alcance de este repositorio la seguridad de aplicaciones construidas **con** el kit (Laravel, Django, etc.); esas deben reportarse en sus proyectos respectivos.

## Cómo reportar

**No abras un issue público** para vulnerabilidades de seguridad.

1. Envía un mensaje privado al mantenedor vía [GitHub Security Advisories](https://github.com/jcalistop/sdd-kit/security/advisories/new) o contacto directo con [@jcalistop](https://github.com/jcalistop).
2. Incluye: descripción, pasos para reproducir, impacto estimado y versión/commit afectado.
3. Espera confirmación en un plazo razonable (objetivo: 5 días hábiles).

## Qué esperar

- Confirmación de recepción del reporte
- Evaluación del impacto y plan de corrección
- Coordinación de divulgación responsable antes de publicar el fix

## Buenas prácticas al usar el kit

- Revisa los scripts de `init-sdd` antes de ejecutarlos en entornos sensibles
- No commitees secretos en `sdd.config.yaml` ni en specs de tu proyecto
- Mantén el submodule actualizado cuando publiquemos correcciones de seguridad
