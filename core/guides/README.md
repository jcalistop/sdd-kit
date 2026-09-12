# Guías SDD (`core/guides/`)

Metodologías del producto kit (agnósticas al stack). Distinto de **contratos/entrada** en la raíz de `core/` (`workflow`, `concepts`, `safe-git-contract`, etc.).

## Ciclo y operación

| Guía | Uso |
| ---- | --- |
| [adoption-guide.md](adoption-guide.md) | Adopción incremental (proyecto nuevo o existente) |
| [upgrade-guide.md](upgrade-guide.md) | Actualizar el kit en una instancia consumidora |
| [agent-setup.md](agent-setup.md) | Adaptadores multi-agente / IDE |
| [operations.md](operations.md) | Rituales y quién actualiza qué |
| [branching.md](branching.md) | Ramas `dev` / `main`, releases, hotfix |
| [checklist-pr.md](checklist-pr.md) | DoD de trazabilidad y release (común a todos los stacks) |
| [healthy-development.md](healthy-development.md) | Arquitectura, patrones, antipatrones, código limpio |

## Metodologías opcionales (artefactos bajo `paths.sdd`)

Las carpetas `audits/` y `research/` bajo `paths.sdd` de cada instancia **no** son obligatorias.

| Guía | Uso | Plantillas |
| ---- | --- | ---------- |
| [audits.md](audits.md) | Corridas de auditoría (registro default; plan solo si grande) | [`audit-registro`](../templates/audit-registro-template.md), [`audit-plan`](../templates/audit-plan-template.md) |
| [research.md](research.md) | Notas de investigación (corta; ensayo largo opcional) | [`research-nota`](../templates/research-nota-template.md) |

Índice general del core: [../README.md](../README.md).
