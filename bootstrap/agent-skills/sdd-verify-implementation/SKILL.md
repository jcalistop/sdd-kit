---
name: sdd-verify-implementation
description: Ejecuta verify-implementation (sensor/feedback) contra un spec SDD antes de commit/push/PR. Usar cuando el humano pide solo verify, verify-implementation, o retoma verificación en sesión nueva tras implementación ya hecha.
---

# SDD Verify Implementation

Gate **verify-implementation** obligatorio (sensor / feedback) antes de publicación en Git compartido. Detecta errores **después** de implementar; no sustituye las guías usadas en Draft/In Build.

**Prohibido sin confirmación humana:** `git commit`, `git push`, abrir PR.

**Contexto mínimo requerido:**

1. Spec del `SDD-NNN` activo — **solo criterios de aceptación** (happy + error path)
2. `{{SDD_PATH}}/../business/domain-rules.md` — reglas aplicables

**NO leer** el spec completo si ya se leyó durante la implementación. Solo re-leer la sección de criterios.
Si verify ya falló 3 veces en esta sesión → **STOP**. Reportar criterios fallidos al humano. No seguir iterando.

## Checklist (sensores)

- [ ] [sensor] Quality gates del perfil en verde (local): ejecutar la tabla **«Verify — comandos obligatorios»** del `checklist-stack.md` del perfil activo (`stack.profile`). Incluye literales de `quality_gates`, tests filtrados si aplica y condicionales (p. ej. audit de dependencias JS si el diff tocó `package.json` / lockfile / assets JS). Atajos de autofix de formato ≠ evidencia de verify/open-pr.
- [ ] [sensor] Criterios de aceptación del spec verificados (happy + error) con evidencia
- [ ] [sensor] Reglas de `domain-rules.md` verificadas (o No aplica documentado)
- [ ] [sensor] Arquitectura sana — checks: YAGNI, DRY, SRP, sin debug (`dd()`, `dump()`), sin over-engineering
- [ ] [sensor] `python {{KIT_PATH}}/cli/sdd.py validate` sin errores

Si falla: **no** `push` ni PR. Corregir o documentar deuda con acuerdo humano.

## Procedimiento

1. Leer spec, `domain-rules.md`.
2. Criterios → evidencia; arquitectura sana.
3. `python {{KIT_PATH}}/cli/sdd.py validate`
4. Quality gates: tabla **Verify** del `checklist-stack` del perfil activo (no improvisar comandos).
5. Reporte + **Smoke manual (humano)**.

Si verify OK: preguntar commit → `sdd-open-pr`.

## Recursos

- `python {{KIT_PATH}}/cli/sdd.py prompt show verify-implementation --full`
