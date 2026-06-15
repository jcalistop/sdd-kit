# Documentación del repositorio `sdd-kit`

> **`docs/`** contiene solo notas de **versión SemVer del producto** (`docs/releases/`).
> Planificación, análisis y contexto de producto viven en [`.github/docs/business/`](../.github/docs/business/).

## Glosario: tres carpetas «releases»

| Capa                              | Ruta                                | Rol                                                                                        | ¿Copiado por `init-sdd`?                         |
| --------------------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------ |
| **Release producto kit**          | `docs/releases/vX.Y.Z.md`           | Notas para consumidores y [GitHub Releases](https://github.com/jcalistop/sdd-kit/releases) | No (vive en el submodule)                        |
| **Cierre campaña SDD (kit)**      | `.github/docs/sdd/releases/vX.Y.Z/` | Acta SDD: specs archivados, gates, enlace al producto                                      | No                                               |
| **Plantillas release consumidor** | `core/releases/`                    | RUNBOOK y plantillas para **apps** que adoptan SDD                                         | Sí → `.github/docs/sdd/releases/` en el proyecto |

## Contenido de `docs/`

| Ruta                         | Uso                                                                                          |
| ---------------------------- | -------------------------------------------------------------------------------------------- |
| [releases/](releases/)       | CHANGELOG y notas `vX.Y.Z.md` del kit                                                        |
| [maintainers/](maintainers/) | Stub de deprecación (v1.2.0+) — ver [business/planning/](../.github/docs/business/planning/) |

## Relacionado

- [`.github/docs/business/domain-rules.md`](../.github/docs/business/domain-rules.md) — reglas DR-6 y DR-7 (capas)
- [`.github/docs/sdd/ADOPTION.md`](../.github/docs/sdd/ADOPTION.md) — adopción SDD en el kit
- [README.md](../README.md) — documentación pública del producto
