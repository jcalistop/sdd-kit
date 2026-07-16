# SDD-011 — Contrato dual-release producto ↔ campaña (cierre sin drift)

---

## Cabecera

| Campo                 | Valor                                                          |
| --------------------- | -------------------------------------------------------------- |
| **ID**                | `SDD-011`                                                      |
| **Dominio**           | `docs`                                                         |
| **Tipo**              | `documentation` + `feature`                                    |
| **Fecha**             | 2026-07-15                                                     |
| **Estado**            | `In Build`                                                     |
| **Versión objetivo**  | `v1.3.0`                                                       |
| **Owner**             | mantenedor                                                     |
| **Prioridad**         | `P1`                                                           |
| **ADRs relacionados** | `ADR-002`                                                      |
| **Dependencias**      | — (complementa SDD-010 en validate-sdd; no bloquea)            |

---

## Problema y objetivo

**Problema:**

El kit mantiene dos carpetas de «releases» con roles distintos:

| Capa | Ruta | Audiencia |
| ---- | ---- | --------- |
| Producto SemVer | `docs/releases/` | Consumidores, GitHub Releases, `upgrade-kit` |
| Campaña SDD | `.github/docs/sdd/releases/` | Mantenedor (acta: specs, gates) |

No son duplicados, pero el dual-write falla: `v1.2.2` tiene acta de campaña y tag, sin `docs/releases/v1.2.2.md` ni enlace «Changelog kit». Unificar ambas carpetas rompería DR-7 y el path de upgrade.

**Objetivo:**

Formalizar el contrato dual-release (fuente de verdad por audiencia), cerrar el drift de `v1.2.2`, endurecer `close-release` / skill para el dogfooding del kit, y añadir WARN en `validate-sdd` cuando exista acta de campaña sin nota de producto.

---

## Alcance

**Incluye:**

- Spec + BACKLOG + contrato documentado en `docs/README.md`, `docs/releases/README.md` y `domain-rules.md` (DR-7 / glosario)
- Backfill `docs/releases/v1.2.2.md` + entrada CHANGELOG + enlace en `release_v1.2.2.md`
- Endurecer `core/prompts/workflow/close-release.md` y `bootstrap/agent-skills/sdd-close-release/`
- Nota en perfil `sdd-kit` (`deploy.md`) alineada al contrato
- WARN en `validate-sdd.ps1` / `.sh`: carpeta campaña `vX.Y.Z` ⇒ falta `docs/releases/vX.Y.Z.md`
- Quitar referencia muerta a `docs/maintainers/` en `docs/README.md`

**Excluye explícitamente:**

- Mover o eliminar `docs/releases/`
- Reescribir GitHub Releases históricos
- Cambiar plantillas de consumidores en `core/releases/` más allá de una nota breve si hace falta
- Convertir el WARN en ERROR en esta iteración

---

## Impacto técnico

> Perfil: `sdd-kit`. Tabla según `profiles/sdd-kit/spec-impact.md`.

| Pregunta                                                              | Respuesta                                                                 |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| ¿Afecta `core/` (workflow, plantillas, guías)?                        | Sí — prompt `close-release`                                               |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)?     | Sí — `profiles/sdd-kit/deploy.md`                                         |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | Sí — `validate-sdd` + skill `sdd-close-release`                           |
| ¿Afecta `cli/` (comandos, librerías)?                                 | No aplica — wrapper delega en validate-sdd                                |
| ¿Afecta `.github/workflows/` o reglas Cursor?                         | No aplica                                                                 |
| ¿Requiere actualizar `README.md` o `INSTALL.md`?                      | No — solo `docs/README.md` / `docs/releases/`                             |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)?                   | Sí — este spec                                                            |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles.   | Sí — refuerzo DR-7 y glosario dual-release                                |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR.          | No — confirma DR-7; alineado a ADR-002                                    |

---

## Reglas de negocio

> Aplica [domain-rules.md](../../../business/domain-rules.md) principios #6, #7 y glosario Release producto / Release campaña. Alineado a [ADR-002](../../adr/ADR-002-2026-07-15-adoptar-harness-engineering-marco-conceptual.md).

Particularidad: la acta de campaña es **sensor** documental del cierre; la nota SemVer es **guía** para consumidores. La acta debe enlace a la nota; no al revés como dependencia.

---

## Criterios de aceptación

**Happy path:**

- [x] Contrato dual documentado en `docs/README.md` y `docs/releases/README.md` (sin unificar carpetas)
- [x] `domain-rules.md` menciona dual-write obligatorio al cerrar versión del kit
- [x] Existe `docs/releases/v1.2.2.md` + entrada en CHANGELOG; `release_v1.2.2.md` enlaza Changelog kit
- [x] `close-release` y skill `sdd-close-release` exigen dual-write cuando el cierre es del producto kit
- [x] `validate-sdd` emite WARN si hay `sdd/releases/vX.Y.Z/` y falta `docs/releases/vX.Y.Z.md` (solo si existe `docs/releases/` en la raíz del proyecto)
- [x] `docs/README.md` no referencia `docs/maintainers/`
- [x] `python cli/sdd.py validate` / `validate-sdd` sin errores (WARN dual-release solo si aplica)

**Error path:**

- [x] Si falta nota producto con acta presente → WARN (no FAIL) en validate-sdd
- [x] Consumidores sin `docs/releases/` en raíz → check dual-release no aplica

---

## Diseño técnico

**Contrato (normativo):**

1. Cada tag SemVer del kit requiere `docs/releases/vX.Y.Z.md` + entrada en `CHANGELOG.md`.
2. Cada cierre de campaña requiere `.github/docs/sdd/releases/vX.Y.Z/release_vX.Y.Z.md` con campo **Changelog kit** apuntando a (1).
3. No duplicar narrativa larga: la acta resume + enlaza; el detalle vive en la nota de producto.
4. Consumidores leen solo `docs/releases/`.

---

## Verificación técnica

```bash
python cli/sdd.py validate
# PowerShell:
.\bootstrap\validate-sdd.ps1 .github/docs/sdd
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| WARN molesta en CI que trate warnings como fail | Baja | Medio | WARN documentado; no ERROR aún |
| close-release confunde consumidores | Baja | Medio | Dual-write solo si existe capa producto (`docs/releases/`) o perfil sdd-kit |

Rollback: revertir archivos individuales; sin migración de datos.

---

## Notas

- Investigación previa: plan «Contrato dual release»; evidencia de drift en v1.2.2.
- Industria: Keep a Changelog / SemVer (público) vs shipping checklist (proceso) — no unificar.
