# Perfil: Python + Django

Extensión del SDD core para aplicaciones **Django 4.2+ / 5.x**: modelos, vistas/templates, admin, migraciones Django, DRF y Celery opcionales, despliegue típico (Docker o PaaS).

| Archivo                                                                              | Uso                                                                |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| [checklist-stack.md](checklist-stack.md)                                             | DoD técnico (pytest, ruff, mypy, admin, migraciones, DRF opcional) |
| [spec-impact.md](spec-impact.md)                                                     | Tabla "Impacto técnico" para specs                                 |
| [deploy.md](deploy.md)                                                               | Docker, PaaS o servidor (gunicorn, migrate, collectstatic)         |
| [branching-extensions.md](branching-extensions.md)                                   | Rama `deps-integration` + Dependabot (pip/poetry/uv)               |
| [release-deploy-section.md](release-deploy-section.md)                               | Bloque para notas de release                                       |
| [examples/SDD-001-crud-productos-admin.md](examples/SDD-001-crud-productos-admin.md) | Spec de ejemplo (referencia de calidad)                            |

## Stack objetivo

- Django 5.x (compatible 4.2 LTS)
- pytest + pytest-django
- ruff (lint/format)
- mypy + django-stubs (opcional)
- DRF (opcional, APIs REST)
- Celery (opcional, tareas en background)

## Estructura típica

```
proyecto/
├── config/              # settings, urls, wsgi/asgi
├── apps/<nombre>/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   ├── urls.py
│   └── migrations/
├── templates/
├── static/
├── tests/
└── manage.py
```

## Quality gates por defecto

- `pytest --cov` (tests + cobertura)
- `ruff check .` (lint)
- `mypy .` (type checking, si está configurado)
- `python manage.py check` (validación Django)
- Migraciones solo en `apps/<app>/migrations/` (sin DDL manual fuera de migraciones)
- CI: `.github/workflows/ci.yml` en verde
