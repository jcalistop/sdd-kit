---
name: sdd-close-release
description: Cierra campaña release SDD — archivar specs, entrada en releases/, validate-sdd. Usar cuando el humano pide close-release, cerrar campaña vX.Y.Z, o ritual post-merge dev.
---

# SDD Close Release

Cerrar campaña semver y archivar specs **Released**.

**Contexto mínimo requerido:**

1. `{{SDD_PATH}}/BACKLOG.md` — specs en Validating a archivar
2. Specs a archivar — **solo cabeceras** (para `git mv` y entradas en release)
3. `{{SDD_PATH}}/sdd.config.yaml` — versión y dominios
4. `{{SDD_PATH}}/releases/RUNBOOK.md` — procedimiento de cierre

**NO leer** specs completos ni domain-rules (ya verificados en fases anteriores).

## Rutas

| Artefacto | Ruta                                     |
| --------- | ---------------------------------------- |
| RUNBOOK   | `{{SDD_PATH}}/releases/RUNBOOK.md`       |
| Releases  | `{{SDD_PATH}}/releases/vX.Y.Z/`          |
| Archive   | `{{SDD_PATH}}/archive/<YYYY>/<dominio>/` |
| Producto (kit) | `docs/releases/vX.Y.Z.md` + `CHANGELOG.md` (solo si aplica dual-release) |

## Procedimiento

1. RUNBOOK Fase 0–2; specs mergeados en `{{DEV_BRANCH}}`.
2. Por cada spec Validating: `git mv` a `archive/`; BACKLOG → Released.
3. Entrada `releases/vX.Y.Z/release_vX.Y.Z.md` (acta campaña).
4. **Dual-release (producto kit):** si `{{PROFILE}}` es `sdd-kit` o existe `docs/releases/` en la raíz:
   - Crear/actualizar `docs/releases/vX.Y.Z.md`
   - Entrada en `docs/releases/CHANGELOG.md`
   - En el acta, campo **Changelog kit** → enlace a la nota producto (sin duplicar narrativa)
5. `validate-sdd` + `python {{KIT_PATH}}/cli/sdd.py validate` (atender WARN dual-release).
6. Deploy según RUNBOOK y perfil `{{PROFILE}}`.
7. Confirmación humana para PR campaña → producción y tag.

## Recursos

- [reference.md](reference.md)
- `python {{KIT_PATH}}/cli/sdd.py prompt show close-release --full`
