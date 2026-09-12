# SDD-025 — Verify: tabla perfil → comandos obligatorios

---

## Cabecera

| Campo                 | Valor                    |
| --------------------- | ------------------------ |
| **ID**                | `SDD-025`                |
| **Dominio**           | `profiles`               |
| **Tipo**              | `feature`                |
| **Fecha**             | 2026-09-11               |
| **Estado**            | `In Build`               |
| **Versión objetivo**  | patch (desde `v1.5.0`)   |
| **Owner**             | mantenedor               |
| **Prioridad**         | `P1`                     |
| **ADRs relacionados** | —                        |
| **Dependencias**      | SDD-022 (Released; no reabrir) |

---

## Problema y objetivo

**Problema:**

En dogfood externo (gap #4), `verify-implementation` pasó en verde diciendo «quality gates en verde» sin nombrar comandos concretos del stack. Gates que **no** viven en `stack.quality_gates` (p. ej. `npm audit` si se tocó `package.json` / lockfile / assets JS) se omitieron; casi se deshizo el pin `quill@2.0.2` (GHSA). SDD-022 alineó Pint=`--test` en Laravel, pero el skill verify sigue genérico y no hay tabla multi-perfil con condicionales.

**Objetivo:**

Formalizar un contrato **solo guía**: cada perfil declara en `checklist-stack.md` la sección **«Verify — comandos obligatorios»** (literales de `quality_gates` + tests filtrados si aplica + condicional JS). El skill `sdd-verify-implementation` obliga a ejecutar esa tabla del perfil activo, sin improvisar. Sin sensor nuevo en `validate-sdd` ni CI.

**Origen:** [informe dogfood gap #4](../../audits/20260906-dogfood-consumidor-externo-informe.md).

---

## Alcance

**Incluye:**

- Sección canónica **«Verify — comandos obligatorios»** (tabla) en los 7 `profiles/*/checklist-stack.md`
- Actualizar bullet de quality gates en `bootstrap/agent-skills/sdd-verify-implementation/SKILL.md` → ejecutar la tabla del `checklist-stack` del perfil activo
- Exigir la sección en `core/templates/profile-template.md` para perfiles nuevos
- Una línea genérica (sin nombres de stack) en `bootstrap/agent-prompts/sdd-workflow-reference.md` (+ espejo `.cursor/rules/` vía sync) apuntando a la tabla del perfil
- Documentar condicional `npm audit` donde aplica (`laravel-voyager`, `laravel-filament`, `react-vite`); en el resto: «No aplica»

**Excluye explícitamente:**

- Sensor `validate-sdd` / CI que compruebe existencia o contenido de la tabla
- Cambiar workflows CI de consumidores
- Meter Pint / `npm` / nombres de framework en `core/prompts/workflow/verify-implementation.md` (DR-1)
- Cambiar valores de `stack.quality_gates` (solo documentarlos en la tabla)
- Gaps dogfood #5–#7
- Reabrir o alterar el contrato Pint de SDD-022

---

## Impacto técnico

> Perfil: `sdd-kit`. Tabla según `profiles/sdd-kit/spec-impact.md`.

| Pregunta                                                              | Respuesta |
| --------------------------------------------------------------------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)?                        | Sí — `profile-template.md` (sección Verify requerida); posible línea genérica en reference vía bootstrap (sin stacks en `core/prompts/`) |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)?     | Sí — los 7 `checklist-stack.md` |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | Sí — skill `sdd-verify-implementation`; `sdd-workflow-reference` (+ sync rules) |
| ¿Afecta `cli/` (comandos, librerías)?                                 | No aplica — sin cambios a CLI ni validate |
| ¿Afecta `.github/workflows/` o reglas Cursor?                         | Sí — regla on-demand tras sync; sin workflows CI nuevos |
| ¿Requiere actualizar `README.md` o `INSTALL.md`?                      | No aplica — contrato en checklist + skill |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)?                   | Solo este ciclo (BACKLOG/spec); consumidores en próximo patch del kit |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles.   | Respeta #1, #2, #4; no modifica el archivo |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR.          | No — guía documental de verify por perfil |

