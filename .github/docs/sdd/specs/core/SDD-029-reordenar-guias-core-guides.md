# SDD-029 — Reordenar guías de raíz `core/` → `core/guides/`

> Copiar desde plantilla core. Al cerrar: `git mv` a `archive/<YYYY>/core/`.

---

## Cabecera

| Campo                 | Valor                  |
| --------------------- | ---------------------- |
| **ID**                | `SDD-029`              |
| **Dominio**           | `core`                 |
| **Tipo**              | `documentation`        |
| **Fecha**             | 2026-09-12             |
| **Estado**            | `In Build`             |
| **Versión objetivo**  | `v1.6.0` |
| **Owner**             | mantenedor kit         |
| **Prioridad**         | `P2`                   |
| **ADRs relacionados** | —                      |
| **Dependencias**      | SDD-028                |

---

## Problema y objetivo

**Problema:**

Tras SDD-028, `core/guides/` existe para audits/research, pero el resto de guías siguen sueltas en la raíz de `core/`, mezcladas con contratos y entradas del ciclo. La raíz queda sobrecargada y el índice del core no distingue claramente «entrada/contrato» vs «metodología opcional».

**Objetivo:**

Mover las guías listadas a `core/guides/` (mismas nombres de archivo), dejar contratos/entrada en la raíz, actualizar el índice de `guides/` y las referencias **activas**. Sin reescribir el cuerpo de las guías ni stubs en rutas viejas.

---

## Alcance

**Incluye:**

1. **`git mv` a `core/guides/`** (mismas nombres):
   - `adoption-guide.md`
   - `upgrade-guide.md`
   - `healthy-development.md`
   - `operations.md`
   - `branching.md`
   - `agent-setup.md`
   - `checklist-pr.md` (DoD canónica → `guides/`, **no** `templates/`; el scaffold copiable sigue en `templates/pr-template.md`)

2. **Raíz (sin mover):** `README.md`, `concepts.md`, `workflow.md`, `safe-git-contract.md`, `prompt-catalog.md`, `sdd-dependency-graph.md` + carpetas `templates/`, `prompts/`, `releases/`, `adr/`, `examples/`, `guides/`.

3. **Índices:** actualizar [`core/guides/README.md`](../../../../core/guides/README.md) y [`core/README.md`](../../../../core/README.md).

4. **Refs activas** a paths nuevos: `core/` (incl. prompts y links relativos internos de archivos movidos), `profiles/`, `bootstrap/` si aplica, `README.md` / `INSTALL.md` / `CONTRIBUTING.md`, docs de producto vigentes, skills/rules, instancia SDD viva (ADOPTION, índices). Sin stubs en rutas viejas.

5. `python cli/sdd.py validate` en verde.

**Excluye explícitamente:**

- Big rewrite del cuerpo de las guías.
- Stubs en `core/<nombre>.md` antiguos.
- Reescribir `archive/` ni auditorías/notas históricas.
- Reestructurar README raíz del kit (Discovery docs aparte).
- Ampliar `validate-sdd` / CLI / CI.
- ADR nuevo.
- Mover `checklist-pr` a `templates/`.

---

## Impacto técnico

Perfil: [`profiles/sdd-kit/spec-impact.md`](../../../../profiles/sdd-kit/spec-impact.md).

| Pregunta | Respuesta |
| -------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)? | Sí — move a `guides/` + README core + links relativos |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)? | Sí — paths a `checklist-pr.md` en checklists de perfil |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | Sí si hay paths hardcodeados a guías movidas |
| ¿Afecta `cli/` (comandos, librerías)? | No aplica |
| ¿Afecta `.github/workflows/` o reglas Cursor? | Sí si rules/skills citan paths viejos |
| ¿Requiere actualizar `README.md` o `INSTALL.md`? | Sí — enlaces a guías movidas |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)? | Sí — spec + BACKLOG; ADOPTION/índices si enlazan |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles. | No cambia el texto; aplica DR-1 |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR. | No |

---

## Reglas de negocio

Aplica [`.github/docs/business/domain-rules.md`](../../business/domain-rules.md):

- **DR-1** — core agnóstico; solo reorden de paths, sin meter stacks en guías.
- **DR-7** — producto en `core/`; proceso sigue en `paths.sdd`.

Particularidad: `checklist-pr` es DoD de referencia (guía), no plantilla copiable.

---

## Criterios de aceptación

**Happy path:**

- [x] Los 7 archivos viven solo bajo `core/guides/` (no quedan en la raíz).
- [x] Raíz conserva contratos/entrada listados; `templates/pr-template.md` sigue siendo el scaffold de PR.
- [x] `core/guides/README.md` índice incluye las 7 + audits/research.
- [x] `core/README.md` distingue entrada vs `guides/`.
- [x] Refs activas (core, profiles, bootstrap si aplica, README/INSTALL/CONTRIBUTING, docs producto, skills/rules, instancia viva) apuntan a `core/guides/...`.
- [x] Links relativos internos de archivos movidos (p. ej. a `workflow.md`) corregidos.
- [x] `python cli/sdd.py validate` en verde.

**Error path:**

- [x] No hay stubs en rutas viejas de la raíz.
- [x] No se reescribieron `archive/` ni informes de auditoría históricos.
- [x] No se movió `checklist-pr` a `templates/`.
- [x] Sin big rewrite de contenido de las guías.

---

## Congelado para implementación _(opcional)_

Omitido — frontera move vs raíz y política de refs cerradas en alcance.

---

## Cambio de BD

No aplica.

---

## Diseño técnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `core/guides/{adoption-guide,upgrade-guide,healthy-development,operations,branching,agent-setup,checklist-pr}.md` | `git mv` desde raíz + fix links relativos |
| `core/guides/README.md` | Índice ampliado |
| `core/README.md` | Tabla entrada vs guides |
| `profiles/*/checklist-stack.md` | Path a `../guides/checklist-pr.md` |
| Prompts / README / INSTALL / CONTRIBUTING / docs producto / rules | Paths nuevos |

**Notas de diseño:**

- Mismas nombres de archivo → menos churn semántico; solo cambia el directorio.
- Política refs: activas sí; archive e históricos no.

---

## Verificación técnica

```bash
python cli/sdd.py validate
# Comprobar: no existen core/{adoption-guide,upgrade-guide,...}.md en raíz
# Comprobar: existen bajo core/guides/
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Enlaces rotos en docs activas | Media | Medio | Grep paths viejos en zonas activas |
| Consumidores con bookmarks a ruta raíz | Baja | Bajo | Nota en release patch; sin stubs |
| Confundir checklist-pr con pr-template | Baja | Bajo | Exclusión explícita + índice guides |

**Rollback:** `git mv` inverso de los 7 archivos + revertir refs.

---

## Notas post-implementación

- Origen: Discovery post SDD-028; frontera confirmada (agent-setup sí; checklist-pr → guides no templates; refs A sin stubs).
- **2026-09-12 (In Build):** `git mv` de 7 guías → `core/guides/`; `init-sdd` copia `core/guides/` completo (layout `paths.sdd/guides/`); skills/rules/profiles/docs producto actualizados; archive/históricos sin tocar.
- Smoke manual (humano): abrir `core/guides/README.md` + una guía movida; confirmar que no existen los 7 en raíz de `core/`.
