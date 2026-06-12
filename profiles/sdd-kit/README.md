# Perfil: SDD Kit (mantenedores)

Extensión del SDD core para **evolucionar el repositorio sdd-kit** (metodología, perfiles, bootstrap, CLI). No usar en proyectos consumidores — ellos eligen su stack (Laravel, FastAPI, React, etc.).

| Archivo                                                                  | Uso                                                  |
| ------------------------------------------------------------------------ | ---------------------------------------------------- |
| [checklist-stack.md](checklist-stack.md)                                 | DoD técnico (CLI, agent-prompts, perfiles, docs)     |
| [spec-impact.md](spec-impact.md)                                         | Tabla "Impacto técnico" para specs del kit           |
| [deploy.md](deploy.md)                                                   | Publicación de versión del kit (tag, GitHub Release) |
| [branching-extensions.md](branching-extensions.md)                       | Dependabot y ramas opcionales                        |
| [release-deploy-section.md](release-deploy-section.md)                   | Bloque para notas de release                         |
| [examples/SDD-001-perfil-sdd-kit.md](examples/SDD-001-perfil-sdd-kit.md) | Spec de ejemplo (este perfil)                        |

**Quality gates por defecto:**

- `python -m compileall -q cli/`
- Validación JSON: `bootstrap/agent-prompts/manifest.json`, `stack-descriptions.json`
- Verificación archivos obligatorios en cada `profiles/<nombre>/`
- `validate-sdd` sobre la instancia SDD del repo (`.github/docs/sdd/`)
- CI: `.github/workflows/ci.yml` en verde
