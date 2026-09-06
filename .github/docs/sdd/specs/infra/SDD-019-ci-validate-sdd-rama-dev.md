# SDD-019 — CI: `sdd validate` y gatillo en rama `dev`

> Copiar desde plantilla core. Al cerrar: `git mv` a `archive/<YYYY>/infra/`.

---

## Cabecera

| Campo                 | Valor        |
| --------------------- | ------------ |
| **ID**                | `SDD-019`    |
| **Dominio**           | `infra`      |
| **Tipo**              | `feature`    |
| **Fecha**             | 2026-09-05   |
| **Estado**            | `In Build`   |
| **Versión objetivo**  | `v1.4.1`     |
| **Owner**             | mantenedor kit |
| **Prioridad**         | `P2`         |
| **ADRs relacionados** | —            |
| **Dependencias**      | — (audita H-B02/H-B03/H-C02; ADOPTION Etapa 3; paralelo a SDD-018 en misma campaña) |

---

## Problema y objetivo

**Problema:**

El workflow [`.github/workflows/ci.yml`](../../../../.github/workflows/ci.yml) solo se dispara en `main` y no ejecuta el sensor documental SDD (`validate-sdd` / `python cli/sdd.py validate`), pese a que el sensor funciona en local (H-C01/C02) y `development_branch` es `dev`. Los PRs hacia `dev` y los pushes a desarrollo no reciben ese gate; ADOPTION Etapa 3 aún lista el job CI como pendiente (H-A07 / H-B02 / H-B03).

**Objetivo:**

Integrar `python cli/sdd.py validate` como step de CI (Linux) y ampliar los gatillos `push` / `pull_request` a la rama **`dev`** (manteniendo `main`), alineando quality gates del perfil `sdd-kit` y cerrando el ítem de ADOPTION Etapa 3 relativo al job.

---

## Alcance

**Incluye:**

- Step en `.github/workflows/ci.yml`: `python cli/sdd.py validate` (instancia `.github/docs/sdd`).
- `on.push` y `on.pull_request` con ramas `[main, dev]` (o equivalente explícito).
- Actualizar `quality_gates` / checklist del perfil `sdd-kit` si el gate CI aún no refleja validate en el workflow.
- Marcar o notar en [ADOPTION.md](../ADOPTION.md) Etapa 3 el job CI con validate.

**Excluye explícitamente:**

- Ampliar el sensor (H-C03 cruzar `ids.next_sdd` vs texto BACKLOG; índice audits/research).
- Cambiar lógica de `bootstrap/validate-sdd.ps1` / `.sh`.
- Tests de adaptadores no-Cursor (H-D08).
- Suite pytest adicional (ya SDD-017).
- Implementación de SDD-018 (higiene `sdd-core`) — campaña compartida, specs distintos.

---

## Impacto técnico

Perfil: [`profiles/sdd-kit/spec-impact.md`](../../../../profiles/sdd-kit/spec-impact.md).

| Pregunta | Respuesta |
| -------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)? | No aplica — solo CI/adopción dogfood |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)? | Sí (menor) — checklist / quality_gates si falta el step CI |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | No aplica — se invoca CLI existente, sin cambiar scripts |
| ¿Afecta `cli/` (comandos, librerías)? | No aplica — solo ejecución en CI |
| ¿Afecta `.github/workflows/` o reglas Cursor? | Sí — `ci.yml` |
| ¿Requiere actualizar `README.md` o `INSTALL.md`? | No aplica (opcional mención breve; no requerida) |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)? | Sí (proceso) — este spec + BACKLOG; quality_gates opcionales en config |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles. | No cambia el texto; aplica DR-4, DR-6, DR-7 |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR. | No |

---

## Reglas de negocio

Aplica [`.github/docs/business/domain-rules.md`](../../business/domain-rules.md):

- **DR-4** — humano aprueba Ready/merge; CI es sensor automatizado.
- **DR-6** — docs SDD en `paths.sdd`.
- **DR-7** — dual-release al cerrar `v1.4.1` (junto a SDD-018 u otros de la campaña).

Particularidad: el sensor ya existe; este spec solo lo cablea a GitHub Actions y a `dev`.

---

## Criterios de aceptación

**Happy path:**

- [x] `ci.yml` incluye step que ejecuta `python cli/sdd.py validate` (exit ≠ 0 falla el job).
- [x] `on.push` y `on.pull_request` incluyen rama `dev` además de `main`.
- [x] Checklist / `quality_gates` del perfil `sdd-kit` reflejan validate en CI (si aplica).
- [x] ADOPTION Etapa 3: ítem del job CI `validate-sdd` marcado o actualizado como cubierto.
- [x] Corrida local `python cli/sdd.py validate` sigue en verde.
- [x] CI verde en un push/PR de prueba a `dev` o evidencia equivalente tras merge del cambio.

**Error path:**

- [x] Incoherencia documental SDD que hoy hace fallar validate en local también falla el job CI (exit no cero).
- [x] WARN de kit-version (pre-tag) no se convierte en requisito nuevo de fallar el job si hoy el CLI sale 0 con WARN — documentar comportamiento actual.

---

## Cambio de BD

No aplica — sin esquema de aplicación.

---

## Diseño técnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `.github/workflows/ci.yml` | Step validate + branches `dev` |
| `profiles/sdd-kit/checklist-stack.md` y/o `sdd.config.yaml` | Gate CI si falta |
| `.github/docs/sdd/ADOPTION.md` | Etapa 3 job CI |

**Notas de diseño:**

- Preferir CLI Python en ubuntu-latest; no invocar `.ps1`.
- Alternativa equivalente: `bash bootstrap/validate-sdd.sh` con `-SddPath` si la CLI requiere cwd distinto — preferir la misma invocación que mantenedores usan en local (`python cli/sdd.py validate`).

---

## Verificación técnica

```bash
python cli/sdd.py validate
# Tras push: Actions en verde para evento en dev
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| CI falla por deuda documental no vista en local | Baja | Medio | Correr validate antes de push; fix docs |
| Doble costo de runner en PRs main+dev | Baja | Bajo | Aceptable; mismo job |
| Confundir WARN kit-version con error | Baja | Bajo | Documentar: exit 0 con WARN no bloquea |

**Rollback:** revertir cambios en `ci.yml` (y notas ADOPTION/checklist).

---

## Notas post-implementación

- Enlazar H-B02 / H-B03 / H-C02 / H-A07 al cerrar `v1.4.1`.
- No mezclar con ampliación del sensor (H-C03).
- **2026-09-05 (In Build):** step `python cli/sdd.py validate` + gatillos `dev`/`main`; ADOPTION Etapa 3 marcado; quality_gates/checklist actualizados. Criterio CI verde en remoto pendiente de push/smoke humano.
- **Smoke manual (2026-09-05):** humano confirmó exitoso (step CI / gatillos `dev`).
- **2026-09-05 (CI fix):** falló en GitHub por `PermissionError` al ejecutar `validate-sdd.sh` sin +x; CLI ahora invoca `bash …/validate-sdd.sh` y el `.sh` queda mode `100755`.
