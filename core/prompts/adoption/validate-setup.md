---
id: validate-setup
title: Validar instalación SDD (Etapa 1)
category: adoption
adoption_stage: 1
workflow_phase: null
when: Tras completar estructura mínima; antes del primer spec
prerequisites:
  - Instancia SDD creada (.github/docs/sdd/)
related:
  - adoption-guide.md#checklist-etapa-1
cli_alternative: sdd validate
tags: [onboarding, validation]
human_approval: false
---

## Cuándo usarlo

Después de bootstrap o adopción manual, para confirmar que la estructura documental está coherente.

## Qué hará el agente

- Ejecuta `validate-sdd` (o `sdd validate`)
- Reporta errores críticos y advertencias
- Propone correcciones concretas si falla

## Prompt

```
Valida la instalación SDD de este proyecto.

Instrucciones:
1. Ejecuta `python sdd-kit/cli/sdd.py validate` (o scripts legacy `validate-sdd.sh` / `.ps1`).
2. Reporta errores críticos y advertencias con rutas de archivo.
3. Si hay fallos, propón correcciones mínimas (sin sobrescribir sin confirmación).
4. Verifica que existan adaptadores de agente según sdd.config.yaml → agent.targets.

No avanzar a specs hasta que validate-sdd pase sin errores críticos.
```

## Después de pegarlo

Corrige errores críticos antes de crear el primer spec. Las advertencias puedes priorizarlas según contexto.

## Ver también

- [`adoption-guide.md`](../../adoption-guide.md) — Checklist Etapa 1
