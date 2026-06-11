# Impacto técnico — Laravel + Voyager + Livewire

> Sección obligatoria en todo spec. Copiar al crear `SDD-NNN` o referenciar desde la plantilla de la instancia.
> Reglas de negocio específicas del proyecto: `.github/docs/business/domain-rules.md`.

## Impacto técnico _(obligatorio)_

Responder cada ítem. Si no aplica: "No aplica — [razón]".

| Pregunta                                                                 | Respuesta |
| ------------------------------------------------------------------------ | --------- |
| ¿Es visible en BREAD de Voyager (`/admin`)?                              |           |
| ¿Afecta componentes Livewire (formularios, listas, acciones)?            |           |
| ¿Requiere policies, roles o permisos nuevos o modificados?               |           |
| ¿Toca rutas HTTP (`routes/web.php`, `routes/api.php`) o rutas dinámicas? |           |
| ¿Requiere invalidar caché de rutas o configuración al deploy?            |           |
| ¿Incluye `db-change` (solo migraciones en `database/migrations/`)?       |           |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles.      |           |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR.             |           |

## Regla de esquema

- Todo cambio de BD vía migraciones Laravel en `database/migrations/`
- Despliegue: `php artisan migrate --force` tras backup (orquestador interno o manual)
- No asumir que `database/migrations/` representa el esquema histórico completo si Voyager fue fuente original
- Datos masivos: seeders o comandos Artisan referenciados en spec y release
