# SDD-030 — Skills: perfil de stack resuelto en install

---

## Cabecera

| Campo                 | Valor              |
| --------------------- | ------------------ |
| **ID**                | `SDD-030`          |
| **Dominio**           | `bootstrap`        |
| **Tipo**              | `bugfix`           |
| **Fecha**             | 2026-09-12         |
| **Estado**            | `Released`         |
| **Versión objetivo**  | `v1.6.0` |
| **Owner**             | mantenedor         |
| **Prioridad**         | `P2`               |
| **ADRs relacionados** | —                  |
| **Dependencias**      | SDD-023 (Released — precedencia instancia > global; este SDD cierra el gap #7 que SDD-023 excluyó) |

---

## Problema y objetivo

**Problema:**

En dogfood externo (gap #7), un `sdd-build-spec` adjunto desde `~/.cursor` citaba `sdd-stack-reports-latex-md` en un consumidor con `stack.profile: laravel-voyager`. El agente aplicó quality gates / rutas de un perfil ajeno.

Las plantillas en `bootstrap/agent-skills/` ya usan `{{PROFILE}}` y `install-agents` lo sustituye al escribir. El hueco restante: el marcador `.cursor/skills/.sdd-kit-manifest.json` solo guarda `kit_path` + `managed_skills` — **no** el perfil. Si cambia `stack.profile` (o se reinstala con otro `--profile`) y el marcador coincide en kit/skills, el install hace **skip** y deja el perfil viejo hardcodeado en las skills del proyecto. Discovery nombraba `{{STACK_PROFILE}}`; el código canónico es `{{PROFILE}}` — falta alias y contrato explícito.

**Objetivo:**

Que `install-agents` (1) exponga `PROFILE` y alias `STACK_PROFILE` (mismo valor) al renderizar skills, (2) persista `profile` en el marcador y **re-renderice** si el perfil (o kit_path / managed set) difiere, y (3) documente que no se hardcodea un perfil ajeno en plantillas fuente ni se adjuntan skills SDD globales con perfil de otro repo.

**Origen:** [informe dogfood gap #7](../../audits/20260906-dogfood-consumidor-externo-informe.md). Excluido de [SDD-023](../../archive/2026/bootstrap/SDD-023-install-agents-branching-precedencia.md).

---

## Alcance

**Incluye:**

- `skill_render_context`: claves `PROFILE` y `STACK_PROFILE` (= mismo string desde `--profile` / config del target).
- Marcador `.sdd-kit-manifest.json`: campo `profile`; skip solo si coinciden `kit_path`, `managed_skills` **y** `profile`.
- Tras install: skills del proyecto con el perfil correcto; sin placeholders crudos `{{PROFILE}}` / `{{STACK_PROFILE}}`.
- Limpieza global managed (SDD-023) se mantiene; no reintroducir install en home.
- Tests en `bootstrap/test_install_skills.py` (perfil A → B fuerza reinstall; sin placeholders; plantillas fuente sin stacks ajenos hardcodeados).
- Nota corta en `core/guides/agent-setup.md` + ítem en checklist `profiles/sdd-kit`.

**Excluye explícitamente:**

- Reintroducir instalación de skills en `~/.cursor/skills`.
- Cambiar reglas always-on / sync de `sdd-stack-*.mdc` (ya van por perfil).
- Gap dogfood #6 (build-spec fail-closed Plan mode).
- Renombrar placeholders existentes en skills (`{{PROFILE}}` se mantiene como canónico).
- Adaptadores Claude / Codex / Copilot.
- Cambiar política de `core/guides/branching.md` u otros gaps dogfood.

---

## Impacto técnico

> Perfil: `sdd-kit`. Tabla según `profiles/sdd-kit/spec-impact.md`.

| Pregunta                                                              | Respuesta |
| --------------------------------------------------------------------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)?                        | Sí (menor) — párrafo en `core/guides/agent-setup.md` |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)?     | Sí (menor) — 1 ítem en `profiles/sdd-kit/checklist-stack.md` |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | Sí — `install-agents.py`, tests; plantillas skills solo si hace falta alias/docs |
| ¿Afecta `cli/` (comandos, librerías)?                                 | No aplica — sin cambios CLI |
| ¿Afecta `.github/workflows/` o reglas Cursor?                         | No aplica — skills on-demand; sin reglas always-on nuevas |
| ¿Requiere actualizar `README.md` o `INSTALL.md`?                      | No aplica — basta `agent-setup` + checklist |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)?                   | Sí (proceso) — este spec + BACKLOG + `ids.next_sdd` |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles.   | Cumple bootstrap/CLI (Python 3.10+, sin deps nuevas). Sin cambio al archivo domain-rules; respeta DR-1/2 |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR.          | No — contrato de install + marcador; no ADR |

---

## Reglas de negocio

Aplica [`.github/docs/business/domain-rules.md`](../../../business/domain-rules.md):

- **DR-1 / DR-2** — Core agnóstico; lo específico de stack vive en perfiles / render de install, no hardcodeado en plantillas globales de skills.
- **Bootstrap/CLI** — Python 3.10+; sin dependencias externas nuevas.
- **DR-4** — El agente ejecuta; el humano aprueba Ready/merge.

Particularidad: el perfil en skills es **guía** resuelta en install (feedforward), no un sensor CI nuevo.

---

## Criterios de aceptación

**Happy path:**

