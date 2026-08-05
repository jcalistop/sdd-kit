# Release campaña v1.3.1 — Archivar specs Descartado

## Cabecera

| Campo                | Valor                                               |
| -------------------- | --------------------------------------------------- |
| **Versión**          | **`v1.3.1`**                                        |
| **Fecha cierre**     | 2026-08-05                                          |
| **Tipo**             | patch                                               |
| **Responsable**      | mantenedor                                          |
| **Campaña anterior** | [v1.3.0](../v1.3.0/release_v1.3.0.md)               |
| **Changelog kit**    | [v1.3.1.md](../../../../../docs/releases/v1.3.1.md) |

---

## Información general

Patch que permite archivar specs en estado terminal **Descartado** junto a **Released**: validadores, workflow, plantillas y prompts de agente. Sin stub en `specs/` tras el `git mv`.

---

## Specs incluidas

| ID      | Dominio | Spec archivado                                                                                                         |
| ------- | ------- | ---------------------------------------------------------------------------------------------------------------------- |
| SDD-015 | core    | [archive/2026/core/SDD-015-archive-specs-descartados.md](../../archive/2026/core/SDD-015-archive-specs-descartados.md) |

## Cambios sin spec

| Dominio | Cambio |
| ------- | ------ |
| —       | —      |

---

## Validación de cierre

| Gate           | Resultado                                                                          |
| -------------- | ---------------------------------------------------------------------------------- |
| `sdd validate` | 0 errores (WARN kit-version pre-tag; WARN metrics históricos; WARN agent manifest) |
| `validate-sdd` | OK (0 errores)                                                                     |
| Tag producto   | `v1.3.1` (pendiente confirmación humana / GitHub Release)                          |

---

## Pendientes post-release (no bloquean)

| Ítem                         | Origen    | Nota                |
| ---------------------------- | --------- | ------------------- |
| Suite pytest CLI             | Discovery | CI hoy `compileall` |
| Dashboard Canvas de métricas | Discovery | Excluido de SDD-013 |

---

## Consumidores

Instancias en `v1.3.0` deben actualizar a `v1.3.1` — ver [`docs/releases/v1.3.1.md`](../../../../../docs/releases/v1.3.1.md). Migrar specs `Deprecated`/Descartado que sigan en `specs/` a `archive/` con cabecera `Descartado`.
