# Operaciones SDD

Guía de **quién actualiza qué** y **rituales**. Detalle normativo en [`workflow.md`](workflow.md) y [`branching.md`](branching.md).

---

## Modo desarrollador solo (recomendado)

Una persona + agente de IA. No hay roles separados: el humano decide y aprueba; el agente ejecuta el ciclo SDD.

| Artefacto                        | Quién                                   | Cuándo                                    |
| -------------------------------- | --------------------------------------- | ----------------------------------------- |
| `BACKLOG.md`                     | Humano o agente                         | Al cambiar estado de cualquier iniciativa |
| _Próximo ID disponible_          | Agente (validar con humano)             | Al crear spec nuevo                       |
| Spec en `specs/`                 | Agente                                  | Discovery → Validating                    |
| Revisión de spec (Ready)         | **Humano aprueba**                      | Antes de In Build                         |
| Código + PR                      | Agente                                  | In Build → Validating                     |
| Merge PR                         | **Humano aprueba**                      | Tras DoD verde                            |
| `checklist-pr.md` + perfil stack | Agente completa; humano verifica        | Validating                                |
| `releases/vX.Y.Z/`               | Agente prepara; humano confirma versión | Antes de PR campaña                       |
| `archive/` + BACKLOG Released    | Agente                                  | Cierre en dev, antes de campaña           |
| Sync prod → dev post-tag         | Agente o humano                         | Inmediato tras tag                        |
| ADR                              | Agente redacta; humano aprueba          | Decisión transversal                      |
| `business/`                      | Humano (contexto producto)              | Cambios duraderos de negocio              |

### Ritual ligero (~15 min, cuando haga falta)

1. Revisar BACKLOG: ¿algo estancado >2 semanas?
2. ¿Próxima prioridad clara en Discovery?
3. Ejecutar `validate-sdd` si hubo cambios documentales.

No requiere reunión ni calendario fijo.

### Flujo resumido

```
Humano da dirección → Agente: Discovery/Draft → Humano aprueba spec
→ Agente: In Build/PR → Humano merge → Agente: release/archivo
```

Ver regla `sdd-agent-workflow.mdc` para detalle por fase.

---

## Modo equipo (opcional)

Para equipos de 2+ personas, usar matriz extendida:

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

### Revisión semanal (~30 min)

1. Actualizar estados en BACKLOG; Discovery → Draft (asignar ID + spec).
2. Ítems sin avance (>2 semanas) → descartar o replanificar.
3. Versión objetivo y dependencias entre `SDD-NNN`.
4. Decisiones transversales → spec o ADR.

Participantes: tech lead, PO, owners con ítems activos.

---

## Extensiones del perfil stack

Rituales específicos (Dependabot, deploy, smoke): ver `profiles/<stack>/` y `sdd.config.yaml` → `stack.profile`.