- [x] `skill_render_context` incluye `PROFILE` y `STACK_PROFILE` con el mismo valor del perfil pasado a install.
- [x] El marcador `.sdd-kit-manifest.json` guarda `profile`; si el perfil instalado difiere del marcador → re-render (no skip).
- [x] Tras install con perfil `laravel-voyager` (o cualquier perfil válido): skills del proyecto contienen `sdd-stack-<ese-perfil>` (donde aplique) y **no** contienen `{{PROFILE}}` ni `{{STACK_PROFILE}}`.
- [x] Plantillas fuente en `bootstrap/agent-skills/` no hardcodean un `sdd-stack-<perfil-ajeno>` concreto (usan placeholder).
- [x] Limpieza de skills managed en `~/.cursor/skills` sigue ocurriendo tras install (comportamiento SDD-023).
- [x] `python -m pytest bootstrap/test_install_skills.py -q` en verde.
- [x] `core/guides/agent-setup.md` documenta: perfil resuelto en install; no adjuntar skills SDD globales de otro proyecto.
- [x] Checklist `sdd-kit` incluye verificación post-install del perfil en skills del proyecto.
- [x] `python ./cli/sdd.py validate` sin errores tras cambios de instancia/docs tocados.

**Error path:**

- [x] Marcador sin campo `profile` (legado) → se trata como desactualizado y se re-renderiza (no skip silencioso).
- [x] Diff que reinstale skills en `~/.cursor/skills` o hardcodee un perfil ajeno en plantilla fuente → fuera de alcance; rechazar en review.

---

## Congelado para implementación

> Obligatorio para LLM de bajo contexto. **Prohibido explorar** fuera de esta lista. Lectura máx. **N = 8** paths de esta lista (+ este spec + `domain-rules.md`).

| Campo | Valor |
| ----- | ----- |
| **Decisión única** | Placeholder canónico `{{PROFILE}}`; alias `{{STACK_PROFILE}}` (= mismo valor) en `skill_render_context`. Marcador guarda `profile`; skip solo si `kit_path` + `managed_skills` + `profile` coinciden. Sin install en home. |
| **API / contrato** | `skill_render_context(...) -> dict` con claves `PROFILE` y `STACK_PROFILE`. Marcador JSON: `{ "managed_skills": [...], "kit_path": "...", "profile": "<stack.profile>" }`. |
| **Paths de test** | `bootstrap/test_install_skills.py` — al menos: (1) install perfil A deja A y sin placeholders; (2) re-install con perfil B distinto fuerza rewrite a B; (3) marcador sin `profile` no hace skip. |
| **Lista de lectura** | Ver lista cerrada abajo |
| **Lectura máx. N** | `8` |
| **Prohibido explorar** | Sí — fuera de la lista: no `grep` / `Glob` / `Read` por curiosidad |

### Lista cerrada de archivos a editar / leer

1. `bootstrap/install-agents.py` — `skill_render_context` (`STACK_PROFILE`); marcador `profile` + condición de skip
2. `bootstrap/test_install_skills.py` — tests de perfil / re-render
3. `bootstrap/agent-skills/**` — solo si hace falta mención/docs del alias; **sin** hardcodear stacks
4. `core/guides/agent-setup.md` — párrafo perfil en install + no adjuntar globals ajenos
5. `profiles/sdd-kit/checklist-stack.md` — ítem post-install: skills del proyecto reflejan `stack.profile`
6. Este spec + BACKLOG / `sdd.config.yaml` (ids) al cerrar ciclo documental si aplica en el mismo PR de producto

**No editar:** gap #6, Claude/Codex/Copilot, `core/guides/branching.md`, reintroducir globals.

### Sensor post-cambio (implementador)

```text
rg "STACK_PROFILE|\"profile\"" bootstrap/install-agents.py
```

→ hits de alias y persistencia de `profile` en marcador.

```text
python -m pytest bootstrap/test_install_skills.py -q
```

→ verde.

```text
python cli/sdd.py validate
```

→ 0 errores si se tocó docs de instancia.

---

## Diseño técnico _(opcional bugfix — resumen)_

| Archivo | Cambio |
| ------- | ------ |
| `bootstrap/install-agents.py` | Alias `STACK_PROFILE`; `profile` en marcador; skip condicional |
| `bootstrap/test_install_skills.py` | Tests perfil A/B y marcador legado |
| `core/guides/agent-setup.md` | Nota perfil + no adjuntar skill global ajena |
| `profiles/sdd-kit/checklist-stack.md` | Ítem verificación perfil en skills del proyecto |

```text
install_cursor_skills(profile)
  → context = { PROFILE, STACK_PROFILE=PROFILE, ... }
  → if marker.kit_path && managed && profile match → skip write
  → else render all managed skills
  → write marker including profile
  → remove_global_managed_skills(manifest ids)
```

---

## Verificación técnica

| Gate | Comando |
| ---- | ------- |
| Tests install skills | `python -m pytest bootstrap/test_install_skills.py -q` |
| Validate SDD | `python cli/sdd.py validate` |
| Compile (si toca solo bootstrap) | No aplica CLI — opcional `python -m compileall -q bootstrap/` si el perfil lo exige en CI |

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Consumidores con marcador legado sin `profile` re-escriben skills en el próximo install | Alta | Bajo | Comportamiento deseado; documentar en agent-setup |
| Cursor sigue cacheando skill global adjuntada a mano | Baja | Medio | SDD-023 borra managed; agent-setup: no adjuntar `sdd-*` del home |
| Confusión `PROFILE` vs `STACK_PROFILE` | Baja | Bajo | Alias mismo valor; canónico `PROFILE` en plantillas |

---

## Notas post-implementación

- Mencionar en nota patch del kit: marcador skills incluye `profile`; re-install si cambia perfil.
- Smoke manual (2026-09-13, humano): exitoso — rewrite A→B visible en `.cursor/skills/` (no en plantilla `bootstrap/agent-skills/`); marcador legado sin `profile` fuerza re-render.
)
