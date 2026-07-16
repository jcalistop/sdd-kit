# Release campaña v1.3.0 — Agent harness, safe-git, dual-release, métricas y upgrade-kit

## Cabecera

| Campo                | Valor                       |
| -------------------- | --------------------------- |
| **Versión**          | **`v1.3.0`**                |
| **Fecha cierre**     | 2026-07-15                  |
| **Tipo**             | minor                       |
| **Responsable**      | mantenedor                  |
| **Campaña anterior** | [v1.2.2](../v1.2.2/release_v1.2.2.md) |
| **Changelog kit**    | [v1.3.0.md](../../../../../docs/releases/v1.3.0.md) |

---

## Información general

Campaña que formaliza sdd-kit como **agent harness**: contrato safe-git, lenguaje guías/sensores, posicionamiento en docs, observabilidad por componente en `validate-sdd`, contrato dual-release producto↔campaña, governance de tokens (A–F), telemetría heurística `sdd metrics tokens`, y alineación del flujo agentico **`upgrade-kit`** para que los consumidores instalen correctamente esos entregables.

---

## Specs incluidas

| ID      | Dominio   | Spec archivado |
| ------- | --------- | -------------- |
| SDD-007 | core      | [archive/2026/core/SDD-007-contrato-safe-git-agente.md](../../archive/2026/core/SDD-007-contrato-safe-git-agente.md) |
| SDD-008 | core      | [archive/2026/core/SDD-008-lenguaje-harness-guides-sensors.md](../../archive/2026/core/SDD-008-lenguaje-harness-guides-sensors.md) |
| SDD-009 | docs      | [archive/2026/docs/SDD-009-posicionamiento-agent-harness.md](../../archive/2026/docs/SDD-009-posicionamiento-agent-harness.md) |
| SDD-010 | cli       | [archive/2026/cli/SDD-010-observabilidad-componente-validate.md](../../archive/2026/cli/SDD-010-observabilidad-componente-validate.md) |
| SDD-011 | docs      | [archive/2026/docs/SDD-011-contrato-dual-release-producto-campana.md](../../archive/2026/docs/SDD-011-contrato-dual-release-producto-campana.md) |
| SDD-012 | core      | [archive/2026/core/SDD-012-governance-tokens-harness.md](../../archive/2026/core/SDD-012-governance-tokens-harness.md) |
| SDD-013 | cli       | [archive/2026/cli/SDD-013-observabilidad-tokens-metrics.md](../../archive/2026/cli/SDD-013-observabilidad-tokens-metrics.md) |
| SDD-014 | bootstrap | [archive/2026/bootstrap/SDD-014-alinear-flujo-upgrade-kit-v130.md](../../archive/2026/bootstrap/SDD-014-alinear-flujo-upgrade-kit-v130.md) |

## Cambios sin spec

| Dominio | Cambio |
| ------- | ------ |
| —       | —      |

---

## Validación de cierre

| Gate           | Resultado |
| -------------- | --------- |
| `sdd validate` | 0 errores (WARN kit-version pre-tag; WARN metrics sin token-usage) |
| `validate-sdd` | OK (0 errores) |
| Tag producto   | `v1.3.0` (pendiente confirmación humana / GitHub Release) |

---

## Pendientes post-release (no bloquean)

| Ítem | Origen | Nota |
| ---- | ------ | ---- |
| Smoke instancia consumidora (p. ej. Centinela) con kit ≥ v1.3.0 | SDD-007 | Confirmar regla `sdd-safe-git` sin duplicar safe-migrations |
| Dashboard Canvas de métricas | Discovery | Excluido de SDD-013; sigue opcional |
| Suite pytest CLI | Discovery | CI hoy `compileall` |

---

## Consumidores

Instancias en `v1.2.2` deben actualizar a `v1.3.0` con el flujo **`upgrade-kit`** — ver [`docs/releases/v1.3.0.md`](../../../../../docs/releases/v1.3.0.md) y [`core/upgrade-guide.md`](../../../../../core/upgrade-guide.md). Reinstalar agentes es obligatorio para safe-git always-on, skills de cost-governance y reglas two-zone.
