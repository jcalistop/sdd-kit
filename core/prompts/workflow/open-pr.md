---
id: open-pr
title: Abrir PR con checklist SDD
category: workflow
adoption_stage: 2
workflow_phase: Validating
when: verify-implementation OK; falta publicar en Git (commit, push, PR)
prerequisites:
  - verify-implementation completado en verde
  - Quality gates en verde
related:
  - checklist-pr.md
  - profiles/<stack>/checklist-stack.md
  - prompts/workflow/verify-implementation.md
tags: [pr]
human_approval: false
---

## Cuándo usarlo

**Solo después de `verify-implementation` en verde.** Publica el trabajo local en el remoto con trazabilidad SDD. Un PR puede referenciar varios `SDD-NNN` (ver `workflow.md`).

## Qué hará el agente

- Commit de entrega, `push` y PR hacia rama de desarrollo (según `sdd.config.yaml`)
- Completa checklist core + perfil stack
- Referencia cada `SDD-NNN` y evidencia de verify + tests
- Actualiza spec(s) y BACKLOG a Validating

## Prompt

```
Abre PR para el spec <SDD-NNN> (o specs <SDD-NNN>, <SDD-MMM>).

Instrucciones:
1. Confirma que verify-implementation ya pasó en verde. Si no, detente y ejecuta verify primero.
2. Commit de entrega, push y PR hacia la rama de desarrollo en sdd.config.yaml.
3. Completa checklist-pr.md y checklist-stack del perfil en la descripción.
4. Referencia cada SDD-NNN, criterios cubiertos y evidencia de verify + tests.
5. Actualiza spec(s) y BACKLOG a Validating.
```

## Después de pegarlo

Revisa el PR con `validate-pr` o frase equivalente antes de mergear.

## Ver también

- [`checklist-pr.md`](../../checklist-pr.md)
- `sdd prompt show verify-implementation`
- `sdd prompt show validate-pr`
