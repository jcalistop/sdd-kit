---
id: validate-pr
title: Validar PR antes de merge (DoD)
category: workflow
adoption_stage: 2
workflow_phase: Validating
when: PR abierto; humano revisa antes de merge
prerequisites:
  - PR en estado Validating
  - Spec SDD-NNN vinculado
related:
  - workflow.md#definition-of-done-dod--proceso
  - checklist-pr.md
tags: [pr, dod, review]
human_approval: true
---

## Cuándo usarlo

Antes de mergear, quieres que el agente verifique DoD y presente evidencia para tu decisión final.

## Qué hará el agente

- Cruza spec, PR y checklist DoD
- Lista ítems pendientes o riesgos
- No mergea sin tu autorización explícita

## Prompt

```
Valida el PR del spec <SDD-NNN> contra Definition of Done.

Instrucciones:
1. Lee el PR, specs/<dominio>/SDD-NNN-*.md y checklist-pr.md + perfil stack.
2. Verifica quality gates, criterios de aceptación, trazabilidad y reglas de domain-rules.md.
3. Lista ítems pendientes numerados.
4. NO hacer merge sin mi autorización explícita.
```

## Después de pegarlo

Si todo está OK, autoriza merge. Tras merge, coordina cierre de release con `close-release`.

## Ver también

- [`workflow.md`](../../workflow.md) — DoD
- [`releases/RUNBOOK.md`](../../releases/RUNBOOK.md)
