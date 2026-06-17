# Backlog SDD — SDD Kit

> Tablero operativo del repositorio **sdd-kit**. Plan estratégico histórico: [business/planning/ROADMAP.md](../../business/planning/ROADMAP.md).
> Adopción: [ADOPTION.md](ADOPTION.md) · Ciclo: [core/workflow.md](../../../core/workflow.md).

**Próximo ID disponible:** `SDD-006`.

**Versión acumulada del kit:** `v1.2.1` (ver [docs/releases/](../../../docs/releases/)).

---

## Discovery

| Dominio  | Idea / necesidad                                                    | Versión | Notas                                       |
| -------- | ------------------------------------------------------------------- | ------- | ------------------------------------------- |
| cli      | Suite pytest para la CLI (`backlog`, `prompts`, round-trip)         | —       | Prioridad media; CI hoy solo `compileall`   |
| docs     | Validación en producción: ciclo SDD con proyecto consumidor externo | —       | Dogfooding en repo ajeno                    |
| cli      | Dashboard Canvas de métricas SDD                                    | —       | Opcional; `sdd metrics` cubre reporte texto |
| profiles | Perfiles adicionales (node-express, go-api, vue-vite) a demanda     | —       | Baja prioridad                              |

---

## In Build

_(vacío)_

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
