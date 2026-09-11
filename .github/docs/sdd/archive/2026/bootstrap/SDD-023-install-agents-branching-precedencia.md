# SDD-023 — install-agents: branching mode + precedencia instancia > global

> Spec Released. Archivado en `archive/2026/bootstrap/`.

---

## Cabecera

| Campo                 | Valor        |
| --------------------- | ------------ |
| **ID**                | `SDD-023`    |
| **Dominio**           | `bootstrap`  |
| **Tipo**              | `feature`    |
| **Fecha**             | 2026-09-10   |
| **Estado**            | `Released`   |
| **Versión objetivo**  | `v1.5.0`     |
| **Owner**             | mantenedor   |
| **Prioridad**         | `P0`         |
| **ADRs relacionados** | —            |
| **Dependencias**      | —            |

---

## Problema y objetivo

**Problema:** Skills SDD en `~/.cursor/skills` (legado o copia) chocan con las de la instancia del repo. En dogfood externo (`minsal-centinela`, kit `v1.4.1`) skills globales asumían push directo a `origin/dev` y prohibían `feature/*`, mientras `branching.md` del consumidor exigía feature → PR a `dev`. Cursor cargó ambas y el agente contradijo la política del proyecto.

**Objetivo:** Que `install-agents` (1) renderice reglas de rama según `agent.branching_mode` en las skills del **proyecto**, y (2) borre skills `sdd-*` del manifest en `~/.cursor/skills` para que la instancia sea la fuente de verdad.

