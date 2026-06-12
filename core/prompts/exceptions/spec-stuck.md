---
id: spec-stuck
title: Spec estancado o rechazado
category: exceptions
adoption_stage: 2
workflow_phase: null
when: Spec sin avance >2 semanas o humano rechazó el Draft
prerequisites:
  - Spec SDD-NNN existente
related:
  - workflow.md#revision-semanal-30-min
  - adoption-guide.md
tags: [exception, replanning]
human_approval: true
---

## Cuándo usarlo

Un spec lleva demasiado tiempo en el mismo estado, fue rechazado, o el alcance cambió por completo.

## Qué hará el agente

- Diagnostica causa (alcance, dependencias, DoR incompleta)
- Propone replanificar, dividir en sub-specs, pausar o descartar
- Actualiza BACKLOG con razón y fecha si aplica

## Prompt

```
El spec <SDD-NNN> está estancado o fue rechazado. Ayúdame a replanificar.

Contexto: <MOTIVO_RECHAZO_O_ESTANCAMIENTO>

Instrucciones:
1. Lee specs/<dominio>/SDD-NNN-*.md y entrada en BACKLOG.md.
2. Diagnostica causa (alcance, dependencias, DoR, prioridad).
3. Propón opciones: corregir Draft, dividir (00/01), pausar en BACKLOG, o descartar con razón.
4. NO pasar a Ready ni implementar sin mi decisión explícita.
```

## Después de pegarlo

Elige una opción y confirma cambios en spec o BACKLOG.

## Ver también

- [`workflow.md`](../../workflow.md) — Revisión semanal
- [`operations.md`](../../operations.md)
