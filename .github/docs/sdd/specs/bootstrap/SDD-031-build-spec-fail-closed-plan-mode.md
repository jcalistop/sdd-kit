# SDD-031 — build-spec fail-closed: Plan mode / «te guío»

---

## Cabecera

| Campo                 | Valor              |
| --------------------- | ------------------ |
| **ID**                | `SDD-031`          |
| **Dominio**           | `bootstrap`        |
| **Tipo**              | `feature`          |
| **Fecha**             | 2026-09-13         |
| **Estado**            | `In Build`         |
| **Versión objetivo**  | `v1.6.0` |
| **Owner**             | mantenedor         |
| **Prioridad**         | `P2`               |
| **ADRs relacionados** | —                  |
| **Dependencias**      | — (independiente de SDD-030; mismo origen dogfood) |

---

## Problema y objetivo

**Problema:**

En dogfood externo (gap #6), el agente intentó cerrar solo un ciclo documental throwaway; el humano frenó con Plan mode / «te guío». Planes «ciclo completo» o invocaciones de build-spec en ese contexto pueden pasar Draft→Ready→In Build **sin frase humana explícita de aprobación**, aunque el workflow ya diga que el humano aprueba Ready.

**Objetivo:**

Hacer **fail-closed** el skill/prompt `build-spec`: si hay señal de Plan mode o guía humana activa («te guío» o equivalente), **no** mutar cabecera ni BACKLOG a Ready/In Build hasta una frase de aprobación explícita (`apruebo SDD-NNN…`, `build-spec`, equivalente). Fuera de esas señales, el contrato actual no cambia.

**Origen:** [informe dogfood gap #6](../../audits/20260906-dogfood-consumidor-externo-informe.md). Alcance acordado: **opción A** (skill + prompt; sin always-on).

---

## Alcance

**Incluye:**

- Gate fail-closed al inicio de [`bootstrap/agent-skills/sdd-build-spec/SKILL.md`](../../../../bootstrap/agent-skills/sdd-build-spec/SKILL.md): detectar señales → parar → pedir frase → solo entonces Draft→Ready→In Build.
- Mismo criterio en [`core/prompts/workflow/build-spec.md`](../../../../core/prompts/workflow/build-spec.md).
- Nota breve en [`bootstrap/agent-skills/sdd-build-spec/reference.md`](../../../../bootstrap/agent-skills/sdd-build-spec/reference.md): ejemplos de frases válidas / no válidas bajo esas señales.
- Tras merge: consumidores reinstalan skills (contrato install existente; **sin** cambios a `install-agents.py`).

**Excluye explícitamente:**

- Cambios a `sdd-agent-workflow` always-on (opción B).
- Reescritura de `core/workflow.md` / `core/guides/operations.md` (opción C).
- Sensor CI / `validate-sdd` que detecte Plan mode.
- Adaptadores Claude / Codex / Copilot.
- Cambiar el contrato general «frase basta» **fuera** de Plan mode / «te guío».
- Gap dogfood #7 / [SDD-030](SDD-030-skills-stack-profile-install.md).

---

## Impacto técnico

> Perfil: `sdd-kit`. Tabla según `profiles/sdd-kit/spec-impact.md`.

| Pregunta                                                              | Respuesta |
| --------------------------------------------------------------------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)?                        | Sí (menor) — solo `core/prompts/workflow/build-spec.md`; no `workflow.md` ni operations |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)?     | No aplica — sin checklist nueva |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | Sí — plantilla skill `sdd-build-spec` (+ `reference.md`); sin `install-agents` |
| ¿Afecta `cli/` (comandos, librerías)?                                 | No aplica — sin cambios CLI |
| ¿Afecta `.github/workflows/` o reglas Cursor?                         | No aplica — skill on-demand; **sin** reglas always-on nuevas |
| ¿Requiere actualizar `README.md` o `INSTALL.md`?                      | No aplica — basta skill + prompt |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)?                   | Sí (proceso) — este spec + BACKLOG + `ids.next_sdd` |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles.   | Cumple DR-4 (humano aprueba Ready). Sin cambio al archivo domain-rules |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR.          | No — refuerzo fail-closed en guía on-demand; no ADR |

---

## Reglas de negocio

Aplica [`.github/docs/business/domain-rules.md`](../../../business/domain-rules.md):

- **DR-4** — El agente ejecuta; el humano aprueba en Ready (spec) y merge (PR). Este SDD endurece ese gate cuando el contexto es Plan mode / guía humana.
- **Bootstrap/CLI** — Sin dependencias externas nuevas; solo markdown de skill/prompt.
- **DR-1** — Core: solo el prompt de workflow `build-spec`; sin acoplar stacks.

Particularidad: es **guía** (feedforward) en skill/prompt, no un sensor CI.

---