---

## Reglas de negocio

> Aplica [domain-rules.md](../../../business/domain-rules.md) principios **#1** (core agnóstico), **#2** (perfiles autocontenidos), **#4** (verify local antes de push/PR).

Particularidad: comandos y condicionales de stack viven solo en `profiles/`; el skill y la reference core/bootstrap solo dicen «ejecutar la tabla del perfil activo».

---

## Criterios de aceptación

**Happy path:**

- [x] Cada uno de los 7 perfiles tiene sección **«Verify — comandos obligatorios»** en `checklist-stack.md` con: filas siempre (= literales actuales de `quality_gates`), nota de tests filtrados al alcance del spec si el stack lo permite, y fila condicional JS (`npm audit` o «No aplica»)
- [x] Laravel (`voyager`/`filament`): formato verify documentado como `vendor/bin/pint --test`; `--dirty` ≠ evidencia
- [x] Skill `sdd-verify-implementation` exige ejecutar esa tabla (no solo «quality gates en verde» genérico)
- [x] `profile-template.md` exige la sección Verify para perfiles nuevos
- [x] Reference de verify (bootstrap → sync) menciona tabla del `checklist-stack` del perfil **sin** nombrar stacks
- [x] `python ./cli/sdd.py validate` sin errores tras los cambios de producto

**Error path:**

- [x] Si el agente usa solo `pint --dirty` como evidencia de verify en Laravel → checklist/skill lo marcan inválido (mismo criterio SDD-022)
- [x] Si el diff tocó `package.json` / lockfile / assets JS en perfil con condicional y no hay evidencia de `npm audit` → verify incompleto (no open-pr)
- [x] Si alguien propone meter nombres de framework en `core/prompts/workflow/verify-implementation.md` → rechazar (DR-1); corregir en perfil/skill

---

## Congelado para implementación

> Obligatorio para LLM de bajo contexto. **Prohibido explorar** fuera de esta lista.

| Campo | Valor |
| ----- | ----- |
| **Decisión única** | Fuente de verdad de comandos de verify = sección **«Verify — comandos obligatorios»** en `profiles/<perfil>/checklist-stack.md`. El skill solo enlaza/obliga a ejecutarla. Sin sensor validate-sdd/CI. |
| **API / contrato** | Ver tablas por perfil abajo + cambio de skill/reference/template. |
| **Paths de test** | No aplica — cambio documental; verificación = `python ./cli/sdd.py validate` + revisión de que las 7 tablas existen y el skill apunta a ellas. |
| **Lista de lectura** | Los 11 paths de la lista cerrada + este spec + `.github/docs/business/domain-rules.md` |
| **Lectura máx. N** | `13` |
| **Prohibido explorar** | Sí — fuera de la lista: no `grep` / `Glob` / `Read` por curiosidad |

### Contrato de la sección (todos los perfiles)

Título exacto: `## Verify — comandos obligatorios`

Tabla mínima de columnas: `| Gate | Cuándo | Comando |`.

Filas:

1. **Siempre** — un comando por cada clave de `stack.quality_gates` del `sdd.config.yaml` del perfil (literal actual; no inventar flags).
2. **Tests** — preferir filtro al alcance del spec si el tooling lo permite; si no, el comando `test`/`pytest` del gate.
3. **Condicional JS** — `npm audit` si el diff tocó `package.json`, lockfile (`package-lock.json` / `pnpm-lock.yaml` / `yarn.lock`) o assets JS del front:
   - **Aplica:** `laravel-voyager`, `laravel-filament`, `react-vite`
   - **No aplica:** `python-fastapi`, `python-django`, `reports-latex-md`, `sdd-kit`

Literales canónicos a documentar (desde YAML actual del perfil):

