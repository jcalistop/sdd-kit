# SDD Build Spec — Referencia

**Fuentes canónicas:** `.cursor/rules/sdd-workflow-reference.mdc` · CLI `./cli/sdd.py prompt show <id> --full`

---

## Transiciones BACKLOG

| De       | A          | Cabecera spec               |
| -------- | ---------- | --------------------------- |
| Draft    | Ready      | `Estado: Ready`             |
| Ready    | In Build   | `Estado: In Build`          |
| In Build | Validating | Tras verify OK + PR abierto |

---

## Convención de ramas

Según tipo del spec y `.github/docs/sdd/branching.md`. PR destino habitual: **`dev`**.

---

## Quality gates — sdd-kit

| Gate           | Comando                                                                        | Cuándo                                |
| -------------- | ------------------------------------------------------------------------------ | ------------------------------------- |
| Compilar CLI   | `python -m compileall -q cli/`                                                 | Tras editar Python del kit            |
| Manifest JSON  | validar `bootstrap/agent-prompts/manifest.json` y `agent-skills/manifest.json` | Tras cambios bootstrap                |
| Validación SDD | `python {{KIT_PATH}}/cli/sdd.py validate`                                      | Tras cambios en specs/BACKLOG del kit |

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
