# SDD-012 — Governance de tokens en el harness SDD (formalización A-F)

---

## Cabecera

| Campo                 | Valor                                                                 |
| --------------------- | --------------------------------------------------------------------- |
| **ID**                | `SDD-012`                                                             |
| **Dominio**           | `core`                                                                |
| **Tipo**              | `feature`                                                             |
| **Fecha**             | 2026-07-15                                                            |
| **Estado**            | `Released`                                                            |
| **Versión objetivo**  | `v1.3.0`                                                              |
| **Owner**             | mantenedor                                                            |
| **Prioridad**         | `P1`                                                                  |
| **ADRs relacionados** | `ADR-002`                                                             |
| **Dependencias**      | SDD-006 (optimización tokens); research token-economics 2026-07-15    |

---

## Problema y objetivo

**Problema:**

SDD-006 redujo ~1,470 líneas de contexto redundante, pero el kit aún no tenía governance de costo a nivel harness: sin two-zone prompt (cache-shape), sin scoping de contexto por skill, sin plantilla compacta, sin circuit breaker de sesión ni threshold documentado para decidir cuándo un cambio trivial no necesita spec. El research [2026-07-15-token-economics-sdd-harness.md](../../research/2026-07-15-token-economics-sdd-harness.md) demostró que el riesgo de quema de tokens no está en el spec (~2.4%) sino en loops agenticos sin governance; y que un harness bien diseñado reduce tokens ~38% y costo ~41%.

Las propuestas A–F del research se implementaron de inmediato (bajo riesgo, sin API nueva). Falta el spec formal para trazabilidad SDD, DoD y cierre en `v1.3.0`.

**Objetivo:**

Formalizar en un spec único las cinco propuestas de governance de tokens ya implementadas en `core/` y `bootstrap/`, con criterios de aceptación verificables, para que el harness SDD incorpore disciplina de costo como atributo del producto (alineado con ADR-002).

---

## Alcance

**Incluye:**

| Propuesta | Entregable |
|-----------|------------|
| **A** Two-zone prompt | `cacheZone` en `bootstrap/agent-prompts/manifest.json`; orden stable→volatile en `install-agents.py` y `sync-cursor-rules.py` |
| **B** Context scoping | `core/sdd-dependency-graph.md`; "Contexto mínimo requerido" en skills `sdd-*` |
| **C** Compact mode | `core/templates/spec-compact-template.md`; sección en `core/workflow.md` |
| **D** Cost governance | Skill `sdd-cost-governance`; entrada `session_start` en `agent-skills/manifest.json`; sección governance en `workflow.md`; referencia desde `sdd-build-spec` |
| **F** Threshold doc | Sección "¿Esta iniciativa necesita spec?" en `core/workflow.md` |

**Excluye explícitamente:**

- Observabilidad de tokens por CLI (`sdd metrics tokens`) — eso es **SDD-013**
- Integración con APIs de pricing de proveedores
- Multi-agente con firewalls de contexto (fuera de alcance actual; ADR-001)
- Cambios en perfiles de stack distintos de lo necesario para instalar skills del kit

---

## Impacto técnico

| Pregunta                                                              | Respuesta |
| --------------------------------------------------------------------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)?                        | Sí — `workflow.md`, `sdd-dependency-graph.md`, `templates/spec-compact-template.md` |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)?     | No aplica — no cambia perfiles |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | Sí — `install-agents.py`, `sync-cursor-rules.py`, `agent-prompts/manifest.json`, `agent-skills/` |
| ¿Afecta `cli/` (comandos, librerías)?                                 | No aplica — CLI en SDD-013 |
| ¿Afecta `.github/workflows/` o reglas Cursor?                         | Indirecto — reglas `.mdc` regeneradas vía sync/install |
| ¿Requiere actualizar `README.md` o `INSTALL.md`?                      | Opcional — mencionar compact template y cost governance en docs de adopción si aplica en campaña |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)?                   | Sí — este spec + BACKLOG |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles.   | DR-1 (core agnóstico), DR-4 (agente ejecuta / humano aprueba), DR-5 (adopción incremental), DR-6 (docs en paths.sdd) |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR.          | No — aplica ADR-002 (harness); no nuevo ADR |

---

## Reglas de negocio

Aplica [`domain-rules.md`](../../../business/domain-rules.md):

- **DR-1:** Core agnóstico — governance y grafo no mencionan stacks concretos.
- **DR-4:** Circuit breaker y STOP no saltan gates Ready/merge; piden al humano.
- **DR-5:** Cambios backward-compatible; campos nuevos opcionales (`cacheZone`, `session_start`).
- **DR-6:** Spec y research solo bajo `paths.sdd`.

