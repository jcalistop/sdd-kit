# SDD-027 — Metodología research (guía + plantilla de nota)

> Copiar desde plantilla core. Al cerrar: `git mv` a `archive/<YYYY>/docs/`.

---

## Cabecera

| Campo                 | Valor                  |
| --------------------- | ---------------------- |
| **ID**                | `SDD-027`              |
| **Dominio**           | `docs`                 |
| **Tipo**              | `documentation`        |
| **Fecha**             | 2026-09-12             |
| **Estado**            | `In Build`             |
| **Versión objetivo**  | patch (desde `v1.5.0`) |
| **Owner**             | mantenedor kit         |
| **Prioridad**         | `P2`                   |
| **ADRs relacionados** | —                      |
| **Dependencias**      | Pareja conceptual de SDD-026 (audits); frontera ya en índice / `audits/README.md` |

---

## Problema y objetivo

**Problema:**

Las notas bajo `research/` existen y el índice (SDD-021) distingue audits vs research, pero no hay **metodología canónica** ni plantilla de nota. Los informes de julio son ensayos largos improvisados; quien inicia una investigación corta no sabe cuándo usar research vs audit vs ADR vs spec, ni el naming/cierre. SDD-026 cubre audits y deja research como ítem aparte.

**Objetivo:**

Publicar una **guía completa** reutilizable bajo `research/` más **una plantilla de nota corta** (sin forzar ensayos largos). Enlazar desde el índice de `paths.sdd` y añadir fila en `core/concepts.md`. Opcional: enlace de reuso desde una nota histórica (sin migrar formato).

---

## Alcance

**Incluye:**

1. **Metodología (guía)** en `.github/docs/sdd/research/README.md`:
   - Glosario: **metodología** (guía reutilizable) vs **nota** (artefacto de *esta* investigación).
   - Tabla **research vs audits** alineada al [README](../../README.md) (research no es cola operativa).
   - **Cuándo** research vs audit vs ADR vs spec SDD.
   - **Default:** una nota por investigación (`research/YYYY-MM-DD-slug.md`); sin par plan/informe.
   - Ensayos largos = **opcional**; la plantilla no los exige.
   - Implicaciones: puede orientar ADR o fila Discovery; **no** inventar `SDD-NNN` sin reflejarlo en BACKLOG.
   - Checklist de cierre: nota usable (estado Listo) → actualizar índice research en README → merge a rama de desarrollo. Sin contrato stub≠SoT de audits (no es corrida de evaluación).
   - No forzar `research/` en consumidores; plantillas agnósticas al stack.

2. **Plantilla** `core/templates/research-nota-template.md` — cabecera (fecha, slug, estado `Borrador`/`Listo`, pregunta) + secciones cortas:
   - Pregunta / motivación
   - Hallazgos (bullets)
   - Implicaciones (ADR / Discovery / nada / link si aplica)
   - Fuentes
   - (Opcional) mapa al kit — sin secciones de ensayo profundo

3. **Índice:** [`.github/docs/sdd/README.md`](../../README.md) — fila research enlaza metodología + plantilla (simetría con audits).

4. Una fila en listado de plantillas de [`core/concepts.md`](../../../../core/concepts.md) (sin reescribir concepts).

5. **Reuso opcional:** enlace corto desde una nota histórica en `research/2026-07-15-*` apuntando a la metodología (sin migrar cuerpo).

**Excluye explícitamente:**

- Migrar las 3 notas `research/2026-07-15-*` al formato nuevo.
- Segundo artefacto «ensayo» o plan hermano.
- Skill/prompt nuevo, CLI, `validate-sdd` sobre research, CI.
- Cambiar metodología de audits (solo simetría en índice).
- ADR nuevo; forzar carpeta `research/` en consumidores.
- Ampliar [`core/releases/RUNBOOK.md`](../../../../core/releases/RUNBOOK.md).

---

## Impacto técnico

Perfil: [`profiles/sdd-kit/spec-impact.md`](../../../../profiles/sdd-kit/spec-impact.md).

