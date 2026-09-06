# Backlog SDD — SDD Kit

> Tablero operativo del repositorio **sdd-kit**. Plan estratégico histórico: [business/planning/ROADMAP.md](../../business/planning/ROADMAP.md).
> Adopción: [ADOPTION.md](ADOPTION.md) · Ciclo: [core/workflow.md](../../../core/workflow.md).

**Próximo ID disponible:** `SDD-020`.

**Versión acumulada del kit:** `v1.4.0` (ver [docs/releases/](../../../docs/releases/)). Campaña abierta: **v1.4.1** (SDD-018, SDD-019).

---

## Discovery

> **Versión (recomendación SemVer):** bump de producto kit al cerrar la iniciativa, desde `v1.4.0`. Criterio auditoría: **patch** = higiene/docs/CI sin API nueva; **minor** = capacidad o perfil nuevo backward-compatible; **major** = ruptura para consumidores (ninguna fila actual); **—** = no define release del kit por sí sola.

| Dominio   | Idea / necesidad                                                                 | Versión | Notas                                                                 |
| --------- | -------------------------------------------------------------------------------- | ------- | --------------------------------------------------------------------- |
| bootstrap | Upgrade/paridad multi-agente: wording v1.3.2, `agent.targets`, safe-git doc      | patch   | H-B06/D03/D05–D07; si se cambia comportamiento real de upgrade → reevaluar **minor** |
| docs      | Índice artefactos `paths.sdd` (audits/research) + banner snapshot ANALYSIS       | patch   | H-A04/E02/B09; versionar `audits/`                                    |
| docs      | Validación en producción: ciclo SDD con proyecto consumidor externo              | —       | Dogfooding externo; no bump de kit hasta que genere cambios productizados |
| profiles  | Perfiles adicionales (node-express, go-api, vue-vite) a demanda                  | minor   | Baja prioridad; perfil nuevo = feature compatible                     |

---

## Draft

| ID  | Dominio | Título | Versión | Spec |
| --- | ------- | ------ | ------- | ---- |
| —   | —       | —      | —       | —    |

## Ready

| ID  | Dominio | Título | Versión | Spec |
| --- | ------- | ------ | ------- | ---- |
| —   | —       | —      | —       | —    |

## In Build

| ID      | Dominio   | Título                                                              | Versión    | Spec |
| ------- | --------- | ------------------------------------------------------------------- | ---------- | ---- |
| SDD-019 | infra     | CI: `sdd validate` y gatillo en rama `dev`                          | **v1.4.1** | [SDD-019-ci-validate-sdd-rama-dev.md](specs/infra/SDD-019-ci-validate-sdd-rama-dev.md) |
| SDD-018 | bootstrap | Higiene agentica: retirar `sdd-core.mdc` residual + alinear docs   | **v1.4.1** | [SDD-018-higiene-agentica-sdd-core.md](specs/bootstrap/SDD-018-higiene-agentica-sdd-core.md) |

## Validating

| ID  | Dominio | Título | Versión | Spec |
| --- | ------- | ------ | ------- | ---- |
| —   | —       | —      | —       | —    |


## Released


