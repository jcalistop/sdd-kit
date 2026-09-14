# Release campaña v1.6.0 — Guías, Verify, Congelado, upgrade de consumo

## Cabecera

| Campo                | Valor                                               |
| -------------------- | --------------------------------------------------- |
| **Versión**          | **`v1.6.0`**                                        |
| **Fecha cierre**     | 2026-09-13                                          |
| **Tipo**             | minor                                               |
| **Responsable**      | mantenedor                                          |
| **Campaña anterior** | [v1.5.0](../v1.5.0/release_v1.5.0.md)               |
| **Changelog kit**    | [v1.6.0.md](../../../../../docs/releases/v1.6.0.md) |

---

## Información general

Minor de producto: layout `core/guides/`, metodologías audits/research, Congelado opcional, tablas Verify por perfil, skills (profile + fail-closed), README de producto, y contrato de upgrade (§ v1.6.0 + skill) para saltos desde ≤v1.2 con un solo tag.

---

## Specs incluidas

| ID      | Dominio   | Spec archivado |
| ------- | --------- | -------------- |
| SDD-024 | core      | [archive/2026/core/SDD-024-congelado-para-implementacion.md](../../archive/2026/core/SDD-024-congelado-para-implementacion.md) |
| SDD-025 | profiles  | [archive/2026/profiles/SDD-025-verify-tabla-comandos-perfil.md](../../archive/2026/profiles/SDD-025-verify-tabla-comandos-perfil.md) |
| SDD-026 | docs      | [archive/2026/docs/SDD-026-metodologia-auditorias-plantillas.md](../../archive/2026/docs/SDD-026-metodologia-auditorias-plantillas.md) |
| SDD-027 | docs      | [archive/2026/docs/SDD-027-metodologia-research-plantilla.md](../../archive/2026/docs/SDD-027-metodologia-research-plantilla.md) |
| SDD-028 | core      | [archive/2026/core/SDD-028-guides-audits-research-core.md](../../archive/2026/core/SDD-028-guides-audits-research-core.md) |
| SDD-029 | core      | [archive/2026/core/SDD-029-reordenar-guias-core-guides.md](../../archive/2026/core/SDD-029-reordenar-guias-core-guides.md) |
| SDD-030 | bootstrap | [archive/2026/bootstrap/SDD-030-skills-stack-profile-install.md](../../archive/2026/bootstrap/SDD-030-skills-stack-profile-install.md) |
| SDD-031 | bootstrap | [archive/2026/bootstrap/SDD-031-build-spec-fail-closed-plan-mode.md](../../archive/2026/bootstrap/SDD-031-build-spec-fail-closed-plan-mode.md) |
| SDD-032 | docs      | [archive/2026/docs/SDD-032-reestructurar-readme-raiz.md](../../archive/2026/docs/SDD-032-reestructurar-readme-raiz.md) |
| SDD-033 | bootstrap | [archive/2026/bootstrap/SDD-033-upgrade-gaps-v160.md](../../archive/2026/bootstrap/SDD-033-upgrade-gaps-v160.md) |

## Cambios sin spec

| Dominio | Cambio |
| ------- | ------ |
| —       | Ninguno relevante en esta campaña |

---

## Validación de cierre

| Gate           | Resultado |
| -------------- | --------- |
| `sdd validate` | 0 errores (2026-09-13; kit-version aún `v1.5.0` hasta tag) |
| Tag producto   | Pendiente confirmación humana (Fase 3 RUNBOOK) |

---

## Pendientes post-release (no bloquean)

| Ítem | Origen | Nota |
| ---- | ------ | ---- |
| Tag + GitHub Release | deploy.md | Tras merge a `main` / confirmación |
| Smoke upgrade en consumidor externo desde v1.2 | SDD-033 | Diferido |

---

## Consumidores

Instancias en `v1.5.0` (o ≤v1.2): ver [`docs/releases/v1.6.0.md`](../../../../../docs/releases/v1.6.0.md) y [`core/guides/upgrade-guide.md`](../../../../../core/guides/upgrade-guide.md) § v1.6.0. Reinstall agents obligatorio.
