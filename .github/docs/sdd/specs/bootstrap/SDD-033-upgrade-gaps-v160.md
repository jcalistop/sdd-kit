# SDD-033 — Gaps de upgrade a v1.6.0 (guía + skill)

> Al cerrar: `git mv` a `archive/<YYYY>/bootstrap/`.

---

## Cabecera

| Campo                 | Valor          |
| --------------------- | -------------- |
| **ID**                | `SDD-033`      |
| **Dominio**           | `bootstrap`    |
| **Tipo**              | `documentation`|
| **Fecha**             | 2026-09-13     |
| **Estado**            | `In Build`     |
| **Versión objetivo**  | `v1.6.0`       |
| **Owner**             | mantenedor kit |
| **Prioridad**         | `P1`           |
| **ADRs relacionados** | —              |
| **Dependencias**      | Campaña SDD-024…032 (documenta su consumo); no bloquea su merge; misma release `v1.6.0` |

---

## Problema y objetivo

**Problema:**

El bump a un tag post-v1.5 (campaña → **v1.6.0**) no está documentado de punta a punta para consumidores (p. ej. desde **v1.2**): falta § **Tras v1.6.0** en el upgrade-guide; la skill `sdd-upgrade-kit` asume `{{SDD_PATH}}/guides/upgrade-guide.md` (la instancia puede no tener `guides/` aún); el `diff -rq sdd-kit/core` no guía el relocate de guías; y no hay playbook de **salto largo** (checklist acumulativo + un solo tag).

**Objetivo:**

Cerrar el contrato de consumo de **v1.6.0**: sección Tras v1.6.0, migración documentada de guías en instancia, skill/reference/prompt alineados (runbook canónico desde el kit tras el bump), y criterios para la nota producto al close-release — sin script automático de migración.

---

## Alcance

**Incluye:**

1. Sección **Tras v1.6.0** en [`core/guides/upgrade-guide.md`](../../../../core/guides/upgrade-guide.md):
   - Paths kit: `core/<guía>.md` → `core/guides/` (sin stubs).
   - Instancia: si existen guías en la raíz de `paths.sdd`, mover a `guides/` (`git mv` / merge con OK humano); no tocar `BACKLOG`/`specs`/`archive`.
   - Diff de merge alineado al layout nuevo (`sdd-kit/core/guides/` ↔ `paths.sdd/guides/`, no solo `core/` plano).
   - Novedades de campaña para el consumidor: Congelado (plantillas), tablas Verify en perfiles, audits/research opcionales, fail-closed build-spec, re-render skills por `profile`.
   - Playbook salto desde ≤v1.2: **un** checkout a `v1.6.0` + aplicar checklists v1.3.0…v1.6.0 en orden (no N bumps de tag).
2. Actualizar [`bootstrap/agent-skills/sdd-upgrade-kit/SKILL.md`](../../../../bootstrap/agent-skills/sdd-upgrade-kit/SKILL.md):
   - Tras bump de submodule, fuente canónica del runbook = `{{KIT_PATH}}/core/guides/upgrade-guide.md` (evitar chicken-egg con instancia vieja).
   - Diff/merge según layout `guides/`.
3. Ampliar [`bootstrap/agent-skills/sdd-upgrade-kit/reference.md`](../../../../bootstrap/agent-skills/sdd-upgrade-kit/reference.md) con checklist v1.5–v1.6 (`branching_mode`, `profile` en marcador, paths `guides/`, borrar `sdd-core` si quedó).
4. Ajuste mínimo de [`core/prompts/exceptions/upgrade-kit.md`](../../../../core/prompts/exceptions/upgrade-kit.md) si contradice lo anterior.
5. Criterios / bullets para que **close-release** incluya en `docs/releases/v1.6.0.md` la migración de paths y el salto checklist (este spec **no** crea aún el archivo de release).

**Excluye explícitamente:**

- Script automático que reescriba la instancia.
- Stubs en raíz `core/` para paths viejos.
- Reescritura total del upgrade-guide.
- Cerrar / taggear `v1.6.0` (close-release de la campaña).
- Cambiar CLI `sdd` (validate/API).
- Cambios a `install-agents.py` salvo mención documental (el re-render por `profile` ya es SDD-030).

---

## Impacto técnico

Perfil: [`profiles/sdd-kit/spec-impact.md`](../../../../profiles/sdd-kit/spec-impact.md).

| Pregunta | Respuesta |
| -------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)? | Sí — `core/guides/upgrade-guide.md` + ajuste mínimo prompt `upgrade-kit` |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)? | No aplica — solo se documenta que el consumidor verá tablas Verify ya en perfiles |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | Sí — skill `sdd-upgrade-kit` (+ `reference.md`); sin cambiar `install-agents.py` |
| ¿Afecta `cli/` (comandos, librerías)? | No aplica |
| ¿Afecta `.github/workflows/` o reglas Cursor? | No aplica — skill on-demand; consumidores reinstalan |
| ¿Requiere actualizar `README.md` o `INSTALL.md`? | No aplica (INSTALL ya apunta a upgrade-guide); release note en close-release |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)? | Sí — este spec + BACKLOG |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles. | No cambia el texto; aplica DR-5 (adopción incremental), DR-7 (producto vs proceso) |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR. | No |

