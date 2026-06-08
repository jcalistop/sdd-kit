# SDD Kit — Spec-Driven Development

Metodología spec-driven portable para equipos pequeños. Agnóstica al producto y al stack (vía perfiles).

## Arquitectura en 3 capas

| Capa          | Carpeta             | Contenido                                                               |
| ------------- | ------------------- | ----------------------------------------------------------------------- |
| **Core**      | `core/`             | Ciclo SDD, BACKLOG, ADR, releases, plantillas base — agnóstico al stack |
| **Profile**   | `profiles/<stack>/` | CI, calidad, deploy, branching extendido                                |
| **Instancia** | En cada proyecto    | `sdd.config.yaml`, BACKLOG, specs, `business/`, historial               |

## Repositorio

**https://github.com/jcalistop/sdd-kit**

Instalación detallada: [INSTALL.md](INSTALL.md).

## Adopción rápida

```bash
git submodule add https://github.com/jcalistop/sdd-kit.git sdd-kit
./sdd-kit/bootstrap/init-sdd.sh --profile laravel-filament --project "Mi App" --cursor
```

En Windows (PowerShell):

```powershell
git submodule add https://github.com/jcalistop/sdd-kit.git sdd-kit
.\sdd-kit\bootstrap\init-sdd.ps1 -Profile laravel-filament -Project "Mi App" -Cursor
```

El script crea `.github/docs/sdd/`, copia plantillas, genera `BACKLOG.md` vacío y opcionalmente reglas Cursor.

## Configuración por proyecto

Copiar `sdd.config.example.yaml` a `.github/docs/sdd/sdd.config.yaml` y ajustar:

- `project.name`, ramas, dominios de iniciativas
- `stack.profile` — perfil a usar
- `paths` — rutas de documentación

## Perfiles disponibles

| Perfil             | Uso                                                                      |
| ------------------ | ------------------------------------------------------------------------ |
| `laravel-filament` | Laravel 10+, Filament 3+, Pint, Pest, migraciones, Laravel Cloud         |
| `laravel-voyager`  | Laravel 10+, Voyager, Livewire 3, PHPUnit, deploy híbrido intranet + CI |

Añadir perfiles nuevos bajo `profiles/` sin tocar `core/`.

## Consumir en proyectos

- **Submodule** (recomendado) — `git submodule add https://github.com/jcalistop/sdd-kit.git sdd-kit`
- **Copia puntual** — `git clone` + carpeta `sdd-kit/` en el proyecto
- **Subtree** — merge periódico desde upstream en monorepos

## Sincronizar cambios del kit (mantenedores)

Si el kit vive como **submodule** en un repo consumidor:

```bash
cd .github/docs/sdd-kit   # o la ruta configurada en el proyecto
# editar, commit y push a este repositorio (sdd-kit)
cd ../..
git add .github/docs/sdd-kit
git commit -m "chore: actualiza puntero sdd-kit"
```

Alternativa histórica con **subtree** desde un monorepo:

```bash
git subtree split -P <ruta-al-kit> -b sdd-kit-export
cd ../sdd-kit && git pull <repo-consumidor> sdd-kit-export:main
```

## Instancia en el proyecto consumidor

Cada proyecto mantiene su capa operativa en `.github/docs/sdd/` (BACKLOG, specs, releases). El submodule `sdd-kit/` aporta core + perfiles; ver `PROJECT.md` y `sdd.config.yaml` en la instancia del consumidor.

## Estructura

```
sdd-kit/
├── README.md
├── sdd.config.example.yaml
├── core/
│   ├── workflow.md
│   ├── operations.md
│   ├── branching.md
│   ├── checklist-pr.md
│   ├── templates/
│   └── releases/
├── profiles/
│   ├── laravel-filament/
│   └── laravel-voyager/
└── bootstrap/
    ├── init-sdd.sh
    ├── init-sdd.ps1
    └── cursor-rules/
```
