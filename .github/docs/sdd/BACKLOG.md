# Backlog SDD — SDD Kit

> Tablero operativo del repositorio **sdd-kit**. Plan estratégico histórico: [business/planning/ROADMAP.md](../../business/planning/ROADMAP.md).
> Adopción: [ADOPTION.md](ADOPTION.md) · Ciclo: [core/workflow.md](../../../core/workflow.md).

**Próximo ID disponible:** `SDD-014`.

**Versión acumulada del kit:** `v1.2.2` (ver [docs/releases/](../../../docs/releases/)).

---

## Discovery

| Dominio  | Idea / necesidad                                                    | Versión | Notas                                       |
| -------- | ------------------------------------------------------------------- | ------- | ------------------------------------------- |
| cli      | Suite pytest para la CLI (`backlog`, `prompts`, round-trip)         | —       | Prioridad media; CI hoy solo `compileall`   |
| docs     | Validación en producción: ciclo SDD con proyecto consumidor externo | —       | Dogfooding en repo ajeno                    |
| cli      | Dashboard Canvas de métricas SDD                                    | —       | Opcional; texto en SDD-013; Canvas aparte   |
| core     | Contrato safe-git agente — **SDD-007 en In Build**                  | v1.3.0  | Incidente consumidor 2026-06-17             |
| core     | Lenguaje guías/sensores (harness) en prompts del agente SDD — **SDD-008 en In Build** | v1.3.0  | Renombrar reglas y verificaciones como guides/sensors |
| docs     | Posicionar sdd-kit como agent harness en documentacion — **SDD-009 en In Build** | v1.3.0  | README.md, concepts.md, agent-setup.md                 |
| cli      | Observabilidad por componente en validate-sdd — **SDD-010 en In Build** | v1.3.0  | Reportar qué componente falló (spec, regla, perfil, dominio) |
| profiles | Perfiles adicionales (node-express, go-api, vue-vite) a demanda     | —       | Baja prioridad                              |

---

## Draft

| ID  | Dominio | Título | Versión | Spec |
| --- | ------- | ------ | ------- | ---- |
| —   | —       | —      | —       | —    |

## In Build

| ID      | Dominio | Título                                          | Versión | Spec                                                                              |
| ------- | ------- | ----------------------------------------------- | ------- | --------------------------------------------------------------------------------- |
| SDD-013 | cli     | Observabilidad de tokens (`sdd metrics tokens`) | v1.4.0  | [SDD-013](specs/cli/SDD-013-observabilidad-tokens-metrics.md) |
| SDD-010 | cli     | Observabilidad por componente validate-sdd | v1.3.0  | [SDD-010](specs/cli/SDD-010-observabilidad-componente-validate.md) |
| SDD-012 | core    | Governance de tokens en el harness (A–F)        | v1.3.0  | [SDD-012](specs/core/SDD-012-governance-tokens-harness.md) |
| SDD-009 | docs    | Posicionar sdd-kit como agent harness       | v1.3.0  | [SDD-009](specs/docs/SDD-009-posicionamiento-agent-harness.md) |
| SDD-008 | core    | Lenguaje guías/sensores (harness) en prompts    | v1.3.0  | [SDD-008](specs/core/SDD-008-lenguaje-harness-guides-sensors.md) |
| SDD-007 | core    | Contrato safe-git para agente (Git destructivo) | v1.3.0  | [SDD-007](specs/core/SDD-007-contrato-safe-git-agente.md)                       |
| SDD-011 | docs    | Contrato dual-release producto ↔ campaña        | v1.3.0  | [SDD-011](specs/docs/SDD-011-contrato-dual-release-producto-campana.md)           |

## Ready

| ID  | Dominio | Título | Versión | Spec |
| --- | ------- | ------ | ------- | ---- |
| —   | —       | —      | —       | —    |

## Validating

| ID  | Dominio | Título | Versión | Spec |
| --- | ------- | ------ | ------- | ---- |
| —   | —       | —      | —       | —    |

