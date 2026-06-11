# Guía de contribución — SDD Kit

Gracias por interesarte en mejorar el kit. Este repositorio es metodología, documentación y herramientas de bootstrap; las contribuciones deben mantener el core **agnóstico al stack** y los perfiles **autocontenidos**.

## Antes de empezar

1. Revisa el [README](README.md) y [INSTALL.md](INSTALL.md) para entender el alcance del kit.
2. Para cambios grandes (nuevo perfil, CLI, flujo SDD), abre un issue o comenta en uno existente.
3. Planificación del mantenedor: [docs/maintainers/](docs/maintainers/). Releases: [docs/releases/](docs/releases/).

## Tipos de contribución

| Tipo                               | Dónde                | Notas                                                                          |
| ---------------------------------- | -------------------- | ------------------------------------------------------------------------------ |
| Core (workflow, plantillas, guías) | `core/`              | Sin referencias a stacks concretos                                             |
| Perfil de stack                    | `profiles/<nombre>/` | Sigue [core/templates/profile-template.md](core/templates/profile-template.md) |
| Bootstrap / agentes                | `bootstrap/`         | Prompts en `agent-prompts/`; reglas Cursor se generan en install               |
| CLI                                | `cli/`               | Python 3.10+, sin dependencias externas obligatorias                           |
| Docs de mantenimiento              | `docs/maintainers/`  | Solo evolución del repo, no se copia a proyectos                               |
| Releases del kit                   | `docs/releases/`     | CHANGELOG y notas `vX.Y.Z.md`; publicar en GitHub Releases                     |

## Flujo de trabajo

1. **Fork** del repositorio y rama desde `main` (`feat/...`, `fix/...`, `docs/...`).
2. Cambios **pequeños y enfocados** — un PR por tema.
3. Actualiza documentación afectada (README, INSTALL, perfil, [docs/releases/CHANGELOG.md](docs/releases/CHANGELOG.md) si aplica).
4. Abre un **Pull Request** con la plantilla completada.

### Nuevo perfil de stack

1. Crea `profiles/<nombre>/` con los archivos obligatorios de la plantilla.
2. Añade `bootstrap/agent-prompts/stacks/<nombre>.md` y entrada en `stack-descriptions.json`.
3. Incluye al menos un ejemplo `SDD-001-*.md` de calidad referencial.
4. No modifiques `core/` salvo que el cambio sea realmente transversal.

### Cambios en CLI

```powershell
python -m compileall cli/
```

Si agregas comandos, documenta en [cli/README.md](cli/README.md).

## Estilo y calidad

- **Idioma:** español latino (Chile) en documentación del kit.
- **Markdown:** enlaces relativos, tablas legibles, sin duplicar contenido entre core y perfiles.
- **Código:** sigue el estilo existente; evita dependencias nuevas sin justificación.
- **Desarrollo sano:** [core/healthy-development.md](core/healthy-development.md).

## Pull requests

- Describe el **por qué** del cambio, no solo el qué.
- Indica si afecta a proyectos que ya usan el kit como submodule (breaking changes).
- El mantenedor revisará y puede pedir ajustes antes del merge.

## Reportar problemas

- **Bug:** usa la plantilla de issue _Reporte de bug_.
- **Idea / mejora:** plantilla _Solicitud de mejora_.
- **Seguridad:** no abras issue público; ver [SECURITY.md](SECURITY.md).

## Licencia

Al contribuir, aceptas que tu aportación se publique bajo la [licencia MIT](LICENSE) del proyecto.
