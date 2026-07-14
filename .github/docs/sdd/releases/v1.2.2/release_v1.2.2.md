# Release campaña v1.2.2 — Optimización de tokens en reglas y skills

## Cabecera

| Campo                | Valor                                         |
| -------------------- | --------------------------------------------- |
| **Versión**          | **`v1.2.2`**                                  |
| **Fecha cierre**     | 2026-07-14                                    |
| **Tipo**             | minor / bootstrap                             |
| **Responsable**      | equipo                                        |
| **Campaña anterior** | [v1.2.1](release_v1.2.1.md)                   |
| **Changelog kit**    | —                                             |

---

## Información general

Optimización de consumo de tokens en reglas Cursor (`alwaysApply`), skills y pipeline de generación del kit SDD. Se fusionan reglas redundantes, se mueve "Lectura previa" a skills, se rompen cadenas circulares de verificación, se agrega guía anti-boilerplate en templates y se evita duplicación en instalación de skills.

---

## Specs incluidas

| ID      | Dominio   | Spec archivado                                                                                                     |
| ------- | --------- | ------------------------------------------------------------------------------------------------------------------ |
| SDD-006 | bootstrap | [archive/2026/bootstrap/SDD-006-optimizacion-tokens-kit.md](../../archive/2026/bootstrap/SDD-006-optimizacion-tokens-kit.md) |

## Cambios sin spec

| Dominio   | Cambio                                              |
| --------- | --------------------------------------------------- |
| bootstrap | Dogfooding: spec SDD-006 en `specs/bootstrap/`       |

---

## Validación de cierre

| Gate           | Resultado |
| -------------- | --------- |
| `sdd validate` | 0 errores |
| `validate-sdd` | OK        |
| Tag producto   | `v1.2.2`  |

---

## Consumidores

Instancias en `v1.2.1` deben bump submodule a `v1.2.2`. Cambio no disruptivo: la regla `sdd-core.mdc` se fusionó en `sdd-agent-workflow.mdc`, por lo que consumidores que reinstalen agentes obtendrán una regla `alwaysApply` menos.
