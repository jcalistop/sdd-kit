---
id: open-pr
title: Abrir PR con checklist SDD
category: workflow
adoption_stage: 2
workflow_phase: In Build
when: Implementación lista; falta PR hacia rama de desarrollo
prerequisites:
  - Código implementado según spec
  - Quality gates en verde
related:
  - checklist-pr.md
  - profiles/<stack>/checklist-stack.md
tags: [pr]
human_approval: false
---

## Cuándo usarlo

La implementación está lista y necesitas un PR con trazabilidad SDD completa.

## Qué hará el agente

- Abre PR hacia rama de desarrollo (según `sdd.config.yaml`)
- Completa checklist core + perfil stack
- Referencia SDD-NNN y evidencia de tests
- Actualiza spec y BACKLOG a Validating

## Prompt

```
Abre PR para el spec <SDD-NNN>.

Instrucciones:
1. Verifica quality gates del perfil stack en verde.
2. Abre PR hacia la rama de desarrollo configurada en sdd.config.yaml.
3. Completa checklist-pr.md y checklist-stack del perfil en la descripción.
4. Referencia SDD-NNN, criterios de aceptación cubiertos y evidencia de tests.
5. Actualiza spec y BACKLOG a Validating.
```

## Después de pegarlo

Revisa el PR con `validate-pr` antes de mergear.

## Ver también

- [`checklist-pr.md`](../../checklist-pr.md)
- `sdd prompt show validate-pr`