## Criterios de aceptación

**Happy path:**

- [x] Con señal Plan mode o «te guío» (o equivalente de guía humana activa) y **frase explícita** de aprobación → build-spec puede pasar Draft→Ready→In Build (cabecera + BACKLOG).
- [x] Sin esas señales → comportamiento actual: frase de aprobación o invocación `build-spec` basta (sin exigir ritual extra).
- [x] `SKILL.md` y `core/prompts/workflow/build-spec.md` documentan el gate fail-closed con las mismas señales y la misma acción (parar + pedir frase).
- [x] `reference.md` del skill lista al menos 2 ejemplos de frase válida y 2 de frase **no** suficiente bajo esas señales (p. ej. «sigue», «implementa el plan», «ok» ambiguo sin nombrar aprobación Ready/build).
- [x] `python ./cli/sdd.py validate` sin errores tras cambios de instancia/docs tocados.

**Error path:**

- [x] Con señal Plan mode / «te guío» y **sin** frase de aprobación → el agente **no** actualiza cabecera ni BACKLOG a Ready ni In Build; pide frase y espera.
- [x] Diff que modifique `sdd-agent-workflow` always-on, `workflow.md`/`operations` como alcance principal, o añada sensor CI de Plan mode → fuera de alcance; rechazar en review.

---

## Congelado para implementación

> Obligatorio para LLM de bajo contexto. **Prohibido explorar** fuera de esta lista. Lectura máx. **N = 5** paths de esta lista (+ este spec + `domain-rules.md`).

| Campo | Valor |
| ----- | ----- |
| **Decisión única** | Fail-closed solo en skill + prompt `build-spec` (opción A). Señales: Plan mode / «te guío» / guía humana activa. Acción: no mutar Ready/In Build hasta frase explícita. Sin always-on ni CI. |
| **API / contrato** | Guía textual en skill/prompt: si señal ∧ ¬frase_aprobación → STOP; si señal ∧ frase_aprobación → Ready→In Build; si ¬señal → contrato actual. Frases válidas incluyen `apruebo SDD-NNN…`, `build-spec`, «apruebo para implementar». |
| **Paths de test** | No aplica automatizado — verificación por review del wording + checklist humano (criterios). Sin pytest nuevo. |
| **Lista de lectura** | Ver lista cerrada abajo |
| **Lectura máx. N** | `5` |
| **Prohibido explorar** | Sí — fuera de la lista: no `grep` / `Glob` / `Read` por curiosidad |

**Lista de lectura (cerrada):**

1. `bootstrap/agent-skills/sdd-build-spec/SKILL.md`
2. `bootstrap/agent-skills/sdd-build-spec/reference.md`
3. `core/prompts/workflow/build-spec.md`
4. `.github/docs/sdd/audits/20260906-dogfood-consumidor-externo-informe.md` (solo fila gap #6)
5. `.github/docs/business/domain-rules.md` (DR-4)

---

## Diseño técnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `bootstrap/agent-skills/sdd-build-spec/SKILL.md` | Sección gate fail-closed antes de «A. Implementación» |
| `bootstrap/agent-skills/sdd-build-spec/reference.md` | Ejemplos frases válidas / no válidas |
| `core/prompts/workflow/build-spec.md` | Mismo gate en «Cuándo usarlo» / instrucciones |

**Señales (mínimo):**

| Señal | Cómo reconocerla (guía) |
| ----- | ----------------------- |
| Plan mode | Sistema/UI indica Plan mode, o el humano está solo planificando sin frase de build |
| «te guío» | Frase humana equivalente: te guío, guiame, vamos paso a paso, no implementes aún |
| Guía humana activa | Humano pidió iterar el plan / Draft sin aprobar Ready |

**No es señal por sí sola:** adjuntar el skill, decir «revisa el spec», o estar en Agent mode sin las señales de arriba.

---

## Verificación técnica

- Review del diff skill + prompt + reference contra criterios.
- `python ./cli/sdd.py validate`
- Sin quality gates de código nuevos (solo markdown).

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Falso positivo: pide frase de más en sesiones normales | Media | Bajo (fricción) | Limitar señales a Plan mode / «te guío»; fuera de eso, contrato actual |
| Agente ignora skill y usa solo always-on | Media | Medio (gap parcialmente abierto) | Aceptado en opción A; opción B queda fuera; documentar en riesgos |
| Wording ambiguo de «frase válida» | Baja | Medio | Ejemplos concretos en `reference.md` |

**Rollback:** revertir los tres archivos markdown; reinstalar skills en consumidores.

---

## Notas post-implementación

- Tras Released: consumidores con skills managed deben re-correr `install-agents` (o upgrade) para recibir el skill actualizado.
- No exigir sync de cursor-rules: este SDD no toca `.mdc` always-on.
