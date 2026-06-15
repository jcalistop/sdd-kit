# SDD Upgrade Kit — Checklist post-upgrade

Tras `install-agents.py` cuando cambien prompts, reglas o **agent-skills**.

## Diff skills vs kit

- [ ] `sdd prompt show build-spec --full` vs `sdd-build-spec/SKILL.md`
- [ ] `sdd prompt show discovery-to-draft --full` vs `sdd-draft-spec`
- [ ] `sdd prompt show verify-implementation --full` vs `sdd-verify-implementation`
- [ ] Reglas `.cursor/rules/sdd-*.mdc` reinstaladas — deltas de instancia preservados
- [ ] Skills `sdd-*` reinstaladas desde `{{KIT_PATH}}/bootstrap/agent-skills/` (manifest)

## Si hay divergencia

1. Preferir contenido del kit; no copiar árbol `prompts/` local.
2. Mantener `reference.md` delgados.
3. Documentar en `UPGRADE-LOG.md`.

## Validación

```bash
python {{KIT_PATH}}/cli/sdd.py validate
{{KIT_PATH}}/bootstrap/validate-sdd.ps1 -SddPath "{{SDD_PATH}}"
```