Fundamento empírico: research token-economics (Harness Effect arXiv:2607.06906; Tokenomics arXiv:2601.14470).

---

## Criterios de aceptación

**Happy path:**

- [x] `core/workflow.md` incluye: threshold "¿necesita spec?", modo compacto, governance de costo
- [x] Existen `core/sdd-dependency-graph.md` y `core/templates/spec-compact-template.md`
- [x] `bootstrap/agent-prompts/manifest.json` declara `cacheZone` (`stable` / `volatile`) en reglas core
- [x] `python bootstrap/sync-cursor-rules.py` genera reglas en orden two-zone (stable, then volatile) sin error
- [x] `install-agents.py` ordena reglas Cursor por `cacheZone` y filename determinista
- [x] Existe `bootstrap/agent-skills/sdd-cost-governance/SKILL.md` y está en `agent-skills/manifest.json` con `session_start: true`
- [x] Skills `sdd-draft-spec`, `sdd-build-spec`, `sdd-verify-implementation`, `sdd-open-pr`, `sdd-close-release`, `sdd-upgrade-kit` declaran contexto mínimo (no "lectura previa" genérica)
- [x] `sdd-build-spec` referencia governance de costo antes de implementar
- [x] `python -m compileall -q cli/` y `bootstrap/install-agents.py` / `sync-cursor-rules.py` en verde
- [x] `python bootstrap/install-agents.py install --agent cursor --target <fixture> --profile sdd-kit --no-prompt` instala `sdd-cost-governance` sin error
- [x] `python cli/sdd.py validate` y `validate-sdd` sin errores

**Error path:**

- [x] Skill `session_start` no aparece como trigger en el mapa de skills de adaptadores (omitida en `build_skills_map_table`)
- [x] Si falta `cacheZone` en una entrada del manifest, el instalador usa default `volatile` (no rompe)

---

## Diseño técnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `core/workflow.md` | Threshold SDD, compact mode, governance de costo |
| `core/sdd-dependency-graph.md` | Grafo de dependencias por skill |
| `core/templates/spec-compact-template.md` | Plantilla reducida |
| `bootstrap/install-agents.py` | Two-zone + omit map session_start |
| `bootstrap/sync-cursor-rules.py` | Two-zone + validación de orden |
| `bootstrap/agent-prompts/manifest.json` | `cacheZone` |
| `bootstrap/agent-skills/manifest.json` | `sdd-cost-governance` |
| `bootstrap/agent-skills/sdd-cost-governance/SKILL.md` | Circuit breaker |
| `bootstrap/agent-skills/sdd-*/SKILL.md` | Context scoping |

**Nota de estado:** La implementación de este alcance ya está en el working tree (sesión 2026-07-15). Este spec formaliza y fija criterios de verify/DoD para el cierre de campaña.

---

## Verificación técnica

```text
python -m compileall -q cli/
python bootstrap/sync-cursor-rules.py
python bootstrap/install-agents.py install --agent cursor --target <fixture> --profile sdd-kit --sdd-path .github/docs/sdd --kit-path . --no-prompt
python cli/sdd.py validate
# + validate-sdd.ps1 / validate-sdd.sh
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Circuit breaker demasiado agresivo (STOP prematuro) | Media | Medio | Límites documentados; humano puede autorizizar continuar |
| Compact mode usado en specs que requieren plantilla completa | Baja | Medio | Criterios explícitos en workflow.md |
| Two-zone no reduce costo real en Cursor (cache opaco) | Media | Bajo | Aún garantiza orden determinista; beneficio medible en SDD-013 |

**Rollback:** revertir commits de governance; skills y workflow vuelven a lectura previa genérica (SDD-006 baseline).

---

## Notas post-implementación

- Research fuente: `.github/docs/sdd/research/2026-07-15-token-economics-sdd-harness.md` §§6–8
- Siguiente: SDD-013 (observabilidad de tokens en CLI)
- **2026-07-15:** Alcance A–F verificado (compileall, sync two-zone, install fixture con `sdd-cost-governance`, `sdd validate` + `validate-sdd` OK). Estado → `In Build`.
- **2026-07-15 (build-spec):** Gap corregido — `sdd-build-spec` y `sdd-verify-implementation` en bootstrap recuperaron context scoping + referencia a cost governance (se habían perdido tras SDD-008). Verify OK.
- **2026-07-15 (smoke manual):** Exitoso — humano confirmó workflow (threshold / compact / governance), `spec-compact-template.md` y skill `sdd-cost-governance`.
