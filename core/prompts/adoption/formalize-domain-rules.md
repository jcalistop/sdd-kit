---
id: formalize-domain-rules
title: Formalizar contexto de negocio (domain-rules)
category: adoption
adoption_stage: 1
workflow_phase: null
when: Antes del primer spec no trivial; domain-rules.md en estado plantilla
prerequisites:
  - business/domain-rules.md existe (puede ser plantilla)
related:
  - adoption-guide.md#formalizar-el-contexto-de-negocio
  - templates/business-domain-template.md
tags: [onboarding, business-context]
human_approval: true
---

## Cuándo usarlo

El agente necesita reglas explícitas en `business/domain-rules.md` para no inventar restricciones ni omitir las que conoces.

## Qué hará el agente

- Detecta si `domain-rules.md` está en estado plantilla
- Hace las preguntas de la sesión guiada (roles, filtros, invariantes)
- Redacta `domain-rules.md` y actualiza `business/README.md`
- Pide tu aprobación antes de continuar con specs

## Prompt

```
Formaliza el contexto de negocio de este proyecto.

Instrucciones:
1. Lee business/domain-rules.md y detecta si está en estado plantilla.
2. Hazme las preguntas de sdd-kit/core/templates/business-domain-template.md (sesión guiada).
3. Con mis respuestas, redacta business/domain-rules.md y actualiza business/README.md.
4. Pide mi aprobación antes de crear specs.

No asumas reglas de negocio no documentadas. Si pospongo, registra nota en BACKLOG.
```

## Después de pegarlo

Responde las preguntas del agente con el detalle que tengas. Revisa y aprueba los archivos generados antes del primer spec.

## Ver también

- [`adoption-guide.md`](../../adoption-guide.md) — Formalizar contexto de negocio
- [`templates/business-domain-template.md`](../../templates/business-domain-template.md)
