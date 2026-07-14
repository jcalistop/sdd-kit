---
name: sdd-verify-implementation
description: Ejecuta verify-implementation contra un spec SDD antes de commit/push/PR. Usar cuando el humano pide solo verify, verify-implementation, o retoma verificación en sesión nueva tras implementación ya hecha.
---

# SDD Verify Implementation

Gate **verify-implementation** obligatorio antes de publicación en Git compartido.

**Prohibido sin confirmación humana:** `git commit`, `git push`, abrir PR.

## Checklist

- [ ] Quality gates del perfil en verde (local)
- [ ] Criterios de aceptación del spec verificados (happy + error) con evidencia
- [ ] Reglas de `domain-rules.md` verificadas (o No aplica documentado)
- [ ] Arquitectura sana — checks: YAGNI, DRY, SRP, sin debug (`dd()`, `dump()`), sin over-engineering
- [ ] `python {{KIT_PATH}}/cli/sdd.py validate` sin errores

Si falla: **no** `push` ni PR. Corregir o documentar deuda con acuerdo humano.

## Procedimiento

1. Leer spec, `domain-rules.md`.
2. Criterios → evidencia; arquitectura sana.
3. `python {{KIT_PATH}}/cli/sdd.py validate`
4. Quality gates si hubo cambios de producto en el working tree.
5. Reporte + **Smoke manual (humano)**.

Si verify OK: preguntar commit → `sdd-open-pr`.

## Recursos

- `python {{KIT_PATH}}/cli/sdd.py prompt show verify-implementation --full`
