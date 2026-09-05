# SDD Upgrade Kit — Checklist post-upgrade

Tras `install-agents.py` cuando cambien prompts, reglas o **agent-skills**.

## Diff skills vs kit

- [ ] `sdd prompt show build-spec --full` vs `sdd-build-spec/SKILL.md`
- [ ] `sdd prompt show discovery-to-draft --full` vs `sdd-draft-spec`
- [ ] `sdd prompt show verify-implementation --full` vs `sdd-verify-implementation`
- [ ] Reglas `.cursor/rules/sdd-*.mdc` reinstaladas — deltas de instancia preservados
- [ ] Skills `sdd-*` reinstaladas desde `{{KIT_PATH}}/bootstrap/agent-skills/` (manifest)

## Artefactos v1.3.0+ (si el tag destino es ≥ v1.3.0)

- [ ] Existe `.cursor/rules/sdd-safe-git.mdc` con `alwaysApply: true`
- [ ] No se duplicó una regla de migraciones BD de instancia (`safe-migrations`, etc.) al instalar safe-git
- [ ] `validate-sdd` / `sdd validate` emite prefijos `[componente]`

## Migración desde v1.3.x (tokens / cost-governance)

A partir de **v1.4.0** (SDD-016):

- La skill `sdd-cost-governance` **ya no se instala**. Si quedó una copia huérfana en `.cursor/skills/sdd-cost-governance/`, bórrala al reinstalar agentes.
- El subcomando `sdd metrics tokens` **fue retirado**. Usa `sdd metrics` solo para salud del proceso (estados, stagnant).
- No se espera `paths.sdd/metrics/token-usage.json`.

Si **solo** se actualizó el submodule y falta safe-git → **reinstalar** adaptadores; no marcar `kit.installed_version` como completo.

## Si hay divergencia

1. Preferir contenido del kit; no copiar árbol `prompts/` local.
2. Mantener `reference.md` delgados.
3. Documentar en `UPGRADE-LOG.md`.

## Validación

```bash
python {{KIT_PATH}}/cli/sdd.py validate
{{KIT_PATH}}/bootstrap/validate-sdd.ps1 -SddPath "{{SDD_PATH}}"
```
