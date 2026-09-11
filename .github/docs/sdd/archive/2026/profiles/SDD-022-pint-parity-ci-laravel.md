# SDD-022 — Pint local = comando CI (Voyager + Filament)

> Spec Released. Archivado en `archive/2026/profiles/`.

---

## Cabecera

| Campo                 | Valor        |
| --------------------- | ------------ |
| **ID**                | `SDD-022`    |
| **Dominio**           | `profiles`   |
| **Tipo**              | `bugfix`    |
| **Fecha**             | 2026-09-10   |
| **Estado**            | `Released`   |
| **Versión objetivo**  | `v1.5.0`     |
| **Owner**             | mantenedor   |
| **Prioridad**         | `P0`         |
| **ADRs relacionados** | —            |
| **Dependencias**      | —            |

---

## Problema y objetivo

**Problema:** En perfiles `laravel-voyager` y `laravel-filament`, checklists, `quality_gates.format`, reglas Cursor y prompts documentan `vendor/bin/pint --dirty` como gate de formato. En dogfood externo (`minsal-centinela` / SDD-231, kit `v1.4.1`) `verify-implementation` pasó con `--dirty` y el CI del PR falló con `vendor/bin/pint --test`. El sensor local no era paridad con CI.

**Objetivo:** Que verify + checklist-stack de Voyager y Filament exijan el **mismo comando de formato que CI** (`vendor/bin/pint --test`) antes de open-pr. `--dirty` solo como tip de autofix en In Build, nunca como evidencia de verify.

**Origen:** [informe dogfood gap #1](../../audits/20260906-dogfood-consumidor-externo-informe.md).

---

## Alcance

**Incluye:**

- Alinear gate Pint → `vendor/bin/pint --test` en perfiles Voyager + Filament y espejos bootstrap listados en **Congelado**.
- Una bullet en skill `sdd-verify-implementation`: ejecutar `stack.quality_gates` del perfil (comando literal).

**Excluye explícitamente:**

- Otros perfiles (Pint no aplica).
- Tabla multi-stack / `npm audit` (gap dogfood #4).
- Productizar plantilla «Congelado» en DoR genérico (gap #3).
- Editar `core/prompts/workflow/verify-implementation.md` (evitar Pint en core; DR-1).
- Cambiar workflows CI de proyectos consumidores.
- Inventar flags combinados (`--dirty --test`).

---

## Congelado para implementación

> Obligatorio para LLM de bajo contexto. **Prohibido explorar** fuera de esta lista. Lectura máx.: estos archivos + este spec + `.github/docs/business/domain-rules.md` (~15 paths).

### Decisión única

Gate de formato (verify / checklist / PR / `quality_gates.format`) = **`vendor/bin/pint --test`**.

### Sustitución canónica

| Contexto | Acción |
| -------- | ------ |
| checklist, `quality_gates.format`, README, cursor-rules, agent-prompts (voyager + filament) | Reemplazar `vendor/bin/pint --dirty` → `vendor/bin/pint --test` donde el texto es el **gate** (ítem checklist, clave `format:`, línea «Formato:»). |
| `bootstrap/agent-skills/stacks/laravel-filament.md` (`pint --dirty --format agent`) | **No** convertir a `--test`. Añadir línea: *verify/open-pr: `vendor/bin/pint --test`*. |
| Ejemplo Filament `SDD-001` (bloque verificación) | Sustituir `vendor/bin/pint --dirty` → `vendor/bin/pint --test`. |

### Lista cerrada de archivos a editar

1. `profiles/laravel-voyager/checklist-stack.md`
2. `profiles/laravel-voyager/sdd.config.yaml`
3. `profiles/laravel-voyager/README.md`
4. `profiles/laravel-filament/checklist-stack.md`
5. `profiles/laravel-filament/sdd.config.yaml`
6. `profiles/laravel-filament/README.md`
7. `profiles/laravel-filament/examples/SDD-001-login-con-recuperacion.md`
8. `bootstrap/cursor-rules/sdd-stack-laravel-voyager.mdc`
9. `bootstrap/cursor-rules/sdd-stack-laravel-filament.mdc`
10. `bootstrap/agent-prompts/stacks/laravel-voyager.md`
11. `bootstrap/agent-prompts/stacks/laravel-filament.md`
12. `bootstrap/agent-skills/stacks/laravel-filament.md`
13. `bootstrap/agent-skills/sdd-verify-implementation/SKILL.md` — **una** bullet: ejecutar comandos literales de `stack.quality_gates` del perfil antes de open-pr (formato Laravel = `format` tras este SDD)

**No editar:** `core/prompts/workflow/verify-implementation.md`.

Tras editar agent-prompts, si el repo exige paridad: correr `python bootstrap/sync-cursor-rules.py` (o equivalente documentado) solo si las reglas `.mdc` no quedaron ya alineadas a mano; este SDD permite editar ambos espejos directamente.

### Prohibido

- Explorar / editar otros perfiles.
- Ampliar a gap #4 o #3 de producto.
- Cambiar CI de consumidores.
- Leer más de ~15 archivos fuera de la lista cerrada + spec + domain-rules.

### Sensor post-cambio (implementador)

```text
rg "pint --dirty" profiles/laravel-voyager profiles/laravel-filament bootstrap/cursor-rules bootstrap/agent-prompts
```

→ **0 hits** (gate). Excepción permitida: `bootstrap/agent-skills/stacks/laravel-filament.md` solo junto a tip «autofix / tras editar PHP».

```text
python cli/sdd.py validate
```

→ 0 errores.

---

## Impacto técnico

Perfil stack: `sdd-kit` ([`profiles/sdd-kit/spec-impact.md`](../../../../profiles/sdd-kit/spec-impact.md)).

| Pregunta                                                              | Respuesta |
| --------------------------------------------------------------------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)?                        | No — no editar prompt core verify; DR-1 |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)?     | Sí — Voyager + Filament: checklist, `quality_gates.format`, README, ejemplo Filament |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | Sí — cursor-rules, agent-prompts stacks Laravel, skill stack filament, skill verify |
| ¿Afecta `cli/` (comandos, librerías)?                                 | No aplica — sin cambios CLI |
| ¿Afecta `.github/workflows/` o reglas Cursor?                         | Sí (menor) — reglas `sdd-stack-laravel-*.mdc` en bootstrap (fuente install) |
| ¿Requiere actualizar `README.md` o `INSTALL.md`?                      | No aplica — solo README de perfiles Laravel |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)?                   | Sí (proceso) — este spec + BACKLOG + `ids.next_sdd` |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles.   | Cumple DR-1 (core agnóstico), DR-2 (stack en perfiles), DR-4 (verify antes de PR). Sin cambio al archivo domain-rules |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR.          | No — comando de gate del perfil, no arquitectura nueva |

