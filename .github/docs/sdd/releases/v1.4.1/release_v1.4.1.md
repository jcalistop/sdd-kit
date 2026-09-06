# Release campaña v1.4.1 — Higiene agentica, CI validate, docs

## Cabecera

| Campo                | Valor                                               |
| -------------------- | --------------------------------------------------- |
| **Versión**          | **`v1.4.1`**                                        |
| **Fecha cierre**     | 2026-09-06                                          |
| **Tipo**             | patch                                               |
| **Responsable**      | mantenedor                                          |
| **Campaña anterior** | [v1.4.0](../v1.4.0/release_v1.4.0.md)               |
| **Changelog kit**    | [v1.4.1.md](../../../../../docs/releases/v1.4.1.md) |

---

## Información general

Patch de higiene y confianza operativa: retira residual `sdd-core.mdc`, cablea `sdd validate` en CI (incl. rama `dev`), alinea upgrade-kit a v1.3.2/`agent.targets`, e indexa `audits`/`research` + banner snapshot en ANALYSIS. Sin cambio de API para consumidores.

---

## Specs incluidas

| ID      | Dominio   | Spec archivado |
| ------- | --------- | -------------- |
| SDD-018 | bootstrap | [archive/2026/bootstrap/SDD-018-higiene-agentica-sdd-core.md](../../archive/2026/bootstrap/SDD-018-higiene-agentica-sdd-core.md) |
| SDD-019 | infra     | [archive/2026/infra/SDD-019-ci-validate-sdd-rama-dev.md](../../archive/2026/infra/SDD-019-ci-validate-sdd-rama-dev.md) |
| SDD-020 | bootstrap | [archive/2026/bootstrap/SDD-020-upgrade-paridad-multi-agente.md](../../archive/2026/bootstrap/SDD-020-upgrade-paridad-multi-agente.md) |
| SDD-021 | docs      | [archive/2026/docs/SDD-021-indice-audits-research-banner-analysis.md](../../archive/2026/docs/SDD-021-indice-audits-research-banner-analysis.md) |

## Cambios sin spec

| Dominio | Cambio |
| ------- | ------ |
| cli     | Fix CI: `validate-sdd.sh` vía `bash` + mode `100755` (PermissionError en Linux) |
| docs    | Plan auditoría dogfood consumidor externo (sin SDD; SemVer —) |

---

## Validación de cierre

| Gate           | Resultado                                                 |
| -------------- | --------------------------------------------------------- |
| `sdd validate` | 0 errores (WARN kit-version pre-tag posible)              |
| CI             | Step validate en verde en `dev` tras fix bash             |
| Tag producto   | `v1.4.1` (pendiente merge a main / confirmación humana)   |

---

## Pendientes post-release (no bloquean)

| Ítem | Origen | Nota |
| ---- | ------ | ---- |
| Dogfood consumidor externo | audits | Plan listo; corrida post-tag |
| Perfiles adicionales on-demand | Discovery | minor |
| Ampliar validate-sdd (H-C04) | deuda | — |

---

## Consumidores

Instancias en `v1.4.0` → `v1.4.1`: ver [`docs/releases/v1.4.1.md`](../../../../../docs/releases/v1.4.1.md). Reinstalar agentes si cambió skills; borrar `sdd-core.mdc` huérfano si quedó.
