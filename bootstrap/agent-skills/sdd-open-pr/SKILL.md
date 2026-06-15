---
name: sdd-open-pr
description: Abre PR hacia dev tras verify-implementation OK y commit confirmado. Usar cuando el humano pide open-pr, crear PR, o publicar cambios SDD validados.
---

# SDD Open PR

Abrir PR con checklist SDD hacia **`{{DEV_BRANCH}}`**.

**Precondiciones:** `verify-implementation` OK; commit confirmado por el humano.

**Prohibido:** PR antes de verify; push sin confirmación humana.

## Rutas

| Artefacto    | Ruta                               |
| ------------ | ---------------------------------- |
| Checklist PR | `{{SDD_PATH}}/checklist-pr.md`     |
| Plantilla PR | `.github/PULL_REQUEST_TEMPLATE.md` |
| Workflow     | `{{SDD_PATH}}/workflow.md`         |

## Procedimiento

1. Confirmar verify OK previo.
2. Spec → `Estado: Validating`; BACKLOG In Build → Validating.
3. `git push -u origin HEAD` con confirmación humana.
4. `gh pr create` hacia **`{{DEV_BRANCH}}`** (título `SDD-NNN: resumen`).
5. Checklist Parte A + B de `checklist-pr.md`.
6. Pedir merge al humano.

## Recursos

- [reference.md](reference.md)
- `python {{KIT_PATH}}/cli/sdd.py prompt show open-pr --full`
