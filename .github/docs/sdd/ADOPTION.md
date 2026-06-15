# Adopción SDD en sdd-kit

> Este repositorio **produce** la metodología SDD pero no la usaba para su propio desarrollo.
> A partir de 2026-06-12 se adopta SDD de forma incremental siguiendo [`core/adoption-guide.md`](../../../core/adoption-guide.md).

## Decisión

| Aspecto                  | Valor                                                           |
| ------------------------ | --------------------------------------------------------------- |
| **Ruta de instancia**    | `.github/docs/sdd/` (estándar consumidor; dogfooding)           |
| **Contexto de producto** | `.github/docs/business/`                                        |
| **Principio**            | No reescribir el pasado — sin specs retrospectivos obligatorios |
| **Etapa actual**         | 2 (nuevas features con ciclo completo)                          |

## Separación producto vs proceso

| Capa                          | Ubicación                                  | Rol                                                             |
| ----------------------------- | ------------------------------------------ | --------------------------------------------------------------- |
| **Producto**                  | `core/`, `profiles/`, `bootstrap/`, `cli/` | Lo que otros proyectos instalan con `init-sdd`                  |
| **Proceso SDD**               | `.github/docs/sdd/` (este directorio)      | BACKLOG, specs, releases de iniciativas                         |
| **Contexto del producto**     | `.github/docs/business/`                   | Qué es el kit y reglas que el agente no debe violar             |
| **Planificación estratégica** | `.github/docs/business/planning/`          | Análisis y roadmap histórico (referencia, no tablero operativo) |
| **Versiones del kit**         | `docs/releases/`                           | Changelog SemVer del producto (`v1.0.0`, etc.)                  |

**Anti-confusión:**

- `business/planning/ROADMAP.md` = snapshot estratégico histórico.
- `BACKLOG.md` (aquí) = tablero operativo de iniciativas.
- `docs/releases/` = versiones publicadas del **kit**.
- `.github/docs/sdd/releases/` = releases de **iniciativas SDD** del kit (acta: specs + gates; narrativa en `docs/releases/`).

### Contrato de releases (tres capas)

| Capa                          | Ruta                                | Rol                                                | ¿Copiado por `init-sdd`?          |
| ----------------------------- | ----------------------------------- | -------------------------------------------------- | --------------------------------- |
| Release producto kit          | `docs/releases/vX.Y.Z.md`           | Notas para consumidores y GitHub Releases          | No (vive en submodule)            |
| Cierre campaña SDD (kit)      | `.github/docs/sdd/releases/vX.Y.Z/` | Acta SDD: specs, gates, enlace al producto         | No                                |
| Plantillas release consumidor | `core/releases/`                    | RUNBOOK y plantillas para **apps** que adoptan SDD | Sí → `.github/docs/sdd/releases/` |

## Etapas de adopción

### Etapa 1 — Mínima viable (completada en documentación)

- [x] Estructura `.github/docs/sdd/` y `.github/docs/business/`
- [x] `sdd.config.yaml` con dominios del kit
- [x] `business/README.md` y `domain-rules.md` completados
- [x] `BACKLOG.md` con inventario pre-SDD y Discovery
- [x] `validate-sdd` en verde
- [x] Adaptadores de agente verificados (Cursor)

### Etapa 2 — Nuevas features con SDD

Todo cambio **no trivial** del kit entra al ciclo: Discovery → Draft → Ready → In Build → Validating → Released.

**Primer spec completado:** `SDD-001` — perfil `profiles/sdd-kit/` ([archivo](archive/2026/profiles/SDD-001-perfil-sdd-kit.md)).

**Campaña v1.2.0 cerrada (2026-06-15):** `SDD-004` — skills en `bootstrap/agent-skills/` ([archivo](archive/2026/bootstrap/SDD-004-agent-skills-cursor.md)); `SDD-005` — reordenamiento documentación ([archivo](archive/2026/docs/SDD-005-reordenamiento-documentacion-kit.md)); release [v1.2.0](releases/v1.2.0/release_v1.2.0.md).

Cambios triviales (typo, bump deps, copy) → ID `—` en release; no requieren spec.

### Etapa 3 — Cobertura completa (opcional, mes 2+)

- Refactors riesgosos con spec tipo `refactor`
- ADRs en `.github/docs/sdd/adr/`
- Job CI con `validate-sdd` en cada PR

## Flujo para mantenedores

| Momento    | Humano             | Agente                                    |
| ---------- | ------------------ | ----------------------------------------- |
| Nueva idea | Describe necesidad | Fila Discovery en BACKLOG                 |
| Draft      | Aprueba spec       | Redacta spec, verifica DoR                |
| In Build   | Autoriza           | Implementa según spec + `domain-rules.md` |
| Validating | Revisa y mergea PR | Checklist + evidencia CI                  |
| Released   | Aprueba cierre     | Archiva spec, actualiza BACKLOG           |

Prompts: [`core/prompt-catalog.md`](../../../core/prompt-catalog.md).

## Referencias

- [BACKLOG.md](BACKLOG.md) — tablero operativo
- [../business/domain-rules.md](../business/domain-rules.md) — reglas del producto kit
- [../business/planning/ROADMAP.md](../business/planning/ROADMAP.md) — roadmap histórico (fases 1–4)
- [../business/planning/ANALYSIS.md](../business/planning/ANALYSIS.md) — análisis crítico previo a la adopción
- [../../../docs/README.md](../../../docs/README.md) — glosario capas `docs/` vs instancia SDD
