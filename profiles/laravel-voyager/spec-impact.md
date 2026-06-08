# Impacto técnico — Laravel + Voyager + Livewire

> Sección obligatoria en todo spec. Copiar al crear `SDD-NNN` o referenciar desde la plantilla de la instancia.

## Impacto técnico _(obligatorio)_

Responder cada ítem. Si no aplica: "No aplica — [razón]".

| Pregunta                                                                       | Respuesta |
| ------------------------------------------------------------------------------ | --------- |
| ¿Afecta flujo pre-2025 (`ano < 2025`)?                                         |           |
| ¿Afecta flujo 2025+ (`ano >= 2025`)?                                           |           |
| ¿Afecta un `indicatorType` concreto? ¿Cuál?                                    |           |
| ¿Afecta filtrado por `cen_hie_dependency_id`?                                  |           |
| ¿Toca rutas dinámicas (`routes/web.php` o `IndicatorType`)?                    |           |
| ¿Requiere invalidar caché `indicator_type_routes`?                             |           |
| ¿Es visible en BREAD de Voyager (`/admin`)?                                    |           |
| ¿Afecta `CurrentCutoffPolicy` (gates `current-add-edit` / `current-download`)? |           |
| ¿Incluye `db-change` (solo migraciones en `database/migrations/`)?             |           |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR.                   |           |

## Regla de esquema

- Todo cambio de BD vía migraciones Laravel en `database/migrations/`
- Despliegue: `php artisan migrate --force` tras backup (orquestador interno o manual)
- No asumir que `database/migrations/` representa el esquema histórico completo si Voyager fue fuente original
- Datos masivos: seeders o comandos Artisan referenciados en spec y release
