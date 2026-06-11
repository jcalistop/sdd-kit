# Documentacion para mantenedores del kit

> Archivos de **planificacion, analisis y evolucion** del repositorio `sdd-kit`.
> **No** se copian a proyectos consumidores con `init-sdd` — viven solo en el repo del kit.

## Contenido

| Documento                            | Uso                                                              |
| ------------------------------------ | ---------------------------------------------------------------- |
| [ANALYSIS.md](ANALYSIS.md)           | Analisis critico del kit: fortalezas, debilidades, oportunidades |
| [ROADMAP.md](ROADMAP.md)             | Plan de evolucion por fases (1–4) y metricas de exito            |
| [release-notes.md](release-notes.md) | Notas de version del kit (mantenedores)                          |

## Kit vs documentacion de mantenimiento

| Capa                 | Ubicacion                                                             | Audiencia                  |
| -------------------- | --------------------------------------------------------------------- | -------------------------- |
| **Kit (consumible)** | `core/`, `profiles/`, `bootstrap/`, `cli/`, `README.md`, `INSTALL.md` | Proyectos que adoptan SDD  |
| **Mantenimiento**    | `docs/maintainers/` (este directorio)                                 | Quienes evolucionan el kit |

## Referencias al kit

- [README.md](../../README.md) — descripcion e instalacion
- [INSTALL.md](../../INSTALL.md) — guia de instalacion
- [core/workflow.md](../../core/workflow.md) — ciclo SDD
- [core/healthy-development.md](../../core/healthy-development.md) — guia de desarrollo sano (humanos y agentes)
