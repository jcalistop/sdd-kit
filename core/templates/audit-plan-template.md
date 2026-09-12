# Plantilla — Plan de auditoría (solo grandes)

> **Opcional.** Usar solo si la auditoría es grande o el alcance debe congelarse/aprobarse **antes** de ejecutar.
> Corridas cortas (p. ej. dogfood): usar solo [`audit-registro-template.md`](audit-registro-template.md).
> Copiar a `paths.sdd/audits/YYYYMMDD-slug.md` y enlazar el registro/informe hermano.
> Agnóstica al stack (sin frameworks concretos).

---

| Campo | Valor |
| ----- | ----- |
| **ID archivo** | `YYYYMMDD-slug` |
| **Tipo** | Plan de auditoría |
| **Estado** | `Pendiente` / `En curso` / `Ejecutado` |
| **Fecha plan** | YYYY-MM-DD |
| **Fecha cierre** | YYYY-MM-DD _(al Ejecutado)_ |
| **Registro / informe** | [enlace al hermano] |
| **Versión / tag referenciado** | |
| **Alcance** | |
| **Fuera de alcance** | |

---

## Objetivo

## Exclusiones

## Prerrequisitos

- [ ]

## Método / pasos (alcance congelado)

| Paso | Acción | Evidencia esperada |
| ---- | ------ | ------------------ |
| A |  |  |

> No rellenar resultados aquí si el hermano es el registro: los OK/FAIL y gaps viven en el registro/informe.

## Criterio de cierre

- [ ] Registro/informe hermano Ejecutado
- [ ] Este plan → `Ejecutado` y mergeado junto al registro
- [ ] Stub del tag ≠ SoT post-corrida
