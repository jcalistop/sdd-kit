# Auditoría — Dogfood ciclo SDD en consumidor externo

| Campo | Valor |
| ----- | ----- |
| **Estado** | **Ejecutado** (cierre completo 2026-09-10) |
| **Fecha plan** | 2026-09-06 |
| **Fecha corrida** | 2026-09-08 (pasos 0–1, 3–4 parcial); **2026-09-10** (paso 2 + evidencia final) |
| **SemVer kit** | `—` (no define release; gaps productizados → SDD / ID `—` aparte) |
| **Sin SDD-NNN** | Intencional — es auditoría operativa, no feature |
| **Informe** | [20260906-dogfood-consumidor-externo-informe.md](20260906-dogfood-consumidor-externo-informe.md) |
| **Consumidor** | `minsal-centinela` · `laravel-voyager` · `dev` |

---

## Objetivo

Validar en un proyecto **fuera** de `sdd-kit` que el ciclo SDD + upgrade/adaptadores funcionan de punta a punta contra el tag **`v1.4.1`**.

## Exclusiones

- No instalar Claude/Codex/Copilot en el repo kit.
- No crear perfiles nuevos ni SDD-022 por esta auditoría sola.
- No “arreglar todo” dentro de este documento: los gaps van a Discovery/specs.

## Prerrequisito

- [x] Tag `v1.4.1` publicado en `main`.
- [x] Repo consumidor elegido (nombre + perfil stack): `minsal-centinela` / `laravel-voyager`.

---

## Pasos (runbook)

### 0. Decidir consumidor
- Repo, stack (`profiles/<nombre>`), rama de desarrollo.

### 1. Baseline
- Submodule (o copia) en tag `v1.4.1`.
- `init-sdd` / `install-agents` si falta instancia.
- `python sdd-kit/cli/sdd.py validate` en verde.
- Anotar `kit.installed_version` y `agent.targets`.

### 2. Ciclo SDD mínimo (en el consumidor)
1. Discovery/Draft de un spec pequeño.
2. Ready → In Build.
3. Implementar + verify-implementation + smoke.
4. Commit / PR a la rama de desarrollo del consumidor.

**Hecho (2026-09-10):** SDD-231 en Centinela — spec `.github/docs/sdd/specs/metas/SDD-231-metas-objetivo-indicador-texto-enriquecido.md`; PR [#172](https://github.com/jcalistop/minsal-centinela/pull/172) mergeado a `dev` (`aff4ae9`).

### 3. Upgrade (si venía de tag anterior)
1. `upgrade-kit` a `v1.4.1`.
2. Reinstall según `agent.targets`.
3. Checklist post-upgrade (sin `sdd-core` / sin `cost-governance` huérfano).
4. `validate` otra vez.

### 4. Evidencia en sdd-kit
- Completar el **informe** hermano.
- Actualizar este plan → estado Ejecutado.
- Filas Discovery o SDD si hay gaps de producto.
- Actualizar [README.md](../README.md) tabla Audits si hace falta.

### 5. Criterio de cierre
- Ciclo Draft→verify (y PR) completado sin bloqueos del kit, **o** bloqueos documentados con follow-ups.
- Informe con OK/FAIL por paso.

---

## Referencias

- Informe auditoría general: [20260905-1202-auditoria-general-kit-informe.md](20260905-1202-auditoria-general-kit-informe.md)
- Nota producto: [`docs/releases/v1.4.1.md`](../../../../docs/releases/v1.4.1.md)
- BACKLOG Discovery (fila docs, SemVer —)