**Origen:** [informe dogfood gap #2](../../audits/20260906-dogfood-consumidor-externo-informe.md).

---

## Alcance

**Incluye:**

- Clave `agent.branching_mode` (`solo-push-dev` | `feature-pr-dev`) leída desde `sdd.config.yaml` del target.
- Placeholder `{{BRANCHING_RULES}}` en skills `sdd-build-spec` y `sdd-open-pr` (SKILL + reference).
- Tras instalar skills en el proyecto: borrar IDs managed del manifest bajo `~/.cursor/skills`.
- Docs: example config, `agent-setup`, ítem checklist `sdd-kit`.
- Tests en `bootstrap/test_install_skills.py`.

**Excluye explícitamente:**

- Gap dogfood #7 (`{{STACK_PROFILE}}` hardcodeado).
- Cambiar la política canónica de `core/branching.md` (sigue feature→PR por defecto del kit).
- Reintroducir instalación de skills en `~/.cursor/skills`.
- Adaptadores Claude / Codex / Copilot.
- Otras skills distintas de build-spec y open-pr.

---

## Congelado para implementación

> Obligatorio para LLM de bajo contexto. **Prohibido explorar** fuera de esta lista. Lectura máx.: estos archivos + este spec + `.github/docs/business/domain-rules.md` (~15 paths).

### Decisión única

1. Clave: `agent.branching_mode` en `{target}/{sdd_path}/sdd.config.yaml` → `solo-push-dev` | `feature-pr-dev`.
2. Si falta la clave: default **`feature-pr-dev`**.
3. Valor inválido: `install-agents` **falla** (exit ≠ 0) con mensaje que cite `agent.branching_mode` y los dos valores válidos.
4. Un solo placeholder `{{BRANCHING_RULES}}`: el instalador elige el fragmento y lo sustituye al escribir skills. **No** dejar `if mode` para el LLM en runtime.
5. Tras escribir skills en `target/.cursor/skills/`: para cada ID del manifest, si existe `Path.home() / ".cursor" / "skills" / <id>`, hacer `shutil.rmtree` y log `removed global skill: <id>`. No tocar otras carpetas.
6. **Override humano:** el modo es el default del harness, no un veto. Si el humano pide explícitamente lo contrario al modo, el agente informa `agent.branching_mode`, pide confirmación escrita y **sigue al humano**. No insistir ni crear conflicto de silencio.

### Fragmentos exactos de `{{BRANCHING_RULES}}`

**`feature-pr-dev`:**

```text
Modo: feature-pr-dev. Crear rama feature/|bugfix/|maintenance/ según tipo; PR obligatorio hacia {{DEV_BRANCH}}; no push directo a origin/{{DEV_BRANCH}}. Si el humano pide explícitamente lo contrario (p. ej. push a origin/{{DEV_BRANCH}} sin PR): informar el modo, pedir confirmación escrita y seguir al humano.
```

**`solo-push-dev`:**

```text
Modo: solo-push-dev. Trabajar en {{DEV_BRANCH}} (o push a origin/{{DEV_BRANCH}} tras verify + confirmación humana). No exigir rama feature/* ni PR. Si el humano pide open-pr o rama feature/*: informar que el modo es solo-push-dev, preguntar si igual quiere eso y, con confirmación escrita, seguir al humano.
```

Nota: `{{DEV_BRANCH}}` en esos fragmentos se resuelve en el mismo `render_template` (ya existe hoy).

### Dónde insertar el placeholder

Bloque corto «Ramas / branching» con `{{BRANCHING_RULES}}` **solo** en:

1. `bootstrap/agent-skills/sdd-build-spec/SKILL.md` — junto al paso de rama
2. `bootstrap/agent-skills/sdd-build-spec/reference.md` — sección Convención de ramas
3. `bootstrap/agent-skills/sdd-open-pr/SKILL.md` — inicio del procedimiento
4. `bootstrap/agent-skills/sdd-open-pr/reference.md` — sección Destino

### Lista cerrada de archivos a editar

1. `bootstrap/install-agents.py` — `read_branching_mode(target, sdd_path)`; ampliar `skill_render_context` con `BRANCHING_RULES`; `remove_global_managed_skills(managed_ids)` llamada al final de `install_cursor_skills` (también cuando el marcador hace skip temprano: **sí** ejecutar limpieza global en ese caso, para no dejar globals viejos)
2. `bootstrap/agent-skills/sdd-build-spec/SKILL.md`
3. `bootstrap/agent-skills/sdd-build-spec/reference.md`
4. `bootstrap/agent-skills/sdd-open-pr/SKILL.md`
5. `bootstrap/agent-skills/sdd-open-pr/reference.md`
6. `bootstrap/test_install_skills.py` — tres tests:
   - default (sin clave) → skills instaladas contienen texto `feature-pr-dev` y **no** `{{BRANCHING_RULES}}`
   - config `solo-push-dev` → skills contienen texto `solo-push-dev`
   - con carpeta global fake (`Path.home` mockeado o patch): borra managed `sdd-draft-spec` (o un id del manifest) en global; **no** borra skill ajena (ej. `other-skill`)
7. `sdd.config.example.yaml` — bajo `agent:` documentar `branching_mode: feature-pr-dev  # feature-pr-dev | solo-push-dev`
8. `core/agent-setup.md` — un párrafo: install escribe en `.cursor/skills` del proyecto; borra `sdd-*` del manifest en `~/.cursor/skills`; precedencia **instancia > global**
9. `profiles/sdd-kit/checklist-stack.md` — un ítem: tras `install-agents`, no deben quedar skills del manifest en `~/.cursor/skills`

**No editar:** `core/branching.md`, otras skills, Claude/Codex/Copilot, gap #7.

### Implementación mínima en `install-agents.py`

- Lector YAML mínimo (mismo estilo que `read_dev_branch`: parseo por líneas, sin PyYAML nuevo): buscar línea `branching_mode:` bajo bloque `agent` o en cualquier nivel si el archivo es pequeño; aceptar valores entre comillas o sin ellas.
- Mapa constante de fragmentos (strings literales del Congelado).
- Función `remove_global_managed_skills(managed_ids: set[str]) -> None`.

### Prohibido

- Explorar / editar skills distintas de build-spec y open-pr.
- Instalar skills en el home del usuario.
- Cambiar `core/branching.md`.
- Ampliar a gap #7 u otros gaps dogfood.
- Leer más de ~15 archivos fuera de la lista cerrada + spec + domain-rules.
- Añadir dependencia PyYAML u otra librería externa.

### Sensor post-cambio (implementador)

```text
rg "{{BRANCHING_RULES}}" bootstrap/agent-skills/sdd-build-spec bootstrap/agent-skills/sdd-open-pr
```

→ ≥1 hit en cada uno de estos 4 archivos: `sdd-build-spec/SKILL.md`, `sdd-build-spec/reference.md`, `sdd-open-pr/SKILL.md`, `sdd-open-pr/reference.md`.

```text
rg "branching_mode|BRANCHING_RULES|remove_global|Path.home" bootstrap/install-agents.py
```

→ hits de las funciones / usos nuevos.

```text
python -m pytest bootstrap/test_install_skills.py -q
```

→ verde.

```text
python cli/sdd.py validate
```

→ 0 errores (si tocó docs de instancia; en build del producto kit tras merge documental).

---

## Impacto técnico

Perfil stack: `sdd-kit` ([`profiles/sdd-kit/spec-impact.md`](../../../../profiles/sdd-kit/spec-impact.md)).

| Pregunta                                                              | Respuesta |
| --------------------------------------------------------------------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)?                        | Sí (menor) — párrafo en `core/agent-setup.md`. **No** editar `core/branching.md` |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)?     | Sí (menor) — 1 ítem en `profiles/sdd-kit/checklist-stack.md` |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | Sí — `install-agents.py`, skills build-spec/open-pr, tests |
| ¿Afecta `cli/` (comandos, librerías)?                                 | No aplica — sin cambios CLI |
| ¿Afecta `.github/workflows/` o reglas Cursor?                         | No aplica — skills on-demand, no reglas always-on nuevas |
| ¿Requiere actualizar `README.md` o `INSTALL.md`?                      | No aplica — basta `agent-setup` + example config |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)?                   | Sí (proceso) — este spec + BACKLOG + `ids.next_sdd` |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles.   | Cumple bootstrap/CLI (Python 3.10+, sin deps nuevas). Sin cambio al archivo domain-rules |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR.          | No — contrato de install + plantillas de skills; no ADR |

