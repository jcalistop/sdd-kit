---
id: draft-review
title: Revisar spec Draft (DoR)
category: workflow
adoption_stage: 2
workflow_phase: Draft
when: Spec Draft creado; quieres verificación DoR antes de aprobar
prerequisites:
  - Spec en specs/<dominio>/SDD-NNN-*.md con Estado Draft
related:
  - workflow.md#definition-of-ready-dor
tags: [spec, dor]
human_approval: true
---

## Cuándo usarlo

El spec está en Draft y quieres que el agente auto-verifique Definition of Ready y presente gaps antes de tu aprobación.

## Qué hará el agente

- Revisa checklist DoR del workflow
- Lista ítems faltantes o ambiguos
- Propone correcciones sin pasar a Ready hasta tu OK

## Prompt

```
Revisa el spec Draft <SDD-NNN> contra Definition of Ready.

Instrucciones:
1. Lee specs/<dominio>/SDD-NNN-*.md y workflow.md (DoR).
2. Verifica tipo, dominio, alcance, exclusiones, impacto técnico, criterios de aceptación, riesgos.
3. Lista gaps o ambigüedades numeradas.
4. Propón correcciones; NO cambiar estado a Ready sin mi aprobación explícita.
```

## Después de pegarlo

Aprueba correcciones o pide ajustes. Cuando el DoR esté completo, usa `approve-ready`.

## Ver también

- [`workflow.md`](../../workflow.md) — DoR
- `sdd prompt show approve-ready`
