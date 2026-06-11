# Extensiones de ramas — Dependabot (Python)

Opcional para repos con **tres ramas**: `main`, `dev`, `deps-integration`.

## Objetivo

Agrupar bumps de Dependabot (pip, poetry, uv) sin ruido en `dev`.

## Reglas

1. Dependabot abre PRs con base **`deps-integration`**.
2. No mezclar features manuales en `deps-integration`.
3. **Ritual semanal:** merge bumps → sync `dev` → `deps-integration` → PR `deps-integration` → `dev`.

## Trazabilidad SDD

Sync y promoción **no requieren** spec. Registrar en release con ID `—` si aplica.

## Configuración sugerida en el repo consumidor

- `.github/dependabot.yml` — ecosystem `pip` o `github-actions`, target `deps-integration`
- `.github/workflows/deps-integration-sync.yml` — sync `dev` → `deps-integration`
