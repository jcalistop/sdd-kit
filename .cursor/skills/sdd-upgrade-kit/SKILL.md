---
name: sdd-upgrade-kit
description: Actualiza submodule sdd-kit en la instancia consumidora. Usar cuando el humano pide upgrade-kit, actualizar kit SDD, o subir kit.installed_version.
---

# SDD Upgrade Kit

Actualizar kit SDD (submodule) en la instancia consumidora.

**Prohibido:** `--force` en merge de instancia; push sin confirmación humana.

## Rutas

| Artefacto     | Ruta                                              |
| ------------- | ------------------------------------------------- |
| Upgrade guide | `.github/docs/sdd/upgrade-guide.md`                   |
| Config        | `.github/docs/sdd/sdd.config.yaml`                    |
| Log           | `.github/docs/sdd/UPGRADE-LOG.md`                     |
| Adaptadores   | `python ./bootstrap/install-agents.py` |

## Procedimiento

Seguir `.github/docs/sdd/upgrade-guide.md`:

1. Detectar versión (`kit.installed_version` + submodule)
2. Changelog destino en `./docs/releases/`
3. Actualizar submodule a tag
4. Diff `core/` vs instancia (excluir `prompts/`, `profiles/`)
5. Merge instancia con confirmación humana
6. Si cambió `agent-prompts/` o `agent-skills/`: `install-agents.py install --agent cursor --profile sdd-kit --sdd-path .github/docs/sdd --kit-path . --no-prompt`
7. Checklist post-upgrade: [reference.md](reference.md)
8. `sdd validate` + `validate-sdd`
9. Actualizar `kit.installed_version`, `UPGRADE-LOG.md`, `ADOPTION.md`
10. Commits separados: submodule + instancia

## Recursos

- `python ./cli/sdd.py prompt show upgrade-kit --full`
