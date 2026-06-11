# Instalación — SDD Kit

## Opción 1: Clonar como submodule (recomendado)

Desde la raíz del proyecto destino:

```bash
git submodule add https://github.com/jcalistop/sdd-kit.git sdd-kit
git submodule update --init
```

```powershell
.\sdd-kit\bootstrap\init-sdd.ps1 -Profile laravel-filament -Project "Mi App"
```

Por defecto (`-Agent auto`) detecta tu IDE/agente y muestra un menú si hay ambigüedad. También puedes forzar adaptadores:

```powershell
.\sdd-kit\bootstrap\init-sdd.ps1 -Profile laravel-filament -Project "Mi App" -Agent cursor,claude
.\sdd-kit\bootstrap\init-sdd.ps1 -Profile laravel-filament -Project "Mi App" -Agent none
```

| Adaptador | Archivos instalados                                                              |
| --------- | -------------------------------------------------------------------------------- |
| `cursor`  | `.cursor/rules/sdd-core.mdc`, `sdd-agent-workflow.mdc`, `sdd-stack-<perfil>.mdc` |
| `claude`  | `CLAUDE.md` (bloque delimitado)                                                  |
| `codex`   | `AGENTS.md` (bloque delimitado)                                                  |
| `copilot` | `.github/copilot-instructions.md`                                                |

Retrocompat: `-Cursor` / `--cursor` equivale a `-Agent cursor`. Guía completa: [core/agent-setup.md](core/agent-setup.md).

## Opción 2: Copia puntual

```bash
git clone https://github.com/jcalistop/sdd-kit.git /tmp/sdd-kit
cp -r /tmp/sdd-kit ./sdd-kit
./sdd-kit/bootstrap/init-sdd.sh --profile laravel-filament --project "Mi App"
```

## Opción 3: Solo documentación core

Si no quieres el submodule, copia manualmente:

- `core/` → `.github/docs/sdd/` (workflow, adoption-guide, templates, etc.)
- `profiles/<stack>/` → `.github/docs/sdd/profiles/<stack>/`
- `sdd.config.example.yaml` → `.github/docs/sdd/sdd.config.yaml`

## Post-instalación

1. Editar `.github/docs/sdd/sdd.config.yaml` (dominios, ramas, IDs).
2. Completar `.github/docs/business/README.md` con contexto de producto.
3. Opcional: completar `.github/docs/business/domain-rules.md` (reglas de negocio transversales).
4. Leer `.github/docs/sdd/adoption-guide.md` — **proyectos existentes**: empezar por Etapa 1.
5. Consultar `.github/docs/sdd/healthy-development.md` — arquitectura, patrones y codigo limpio.
6. Crear primer spec real desde `templates/spec-template.md` (usar `profiles/<stack>/examples/` como referencia).
7. Validar: `.\sdd-kit\bootstrap\validate-sdd.ps1`

## CLI SDD (recomendado)

Requiere Python 3.10+. Ver [cli/README.md](cli/README.md).

```powershell
.\sdd-kit\bootstrap\sdd.ps1 validate
.\sdd-kit\bootstrap\sdd.ps1 backlog
.\sdd-kit\bootstrap\sdd.ps1 spec new --domain api --type feature --title "CRUD productos"
.\sdd-kit\bootstrap\sdd.ps1 release changelog
.\sdd-kit\bootstrap\sdd.ps1 metrics
.\sdd-kit\bootstrap\sdd.ps1 backlog sync --dry-run   # requiere gh CLI
```

## Reinstalar adaptadores de agente

Tras actualizar el kit o cambiar de herramienta:

```powershell
python .\sdd-kit\bootstrap\install-agents.py install --profile laravel-filament --agent cursor,claude
python .\sdd-kit\bootstrap\install-agents.py detect
```

Ver [core/agent-setup.md](core/agent-setup.md).

## Validación documental (scripts directos)

```powershell
.\sdd-kit\bootstrap\validate-sdd.ps1
```

```bash
./sdd-kit/bootstrap/validate-sdd.sh
```

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

| Perfil             | Comando init                |
| ------------------ | --------------------------- |
| `laravel-filament` | `-Profile laravel-filament` |
| `laravel-voyager`  | `-Profile laravel-voyager`  |
| `python-fastapi`   | `-Profile python-fastapi`   |
| `python-django`    | `-Profile python-django`    |
| `react-vite`       | `-Profile react-vite`       |
| `reports-latex-md` | `-Profile reports-latex-md` |

Añadir perfiles en `profiles/<nombre>/` sin modificar `core/`. Guía: [core/templates/profile-template.md](core/templates/profile-template.md).

## Proyectos existentes

No requiere reescribir documentación ni specs retrospectivos. Ver [core/adoption-guide.md](core/adoption-guide.md):

1. **Etapa 1** — BACKLOG + inventario (día 1)
2. **Etapa 2** — nuevas features con ciclo SDD completo
3. **Etapa 3** — cobertura completa y migración de docs legacy
