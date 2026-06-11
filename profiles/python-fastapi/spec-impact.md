# Impacto técnico — Python + FastAPI

> Sección obligatoria en todo spec. Copiar al crear `SDD-NNN` o referenciar desde la plantilla de la instancia.
> Reglas de negocio específicas: `.github/docs/business/domain-rules.md`.

## Impacto técnico _(obligatorio)_

Responder cada ítem. Si no aplica: "No aplica — [razón]".

| Pregunta                                                            | Respuesta |
| ------------------------------------------------------------------- | --------- |
| ¿Afecta endpoints REST (`app/routers/`, `app/api/`)? ¿Cuáles?       |           |
| ¿Modifica modelos SQLAlchemy o esquema Pydantic compartido?         |           |
| ¿Requiere auth (JWT, API key, OAuth2, sesión)?                      |           |
| ¿Incluye `db-change` (migración Alembic en `alembic/versions/`)?    |           |
| ¿Afecta tareas en background (Celery, RQ, BackgroundTasks)?         |           |
| ¿Expone o modifica contrato OpenAPI (breaking change)?              |           |
| ¿Requiere variables de entorno nuevas? Listar claves (sin valores). |           |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles. |           |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR.        |           |

## Regla de esquema

- Todo cambio de BD vía migraciones Alembic en `alembic/versions/` (o ruta configurada en el proyecto)
- Despliegue: `alembic upgrade head` tras backup si hay `db-change`
- Datos masivos: scripts o seeders referenciados en spec y release