## Released

| ID      | Dominio   | Título                                                                                            | Versión | Fecha      | Spec archivado                                                                                                                   |
| ------- | --------- | ------------------------------------------------------------------------------------------------- | ------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------- |
| —       | bootstrap | Preservar bloque `kit` al reinstalar agent en `sdd.config.yaml`                                   | v1.2.1  | 2026-06-17 | —                                                                                                                                |
| SDD-006 | bootstrap | Optimización de tokens en reglas, skills y pipeline de generación del kit                         | v1.2.2  | 2026-07-14 | [archive/2026/bootstrap/SDD-006-optimizacion-tokens-kit.md](archive/2026/bootstrap/SDD-006-optimizacion-tokens-kit.md)           |
| SDD-005 | docs      | Reordenamiento documentación kit                                                                  | v1.2.0  | 2026-06-15 | [archive/2026/docs/SDD-005-reordenamiento-documentacion-kit.md](archive/2026/docs/SDD-005-reordenamiento-documentacion-kit.md)   |
| SDD-004 | bootstrap | Skills SDD en bootstrap (multi-agente)                                                            | v1.2.0  | 2026-06-15 | [archive/2026/bootstrap/SDD-004-agent-skills-cursor.md](archive/2026/bootstrap/SDD-004-agent-skills-cursor.md)                   |
| SDD-003 | core      | Refactor ciclo SDD: momentos semánticos vs prompts                                                | v1.1.0  | 2026-06-12 | [archive/2026/core/SDD-003-refactor-ciclo-sdd-prompts.md](archive/2026/core/SDD-003-refactor-ciclo-sdd-prompts.md)               |
| SDD-002 | bootstrap | Actualización del kit en instancias consumidoras                                                  | v1.1.0  | 2026-06-12 | [archive/2026/bootstrap/SDD-002-actualizacion-kit-instancias.md](archive/2026/bootstrap/SDD-002-actualizacion-kit-instancias.md) |
| SDD-001 | profiles  | Perfil `sdd-kit` para mantenedores                                                                | v1.1.0  | 2026-06-12 | [archive/2026/profiles/SDD-001-perfil-sdd-kit.md](archive/2026/profiles/SDD-001-perfil-sdd-kit.md)                               |
| —       | core      | Fundación agentica: `sdd-agent-workflow`, `adoption-guide`, `validate-sdd`, spec ejemplo Filament | v1.0.0  | 2026-06-11 | pre-SDD                                                                                                                          |
| —       | profiles  | Perfiles python-fastapi, react-vite, python-django, reports-latex-md                              | v1.0.0  | 2026-06-11 | pre-SDD                                                                                                                          |
| —       | cli       | CLI `sdd`, sync GitHub Issues, CHANGELOG automático, catálogo de prompts                          | v1.0.0  | 2026-06-11 | pre-SDD                                                                                                                          |
| —       | core      | Formalización contexto negocio: domain-rules, reglas stack, sesión guiada                         | v1.0.0  | 2026-06-11 | pre-SDD                                                                                                                          |
| —       | bootstrap | `install-agents.py`, `sync-cursor-rules.py`, adaptadores multi-agente                             | v1.0.0  | 2026-06-11 | pre-SDD                                                                                                                          |
| —       | infra     | Optimización tokens reglas always-on (`TOKEN-OPTIMIZATION`)                                       | v1.0.0  | 2026-06-11 | pre-SDD                                                                                                                          |
| —       | profiles  | Limpieza perfil laravel-voyager (sin dominio de negocio ajeno)                                    | v1.0.0  | 2026-06-11 | pre-SDD                                                                                                                          |
| —       | docs      | Adopción SDD en el propio repositorio (Etapa 1 documentación)                                     | —       | 2026-06-12 | pre-SDD                                                                                                                          |

## Descartado / en pausa

| Idea / ID | Razón | Fecha |
| --------- | ----- | ----- |
| —         | —     | —     |
