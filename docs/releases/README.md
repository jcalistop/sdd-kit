# Releases del SDD Kit

> Historial de **versiones del repositorio** `sdd-kit`.

## Contrato de capas (releases)

| Capa                              | Ruta                                     | Rol                                                   | ¿Copiado por `init-sdd`?          |
| --------------------------------- | ---------------------------------------- | ----------------------------------------------------- | --------------------------------- |
| **Release producto kit**          | `docs/releases/vX.Y.Z.md` (esta carpeta) | Notas para consumidores y GitHub Releases             | No (vive en submodule)            |
| **Cierre campaña SDD (kit)**      | `.github/docs/sdd/releases/vX.Y.Z/`      | Acta SDD: specs archivados, gates, enlace al producto | No                                |
| **Plantillas release consumidor** | `core/releases/`                         | RUNBOOK para **apps** que adoptan SDD                 | Sí → `.github/docs/sdd/releases/` |

Glosario ampliado: [docs/README.md](../README.md).

## Contrato dual-write

Al etiquetar `vX.Y.Z` del kit:

1. Esta carpeta: `vX.Y.Z.md` + entrada en [CHANGELOG.md](CHANGELOG.md).
2. Acta SDD: `.github/docs/sdd/releases/vX.Y.Z/release_vX.Y.Z.md` con **Changelog kit** → este archivo.
3. `validate-sdd` advierte (WARN) si existe acta de campaña y falta la nota producto aquí.

Consumidores del submodule **solo** leen esta carpeta.

## Dónde mirar

| Recurso                                                          | Uso                                     |
| ---------------------------------------------------------------- | --------------------------------------- |
| [CHANGELOG.md](CHANGELOG.md)                                     | Resumen técnico de cambios por versión  |
| [v1.2.2.md](v1.2.2.md)                                           | Última versión (optimización de tokens) |
| [v1.2.1.md](v1.2.1.md)                                           | Patch bootstrap (bloque `kit`)          |
| [v1.2.0.md](v1.2.0.md)                                           | Skills + documentación                  |
| [v1.1.0.md](v1.1.0.md)                                           | Perfil sdd-kit y upgrade en instancias  |
| [v1.0.0.md](v1.0.0.md)                                           | Primera versión estable                 |
| [v0.1.0.md](v0.1.0.md)                                           | Pre-release inicial                     |
| [GitHub Releases](https://github.com/jcalistop/sdd-kit/releases) | Publicación oficial por etiqueta        |

## Convención

- **Etiqueta Git:** `vX.Y.Z` (SemVer)
- **Archivo en repo:** `docs/releases/vX.Y.Z.md` — texto en lenguaje accesible (público en GitHub Release)
- **CHANGELOG:** entrada breve con secciones Añadido / Cambiado / Corregido
- **Pre-release:** `prerelease: true` en GitHub (como v0.1.0)
- **Estable:** `prerelease: false` (desde v1.0.0)

## Planificación del kit

Roadmap y análisis (no son notas de versión): [`.github/docs/business/planning/`](../.github/docs/business/planning/)
