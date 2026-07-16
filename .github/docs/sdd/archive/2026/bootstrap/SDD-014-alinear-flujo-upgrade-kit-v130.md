# SDD-014 — Alinear flujo agentico upgrade-kit al consumo de v1.3.0+

---

## Cabecera

| Campo                 | Valor                                                                 |
| --------------------- | --------------------------------------------------------------------- |
| **ID**                | `SDD-014`                                                             |
| **Dominio**           | `bootstrap`                                                           |
| **Tipo**              | `documentation`                                                       |
| **Fecha**             | 2026-07-15                                                            |
| **Estado**            | `Released`                                                            |
| **Versión objetivo**  | `v1.3.0`                                                              |
| **Owner**             | mantenedor                                                            |
| **Prioridad**         | `P1`                                                                  |
| **ADRs relacionados** | `ADR-002`                                                             |
| **Dependencias**      | SDD-002 (Released); SDD-007…013 (Released — entregables a consumir)   |

---

## Problema y objetivo

**Problema:**

La campaña `v1.3.0` introdujo cambios importantes para consumidores (safe-git always-on, cost-governance, two-zone, compact template, `sdd metrics tokens`, validate-sdd por componente). La nota producto [`docs/releases/v1.3.0.md`](../../../../../docs/releases/v1.3.0.md) ofrece un atajo de 4 pasos que menciona `upgrade-kit` de pasada, pero **no** apunta de forma canónica al runbook ni al flujo agentico completo.

Además hay drift interno:

- `core/upgrade-guide.md` — sección “Tras v1.3.0+” solo cubre safe-git.
- Prompt `upgrade-kit.md` — reinstala si cambió `agent-prompts/`, pero no menciona `agent-skills/` (la skill sí lo hace).
- `sdd-upgrade-kit/reference.md` — checklist post-upgrade no verifica artefactos nuevos de v1.3.0.

Riesgo: instancia con submodule en `v1.3.0` pero sin reglas/skills nuevas, sin checklist y sin trazabilidad vía `UPGRADE-LOG`.

**Objetivo:**

Dejar el **flujo agentico** (`upgrade-kit` / skill `sdd-upgrade-kit` + `upgrade-guide.md`) como camino canónico de actualización, alineado con la nota de release, para que consumidores de `v1.3.0+` instalen y verifiquen todos los entregables relevantes sin reinventar el proceso.

---

## Alcance

**Incluye:**

1. **`docs/releases/v1.3.0.md`**: sección “Actualizar tu proyecto consumidor” prioriza `upgrade-kit` / skill `sdd-upgrade-kit` + enlace a `core/upgrade-guide.md`; checklist breve de verificación post-upgrade (safe-git, cost-governance, validate por componente, `sdd metrics` opcional).
2. **`core/upgrade-guide.md`**: ampliar “Tras v1.3.0+” más allá de safe-git (cost-governance / `session_start`, two-zone vía reinstall, plantilla compacta disponible en kit, salida validate-sdd por componente, CLI metrics viene con el submodule).
3. **`core/prompts/exceptions/upgrade-kit.md`**: sincronizar con la skill — reinstalar si cambió `agent-prompts/` **o** `agent-skills/`.
4. **`bootstrap/agent-skills/sdd-upgrade-kit/reference.md`**: checklist explícito (`sdd-safe-git.mdc`, skill `sdd-cost-governance`, no duplicar safe-migrations de instancia).
5. **`bootstrap/agent-skills/sdd-upgrade-kit/SKILL.md`**: solo si hace falta un ajuste menor de wording para coherencia con la guía (sin cambiar el procedimiento de 10 pasos).
6. Dual-release al cerrar `v1.3.0`: acta campaña + nota producto + CHANGELOG (misma campaña que SDD-007…013).

**Excluye explícitamente:**

- Cambios de comportamiento en `install-agents.py` / `sync-cursor-rules.py` (salvo documentación).
- Nuevo comando CLI `sdd upgrade` o merge automático de instancia.
- Dashboard Canvas, suite pytest CLI, perfiles nuevos.
- Reabrir o reescribir specs SDD-007…013.
- Migración masiva de instancias existentes en la wild (solo mejorar el flujo para quien actualice).

---

## Impacto técnico

> Perfil: `sdd-kit`.

