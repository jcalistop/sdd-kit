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
- Genera `releases/vX.Y.Z/release_vX.Y.Z.md`
- Verifica con `sdd release close` si está disponible

## Prompt

```
Cierra la release <VERSION> (vX.Y.Z) según sdd-agent-workflow y RUNBOOK.

Instrucciones:
1. Lee releases/RUNBOOK.md y sdd.config.yaml (ramas).
2. Archiva specs mergeados: git mv a archive/<YYYY>/<dominio>/.
3. Actualiza BACKLOG a Released para cada SDD-NNN incluido.
4. Genera releases/vX.Y.Z/release_vX.Y.Z.md con tabla de specs (o ID — documentado).
5. Ejecuta sdd release close <VERSION> --changelog si CLI disponible.
6. Reporta pasos pendientes de deploy según perfil stack.

Pide confirmación antes de crear tag o push.
```

## Después de pegarlo

Revisa release notes y tabla de specs. Aprueba tag y deploy según perfil.

## Ver también

- [`releases/RUNBOOK.md`](../../releases/RUNBOOK.md)
- `sdd release changelog`
