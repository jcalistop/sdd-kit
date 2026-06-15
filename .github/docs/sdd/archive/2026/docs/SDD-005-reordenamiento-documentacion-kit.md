# SDD-005 — Reordenamiento documentación kit (business + docs/releases)

---

## Cabecera

| Campo                 | Valor                        |
| --------------------- | ---------------------------- |
| **ID**                | `SDD-005`                    |
| **Dominio**           | `docs`                       |
| **Tipo**              | `refactor` + `documentation` |
| **Fecha**             | 2026-06-15                   |
| **Estado**            | `Released`                   |
| **Versión objetivo**  | `v1.2.0`                     |
| **Owner**             | equipo                       |
| **Prioridad**         | `P2`                         |
| **ADRs relacionados** | —                            |
| **Dependencias**      | SDD-004 Released (`v1.2.0`)  |

---

## Problema y objetivo

**Problema:**

La raíz `docs/` mezcla dos propósitos: **releases SemVer del producto** (consumibles vía `upgrade-kit`) y **documentación de planificación inicial** (`docs/maintainers/`: ROADMAP, ANALYSIS, TOKEN-OPTIMIZATION, meta PROMPT-CATALOG). Eso colisiona con el modelo de capas ya definido en [`domain-rules.md`](../../business/domain-rules.md) y [`ADOPTION.md`](../ADOPTION.md), donde el contexto de producto vive en `.github/docs/business/` y el proceso SDD en `.github/docs/sdd/`.

Además existen solapamientos que confunden mantenedores y agentes:

- `docs/releases/vX.Y.Z.md` vs `.github/docs/sdd/releases/vX.Y.Z/release_vX.Y.Z.md` (mismo hito, narrativas parecidas)
- `bootstrap/agent-skills/` vs `.cursor/skills/sdd-*` (fuente vs instalado, ambos versionados en el repo del kit)
- `core/releases/` (plantillas para consumidores) vs `docs/releases/` vs `.github/docs/sdd/releases/` (tres “releases” con nombres parecidos)

**Objetivo:**

Reordenar la documentación del repositorio `sdd-kit` para que:

1. **`docs/`** contenga solo **`docs/releases/`** (changelog SemVer del producto, fuente para consumidores).
2. **`docs/maintainers/`** migre a **`.github/docs/business/`** (contexto y planificación del producto kit).
3. Queden **contratos explícitos** por capa para evitar drift y duplicación futura.
4. Referencias rotas se corrijan en README, ADOPTION, domain-rules, agent-setup y CHANGELOG.

---

## Alcance

### Incluye

**Fase 1 — Migración `docs/maintainers/` → `business/`**

- `git mv` de archivos a `.github/docs/business/planning/` (o subcarpeta acordada en Ready):
    - `ANALYSIS.md`, `ROADMAP.md`, `TOKEN-OPTIMIZATION.md`, `PROMPT-CATALOG.md` (meta mantenedores), `README.md`
- Actualizar [`business/README.md`](../../business/README.md) y [`domain-rules.md`](../../business/domain-rules.md) (reglas 6–7, diagrama de capas).
- Stub deprecación: `docs/maintainers/README.md` con enlaces a nueva ubicación (una versión; sin contenido duplicado).
- Barrido de enlaces en: `README.md`, `ADOPTION.md`, `BACKLOG.md`, `core/agent-setup.md`, `docs/releases/CHANGELOG.md`, `docs/maintainers/ROADMAP.md` (rutas internas).

**Fase 2 — Contrato `docs/releases/` vs instancia SDD**

- Documentar en [`docs/releases/README.md`](../../../docs/releases/README.md) y [`ADOPTION.md`](../ADOPTION.md):

| Capa                          | Ruta                                | Rol                                                | ¿Copiado por `init-sdd`?          |
| ----------------------------- | ----------------------------------- | -------------------------------------------------- | --------------------------------- |
| Release producto kit          | `docs/releases/vX.Y.Z.md`           | Notas para consumidores y GitHub Releases          | No (vive en submodule)            |
| Cierre campaña SDD (kit)      | `.github/docs/sdd/releases/vX.Y.Z/` | Acta SDD: specs, gates, enlace al producto         | No                                |
| Plantillas release consumidor | `core/releases/`                    | RUNBOOK y plantillas para **apps** que adoptan SDD | Sí → `.github/docs/sdd/releases/` |

- Adelgazar plantilla de `release_vX.Y.Z.md` en instancia kit: **enlace** a `docs/releases/vX.Y.Z.md` + tabla specs + gates (sin repetir “novedades”).

**Fase 3 — Mejoras adicionales (propuestas incluidas)**

