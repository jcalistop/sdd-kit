# SDD Kit — contexto de producto

> Contexto de **negocio del producto kit**, no de un proyecto consumidor.
> Separado de la metodología SDD en `.github/docs/sdd/`.

## Qué es

**SDD Kit** es una metodología y conjunto de herramientas para desarrollar software **con un plan antes de codear**. Está pensado para equipos pequeños (típicamente una persona) y desarrollo asistido por agente de IA.

Principio rector: **spec antes de código, evidencia antes de despliegue, archivo después de release.**

## Problema que resuelve

Proyectos sin hoja de ruta, erráticos y de difícil mantención — especialmente cuando un solo desarrollador trabaja con IA sin proceso claro.

## Audiencias

| Audiencia      | Qué consume                           | Dónde                                                    |
| -------------- | ------------------------------------- | -------------------------------------------------------- |
| **Consumidor** | Metodología, perfiles, bootstrap, CLI | `core/`, `profiles/`, `bootstrap/`, `cli/` vía submodule |
| **Mantenedor** | Evolución del kit, backlog, specs     | `.github/docs/sdd/`, `docs/maintainers/`                 |

## Módulos principales

| Módulo        | Ubicación           | Responsabilidad                                   |
| ------------- | ------------------- | ------------------------------------------------- |
| **Core**      | `core/`             | Ciclo SDD, plantillas, guías (agnóstico al stack) |
| **Perfiles**  | `profiles/<stack>/` | Quality gates, deploy y checklist por tecnología  |
| **Bootstrap** | `bootstrap/`        | `init-sdd`, `validate-sdd`, adaptadores de agente |
| **CLI**       | `cli/`              | Comandos `sdd` (validate, backlog, spec, release) |

## Relacionado

- [domain-rules.md](domain-rules.md) — reglas que el agente debe respetar al evolucionar el kit
- [../sdd/BACKLOG.md](../sdd/BACKLOG.md) — iniciativas en curso
- [../../README.md](../../README.md) — documentación pública del kit
