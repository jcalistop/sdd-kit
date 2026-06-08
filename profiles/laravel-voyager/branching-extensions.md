# Extensiones de ramas — Dependabot (Laravel + Voyager)

Para repos con **tres ramas**: `main`, `dev`, `deps-integration`.

## Objetivo

Agrupar bumps de Dependabot sin ruido en `dev`.

## Reglas

1. Dependabot abre PRs con base **`deps-integration`** (no `dependabot` — conflicto de namespace con refs `dependabot/*`).
2. No mezclar features/fixes manuales en `deps-integration`.
3. **Domingo (automático):** workflow sync hace fast-forward `dev` → `deps-integration`.
4. **Ritual semanal:** merge bumps en `deps-integration` → PR `deps-integration` → `dev`.

## Trazabilidad SDD

Sync y promoción **no requieren** spec. Registrar en release con ID `—` si aplica.

## Workflow sugerido en el repo consumidor

- `.github/workflows/deps-integration-sync.yml` — sync `dev` → `deps-integration`
- `.github/dependabot.yml` — target `deps-integration`
