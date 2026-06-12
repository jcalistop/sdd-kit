---
id: implement-spec
title: Implementar spec aprobado
category: workflow
adoption_stage: 2
workflow_phase: In Build
when: Spec en Ready o In Build; implementación en curso
prerequisites:
  - Spec con Estado Ready o In Build
  - Rama de feature creada
related:
  - workflow.md#in-build
  - healthy-development.md
tags: [implementation]
human_approval: false
---

## Cuándo usarlo

El spec ya está aprobado y quieres que el agente continúe o retome la implementación sin redefinir alcance.

## Qué hará el agente

- Implementa según spec y perfil stack
- Ejecuta quality gates (tests, lint, build)
- Prepara evidencia para PR

## Prompt

```
Implementa el spec <SDD-NNN> según sdd-agent-workflow.

Instrucciones:
1. Lee specs/<dominio>/SDD-NNN-*.md, business/domain-rules.md y checklist del perfil stack.
2. Mantén estado In Build en spec y BACKLOG.
3. Implementa solo lo del alcance; cambios fuera de alcance → actualizar spec primero.
4. Ejecuta quality gates del perfil (tests, lint, build).
5. Cuando esté listo, prepara PR con checklist core + stack.
```

## Después de pegarlo

Revisa el PR cuando el agente lo abra. No merges sin validar DoD.

## Ver también

- [`healthy-development.md`](../../healthy-development.md)
- `sdd prompt show open-pr`