---

## Reglas de negocio

Aplica [`.github/docs/business/domain-rules.md`](../../../business/domain-rules.md):

- **Bootstrap/CLI** — Python 3.10+; sin dependencias externas nuevas (parseo YAML mínimo como `read_dev_branch`).
- **DR-1** Core agnóstico — no meter política `solo-push-dev` en `core/branching.md`; el override vive en config de instancia + skills renderizadas.
- **DR-4** El agente ejecuta; el humano aprueba — push/PR solo tras confirmación humana; override del modo también exige frase explícita del humano.

Particularidad: precedencia instancia > global es contrato de harness Cursor, no de negocio de consumidores.

---

## Criterios de aceptación

**Happy path:**

- [x] Sin `branching_mode` en config: install renderiza fragmento `feature-pr-dev`; skills del proyecto no contienen `{{BRANCHING_RULES}}`.
- [x] Con `agent.branching_mode: solo-push-dev`: skills build-spec/open-pr instaladas contienen el fragmento `solo-push-dev` (incl. aviso si piden open-pr o feature/* + override con confirmación).
- [x] Con `feature-pr-dev` explícito: fragmento exige rama tipada + PR a `{{DEV_BRANCH}}` resuelto, más cláusula de override humano con confirmación escrita.
- [x] Tras install, IDs del manifest no existen bajo `~/.cursor/skills` (si existían, se borraron con log).
- [x] Skill no gestionada en `~/.cursor/skills` permanece.
- [x] `sdd.config.example.yaml` documenta `branching_mode`.
- [x] `core/agent-setup.md` documenta precedencia instancia > global + borrado de managed en home.
- [x] Checklist `sdd-kit` incluye ítem de verificación post-install sobre globals.
- [x] Sensores Congelado en verde (`rg` + `pytest`).

**Error path:**

- [x] `agent.branching_mode: foobar` → install falla con mensaje que cita la clave y `solo-push-dev` / `feature-pr-dev`; no deja skills a medias si el fallo es antes de escribir (o documentar: validar modo **antes** de escribir skills).
- [x] Diff que edite `core/branching.md` o skills fuera de la lista → fuera de alcance; rechazar.
- [x] Diff que reinstale skills en `~/.cursor/skills` → fuera de alcance; rechazar.

---

## Cambio de BD _(solo si incluye `db-change`)_

No aplica — sin BD.

---

## Diseño técnico

| Archivo | Cambio |
| ------- | ------ |
| `bootstrap/install-agents.py` | Leer modo; mapear a `BRANCHING_RULES`; limpiar globals managed |
| Skills build-spec / open-pr (4 archivos) | Insertar `{{BRANCHING_RULES}}` |
| `bootstrap/test_install_skills.py` | 3 tests Congelado |
| `sdd.config.example.yaml` | Documentar clave |
| `core/agent-setup.md` | Párrafo precedencia |
| `profiles/sdd-kit/checklist-stack.md` | 1 ítem |

Flujo:

```text
install_cursor_skills
  → read_branching_mode (default feature-pr-dev | fail si inválido)
  → render skills proyecto con BRANCHING_RULES
  → remove_global_managed_skills(manifest ids)
```

---

## Verificación técnica

```bash
rg "{{BRANCHING_RULES}}" bootstrap/agent-skills/sdd-build-spec bootstrap/agent-skills/sdd-open-pr
rg "branching_mode|BRANCHING_RULES|remove_global|Path.home" bootstrap/install-agents.py
python -m pytest bootstrap/test_install_skills.py -q
python -m compileall -q cli/ bootstrap/install-agents.py
python cli/sdd.py validate
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Borrar skill global que el humano quería conservar | Media | Medio | Solo IDs del manifest; log claro; documentar en agent-setup |
| Parseo YAML frágil (comentarios / indent) | Baja | Medio | Misma estrategia que `read_dev_branch`; test con línea simple |
| Cursor sigue cacheando skill global adjuntada a mano | Baja | Bajo | Reinstall + no adjuntar skill global; texto en agent-setup |
| Consumidor sin clave asume feature-pr-dev (cambio vs expectativa solo-push implícita) | Media | Medio | Default alineado a `core/branching.md`; documentar en release minor |

**Rollback:** revertir commit del SDD; reinstalar agents con kit anterior.

---

## Notas post-implementación

- Mencionar en `docs/releases/v1.5.0.md`: clave `agent.branching_mode`, default `feature-pr-dev`, borrado de skills managed en `~/.cursor/skills`.
- Gap #7 (`STACK_PROFILE`) sigue en Discovery; no mezclar.
- **Smoke manual:** diferido — probar en instancia consumidora externa (crear `~/.cursor/skills/sdd-open-pr` fake → `install-agents` → confirmar borrado global + texto de modo en skills del repo). No bloquea commit en el kit.
- **Nota implementación:** `update_sdd_config` preserva `branching_mode` al reescribir el bloque `agent`.
