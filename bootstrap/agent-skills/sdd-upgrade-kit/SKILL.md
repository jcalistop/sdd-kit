---
name: sdd-upgrade-kit
description: Actualiza submodule sdd-kit en la instancia consumidora. Usar cuando el humano pide upgrade-kit, actualizar kit SDD, o subir kit.installed_version.
---

# SDD Upgrade Kit

Actualizar kit SDD (submodule) en la instancia consumidora.

**Prohibido:** `--force` en merge de instancia; push sin confirmación humana.

**Contexto mínimo requerido:**

1. `{{SDD_PATH}}/sdd.config.yaml` — `kit.installed_version`
2. `{{SDD_PATH}}/UPGRADE-LOG.md` — historial de upgrades

**NO leer** specs, BACKLOG ni domain-rules (no son necesarios para el upgrade del kit).

## Rutas

| Artefacto     | Ruta                                              |
| ------------- | ------------------------------------------------- |
| Upgrade guide | `{{SDD_PATH}}/upgrade-guide.md`                   |
| Config        | `{{SDD_PATH}}/sdd.config.yaml`                    |
| Log           | `{{SDD_PATH}}/UPGRADE-LOG.md`                     |
| Adaptadores   | `python {{KIT_PATH}}/bootstrap/install-agents.py` |

## Procedimiento

Seguir `{{SDD_PATH}}/upgrade-guide.md`:

1. Detectar versión (`kit.installed_version` + submodule)
2. Changelog destino en `{{KIT_PATH}}/docs/releases/`
3. Actualizar submodule a tag
4. Diff `core/` vs instancia (excluir `prompts/`, `profiles/`)
5. Merge instancia con confirmación humana
6. Si cambió `agent-prompts/` o `agent-skills/`: `install-agents.py install --agent cursor --profile {{PROFILE}} --sdd-path {{SDD_PATH}} --kit-path {{KIT_PATH}} --no-prompt`
7. Checklist post-upgrade: [reference.md](reference.md)
8. `sdd validate` + `validate-sdd`
9. Actualizar `kit.installed_version`, `UPGRADE-LOG.md`, `ADOPTION.md`
10. Commits separados: submodule + instancia

## Recursos

- `python {{KIT_PATH}}/cli/sdd.py prompt show upgrade-kit --full`