| Pregunta | Respuesta |
| -------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)? | Sí — `research-nota-template.md`; fila en concepts |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)? | No aplica |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | No aplica |
| ¿Afecta `cli/` (comandos, librerías)? | No aplica |
| ¿Afecta `.github/workflows/` o reglas Cursor? | No aplica |
| ¿Requiere actualizar `README.md` o `INSTALL.md`? | No aplica (raíz kit); sí README de `paths.sdd` |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)? | Sí — este spec + metodología research + índice |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles. | No cambia el texto; aplica DR-1, DR-6 |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR. | No |

---

## Reglas de negocio

Aplica [`.github/docs/business/domain-rules.md`](../../business/domain-rules.md):

- **DR-1** — plantilla en `core/` agnóstica al stack.
- **DR-6** — metodología y notas en `paths.sdd` (`research/`).

Particularidad: guía de mantenedores; plantilla disponible en el kit sin obligar `research/` a consumidores. DR-7 no es foco (no hay stub/tag de corrida como en audits).

---

## Criterios de aceptación

**Happy path:**

- [x] Existe `.github/docs/sdd/research/README.md` con: glosario; research vs audits; cuándo research vs audit vs ADR vs spec; default = una nota `YYYY-MM-DD-slug`; ensayos largos opcionales; implicaciones sin inventar SDD-NNN; checklist de cierre + índice.
- [x] El índice [`.github/docs/sdd/README.md`](../../README.md) enlaza metodología research + plantilla `research-nota`.
- [x] Existe `core/templates/research-nota-template.md` (cabecera + pregunta/hallazgos/implicaciones/fuentes; mapa al kit opcional; sin forzar ensayo largo).
- [x] Una fila en la tabla de plantillas de `core/concepts.md`.
- [x] Un mantenedor puede iniciar una investigación corta copiando solo la plantilla de nota.
- [x] `python cli/sdd.py validate` en verde.

**Error path:**

- [x] Documentado: research no es tablero operativo ni sustituye spec/ADR.
- [x] La metodología no exige migrar notas históricas ni par plan/informe.
- [x] Plantilla sin stacks concretos (DR-1).

---

## Congelado para implementación _(opcional)_

Omitido — alcance y paths cerrados; riesgo de LLM bajo.

---

## Cambio de BD

No aplica.

---

## Diseño técnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `.github/docs/sdd/research/README.md` | Guía completa (punto de entrada para agentes) |
| `core/templates/research-nota-template.md` | Plantilla corta default |
| `.github/docs/sdd/README.md` | Índice: enlaces metodología + plantilla |
| `core/concepts.md` | 1 fila en tabla plantillas |
| `research/2026-07-15-*.md` (opcional, una) | Enlace reuso a metodología |

**Notas de diseño:**

- Vocabulario: **metodología/guía** ≠ **nota** (instancia). No “runbook”.
- Simetría documental con SDD-026; sin plan hermano ni stub≠SoT.
- Congelado: omitido.

---

## Verificación técnica

```bash
python cli/sdd.py validate
# Al implementar: research/README.md + research-nota-template + enlaces índice + fila concepts
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Confundir research con audit o Discovery | Media | Medio | Tabla cuándo-usar en la guía + índice |
| Mantenedores siguen escribiendo solo ensayos largos | Media | Bajo | Plantilla corta default; ensayo marcado opcional |
| Inventar SDD-NNN desde una nota | Baja | Medio | Regla explícita: BACKLOG primero |

**Rollback:** revertir metodología, plantilla y diffs de índice/concepts/reuso.

---

## Notas post-implementación

- Origen: fila Discovery «Metodología research» (pareja SDD-026); índice SDD-021.
- Ejemplos históricos (no migrar): `research/2026-07-15-harness-engineering.md` y hermanas.
- **2026-09-12 (In Build):** `research/README.md` + `research-nota-template.md` + índice + fila concepts + reuso en harness-engineering; puntero en `audits/README.md`. Renombre `METODOLOGIA.md` → `README.md` (audits + research) para descubrimiento por agentes.
- **2026-09-12 (SDD-028):** SoT metodología → [`core/guides/research.md`](../../../../core/guides/research.md); `research/README.md` queda stub de instancia.
- **Smoke manual (2026-09-12):** humano confirmó OK — guía research usable; plantilla corta sin forzar ensayo; enlaces índice (pre-SDD-028 y post stubs).
