---
id: approve-ready
title: Aprobar spec → Ready → In Build
category: workflow
adoption_stage: 2
workflow_phase: Ready
when: Spec Draft cumple DoR; humano aprueba para implementar
prerequisites:
  - Spec Draft revisado y DoR completa
related:
  - workflow.md#ready
tags: [spec, approval]
human_approval: true
---

## Cuándo usarlo

Apruebas el spec y autorizas que el agente pase a **Ready** e inicie implementación (**In Build**).

## Qué hará el agente

- Actualiza cabecera del spec y BACKLOG a Ready, luego In Build
- Crea rama según convención del perfil
- Comienza implementación según spec y checklist del stack

## Prompt

```
Apruebo el spec <SDD-NNN> para implementación.

Instrucciones:
1. Actualiza estado del spec y BACKLOG: Ready → In Build.
2. Crea rama según branching.md y perfil stack.
3. Implementa según el spec; aplica healthy-development.md y reglas del perfil.
4. No ampliar alcance sin actualizar el spec primero.
```

## Después de pegarlo

Supervisa la implementación. El siguiente hito humano es revisar el PR (`validate-pr`).

## Ver también

- [`workflow.md`](../../workflow.md) — Ready / In Build
- [`branching.md`](../../branching.md)
