# SDD-032 — Reestructurar README.md raíz (v1.3–v1.5 + rutas actuales)

> Copiar desde plantilla core. Al cerrar: `git mv` a `archive/<YYYY>/docs/`.

---

## Cabecera

| Campo                 | Valor                  |
| --------------------- | ---------------------- |
| **ID**                | `SDD-032`              |
| **Dominio**           | `docs`                 |
| **Tipo**              | `documentation`        |
| **Fecha**             | 2026-09-13             |
| **Estado**            | `In Build`             |
| **Versión objetivo**  | `v1.6.0` |
| **Owner**             | mantenedor kit         |
| **Prioridad**         | `P2`                   |
| **ADRs relacionados** | —                      |
| **Dependencias**      | Tras SDD-026/027/028 (audits/research) y SDD-029 (`core/guides/`); no bloquea cierre de esos specs |

---

## Problema y objetivo

**Problema:**

El contenido editorial del [`README.md`](../../../../README.md) raíz quedó anclado a **v1.2.0** (skills, navegación). Desde entonces el kit llegó a **v1.5.0** y solo se parchearon rutas a `core/guides/` (SDD-029). Faltan capacidades y contratos de v1.3–v1.5 (safe-git, dual-release, audits/research, CI `validate`, `branching_mode`); hay refs stale (`checklist-pr.md`, enlace destacado a `docs/releases/v1.2.0`); y `sdd metrics` aparece sin aclarar que es **salud del proceso** (no tokens — retirados en v1.3.2).

**Objetivo:**

Actualizar el README de producto **sin big rewrite**: conservar el esqueleto de onboarding, corregir rutas, y hacer descubribles harness/safe-git, dual-release, audits/research, validate en CI y `branching_mode`, alineado a rutas post-`core/guides/`.

---

## Alcance

**Incluye:**

1. **Navegación rápida** — añadir como máximo 3 filas: safe-git (`core/safe-git-contract.md`), mapa core (`core/README.md` y/o `core/guides/`), audits/research (una fila o dos compactas).
2. **Cómo trabajar con el agente** — mención explícita del contrato safe-git + `agent.branching_mode` (enlace a `core/guides/agent-setup.md` / upgrade v1.5).
3. **CLI** — aclarar que `metrics` mide salud del proceso SDD (no tokens); destacar `validate` (local + CI en `main`/`dev`).
4. **Archivos frecuentes** — paths correctos bajo `paths.sdd` implícito; checklist → `core/guides/checklist-pr.md`.
5. **Cómo está organizado** — una línea: raíz `core/` = contratos/entrada vs `core/guides/` = metodologías.
6. **Siguiente lectura / Mantenedores** — dual-release (producto `docs/releases/` ↔ acta `.github/docs/sdd/releases/`); bump enlace de versión a **v1.5.0**; audits/research como opcionales bajo `paths.sdd`.
7. Pasada de **enlaces rotos** relativos desde la raíz del kit.
8. **Wording:** reemplazar «codear» / «Codea» por «escribir código» / «escribe código» en el `README.md` raíz (p. ej. hero, idea en 30 s, tabla agente).

**Excluye explícitamente:**

- Reescribir `INSTALL.md`, `CONTRIBUTING.md` o notas en `docs/releases/`.
- Barrido global de «codear» fuera del `README.md` raíz (otros docs quedan fuera).
- Documentar en profundidad SDD-024/025/030/031 (no son day-1 del consumidor).
- Cambiar badges de stacks, emoji decorativos o el diagrama Mermaid.
- Traducir o acortar el onboarding «Empieza aquí» (salvo corrección factual).
- Reintroducir `metrics tokens` o `sdd-cost-governance`.
- Big rewrite / nuevo README desde cero.

---

## Impacto técnico

Perfil: [`profiles/sdd-kit/spec-impact.md`](../../../../profiles/sdd-kit/spec-impact.md).

