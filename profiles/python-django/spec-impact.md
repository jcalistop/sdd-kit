# Impacto técnico — Python + Django

> Sección obligatoria en todo spec. Copiar al crear `SDD-NNN` o referenciar desde la plantilla de la instancia.
> Reglas de negocio específicas: `.github/docs/business/domain-rules.md`.

## Impacto técnico _(obligatorio)_

Responder cada ítem. Si no aplica: "No aplica — [razón]".

| Pregunta                                                            | Respuesta |
| ------------------------------------------------------------------- | --------- |
| ¿Qué apps Django afecta (`apps/<app>/`)?                            |           |
| ¿Modifica modelos, relaciones, managers o `Meta`?                   |           |
| ¿Afecta vistas (FBV/CBV) y templates? ¿Cuáles rutas?                |           |
| ¿Afecta admin (`admin.py`, inlines, acciones)?                      |           |
| ¿Incluye `db-change` (migración en `apps/<app>/migrations/`)?       |           |
| ¿Afecta DRF (serializers, viewsets, permisos, routers)?             |           |
| ¿Requiere auth (sesión, permisos Django, grupos)?                   |           |
| ¿Afecta Celery tasks, signals o management commands?                |           |
| ¿Requiere variables de entorno nuevas? Listar claves (sin valores). |           |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles. |           |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR.        |           |

## Regla de esquema

- Todo cambio de BD vía `python manage.py makemigrations` en la app correspondiente
- Despliegue: `python manage.py migrate` tras backup si hay `db-change`
- No DDL manual fuera de migraciones salvo excepción documentada en el spec
- Datos masivos: fixtures, seeders o management commands referenciados en spec y release
