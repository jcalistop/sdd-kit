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
| **Planificación estratégica** | `docs/maintainers/`                        | Análisis y roadmap histórico (referencia, no tablero operativo) |
| **Versiones del kit**         | `docs/releases/`                           | Changelog SemVer del producto (`v1.0.0`, etc.)                  |

**Anti-confusión:**

- `docs/maintainers/ROADMAP.md` = snapshot estratégico histórico.
- `BACKLOG.md` (aquí) = tablero operativo de iniciativas.
- `docs/releases/` = versiones publicadas del **kit**.
- `.github/docs/sdd/releases/` = releases de **iniciativas SDD** del kit (cuando aplique).

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
- [docs/maintainers/ROADMAP.md](../../../docs/maintainers/ROADMAP.md) — roadmap histórico (fases 1–4)
- [docs/maintainers/ANALYSIS.md](../../../docs/maintainers/ANALYSIS.md) — análisis crítico previo a la adopción
