# Informe — Dogfood consumidor externo

| Campo | Valor |
| ----- | ----- |
| **Estado** | **Ejecutado** |
| **Fecha** | 2026-09-08 |
| **Plan** | [20260906-dogfood-consumidor-externo.md](20260906-dogfood-consumidor-externo.md) |
| **Tag kit** | `v1.4.1` (`a52576b`) |
| **Consumidor** | `minsal-centinela` · perfil `laravel-voyager` · rama `dev` · paths `.github/docs/sdd` + submodule `.github/docs/sdd-kit` |

> Corrida post-tag `v1.4.1`: upgrade consumidor v1.3.1 → v1.4.1 + smoke operativo (sin SDD throwaway).

---

## Resumen ejecutivo

El consumidor Centinela actualizó el submodule a `v1.4.1`, portó el delta core del salto (`upgrade-guide`, `agent-setup`, `workflow`, NEW `prompts/exceptions/upgrade-kit.md`), reinstaló adaptadores Cursor (`laravel-voyager`), retiró residuales `sdd-core.mdc` y `sdd-cost-governance`, y dejó `kit.installed_version: "v1.4.1"`. `python cli/sdd.py validate` → **0 errores, 0 advertencias**. El ciclo Draft→PR de feature nueva no se ejecutó a propósito (smoke + upgrade documentados; follow-up opcional).

## Resultados por paso

| Paso | Resultado | Evidencia |
| ---- | --------- | --------- |
| 0 Consumidor | OK | Repo `minsal-centinela`; `stack.profile: laravel-voyager`; `agent.targets: [cursor]`; rama `dev` |
| 1 Baseline / validate | OK | Submodule en tag `v1.4.1`; `sdd validate` OK (prefijos `[specs]`/`[config]`/`[agent]`); `installed_version` alineado post-upgrade |
| 2 Ciclo SDD mínimo | PARCIAL | Smoke: skills `sdd-*` del manifest reinstaladas; `centinela-informe-historico` intacta; checklist post-upgrade (safe-git `alwaysApply: true`; sin cost-governance; sin `sdd-core`). Sin Discovery→Draft→verify→PR de feature nueva |
| 3 Upgrade | OK | Salto v1.3.1→v1.4.1 vía skill upgrade-kit; commits consumidor `chore(sdd): bump sdd-kit submodule to v1.4.1` + `docs(sdd): merge instancia v1.4.1…`; fila en `UPGRADE-LOG.md` |
| 4 Evidencia en kit | OK | Este informe + plan marcado Ejecutado (rama kit `docs/dogfood-centinela-20260908`; pin consumidor permanece en tag `v1.4.1`) |

## Gaps / follow-ups

| Hallazgo | Acción sugerida | SemVer |
| -------- | --------------- | ------ |
| Paso 2 sin ciclo Draft→verify→PR de feature | Opcional: dogfood con SDD documental mínimo en un consumidor en sesión dedicada | — |
| Informe vive en rama kit post-tag | Merge a `main` del kit (o incluir en próximo patch) para que el stub deje de figurar pendiente en el árbol `v1.4.1` | patch docs |

## Conclusión

**OK con matiz.** Upgrade y baseline validate del consumidor externo contra `v1.4.1` sin bloqueos del kit. Criterio de cierre del plan cumplido vía upgrade + smoke + follow-up explícito del ciclo Draft completo.
