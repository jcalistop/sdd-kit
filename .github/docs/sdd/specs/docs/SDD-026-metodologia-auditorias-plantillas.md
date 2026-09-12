# SDD-026 — Metodología de auditorías (guía + registro; plan solo si grande)

> Copiar desde plantilla core. Al cerrar: `git mv` a `archive/<YYYY>/docs/`.

---

## Cabecera

| Campo                 | Valor                    |
| --------------------- | ------------------------ |
| **ID**                | `SDD-026`                |
| **Dominio**           | `docs`                   |
| **Tipo**              | `documentation`          |
| **Fecha**             | 2026-09-11               |
| **Estado**            | `In Build`               |
| **Versión objetivo**  | patch (desde `v1.5.0`)   |
| **Owner**             | mantenedor kit           |
| **Prioridad**         | `P2`                     |
| **ADRs relacionados** | —                        |
| **Dependencias**      | — (absorbe dogfood gap #5; merge Centinela ya en `dev` / `v1.5.0`) |

---

## Problema y objetivo

**Problema:**

Las auditorías del kit se ejecutan copiando el último par plan+informe e improvisando. No hay metodología canónica ni plantilla de registro. El par dual es costoso en corridas cortas (p. ej. dogfood) y además facilitó el fallo Centinela: stubs «Pendiente» en el tag vs evidencia real post-tag. El merge de Centinela **ya está hecho**; falta un método reutilizable con el menor número de artefactos por corrida.

**Objetivo:**

Publicar una **metodología corta** (guía reutilizable, no plan de una corrida) más **una plantilla de registro** por defecto (alcance + resultados + gaps + cierre). **Plan separado solo** en auditorías grandes o cuando el alcance deba congelarse antes de ejecutar. Incluir contrato stub ≠ SoT y checklist de merge. Enlazar desde el índice de `paths.sdd` y desde el audit dogfood Centinela (reuso).

---

## Alcance

**Incluye:**

1. **Metodología (guía)** bajo `.github/docs/sdd/audits/` (p. ej. `audits/README.md` o `audits/METODOLOGIA.md`) — **no** llamarla runbook de release ni “plan” de corrida:
   - **Audits vs research** (declarar en la guía y alinear con el índice): audit = evaluar estado y gaps accionables → BACKLOG; research = explorar ideas/marcos, no es tablero ni spec (metodología research = otro ítem Discovery).
   - Cuándo auditoría vs spec SDD (operativa; gaps → Discovery/SDD).
   - **Default:** un **registro** por corrida (un archivo) con secciones alcance/método + resultados + gaps + cierre.
   - **Excepción:** **plan separado** solo si la auditoría es **grande** o el alcance requiere freeze/aprobación humana previa; entonces plan (alcance) + registro/informe (resultados), enlazados.
   - Criterio orientativo “grande”: varios días, muchos ámbitos, o varios ejecutores; dogfood típico = **no** grande → solo registro.
   - Anexo/sección **dogfood consumidor** (baseline → ciclo mínimo → upgrade → evidencia), sin reescribir el cierre histórico Centinela.
   - **Stub ≠ SoT:** stub en tag = borrador pre-corrida; registro (y plan, si existe) **mergeados** = SoT; si chocan, gana el registro Ejecutado en `main`/`dev`.
   - **Checklist de cierre:** registro completo (estado Ejecutado) → PR a `dev` → a `main` a más tardar en el próximo patch dual-release → actualizar índice; gaps a Discovery/SDD. Si hubo plan separado, mergear ambos.

2. **Plantillas** en `core/templates/`:
   - `audit-registro-template.md` — **default**: cabecera, alcance/exclusiones, método/pasos, resultados OK/FAIL, gaps (id, hallazgo, acción, SemVer, prioridad), cierre.
   - `audit-plan-template.md` — **solo corridas grandes**: alcance congelado, exclusiones, prerrequisitos, método; enlace al registro/informe hermano.

3. **Índice:** [`.github/docs/sdd/README.md`](../../README.md) → metodología + plantillas.
4. **Reuso:** nota en [audits/20260906-dogfood-consumidor-externo.md](../../audits/20260906-dogfood-consumidor-externo.md) (y/o informe) apuntando a metodología/plantillas.
5. Una fila en listado de plantillas de [`core/concepts.md`](../../../../core/concepts.md) si ya hay tabla (sin reescribir concepts).

**Excluye explícitamente:**

- Re-merge / retag Centinela o `v1.4.1`.
- Migrar audits históricos al formato nuevo (solo enlace de reuso).
- Exigir plan+informe dual como regla general (queda como excepción “grande”).
- Skill/prompt nuevo, CLI, `validate-sdd` sobre audits, CI.
- Gaps dogfood #6 y #7.
- Ampliar [`core/releases/RUNBOOK.md`](../../../../core/releases/RUNBOOK.md).
- ADR; forzar `audits/` en consumidores.
- Metodología/plantilla de **research/** (fila Discovery aparte; este SDD solo declara la frontera audits vs research).

---

## Impacto técnico

Perfil: [`profiles/sdd-kit/spec-impact.md`](../../../../profiles/sdd-kit/spec-impact.md).

| Pregunta | Respuesta |
| -------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)? | Sí — `audit-registro-template.md` + `audit-plan-template.md`; fila opcional en concepts |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)? | No aplica |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | No aplica |
| ¿Afecta `cli/` (comandos, librerías)? | No aplica |
| ¿Afecta `.github/workflows/` o reglas Cursor? | No aplica |
| ¿Requiere actualizar `README.md` o `INSTALL.md`? | No aplica (raíz kit); sí README de `paths.sdd` |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)? | Sí — este spec + metodología audits + índice + nota Centinela |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles. | No cambia el texto; aplica DR-1, DR-6, DR-7 |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR. | No |

---

## Reglas de negocio

Aplica [`.github/docs/business/domain-rules.md`](../../business/domain-rules.md):

- **DR-1** — plantillas en `core/` agnósticas al stack.
- **DR-6** — metodología y registros de corrida en `paths.sdd` (`audits/`).
- **DR-7** — checklist merge a `main` vía próximo patch dual-release.

Particularidad: guía de mantenedores; plantillas disponibles en el kit sin obligar `audits/` a consumidores.

---

## Criterios de aceptación

**Happy path:**

- [x] Existe metodología bajo `.github/docs/sdd/audits/` que declara: audits vs research; default = un registro; plan separado = solo grandes / freeze; stub ≠ SoT; checklist de cierre.
- [x] El índice [`.github/docs/sdd/README.md`](../../README.md) declara audits vs research y enlaza metodología/plantillas de audit.
- [x] Existen `core/templates/audit-registro-template.md` y `core/templates/audit-plan-template.md` (esta última marcada como opcional / solo grandes).
- [x] Un mantenedor inicia una corrida corta (tipo dogfood) con **solo** la plantilla de registro, sin inventar un plan hermano.
- [x] El audit dogfood Centinela enlaza la metodología (reuso).
- [x] `python cli/sdd.py validate` en verde.

**Error path:**

- [x] Documentado: stub del tag no gana frente a registro Ejecutado mergeado.
- [x] La metodología no exige retag/re-merge de Centinela ni plan+informe dual en corridas cortas.
- [x] Plantillas sin stacks concretos (DR-1).

---

## Cambio de BD

No aplica.

---

## Diseño técnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `.github/docs/sdd/audits/README.md` o `METODOLOGIA.md` | Guía: default registro; plan solo si grande; stub ≠ SoT; cierre |
| `core/templates/audit-registro-template.md` | Plantilla default |
| `core/templates/audit-plan-template.md` | Plantilla opcional (grandes) |
| `.github/docs/sdd/README.md` | Índice |
| `audits/20260906-dogfood-consumidor-externo.md` | Nota reuso |
| `core/concepts.md` (opcional) | 1–2 filas en tabla plantillas |

**Notas de diseño:**

- Vocabulario: **metodología/guía** (reutilizable) ≠ **plan** (instancia, solo grandes) ≠ **registro** (SoT de la corrida).
- No usar “runbook” como nombre principal (evitar choque con `core/releases/RUNBOOK.md`).
- Congelado: **omitido**.

---

## Verificación técnica

```bash
python cli/sdd.py validate
# Al implementar: metodología + audit-registro-template + audit-plan-template + enlaces índice
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Criterio “grande” ambiguo | Media | Bajo | Orientación en metodología + ejemplo dogfood = solo registro |
| Mantenedores siguen creando plan+informe por hábito | Media | Medio | Default explícito en guía e índice; plan template marcado opcional |
| Confundir metodología con plan de corrida | Media | Bajo | Nombres y glosario corto al inicio de la guía |
| Confundir con RUNBOOK de release | Baja | Bajo | No llamar runbook al artefacto principal |

**Rollback:** revertir metodología, plantillas y diffs de índice/nota.

---

## Notas post-implementación

- Origen gap #5: [informe dogfood](../../audits/20260906-dogfood-consumidor-externo-informe.md).
- Iteración 2026-09-12: default un registro; plan separado solo auditorías grandes; frontera audits vs research; research → Discovery aparte.
- **2026-09-12 (In Build):** `audits/METODOLOGIA.md` + plantillas registro/plan + índice + nota Centinela + filas en `core/concepts.md`.
- **Smoke manual (2026-09-12):** humano confirmó OK — metodología (default vs plan grande), plantilla registro suficiente para corrida corta, enlaces del índice README.
- Ejemplos de referencia (no migrar): `20260905-…` (grande / dual de facto) y `20260906-…` (corta / debería ser un registro en el modelo nuevo).
