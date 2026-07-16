# Publicación — SDD Kit

Perfil de **publicación del producto kit** (no despliegue de aplicación). Los consumidores obtienen el kit vía submodule Git o copia puntual.

## Principio

El merge a `main` integra cambios; la **versión publicada** se etiqueta con SemVer (`vX.Y.Z`) y exige **dual-release**:

| Capa | Dónde | Qué valida |
| ---- | ----- | ---------- |
| CI | `.github/workflows/ci.yml` | CLI, JSON agent-prompts, perfiles |
| Nota producto | `docs/releases/vX.Y.Z.md` + GitHub Releases | Notas para consumidores, CHANGELOG, tag |
| Acta campaña | `.github/docs/sdd/releases/vX.Y.Z/release_vX.Y.Z.md` | Specs archivados, gates, enlace a nota producto |

## Pasos (alineados con runbook del kit)

1. Crear/actualizar `docs/releases/vX.Y.Z.md` y entrada en `docs/releases/CHANGELOG.md`.
2. Crear acta `.github/docs/sdd/releases/vX.Y.Z/release_vX.Y.Z.md` con **Changelog kit** enlazando la nota producto.
3. Confirmar CI en verde en el commit a etiquetar.
4. Ejecutar `validate-sdd` sobre `.github/docs/sdd/` (WARN si falta nota producto).
5. Crear tag `vX.Y.Z` y GitHub Release con el cuerpo de la nota producto.
6. Comunicar a consumidores: actualizar submodule (`git submodule update --remote sdd-kit`).

## Smoke post-publicación

- [ ] Tag apunta al commit correcto
- [ ] GitHub Release contiene notas legibles
- [ ] `init-sdd` funciona con el tag en proyecto de prueba _(muestra)_
- [ ] Perfiles listados en README coinciden con carpetas en `profiles/`

## Rollback

- Eliminar o marcar release como retractada en GitHub
- Consumidores fijan submodule al tag anterior
- Hotfix: rama `fix/` → patch version
