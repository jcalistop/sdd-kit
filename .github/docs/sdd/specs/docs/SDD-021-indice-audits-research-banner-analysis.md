# SDD-021 — Índice artefactos paths.sdd (audits/research) + banner ANALYSIS

> Copiar desde plantilla core. Al cerrar: `git mv` a `archive/<YYYY>/docs/`.

---

## Cabecera

| Campo                 | Valor          |
| --------------------- | -------------- |
| **ID**                | `SDD-021`      |
| **Dominio**           | `docs`         |
| **Tipo**              | `documentation` |
| **Fecha**             | 2026-09-05     |
| **Estado**            | `In Build`     |
| **Versión objetivo**  | `v1.4.1`       |
| **Owner**             | mantenedor kit |
| **Prioridad**         | `P2`           |
| **ADRs relacionados** | —              |
| **Dependencias**      | — (audita H-A04/E02/B09; `audits/` ya versionado en v1.4.0) |

---

## Problema y objetivo

**Problema:**

Las carpetas `audits/` y `research/` bajo `paths.sdd` no figuran en un mapa canónico (ADOPTION / README del proceso), así que su rol documental es ambiguo (H-A04). `ANALYSIS.md` se lee como evaluación “actual” sin banner de snapshot (a diferencia de ROADMAP), pese a ser baseline 2026-06-11; la fuente operativa post-auditoría es el informe en `audits/` + BACKLOG (H-E02 / H-E06).

**Objetivo:**

Publicar un índice corto de artefactos del proceso SDD (incl. audits/research) y añadir banner de snapshot a ANALYSIS con enlace al informe de auditoría y al BACKLOG — sin reescribir el cuerpo histórico ni ampliar `validate-sdd`.

---

## Alcance

**Incluye:**

- Crear [`.github/docs/sdd/README.md`](../../README.md) como índice del árbol proceso (`audits/`, `research/`, `adr/`, `archive/`, `specs/`, `releases/`, BACKLOG, etc.).
- Enlace de una línea desde [`ADOPTION.md`](../../ADOPTION.md) al README índice; mencionar que `audits/` está versionado.
- Banner snapshot al inicio de [`.github/docs/business/planning/ANALYSIS.md`](../../../business/planning/ANALYSIS.md) (estilo ROADMAP): fecha baseline, “no es tablero operativo”, enlace a informe `audits/20260905-…-informe.md` y a `BACKLOG.md`.

**Excluye explícitamente:**

- Ampliar `validate-sdd` para exigir índice/carpetas (H-C04).
- Reescribir cuerpo ANALYSIS / ROADMAP.
- Fix ruta harness en `core/concepts.md` (H-A05).
- Dogfooding consumidor externo (otra fila Discovery).
- Nota release / upgrade-guide § v1.4.1 detallada salvo al cierre Released.

---

## Impacto técnico

Perfil: [`profiles/sdd-kit/spec-impact.md`](../../../../profiles/sdd-kit/spec-impact.md).

| Pregunta | Respuesta |
| -------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)? | No aplica |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)? | No aplica |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | No aplica |
| ¿Afecta `cli/` (comandos, librerías)? | No aplica |
| ¿Afecta `.github/workflows/` o reglas Cursor? | No aplica |
| ¿Requiere actualizar `README.md` o `INSTALL.md`? | No aplica (README de `paths.sdd`, no raíz del kit) |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)? | Sí — este spec + ADOPTION + README proceso + planning ANALYSIS |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles. | No cambia el texto; aplica DR-6, DR-7 |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR. | No |

---

## Reglas de negocio

Aplica [`.github/docs/business/domain-rules.md`](../../business/domain-rules.md):

- **DR-6** — documentación SDD en `paths.sdd`; planning histórico en `business/planning/`.
- **DR-7** — dual-release al cerrar `v1.4.1`.

Particularidad: navegación documental; no cambia producto kit instalable.

---

## Criterios de aceptación

**Happy path:**

- [x] Existe `.github/docs/sdd/README.md` con roles de `audits/`, `research/` y demás carpetas clave del proceso.
- [x] `ADOPTION.md` enlaza al índice y reconoce `audits/` versionado.
- [x] `ANALYSIS.md` tiene banner de snapshot (baseline 2026-06-11) con enlace al informe de auditoría 2026-09-05 y a BACKLOG.
- [x] Cuerpo histórico de ANALYSIS no reescrito (solo cabecera/banner).
- [x] `python cli/sdd.py validate` en verde.

**Error path:**

- [x] Si se añade un audit/research nuevo sin actualizar el README: el spec deja nota de mantenimiento (“actualizar índice al añadir artefacto”); no falla CI (validate no exige el índice).

---

## Cambio de BD

No aplica.

---

## Diseño técnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `.github/docs/sdd/README.md` | Nuevo índice |
| `.github/docs/sdd/ADOPTION.md` | Enlace + mención audits |
| `.github/docs/business/planning/ANALYSIS.md` | Banner snapshot |

**Notas de diseño:**

- Modelo de banner: párrafo inicial de ROADMAP (`Snapshot histórico` + BACKLOG operativo).
- Listar research existentes por nombre de archivo o carpeta, sin resumir cada nota.

---

## Verificación técnica

```bash
# Existencia del índice y banner
Test-Path .github/docs/sdd/README.md
Select-String -Path .github/docs/business/planning/ANALYSIS.md -Pattern 'Snapshot|2026-06-11|audits'
python cli/sdd.py validate
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Índice se desactualiza | Media | Bajo | Nota de mantenimiento en README |
| Lectores siguen tomando ANALYSIS como actual | Baja | Medio | Banner visible al inicio |

**Rollback:** revertir README / diffs ADOPTION / banner ANALYSIS.

---

## Notas post-implementación

- Enlazar H-A04 / H-E02 / H-B09 al cerrar `v1.4.1`.
- H-C04 (sensor validate) queda como deuda explícita fuera de alcance.
- **2026-09-05 (In Build):** README índice + ADOPTION + banner ANALYSIS.
- **Smoke manual (2026-09-06):** humano confirmó exitoso — índice README y banner ANALYSIS revisados.
