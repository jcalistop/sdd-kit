# SDD-020 — Upgrade / paridad multi-agente (wording, targets, safe-git doc)

> Copiar desde plantilla core. Al cerrar: `git mv` a `archive/<YYYY>/bootstrap/`.

---

## Cabecera

| Campo                 | Valor          |
| --------------------- | -------------- |
| **ID**                | `SDD-020`      |
| **Dominio**           | `bootstrap`    |
| **Tipo**              | `documentation` |
| **Fecha**             | 2026-09-05     |
| **Estado**            | `In Build`     |
| **Versión objetivo**  | `v1.4.1`       |
| **Owner**             | mantenedor kit |
| **Prioridad**         | `P2`           |
| **ADRs relacionados** | —              |
| **Dependencias**      | — (audita H-B06/D03/D05–D07; post SDD-016 / v1.3.2; campaña con SDD-018/019) |

---

## Problema y objetivo

**Problema:**

Tras v1.3.2 (retiro de `cost-governance`), la skill [`sdd-upgrade-kit/SKILL.md`](../../../../bootstrap/agent-skills/sdd-upgrade-kit/SKILL.md) sigue citándolo en el checklist post-upgrade (H-B06/D03) y hardcodea `--agent cursor` en la reinstalación (H-D07), ignorando `agent.targets`. Además, la paridad multi-agente y la asimetría de safe-git (Cursor = regla completa; Claude/Codex/Copilot = mención en preamble) no están documentadas de forma explícita como límite de producto del kit (H-D05/D06; decisión auditoría: no dogfood no-Cursor en el repo).

**Objetivo:**

Alinear wording de upgrade a reference v1.3.2, hacer que el paso de reinstalación use `agent.targets` del config, y documentar en `agent-setup` (y nota breve en upgrade-guide si aplica) el dogfood Cursor-only del kit y la asimetría safe-git — sin cambiar `install-agents.py` ni instalar adaptadores extra en el repo.

---

## Alcance

**Incluye:**

- Corregir `bootstrap/agent-skills/sdd-upgrade-kit/SKILL.md`: quitar `cost-governance` del checklist; alinear a [`reference.md`](../../../../bootstrap/agent-skills/sdd-upgrade-kit/reference.md).
- Mismo SKILL: reinstalar adaptadores según `agent.targets` de `sdd.config.yaml` (no hardcode solo `cursor`).
- Documentar en [`core/agent-setup.md`](../../../../core/agent-setup.md): dogfood del kit = Cursor; asimetría safe-git Cursor vs preamble no-Cursor.
- Nota breve en `core/upgrade-guide.md` si refuerza el punto de targets / sin cost-governance.
- Sync/copia de la skill al dogfood `.cursor/skills/sdd-upgrade-kit/` si el repo la versiona en paralelo.

**Excluye explícitamente:**

- Instalar Claude/Codex/Copilot en el repositorio kit (H-D05).
- Cambiar `install-agents.py` / `combined_body` para embeber el contrato safe-git completo en no-Cursor (posible minor / otro SDD).
- Tests de adaptadores no-Cursor (H-D08); ampliar `validate-sdd`.
- Reescribir ANALYSIS / TOKEN-OPTIMIZATION históricos.
- Índice audits (otra fila Discovery docs).

---

## Impacto técnico

Perfil: [`profiles/sdd-kit/spec-impact.md`](../../../../profiles/sdd-kit/spec-impact.md).

| Pregunta | Respuesta |
| -------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)? | Sí (menor) — `agent-setup.md`; posiblemente `upgrade-guide.md` |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)? | No aplica |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | Sí — skill `sdd-upgrade-kit` (texto); **no** `install-agents.py` |
| ¿Afecta `cli/` (comandos, librerías)? | No aplica |
| ¿Afecta `.github/workflows/` o reglas Cursor? | No aplica (salvo copia skill dogfood en `.cursor/skills` si existe) |
| ¿Requiere actualizar `README.md` o `INSTALL.md`? | No aplica (salvo mención cruzada mínima; no requerida) |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)? | Sí (proceso) — este spec + BACKLOG |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles. | No cambia el texto; aplica DR-4, DR-6, DR-7 |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR. | No — documenta decisión ya tomada en auditoría |

---

## Reglas de negocio

Aplica [`.github/docs/business/domain-rules.md`](../../business/domain-rules.md):

- **DR-4** — humano aprueba Ready/merge.
- **DR-6** — docs SDD en `paths.sdd`.
- **DR-7** — dual-release al cerrar `v1.4.1`.

Particularidad: documentación + wording de skill; el instalador multi-agente ya existe.

---

## Criterios de aceptación

**Happy path:**

- [x] `sdd-upgrade-kit/SKILL.md` no lista `cost-governance` como artefacto post-upgrade vigente.
- [x] El paso de `install-agents` en la skill usa `agent.targets` (o equivalente documentado), no solo `--agent cursor` fijo.
- [x] `core/agent-setup.md` declara dogfood Cursor-only del kit y la asimetría safe-git (Cursor regla vs preamble no-Cursor).
- [x] Copia dogfood `.cursor/skills/sdd-upgrade-kit/` alineada si el repo la mantiene. _(No aplica — el repo no versiona esa copia; fuente canónica = bootstrap.)_
- [x] `python cli/sdd.py validate` en verde.

**Error path:**

- [x] Si `agent.targets` está vacío o ausente: la skill documenta fallback (p. ej. detectar / pedir humano / `cursor`), sin silenciar el caso.
- [x] Consumidor que aún tenga skill huérfana `sdd-cost-governance`: reference/upgrade-guide siguen indicando borrado manual (no regresión).

---

## Cambio de BD

No aplica — sin esquema de aplicación.

---

## Diseño técnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `bootstrap/agent-skills/sdd-upgrade-kit/SKILL.md` | Wording v1.3.2 + targets |
| `core/agent-setup.md` | Límites dogfood + asimetría safe-git |
| `core/upgrade-guide.md` | Nota breve si aplica |
| `.cursor/skills/sdd-upgrade-kit/SKILL.md` | Sync si existe en repo |

**Notas de diseño:**

- SemVer patch: no nueva API; alinea skill al comportamiento ya soportado por `install-agents --agent`.
- No tocar `combined_body` / preambles salvo documentación.

---

## Verificación técnica

```bash
rg -n "cost-governance" bootstrap/agent-skills/sdd-upgrade-kit/SKILL.md
# no debe aparecer como checklist vigente post-upgrade
rg -n "agent.targets|--agent cursor" bootstrap/agent-skills/sdd-upgrade-kit/SKILL.md
python cli/sdd.py validate
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Instancia con varios targets reinstala más adaptadores | Baja | Bajo | Deseado; documentar |
| Confundir “documentar asimetría” con “arreglar paridad código” | Media | Bajo | Exclusión explícita en alcance |
| Desync skill bootstrap vs `.cursor/skills` | Baja | Medio | Criterio de sync en DoD |

**Rollback:** revertir commits de skill/docs.

---

## Notas post-implementación

- Enlazar H-B06 / D03 / D05–D07 al cerrar `v1.4.1`.
- Embeber safe-git completo en no-Cursor = iniciativa futura (minor).
- **2026-09-05 (In Build):** SKILL upgrade alineada a v1.3.2 + `agent.targets`; `agent-setup` + `upgrade-guide` § v1.4.1 actualizados.
- **Smoke manual (2026-09-05):** humano confirmó exitoso — skill pasos 6–7 y `agent-setup.md` revisados.
