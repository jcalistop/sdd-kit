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

Retrospectiva de sesión (2026-09-10): el ciclo validó harness + skills; los gaps de producto del kit están abajo (prioridad sugerida: Pint=CI → branching install → Draft congelado → quality gates explícitos).

## Resultados por paso

| Paso | Resultado | Evidencia |
| ---- | --------- | --------- |
| 0 Consumidor | OK | Repo `minsal-centinela`; `stack.profile: laravel-voyager`; `agent.targets: [cursor]`; rama `dev` |
| 1 Baseline / validate | OK | Submodule en tag `v1.4.1`; `sdd validate` OK; `installed_version` alineado post-upgrade |
| 2 Ciclo SDD mínimo | **OK** | Spec consumidor: `.github/docs/sdd/specs/metas/SDD-231-metas-objetivo-indicador-texto-enriquecido.md`. Ciclo Discovery→Draft→Ready→In Build→verify→commit→PR. PR [#172](https://github.com/jcalistop/minsal-centinela/pull/172) merge `aff4ae9` (2026-09-10). Smoke OK. CI: primer run falló Pint (`pint --test`); corregido en `c201fd2` antes del merge (ver Gaps). |
| 3 Upgrade | OK | Salto v1.3.1→v1.4.1 vía skill upgrade-kit; commits consumidor de bump + merge instancia; fila en `UPGRADE-LOG.md` |
| 4 Evidencia en kit | OK | Este informe actualizado (paso 2 → OK + hallazgos de retrospectiva); plan con fecha de cierre 2026-09-10; rama kit `docs/dogfood-centinela-20260908`; pin consumidor sigue en tag `v1.4.1` |

## Gaps / follow-ups

| # | Hallazgo | Acción sugerida | SemVer | Prio |
| - | -------- | --------------- | ------ | ---- |
| 1 | **verify-implementation en verde no implica Pint CI en verde.** En SDD-231 el sensor local pasó (`pint --dirty` + tests acotados + `validate`), pero el PR [#172](https://github.com/jcalistop/minsal-centinela/pull/172) falló en CI con `vendor/bin/pint --test` (4 archivos: `ObjetivoHtml`, form Livewire, tests). Fix: commit `c201fd2`. Causa probable: `--dirty` / alcance incompleto vs `--test` en el árbol tocado, o estilo no re-chequeado tras últimos edits antes del push. | Endurecer `verify-implementation` + checklist `laravel-voyager`: exigir el **mismo comando que CI** (`vendor/bin/pint --test`, o paths PHP del diff del spec) **antes** de open-pr; documentar en checklist PR / skill build-spec. | patch (prompts/skills/checklist) | P0 |
| 2 | **Skills globales vs instancia (branching).** Skills en `~/.cursor/skills` (modo «desarrollador solo») asumen commits/push directo a `origin/dev` y prohíben `feature/*`. Centinela (`branching.md` + skills del repo) exige feature → PR a `dev`. En la sesión chocaron; el humano pidió rama nueva a pesar del skill global. | `install-agents`: precedencia **instancia > global**; skills bootstrap con `{{BRANCHING_MODE}}` (`solo-push-dev` \| `feature-pr-dev`) leído de `branching.md` / config. | minor (contrato install + plantillas) | P0 |
| 3 | **Specs flojos para LLM de bajo contexto.** El Draft inicial pasaba DoR humano pero dejaba decisiones abiertas (Trix\|TipTap, API vaga, tests `...`). Hubo que enmendar el Draft congelando Quill, allowlist, API `ObjetivoHtml`, paths de test y lista de lectura. | En `draft-spec` / plantilla / DoR: sección opcional **«Congelado para implementación»** (decisión única, API, paths de test, lectura máx. N archivos, «prohibido explorar»). | patch (docs + skill draft) | P1 |
| 4 | **verify no nombra quality gates del perfil.** El skill dice «quality gates en verde» sin comando concreto por stack. Casi se deshizo el pin `quill@2.0.2` (GHSA-v3m3-f69x-jf25 / `npm audit`) como «accidental». | Tabla en skill/prompt verify: perfil → comandos obligatorios (Pint alineado a CI, tests filtrados, `npm audit` si tocó `package.json`, etc.). | patch (perfil + verify) | P1 |
| 5 | **Informe dogfood vive en rama post-tag.** El stub en el árbol del tag `v1.4.1` sigue «Pendiente / no ejecutado» mientras la fuente de verdad es esta rama docs. | Runbook dogfood: el stub del tag no es fuente de verdad post-corrida; checklist merge informe → `main` (o próximo patch) al cerrar. | patch docs audits | P2 |
| 6 | **Ritmo Discovery / build en auditorías.** El agente intentó cerrar solo un ciclo documental throwaway; el humano frenó y guió desde historia de usuario (correcto). Planes «ciclo completo» no deben saltar Ready sin frase humana. | Reforzar en `build-spec` / dogfood: si el humano dice «te guío» o hay Plan mode, no pasar a Ready/In Build sin aprobación explícita (ya implícito en workflow; hacer fail-closed). | patch (skills) | P2 |
| 7 | **Skills adjuntas con perfil hardcodeado equivocado.** Un `sdd-build-spec` desde `~/.cursor` citaba `sdd-stack-reports-latex-md` en un consumidor `laravel-voyager`. | Skills con `{{STACK_PROFILE}}` resuelto en install; nunca hardcodear otro perfil en el skill global. | patch (bootstrap skills) | P2 |
| 8 | Quill `=2.0.3` (GHSA-v3m3-f69x-jf25) | Mitigado en consumidor con pin `quill@2.0.2` (fuera del kit; evidencia de por qué verify debe mencionar `npm audit` cuando hay JS). | — | — |

### Qué funcionó bien (no gap)

- DoR → enmienda bajo contexto → build guiado.
- Exclusiones explícitas (no TinyMCE Voyager) evitaron deuda T3 / strangler.
- Separación consumidor vs productor (SDD-NNN solo en Centinela; kit solo informe).
- Cost governance + safe-git no estorbaron el ciclo.

## Conclusión

**OK.** Dogfood consumidor externo contra `v1.4.1` cerrado: baseline, upgrade y ciclo SDD mínimo (Draft→verify→PR a `dev`) sin bloqueos del kit. Gaps de harness priorizados: (1) Pint=`CI`, (2) modo branching en install, (3) bloque «congelado» en Draft, (4) quality gates explícitos + `npm audit` si hay JS.
