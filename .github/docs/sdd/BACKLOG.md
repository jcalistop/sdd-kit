# Backlog SDD — SDD Kit

> Tablero operativo del repositorio **sdd-kit**. Plan estratégico histórico: [business/planning/ROADMAP.md](../../business/planning/ROADMAP.md).
> Adopción: [ADOPTION.md](ADOPTION.md) · Ciclo: [core/workflow.md](../../../core/workflow.md).

**Próximo ID disponible:** `SDD-024`.

**Versión acumulada del kit:** `v1.4.1` (ver [docs/releases/](../../../docs/releases/)).

---

## Discovery

> **Versión (recomendación SemVer):** bump de producto kit al cerrar la iniciativa, desde `v1.4.1`. Criterio auditoría: **patch** = higiene/docs/CI sin API nueva; **minor** = capacidad o perfil nuevo backward-compatible; **major** = ruptura para consumidores (ninguna fila actual); **—** = no define release del kit por sí sola.
>
> Dogfood externo **cerrado** (2026-09-10): [plan](audits/20260906-dogfood-consumidor-externo.md) · [informe](audits/20260906-dogfood-consumidor-externo-informe.md) (`minsal-centinela` / `v1.4.1`). Gaps abajo.

| Dominio   | Idea / necesidad                                                                 | Versión | Notas                                                                 |
| --------- | -------------------------------------------------------------------------------- | ------- | --------------------------------------------------------------------- |
| core      | Draft/DoR: sección opcional «Congelado para implementación» (API, tests, lectura máx.) | patch   | Dogfood gap #3 P1; specs flojos para LLM de bajo contexto             |
| profiles  | verify: tabla perfil → comandos obligatorios (Pint=CI, tests, `npm audit` si tocó JS) | patch   | Dogfood gap #4 P1                                                     |
| docs      | Runbook dogfood: stub del tag no es fuente de verdad; checklist merge informe → main | patch   | Dogfood gap #5 P2                                                     |
| bootstrap | Skills: `{{STACK_PROFILE}}` en install; no hardcodear perfil ajeno en skill global | patch   | Dogfood gap #7 P2                                                     |
| bootstrap | build-spec fail-closed: no Ready/In Build sin frase humana si hay Plan mode / «te guío» | patch   | Dogfood gap #6 P2                                                     |

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

| ID      | Dominio   | Título                                                           | Versión | Spec |
| ------- | --------- | ---------------------------------------------------------------- | ------- | ---- |
| SDD-023 | bootstrap | install-agents: branching mode + precedencia instancia > global  | v1.5.0  | [specs/bootstrap/SDD-023-install-agents-branching-precedencia.md](specs/bootstrap/SDD-023-install-agents-branching-precedencia.md) |
| SDD-022 | profiles  | Pint local = comando CI (voyager + filament)                     | v1.4.2  | [specs/profiles/SDD-022-pint-parity-ci-laravel.md](specs/profiles/SDD-022-pint-parity-ci-laravel.md) |

## Validating

| ID  | Dominio | Título | Versión | Spec |
| --- | ------- | ------ | ------- | ---- |
| —   | —       | —      | —       | —    |


## Released


| ID      | Dominio   | Título                                                                                            | Versión | Fecha      | Spec archivado                                                                                                                             |
| ------- | --------- | ------------------------------------------------------------------------------------------------- | ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| SDD-021 | docs      | Índice artefactos paths.sdd (audits/research) + banner ANALYSIS                                   | v1.4.1  | 2026-09-06 | [archive/2026/docs/SDD-021-indice-audits-research-banner-analysis.md](archive/2026/docs/SDD-021-indice-audits-research-banner-analysis.md) |
| SDD-020 | bootstrap | Upgrade / paridad multi-agente (wording, targets, safe-git doc)                                   | v1.4.1  | 2026-09-06 | [archive/2026/bootstrap/SDD-020-upgrade-paridad-multi-agente.md](archive/2026/bootstrap/SDD-020-upgrade-paridad-multi-agente.md)           |
| SDD-019 | infra     | CI: `sdd validate` y gatillo en rama `dev`                                                        | v1.4.1  | 2026-09-06 | [archive/2026/infra/SDD-019-ci-validate-sdd-rama-dev.md](archive/2026/infra/SDD-019-ci-validate-sdd-rama-dev.md)                           |
| SDD-018 | bootstrap | Higiene agentica: retirar `sdd-core.mdc` residual + alinear docs                                  | v1.4.1  | 2026-09-06 | [archive/2026/bootstrap/SDD-018-higiene-agentica-sdd-core.md](archive/2026/bootstrap/SDD-018-higiene-agentica-sdd-core.md)                 |
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


| ID  | Dominio  | Título                                                              | Razón                                      | Fecha      | Spec |
| --- | -------- | ------------------------------------------------------------------- | ------------------------------------------ | ---------- | ---- |
| —   | profiles | Perfiles adicionales (node-express, go-api, vue-vite) a demanda     | En pausa — baja prioridad; retomar a demanda | 2026-09-10 | —    |


