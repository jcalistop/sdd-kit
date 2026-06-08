# Instalación — SDD Kit

## Opción 1: Clonar como submodule (recomendado)

Desde la raíz del proyecto destino:

```bash
git submodule add https://github.com/jcalistop/sdd-kit.git sdd-kit
git submodule update --init
```

```powershell
.\sdd-kit\bootstrap\init-sdd.ps1 -Profile laravel-filament -Project "Mi App" -Cursor
```

## Opción 2: Copia puntual

```bash
git clone https://github.com/jcalistop/sdd-kit.git /tmp/sdd-kit
cp -r /tmp/sdd-kit ./sdd-kit
./sdd-kit/bootstrap/init-sdd.sh --profile laravel-filament --project "Mi App" --cursor
```

## Opción 3: Solo documentación core

Si no quieres el submodule, copia manualmente:

- `core/` → `.github/docs/sdd/` (workflow, templates, etc.)
- `profiles/<stack>/` → `.github/docs/sdd/profiles/<stack>/`
- `sdd.config.example.yaml` → `.github/docs/sdd/sdd.config.yaml`

## Post-instalación

1. Editar `.github/docs/sdd/sdd.config.yaml` (dominios, ramas, IDs).
2. Completar `.github/docs/business/README.md` con contexto de producto.
3. Crear primer spec: `specs/<dominio>/SDD-001-slug.md` desde `templates/spec-template.md`.
4. Ajustar `.github/PULL_REQUEST_TEMPLATE.md` si el bootstrap no lo creó.

## Actualizar el kit (submodule)

```bash
cd sdd-kit
git pull origin main
cd ..
git add sdd-kit
git commit -m "chore: actualiza sdd-kit"
```

Los archivos en `.github/docs/sdd/` **no** se sobrescriben solos; revisar diff del kit y portar mejoras manualmente o re-ejecutar init en proyecto nuevo.

## Perfiles

| Perfil | Comando init |
|--------|----------------|
| `laravel-filament` | `-Profile laravel-filament` |

Añadir perfiles en `profiles/<nombre>/` sin modificar `core/`.
