# Plantilla — Registro de auditoría

> **Default** para toda corrida. Copiar a `paths.sdd/audits/YYYYMMDD-slug.md`.
> Metodología: instancia SDD → `audits/METODOLOGIA.md` (repo kit) o equivalente.
> Agnóstica al stack (sin frameworks concretos).

---

| Campo | Valor |
| ----- | ----- |
| **ID archivo** | `YYYYMMDD-slug` |
| **Tipo** | Registro de auditoría |
| **Estado** | `Pendiente` / `En curso` / `Ejecutado` |
| **Fecha inicio** | YYYY-MM-DD |
| **Fecha cierre** | YYYY-MM-DD _(al Ejecutado)_ |
| **Versión / tag referenciado** | _(p. ej. vX.Y.Z o —)_ |
| **Alcance** | _(qué se evalúa)_ |
| **Plan hermano** | — _(solo si auditoría grande; enlace)_ |
| **SemVer kit** | `patch` / `minor` / `major` / `—` |

---

## Objetivo

_(Qué se quiere validar o descubrir.)_

## Exclusiones

- 

## Método / pasos

| Paso | Acción | Resultado |
| ---- | ------ | --------- |
| 1 |  | Pendiente / OK / FAIL |

## Resultados

**Resumen:**

**OK/FAIL por paso:** _(completar al cerrar)_

## Gaps

| ID | Hallazgo | Acción sugerida | SemVer | Prioridad |
| -- | -------- | --------------- | ------ | --------- |
| 1 |  | Discovery / SDD / trivial / no hacer | patch / — | P0–P3 |

**Severidad:** P0 bloquea · P1 degrada confianza · P2 fricción · P3 nice-to-have.

## Cierre

- [ ] Estado → `Ejecutado`
- [ ] Gaps en BACKLOG o specs (o descartados aquí)
- [ ] Índice `paths.sdd/README.md` actualizado
- [ ] Merge a rama de desarrollo; a producción/`main` en el próximo patch como máximo
- [ ] Stub en tag (si existe) **no** se cita como SoT — gana este registro mergeado
