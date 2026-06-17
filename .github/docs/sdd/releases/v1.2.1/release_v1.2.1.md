# Release campaña v1.2.1 — Fix bootstrap `sdd.config.yaml`

## Cabecera

| Campo                | Valor                                         |
| -------------------- | --------------------------------------------- |
| **Versión**          | **`v1.2.1`**                                  |
| **Fecha cierre**     | 2026-06-17                                    |
| **Tipo**             | patch / bootstrap                             |
| **Responsable**      | equipo                                        |
| **Campaña anterior** | [v1.2.0](../../../docs/releases/v1.2.0.md)    |
| **Changelog kit**    | [v1.2.1.md](../../../docs/releases/v1.2.1.md) |

---

## Información general

Corrección en `install-agents.py`: al reinstalar configuración de agente, se preserva el bloque `kit:` (`installed_version`, `installed_at`) en `sdd.config.yaml`. **Narrativa completa:** [v1.2.1.md](../../../docs/releases/v1.2.1.md).

---

## Specs incluidas

| ID | Dominio   | Spec archivado |
| -- | --------- | -------------- |
| —  | bootstrap | Sin spec (bugfix puntual) |

---

## Validación de cierre

| Gate           | Resultado |
| -------------- | --------- |
| `sdd validate` | 0 errores |
| `validate-sdd` | OK        |
| Tag producto   | `v1.2.1`  |

---

## Consumidores

Instancias en `v1.2.0` deben bump submodule a `v1.2.1` y ejecutar `install-agents.py` si reinstalan agente tras upgrade.
