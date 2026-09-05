# Release campaña v1.3.2 — Retiro metering tokens / cost-governance

## Cabecera

| Campo                | Valor                                               |
| -------------------- | --------------------------------------------------- |
| **Versión**          | **`v1.3.2`**                                        |
| **Fecha cierre**     | 2026-09-05                                          |
| **Tipo**             | patch (breaking menor documentado)                  |
| **Responsable**      | mantenedor                                          |
| **Campaña anterior** | [v1.3.1](../v1.3.1/release_v1.3.1.md)               |
| **Changelog kit**    | [v1.3.2.md](../../../../../docs/releases/v1.3.2.md) |

---

## Información general

Patch que retira la observabilidad heurística de tokens (`sdd metrics tokens`, `token-usage.json`, WARNs validate-sdd) y la skill `sdd-cost-governance`. Cursor no expone usage por API; los datos no informaban gobernanza real. Se conservan two-zone, compact, scoping y threshold (A/B/C/F de SDD-012 salvo skill D).

---

## Specs incluidas

| ID      | Dominio | Spec archivado                                                                                                                   |
| ------- | ------- | -------------------------------------------------------------------------------------------------------------------------------- |
| SDD-016 | core    | [archive/2026/core/SDD-016-deprecar-tokens-cost-governance.md](../../archive/2026/core/SDD-016-deprecar-tokens-cost-governance.md) |

## Cambios sin spec

| Dominio | Cambio |
| ------- | ------ |
| —       | —      |

---

## Validación de cierre

| Gate           | Resultado                                                                          |
| -------------- | ---------------------------------------------------------------------------------- |
| `sdd validate` | 0 errores (WARN kit-version pre-tag: installed v1.3.2 vs disco v1.3.1-1-g…)       |
| `validate-sdd` | OK (0 errores, 1 WARN kit-version)                                                 |
| Tag producto   | `v1.3.2` (pendiente confirmación humana / GitHub Release)                          |

---

## Pendientes post-release (no bloquean)

| Ítem                         | Origen    | Nota                |
| ---------------------------- | --------- | ------------------- |
| Suite pytest CLI             | Discovery | CI hoy `compileall` |
| Dogfooding consumidor externo | Discovery | —                   |

---

## Consumidores

Instancias en `v1.3.1` deben actualizar a `v1.3.2` — ver [`docs/releases/v1.3.2.md`](../../../../../docs/releases/v1.3.2.md). Reinstalar agentes y borrar skill huérfana `sdd-cost-governance` si quedó en `.cursor/skills/`.
