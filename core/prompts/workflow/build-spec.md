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
  - guides/healthy-development.md
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

### Gate fail-closed (Plan mode / «te guío»)

**Señales** (cualquiera basta): Plan mode activo; el humano dijo «te guío» / «guiame» / «vamos paso a paso» / «no implementes aún»; o guía humana activa (iterar plan/Draft **sin** aprobar Ready).

| Contexto | Acción |
| -------- | ------ |
| Señal **y** sin frase de aprobación | **STOP.** No mutar cabecera/BACKLOG a Ready/In Build. Pedir frase explícita y esperar. |
| Señal **y** frase de aprobación | Permitido: Draft→Ready→In Build. |
| Sin señal | Contrato actual: frase o `build-spec` basta. |

Frases válidas (ej.): `apruebo SDD-NNN…`, `build-spec`, «apruebo para implementar». No bastan bajo señal: «sigue», «implementa el plan», «ok» ambiguo.

## Qué hará el agente

- Comprueba el gate fail-closed antes de cambiar estado.
- Actualiza cabecera y BACKLOG: **Ready** → **In Build** (si venía de Draft aprobado).
- Crea rama local según convención del perfil.
- Implementa según spec, `domain-rules.md` y checklist del stack.
- Ejecuta quality gates (tests, lint, build) en local.
- **No** hace `push`, **no** abre PR — eso es después de `verify-implementation`.

## Prompt

```
Apruebo e implementa el spec <SDD-NNN> según sdd-agent-workflow.

Instrucciones:
0. Gate fail-closed: si hay Plan mode / «te guío» / guía humana activa y no hay frase de aprobación explícita → STOP (no Ready/In Build); pedir frase y esperar. Si no hay esas señales, o hay frase (`apruebo…`, `build-spec`), continuar.
1. Si el spec está en Draft: actualiza a Ready (aprobación recibida) y luego In Build en spec y BACKLOG.
2. Crea rama local según guides/branching.md y perfil stack.
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
