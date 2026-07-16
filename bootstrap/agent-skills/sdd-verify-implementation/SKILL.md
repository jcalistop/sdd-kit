---
name: sdd-verify-implementation
description: Ejecuta verify-implementation (sensor/feedback) contra un spec SDD antes de commit/push/PR. Usar cuando el humano pide solo verify, verify-implementation, o retoma verificación en sesión nueva tras implementación ya hecha.
---

# SDD Verify Implementation

Gate **verify-implementation** obligatorio (sensor / feedback) antes de publicación en Git compartido. Detecta errores **después** de implementar; no sustituye las guías usadas en Draft/In Build.

**Prohibido sin confirmación humana:** `git commit`, `git push`, abrir PR.

## Checklist (sensores)

- [ ] [sensor] Quality gates del perfil en verde (local)
- [ ] [sensor] Criterios de aceptación del spec verificados (happy + error) con evidencia
- [ ] [sensor] Reglas de `domain-rules.md` verificadas (o No aplica documentado)
- [ ] [sensor] Arquitectura sana — checks: YAGNI, DRY, SRP, sin debug (`dd()`, `dump()`), sin over-engineering
- [ ] [sensor] `python {{KIT_PATH}}/cli/sdd.py validate` sin errores

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
