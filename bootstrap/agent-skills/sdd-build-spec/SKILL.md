---
name: sdd-build-spec
description: Aprueba un spec SDD (Draft→Ready→In Build), implementa su alcance y ejecuta verify-implementation antes de Git. Usar cuando el humano aprueba un spec, menciona build-spec, implementar SDD-NNN, verify-implementation, o retoma implementación en Ready/In Build.
---

# SDD Build Spec

Aprobar e implementar un spec **SDD-NNN** según `sdd-agent-workflow`. Incluye gate **verify-implementation** antes de cualquier acción en Git.

**Prohibido sin confirmación humana:** `git commit`, `git push`, abrir PR.

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
- Solo verify → `sdd-verify-implementation` (§ B sin § A).

---

## A. Implementación

1. Draft aprobado → Ready → In Build (spec + BACKLOG).
2. Preguntar rama local según `branching.md` o rama actual.
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
