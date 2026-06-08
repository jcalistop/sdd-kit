# SDD Kit — Spec-Driven Development

Metodología spec-driven portable para equipos pequeños. Extraída y generalizada desde [backoffice-v2](https://github.com/jcalistop/backoffice-v2).

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

| Perfil             | Uso                                                              |
| ------------------ | ---------------------------------------------------------------- |
| `laravel-filament` | Laravel 10+, Filament 3+, Pint, Pest, migraciones, Laravel Cloud |

Añadir perfiles nuevos bajo `profiles/` sin tocar `core/`.

## Consumir en proyectos

- **Submodule** (recomendado) — `git submodule add https://github.com/jcalistop/sdd-kit.git sdd-kit`
- **Copia puntual** — `git clone` + carpeta `sdd-kit/` en el proyecto
- **Subtree** — merge periódico desde upstream en monorepos

## Sincronizar desde backoffice-v2 (mantenedores)

Si el kit vive embebido en `backoffice-v2` antes de publicar cambios:

```bash
# En backoffice-v2, tras commit de sdd-kit/
git subtree split -P sdd-kit -b sdd-kit-export
cd ../sdd-kit && git pull ../backoffice-v2 sdd-kit-export:main
```

## Relación con backoffice-v2

`backoffice-v2` es la **instancia de referencia**. Sus documentos en `.github/docs/sdd/` siguen siendo la fuente operativa hasta que se migre gradualmente al kit. Ver `.github/docs/sdd/PROJECT.md` en ese repo.

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
│   └── laravel-filament/
└── bootstrap/
    ├── init-sdd.sh
    ├── init-sdd.ps1
    └── cursor-rules/
```
