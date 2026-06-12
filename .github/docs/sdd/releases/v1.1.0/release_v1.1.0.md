# Release v1.1.0 — SDD Kit (instancia)

> Cierre documental Fase 0 — campaña v1.1.0. PR de campaña: [#1](https://github.com/jcalistop/sdd-kit/pull/1) (mergeado).

---

## Cabecera

| Campo           | Valor      |
| --------------- | ---------- |
| **Versión**     | v1.1.0     |
| **Fecha**       | 2026-06-12 |
| **Tipo**        | menor      |
| **Responsable** | mantenedor |

---

## Información general

### En qué consiste esta versión

Primera campaña de release con SDD operativo en el propio repositorio: perfil para mantenedores, flujo de actualización en instancias consumidoras y refactor del ciclo SDD (momentos semánticos vs prompts).

### Novedades visibles

- Runbook `core/upgrade-guide.md` y prompt `upgrade-kit`
- `kit.installed_version` y `UPGRADE-LOG.md` en instancias
- Perfil `profiles/sdd-kit/` para dogfooding
- `validate-sdd` advierte si la versión registrada difiere del kit en disco
- Prompt `verify-implementation` — gate obligatorio antes de push/PR
- Prompt `build-spec` — fusiona `approve-ready` + `implement-spec`
- Diagramas de secuencia Mermaid del ciclo humano–agente

### Limitaciones o pendientes

- CLI `sdd upgrade` con merge automático no incluido (backlog futuro)

---

## Información técnica

### Resumen técnico

Cambios en `core/`, `bootstrap/`, `profiles/sdd-kit/` y documentación de adopción. Sin cambios en perfiles de stacks consumidores.

### Specs incluidos

| ID      | Dominio   | Tipo     | Título                                             | Spec archivado                                                                                                                         |
| ------- | --------- | -------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| SDD-001 | profiles  | feature  | Perfil `sdd-kit` para mantenedores                 | [archive/2026/profiles/SDD-001-perfil-sdd-kit.md](../../archive/2026/profiles/SDD-001-perfil-sdd-kit.md)                               |
| SDD-002 | bootstrap | feature  | Actualización del kit en instancias consumidoras   | [archive/2026/bootstrap/SDD-002-actualizacion-kit-instancias.md](../../archive/2026/bootstrap/SDD-002-actualizacion-kit-instancias.md) |
| SDD-003 | core      | refactor | Refactor ciclo SDD: momentos semánticos vs prompts | [archive/2026/core/SDD-003-refactor-ciclo-sdd-prompts.md](../../archive/2026/core/SDD-003-refactor-ciclo-sdd-prompts.md)               |

Cambios sin spec en esta versión: ver entradas ID `—` en BACKLOG Released (pre-SDD v1.0.0).

### ADRs incluidos

| ID  | Estado | Impacto |
| --- | ------ | ------- |
| —   | —      | —       |

### Cambio de esquema / datos

No aplica — producto de metodología y tooling.

### Despliegue

### Publicación (SDD Kit)

Versión del **producto kit** — no confundir con releases de iniciativas en `.github/docs/sdd/releases/`.

- [ ] CI GitHub en verde para el commit etiquetado
- [ ] `validate-sdd` en verde sobre `.github/docs/sdd/`
- [ ] Nota `docs/releases/v1.1.0.md` actualizada
- [ ] CHANGELOG actualizado
- [ ] Tag `v1.1.0` creado y GitHub Release publicada
- [ ] Specs de la versión archivados en `.github/docs/sdd/archive/` si aplica

### Validación post-publicación

- [ ] Tag y release visibles en GitHub
- [ ] README e INSTALL coherentes con la versión
- [ ] Sin breaking changes sin documentar en notas de release

### Validación post-despliegue

- [ ] Smoke según perfil stack
- [ ] Logs sin errores nuevos

### Riesgos residuales

Consumidores sin submodule deben seguir el runbook manual para detectar versión. Prompts deprecados (`approve-ready`, `implement-spec`) requieren migración a `build-spec`.

### Rollback

Fijar submodule al tag `v1.0.0`; revertir `kit.installed_version` en instancia.
