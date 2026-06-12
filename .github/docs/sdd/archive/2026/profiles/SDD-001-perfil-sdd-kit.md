# SDD-001 — Perfil sdd-kit para mantenedores

---

## Cabecera

| Campo                 | Valor                                                       |
| --------------------- | ----------------------------------------------------------- |
| **ID**                | `SDD-001`                                                   |
| **Dominio**           | `profiles`                                                  |
| **Tipo**              | `feature`                                                   |
| **Fecha**             | 2026-06-12                                                  |
| **Estado**            | `Released`                                                  |
| **Versión objetivo**  | v1.1.0                                                      |
| **Owner**             | mantenedor                                                  |
| **Prioridad**         | `P1`                                                        |
| **ADRs relacionados** | —                                                           |
| **Dependencias**      | Adopción SDD Etapa 1 (documentación en `.github/docs/sdd/`) |

---

## Problema y objetivo

**Problema:**

La instancia SDD del repositorio `sdd-kit` usaba `stack.profile: python-fastapi` como placeholder. Ese perfil asume una API REST con pytest/ruff/mypy, lo que no refleja los quality gates reales del kit (CLI Python, validación JSON, verificación de perfiles).

**Objetivo:**

Crear el perfil `profiles/sdd-kit/` para quienes mantienen el repositorio del kit, con checklist, spec-impact y deploy alineados a la CI existente, y activarlo en la instancia SDD del propio repo.

---

## Alcance

**Incluye:**

- Carpeta `profiles/sdd-kit/` con archivos obligatorios del profile-template
- Prompt `bootstrap/agent-prompts/stacks/sdd-kit.md` y entrada en `stack-descriptions.json`
- Regla Cursor generada vía `sync-cursor-rules.py`
- Spec de ejemplo en `profiles/sdd-kit/examples/`
- Actualizar instancia: `stack.profile: sdd-kit` en `.github/docs/sdd/sdd.config.yaml`
- Entradas en `README.md` e `INSTALL.md`

**Excluye explícitamente:**

- Cambios en `core/workflow.md` o ciclo SDD
- Nuevo job CI (la CI actual ya valida perfiles genéricamente)
- Perfiles de stacks consumidores (Laravel, React, etc.)

---

## Impacto técnico

| Pregunta                                        | Respuesta                                                                   |
| ----------------------------------------------- | --------------------------------------------------------------------------- |
| ¿Afecta `core/`?                                | No aplica — solo nuevo perfil                                               |
| ¿Afecta `bootstrap/` (scripts, agent-prompts)?  | Sí — `stacks/sdd-kit.md`, `stack-descriptions.json`, cursor-rules generadas |
| ¿Afecta `cli/`?                                 | No — solo documentación de gates existentes                                 |
| ¿Afecta `.github/workflows/ci.yml`?             | No aplica — gates ya cubiertos                                              |
| ¿Requiere `db-change`?                          | No aplica                                                                   |
| ¿Afecta reglas en `business/domain-rules.md`?   | Sí — refuerza invariantes 1–3 (core agnóstico, perfiles autocontenidos)     |
| ¿Introduce decisión arquitectónica transversal? | No                                                                          |

---

## Reglas de negocio

- Perfil sin reglas de negocio de proyectos consumidores (domain-rules.md § invariantes 1–3).
- Documentación en español latino (Chile).

---

## Criterios de aceptación

**Happy path:**

- [x] `profiles/sdd-kit/` existe con README, sdd.config.yaml, checklist, spec-impact, deploy, release-deploy-section, branching-extensions, examples/
- [x] `bootstrap/agent-prompts/stacks/sdd-kit.md` y entrada en `stack-descriptions.json`
- [x] `sync-cursor-rules.py` genera `sdd-stack-sdd-kit.mdc`
- [x] `.github/docs/sdd/sdd.config.yaml` → `stack.profile: sdd-kit`
- [x] `validate-sdd` en verde
- [x] README e INSTALL listan el perfil `sdd-kit`

**Error path:**

- [x] Si falta archivo obligatorio del perfil, CI del kit falla en job `validate`
- [x] Perfil no incluye referencias a dominio de un proyecto consumidor

---

## Diseño técnico

**Archivos principales:**

| Archivo                                           | Cambio                      |
| ------------------------------------------------- | --------------------------- |
| `profiles/sdd-kit/*`                              | Nuevo perfil completo       |
| `bootstrap/agent-prompts/stacks/sdd-kit.md`       | Prompt de stack             |
| `bootstrap/agent-prompts/stack-descriptions.json` | Entrada `sdd-kit`           |
| `bootstrap/cursor-rules/sdd-stack-sdd-kit.mdc`    | Generado por sync           |
| `.github/docs/sdd/sdd.config.yaml`                | `stack.profile: sdd-kit`    |
| `README.md`, `INSTALL.md`                         | Tabla de perfiles           |
| `core/templates/profile-template.md`              | Fila en tabla de referencia |

---

## Riesgos y rollback

| Riesgo                         | Mitigación                                                         |
| ------------------------------ | ------------------------------------------------------------------ |
| Confusión con perfiles de apps | Nombre explícito `sdd-kit`; solo para repo del kit                 |
| Rollback                       | Revertir PR; restaurar `python-fastapi` en sdd.config de instancia |
