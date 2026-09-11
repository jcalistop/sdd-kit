# Release campaña v1.5.0 — Branching install + Pint CI parity

## Cabecera

| Campo                | Valor                                               |
| -------------------- | --------------------------------------------------- |
| **Versión**          | **`v1.5.0`**                                        |
| **Fecha cierre**     | 2026-09-10                                          |
| **Tipo**             | minor                                               |
| **Responsable**      | mantenedor                                          |
| **Campaña anterior** | [v1.4.1](../v1.4.1/release_v1.4.1.md)               |
| **Changelog kit**    | [v1.5.0.md](../../../../../docs/releases/v1.5.0.md) |

---

## Información general

Minor post-dogfood Centinela: (1) contrato `agent.branching_mode` + precedencia skills instancia > global en `install-agents`; (2) paridad Pint verify ↔ CI en perfiles Voyager/Filament. Incluye cierre documental del dogfood (audits) ya mergeado en `dev` desde `v1.4.1`.

---

## Specs incluidas

| ID      | Dominio   | Spec archivado |
| ------- | --------- | -------------- |
| SDD-022 | profiles  | [archive/2026/profiles/SDD-022-pint-parity-ci-laravel.md](../../archive/2026/profiles/SDD-022-pint-parity-ci-laravel.md) |
| SDD-023 | bootstrap | [archive/2026/bootstrap/SDD-023-install-agents-branching-precedencia.md](../../archive/2026/bootstrap/SDD-023-install-agents-branching-precedencia.md) |

## Cambios sin spec

| Dominio | Cambio |
| ------- | ------ |
| docs    | Dogfood consumidor externo Centinela: plan + informe + hallazgos retrospectiva (gaps priorizados) — SemVer cubierto por SDD-022/023 |
| —       | ID `—` en commits docs audits post-tag v1.4.1 |

---

## Validación de cierre

| Gate           | Resultado                                                 |
| -------------- | --------------------------------------------------------- |
| `sdd validate` | 0 errores (WARN kit-version pre-tag posible)              |
| pytest         | `bootstrap/test_install_skills.py` + `cli/tests` verde    |
| Tag producto   | `v1.5.0` (pendiente push `dev` / merge a main / confirmación humana) |

---

## Pendientes post-release (no bloquean)

| Ítem | Origen | Nota |
| ---- | ------ | ---- |
| Smoke SDD-023 en instancia externa | SDD-023 notas | Diferido a propósito |
| Congelado DoR genérico | Discovery gap #3 | patch |
| Tabla verify multi-stack + npm audit | Discovery gap #4 | patch |
| `{{STACK_PROFILE}}` en skills | Discovery gap #7 | patch |
| build-spec fail-closed Plan mode | Discovery gap #6 | patch |
| Runbook dogfood stub tag | Discovery gap #5 | patch |

---

## Consumidores

Instancias en `v1.4.1` → `v1.5.0`: ver [`docs/releases/v1.5.0.md`](../../../../../docs/releases/v1.5.0.md). Reinstalar agents obligatorio si usan Cursor skills (branching + limpieza global).
