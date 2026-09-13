# SDD Build Spec — Referencia

**Fuentes canónicas:** `.cursor/rules/sdd-workflow-reference.mdc` · CLI `{{KIT_PATH}}/cli/sdd.py prompt show <id> --full`

---

## Gate fail-closed — frases (Plan mode / «te guío»)

Cuando hay **señal** (Plan mode, «te guío» / equivalentes, o guía humana activa sin aprobar Ready):

| Válidas (sí pasan a Ready/In Build) | No suficientes (STOP; pedir frase) |
| ----------------------------------- | ----------------------------------- |
| `apruebo SDD-NNN para implementar` | `sigue` / `continúa` |
| `build-spec` / `/sdd-build-spec` (con SDD-NNN o spec adjunto) | `implementa el plan` |
| `apruebo para implementar` / `pasa a Ready e implementa` | `ok` / `dale` (ambiguo, sin nombrar aprobación Ready/build) |

Sin señal: el contrato general no cambia (frase de aprobación o `build-spec` basta).

---

## Transiciones BACKLOG

| De       | A          | Cabecera spec               |
| -------- | ---------- | --------------------------- |
| Draft    | Ready      | `Estado: Ready`             |
| Ready    | In Build   | `Estado: In Build`          |
| In Build | Validating | Tras verify OK + PR abierto |

---

## Convención de ramas

{{BRANCHING_RULES}}

También: tipo del spec y `{{SDD_PATH}}/guides/branching.md`. PR destino habitual (si aplica): **`{{DEV_BRANCH}}`**.

---

## Quality gates — {{PROFILE}}

{{STACK_GATES}}

---

## Enrutamiento skills de dominio (proyecto)

| Señal en spec          | Skill típica (ej. Laravel)       |
| ---------------------- | -------------------------------- |
| PHP/Laravel backend    | `laravel-best-practices`         |
| Tests                  | `pest-testing`                   |
| UI Filament / Tailwind | `tailwindcss-development`        |
| Media/adjuntos         | `medialibrary-development`       |
| RBAC/permisos          | `laravel-permission-development` |
| Deploy                 | `deploying-laravel-cloud`        |

---

## Plantilla reporte verify

Ver skill `sdd-verify-implementation` y prompt `verify-implementation`.

---

## Smoke manual (humano)

Derivar de criterios sin cobertura automatizada (UI, permisos por rol, archivos). Formato: qué hacer, dónde, resultado esperado.
