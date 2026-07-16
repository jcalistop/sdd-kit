# SDD-013 — Observabilidad de tokens por spec (`sdd metrics tokens`)

---

## Cabecera

| Campo                 | Valor                                                                 |
| --------------------- | --------------------------------------------------------------------- |
| **ID**                | `SDD-013`                                                             |
| **Dominio**           | `cli`                                                                 |
| **Tipo**              | `feature`                                                             |
| **Fecha**             | 2026-07-15                                                            |
| **Estado**            | `Released`                                                            |
| **Versión objetivo**  | `v1.3.0`                                                              |
| **Owner**             | mantenedor                                                            |
| **Prioridad**         | `P1`                                                                  |
| **ADRs relacionados** | `ADR-002`                                                             |
| **Dependencias**      | SDD-010 (observabilidad por componente); SDD-012 (governance tokens)  |

---

## Problema y objetivo

**Problema:**

Ningún framework público de agent harness publica **per-task token accounting** (Harness Effect, arXiv:2607.06906 §4.4). Sin métricas por `SDD-NNN`, el token maxing es inobservable: no se sabe qué specs queman más tokens, si verify pasa al primer intento, ni si un outlier supera 2× el promedio del dominio. SDD-012 aporta governance (límites, scoping, circuit breaker) pero no telemetría automática.

Cursor no expone token counts por API; cualquier solución debe ser **heurística** (mensajes, tool calls, tamaños de archivo), no facturación exacta.

**Objetivo:**

Entregar `sdd metrics tokens` en la CLI y checks WARN en `validate-sdd` para estimar y reportar consumo por spec, formalizando el logging que `sdd-cost-governance` ya anticipa. Primer paso hacia observabilidad económica del harness SDD.

---

## Alcance

**Incluye:**

1. **`cli/lib/metrics.py`** (o extensión del módulo `metrics` existente):
   - `estimate_tokens(spec_id, …)` — heurística: mensajes, tool calls, tamaño de archivos leídos/escritos; retorna `estimated_input_tokens`, `estimated_output_tokens`, `estimated_total_tokens`, `confidence` (`low`/`medium`/`high`)
   - `format_token_report(specs)` — tabla: SDD-NNN, dominio, fase más cara, tokens est., verify 1er intento
   - Persistencia opcional en `.github/docs/sdd/metrics/token-usage.json` (o ruta `paths.sdd`/metrics/)

2. **`cli/sdd.py`** — subcomando `sdd metrics tokens`:
   - `sdd metrics tokens SDD-NNN`
   - `sdd metrics tokens --all`
   - `sdd metrics tokens --summary` (total, promedio, mediana, top consumer)
   - `--format json|table|text` (default: `table`)

3. **`validate-sdd.ps1` / `validate-sdd.sh`** — checks opcionales (WARN, no ERROR):
   - Specs Released sin entrada de token-usage → WARN
   - Spec con consumo >2× el promedio del dominio → WARN

4. **Contrato con `sdd-cost-governance`:** documentar el schema JSON de registro por fase y que CLI puede leerlo o estimarlo.

**Excluye explícitamente:**

- Integración con APIs de pricing de OpenAI/Anthropic/etc.
- Instrumentar el runtime de Cursor para counts reales
- Dashboard Canvas (sigue en Discovery como opcional)
- Cambiar el ciclo SDD o inventar nuevos estados

---

## Impacto técnico

| Pregunta                                                              | Respuesta |
| --------------------------------------------------------------------- | --------- |
| ¿Afecta `core/` (workflow, plantillas, guías)?                        | Mínimo — posible nota en workflow/governance apuntando a `sdd metrics tokens` |
| ¿Afecta `profiles/<stack>/`?                                          | No aplica — perfil `sdd-kit` solo si quality gates CLI lo requieren |
| ¿Afecta `bootstrap/`?                                                 | Posible — actualizar skill cost-governance con ruta de metrics; no obligatorio al inicio |
| ¿Afecta `cli/` (comandos, librerías)?                                 | Sí — `cli/lib/metrics.py`, `cli/sdd.py` |
| ¿Afecta `.github/workflows/` o reglas Cursor?                         | No aplica — CI puede llamar `sdd metrics` en el futuro, fuera de este spec |
| ¿Requiere actualizar `README.md` o `INSTALL.md`?                      | Sí — documentar subcomando en docs CLI / README del kit |
| ¿Afecta instancia SDD (BACKLOG, specs, sdd.config)?                   | Sí — directorio `metrics/` bajo `paths.sdd` |
| ¿Afecta reglas en `business/domain-rules.md`?                         | DR-1, DR-6, DR-7 (separación producto/proceso) |
| ¿Introduce decisión arquitectónica transversal?                       | No — métricas son observabilidad; no nuevo ADR |

