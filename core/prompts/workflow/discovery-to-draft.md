---
id: discovery-to-draft
title: Discovery → spec Draft
category: workflow
adoption_stage: 2
workflow_phase: Draft
when: Idea anotada en BACKLOG; listo para redactar spec
prerequisites:
  - Ítem en BACKLOG con estado Discovery
  - Dominio definido en sdd.config.yaml
related:
  - workflow.md#discovery
  - templates/spec-template.md
cli_alternative: sdd spec new --domain <DOMINIO> --title "<TITULO>"
tags: [spec, draft]
human_approval: false
---

## Cuándo usarlo

Tienes una iniciativa en **Discovery** y quieres que el agente cree el spec Draft. Si ya tienes `sdd-agent-workflow` instalado, basta con describir la idea; este prompt es útil para forzar el flujo explícitamente.

## Qué hará el agente

- Asigna ID global `SDD-NNN`
- Crea spec en `specs/<dominio>/` con plantilla adecuada (completa o simple)
- Actualiza BACKLOG a Draft
- Auto-verifica DoR antes de pedir revisión

## Prompt

```
Sigue sdd-agent-workflow: crea un spec Draft para esta iniciativa.

Idea: <DESCRIPCION_BREVE>
Dominio: <DOMINIO>
Tipo: <feature|bugfix|refactor|...>

Instrucciones:
1. Asigna SDD-NNN global y crea specs/<dominio>/SDD-NNN-slug.md.
2. Elige plantilla completa o simple según reglas de sdd-agent-workflow.
3. Completa DoR; cita reglas de business/domain-rules.md si aplican.
4. Actualiza BACKLOG.md a Draft.
5. Presenta el spec para mi revisión.
```

## Después de pegarlo

Revisa el spec Draft. Corrige alcance, exclusiones y criterios de aceptación antes de aprobar.

## Ver también

- [`workflow.md`](../../workflow.md) — Discovery / Draft
- `profiles/<perfil>/examples/SDD-001-*.md` — referencia de calidad
