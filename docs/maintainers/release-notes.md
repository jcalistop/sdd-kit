Primera versión del SDD Kit — metodología spec-driven development portable para equipos pequeños.

## Qué incluye

- **Core**: ciclo SDD, BACKLOG, ADR, releases, plantillas base (agnóstico al stack)
- **Bootstrap**: scripts de inicialización `init-sdd.sh` y `init-sdd.ps1` para Linux/macOS y Windows
- **Configuración**: `sdd.config.example.yaml` para personalizar por proyecto
- **Perfil `laravel-filament`**: Laravel 10+, Filament 3+, Pint, Pest, migraciones, Laravel Cloud
- **Perfil `laravel-voyager`**: Laravel 10+, Voyager, Livewire 3, PHPUnit, deploy híbrido intranet + CI
- **Reglas Cursor AI**: integración opcional con Cursor IDE vía flag `--cursor`

## Instalación rápida

```bash
git submodule add https://github.com/jcalistop/sdd-kit.git sdd-kit
./sdd-kit/bootstrap/init-sdd.sh --profile laravel-filament --project "Mi App" --cursor
```

Más info en [README.md](../../README.md) e [INSTALL.md](../../INSTALL.md).
