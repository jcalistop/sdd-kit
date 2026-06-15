# Release campaña v1.2.0 — Skills bootstrap + documentación

## Cabecera

| Campo                | Valor                                         |
| -------------------- | --------------------------------------------- |
| **Versión**          | **`v1.2.0`**                                  |
| **Fecha cierre**     | 2026-06-15                                    |
| **Tipo**             | minor / bootstrap + docs                      |
| **Responsable**      | equipo                                        |
| **Campaña anterior** | [v1.1.0](../../../docs/releases/v1.1.0.md)    |
| **Changelog kit**    | [v1.2.0.md](../../../docs/releases/v1.2.0.md) |

---

## Información general

Skills SDD en bootstrap, instalación multi-agente y reordenamiento de documentación (`business/planning/`). **Narrativa completa:** [v1.2.0.md](../../../docs/releases/v1.2.0.md).

---

## Specs incluidas

| ID      | Dominio   | Spec archivado                                                                                                                       |
| ------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| SDD-005 | docs      | [archive/2026/docs/SDD-005-reordenamiento-documentacion-kit.md](../../archive/2026/docs/SDD-005-reordenamiento-documentacion-kit.md) |
| SDD-004 | bootstrap | [archive/2026/bootstrap/SDD-004-agent-skills-cursor.md](../../archive/2026/bootstrap/SDD-004-agent-skills-cursor.md)                 |

---

## Validación de cierre

| Gate           | Resultado |
| -------------- | --------- |
| `sdd validate` | 0 errores |
| `validate-sdd` | OK        |
| Tag producto   | `v1.2.0`  |

---

## Consumidores

Instancias que adopten v1.2.0 deben seguir prompt `upgrade-kit` o spec consumidor equivalente (ej. backoffice **SDD-061**).
