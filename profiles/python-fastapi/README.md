# Perfil: Python + FastAPI

Extensión del SDD core para APIs REST con FastAPI, SQLAlchemy/Alembic y despliegue típico (Docker o PaaS).

| Archivo                                                                          | Uso                                                      |
| -------------------------------------------------------------------------------- | -------------------------------------------------------- |
| [checklist-stack.md](checklist-stack.md)                                         | DoD técnico (pytest, ruff, mypy, endpoints, migraciones) |
| [spec-impact.md](spec-impact.md)                                                 | Tabla "Impacto técnico" para specs                       |
| [deploy.md](deploy.md)                                                           | Docker, PaaS o script de deploy                          |
| [branching-extensions.md](branching-extensions.md)                               | Rama `deps-integration` + Dependabot (pip/poetry)        |
| [release-deploy-section.md](release-deploy-section.md)                           | Bloque para notas de release                             |
| [examples/SDD-001-api-crud-productos.md](examples/SDD-001-api-crud-productos.md) | Spec de ejemplo (referencia de calidad)                  |

**Quality gates por defecto:**

- `pytest --cov` (tests + cobertura)
- `ruff check .` (lint)
- `mypy .` (type checking, si está configurado)
- Migraciones solo en `alembic/versions/` (o ruta del proyecto)
- CI: `.github/workflows/ci.yml` en verde
