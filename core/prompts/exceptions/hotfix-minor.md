---
id: hotfix-minor
title: Hotfix urgente o cambio trivial (sin spec)
category: exceptions
adoption_stage: 2
workflow_phase: null
when: Bug crítico en producción o cambio menor (typo, copy, bump deps)
prerequisites:
  - Cambio no requiere spec según workflow.md
related:
  - workflow.md#hotfix
  - branching.md
tags: [hotfix, exception]
human_approval: true
---

## Cuándo usarlo

Urgencia extrema o cambio tan pequeño que no justifica spec. Se registra en release con ID `—`.

## Qué hará el agente

- Crea rama hotfix según branching.md
- Implementa fix mínimo
- Documenta en PR y prepara entrada ID `—` en próxima release
- No crea spec SDD-NNN salvo que el bug sea no trivial

## Prompt

```
Hotfix urgente / cambio trivial (sin spec propio).

Problema: <DESCRIPCION>
Urgencia: <critica|media>

Instrucciones:
1. Lee branching.md (hotfix) y workflow.md (cambios triviales, ID —).
2. Si es trivial (typo, copy, bump): rama corta, sin spec; documentar ID — en release.
3. Si es bug no trivial pero urgente: evalúa spec bugfix simplificado vs ID — con justificación.
4. PR con checklist mínimo; quality gates del perfil en verde.
5. NO ampliar alcance.

Pide confirmación antes de merge a producción.
```

## Después de pegarlo

Aprueba merge y deploy. Verifica que la release documente el cambio con ID `—`.

## Ver también

- [`branching.md`](../../branching.md) — Hotfix
- [`workflow.md`](../../workflow.md) — Cambios triviales
