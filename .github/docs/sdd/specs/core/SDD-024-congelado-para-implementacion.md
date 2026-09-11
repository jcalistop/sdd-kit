# SDD-024 — Sección opcional «Congelado para implementación»

---

## Cabecera

| Campo                 | Valor              |
| --------------------- | ------------------ |
| **ID**                | `SDD-024`          |
| **Dominio**           | `core`             |
| **Tipo**              | `documentation`    |
| **Fecha**             | 2026-09-11         |
| **Estado**            | `In Build`         |
| **Versión objetivo**  | patch (desde `v1.5.0`) |
| **Owner**             | mantenedor         |
| **Prioridad**         | `P1`               |
| **ADRs relacionados** | —                  |
| **Dependencias**      | —                  |

---

## Problema y objetivo

**Problema:**

En dogfood externo (gap #3), un Draft pasó DoR humano pero dejó decisiones abiertas (tecnología alternativa, API vaga, tests `...`). Un LLM de bajo contexto improvisó o exploró el repo sin límite. Hubo que enmendar el Draft a mano congelando decisión única, API, paths de test y lista de lectura. Hoy plantillas y DoR no ofrecen un bloque opcional para ese contrato; en In Build el agente explora a criterio propio.

**Objetivo:**

Agregar la sección opcional **«Congelado para implementación»** en plantilla(s), DoR y skill `draft-spec`, para que un Draft pueda fijar decisión única, API, paths de test, lista de lectura + **N** (sin default de plantilla) y «prohibido explorar». Si la sección no se usa, no se impone tope de lectura.

---

## Alcance

**Incluye:**

- Sección opcional en `core/templates/spec-template.md` (y `spec-compact-template.md` si cabe sin inflar el modo compacto)
- Ítem de recuerdo en DoR (`sdd-workflow-reference`: fuente bootstrap → sync a `.cursor/rules/`)
- Instrucciones en skill `sdd-draft-spec` (bootstrap + paridad instancia vía install/sync del kit)
- Mención breve en prompts/workflow de Draft si hace falta coherencia
- Documentar que, **si el bloque existe**, In Build / `build-spec` debe respetarlo (guía; no nuevo sensor CI)

**Excluye explícitamente:**

- Hacer la sección obligatoria (siempre opcional; DoR solo recuerda usarla con decisiones abiertas / LLM de bajo contexto)
- Default numérico de N en plantilla (N y lista los declara el humano al usar la sección)
- Endurecer `validate-sdd` para exigir o parsear el bloque
- Cambios a verify/quality gates de perfiles (gap #4 es otro ítem)
- Plantilla `spec-simple-template.md` salvo nota mínima no técnica (no forzar API/tests)

---

## Impacto técnico

> Perfil: `sdd-kit`. Tabla según `profiles/sdd-kit/spec-impact.md`.

| Pregunta                                                              | Respuesta |
| --------------------------------------------------------------------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)?                        | Sí — plantilla(s) de spec; posible nota en prompt-catalog / workflow core |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)?     | No aplica — cambio transversal de metodología, no de stack |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | Sí — `sdd-workflow-reference`, skill `sdd-draft-spec`; sync rules/skills |
| ¿Afecta `cli/` (comandos, librerías)?                                 | No aplica — sin cambios a `validate-sdd` ni comandos |
| ¿Afecta `.github/workflows/` o reglas Cursor?                         | Sí — regla on-demand DoR tras sync desde bootstrap |
| ¿Requiere actualizar `README.md` o `INSTALL.md`?                      | No aplica — cambio interno de plantilla/DoR/skill |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)?                   | Solo este ciclo (BACKLOG/spec); consumidores reciben el cambio en próximo patch del kit |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles.   | No aplica — no cambia invariantes; las respeta (#1, #4, #6) |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR.          | No — guía documental opcional; sin ADR |

---

## Reglas de negocio

> Aplica [domain-rules.md](../../../business/domain-rules.md) principios #1 (core agnóstico al stack), #4 (agente ejecuta; humano aprueba), #6 (documentación SDD en `paths.sdd`).

Particularidad: el bloque es **guía** (feedforward) opcional; no es sensor CI ni reemplaza criterios de aceptación.

---

## Criterios de aceptación

**Happy path:**

- [x] `spec-template.md` incluye sección opcional «Congelado para implementación» con placeholders para: decisión única, API/contrato, paths de test, lista de lectura, **N** (sin valor por defecto), y «prohibido explorar»
- [x] DoR recuerda usar el bloque cuando hay decisiones abiertas o riesgo de LLM de bajo contexto (sin volverlo obligatorio)
- [x] Skill `sdd-draft-spec` indica cuándo ofrecer/completar el bloque y que N + lista son obligatorios **solo si** se incluye la sección
- [x] Si un spec incluye el bloque, la guía de In Build / build-spec indica respetar lista + N y no explorar fuera
- [x] `python ./cli/sdd.py validate` sin errores tras los cambios de producto
- [x] Core sigue agnóstico al stack (sin ejemplos acoplados a un framework concreto en plantillas core)

**Error path:**

- [x] Si un Draft usa la sección sin N o sin lista de paths → DoR/skill lo marca incompleto antes de pedir Ready (no pasa validate-sdd; es checklist guía)
- [x] Si alguien interpreta el bloque como obligatorio → docs dejan claro que es opcional; corrección documental

---

## Diseño técnico

**Contenido típico del bloque (en plantilla):**

| Campo | Rol |
| ----- | --- |
| Decisión única | Tecnología/enfoque sin alternativas abiertas |
| API / contrato | Firma o contrato concreto a implementar |
| Paths de test | Archivos o filtros de test acordados |
| Lista de lectura | Paths que el agente **sí** puede abrir en In Build |
| Lectura máx. N | Entero declarado por el humano (sin default de plantilla) |
| Prohibido explorar | Fuera de la lista: no `grep`/`Glob`/`Read` por curiosidad |

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `core/templates/spec-template.md` | Agregar sección opcional con placeholders |
| `core/templates/spec-compact-template.md` | Incluir solo si no rompe el modo compacto; si no, omitir |
| `bootstrap/agent-prompts/sdd-workflow-reference.md` | Ítem DoR de recuerdo |
| `bootstrap/agent-skills/sdd-draft-spec/SKILL.md` (+ reference si aplica) | Cuándo ofrecer el bloque; N sin default |
| `.cursor/rules/sdd-workflow-reference.mdc` | Paridad vía sync |
| `.cursor/skills/sdd-draft-spec/` | Paridad vía install/sync del kit |
| Skills/prompts build (mención mínima) | Respetar bloque si existe |

---

## Verificación técnica

- `python ./cli/sdd.py validate`
- Quality gates perfil `sdd-kit` tocados por el cambio (compile/pytest solo si se toca `cli/`; aquí no aplica salvo validate)
- Tras sync: revisar que DoR y skill instalados mencionan el bloque

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Agentes ignoran el bloque aunque exista | Media | Medio | Mención explícita en draft-spec + build-spec; DoR de recuerdo |
| Humanos dejan N vacío al usar la sección | Media | Bajo | Checklist DoR/skill: incompleto sin N + lista |
| Sobre-restringir exploración en specs grandes | Baja | Medio | Sección opcional; N lo elige el humano por spec |
| Confundir con obligatoriedad / validate-sdd | Baja | Bajo | Exclusiones y error path documentados |

**Rollback:** revertir commits de plantilla/DoR/skill; consumidores recuperan comportamiento previo en próximo upgrade.

---

## Notas post-implementación

- Origen: [audits/20260906-dogfood-consumidor-externo-informe.md](../../audits/20260906-dogfood-consumidor-externo-informe.md) gap #3
- SemVer kit: **patch** (docs + skill draft; sin API de CLI nueva)
