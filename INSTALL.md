# Instalación — SDD Kit

## Requisitos previos

| Requisito        | Obligatorio             | Notas                                                                                                 |
| ---------------- | ----------------------- | ----------------------------------------------------------------------------------------------------- |
| Git              | Sí                      | Para submodule o copia versionada                                                                     |
| Python 3.10+     | Recomendado             | CLI (`python sdd-kit/cli/sdd.py`), `install-agents.py`; atajos `sdd.sh` / `sdd.ps1` (solo PowerShell) |
| Stack del perfil | Según perfil            | PHP/Composer (Laravel), Node (React), etc. — ver `profiles/<perfil>/README.md`                        |
| Agente IA        | Recomendado             | Cursor, Claude Code, Codex o Copilot — ver [core/agent-setup.md](core/agent-setup.md)                 |
| Pandoc + LaTeX   | Solo `reports-latex-md` | Compilación de informes                                                                               |
| `gh` CLI         | Opcional                | `sdd backlog sync` con GitHub Issues                                                                  |

---

## Modo agente (recomendado en proyectos existentes)

En repos **con código y documentación previa**, evita ejecutar `init-sdd` manualmente sin revisar el contexto. Flujo seguro:

1. **Humano:** añade el submodule (un comando Git).
2. **Humano:** pega el prompt de adopción en el agente (ver [README.md](README.md) — Paso 3, proyecto existente).
3. **Agente:** lee `core/adoption-guide.md` Etapa 1, ejecuta `init-sdd` solo si no hay instancia SDD, completa config y BACKLOG sin specs retrospectivos, instala adaptadores y corre `validate-sdd`.

El agente debe **preguntar antes de sobrescribir** cualquier archivo en `.github/docs/sdd/` o `business/` que ya exista.

### Prompt de adopción

```bash
python sdd-kit/cli/sdd.py prompt show adopt-existing
```

Catálogo completo: [core/prompt-catalog.md](core/prompt-catalog.md) — también en `.github/docs/sdd/` tras `init-sdd`.

---

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

| Adaptador | Archivos instalados                                                                                            |
| --------- | -------------------------------------------------------------------------------------------------------------- |
| `cursor`  | `.cursor/rules/sdd-core.mdc`, `sdd-agent-workflow.mdc`, `sdd-workflow-reference.mdc`, `sdd-stack-<perfil>.mdc` |
| `claude`  | `CLAUDE.md` (bloque delimitado)                                                                                |
| `codex`   | `AGENTS.md` (bloque delimitado)                                                                                |
| `copilot` | `.github/copilot-instructions.md`                                                                              |

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
7. Validar: `python sdd-kit/cli/sdd.py validate`

## CLI SDD (recomendado)

Requiere Python 3.10+. Ver [cli/README.md](cli/README.md).

```bash
python sdd-kit/cli/sdd.py validate
python sdd-kit/cli/sdd.py backlog
python sdd-kit/cli/sdd.py spec new --domain api --type feature --title "CRUD productos"
python sdd-kit/cli/sdd.py release changelog
python sdd-kit/cli/sdd.py metrics
python sdd-kit/cli/sdd.py backlog sync --dry-run   # requiere gh CLI
```

## Reinstalar adaptadores de agente

Tras actualizar el kit o cambiar de herramienta:

```powershell
python .\sdd-kit\bootstrap\install-agents.py install --profile laravel-filament --agent cursor,claude
python .\sdd-kit\bootstrap\install-agents.py detect
```

Ver [core/agent-setup.md](core/agent-setup.md).

## Validación documental

```bash
python sdd-kit/cli/sdd.py validate
```

Scripts legacy (misma lógica): `./sdd-kit/bootstrap/validate-sdd.sh` · `.\sdd-kit\bootstrap\validate-sdd.ps1` (PowerShell)

```bash
./sdd-kit/bootstrap/validate-sdd.sh
```

## Actualizar el kit (submodule)

Cuando publica una versión nueva del kit, sigue el runbook **[`core/upgrade-guide.md`](core/upgrade-guide.md)** (detectar versión → changelog → submodule → merge instancia → adaptadores → validate → log).

**Prompt recomendado** (modo agente):

```bash
python sdd-kit/cli/sdd.py prompt show upgrade-kit --full
```

Sustituye `<VERSION>` por el tag SemVer (ej. `v1.1.0`).

Resumen manual del submodule:

```bash
cd sdd-kit
git fetch origin --tags
git checkout vX.Y.Z
cd ..
git add sdd-kit
git commit -m "chore: actualiza sdd-kit a vX.Y.Z"
```

Los archivos en `.github/docs/sdd/` **no** se sobrescriben solos. Registra cada upgrade en `UPGRADE-LOG.md` y actualiza `kit.installed_version` en `sdd.config.yaml` tras validar.

## Perfiles

| Perfil             | Comando init                   |
| ------------------ | ------------------------------ |
| `laravel-filament` | `-Profile laravel-filament`    |
| `laravel-voyager`  | `-Profile laravel-voyager`     |
| `python-fastapi`   | `-Profile python-fastapi`      |
| `python-django`    | `-Profile python-django`       |
| `react-vite`       | `-Profile react-vite`          |
| `reports-latex-md` | `-Profile reports-latex-md`    |
| `sdd-kit`          | Solo repo del kit (dogfooding) |

Añadir perfiles en `profiles/<nombre>/` sin modificar `core/`. Guía: [core/templates/profile-template.md](core/templates/profile-template.md).

## Proyectos existentes

No requiere reescribir documentación ni specs retrospectivos.

**Instalación:** usar [Modo agente](#modo-agente-recomendado-en-proyectos-existentes) arriba. Si instalas a mano, revisa que `init-sdd` no pise archivos ya editados (el script no sobrescribe `business/README.md` si existe, pero sí copia plantillas core a `.github/docs/sdd/`).

Ver [core/adoption-guide.md](core/adoption-guide.md):

1. **Etapa 1** — BACKLOG + inventario (día 1); sin specs para lo ya en producción
2. **Etapa 2** — nuevas features con ciclo SDD completo
3. **Etapa 3** — cobertura completa y migración de docs legacy

### Qué debe evitar el agente (y tú) en repos existentes

- Crear specs retrospectivos para todo el código ya desplegado
- Reemplazar documentación que ya existe en el proyecto (READMEs, docs en repo, Confluence, Google Docs, correos, lo que sea) sin un plan acordado — eso va en Etapa 3, no en la instalación
- Ejecutar `init-sdd` repetido esperando “resetear” la instancia SDD
- Mover o borrar documentación fuera de `paths.sdd` sin petición explícita
