# Changelog — SDD Kit

Todos los cambios relevantes del **repositorio del kit** se documentan aquí.

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/).  
Las notas detalladas en lenguaje accesible están en `vX.Y.Z.md` y en [GitHub Releases](https://github.com/jcalistop/sdd-kit/releases).

---

## [1.3.1] - 2026-08-05

Ver [v1.3.1.md](v1.3.1.md).

### Cambiado

- `archive/` acepta specs **Released** o **Descartado** (`validate-sdd`, workflow, prompts de agente) — SDD-015
- Spec formalizado Descartado: `git mv` completo a `archive/` **sin stub** en `specs/`
- Estado canónico de cabecera: `Descartado` (dejar de usar `Deprecated`)
- Plantilla BACKLOG: columnas ID / Dominio / Título / Razón / Fecha / Spec en Descartado

### Migración consumidores

- Specs Descartados o `Deprecated` que sigan en `specs/` fallarán `validate-sdd` tras el upgrade: renombrar estado a `Descartado` y mover a `archive/`

---

## [1.3.0] - 2026-07-15

Ver [v1.3.0.md](v1.3.0.md).

### Añadido

- Contrato safe-git always-on (`core/safe-git-contract.md`, regla Cursor) — SDD-007
- Lenguaje guías/sensores en workflow, reference y skills — SDD-008
- Posicionamiento “agent harness” en README y core docs — SDD-009
- `validate-sdd` con salida por componente — SDD-010
- Contrato dual-release producto ↔ campaña + WARN validate — SDD-011
- Governance de tokens A–F (two-zone, compact template, cost-governance) — SDD-012
- CLI `sdd metrics tokens` + checks WARN en validate-sdd — SDD-013

### Cambiado

- Camino canónico de upgrade: `upgrade-kit` / `sdd-upgrade-kit` + checklist post-upgrade (SDD-014)
- `upgrade-guide.md` — verificación safe-git, cost-governance, validate por componente, metrics
- Prompt `upgrade-kit` — reinstalar también si cambió `agent-skills/`

---

## [1.2.2] - 2026-07-14

Ver [v1.2.2.md](v1.2.2.md).

### Cambiado

- Reglas Cursor: fusión `sdd-core` → `sdd-agent-workflow` (menos always-on)
- Skills: lectura previa acotada a draft/build; verify sin cadena circular
- `install-agents.py` — no duplicar skills globales si ya existen en el proyecto
- Plantilla de spec: guía anti-boilerplate (SDD-006)

---

## [1.2.1] - 2026-06-17

Ver [v1.2.1.md](v1.2.1.md).

### Corregido

- `install-agents.py` — `update_sdd_config()` ya no elimina el bloque `kit:` al reinstalar `agent:` en `sdd.config.yaml`
- `bootstrap/test_install_skills.py` — test de regresión para preservación del bloque `kit`

---

## [1.2.0] - 2026-06-15

Ver [v1.2.0.md](v1.2.0.md).

### Añadido

- `bootstrap/agent-skills/` — 6 skills SDD + `manifest.json` y fragmentos por stack (SDD-004)
- `install-agents.py` — `install_cursor_skills()`, mapa skills en preambulos multi-agente, `--kit-path`
- `bootstrap/test_install_skills.py` — tests de instalación
- `validate-sdd` — advertencia si falta `.sdd-kit-manifest.json` con Cursor en targets
- Sección Skills en `core/prompt-catalog.md` y `core/agent-setup.md`
- `docs/README.md` — glosario de capas releases

### Cambiado

- `upgrade-guide.md` — reinstalar skills tras cambios en `agent-skills/`
- CI valida `agent-skills/manifest.json` y ejecuta tests de skills
- Glosario de capas releases en ADOPTION
- `.cursor/skills/sdd-*` y manifest fuera de git (fuente: `bootstrap/agent-skills/`)

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

- `.github/docs/business/planning/` — planificación histórica (ROADMAP, ANALYSIS)
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
