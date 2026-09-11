# SDD Build Spec — Referencia

**Fuentes canónicas:** `.cursor/rules/sdd-workflow-reference.mdc` · CLI `{{KIT_PATH}}/cli/sdd.py prompt show <id> --full`

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

También: tipo del spec y `{{SDD_PATH}}/branching.md`. PR destino habitual (si aplica): **`{{DEV_BRANCH}}`**.

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
