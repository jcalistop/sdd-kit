# Release campaña v1.4.0 — Suite pytest CLI

## Cabecera

| Campo                | Valor                                               |
| -------------------- | --------------------------------------------------- |
| **Versión**          | **`v1.4.0`**                                        |
| **Fecha cierre**     | 2026-09-05                                          |
| **Tipo**             | minor                                               |
| **Responsable**      | mantenedor                                          |
| **Campaña anterior** | [v1.3.2](../v1.3.2/release_v1.3.2.md)               |
| **Changelog kit**    | [v1.4.0.md](../../../../../docs/releases/v1.4.0.md) |

---

## Información general

Minor que añade suite **pytest** para la CLI del kit (backlog, prompts, round-trip `spec new`), integrada en CI y documentada para mantenedores. Cierra H-B01 de la auditoría general 2026-09-05. Sin cambio de API para consumidores.

---

## Specs incluidas

| ID      | Dominio | Spec archivado                                                                                                 |
| ------- | ------- | -------------------------------------------------------------------------------------------------------------- |
| SDD-017 | cli     | [archive/2026/cli/SDD-017-suite-pytest-cli.md](../../archive/2026/cli/SDD-017-suite-pytest-cli.md)             |

## Cambios sin spec

| Dominio | Cambio                                                                 |
| ------- | ---------------------------------------------------------------------- |
| docs    | Artefactos `audits/` 2026-09-05 (plan + informe) versionados en repo   |
| —       | Filas Discovery residuales en BACKLOG (post-auditoría; no bump extra)  |

---

## Validación de cierre

| Gate           | Resultado                                                         |
| -------------- | ----------------------------------------------------------------- |
| `sdd validate` | 0 errores                                                         |
| `pytest`       | 8 passed (`cli/tests`)                                            |
| Smoke manual   | OK (humano, 2026-09-05)                                           |
| Tag producto   | `v1.4.0` (pendiente confirmación humana / GitHub Release)         |

---

## Pendientes post-release (no bloquean)

| Ítem                                      | Origen    | Nota        |
| ----------------------------------------- | --------- | ----------- |
| Higiene `sdd-core.mdc` residual           | Discovery | patch       |
| CI `validate-sdd` + gatillo en `dev`      | Discovery | patch       |
| Upgrade/paridad multi-agente wording      | Discovery | patch       |
| Índice audits + banner ANALYSIS           | Discovery | patch       |
| Dogfooding consumidor externo             | Discovery | —           |
| Perfiles adicionales on-demand            | Discovery | minor       |

---

## Consumidores

Instancias en `v1.3.2` pueden actualizar a `v1.4.0` — ver [`docs/releases/v1.4.0.md`](../../../../../docs/releases/v1.4.0.md). Sin reinstalar agentes obligatoria por esta versión.
