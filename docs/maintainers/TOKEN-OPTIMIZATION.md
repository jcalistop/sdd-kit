# Optimizacion de tokens — reglas del agente SDD

> Plan de mantenimiento para reducir el consumo fijo de tokens en sesiones de Cursor y otros agentes.
> Fecha: 2026-06-12

**Relacionado:** [ANALYSIS.md](ANALYSIS.md) · [ROADMAP.md](ROADMAP.md) · [core/agent-setup.md](../../core/agent-setup.md)

---

## Problema

Tres archivos `.mdc` con `alwaysApply: true` inyectaban ~2,900 tokens en **cada** sesion de Cursor, incluso para tareas que no involucran SDD (preguntas triviales, fixes de copy, etc.).

| Archivo (antes)          | Lineas | Tokens aprox. |
| ------------------------ | ------ | ------------- |
| `sdd-agent-workflow.mdc` | 260    | ~2,100        |
| `sdd-core.mdc`           | 55     | ~475          |
| `sdd-stack-*.mdc`        | ~43    | ~325          |

**Causa raiz:** `bootstrap/adapters/cursor-rule.mdc.tpl` hardcodeaba `alwaysApply: true` y `sdd-agent-workflow.md` era un manual de referencia completo (checklists, tablas de antipatrones, manejo de errores), no reglas minimas.

### Escenarios de desperdicio

| Escenario                       | Tokens en reglas | Utilidad |
| ------------------------------- | ---------------- | -------- |
| Pregunta simple ("que hace X?") | ~2,900           | ~0%      |
| Fix trivial (typo)              | ~2,900           | ~15%     |
| Ciclo SDD completo (spec → PR)  | ~2,900           | ~100%    |

En un dia con ~20 chats mixtos, el desperdicio estimado es **50,000–60,000 tokens** solo en reglas always-on.

---

## Solucion

Dividir las reglas en dos niveles de persistencia:

| Nivel          | Cuando se carga                       | Contenido                                     |
| -------------- | ------------------------------------- | --------------------------------------------- |
| **Esencial**   | `alwaysApply: true` — cada sesion     | Dispatch minimo + fases con acciones clave    |
| **Referencia** | `alwaysApply: false` — bajo demanda   | Checklists DoR/DoD, antipatrones, errores     |
| **Stack**      | `alwaysApply: false` — fase In Build+ | Quality gates, migraciones, deploy del perfil |

### Arquitectura objetivo

```
bootstrap/agent-prompts/          (fuente unica)
├── sdd-core.md                   → sdd-core.mdc                  alwaysApply: true   ~150 tokens
├── sdd-agent-workflow.md         → sdd-agent-workflow.mdc        alwaysApply: true   ~450 tokens
├── sdd-workflow-reference.md     → sdd-workflow-reference.mdc    alwaysApply: false  ~1,300 tokens
└── stacks/<perfil>.md          → sdd-stack-<perfil>.mdc        alwaysApply: false  ~325 tokens
```

**Total always-apply (medido):** ~950 tokens (**ahorro ~67%** vs. ~2,900 anteriores). Objetivo inicial ~600; margen de mejora futura en `sdd-agent-workflow.md` si hace falta.

El agente lee `sdd-workflow-reference.mdc` cuando entra en Draft (DoR), In Build (arquitectura sana) o Validating (DoD). Los prompts copy-paste del [catalogo](../../core/prompt-catalog.md) siguen siendo disparadores explicitos del humano.

---

## Cambios implementados

| Archivo                                             | Cambio                                                                   |
| --------------------------------------------------- | ------------------------------------------------------------------------ |
| `bootstrap/adapters/cursor-rule.mdc.tpl`            | `alwaysApply` parametrizable (`{{ALWAYS_APPLY}}`)                        |
| `bootstrap/agent-prompts/sdd-core.md`               | Reducido a dispatch minimo (~20 lineas)                                  |
| `bootstrap/agent-prompts/sdd-agent-workflow.md`     | Reescrito a nivel esencial (~80–100 lineas)                              |
| `bootstrap/agent-prompts/sdd-workflow-reference.md` | **Nuevo** — checklists y tablas extraidas del workflow                   |
| `bootstrap/agent-prompts/manifest.json`             | Entrada `reference`                                                      |
| `bootstrap/install-agents.py`                       | Instala reference y stack con `alwaysApply: false`                       |
| `bootstrap/cursor-rules/*.mdc`                      | Sincronizados con la nueva estructura                                    |
| `bootstrap/sync-cursor-rules.py`                    | Script de mantenimiento: regenera `cursor-rules/` desde `agent-prompts/` |
| `core/agent-setup.md`                               | Tabla de archivos y politica alwaysApply actualizada                     |

---

## Que NO cambia

- CLI `sdd prompt show <id>` — ya extrae solo el bloque `## Prompt` (~60–100 tokens).
- Documentacion en `core/` (`workflow.md`, `adoption-guide.md`, etc.) — se lee bajo demanda, no se inyecta.
- Prompts copy-paste en `core/prompts/` — sin cambios.
- Claude Code / Codex / Copilot — `combined_body()` incluye core + workflow + reference + stack (bloque unico por sesion; sin `alwaysApply` repetido por mensaje).

---

## Metricas de exito

- [x] Tokens always-apply en Cursor ≤ 1,000 (medido ~952: core ~246 + workflow ~706)
- [ ] Agente sigue completando ciclo Discovery → Released en proyecto real
- [ ] `install-agents.py install --agent cursor` genera 4 archivos `.mdc` con flags correctos
- [ ] Proyectos existentes: reinstalar adaptadores tras actualizar submodule

---

## Reinstalacion en proyectos consumidores

Tras actualizar el submodule `sdd-kit`:

```powershell
python .\sdd-kit\bootstrap\install-agents.py install `
  --profile <perfil> `
  --agent cursor `
  --sdd-path .github/docs/sdd
```

Verificar en `.cursor/rules/` que existan `sdd-core.mdc`, `sdd-agent-workflow.mdc`, `sdd-workflow-reference.mdc` y `sdd-stack-<perfil>.mdc` con los `alwaysApply` esperados.

---

## Referencias

- [core/prompt-catalog.md](../../core/prompt-catalog.md) — cuando copiar prompt vs. dejar que las reglas actuen solas
- [PROMPT-CATALOG.md](PROMPT-CATALOG.md) — mantenimiento del catalogo de prompts
