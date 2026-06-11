# Impacto técnico — Laravel + Filament

> Sección obligatoria en todo spec. Copiar al crear `SDD-NNN` o referenciar desde la plantilla.

## Impacto técnico _(obligatorio)_

Responder cada ítem. Si no aplica: "No aplica — [razón]".

| Pregunta                                                              | Respuesta |
| --------------------------------------------------------------------- | --------- |
| ¿Afecta panel Filament (resources, pages, widgets)?                   |           |
| ¿Requiere policies, roles o permisos nuevos o modificados?            |           |
| ¿Incluye `db-change` (solo migraciones en `database/migrations/`)?    |           |
| ¿Afecta rutas HTTP o API pública?                                     |           |
| ¿Requiere `php artisan optimize:clear` / limpieza de caché al deploy? |           |
| ¿Introduce dependencia o integración externa nueva?                   |           |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR.          |           |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles.   |           |

## Regla de esquema

- Todo cambio de BD vía migraciones Laravel en `database/migrations/`
- Despliegue: `php artisan migrate --force` (backup documentado en release)
- Datos masivos: seeders o comandos Artisan referenciados en spec y release
