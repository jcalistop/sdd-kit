# SDD-016 — Deprecar métricas de tokens y cost-governance

---

## Cabecera

| Campo                 | Valor                                                                 |
| --------------------- | --------------------------------------------------------------------- |
| **ID**                | `SDD-016`                                                             |
| **Dominio**           | `core`                                                                |
| **Tipo**              | `feature`                                                             |
| **Fecha**             | 2026-09-05                                                            |
| **Estado**            | `In Build`                                                            |
| **Versión objetivo**  | `v1.4.0`                                                              |
| **Owner**             | mantenedor                                                            |
| **Prioridad**         | `P1`                                                                  |
| **ADRs relacionados** | —                                                                     |
| **Dependencias**      | SDD-012 (governance A–F); SDD-013 (observabilidad tokens)             |

---

## Problema y objetivo

**Problema:**

La observabilidad de tokens (`sdd metrics tokens`, `token-usage.json`, WARNs en validate-sdd) y la skill `sdd-cost-governance` (propuesta D de SDD-012) no entregan dato útil: Cursor no expone usage por API; el registro manual no forma parte del ritual `close-release`; la heurística por tamaño de spec engaña. Mantener esa superficie finge gobernanza económica que el kit no puede medir.

**Objetivo:**

Retirar del kit la metering de tokens y la skill de cost-governance. Conservar optimizaciones de harness A/B/C/F (two-zone, scoping, compact, threshold) y el comando `sdd metrics` de salud del proceso. Documentar el breaking change en upgrade-guide hacia `v1.4.0`.

---

## Alcance

**Incluye:**

- Eliminar subcomando `sdd metrics tokens` y funciones de tokens en `cli/lib/metrics.py`
- Eliminar `paths.sdd/metrics/token-usage.json` + README de tokens (y el directorio si queda vacío)
- Quitar WARNs de token-usage / outliers en `validate-sdd.ps1` / `.sh`
- Borrar skill `sdd-cost-governance` y su entrada `session_start` en `bootstrap/agent-skills/manifest.json`
- Quitar referencias en `sdd-build-spec`, `sdd-upgrade-kit/reference.md`, `core/workflow.md` (sección Governance de costo), README, `cli/README.md`, `core/upgrade-guide.md`
- Quitar de BACKLOG el ítem Discovery “Dashboard Canvas de métricas SDD”
- Nota de migración: consumidores 1.3.x → la skill ya no se instala

**Excluye explícitamente:**

- Revertir A/B/C/F de SDD-012 (two-zone, grafo, compact, threshold)
- Reescribir research `2026-07-15-token-economics-sdd-harness.md`
- Marcar Descartado los specs archivados SDD-012 / SDD-013 (permanecen Released históricos)
- Integración con APIs de pricing o telemetría del IDE
- Dashboard Canvas

---

## Impacto técnico

| Pregunta                                                              | Respuesta |
| --------------------------------------------------------------------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)?                        | Sí — `workflow.md`, `upgrade-guide.md` |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)?     | No aplica — no cambia perfiles |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | Sí — validate-sdd, agent-skills (borrar cost-governance), build-spec, upgrade-kit |
| ¿Afecta `cli/` (comandos, librerías)?                                 | Sí — `sdd.py`, `lib/metrics.py` |
| ¿Afecta `.github/workflows/` o reglas Cursor?                         | Indirecto — skills instaladas vía install-agents |
| ¿Requiere actualizar `README.md` o `INSTALL.md`?                      | Sí — README y cli/README; INSTALL solo si menciona tokens |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)?                   | Sí — este spec, BACKLOG, borrar metrics/, `ids.next_sdd` |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles.   | DR-1, DR-4, DR-6, DR-7 |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR.          | No — retiro de observabilidad; no nuevo ADR |

---

## Reglas de negocio

Aplica [`domain-rules.md`](../../../business/domain-rules.md):

- **DR-1:** Core sin acoplar a IDE concreto en la API pública restante de la CLI.
- **DR-4:** Retiro no salta gates Ready/merge; humano aprueba.
- **DR-6:** Spec y métricas bajo `paths.sdd`.
- **DR-7:** Breaking change documentado en `docs/releases/` + upgrade-guide (producto), no solo acta campaña.

---

## Criterios de aceptación

**Happy path:**

- [x] `python cli/sdd.py metrics tokens …` falla (subcomando inexistente / uso desconocido)
- [x] `python cli/sdd.py metrics` (salud del proceso) sigue OK
- [x] `validate-sdd` sin WARN de `token-usage` / outliers
- [x] Skill `sdd-cost-governance` ausente del manifest y del árbol `bootstrap/agent-skills/`
- [x] Docs públicas y `workflow.md` sin referencias operativas a metering / governance skill
- [x] `python -m compileall -q cli/` en verde
- [x] `python cli/sdd.py validate` sin errores
- [x] `upgrade-guide.md` menciona retiro en v1.4.0

**Error path:**

- [x] Invocar `metrics tokens` no cae con traceback no controlado (argparse usage / exit ≠ 0)

---

## Diseño técnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `cli/sdd.py` | Quitar parser/handlers `metrics tokens` |
| `cli/lib/metrics.py` | Dejar solo salud del proceso |
| `bootstrap/validate-sdd.ps1` / `.sh` | Quitar bloque token-usage |
| `bootstrap/agent-skills/sdd-cost-governance/` | Eliminar |
| `bootstrap/agent-skills/manifest.json` | Quitar entrada |
| `bootstrap/agent-skills/sdd-build-spec/SKILL.md` | Quitar paso cost-governance |
| `bootstrap/agent-skills/sdd-upgrade-kit/reference.md` | Migración / quitar checks tokens |
| `core/workflow.md` | Eliminar sección Governance de costo |
| `core/upgrade-guide.md` | Breaking change v1.4.0 |
| `.github/docs/sdd/metrics/` | Eliminar |
| README / cli/README | Quitar ejemplos |

---

## Verificación técnica

```bash
python -m compileall -q cli/
python cli/sdd.py metrics
python cli/sdd.py metrics tokens --summary   # debe fallar
python cli/sdd.py validate
# + validate-sdd.ps1 / .sh sin WARN metrics tokens
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Consumidores 1.3.x esperan la skill | Media | Bajo | upgrade-guide + CHANGELOG |
| Scripts externos llaman `metrics tokens` | Baja | Bajo | Documentar retiro; exit ≠ 0 |

**Rollback:** revertir PR de esta rama.

---

## Notas post-implementación

- Specs SDD-012/013 permanecen `Released` en archive (histórico).
- A/B/C/F de SDD-012 no se revierten (salvo skill D retirada).
- **2026-09-05 (verify):** compileall OK; `metrics` OK; `metrics tokens` → exit 2 argparse; `sdd validate` + `validate-sdd.ps1` 0 errores / 0 WARN tokens; manifest sin cost-governance.
