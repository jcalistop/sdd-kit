---
id: close-release
title: Cerrar release y archivar specs
category: workflow
adoption_stage: 2
workflow_phase: Released
when: PRs mergeados; listo para tag, release notes y archivado
prerequisites:
  - Specs en Validating mergeados
  - Versión objetivo definida (vX.Y.Z)
related:
  - releases/RUNBOOK.md
cli_alternative: sdd release close vX.Y.Z --changelog
tags: [release]
human_approval: true
---

## Cuándo usarlo

Cierre de entrega: archivar specs, actualizar BACKLOG, generar release notes y seguir RUNBOOK.

## Qué hará el agente

- Sigue `releases/RUNBOOK.md` Fase 0
- Archiva specs a `archive/<YYYY>/<dominio>/`
- Actualiza BACKLOG a Released
- Genera `releases/vX.Y.Z/release_vX.Y.Z.md` (acta de campaña SDD)
- Si el cierre es del **producto kit** (perfil `sdd-kit` o existe `docs/releases/` en la raíz): crea también la nota SemVer y enlaza desde el acta
- Verifica con `sdd release close` si está disponible

## Dual-release (solo producto kit)

Cuando el repositorio publica el kit como producto (dogfooding `sdd-kit` o capa `docs/releases/` presente):

| Artefacto | Ruta | Obligatorio |
| --------- | ---- | ----------- |
| Nota producto | `docs/releases/vX.Y.Z.md` + entrada en `docs/releases/CHANGELOG.md` | Sí |
| Acta campaña | `.github/docs/sdd/releases/vX.Y.Z/release_vX.Y.Z.md` | Sí |
| Enlace | Campo **Changelog kit** en el acta → nota producto | Sí |

- No duplicar narrativa larga: acta = resumen + specs/gates + enlace; detalle = nota producto.
- Consumidores leen solo `docs/releases/`.
- Instancias que no son el kit: solo acta en `paths.sdd/releases/` (sin `docs/releases/`).

## Prompt

```
Cierra la release <VERSION> (vX.Y.Z) según sdd-agent-workflow y RUNBOOK.

Instrucciones:
1. Lee releases/RUNBOOK.md y sdd.config.yaml (ramas, stack.profile).
2. Archiva specs mergeados: git mv a archive/<YYYY>/<dominio>/.
3. Actualiza BACKLOG a Released para cada SDD-NNN incluido.
4. Genera paths.sdd/releases/vX.Y.Z/release_vX.Y.Z.md con tabla de specs (o ID — documentado).
5. Si perfil es sdd-kit o existe docs/releases/ en la raíz del repo:
   a. Crea o actualiza docs/releases/vX.Y.Z.md (notas para consumidores).
   b. Añade entrada en docs/releases/CHANGELOG.md.
   c. En el acta, campo Changelog kit con enlace a docs/releases/vX.Y.Z.md.
6. Ejecuta sdd release close <VERSION> --changelog si CLI disponible.
7. Ejecuta validate-sdd; corrige WARN de dual-release si aparece.
8. Reporta pasos pendientes de deploy según perfil stack.

Pide confirmación antes de crear tag o push.
```

## Después de pegarlo

Revisa release notes y tabla de specs. Aprueba tag y deploy según perfil.

## Ver también

- [`releases/RUNBOOK.md`](../../releases/RUNBOOK.md)
- [`docs/README.md`](../../../docs/README.md) — contrato de capas (kit)
- `sdd release changelog`
