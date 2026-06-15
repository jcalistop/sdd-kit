# SDD-004 — Skills SDD en bootstrap (multi-agente)

---

## Cabecera

| Campo                 | Valor                                                            |
| --------------------- | ---------------------------------------------------------------- |
| **ID**                | `SDD-004`                                                        |
| **Dominio**           | `bootstrap`                                                      |
| **Tipo**              | `feature` + `documentation`                                      |
| **Fecha**             | 2026-06-15                                                       |
| **Estado**            | `Released`                                                       |
| **Versión objetivo**  | `v1.2.0`                                                         |
| **Owner**             | equipo                                                           |
| **Prioridad**         | `P1`                                                             |
| **ADRs relacionados** | —                                                                |
| **Dependencias**      | SDD-003 (v1.1.0); dogfooding desde instancia consumidora SDD-059 |

---

## Problema y objetivo

**Problema:**

Las skills SDD del ciclo (`sdd-draft-spec`, `sdd-build-spec`, etc.) existen solo en proyectos consumidores que las crearon a mano. `install-agents.py` instala reglas `.mdc` pero no skills; `agent-setup.md` las declara fuera de alcance. Cada adopción o upgrade pierde activación on-demand en Cursor y no hay paridad documentada para Claude, Codex y Copilot.

**Objetivo:**

Publicar skills SDD canónicas en `bootstrap/agent-skills/`, extender `install-agents.py` para instalarlas (Cursor) e inyectar mapa trigger→prompt en adaptadores multi-agente, documentar en v1.2.0.

---

## Alcance

**Incluye:**

- Árbol `bootstrap/agent-skills/` con 6 skills, `manifest.json`, fragmentos por stack
- `install_cursor_skills()` y mapa en preambles Claude/Codex/Copilot
- `init-sdd` invoca instalación de skills
- Actualización `agent-setup.md`, `upgrade-guide.md`, `prompt-catalog.md`, ROADMAP
- `docs/releases/v1.2.0.md`, CHANGELOG
- Test Python mínimo de instalación
- Advertencia en `validate-sdd` si faltan skills Cursor del manifest

**Excluye:**

- Skills de stack del proyecto (Boost, Laravel, etc.)
- Antigravity u otros IDEs sin adaptador
- Editar `AGENTS.md` de consumidores que mezclan Boost

---

## Impacto técnico

| Pregunta                        | Respuesta                                                     |
| ------------------------------- | ------------------------------------------------------------- |
| ¿Afecta código de aplicación?   | No                                                            |
| ¿db-change?                     | No                                                            |
| ¿Decisión arquitectónica nueva? | Sí — skills como capa paralela a prompts, fuente en bootstrap |

---

## Reglas de negocio

No aplica — producto kit.

---

## Criterios de aceptación

**Happy path:**

- [x] `bootstrap/agent-skills/` con 6 skills + manifest
- [x] `install-agents.py install --agent cursor` copia skills renderizadas a `.cursor/skills/sdd-*`
- [x] Preambles multi-agente incluyen mapa skills → prompts
- [x] `init-sdd` invoca install-agents (skills tras rules)
- [x] Test install skills en verde
- [x] Tag `v1.2.0` documentado

**Error path:**

- [x] Reinstalar no elimina skills ajenas al manifest
- [x] Perfil sin fragmento stack → quality gates genéricos en reference

---

## Notas post-implementación

**2026-06-15** — Released en campaña **v1.2.0**. Tag producto `v1.2.0`. Consumidor de referencia: backoffice SDD-061.
