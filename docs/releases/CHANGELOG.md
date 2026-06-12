# Changelog — SDD Kit

Todos los cambios relevantes del **repositorio del kit** se documentan aquí.

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/).  
Las notas detalladas en lenguaje accesible están en `vX.Y.Z.md` y en [GitHub Releases](https://github.com/jcalistop/sdd-kit/releases).

---

## [1.1.0] - 2026-06-12

Ver [v1.1.0.md](v1.1.0.md).

### Añadido

- Runbook `core/upgrade-guide.md` y prompt `upgrade-kit` para actualizar instancias consumidoras
- `kit.installed_version` / `kit.installed_at` en `sdd.config.yaml` y plantilla `UPGRADE-LOG.md`
- `bootstrap/kit-version.py` — detección de versión para `init-sdd` y `validate-sdd`
- Perfil `profiles/sdd-kit/` para mantenedores (SDD-001)
- Prompt `verify-implementation` — gate obligatorio antes de push/PR (SDD-003)
- Prompt `build-spec` — fusiona `approve-ready` + `implement-spec` (SDD-003)
- Diagramas de secuencia Mermaid del ciclo humano–agente (SDD-003)

### Cambiado

- `init-sdd` registra versión del kit al bootstrap
- `validate-sdd` advierte si la versión registrada difiere del kit en disco
- README, INSTALL y `adoption-guide` enlazan al flujo de actualización
- `workflow.md`, `prompt-catalog.md` y `concepts.md` — momentos semánticos vs prompts (SDD-003)
- `draft-review` documentado como opcional
- `checklist-pr.md` — multi-spec y evidencia de verify
- Reglas Cursor y bootstrap sincronizados con el nuevo flujo

### Deprecado

- `approve-ready` e `implement-spec` → usar `build-spec`

---

## [1.0.0] - 2026-06-11

Primera versión **estable**. Ver [v1.0.0.md](v1.0.0.md).

### Añadido

- Perfiles: `python-fastapi`, `python-django`, `react-vite`, `reports-latex-md`
- CLI unificada (`validate`, `backlog`, `spec new`, `metrics`, sync con GitHub Issues)
- Adaptadores multi-agente: Cursor, Claude Code, Codex, GitHub Copilot (`core/agent-setup.md`, `install-agents.py`)
- Guías: `concepts.md`, `adoption-guide.md`, `healthy-development.md`, plantilla spec simple
- Flujo agéntico (`sdd-agent-workflow.mdc`) y guardias de arquitectura sana
- Contexto de negocio: `business/domain-rules.md`, sesión guiada con el agente
- Ejemplos de spec por perfil y ejemplo no técnico en `core/examples/`
- Validador SDD mejorado (códigos de salida 1 vs 2)
- Documentación de instalación: requisitos previos y **modo agente** para proyectos existentes
- Artefactos de comunidad: CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, plantillas GitHub, CI

### Cambiado

- README e INSTALL orientados a principiantes técnicos
- Dominio de negocio desacoplado del perfil `laravel-voyager`
- `init-sdd` detecta agente automáticamente (`-Agent auto`)

### Documentación

- `docs/maintainers/` — planificación (ROADMAP, ANALYSIS)
- `docs/releases/` — historial de versiones del kit (este archivo)

---

## [0.1.0] - 2026-06-11

**Pre-release** — primera publicación de prueba. Ver [v0.1.0.md](v0.1.0.md).

### Añadido

- Core SDD: workflow, plantillas, BACKLOG, ADR, releases
- Bootstrap: `init-sdd.sh`, `init-sdd.ps1`
- Perfiles: `laravel-filament`, `laravel-voyager`
- Reglas Cursor (`--cursor` / `sdd-stack-*.mdc`)
- `sdd.config.example.yaml`
