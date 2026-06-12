# Backlog SDD — SDD Kit

> Tablero operativo del repositorio **sdd-kit**. Plan estratégico histórico: [docs/maintainers/ROADMAP.md](../../../docs/maintainers/ROADMAP.md).
> Adopción: [ADOPTION.md](ADOPTION.md) · Ciclo: [core/workflow.md](../../../core/workflow.md).

**Próximo ID disponible:** `SDD-003`.

**Versión acumulada del kit:** `v1.0.0` (ver [docs/releases/](../../../docs/releases/)).

---

## Discovery

| Dominio  | Idea / necesidad                                                    | Versión | Notas                                       |
| -------- | ------------------------------------------------------------------- | ------- | ------------------------------------------- |
| cli      | Suite pytest para la CLI (`backlog`, `prompts`, round-trip)         | —       | Prioridad media; CI hoy solo `compileall`   |
| docs     | Validación en producción: ciclo SDD con proyecto consumidor externo | —       | Dogfooding en repo ajeno                    |
| cli      | Dashboard Canvas de métricas SDD                                    | —       | Opcional; `sdd metrics` cubre reporte texto |
| profiles | Perfiles adicionales (node-express, go-api, vue-vite) a demanda     | —       | Baja prioridad                              |

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

| ID  | Dominio | Título | Versión | Spec |
| --- | ------- | ------ | ------- | ---- |
| —   | —       | —      | —       | —    |

## Validating

| ID      | Dominio   | Título                                           | Versión | Spec                                                                                                               |
| ------- | --------- | ------------------------------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------ |
| SDD-002 | bootstrap | Actualización del kit en instancias consumidoras | v1.1.0  | [specs/bootstrap/SDD-002-actualizacion-kit-instancias.md](specs/bootstrap/SDD-002-actualizacion-kit-instancias.md) |

## Released

| ID      | Dominio   | Título                                                                                            | Versión | Fecha      | Spec archivado                                                                                     |
| ------- | --------- | ------------------------------------------------------------------------------------------------- | ------- | ---------- | -------------------------------------------------------------------------------------------------- |
| SDD-001 | profiles  | Perfil `sdd-kit` para mantenedores                                                                | v1.1.0  | 2026-06-12 | [archive/2026/profiles/SDD-001-perfil-sdd-kit.md](archive/2026/profiles/SDD-001-perfil-sdd-kit.md) |
| —       | core      | Fundación agentica: `sdd-agent-workflow`, `adoption-guide`, `validate-sdd`, spec ejemplo Filament | v1.0.0  | 2026-06-11 | pre-SDD                                                                                            |
| —       | profiles  | Perfiles python-fastapi, react-vite, python-django, reports-latex-md                              | v1.0.0  | 2026-06-11 | pre-SDD                                                                                            |
| —       | cli       | CLI `sdd`, sync GitHub Issues, CHANGELOG automático, catálogo de prompts                          | v1.0.0  | 2026-06-11 | pre-SDD                                                                                            |
| —       | core      | Formalización contexto negocio: domain-rules, reglas stack, sesión guiada                         | v1.0.0  | 2026-06-11 | pre-SDD                                                                                            |
| —       | bootstrap | `install-agents.py`, `sync-cursor-rules.py`, adaptadores multi-agente                             | v1.0.0  | 2026-06-11 | pre-SDD                                                                                            |
| —       | infra     | Optimización tokens reglas always-on (`TOKEN-OPTIMIZATION`)                                       | v1.0.0  | 2026-06-11 | pre-SDD                                                                                            |
| —       | profiles  | Limpieza perfil laravel-voyager (sin dominio de negocio ajeno)                                    | v1.0.0  | 2026-06-11 | pre-SDD                                                                                            |
| —       | docs      | Adopción SDD en el propio repositorio (Etapa 1 documentación)                                     | —       | 2026-06-12 | pre-SDD                                                                                            |

## Descartado / en pausa

| Idea / ID | Razón | Fecha |
| --------- | ----- | ----- |
| —         | —     | —     |
