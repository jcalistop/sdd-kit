# Instancia SDD — índice de artefactos

> Mapa del directorio proceso **`.github/docs/sdd/`** (`paths.sdd`) del repositorio sdd-kit.
> Adopción: [ADOPTION.md](ADOPTION.md) · Tablero: [BACKLOG.md](BACKLOG.md).

**Mantenimiento:** al añadir un audit, research u otra carpeta de proceso, actualiza esta tabla.

| Ruta | Rol |
| ---- | --- |
| [BACKLOG.md](BACKLOG.md) | Tablero operativo (Discovery → Released) |
| [sdd.config.yaml](sdd.config.yaml) | Config de instancia (dominios, IDs, kit, gates) |
| [ADOPTION.md](ADOPTION.md) | Adopción SDD en este repo (etapas, producto vs proceso) |
| [UPGRADE-LOG.md](UPGRADE-LOG.md) | Historial de upgrades del kit en esta instancia |
| [specs/](specs/) | Specs activos (no Released/Descartado) |
| [archive/](archive/) | Specs Released o Descartado |
| [releases/](releases/) | Actas de campaña SDD (`vX.Y.Z/`) |
| [adr/](adr/) | Decisiones arquitectónicas del proceso kit |
| [audits/](audits/) | Auditorías versionadas (planes e informes); **versionado en git** |
| [research/](research/) | Notas de investigación (no son specs ni tablero) |

### Audits actuales

| Artefacto | Nota |
| --------- | ---- |
| [20260906-dogfood-consumidor-externo.md](audits/20260906-dogfood-consumidor-externo.md) | Plan dogfood consumidor externo (**Ejecutado** 2026-09-10) |
| [20260906-dogfood-consumidor-externo-informe.md](audits/20260906-dogfood-consumidor-externo-informe.md) | Informe: Centinela / `v1.4.1` — ciclo OK + gaps harness |
| [20260905-1202-auditoria-general-kit.md](audits/20260905-1202-auditoria-general-kit.md) | Plan de auditoría general |
| [20260905-1202-auditoria-general-kit-informe.md](audits/20260905-1202-auditoria-general-kit-informe.md) | Informe A–F (fuente operativa post-2026-09 vs ANALYSIS histórico) |

### Research actuales

| Artefacto | Nota |
| --------- | ---- |
| [2026-07-15-harness-engineering.md](research/2026-07-15-harness-engineering.md) | Marco harness |
| [2026-07-15-agentes-subagentes.md](research/2026-07-15-agentes-subagentes.md) | Agentes / subagentes |
| [2026-07-15-token-economics-sdd-harness.md](research/2026-07-15-token-economics-sdd-harness.md) | Economía de tokens |

`validate-sdd` **no** exige este índice ni el contenido de `audits/` / `research/` (deuda H-C04 fuera de SDD-021).
