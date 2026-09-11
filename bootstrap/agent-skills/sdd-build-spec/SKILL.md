---
name: sdd-build-spec
description: Aprueba un spec SDD (Draft→Ready→In Build), implementa con guías (domain-rules, perfil) y ejecuta verify-implementation (sensor) antes de Git. Usar cuando el humano aprueba un spec, menciona build-spec, implementar SDD-NNN, verify-implementation, o retoma implementación en Ready/In Build.
---

# SDD Build Spec

Aprobar e implementar un spec **SDD-NNN** según `sdd-agent-workflow`. Incluye gate **verify-implementation** (sensor) antes de cualquier acción en Git.

Usa **guías** (feedforward) al implementar: `domain-rules.md`, perfil stack, alcance del spec. Al terminar aplica **sensores** (feedback): quality gates, verify-implementation, `validate-sdd`.

**Prohibido sin confirmación humana:** `git commit`, `git push`, abrir PR.

**Contexto mínimo requerido** (ver `{{SDD_PATH}}/workflow.md` → grafo de dependencias):

1. Spec del `SDD-NNN` activo — completo (cabecera, alcance, criterios, impacto técnico)
2. `{{SDD_PATH}}/../business/domain-rules.md` — reglas aplicables
3. `.cursor/rules/sdd-stack-{{PROFILE}}.mdc` — quality gates del perfil

**NO leer** specs de otras features ni releases anteriores.
Si el spec referencia un ADR, leer solo ese ADR.

## Rutas (instancia consumidora)

| Artefacto         | Ruta                                        |
| ----------------- | ------------------------------------------- |
| Spec              | `{{SDD_PATH}}/specs/<dominio>/SDD-NNN-*.md` |
| BACKLOG           | `{{SDD_PATH}}/BACKLOG.md`                   |
| Config            | `{{SDD_PATH}}/sdd.config.yaml`              |
| Reglas de negocio | `{{SDD_PATH}}/../business/domain-rules.md`  |
| Ramas             | `{{SDD_PATH}}/branching.md`                 |
| Verificación      | `.cursor/rules/sdd-workflow-reference.mdc`  |
| Perfil stack      | `.cursor/rules/sdd-stack-{{PROFILE}}.mdc`   |

## Cuándo usar

- Humano aprueba spec Draft (`build-spec`, frase de aprobación).
- Retoma implementación en **Ready** o **In Build**.
- Solo verify → usar skill `sdd-verify-implementation` (autosuficiente, checklist inline).

---

## A. Implementación

1. Draft aprobado → Ready → In Build (spec + BACKLOG).
2. Preguntar rama local según `branching.md` o rama actual.

### Ramas / branching

{{BRANCHING_RULES}}

3. Implementar alcance del spec; quality gates del perfil `{{PROFILE}}`.
4. Al terminar → verify § B + **Smoke manual (humano)**.

### Enrutamiento skills de dominio

Activar según señales del spec (skills del proyecto, no SDD): ver [reference.md](reference.md).

### Quality gates

Ver `{{SDD_PATH}}/sdd.config.yaml` → `stack.quality_gates` y [reference.md](reference.md).

---

## B. Verificación

1. Leer spec, `domain-rules.md`, `sdd-workflow-reference`.
2. Criterios de aceptación → evidencia.
3. Arquitectura sana; `python {{KIT_PATH}}/cli/sdd.py validate`.
4. Reporte según plantilla en reference.md.
5. Si OK: preguntar commit (no ejecutar solo).

## Recursos

- [reference.md](reference.md)
- `python {{KIT_PATH}}/cli/sdd.py prompt show build-spec --full`
