# Spec Template — SDD

> Copiar como `specs/<dominio>/SDD-NNN-slug.md`. Al cerrar: `git mv` a `archive/<YYYY>/<dominio>/`.

---

## Cabecera

| Campo                 | Valor                                                                             |
| --------------------- | --------------------------------------------------------------------------------- |
| **ID**                | `SDD-NNN`                                                                         |
| **Dominio**           | _(ver `sdd.config.yaml` → domains)_                                               |
| **Tipo**              | `feature` / `bugfix` / `refactor` / `performance` / `db-change` / `documentation` |
| **Fecha**             | YYYY-MM-DD                                                                        |
| **Estado**            | `Draft` / `Ready` / `In Build` / `Validating` — `Released` solo en `archive/`     |
| **Versión objetivo**  | vX.Y.Z                                                                            |
| **Owner**             | nombre                                                                            |
| **Prioridad**         | `P0` / `P1` / `P2` / `P3`                                                         |
| **ADRs relacionados** | `ADR-NNN` _(0..N)_                                                                |
| **Dependencias**      | otros `SDD-NNN` _(vacío si no aplica)_                                            |

---

## Problema y objetivo

**Problema:**

**Objetivo:**

---

## Alcance

**Incluye:**

**Excluye explícitamente:**

---

## Impacto técnico

> Completar la tabla del **perfil stack** (`profiles/<stack>/spec-impact.md`). Si no aplica un ítem: "No aplica — razón".

_(Insertar tabla del perfil o enlazar sección copiada aquí.)_

---

## Reglas de negocio

- ***

## Criterios de aceptación

**Happy path:**

- [ ]

**Error path:**

- [ ]

---

## Cambio de BD _(solo si incluye `db-change`)_

**Contexto:**

**Objetos afectados:**

| Objeto | Tipo de cambio | Detalle |
| ------ | -------------- | ------- |
|        |                |         |

**Riesgos / rollback / validación post-ejecución:**

---

## Diseño técnico _(obligatorio feature/refactor; opcional bugfix)_

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
|         |        |

---

## Verificación técnica

_(Comandos del perfil stack — tests, lint, build.)_

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
|        |              |         |            |

---

## Notas post-implementación

-
