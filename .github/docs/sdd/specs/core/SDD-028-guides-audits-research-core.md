# SDD-028 — Guías audits + research en `core/guides/`

> Copiar desde plantilla core. Al cerrar: `git mv` a `archive/<YYYY>/core/`.

---

## Cabecera

| Campo                 | Valor                  |
| --------------------- | ---------------------- |
| **ID**                | `SDD-028`              |
| **Dominio**           | `core`                 |
| **Tipo**              | `documentation`        |
| **Fecha**             | 2026-09-12             |
| **Estado**            | `In Build`             |
| **Versión objetivo**  | `v1.6.0` |
| **Owner**             | mantenedor kit         |
| **Prioridad**         | `P2`                   |
| **ADRs relacionados** | —                      |
| **Dependencias**      | SDD-026, SDD-027 (guías hoy en instancia `paths.sdd`) |

---

## Problema y objetivo

**Problema:**

Las metodologías de audits y research viven solo en la instancia dogfood (`.github/docs/sdd/audits|research/README.md`). Los consumidores del kit ven las plantillas en `core/templates/` pero no la guía canónica; la raíz de `core/` ya está cargada, así que no conviene soltar dos archivos sueltos más ahí.

**Objetivo:**

Publicar la metodología **audits + research** como producto kit bajo `core/guides/` (SoT). Los README de la instancia pasan a **stub** (rol local + enlace al core). Índice mínimo en `core/guides/README.md`. Sin reordenar el resto de guías de la raíz (Discovery aparte).

---

## Alcance

**Incluye:**

1. **`core/guides/`** (carpeta nueva):
   - `audits.md` — contenido migrado/adaptado desde `paths.sdd/audits/README.md` (agnóstico DR-1; sin historial dogfood ni stubs de tag como SoT de instancia).
   - `research.md` — idem desde `paths.sdd/research/README.md` (sin notas históricas).
   - `README.md` — índice mínimo de la carpeta (enlaces a audits + research + plantillas).

2. **Stubs de instancia:**
   - `.github/docs/sdd/audits/README.md` y `research/README.md` → rol local + enlace a `core/guides/*` (sin duplicar cuerpo).

3. **Referencias:**
   - [`.github/docs/sdd/README.md`](../../README.md) — celda Metodología apunta a `core/guides/`.
   - [`core/README.md`](../../../../core/README.md) — fila(s) a `guides/`.
   - [`core/concepts.md`](../../../../core/concepts.md) — enlace a guías (sin reescribir concepts).
   - Plantillas `audit-*` / `research-nota` y notas de reuso (dogfood / harness) → SoT en `core/guides/`.

4. Actualizar notas post-implementación de SDD-026/027 solo si hace falta coherencia de paths (sin reabrir alcance de esos specs).

**Excluye explícitamente:**

- Mover `healthy-development`, `adoption-guide`, `upgrade-guide`, `operations`, `branching`, etc. (fila Discovery «reorden core»).
- Bootstrap creando carpetas `audits/` / `research/` en consumidores.
- Ampliar `validate-sdd`; skill/CLI/CI.
- Migrar corridas/notas históricas.
- ADR nuevo.

---

## Impacto técnico

Perfil: [`profiles/sdd-kit/spec-impact.md`](../../../../profiles/sdd-kit/spec-impact.md).

| Pregunta | Respuesta |
| -------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)? | Sí — `core/guides/` + README core + concepts |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)? | No aplica |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | No aplica |
| ¿Afecta `cli/` (comandos, librerías)? | No aplica |
| ¿Afecta `.github/workflows/` o reglas Cursor? | No aplica |
| ¿Requiere actualizar `README.md` o `INSTALL.md`? | No aplica (raíz kit); sí `core/README.md` |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)? | Sí — stubs audits/research + índice paths.sdd |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles. | No cambia el texto; aplica DR-1, DR-6 |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR. | No |

---

## Reglas de negocio

Aplica [`.github/docs/business/domain-rules.md`](../../business/domain-rules.md):

- **DR-1** — guías en `core/` agnósticas al stack.
- **DR-6** — artefactos de corrida/nota siguen en `paths.sdd`; la guía canónica pasa a producto kit.

Particularidad: no obligar carpetas `audits/`/`research/` a consumidores; plantillas + guías disponibles para adopción voluntaria.

---

## Criterios de aceptación

**Happy path:**

- [x] Existen `core/guides/audits.md`, `core/guides/research.md` y `core/guides/README.md` (índice mínimo).
- [x] Contenido de las guías es agnóstico (DR-1) y enlaza plantillas en `core/templates/`.
- [x] `paths.sdd/audits/README.md` y `research/README.md` son stubs que apuntan al core (sin cuerpo duplicado).
- [x] Índice paths.sdd y `core/README.md` (y concepts si aplica) enlazan `core/guides/`.
- [x] Un consumidor del submodule puede abrir la guía sin depender de `.github/docs/sdd/` del kit.
- [x] `python cli/sdd.py validate` en verde.

**Error path:**

- [x] Documentado: carpetas `audits/`/`research/` en consumidores siguen opcionales.
- [x] No se migraron notas/corridas históricas ni se movieron otras guías de la raíz de `core/`.
- [x] Guías sin stacks concretos (DR-1).

---

## Congelado para implementación _(opcional)_

Omitido — paths y stubs cerrados.

---

## Cambio de BD

No aplica.

---

## Diseño técnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `core/guides/audits.md` | SoT metodología audits |
| `core/guides/research.md` | SoT metodología research |
| `core/guides/README.md` | Índice mínimo |
| `.github/docs/sdd/audits/README.md` | Stub |
| `.github/docs/sdd/research/README.md` | Stub |
| `.github/docs/sdd/README.md` | Enlaces a core/guides |
| `core/README.md` / `core/concepts.md` | Enlaces |
| Plantillas / reuso | Paths SoT |

**Notas de diseño:**

- SoT = `core/guides/*`; instancia = descubrimiento local + listado de artefactos en índice padre.
- Congelado: omitido.

---

## Verificación técnica

```bash
python cli/sdd.py validate
# Al implementar: core/guides/* + stubs + enlaces
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Enlaces rotos a README de instancia | Media | Medio | Grep + actualizar plantillas/reuso en el mismo PR |
| Duplicar cuerpo en stub | Baja | Medio | Stub ≤ ~15 líneas; enlace explícito «canónico en core» |
| Confundir con reorden amplio de core | Baja | Bajo | Exclusión + Discovery aparte |

**Rollback:** revertir `core/guides/` y restaurar cuerpos en stubs de instancia.

---

## Notas post-implementación

- Origen: conversación post SDD-027 (guías solo en dogfood; raíz core sobrecargada).
- Discovery hermano: reordenar otras guías de raíz → `core/guides/` (no este SDD).
- **2026-09-12 (In Build):** `core/guides/{audits,research,README}.md`; stubs en instancia; enlaces índice/core/concepts/plantillas/reuso.
- **Smoke manual (2026-09-12):** humano confirmó OK — `core/guides/audits.md` usable sin paths.sdd; stubs sin cuerpo duplicado; índice paths.sdd → `core/guides/`.
