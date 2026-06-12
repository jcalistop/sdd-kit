# Documentacion para mantenedores del kit

> Archivos de **planificacion, analisis y evolucion** del repositorio `sdd-kit`.
> **No** se copian a proyectos consumidores con `init-sdd` — viven solo en el repo del kit.

## Contenido

| Documento                                                                | Uso                                                                 |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| [ANALYSIS.md](ANALYSIS.md)                                               | Analisis critico del kit: fortalezas, debilidades, oportunidades    |
| [ROADMAP.md](ROADMAP.md)                                                 | Plan de evolucion por fases (1–4) y metricas de exito               |
| [PROMPT-CATALOG.md](PROMPT-CATALOG.md)                                   | Catálogo de prompts usuario: arquitectura, mantenimiento, CLI       |
| [TOKEN-OPTIMIZATION.md](TOKEN-OPTIMIZATION.md)                           | Reduccion de tokens en reglas always-on del agente (Cursor)         |
| [../../.github/docs/sdd/ADOPTION.md](../../.github/docs/sdd/ADOPTION.md) | Plan de adopción SDD en el propio kit (dogfooding)                  |
| [../../.github/docs/sdd/BACKLOG.md](../../.github/docs/sdd/BACKLOG.md)   | Tablero operativo de iniciativas (reemplaza ROADMAP como día a día) |

## Historial de versiones

Notas de release y changelog del kit: **[docs/releases/](../releases/)** (no en este directorio).

## Kit vs documentacion de mantenimiento

| Capa                  | Ubicacion                                                             | Audiencia                        |
| --------------------- | --------------------------------------------------------------------- | -------------------------------- |
| **Kit (consumible)**  | `core/`, `profiles/`, `bootstrap/`, `cli/`, `README.md`, `INSTALL.md` | Proyectos que adoptan SDD        |
| **Proceso SDD**       | `.github/docs/sdd/` (BACKLOG, specs, ADOPTION)                        | Cómo evoluciona el kit con SDD   |
| **Contexto producto** | `.github/docs/business/`                                              | Qué es el kit; reglas del agente |
| **Mantenimiento**     | `docs/maintainers/` (este directorio)                                 | Análisis y roadmap histórico     |
| **Releases del kit**  | `docs/releases/`                                                      | Historial de versiones SemVer    |

## Referencias al kit

- [README.md](../../README.md) — descripcion e instalacion
- [INSTALL.md](../../INSTALL.md) — guia de instalacion
- [core/workflow.md](../../core/workflow.md) — ciclo SDD
- [core/healthy-development.md](../../core/healthy-development.md) — guia de desarrollo sano (humanos y agentes)
- [core/prompt-catalog.md](../../core/prompt-catalog.md) — indice de prompts para usuarios del kit
