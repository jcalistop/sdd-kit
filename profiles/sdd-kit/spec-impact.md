# Impacto técnico — SDD Kit (mantenedores)

> Sección obligatoria en todo spec del repositorio sdd-kit.
> Reglas del producto: `.github/docs/business/domain-rules.md`.

## Impacto técnico _(obligatorio)_

Responder cada ítem. Si no aplica: "No aplica — [razón]".

| Pregunta                                                              | Respuesta |
| --------------------------------------------------------------------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)?                        |           |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)?     |           |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? |           |
| ¿Afecta `cli/` (comandos, librerías)?                                 |           |
| ¿Afecta `.github/workflows/` o reglas Cursor?                         |           |
| ¿Requiere actualizar `README.md` o `INSTALL.md`?                      |           |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)?                   |           |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles.   |           |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR.          |           |

## Regla de esquema

No aplica — el kit no tiene base de datos. Cambios de datos son documentales (markdown, YAML, JSON).
