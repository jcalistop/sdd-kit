# SDD-018 — Higiene agentica: retirar `sdd-core.mdc` residual

> Copiar desde plantilla core. Al cerrar: `git mv` a `archive/<YYYY>/bootstrap/`.

---

## Cabecera

| Campo                 | Valor          |
| --------------------- | -------------- |
| **ID**                | `SDD-018`      |
| **Dominio**           | `bootstrap`    |
| **Tipo**              | `documentation` |
| **Fecha**             | 2026-09-05     |
| **Estado**            | `Released`     |
| **Versión objetivo**  | `v1.4.1`       |
| **Owner**             | mantenedor kit |
| **Prioridad**         | `P1`           |
| **ADRs relacionados** | —              |
| **Dependencias**      | — (audita H-D01/H-D04; post SDD-006 / v1.2.2) |

---

## Problema y objetivo

**Problema:**

Tras la fusión de `sdd-core` en `sdd-agent-workflow` (SDD-006 / v1.2.2), el pipeline canónico (`agent-prompts/`, `cursor-rules/`, `install-agents`) ya no genera `sdd-core.mdc`. En el repo productor queda un residual [`.cursor/rules/sdd-core.mdc`](../../../../.cursor/rules/sdd-core.mdc) versionado con `alwaysApply: true`, que duplica tokens y contradice el diseño actual. Además, [INSTALL.md](../../../../INSTALL.md) y [README.md](../../../../README.md) aún documentan `sdd-core` como artefacto Cursor vigente (hallazgos H-D01 / H-D04).

**Objetivo:**

Eliminar el residual en dogfood Cursor del kit, alinear INSTALL/README al set real de reglas (`sdd-agent-workflow`, `sdd-workflow-reference`, `sdd-stack-<perfil>`, más `sdd-safe-git` si aplica), limpiar mapa legacy en `_extract_prompts.py` si aún referencia `sdd-core`, y dejar documentado el borrado manual de copias huérfanas en consumidores (upgrade-guide / nota v1.4.1).

---

## Alcance

**Incluye:**

- Borrar `.cursor/rules/sdd-core.mdc` del repositorio productor.
- Actualizar `INSTALL.md` y `README.md` para no listar `sdd-core` como regla instalada.
- Limpiar referencia a `sdd-core` en `bootstrap/_extract_prompts.py` si persiste.
- Verificar que `sync-cursor-rules` / `install-agents` **no** regeneran el archivo.
- Una línea en `core/upgrade-guide.md` (y/o nota de release al cerrar) sobre borrar copia local huérfana en consumidores.

**Excluye explícitamente:**

- Fila Discovery *Upgrade/paridad multi-agente* (H-B06 / D03 / D05–D07) — otro Draft.
- Cambiar comportamiento de `install-agents`, skills o manifests (ya sin `sdd-core`).
- Reescribir `TOKEN-OPTIMIZATION.md` / ANALYSIS históricos (pueden citar `sdd-core` como pasado).
- Nueva API CLI, perfiles nuevos, CI `validate-sdd`.

---

## Impacto técnico

Perfil: [`profiles/sdd-kit/spec-impact.md`](../../../../profiles/sdd-kit/spec-impact.md).

| Pregunta | Respuesta |
| -------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)? | Sí (menor) — línea en `upgrade-guide.md` § v1.4.1 |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)? | No aplica |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | Sí (menor) — higiene `_extract_prompts.py` si aplica; sin cambio de pipeline de generación |
| ¿Afecta `cli/` (comandos, librerías)? | No aplica |
| ¿Afecta `.github/workflows/` o reglas Cursor? | Sí — eliminar residual `.cursor/rules/sdd-core.mdc` |
| ¿Requiere actualizar `README.md` o `INSTALL.md`? | Sí — alinear lista de reglas Cursor |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)? | Sí (proceso) — este spec + BACKLOG |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles. | No cambia el texto; aplica DR-4, DR-6, DR-7 |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR. | No — ya decidido en SDD-006 |

---

## Reglas de negocio

Aplica [`.github/docs/business/domain-rules.md`](../../business/domain-rules.md):

- **DR-4** — el agente ejecuta; humano aprueba Ready/merge.
- **DR-6** — documentación SDD solo en `paths.sdd`.
- **DR-7** — dual-release al cerrar `v1.4.1`.
- Bootstrap: cambios en prompts sincronizados con `cursor-rules` vía sync (aquí no se regenera `sdd-core`).

Particularidad: higiene de artefacto residual dogfood + docs de instalación; no cambia metodología SDD.

---

## Criterios de aceptación

**Happy path:**

- [x] `.cursor/rules/sdd-core.mdc` no existe en el working tree del kit.
- [x] `INSTALL.md` y `README.md` no documentan `sdd-core` como regla Cursor vigente.
- [x] `bootstrap/_extract_prompts.py` no mapea `sdd-core.mdc` (si tenía la entrada).
- [x] Tras `sync-cursor-rules` / revisión de fuentes, el archivo **no** reaparece.
- [x] `upgrade-guide.md` (o nota producto al cierre) indica borrado manual de copia huérfana en consumidores.
- [x] `python cli/sdd.py validate` en verde.

**Error path:**

- [x] Si un consumidor mantiene `.cursor/rules/sdd-core.mdc` local tras upgrade: la nota de migración indica borrarlo; no se falla `validate-sdd` por esa copia ajena al kit.

---

## Cambio de BD

No aplica — sin esquema de aplicación.

---

## Diseño técnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `.cursor/rules/sdd-core.mdc` | Eliminar |
| `INSTALL.md` | Quitar `sdd-core.mdc` de la tabla de adaptadores Cursor |
| `README.md` | Quitar mención a regla `sdd-core` |
| `bootstrap/_extract_prompts.py` | Quitar mapa legacy si existe |
| `core/upgrade-guide.md` | § v1.4.1 breve (huérfano local) |

**Notas de diseño:**

- Fuente canónica de reglas always-on: `sdd-agent-workflow` (+ `sdd-workflow-reference` on-demand, stack, safe-git).
- No modificar `agent-prompts/manifest.json` salvo que aún liste `core` (hoy no).

---

## Verificación técnica

```bash
# Ausencia del residual
Test-Path .cursor/rules/sdd-core.mdc   # debe ser False (PowerShell)
# o: test ! -f .cursor/rules/sdd-core.mdc

rg -n "sdd-core\.mdc|regla `sdd-core`" INSTALL.md README.md
python cli/sdd.py validate
```

Opcional: ejecutar sync de cursor-rules y confirmar que no crea `sdd-core.mdc`.

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Algún flujo aún espera el archivo por nombre | Baja | Bajo | Contenido ya en `sdd-agent-workflow`; documentar en upgrade |
| Docs históricos confunden (TOKEN-OPTIMIZATION) | Baja | Bajo | Fuera de alcance; son snapshot |
| Reintroducción accidental vía script extract | Baja | Medio | Limpiar `_extract_prompts.py` |

**Rollback:** restaurar el `.mdc` desde git y revertir docs.

---

## Notas post-implementación

- Enlazar H-D01 / H-D04 del informe de auditoría al cerrar `v1.4.1`.
- No mezclar con Discovery upgrade/paridad multi-agente.
- **2026-09-05 (In Build):** residual eliminado; INSTALL/README alineados; `_extract_prompts` sin mapa `sdd-core`; `sync-cursor-rules` no regenera el archivo; § v1.4.1 en upgrade-guide.
- **Smoke manual (2026-09-05):** humano confirmó exitoso — sin regla `sdd-core` en Cursor; tabla INSTALL revisada.
