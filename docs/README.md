# Documentación del repositorio `sdd-kit`

> **`docs/`** contiene solo notas de **versión SemVer del producto** (`docs/releases/`).
> Planificación, análisis y contexto de producto viven en [`.github/docs/business/`](../.github/docs/business/).

## Glosario: tres carpetas «releases»

| Capa                              | Ruta                                | Rol                                                                                        | ¿Copiado por `init-sdd`?                         |
| --------------------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------ |
| **Release producto kit**          | `docs/releases/vX.Y.Z.md`           | Notas para consumidores y [GitHub Releases](https://github.com/jcalistop/sdd-kit/releases) | No (vive en el submodule)                        |
| **Cierre campaña SDD (kit)**      | `.github/docs/sdd/releases/vX.Y.Z/` | Acta SDD: specs archivados, gates, enlace al producto                                      | No                                               |
| **Plantillas release consumidor** | `core/releases/`                    | RUNBOOK y plantillas para **apps** que adoptan SDD                                         | Sí → `.github/docs/sdd/releases/` en el proyecto |

## Contrato dual-release (producto kit)

Al cerrar una versión SemVer del kit son **obligatorios ambos** artefactos:

1. **Nota producto** — `docs/releases/vX.Y.Z.md` + entrada en `CHANGELOG.md` (audiencia: consumidores / `upgrade-kit`).
2. **Acta campaña** — `.github/docs/sdd/releases/vX.Y.Z/release_vX.Y.Z.md` con campo **Changelog kit** enlazando (1).

No unificar carpetas. No duplicar narrativa larga en el acta (resumen + specs/gates + enlace). Ver [releases/README.md](releases/README.md) y SDD-011.

## Contenido de `docs/`

| Ruta                   | Uso                                       |
| ---------------------- | ----------------------------------------- |
| [releases/](releases/) | CHANGELOG y notas `vX.Y.Z.md` del kit     |

Planificación histórica del kit: [`.github/docs/business/planning/`](../.github/docs/business/planning/).

## Relacionado

- [`.github/docs/business/domain-rules.md`](../.github/docs/business/domain-rules.md) — reglas DR-6 y DR-7 (capas)
- [`.github/docs/sdd/ADOPTION.md`](../.github/docs/sdd/ADOPTION.md) — adopción SDD en el kit
- [README.md](../README.md) — documentación pública del producto