---

## Reglas de negocio

Aplica [`.github/docs/business/domain-rules.md`](../../../business/domain-rules.md):

- **DR-5** — Adopción/upgrade incremental; no exigir reescritura retrospectiva de specs.
- **DR-7** — Separación producto (`docs/releases/`) / proceso; este SDD prepara el wording de la nota producto en close-release.
- **Bootstrap** — Sin dependencias externas nuevas; markdown de guía + skill.

---

## Criterios de aceptación

**Happy path:**

- [x] Existe § **Tras v1.6.0** en `core/guides/upgrade-guide.md` con: paths kit; migrate instancia → `guides/`; diff `core/guides` ↔ `paths.sdd/guides`; novedades campaña; playbook salto ≤v1.2 (un tag + checklists ordenados).
- [x] `sdd-upgrade-kit/SKILL.md` usa como runbook canónico post-bump `{{KIT_PATH}}/core/guides/upgrade-guide.md` y describe diff/merge de `guides/`.
- [x] `sdd-upgrade-kit/reference.md` incluye checklist v1.5–v1.6 (`branching_mode`, profile en marcador, guides, sin `sdd-core` huérfano).
- [x] Prompt `upgrade-kit` no contradice la fuente canónica del kit ni el layout `guides/`.
- [x] Spec deja bullets explícitos para `docs/releases/v1.6.0.md` (close-release).
- [x] `python ./cli/sdd.py validate` en verde.

**Error path:**

- [x] Skill **no** exige que `paths.sdd/guides/upgrade-guide.md` exista **antes** del merge de instancia / bump.
- [x] No se reintroduce `cost-governance` ni `metrics tokens` como pasos vigentes.
- [x] No se pide N checkouts intermedios (1.2→1.3→…→1.6) como camino obligatorio.
- [x] Sin script de migración automática ni stubs en raíz `core/`.

---

## Congelado para implementación _(opcional)_

Omitido — alcance documental cerrado; paths conocidos.

---

## Cambio de BD

No aplica.

---

## Diseño técnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `core/guides/upgrade-guide.md` | § Tras v1.6.0 + ajuste diff en flujo genérico si hace falta |
| `bootstrap/agent-skills/sdd-upgrade-kit/SKILL.md` | Runbook canónico kit; merge `guides/` |
| `bootstrap/agent-skills/sdd-upgrade-kit/reference.md` | Checklist v1.5–v1.6 |
| `core/prompts/exceptions/upgrade-kit.md` | Ajuste mínimo de coherencia |
| `docs/releases/v1.6.0.md` | Solo en close-release (criterios aquí) |

**Notas de diseño:**

- Orden consumidor: bump submodule → leer guía **del kit** → migrate/merge instancia → reinstall agents → validate → `kit.installed_version`.
- Salto largo = un tag + checklists acumulativos (v1.3.0+ … v1.6.0), no N tags.

**Bullets mínimos para nota producto v1.6.0 (close-release):**

- Paths: guías en `core/guides/`; actualizar enlaces y mover copia en `paths.sdd` a `guides/` si aplica.
- Un bump a `v1.6.0` + checklists upgrade-guide en orden (desde ≤v1.2).
- Reinstall agents obligatorio (skills/prompts; `branching_mode`; profile en marcador).
- Opcional: audits/research; Congelado en plantillas; Verify tablas en checklist-stack.

---

## Verificación técnica

```bash
python cli/sdd.py validate
# En In Build: grep -n "Tras v1.6.0|KIT_PATH.*upgrade-guide|core/guides" \
#   core/guides/upgrade-guide.md bootstrap/agent-skills/sdd-upgrade-kit/*
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Consumidor solo lee skill vieja pre-reinstall | Media | Medio | Prompt + INSTALL ya dicen leer guía del kit tras bump; skill nueva prioriza KIT_PATH |
| Diff genérico sigue confuso | Media | Medio | Reescribir ejemplo de diff en la misma § / paso 3 |
| Scope creep a script de migración | Baja | Alto | Exclusión explícita |

**Rollback:** revertir diffs de guía/skill/prompt.

---

## Notas post-implementación

- Origen: análisis upgrade v1.2→v1.6 (gaps de guía/skill/layout); campaña SemVer minor v1.6.0.
- **2026-09-13 (In Build):** § Tras v1.6.0 + diff `guides/`; skill/reference/prompt con runbook `KIT_PATH`; playbook salto largo.
- **Smoke manual (2026-09-13):** humano confirmó OK.