| Pregunta                                                              | Respuesta |
| --------------------------------------------------------------------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)?                        | Sí — `upgrade-guide.md`, prompt `upgrade-kit.md` |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)?     | No aplica — runbook agnóstico al stack |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | Sí — skill `sdd-upgrade-kit` (reference; SKILL solo si wording) |
| ¿Afecta `cli/` (comandos, librerías)?                                 | No aplica — no nuevo comando |
| ¿Afecta `.github/workflows/` o reglas Cursor?                         | No aplica — consumidores reinstalan vía install-agents |
| ¿Requiere actualizar `README.md` o `INSTALL.md`?                      | Opcional — enlace a upgrade-guide si la sección “Actualizar el kit” está desactualizada |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)?                   | Sí — este spec + BACKLOG; cierre en campaña v1.3.0 |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles.   | DR-1, DR-4, DR-5, DR-7 (no cambia el texto; aplica) |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR.          | No — aplica ADR-002; no nuevo ADR |

---

## Reglas de negocio

Aplica [`domain-rules.md`](../../../business/domain-rules.md):

- **DR-1:** Guía y prompt en `core/` sin stacks concretos.
- **DR-4:** Merge de instancia y commits requieren confirmación humana (`human_approval` del prompt).
- **DR-5:** Upgrade incremental; no exigir `init-sdd` de nuevo.
- **DR-7:** Notas de consumo en `docs/releases/`; dual-release al cerrar `v1.3.0`.

Particularidad: el flujo opera entre submodule (`sdd-kit/`) e instancia (`.github/docs/sdd/`); no unifica capas producto/proceso.

---

## Criterios de aceptación

**Happy path:**

- [x] `docs/releases/v1.3.0.md` indica `upgrade-kit` / `sdd-upgrade-kit` como camino **recomendado** y enlaza `core/upgrade-guide.md`
- [x] `upgrade-guide.md` § “Tras v1.3.0+” lista verificación de: safe-git, cost-governance, reinstall prompts+skills, validate por componente; menciona metrics como beneficio del submodule
- [x] Prompt `upgrade-kit.md` menciona reinstalar cuando cambie `agent-prompts/` **o** `agent-skills/`
- [x] `sdd-upgrade-kit/reference.md` incluye checks de `sdd-safe-git.mdc` y `sdd-cost-governance` (y no duplicar safe-migrations)
- [x] Skill y prompt no se contradicen en el orden del flujo
- [x] `python cli/sdd.py validate` / `validate-sdd` sin errores tras los cambios documentales
- [x] Al cerrar campaña: dual-release `v1.3.0` (nota + acta + CHANGELOG; SDD-014 incluido)

**Error path:**

- [x] Si el humano rechaza merge de un archivo de instancia → el flujo documentado sigue prohibiendo marcar `kit.installed_version` completo (ya en guía; no se regresa)
- [x] Si solo se bumpea submodule sin reinstall → checklist post-upgrade detecta ausencia de `sdd-safe-git.mdc` / skill cost-governance

---

## Diseño técnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `docs/releases/v1.3.0.md` | Sección actualizar → camino canónico upgrade-kit; incluye SDD-014 |
| `docs/releases/CHANGELOG.md` | Entrada 1.3.0 (Añadido + Cambiado SDD-014) |
| `core/upgrade-guide.md` | Ampliar checklist post-v1.3.0 |
| `core/prompts/exceptions/upgrade-kit.md` | Sync agent-skills |
| `bootstrap/agent-skills/sdd-upgrade-kit/reference.md` | Checklist artefactos v1.3.0+ |
| `bootstrap/agent-skills/sdd-upgrade-kit/SKILL.md` | Ajuste menor si hace falta coherencia |

---

## Verificación técnica

```bash
python -m compileall -q cli/
python cli/sdd.py validate
# o: bootstrap/validate-sdd.ps1
```

Smoke manual: leer prompt `sdd prompt show upgrade-kit --full` y contrastar con skill + guía.

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Consumidores ya leyeron una nota corta y omiten el upgrade-kit | Media | Medio | Nota v1.3.0 prioriza upgrade-kit; checklist en guía y skill |
| Checklist demasiado largo → el agente lo salta | Baja | Bajo | Mantener checklist corto (5–7 ítems) en reference |
| Duplicar narrativa entre release, guía y skill | Media | Bajo | Release apunta a guía; guía es fuente de verdad; skill/prompt derivan |

---

## Notas post-implementación

- Smoke en instancia consumidora (p. ej. Centinela) sigue siendo pendiente post-release de SDD-007; este spec solo endurece el flujo documentado/agentico.
