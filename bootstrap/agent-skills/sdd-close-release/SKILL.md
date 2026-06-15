---
name: sdd-close-release
description: Cierra campaña release SDD — archivar specs, entrada en releases/, validate-sdd. Usar cuando el humano pide close-release, cerrar campaña vX.Y.Z, o ritual post-merge dev.
---

# SDD Close Release

Cerrar campaña semver y archivar specs **Released**.

## Rutas

| Artefacto | Ruta                                     |
| --------- | ---------------------------------------- |
| RUNBOOK   | `{{SDD_PATH}}/releases/RUNBOOK.md`       |
| Releases  | `{{SDD_PATH}}/releases/vX.Y.Z/`          |
| Archive   | `{{SDD_PATH}}/archive/<YYYY>/<dominio>/` |

## Procedimiento

1. RUNBOOK Fase 0–2; specs mergeados en `{{DEV_BRANCH}}`.
2. Por cada spec Validating: `git mv` a `archive/`; BACKLOG → Released.
3. Entrada `releases/vX.Y.Z/release_vX.Y.Z.md`.
4. `validate-sdd` + `python {{KIT_PATH}}/cli/sdd.py validate`.
5. Deploy según RUNBOOK y perfil `{{PROFILE}}`.
6. Confirmación humana para PR campaña → producción y tag.

## Recursos

- [reference.md](reference.md)
- `python {{KIT_PATH}}/cli/sdd.py prompt show close-release --full`