| Pregunta | Respuesta |
| -------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)? | No aplica — solo enlaces hacia core ya existentes |
| ¿Afecta `profiles/<stack>/` (nuevo perfil o cambio de checklist)? | No aplica |
| ¿Afecta `bootstrap/` (init, validate, install-agents, agent-prompts)? | No aplica |
| ¿Afecta `cli/` (comandos, librerías)? | No aplica — wording del README sobre CLI existente |
| ¿Afecta `.github/workflows/` o reglas Cursor? | No aplica |
| ¿Requiere actualizar `README.md` o `INSTALL.md`? | Sí — solo `README.md` raíz; INSTALL fuera de alcance |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)? | Sí — este spec + fila BACKLOG |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles. | No cambia el texto; aplica DR-6 (spec en paths.sdd), DR-7 (README = producto) |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR. | No |

---

## Reglas de negocio

Aplica [`.github/docs/business/domain-rules.md`](../../business/domain-rules.md):

- **DR-6** — el spec vive en `paths.sdd`; no duplicar metodología SDD fuera de esa ruta.
- **DR-7** — README raíz es documentación de **producto**; dual-release y actas de campaña se enlazan, no se unifican carpetas.

---

## Criterios de aceptación

**Happy path:**

- [x] Un lector nuevo llega a install/adopción sin rutas rotas en el README.
- [x] Safe-git y audits/research son descubribles desde navegación rápida o «siguiente lectura».
- [x] Mantenedores: dual-release visible; enlace de versión destacado apunta a **v1.5.0** (no v1.2.0).
- [x] Sección CLI aclara que `metrics` = salud del proceso SDD (sin `metrics tokens`).
- [x] Mención de `validate` en CI (`main`/`dev`) y de `branching_mode` (o enlace claro).
- [x] `checklist-pr` enlaza a `core/guides/checklist-pr.md`.
- [x] Nota explícita contratos (`core/`) vs guías (`core/guides/`).
- [x] En el `README.md` raíz no quedan «codear» / «Codea» como verbo de implementación; se usa «escribir código» / «escribe código».
- [x] `python cli/sdd.py validate` en verde tras el cambio documental del spec/BACKLOG (y tras el edit del README en In Build).

**Error path:**

- [x] Ningún enlace interno del README apunta a paths pre-`core/guides/` inexistentes.
- [x] No se reintroduce `metrics tokens` ni `sdd-cost-governance`.
- [x] El esqueleto de secciones del README se conserva (no big rewrite).
- [x] No se exige barrido de «codear» fuera del README raíz.

---

## Congelado para implementación _(opcional)_

Omitido — alcance cerrado; un solo archivo de producto; sin API/código.

---

## Cambio de BD

No aplica.

---

## Diseño técnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `README.md` (raíz del kit) | Única superficie de implementación |
| `.github/docs/sdd/specs/docs/SDD-032-*.md` | Este spec |
| `.github/docs/sdd/BACKLOG.md` | Draft → estados posteriores |

**Notas de diseño:**

- Conservar orden: hero → nav → audiencia → idea → requisitos → empieza aquí → agente/skills → archivos → CLI → capas → siguiente lectura → mantenedores → legal.
- Solo filas/callouts/correcciones; máximo 3 filas nuevas en nav.
- `sdd metrics` permanece (salud proceso); aclarar wording — no eliminar del CLI ni del kit.
- Wording local: «codear»→«escribir código»; «Codea»→«escribe código» (solo README raíz).

---

## Verificación técnica

```bash
python cli/sdd.py validate
# En In Build: revisar enlaces relativos del README;
# grep -iE "metrics tokens|cost-governance|checklist-pr\.md|\bcodear\b|\bcodea\b" README.md
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Scope creep → big rewrite del README | Media | Medio | Exclusiones explícitas; conservar esqueleto |
| Confundir `metrics` con tokens | Baja | Bajo | Frase aclaratoria en sección CLI |
| Duplicar INSTALL o upgrade-guide | Baja | Bajo | Enlazar; no copiar runbooks |

**Rollback:** revertir diff de `README.md` y/o este spec.

---

## Notas post-implementación

- Origen: Discovery «Reestructurar README.md raíz…» (2026-09-12).
- Análisis de gaps: contenido anclado a v1.2; rutas guides ya OK post-SDD-029; gaps v1.3–v1.5 listados en plan Draft.
- **2026-09-13 (In Build):** `README.md` actualizado (nav +3, safe-git/`branching_mode`, CLI metrics/validate CI, checklist path, core vs guides, dual-release + v1.5.0, wording codear→escribir código). Spec + BACKLOG → In Build en `dev`.
- **Smoke manual (2026-09-13):** humano confirmó OK.
