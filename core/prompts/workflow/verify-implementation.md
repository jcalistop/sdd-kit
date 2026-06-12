---
id: verify-implementation
title: Verificar implementación vs spec (antes de Git)
category: workflow
adoption_stage: 2
workflow_phase: In Build
when: Código listo y quality gates en verde; antes de push o PR
prerequisites:
  - Spec en In Build
  - Quality gates del perfil stack en verde (local)
related:
  - workflow.md#verificación-local-antes-de-git-compartido
  - sdd-workflow-reference.mdc
tags: [verification, dor, dod]
human_approval: true
---

## Cuándo usarlo

Gate **obligatorio** entre implementación local y publicación en Git. Cruza lo construido contra el spec, reglas de negocio y arquitectura sana.

## Qué hará el agente

- Verifica criterios de aceptación (happy + error path) del spec.
- Cruza `business/domain-rules.md` (o documenta No aplica).
- Ejecuta checklist de arquitectura sana (`healthy-development.md`).
- Presenta evidencia numerada (comandos, salidas, pasos manuales).
- **No** hace `push` ni abre PR si hay ítems pendientes.
- Si todo OK, indica que puede proceder `open-pr`.

## Prompt

```
Verifica la implementación del spec <SDD-NNN> antes de publicar en Git.

Instrucciones:
1. Lee specs/<dominio>/SDD-NNN-*.md, business/domain-rules.md y sdd-workflow-reference (verificación post-implementación).
2. Cruza cada criterio de aceptación (happy + error) con evidencia concreta.
3. Verifica reglas de domain-rules aplicables.
4. Ejecuta checklist de arquitectura sana; reporta señales con opciones.
5. Lista ítems pendientes numerados. Si hay pendientes: NO push ni PR.
6. Si todo OK: resume evidencia y confirma que puede abrirse PR (open-pr).
```

## Después de pegarlo

Si la verificación pasa, usa `open-pr` o pide al agente publicar. El siguiente hito humano es revisar el PR antes de merge (`validate-pr` o frase equivalente).

## Ver también

- [`workflow.md`](../../workflow.md)
- `sdd prompt show open-pr`
