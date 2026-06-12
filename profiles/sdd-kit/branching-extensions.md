# Extensiones de ramas — SDD Kit

Opcional para el repositorio del kit con **Dependabot** (GitHub Actions, pip si se añaden deps).

## Objetivo

Mantener `main` estable mientras se agrupan bumps de dependencias.

## Reglas

1. Dependabot puede apuntar a rama `deps-integration` si se configura.
2. Bumps rutinarios **no requieren spec** — ID `—` en release.
3. Cambios en `bootstrap/` o `cli/` por bump de deps: verificar `compileall` y `validate-sdd`.

## Trazabilidad SDD

Sync de dependencias no requiere spec salvo que cambie comportamiento del CLI o scripts de bootstrap.