---

## Reglas de negocio

Aplica [`domain-rules.md`](../../../business/domain-rules.md):

- **DR-1:** Estimadores y reportes sin acoplar a un IDE concreto en la API pública de la CLI.
- **DR-6:** Artefactos de métricas bajo `paths.sdd` (p. ej. `.github/docs/sdd/metrics/`).
- **DR-7:** Métricas de campaña ≠ release producto; no mezclar con `docs/releases/` salvo enlace documental.

---

## Criterios de aceptación

**Happy path:**

- [x] `sdd metrics tokens --summary` imprime tabla con al menos: SDD-NNN, dominio, tokens estimados, verify 1er intento (si hay datos)
- [x] `sdd metrics tokens SDD-NNN` y `--all` funcionan; `--format json` emite JSON válido
- [x] Heurística documentada (qué cuenta y qué no); `confidence` presente en salida JSON
- [x] Schema de `token-usage.json` documentado (compatible con lo anticipado en `sdd-cost-governance`)
- [x] `validate-sdd` emite WARN (no ERROR) si specs Released carecen de token-usage
- [x] `validate-sdd` emite WARN si un spec supera 2× el promedio del dominio (cuando hay ≥N muestras, N documentado)
- [x] `python -m compileall -q cli/` en verde
- [x] `python cli/sdd.py validate` sin errores

**Error path:**

- [x] Spec ID inexistente → mensaje claro, exit code ≠ 0
- [x] Sin datos de métricas → `--summary` reporta vacío o "sin datos" sin crash
- [x] Falta `metrics/` → WARN o creación opcional documentada, no ERROR hard de validate-sdd

---

## Diseño técnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `cli/lib/metrics.py` | Estimación + formateo (extender si ya existe) |
| `cli/sdd.py` | Subcomando `metrics tokens` |
| `bootstrap/validate-sdd.ps1` | WARN token-usage / outlier |
| `bootstrap/validate-sdd.sh` | Paridad con PowerShell |
| `.github/docs/sdd/metrics/` | Directorio + `.gitkeep` o README corto |
| `bootstrap/agent-skills/sdd-cost-governance/SKILL.md` | Enlace a schema/CLI (si aplica) |

**Heurística (orden de magnitud, no precisión):**

- Mensaje usuario ~200 tokens; asistente ~800 (ajustable)
- Tool Read/Write ~ `chars/4` del payload
- Ratio input/output alineado a Tokenomics (~54% / ~24% / ~22% reasoning) solo para desglose estimado
- `confidence: low` si no hay session log; `medium` con log parcial; `high` solo con datos ricos

---

## Verificación técnica

```text
python -m compileall -q cli/
python cli/sdd.py metrics tokens --summary
python cli/sdd.py metrics tokens --all --format json
python cli/sdd.py validate
# validate-sdd.ps1 / .sh — revisar WARN de metrics
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigación |
| ------ | ------------ | ------- | ---------- |
| Heurística engañosa (equipo confía en $ exactos) | Alta | Medio | Documentar "estimado"; `confidence`; no mostrar $ sin disclaimer |
| Falsa sensación de precisión vs Cursor real | Alta | Bajo | Mensaje en `--help` y research |
| WARN ruidoso en validate-sdd | Media | Bajo | WARN opt-in o umbral N mínimo de muestras |

**Rollback:** deshabilitar subcomando y checks WARN; dejar `metrics/` vacío.

---

## Notas post-implementación

- Research: `.github/docs/sdd/research/2026-07-15-token-economics-sdd-harness.md` §7.5 (Propuesta E)
- Complementa SDD-010 (fallas por componente) con dimensión costo
- **2026-07-15 (build-spec):** Implementado `metrics tokens`, `metrics/token-usage.json` + README, WARN en validate-sdd (ps1/sh), docs CLI/README. Estado → `In Build`. Verify local OK.
- **2026-07-15 (smoke manual):** Exitoso — humano confirmó `metrics tokens --summary`, JSON por SDD-NNN y WARN de Released sin token-usage en validate-sdd.
