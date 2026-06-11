# Changelog — SDD Kit

Todos los cambios relevantes del **repositorio del kit** se documentan aquí.

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/).  
Las notas detalladas en lenguaje accesible están en `vX.Y.Z.md` y en [GitHub Releases](https://github.com/jcalistop/sdd-kit/releases).

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
