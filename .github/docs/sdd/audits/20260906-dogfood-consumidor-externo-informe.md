# Informe — Dogfood consumidor externo

| Campo | Valor |
| ----- | ----- |
| **Estado** | **Ejecutado** (cierre completo) |
| **Fecha** | 2026-09-08 (baseline/upgrade); **2026-09-10** (paso 2 ciclo SDD) |
| **Plan** | [20260906-dogfood-consumidor-externo.md](20260906-dogfood-consumidor-externo.md) |
| **Tag kit** | `v1.4.1` (`a52576b`) |
| **Consumidor** | `minsal-centinela` · perfil `laravel-voyager` · rama `dev` · paths `.github/docs/sdd` + submodule `.github/docs/sdd-kit` |

> Corrida post-tag `v1.4.1`: upgrade + baseline (2026-09-08) y ciclo SDD mínimo Discovery→PR mergeado a `dev` (2026-09-10). Pin del consumidor **permanece** en `v1.4.1`.

---

## Resumen ejecutivo

El consumidor Centinela actualizó el submodule a `v1.4.1`, portó el delta core del salto, reinstaló adaptadores Cursor (`laravel-voyager`) y dejó `kit.installed_version: "v1.4.1"` con `validate` en verde (2026-09-08). El **2026-09-10** se completó el follow-up del paso 2: ciclo SDD de punta a punta en el consumidor con **SDD-231** (feature Metas: objetivo enriquecido con Quill + HTML allowlist), verify-implementation OK, smoke manual OK, PR [#172](https://github.com/jcalistop/minsal-centinela/pull/172) mergeado a `dev` (`aff4ae9`). Sin bloqueos atribuibles al kit. No se creó SDD-NNN ni BACKLOG dentro del repo productor `sdd-kit`.

## Resultados por paso

| Paso | Resultado | Evidencia |
| ---- | --------- | --------- |
| 0 Consumidor | OK | Repo `minsal-centinela`; `stack.profile: laravel-voyager`; `agent.targets: [cursor]`; rama `dev` |
| 1 Baseline / validate | OK | Submodule en tag `v1.4.1`; `sdd validate` OK; `installed_version` alineado post-upgrade |
| 2 Ciclo SDD mínimo | **OK** | Spec consumidor: `.github/docs/sdd/specs/metas/SDD-231-metas-objetivo-indicador-texto-enriquecido.md`. Ciclo Discovery→Draft→Ready→In Build→verify→commit→PR. PR [#172](https://github.com/jcalistop/minsal-centinela/pull/172) merge `aff4ae9` (2026-09-10). Smoke + Pint CI OK. |
| 3 Upgrade | OK | Salto v1.3.1→v1.4.1 vía skill upgrade-kit; commits consumidor de bump + merge instancia; fila en `UPGRADE-LOG.md` |
| 4 Evidencia en kit | OK | Este informe actualizado (paso 2 → OK); plan con fecha de cierre 2026-09-10; rama kit `docs/dogfood-centinela-20260908`; pin consumidor sigue en tag `v1.4.1` |

## Gaps / follow-ups

| Hallazgo | Acción sugerida | SemVer |
| -------- | --------------- | ------ |
| Informe vive en rama kit post-tag | Merge a `main` del kit (o incluir en próximo patch) para que el stub de `v1.4.1` deje de figurar pendiente | patch docs |
| Quill `=2.0.3` (GHSA-v3m3-f69x-jf25) | Mitigado en consumidor con pin `quill@2.0.2` (fuera del kit) | — |

## Conclusión

**OK.** Dogfood consumidor externo contra `v1.4.1` cerrado: baseline, upgrade y ciclo SDD mínimo (Draft→verify→PR a `dev`) sin bloqueos del kit.
