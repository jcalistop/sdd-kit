---
name: sdd-verify-implementation
description: Ejecuta verify-implementation contra un spec SDD antes de commit/push/PR. Usar cuando el humano pide solo verify, verify-implementation, o retoma verificación en sesión nueva tras implementación ya hecha.
---

# SDD Verify Implementation

Gate **verify-implementation** obligatorio antes de publicación en Git compartido.

**Prohibido sin confirmación humana:** `git commit`, `git push`, abrir PR.

## Rutas

| Artefacto         | Ruta                                                          |
| ----------------- | ------------------------------------------------------------- |
| Spec              | `{{SDD_PATH}}/specs/<dominio>/SDD-NNN-*.md`                   |
| Verify            | `.cursor/rules/sdd-workflow-reference.mdc`                    |
| Plantilla reporte | [sdd-build-spec/reference.md](../sdd-build-spec/reference.md) |

## Procedimiento

Ejecutar **§ B** de [`sdd-build-spec`](../sdd-build-spec/SKILL.md) (sin § A):

1. Leer spec, `domain-rules.md`, `sdd-workflow-reference`.
2. Criterios → evidencia; arquitectura sana.
3. `python {{KIT_PATH}}/cli/sdd.py validate`
4. Quality gates si hubo cambios de producto en el working tree.
5. Reporte + **Smoke manual (humano)**.

Si verify OK: preguntar commit → `sdd-open-pr`.

## Recursos

- `python {{KIT_PATH}}/cli/sdd.py prompt show verify-implementation --full`
