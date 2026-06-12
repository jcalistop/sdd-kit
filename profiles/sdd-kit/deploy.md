# Publicación — SDD Kit

Perfil de **publicación del producto kit** (no despliegue de aplicación). Los consumidores obtienen el kit vía submodule Git o copia puntual.

## Principio

El merge a `main` integra cambios; la **versión publicada** se etiqueta con SemVer (`vX.Y.Z`) y se documenta en `docs/releases/`.

| Capa    | Dónde                                       | Qué valida                        |
| ------- | ------------------------------------------- | --------------------------------- |
| CI      | `.github/workflows/ci.yml`                  | CLI, JSON agent-prompts, perfiles |
| Release | `docs/releases/vX.Y.Z.md` + GitHub Releases | Notas, CHANGELOG, tag             |

## Pasos (alineados con runbook del kit)

1. Revisar `docs/releases/vX.Y.Z/release_vX.Y.Z.md` (o crear nota de release).
2. Confirmar CI en verde en el commit a etiquetar.
3. Ejecutar `validate-sdd` sobre `.github/docs/sdd/`.
4. Actualizar `docs/releases/CHANGELOG.md` (`sdd release changelog` si aplica).
5. Crear tag `vX.Y.Z` y GitHub Release con notas.
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
