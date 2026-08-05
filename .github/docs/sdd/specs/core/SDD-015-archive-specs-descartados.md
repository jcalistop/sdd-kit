# Spec — Archivar specs en estado Descartado

---

## Cabecera

| Campo                 | Valor                        |
| --------------------- | ---------------------------- |
| **ID**                | `SDD-015`                    |
| **Dominio**           | `core`                       |
| **Tipo**              | `refactor` + `documentation` |
| **Fecha**             | 2026-08-05                   |
| **Estado**            | `In Build`                   |
| **Versión objetivo**  | `v1.3.1`                     |
| **Owner**             | José Luis Calisto Peñafiel   |
| **Prioridad**         | `P2`                         |
| **ADRs relacionados** | —                            |
| **Dependencias**      | —                            |

> **Nota de ID:** un intento previo numeró este alcance como SDD-007 sobre un `main` desfasado; en `dev` ese ID es safe-git (Released v1.3.0). El ID canónico es **SDD-015**.

---

## Problema y objetivo

**Problema:**

El ciclo SDD trata `archive/` como exclusivo de specs **Released**. Los validadores (`validate-sdd.ps1` / `.sh`) fallan si un `.md` en `archive/` no está en la sección Released del BACKLOG. Las reglas de agente prohíben explícitamente «specs en `archive/` con estado distinto de `Released`».

En la práctica, iniciativas **Descartadas** (obsoletas, supersedidas o abandonadas tras implementación parcial) quedan en `specs/<dominio>/` para no romper el validador. Eso mezcla trabajo vivo con histórico cerrado y confunde a humanos y agentes.

Además, `workflow.md` dice que Descartado es «solo en BACKLOG (no en cabecera)», lo que impide cerrar documentalmente el archivo del spec. El término informal **Deprecated** aparece en instancias consumidoras sin contrato en el kit.

**Objetivo:**

1. Definir **`Descartado`** como estado terminal de cabecera (además de fila en BACKLOG).
2. Permitir `git mv` del `.md` completo a `archive/<YYYY>/<dominio>/` cuando el spec está Descartado — **sin stub** en `specs/`.
3. Actualizar validadores, workflow, plantillas y prompts de agente para que `archive/` acepte **Released ∪ Descartado**.
4. Documentar migración: dejar de usar `Deprecated` en cabecera; unificar a `Descartado`.

---

## Alcance

### Incluye

**Contrato metodológico (`core/`)**

- Actualizar `core/workflow.md`: Descartado terminal; `specs/` solo estados activos; `archive/` = Released o Descartado; sin stub tras `git mv`.
- Plantilla `spec-template.md` y `BACKLOG-template.md`.
- Nota breve en `core/concepts.md` si aplica.

**Validación (`bootstrap/`)**

- `validate-sdd.ps1` / `.sh` (API por componente SDD-010): archive + Released|Descartado OK; specs + Descartado ERROR; cabecera terminal en specs ERROR.

**Agentes**

- `bootstrap/agent-prompts/sdd-agent-workflow.md` (+ sync cursor-rules): antipatrón archive solo Released o Descartado.

**CLI**

- `cli/lib/backlog.py`: parseo Descartado con ID `SDD-NNN` y columnas alineadas a la plantilla.

**Release producto**

- `docs/releases/CHANGELOG.md` + `v1.3.1.md` + nota en `upgrade-guide.md`.

### Excluye explícitamente

- Migrar specs de consumidores (p. ej. Centinela SDD-047 / SDD-107).
- Cambiar el grafo hacia Released.
- ADR.
- Suites pytest de la CLI.
- Reabrir SDD-007 safe-git (ya Released en v1.3.0).

---

## Impacto técnico

| Pregunta | Respuesta |
| -------- | --------- |
| ¿Afecta `core/`? | Sí — workflow, plantillas, concepts, upgrade-guide |
| ¿Afecta perfiles? | No aplica |
| ¿Afecta `bootstrap/`? | Sí — validate-sdd, agent-prompts, cursor-rules |
| ¿Afecta `cli/`? | Parcial — backlog.py |
| ¿Afecta workflows/reglas Cursor? | Sí — sync desde agent-prompts |
| ¿README/INSTALL? | Parcial — release notes |
| ¿Instancia SDD del kit? | Sí — BACKLOG, spec, next_sdd |
| ¿domain-rules? | Principios 1, 4, 6, 7 |
| ¿ADR? | No |

---

## Reglas de negocio

Desde `.github/docs/business/domain-rules.md`: #1 core agnóstico; #4 agente/humano; #6 paths.sdd; #7 producto/proceso.

---

## Criterios de aceptación

**Happy path:**

- [x] Fixture archive + BACKLOG Descartado → validate exit 0
- [x] archive + Released sin regresión
- [x] workflow + plantilla documentan Descartado en archive
- [x] Antipatrón de agente actualizado
- [x] CHANGELOG / v1.3.1 + upgrade-guide
- [x] Política sin stub

**Error path:**

- [x] archive + Draft → error
- [x] specs + Descartado → error
- [x] specs + cabecera Descartado → error

---

## Diseño técnico

Lógica validate:

```
si archivo en archive/:
  BACKLOG ∈ {Released, Descartado} → OK
  else → error
si archivo en specs/:
  BACKLOG ∈ {Released, Descartado} → error
  cabecera ∈ {Released, Descartado} → error
  BACKLOG ∈ activos → OK
si BACKLOG Descartado sin archivo → OK
```

---

## Verificación técnica

```powershell
python -m compileall -q cli/
python cli/sdd.py validate
python bootstrap/sync-cursor-rules.py
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Consumidores con Descartado en `specs/` fallan validate | Alta | Medio | v1.3.1 + upgrade-guide |
| Confusión con SDD-007 safe-git | Media | Bajo | Nota de ID + numeración SDD-015 |

**Rollback:** revertir commit del kit; consumidores revierten submodule.

---

## Notas post-implementación

- Tras Released de SDD-015, consumidores pueden archivar specs Descartados.
- Unificar lenguaje: sección «Descartado / en pausa» + enlace a `archive/…`.
