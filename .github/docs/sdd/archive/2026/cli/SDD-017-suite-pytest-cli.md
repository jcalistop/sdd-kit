# SDD-017 — Suite pytest para la CLI (backlog, prompts, round-trip)

> Copiar desde plantilla core. Al cerrar: `git mv` a `archive/<YYYY>/cli/`.

---

## Cabecera

| Campo                 | Valor        |
| --------------------- | ------------ |
| **ID**                | `SDD-017`    |
| **Dominio**           | `cli`        |
| **Tipo**              | `feature`    |
| **Fecha**             | 2026-09-05   |
| **Estado**            | `Released`   |
| **Versión objetivo**  | `v1.4.0`     |
| **Owner**             | mantenedor kit |
| **Prioridad**         | `P1`         |
| **ADRs relacionados** | —            |
| **Dependencias**      | — (audita H-B01; fila Discovery cli) |

---

## Problema y objetivo

**Problema:**

La CLI (`cli/sdd.py` + `cli/lib/`) solo se valida en CI con `python -m compileall`. No hay suite automatizada de comportamiento: regresiones en parseo de BACKLOG, catálogo de prompts o el flujo `spec new` → fila Draft pasan desapercibidas hasta uso manual. La auditoría general (H-B01) lo marcó como P1.

**Objetivo:**

Añadir una suite **pytest** enfocada en `backlog`, `prompt list`/`show` y un **round-trip** de `spec new` sobre un directorio SDD temporal, integrada en CI del kit, sin depender de red ni de `gh`, y documentada en `cli/README.md`.

---

## Alcance

**Incluye:**

- Layout de tests (p. ej. `cli/tests/` o `tests/cli/`) con fixtures que construyen una mini-instancia SDD en `tmpdir`.
- Casos pytest para:
  - **backlog:** listar / filtrar por estado o dominio sobre BACKLOG de fixture.
  - **prompts:** `prompt list` y `prompt show <id>` (salida no vacía / id conocido del catálogo del kit).
  - **round-trip:** `spec new` crea archivo en `specs/<dominio>/` y fila coherente en BACKLOG Draft.
- Paso en `.github/workflows/ci.yml` que ejecute pytest (tras instalar pytest en el job).
- Nota breve en `cli/README.md` (cómo correr tests).
- Actualizar quality gate / checklist del perfil `sdd-kit` si aplica (`compile` + `pytest`).

**Excluye explícitamente:**

- Tests de `backlog sync` contra GitHub real (mocks opcionales fuera de MVP).
- Suite E2E de `validate-sdd` / `sdd validate` shell (fila Discovery **infra**).
- Higiene `sdd-core.mdc`, paridad multi-agente, perfiles nuevos.
- Dependencias Python **runtime** nuevas para consumidores del kit (pytest solo en CI/dev del repo productor).
- Campaña completa v1.4.0 (otros SDD pueden sumarse; este spec solo aporta la suite).

---

## Impacto técnico

Perfil: [`profiles/sdd-kit/spec-impact.md`](../../../../profiles/sdd-kit/spec-impact.md).

| Pregunta | Respuesta |
| -------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)? | No aplica — solo tooling CLI/CI |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)? | Sí (menor) — gate `pytest` en checklist / quality_gates de `sdd-kit` si se acuerda |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | No aplica |
| ¿Afecta `cli/` (comandos, librerías)? | Sí — tests + helpers/fixtures |
| ¿Afecta `.github/workflows/` o reglas Cursor? | Sí — step pytest en CI; no reglas Cursor |
| ¿Requiere actualizar `README.md` o `INSTALL.md`? | Sí (menor) — `cli/README.md`; INSTALL solo si se documenta dep dev |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)? | Sí (proceso) — este spec + BACKLOG; quality_gates opcionales en config |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles. | No cambia el texto; aplica DR-1, DR-4, DR-6, DR-7 |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR. | No |

---

## Reglas de negocio

Aplica [`.github/docs/business/domain-rules.md`](../../business/domain-rules.md):

- **DR-1:** tests no introducen menciones de stack de apps en `core/`.
- **DR-4:** implementación tras Ready; verify antes de push/PR.
- **DR-6:** spec y BACKLOG solo bajo `paths.sdd`.
- **DR-7:** al cerrar campaña **v1.4.0**, dual-release (nota producto + acta).

Particularidad: pytest es dependencia de **desarrollo/CI del kit**, no requisito de instalación del consumidor.

---

## Criterios de aceptación

**Happy path:**

- [x] Existe suite pytest ejecutable desde la raíz del repo (comando documentado).
- [x] Al menos un test de `backlog` pasa sobre fixture.
- [x] Al menos un test de `prompt list` y uno de `prompt show` pasan.
- [x] Round-trip: `spec new` en tmpdir deja spec + fila Draft verificables.
- [x] CI ejecuta pytest en verde en el job `validate` (o job dedicado).
- [x] `cli/README.md` documenta cómo correr los tests.
- [x] `python cli/sdd.py validate` sigue en verde sobre la instancia del kit.

**Error path:**

- [x] Test o assertion falla de forma clara si el BACKLOG de fixture está malformado (no crash opaco sin mensaje).
- [x] `prompt show` de id inexistente: comportamiento actual documentado o test de código de salida / mensaje (sin romper la suite).

---

## Cambio de BD

No aplica — sin esquema de aplicación.

---

## Diseño técnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `cli/tests/` (o `tests/cli/`) | Nuevos tests + `conftest.py` |
| `.github/workflows/ci.yml` | Step `pytest` (+ install) |
| `cli/README.md` | Sección tests |
| `profiles/sdd-kit/checklist-stack.md` y/o `sdd.config.yaml` | Gate pytest opcional pero recomendado |
| `requirements-dev.txt` o equivalente | Si se formaliza dep pytest |

**Notas de diseño:**

- Preferir invocar funciones de `cli/lib/*` o subprocess a `cli/sdd.py` con `cwd`/env `SDD_PATH` apuntando al tmpdir.
- Fixtures mínimas: `BACKLOG.md`, `sdd.config.yaml`, plantilla spec si `spec new` la requiere.
- No requerir red.

---

## Verificación técnica

```bash
python -m compileall -q cli/
python -m pytest cli/tests -q   # o ruta acordada en implementación
python cli/sdd.py validate
```

CI: mismo pytest en `.github/workflows/ci.yml`.

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Acoplar tests a formato frágil de BACKLOG | Media | Media | Fixtures pequeñas; asertar comportamiento estable |
| pytest no disponible en runners locales de mantenedores | Baja | Baja | Documentar install; CI es gate canónico |
| Ampliar alcance a sync/validate-sdd | Media | Baja | Exclusiones explícitas; no mezclar con infra Discovery |

**Rollback:** revertir commit de tests/CI; CLI runtime sin cambio obligatorio.

---

## Notas post-implementación

- Enlazar H-B01 del informe de auditoría al cerrar release v1.4.0.
- Evaluar en campaña posterior: mocks de `gh` / validate-sdd en CI (otros ítems Discovery).
- **Smoke manual (2026-09-05):** humano confirmó exitoso — `pip install -r requirements-dev.txt` + `python -m pytest cli/tests -q` (8 passed) y revisión del step CI.
- **2026-09-05 (close-release):** Campaña `v1.4.0`; archivado en `archive/2026/cli/`.
