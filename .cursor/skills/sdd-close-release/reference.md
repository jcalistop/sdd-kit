# SDD Close Release — Referencia

Fuente canónica: `.github/docs/sdd/releases/RUNBOOK.md`.

## Orden documental

1. Specs mergeados en `dev`
2. `git mv` a `archive/` + BACKLOG Released
3. Entrada `releases/vX.Y.Z/`
4. `validate-sdd` + `sdd validate`
5. PR campaña → producción (merge commit)
6. Tag + sync ramas + deploy

## Prohibido

- `Estado: Released` en `specs/` sin `git mv`
- Archivar antes de merge en `dev`
