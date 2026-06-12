---
id: update-submodule
title: Actualizar submodule sdd-kit (legacy)
category: exceptions
adoption_stage: null
workflow_phase: null
when: Atajo rápido; preferir upgrade-kit para flujo completo con trazabilidad
prerequisites:
  - sdd-kit/ como submodule
related:
  - upgrade-guide.md
  - upgrade-kit.md
  - INSTALL.md
tags: [maintenance, submodule]
human_approval: true
---

## Cuándo usarlo

Alias breve. Para upgrades con registro de versión, log y checklist completo usa **`upgrade-kit`**.

## Qué hará el agente

Redirige al flujo de [`upgrade-kit.md`](upgrade-kit.md) o ejecuta los pasos mínimos del submodule.

## Prompt

```
Usa el prompt upgrade-kit para actualizar el kit SDD a <VERSION>.
Si solo necesitas el submodule: git -C sdd-kit fetch --tags && git -C sdd-kit checkout <VERSION>.
Luego sigue upgrade-guide.md para merge de instancia y validate-sdd.
```

## Ver también

- [`upgrade-kit.md`](upgrade-kit.md) — **recomendado**
- [`upgrade-guide.md`](../../upgrade-guide.md)
- [`INSTALL.md`](../../../INSTALL.md)
