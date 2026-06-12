---
id: update-submodule
title: Actualizar submodule sdd-kit
category: exceptions
adoption_stage: null
workflow_phase: null
when: Nueva versión del kit disponible; actualizar en proyecto consumidor
prerequisites:
  - sdd-kit/ como submodule
related:
  - INSTALL.md
tags: [maintenance, submodule]
human_approval: true
---

## Cuándo usarlo

Quieres actualizar el kit SDD en tu proyecto sin romper la instancia local en `.github/docs/sdd/`.

## Qué hará el agente

- Actualiza submodule a tag o commit indicado
- Compara cambios en core/templates con copia local
- Propone merge de archivos nuevos sin sobrescribir customizaciones
- Reinstala adaptadores de agente si cambió el manifest

## Prompt

```
Actualiza el submodule sdd-kit a la versión <TAG_O_COMMIT>.

Instrucciones:
1. git submodule update --remote sdd-kit (o checkout tag específico).
2. Compara sdd-kit/core/ con .github/docs/sdd/ — NO sobrescribir sin preguntar.
3. Si hay prompt-catalog.md o prompts/ nuevos, copiar solo lo faltante.
4. Ejecuta install-agents.py si cambió bootstrap/agent-prompts/.
5. Ejecuta validate-sdd y reporta diferencias.

Pide confirmación antes de sobrescribir archivos de la instancia SDD.
```

## Después de pegarlo

Revisa diff de adaptadores y docs. Commit del submodule por separado del código de features.

## Ver también

- [`INSTALL.md`](../../../INSTALL.md)
- [`agent-setup.md`](../../agent-setup.md)
