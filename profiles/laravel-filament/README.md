# Perfil: Laravel + Filament

Extensión del SDD core para proyectos Laravel 10+ con Filament 3+.

| Archivo                                                | Uso                                             |
| ------------------------------------------------------ | ----------------------------------------------- |
| [checklist-stack.md](checklist-stack.md)               | DoD técnico (Pint, Pest, Filament, migraciones) |
| [spec-impact.md](spec-impact.md)                       | Tabla "Impacto técnico" para specs              |
| [deploy.md](deploy.md)                                 | Laravel Cloud y smoke                           |
| [branching-extensions.md](branching-extensions.md)     | Rama `dep-integration` + Dependabot             |
| [release-deploy-section.md](release-deploy-section.md) | Bloque para notas de release                    |

**Quality gates por defecto:**

- `php artisan test --compact`
- `vendor/bin/pint --dirty`
- Migraciones solo en `database/migrations/`
- Deploy: Laravel Cloud al merge en `main`
