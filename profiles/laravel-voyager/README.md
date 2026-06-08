# Perfil: Laravel + Voyager + Livewire

Extensión del SDD core para proyectos Laravel 10+ con Voyager (admin `/admin`), Livewire 3, PHPUnit y deploy híbrido (CI GitHub + intranet).

| Archivo | Uso |
| ------------------------------------------------------ | --------------------------------------------------------------- |
| [checklist-stack.md](checklist-stack.md) | DoD técnico (PHPUnit, Pint, Voyager, Livewire, migraciones) |
| [spec-impact.md](spec-impact.md) | Tabla "Impacto técnico" para specs |
| [deploy.md](deploy.md) | Orquestador intranet, backup, smoke |
| [branching-extensions.md](branching-extensions.md) | Rama `deps-integration` + Dependabot |
| [release-deploy-section.md](release-deploy-section.md) | Bloque para notas de release |

**Quality gates por defecto:**

- `php artisan test --compact`
- `vendor/bin/pint --dirty`
- Migraciones solo en `database/migrations/`
- Deploy: orquestador interno en servidor intranet (no auto-deploy desde GitHub)
