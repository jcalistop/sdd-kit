# Operaciones SDD

Guía de **quién actualiza qué** y **rituales**. Detalle normativo en [`workflow.md`](workflow.md) y [`branching.md`](branching.md).

---

## Matriz de responsabilidades

| Artefacto                           | Quién                  | Cuándo                              |
| ----------------------------------- | ---------------------- | ----------------------------------- |
| `BACKLOG.md`                        | Tech lead / PO         | Revisión semanal; al cambiar estado |
| _Próximo ID disponible_             | Líder backlog          | Al asignar `SDD-NNN` nuevo          |
| Spec en `specs/`                    | Owner                  | Draft → Validating                  |
| `checklist-pr.md` + perfil stack    | Autor + revisor        | Validating                          |
| `releases/vX.Y.Z/release_vX.Y.Z.md` | Release owner          | Cierre en dev antes de campaña      |
| `archive/`                          | Release owner / Owner  | Antes de PR de campaña              |
| Sync prod → dev post-tag            | Release owner          | Inmediato tras tag                  |
| ADR                                 | Tech lead / arquitecto | Decisión transversal                |
| `business/` (si existe)             | PO / tech lead         | Cambios duraderos de producto       |

---

## Revisión semanal (~30 min)

1. Actualizar estados en BACKLOG; Discovery → Draft (asignar ID + spec).
2. Ítems sin avance (>2 semanas) → descartar o replanificar.
3. Versión objetivo y dependencias entre `SDD-NNN`.
4. Decisiones transversales → spec o ADR.

Participantes: tech lead, PO, owners con ítems activos.

---

## Extensiones del perfil stack

Rituales específicos (Dependabot, deploy, smoke): ver `profiles/<stack>/` y `sdd.config.yaml` → `stack.profile`.
