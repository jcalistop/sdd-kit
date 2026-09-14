---
name: sdd-upgrade-kit
description: Actualiza submodule sdd-kit en la instancia consumidora. Usar cuando el humano pide upgrade-kit, actualizar kit SDD, o subir kit.installed_version.
---

# SDD Upgrade Kit

Actualizar kit SDD (submodule) en la instancia consumidora.

**Prohibido:** `--force` en merge de instancia; push sin confirmación humana.

**Contexto mínimo requerido:**

1. `{{SDD_PATH}}/sdd.config.yaml` — `kit.installed_version` y `agent.targets`
2. `{{SDD_PATH}}/UPGRADE-LOG.md` — historial de upgrades

**NO leer** specs, BACKLOG ni domain-rules (no son necesarios para el upgrade del kit).

## Rutas

| Artefacto | Ruta |
| --------- | ---- |
| Upgrade guide (**canónico post-bump**) | `{{KIT_PATH}}/core/guides/upgrade-guide.md` |
| Copia en instancia (tras migrate `guides/`) | `{{SDD_PATH}}/guides/upgrade-guide.md` |
| Config | `{{SDD_PATH}}/sdd.config.yaml` |
| Log | `{{SDD_PATH}}/UPGRADE-LOG.md` |
| Adaptadores | `python {{KIT_PATH}}/bootstrap/install-agents.py` |

**No exijas** que exista `{{SDD_PATH}}/guides/upgrade-guide.md` **antes** del bump o del merge: lee siempre el runbook del **kit** tras actualizar el submodule.

## Procedimiento

Seguir `{{KIT_PATH}}/core/guides/upgrade-guide.md`:

1. Detectar versión (`kit.installed_version` + submodule)
2. Changelog destino en `{{KIT_PATH}}/docs/releases/`
3. Actualizar submodule a tag
4. Si el destino es ≥ **v1.6.0** y la instancia tiene guías en la **raíz** de `{{SDD_PATH}}` (sin carpeta `guides/`): migrar a `{{SDD_PATH}}/guides/` con confirmación humana (`git mv`); no tocar `BACKLOG` / `specs` / `archive`
5. Diff `{{KIT_PATH}}/core/guides/` vs `{{SDD_PATH}}/guides/` (y contratos de `core/` solo si la instancia los mantiene). No uses solo `diff -rq …/core …/sdd` como único paso
6. Merge instancia con confirmación humana
7. Si cambió `agent-prompts/` **o** `agent-skills/`: reinstalar adaptadores según `agent.targets` en `{{SDD_PATH}}/sdd.config.yaml`:
   - Leer la lista `agent.targets` (p. ej. `[cursor]` o `[cursor, claude]`).
   - Si está **ausente o vacía**: preguntar al humano qué agentes reinstalar; si no hay respuesta y hace falta `--no-prompt`, usar `cursor` como fallback y documentarlo en `UPGRADE-LOG`.
   - Ejecutar: `python {{KIT_PATH}}/bootstrap/install-agents.py install --agent <lista-separada-por-comas> --profile {{PROFILE}} --sdd-path {{SDD_PATH}} --kit-path {{KIT_PATH}} --no-prompt`  
     Ejemplo con un solo target: `--agent cursor`. Con varios: `--agent cursor,claude`.
8. Checklist post-upgrade: [reference.md](reference.md)
9. `sdd validate` + `validate-sdd`
10. Actualizar `kit.installed_version`, `UPGRADE-LOG.md`, `ADOPTION.md`
11. Commits separados: submodule + instancia

**Salto largo (p. ej. desde ≤v1.2 a v1.6):** un solo checkout al tag destino; aplicar checklists del upgrade-guide en orden (v1.3.0+ … v1.6.0). No exijas N bumps intermedios.

Si el humano rechazó algún merge de instancia: documentar en `UPGRADE-LOG` y **no** marcar `installed_version` como la versión destino.

## Recursos

- `python {{KIT_PATH}}/cli/sdd.py prompt show upgrade-kit --full`