| Perfil | Comandos siempre (quality_gates) |
| ------ | -------------------------------- |
| `laravel-voyager` | `php artisan test --compact`; `vendor/bin/pint --test` |
| `laravel-filament` | `php artisan test --compact`; `vendor/bin/pint --test` |
| `python-fastapi` | `pytest --cov`; `ruff check .`; `mypy .` |
| `python-django` | `pytest --cov`; `ruff check .`; `mypy .`; `python manage.py check` |
| `react-vite` | `vitest run`; `eslint .`; `prettier --check .`; `tsc --noEmit` |
| `reports-latex-md` | `markdownlint "content/**/*.md"`; pandoc PDF; `latexmk -pdf …`; `python -m pytest scripts/tests/ -q` |
| `sdd-kit` | compileall `cli/`; pytest `cli/tests`; manifest JSON; verificación perfiles (CI); `python cli/sdd.py validate` |

Nota Laravel (fila formato): `--dirty` solo tip In Build; **no** evidencia de verify/open-pr.

### Lista cerrada de archivos a editar

1. `profiles/laravel-voyager/checklist-stack.md`
2. `profiles/laravel-filament/checklist-stack.md`
3. `profiles/python-fastapi/checklist-stack.md`
4. `profiles/python-django/checklist-stack.md`
5. `profiles/react-vite/checklist-stack.md`
6. `profiles/reports-latex-md/checklist-stack.md`
7. `profiles/sdd-kit/checklist-stack.md`
8. `bootstrap/agent-skills/sdd-verify-implementation/SKILL.md`
9. `core/templates/profile-template.md`
10. `bootstrap/agent-prompts/sdd-workflow-reference.md`
11. `.cursor/rules/sdd-workflow-reference.mdc` — paridad vía `python bootstrap/sync-cursor-rules.py` tras editar (10), o alinear a mano si el sync no cubre el delta

**No editar:** `core/prompts/workflow/verify-implementation.md`; README de perfiles; `sdd.config.yaml` de perfiles (valores de gates); CI consumidores; validate CLI.

### Sensor post-cambio (implementador)

```text
rg "Verify — comandos obligatorios" profiles/*/checklist-stack.md
rg "checklist-stack" bootstrap/agent-skills/sdd-verify-implementation/SKILL.md
python ./cli/sdd.py validate
```

---

## Diseño técnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `profiles/*/checklist-stack.md` (×7) | Agregar sección Verify con tabla |
| `bootstrap/agent-skills/sdd-verify-implementation/SKILL.md` | Bullet: ejecutar tabla del perfil activo |
| `core/templates/profile-template.md` | Exigir sección Verify en checklist |
| `bootstrap/agent-prompts/sdd-workflow-reference.md` | Ítem verify → tabla del checklist-stack (genérico) |
| `.cursor/rules/sdd-workflow-reference.mdc` | Paridad sync |

---

## Verificación técnica

- `python ./cli/sdd.py validate`
- `rg` de sensor post-cambio (arriba)
- Tras sync: reference instalada menciona la tabla del perfil

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Agente ignora la tabla y vuelve a «gates en verde» | Media | Medio | Bullet explícito en skill + reference |
| `npm audit` en perfiles sin JS confunde | Baja | Bajo | Fila «No aplica» explícita |
| Drift skill instalado vs bootstrap | Media | Bajo | Documentar sync/install en verificación |
| Inflar checklists sin valor | Baja | Bajo | Una sección acotada; no duplicar todo el DoD |

**Rollback:** revertir commits de checklists/skill/template/reference; consumidores recuperan texto previo en próximo upgrade.

---

## Notas post-implementación

- Origen: dogfood gap #4; complementa SDD-022 (gap #1 Pint)
- SemVer kit: **patch** (docs + skill verify; sin API CLI)
- **Smoke manual (2026-09-11):** OK — humano confirmó tabla Verify en checklist (p. ej. perfil Laravel) y skill bootstrap apuntando a `checklist-stack` / tabla Verify.
)
