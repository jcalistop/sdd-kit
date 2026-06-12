---
id: build-spec
title: Aprobar e implementar spec (local)
category: workflow
adoption_stage: 2
workflow_phase: In Build
when: Spec Draft cumple DoR y humano aprueba; o retomas implementación en curso
prerequisites:
  - Spec con Estado Draft (DoR completa) o Ready / In Build
related:
  - workflow.md#ready
  - workflow.md#in-build
  - healthy-development.md
tags: [spec, approval, implementation]
human_approval: true
deprecated_aliases:
  - approve-ready
  - implement-spec
---

## Cuándo usarlo

- Apruebas un spec Draft y autorizas implementación (**Ready** → **In Build**).
- Retomas la implementación de un spec ya en **Ready** o **In Build** en otra sesión.

No hace falta si el agente ya sigue `sdd-agent-workflow` en el mismo hilo: una frase de aprobación basta.

## Qué hará el agente

- Actualiza cabecera y BACKLOG: **Ready** → **In Build** (si venía de Draft aprobado).
- Crea rama local según convención del perfil.
- Implementa según spec, `domain-rules.md` y checklist del stack.
- Ejecuta quality gates (tests, lint, build) en local.
- **No** hace `push`, **no** abre PR — eso es después de `verify-implementation`.

## Prompt

```
Apruebo e implementa el spec <SDD-NNN> según sdd-agent-workflow.

Instrucciones:
1. Si el spec está en Draft: actualiza a Ready (aprobación recibida) y luego In Build en spec y BACKLOG.
2. Crea rama local según branching.md y perfil stack.
3. Implementa solo el alcance del spec; cambios fuera de alcance → actualizar spec primero.
4. Ejecuta quality gates del perfil en local.
5. NO hacer push ni abrir PR. Al terminar, indica que sigue verify-implementation.
```

## Después de pegarlo

Ejecuta o solicita `verify-implementation` antes de cualquier publicación en Git.

## Ver también

- [`workflow.md`](../../workflow.md) — orden local vs Git compartido
- `sdd prompt show verify-implementation`
- _Deprecado:_ `approve-ready`, `implement-spec` — usar este prompt
