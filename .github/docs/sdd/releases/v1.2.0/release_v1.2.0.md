# Release campaña v1.2.0 — Skills SDD en bootstrap

## Cabecera

| Campo                | Valor                                         |
| -------------------- | --------------------------------------------- |
| **Versión**          | **`v1.2.0`**                                  |
| **Fecha cierre**     | 2026-06-15                                    |
| **Tipo**             | minor / bootstrap                             |
| **Responsable**      | equipo                                        |
| **Campaña anterior** | [v1.1.0](../../../docs/releases/v1.1.0.md)    |
| **Changelog kit**    | [v1.2.0.md](../../../docs/releases/v1.2.0.md) |

---

## Información general

Publica skills SDD canónicas en `bootstrap/agent-skills/`, extiende `install-agents.py` para instalarlas en Cursor e inyecta mapa trigger→prompt en adaptadores multi-agente (Claude, Codex, Copilot).

### Entregables principales

- Árbol `bootstrap/agent-skills/` (6 skills + manifest + stacks por perfil)
- `install_cursor_skills()` y `--kit-path` en `install-agents.py`
- Tests `bootstrap/test_install_skills.py`
- Documentación: `agent-setup.md`, `upgrade-guide.md`, `prompt-catalog.md`

---

## Specs incluidas

| ID      | Dominio   | Spec archivado                                                                                                       |
| ------- | --------- | -------------------------------------------------------------------------------------------------------------------- |
| SDD-004 | bootstrap | [archive/2026/bootstrap/SDD-004-agent-skills-cursor.md](../../archive/2026/bootstrap/SDD-004-agent-skills-cursor.md) |

---

## Validación de cierre

| Gate           | Resultado esperado |
| -------------- | ------------------ |
| `sdd validate` | 0 errores          |
| `validate-sdd` | OK                 |
| Tag producto   | `v1.2.0`           |

---

## Consumidores

Instancias que adopten v1.2.0 deben seguir prompt `upgrade-kit` o spec consumidor equivalente (ej. backoffice **SDD-061**).
