# SDD-NNN — [Título descriptivo]

> **Modo compacto** — Este spec sigue el patrón documentado en `[referencia al patrón]`.
> Secciones estándar omitidas: checklist stack, impacto técnico detallado, diagramas, riesgos de rollback.
> Aplica reglas de negocio en `business/domain-rules.md`. Checklist stack según perfil `[nombre]`.
> Para secciones completas, ver [`spec-template.md`](spec-template.md).

---

## Cabecera

| Campo | Valor |
|-------|-------|
| **ID** | `SDD-NNN` |
| **Dominio** | `[dominio]` |
| **Tipo** | `[feature|bugfix|refactor|performance|documentation]` |
| **Fecha** | [YYYY-MM-DD] |
| **Estado** | `Draft` |
| **Versión objetivo** | vX.Y.Z |
| **Owner** | [equipo o persona] |
| **Prioridad** | `[P0|P1|P2|P3]` |

---

## Problema y objetivo

[1-2 párrafos. Solo lo específico de este spec. No repetir contexto del dominio ni reglas de negocio ya documentadas en `domain-rules.md`.]

---

## Alcance

- **Incluye:** [3-5 bullets concretos]
- **Excluye explícitamente:** [1-3 bullets]

---

## Criterios de aceptación

- [ ] [Criterio 1 — happy path]
- [ ] [Criterio 2 — happy path]
- [ ] [Criterio 3 — error path]
- [ ] Verify local OK: quality gates del perfil stack + `validate-sdd`
- [ ] Reglas de dominio (`business/domain-rules.md`) respetadas

---

## Dependencias

| ID | Estado | Relación |
|----|--------|----------|
| — | — | — |

---

## ADR relacionados

| ID | Fecha | Impacto |
|----|-------|---------|
| — | — | — |