---

## Reglas de negocio

Aplica [`.github/docs/business/domain-rules.md`](../../../business/domain-rules.md):

- **DR-1** Core agnóstico — no meter Pint en `core/`.
- **DR-2** Perfiles autocontenidos — comando en `profiles/laravel-*` + espejos bootstrap de stack.
- **DR-4** Verify local antes de push/PR — el gate de formato debe ser el de CI.

Particularidad: paridad comando local ↔ CI solo para stacks Laravel con Pint.

---

## Criterios de aceptación

**Happy path:**

- [x] Checklists Voyager y Filament: ítem Pint = `vendor/bin/pint --test` (exit 0 / sin diferencias).
- [x] `stack.quality_gates.format` en ambos `profiles/laravel-*/sdd.config.yaml` = `vendor/bin/pint --test`.
- [x] README + cursor-rules + agent-prompts de ambos stacks: gate «Formato» = `--test` (no `--dirty` como evidencia).
- [x] Ejemplo Filament SDD-001: verificación usa `--test`.
- [x] Skill stack filament: tip autofix puede conservar `--dirty --format agent`; línea explícita verify/open-pr = `--test`.
- [x] Skill `sdd-verify-implementation`: bullet que obliga a ejecutar `quality_gates` literales del perfil antes de open-pr.
- [x] Nota implícita o explícita en checklist/README: `--dirty` ≠ evidencia de paridad CI.
- [x] `rg` del sensor Congelado en verde; `python cli/sdd.py validate` OK.

**Error path:**

- [x] Reportar verify OK **solo** con `pint --dirty` → **no** listo para open-pr. _(documentado en skill verify + checklist)_
- [x] Diff que deje `--dirty` como único comando de formato en checklist o `quality_gates.format` de Voyager o Filament → DoD fallido. _(gates usan `--test`)_
- [x] Diff que edite otros perfiles o `core/prompts/workflow/verify-implementation.md` → fuera de alcance; rechazar. _(no tocados)_

---

## Cambio de BD _(solo si incluye `db-change`)_

No aplica — sin BD.

---

## Diseño técnico _(bugfix documental / harness)_

| Archivo | Cambio |
| ------- | ------ |
| Lista cerrada en **Congelado** | Sustitución gate `--dirty` → `--test`; skill filament + verify según tabla |

---

## Verificación técnica

```bash
rg "pint --dirty" profiles/laravel-voyager profiles/laravel-filament bootstrap/cursor-rules bootstrap/agent-prompts
python cli/sdd.py validate
```

(Perfil `sdd-kit`: no requiere Pint ni PHPUnit del kit.)

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Consumidores con CI que aún no usa `--test` | Baja | Medio | Documentar en nota release patch; comando alineado al patrón CI Laravel habitual del dogfood |
| Agente sigue usando `--dirty` por memoria de skills globales viejas | Media | Medio | Bullet en verify + reinstall agents tras upgrade |
| Espejos prompts vs cursor-rules desalineados | Baja | Bajo | Editar ambos en la lista cerrada; sync si aplica |

**Rollback:** revertir commit del SDD; restaurar literales `--dirty` en la lista cerrada.

---

## Notas post-implementación

- **Smoke manual (humano):** OK — 2026-09-10. Revisados checklists Voyager/Filament: gate Pint = `vendor/bin/pint --test`; nota `--dirty` ≠ evidencia de verify.
- Mencionar en `docs/releases/v1.4.2.md` el breaking menor de **documentación de gate** para consumidores Laravel (comando verify local).
- Gap #4 (tabla verify multi-stack) sigue en Discovery; no mezclar.