| ID      | Dominio   | Título                                                                                            | Versión | Fecha      | Spec archivado                                                                                                                             |
| ------- | --------- | ------------------------------------------------------------------------------------------------- | ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| SDD-017 | cli       | Suite pytest para la CLI (backlog, prompts, round-trip)                                           | v1.4.0  | 2026-09-05 | [archive/2026/cli/SDD-017-suite-pytest-cli.md](archive/2026/cli/SDD-017-suite-pytest-cli.md)                                               |
| SDD-016 | core      | Deprecar métricas de tokens y cost-governance                                                     | v1.3.2  | 2026-09-05 | [archive/2026/core/SDD-016-deprecar-tokens-cost-governance.md](archive/2026/core/SDD-016-deprecar-tokens-cost-governance.md)               |
| SDD-015 | core      | Archivar specs en estado Descartado                                                               | v1.3.1  | 2026-08-05 | [archive/2026/core/SDD-015-archive-specs-descartados.md](archive/2026/core/SDD-015-archive-specs-descartados.md)                           |
| SDD-014 | bootstrap | Alinear flujo agentico upgrade-kit al consumo de v1.3.0+                                          | v1.3.0  | 2026-07-15 | [archive/2026/bootstrap/SDD-014-alinear-flujo-upgrade-kit-v130.md](archive/2026/bootstrap/SDD-014-alinear-flujo-upgrade-kit-v130.md)       |
| SDD-013 | cli       | Observabilidad de tokens (`sdd metrics tokens`)                                                   | v1.3.0  | 2026-07-15 | [archive/2026/cli/SDD-013-observabilidad-tokens-metrics.md](archive/2026/cli/SDD-013-observabilidad-tokens-metrics.md)                     |
| SDD-012 | core      | Governance de tokens en el harness (A–F)                                                          | v1.3.0  | 2026-07-15 | [archive/2026/core/SDD-012-governance-tokens-harness.md](archive/2026/core/SDD-012-governance-tokens-harness.md)                           |
| SDD-011 | docs      | Contrato dual-release producto ↔ campaña                                                          | v1.3.0  | 2026-07-15 | [archive/2026/docs/SDD-011-contrato-dual-release-producto-campana.md](archive/2026/docs/SDD-011-contrato-dual-release-producto-campana.md) |
| SDD-010 | cli       | Observabilidad por componente validate-sdd                                                        | v1.3.0  | 2026-07-15 | [archive/2026/cli/SDD-010-observabilidad-componente-validate.md](archive/2026/cli/SDD-010-observabilidad-componente-validate.md)           |
| SDD-009 | docs      | Posicionar sdd-kit como agent harness                                                             | v1.3.0  | 2026-07-15 | [archive/2026/docs/SDD-009-posicionamiento-agent-harness.md](archive/2026/docs/SDD-009-posicionamiento-agent-harness.md)                   |
| SDD-008 | core      | Lenguaje guías/sensores (harness) en prompts                                                      | v1.3.0  | 2026-07-15 | [archive/2026/core/SDD-008-lenguaje-harness-guides-sensors.md](archive/2026/core/SDD-008-lenguaje-harness-guides-sensors.md)               |
| SDD-007 | core      | Contrato safe-git para agente (Git destructivo)                                                   | v1.3.0  | 2026-07-15 | [archive/2026/core/SDD-007-contrato-safe-git-agente.md](archive/2026/core/SDD-007-contrato-safe-git-agente.md)                             |
| —       | bootstrap | Preservar bloque `kit` al reinstalar agent en `sdd.config.yaml`                                   | v1.2.1  | 2026-06-17 | —                                                                                                                                          |
| SDD-006 | bootstrap | Optimización de tokens en reglas, skills y pipeline de generación del kit                         | v1.2.2  | 2026-07-14 | [archive/2026/bootstrap/SDD-006-optimizacion-tokens-kit.md](archive/2026/bootstrap/SDD-006-optimizacion-tokens-kit.md)                     |
| SDD-005 | docs      | Reordenamiento documentación kit                                                                  | v1.2.0  | 2026-06-15 | [archive/2026/docs/SDD-005-reordenamiento-documentacion-kit.md](archive/2026/docs/SDD-005-reordenamiento-documentacion-kit.md)             |
| SDD-004 | bootstrap | Skills SDD en bootstrap (multi-agente)                                                            | v1.2.0  | 2026-06-15 | [archive/2026/bootstrap/SDD-004-agent-skills-cursor.md](archive/2026/bootstrap/SDD-004-agent-skills-cursor.md)                             |
| SDD-003 | core      | Refactor ciclo SDD: momentos semánticos vs prompts                                                | v1.1.0  | 2026-06-12 | [archive/2026/core/SDD-003-refactor-ciclo-sdd-prompts.md](archive/2026/core/SDD-003-refactor-ciclo-sdd-prompts.md)                         |
| SDD-002 | bootstrap | Actualización del kit en instancias consumidoras                                                  | v1.1.0  | 2026-06-12 | [archive/2026/bootstrap/SDD-002-actualizacion-kit-instancias.md](archive/2026/bootstrap/SDD-002-actualizacion-kit-instancias.md)           |
| SDD-001 | profiles  | Perfil `sdd-kit` para mantenedores                                                                | v1.1.0  | 2026-06-12 | [archive/2026/profiles/SDD-001-perfil-sdd-kit.md](archive/2026/profiles/SDD-001-perfil-sdd-kit.md)                                         |
| —       | core      | Fundación agentica: `sdd-agent-workflow`, `adoption-guide`, `validate-sdd`, spec ejemplo Filament | v1.0.0  | 2026-06-11 | pre-SDD                                                                                                                                    |
| —       | profiles  | Perfiles python-fastapi, react-vite, python-django, reports-latex-md                              | v1.0.0  | 2026-06-11 | pre-SDD                                                                                                                                    |
| —       | cli       | CLI `sdd`, sync GitHub Issues, CHANGELOG automático, catálogo de prompts                          | v1.0.0  | 2026-06-11 | pre-SDD                                                                                                                                    |
| —       | core      | Formalización contexto negocio: domain-rules, reglas stack, sesión guiada                         | v1.0.0  | 2026-06-11 | pre-SDD                                                                                                                                    |
| —       | bootstrap | `install-agents.py`, `sync-cursor-rules.py`, adaptadores multi-agente                             | v1.0.0  | 2026-06-11 | pre-SDD                                                                                                                                    |
| —       | infra     | Optimización tokens reglas always-on (`TOKEN-OPTIMIZATION`)                                       | v1.0.0  | 2026-06-11 | pre-SDD                                                                                                                                    |
| —       | profiles  | Limpieza perfil laravel-voyager (sin dominio de negocio ajeno)                                    | v1.0.0  | 2026-06-11 | pre-SDD                                                                                                                                    |
| —       | docs      | Adopción SDD en el propio repositorio (Etapa 1 documentación)                                     | —       | 2026-06-12 | pre-SDD                                                                                                                                    |


## Descartado / en pausa


| ID  | Dominio | Título | Razón | Fecha | Spec |
| --- | ------- | ------ | ----- | ----- | ---- |
| —   | —       | —      | —     | —     | —    |


