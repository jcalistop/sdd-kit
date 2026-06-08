# Extensiones de ramas — Dependabot (Laravel)

Opcional para repos con **tres ramas**: `main`, `dev`, `dep-integration`.

## Objetivo

Agrupar bumps de Dependabot sin ruido en `dev`.

## Reglas

1. Dependabot abre PRs con base **`dep-integration`**.
2. No mezclar features manuales en `dep-integration`.
3. **Ritual semanal:** merge bumps → sync `dev` → `dep-integration` (automático) → PR `dep-integration` → `dev`.

## Trazabilidad SDD

Sync y promoción **no requieren** spec. Registrar en release con ID `—` si aplica.

## Workflow sugerido

- `.github/workflows/deps-sync.yml` — sync en push a `dev`
- `.github/dependabot.yml` — target `dep-integration`

Implementar en el repo consumidor: `.github/workflows/deps-sync.yml` y `.github/dependabot.yml` con target `dep-integration`.