| #   | Mejora                                                    | Acción                                                                                                                                                              |
| --- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| M1  | `.cursor/skills/sdd-*` duplican `bootstrap/agent-skills/` | Añadir `.cursor/skills/sdd-*` y `.sdd-kit-manifest.json` a `.gitignore` del kit; documentar `install-agents.py` post-clone en `CONTRIBUTING` o `business/planning/` |
| M2  | Tres carpetas “releases”                                  | Glosario en `docs/README.md` (nuevo, 1 página) + fila en `domain-rules`                                                                                             |
| M3  | `PROMPT-CATALOG.md` meta vs `core/prompt-catalog.md`      | Renombrar a `business/planning/prompt-catalog-meta.md` y enlace bidireccional explícito                                                                             |
| M4  | ROADMAP histórico vs BACKLOG                              | Cabecera en `ROADMAP.md`: “snapshot 2026-06; operativo → BACKLOG”                                                                                                   |
| M5  | Validación                                                | Script o paso en `validate-sdd`: fallar si existe `docs/maintainers/*.md` salvo README stub                                                                         |

**Fase 4 — Consumidores**

- Nota en `docs/releases/v1.2.0.md`: sin cambio de API; solo rutas de docs del submodule.
- Backoffice y demás instancias: **sin** merge de `docs/maintainers/` (nunca se copiaba).

### Excluye

- Mover `core/`, `bootstrap/`, `profiles/`, `cli/` bajo `docs/` o `business/`
- Unificar `docs/releases/` con `.github/docs/sdd/releases/` en un solo archivo (se mantienen roles distintos)
- Copiar `business/planning/` a proyectos consumidores vía `init-sdd`
- Cambios en código de producto Laravel/backoffice
- Archivar specs de campañas consumidoras

---

## Impacto técnico

| Pregunta                  | Respuesta                                                                 |
| ------------------------- | ------------------------------------------------------------------------- |
| ¿Afecta `init-sdd`?       | No — no copiaba `docs/maintainers/`                                       |
| ¿Afecta consumidores?     | Solo enlaces rotos si bookmarkaban URLs GitHub a `docs/maintainers/`      |
| ¿db-change?               | No                                                                        |
| ¿Decisión arquitectónica? | Sí — consolida capa `business/` como único hogar de contexto producto kit |

---

## Reglas de negocio

| Regla                        | Aplicación                                                                      |
| ---------------------------- | ------------------------------------------------------------------------------- |
| **DR-6** (`domain-rules.md`) | Actualizar: specs solo en `.github/docs/sdd/`; planning en `business/planning/` |
| **DR-7**                     | Actualizar diagrama: `docs/` = solo `releases/`                                 |
| **DR-1**                     | Sin acoplar stacks en docs movidos                                              |

---

## Criterios de aceptación

**Happy path:**

- [x] `docs/maintainers/` vacío salvo `README.md` stub con enlaces
- [x] Contenido en `.github/docs/business/planning/` (5 archivos migrados)
- [x] `docs/README.md` explica capas releases (producto / instancia / core)
- [x] Cero referencias a `docs/maintainers/*.md` salvo stub (grep en repo)
- [x] `release_v1.2.0.md` (o próximo) sigue patrón adelgazado documentado
- [x] M1: `.gitignore` + nota post-clone (si se aprueba en Ready)
- [x] `python cli/sdd.py validate` → 0 errores
- [x] `validate-sdd.ps1` → OK

**Error path:**

- [x] Stub `docs/maintainers/README.md` visible en GitHub con destino correcto
- [x] No se elimina historial git de archivos movidos (`git mv`)

---

## Riesgos

| Riesgo                                                        | Mitigación                                                   |
| ------------------------------------------------------------- | ------------------------------------------------------------ |
| Enlaces externos rotos                                        | Stub una versión; mención en CHANGELOG v1.2.0                |
| Agente busca `docs/maintainers/ROADMAP`                       | Actualizar reglas Cursor del kit si referencian ruta vieja   |
| Confundir `business/planning/` con `business/domain-rules.md` | README en subcarpeta con audiencia “histórico/planificación” |

---

## Alternativas consideradas

| Opción                                             | Pros                                            | Contras                               |
| -------------------------------------------------- | ----------------------------------------------- | ------------------------------------- |
| **A (recomendada)** `business/planning/`           | Alineado a ADOPTION; separa reglas vs histórico | Más profundidad de rutas              |
| **B** Archivar en `.github/docs/sdd/archive/docs/` | Cerca del proceso SDD                           | Mezcla producto con proceso           |
| **C** Eliminar ROADMAP/ANALYSIS                    | Menos ruido                                     | Pérdida de contexto de diseño inicial |

---

## Referencias

- Análisis previo (sesión): duplicación `docs/` vs `.github/docs/sdd/`
- [`docs/maintainers/README.md`](../../../docs/maintainers/README.md) — tabla capas actual
- SDD-004 — skills upstream (`v1.2.0`)
