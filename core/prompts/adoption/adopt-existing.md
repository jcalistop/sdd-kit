---
id: adopt-existing
title: Adoptar SDD en proyecto existente
category: adoption
adoption_stage: 1
workflow_phase: null
when: Repo con código y documentación previa; submodule ya añadido
prerequisites:
  - sdd-kit/ como submodule
  - Perfil elegido
related:
  - adoption-guide.md#etapa-1
  - agent-setup.md
cli_alternative: null
tags: [onboarding, existing-project]
human_approval: true
---

## Cuándo usarlo

Proyecto **existente** con código en marcha. **No ejecutes `init-sdd` manualmente** sin contexto; el agente lee lo que ya hay y no sobrescribe sin confirmación.

## Qué hará el agente

- Lee documentación y estructura actual del proyecto
- Ejecuta `init-sdd` solo si no existe `.github/docs/sdd/`
- Completa config, business y BACKLOG (inventario pre-SDD con ID `—`)
- Instala adaptadores y valida con `validate-sdd`
- Propone 3–5 ítems Discovery reales

## Prompt

```
Adopta SDD en este proyecto con perfil <PERFIL>.

Contexto:
- Proyecto EXISTENTE con código y posible documentación previa.
- El kit está en sdd-kit/ (submodule).

Instrucciones:
1. Lee sdd-kit/core/adoption-guide.md (Etapa 1) y sdd-kit/core/agent-setup.md.
2. Ejecuta init-sdd solo si no existe .github/docs/sdd/; si ya existe, NO sobrescribas archivos sin preguntar.
3. Completa sdd.config.yaml, business/README.md y BACKLOG (inventario pre-SDD con ID —, sin specs retrospectivos).
4. Instala adaptadores de agente (-Agent auto).
5. Ejecuta validate-sdd y reporta resultado.
6. Propón 3–5 ítems en Discovery para el backlog real.

No reescribir el pasado. No crear specs para features ya implementadas.
```

## Después de pegarlo

Aprueba cambios en archivos existentes antes de que el agente los sobrescriba. Revisa el inventario pre-SDD y los ítems Discovery propuestos.

## Ver también

- [`adoption-guide.md`](../../adoption-guide.md) — Etapa 1
- [`INSTALL.md`](../../../INSTALL.md) — Modo agente
