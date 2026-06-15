# Planificación y análisis del kit

> **Audiencia:** mantenedores del repositorio `sdd-kit`.
> Documentación **histórica y estratégica** — no se copia a proyectos consumidores con `init-sdd`.

**Tablero operativo diario:** [BACKLOG](../../sdd/BACKLOG.md) · **Adopción SDD:** [ADOPTION](../../sdd/ADOPTION.md)

## Contenido

| Documento                                        | Uso                                                        |
| ------------------------------------------------ | ---------------------------------------------------------- |
| [ANALYSIS.md](ANALYSIS.md)                       | Análisis crítico: fortalezas, debilidades, oportunidades   |
| [ROADMAP.md](ROADMAP.md)                         | Snapshot de evolución por fases (histórico)                |
| [prompt-catalog-meta.md](prompt-catalog-meta.md) | Notas internas del catálogo de prompts (meta mantenedores) |
| [TOKEN-OPTIMIZATION.md](TOKEN-OPTIMIZATION.md)   | Reducción de tokens en reglas always-on (Cursor)           |

**Catálogo público de prompts:** [core/prompt-catalog.md](../../../../core/prompt-catalog.md) (consumidores).

## Post-clone (mantenedores)

Tras clonar o actualizar el kit, reinstala artefactos locales del agente:

```bash
python bootstrap/install-agents.py --kit-path .
```

Esto genera `.cursor/rules/` y `.cursor/skills/sdd-*` desde `bootstrap/agent-prompts/` y `bootstrap/agent-skills/`. Esas rutas están en `.gitignore` — no se versionan (fuente canónica en `bootstrap/`).

## Capas del repositorio

| Capa                  | Ubicación                                           | Audiencia                        |
| --------------------- | --------------------------------------------------- | -------------------------------- |
| **Kit (consumible)**  | `core/`, `profiles/`, `bootstrap/`, `cli/`          | Proyectos que adoptan SDD        |
| **Proceso SDD**       | `.github/docs/sdd/`                                 | Ciclo de iniciativas del kit     |
| **Contexto producto** | `.github/docs/business/`                            | Qué es el kit; reglas del agente |
| **Planificación**     | `.github/docs/business/planning/` (este directorio) | Análisis y roadmap histórico     |
| **Releases del kit**  | `docs/releases/`                                    | Historial SemVer del producto    |

## Referencias

- [domain-rules.md](../domain-rules.md) — invariantes del producto
- [README.md](../../../../README.md) — descripción e instalación
- [docs/releases/](../../../../docs/releases/) — notas de versión
