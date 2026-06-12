---
id: adopt-new
title: Adoptar SDD en proyecto nuevo
category: adoption
adoption_stage: 1
workflow_phase: null
when: Repo nuevo o vacío; submodule sdd-kit/ ya añadido
prerequisites:
  - sdd-kit/ como submodule
  - Perfil elegido (ej. laravel-filament)
related:
  - adoption-guide.md#etapa-1
  - agent-setup.md
cli_alternative: sdd init --profile <PERFIL> --project "<NOMBRE>"
tags: [onboarding, new-project]
human_approval: false
---

## Cuándo usarlo

Proyecto **nuevo** donde puedes ejecutar bootstrap sin riesgo de pisar documentación previa. Alternativa al comando manual `init-sdd`.

## Qué hará el agente

- Ejecuta `init-sdd` con el perfil indicado
- Completa `sdd.config.yaml`, `business/README.md` y `BACKLOG.md`
- Instala adaptadores de agente (`-Agent auto`)
- Corre `validate-sdd` y reporta resultado
- Propone 3–5 ítems en Discovery

## Prompt

```
Adopta SDD en este proyecto NUEVO con perfil <PERFIL>.

Contexto:
- Proyecto nuevo (sin instancia SDD previa).
- El kit está en sdd-kit/ (submodule).

Instrucciones:
1. Lee sdd-kit/core/adoption-guide.md (Etapa 1) y sdd-kit/core/agent-setup.md.
2. Ejecuta init-sdd con perfil <PERFIL> y nombre de proyecto "<NOMBRE_PROYECTO>".
3. Completa sdd.config.yaml, business/README.md y BACKLOG (3–5 ítems en Discovery).
4. Instala adaptadores de agente (-Agent auto).
5. Ejecuta validate-sdd y reporta resultado.

No crear specs retrospectivos. No inventar reglas de negocio sin preguntar.
```

## Después de pegarlo

Revisa `sdd.config.yaml`, `business/README.md` y el BACKLOG propuesto. Aprueba o corrige antes de empezar el primer spec.

## Ver también

- [`adoption-guide.md`](../../adoption-guide.md) — Etapa 1
- [`agent-setup.md`](../../agent-setup.md)
- `sdd prompt show formalize-domain-rules` — antes del primer spec no trivial
