# Plan de auditoría general — SDD Kit

| Campo | Valor |
| --- | --- |
| **ID archivo** | `20260905-1202-auditoria-general-kit` |
| **Tipo** | Plan de auditoría |
| **Estado** | Ejecutado (2026-09-05) |
| **Fecha plan** | 2026-09-05 12:02 |
| **Fecha cierre** | 2026-09-05 |
| **Informe** | [20260905-1202-auditoria-general-kit-informe.md](20260905-1202-auditoria-general-kit-informe.md) |
| **Versión kit referenciada** | `v1.3.2` (`sdd.config.yaml` / BACKLOG) |
| **Alcance** | Repositorio productor `sdd-kit` (core, profiles, bootstrap, cli, docs, instancia SDD) |
| **Fuera de alcance** | Auditoría de seguridad de terceros; performance de modelos LLM; repos consumidores reales (salvo checklist de dogfooding) |
| **Referencias** | [BACKLOG](../BACKLOG.md) · [ADOPTION](../ADOPTION.md) · [ANALYSIS histórico](../../business/planning/ANALYSIS.md) · [domain-rules](../../business/domain-rules.md) |

---

## 1. Objetivo

Evaluar de forma sistemática la madurez del kit como **agent harness** multi-stack: propuesta de valor, arquitectura, metodología, adopción, integración agentica, perfiles, CLI/calidad, gobernanza y riesgos — y convertir hallazgos en **gaps accionables** (BACKLOG / specs) o descartes documentados.

### Resultado esperado al cerrar la auditoría

1. Informe de hallazgos en `audits/` (mismo prefijo temporal o archivo hermano `…-informe.md`).
2. Tabla gap → severidad → dominio → acción sugerida (spec / trivial / no hacer).
3. Actualización opcional de Discovery en BACKLOG con ítems priorizados.

---

## 2. Método

| Paso | Acción | Sensor / evidencia |
| --- | --- | --- |
| A | Lectura guiada de docs canónicos (`concepts`, `workflow`, `agent-setup`, `ADOPTION`, ADRs) | Hecho 2026-09-05 — [informe §2–§4](20260905-1202-auditoria-general-kit-informe.md) |
| B | Inspección estructural (árbol, manifiestos, perfiles, CI) | Hecho 2026-09-05 — [informe §4–§5](20260905-1202-auditoria-general-kit-informe.md) |
| C | Dogfooding de instancia SDD del kit | Hecho 2026-09-05 — [informe §5](20260905-1202-auditoria-general-kit-informe.md) (`validate-sdd` exit 0) |
| D | Muestreo de skills/prompts vs reglas always-on | Hecho 2026-09-05 — [informe §6](20260905-1202-auditoria-general-kit-informe.md) |
| E | Contraste con ANALYSIS 2026-06-11 | Hecho 2026-09-05 — [informe §7](20260905-1202-auditoria-general-kit-informe.md) |
| F | Síntesis gaps + backlog | Hecho 2026-09-05 — [informe §10](20260905-1202-auditoria-general-kit-informe.md) + [BACKLOG Discovery](../BACKLOG.md) |

**Severidad:** P0 bloquea adopción o integridad SDD · P1 degrada calidad/confianza · P2 fricción · P3 nice-to-have.

---

## 3. Ámbitos a auditar

### 3.1 Producto y propuesta de valor

| Qué verificar | Cómo |
| --- | --- |
| Claridad “agent harness” vs metodología genérica | README, SDD-009, posicionamiento público |
| Audiencia (solo-dev + agente) coherente en docs | `concepts.md`, CONTRIBUTING, ADOPTION |
| Diferenciación frente a “solo prompts” | Catálogo prompts vs skills vs reglas |

**Gaps / mejoras (hipótesis preliminar):**

- ANALYSIS histórico (2026-06) está **desactualizado** respecto a v1.3.x; riesgo de decisiones con evidencia vieja.
- Falta evidencia pública de **adopción en consumidor externo** (ya en Discovery BACKLOG).
- Posible oportunidad: one-pager “qué ganas en 15 min” para onboarding frío.

---

### 3.2 Arquitectura del kit

| Qué verificar | Cómo |
| --- | --- |
| Separación core agnóstico / profiles / bootstrap / cli | Muestreo de referencias a frameworks en `core/` |
| Contrato dual-release (producto vs campaña) | `docs/releases/` ↔ `.github/docs/sdd/releases/` (SDD-011) |
| Paths `sdd` vs `business` vs `docs/` | DR-6 / DR-7; sin docs SDD fuera de `paths.sdd` |

**Gaps / mejoras (hipótesis preliminar):**

- Carpetas `metrics/` residuales o docs de tokens post SDD-016: confirmar limpieza completa en instancia y artefactos instalables.
- `docs/maintainers/` stub vs planning en `business/planning/`: claridad para mantenedores nuevos.
- Oportunidad: diagrama actualizado de arquitectura (ANALYSIS muestra solo Laravel; ya hay más perfiles).

---

### 3.3 Metodología y flujo

| Qué verificar | Cómo |
| --- | --- |
| Estados Discovery→Released + Descartado | `workflow.md`, BACKLOG, archive |
| Guías vs sensores (DoR / verify / DoD) | rules + skills `verify-implementation` |
| Safe-git | `safe-git-contract.md` + regla always-on |
| Cuándo hay/no hay spec | Tabla trivial vs no trivial |

**Gaps / mejoras (hipótesis preliminar):**

- Higiene instancia: existen stubs en `specs/core/` de specs **ya Released** (p. ej. SDD-007, SDD-016) conviviendo con `archive/` — posible fallo de ritual Released o de `validate-sdd`.
- Oportunidad: sensor CLI que falle si un ID Released permanece en `specs/`.
- Clarificar en docs el rol de `audits/` (este directorio) vs `research/` vs `business/planning/`.

---

### 3.4 Experiencia de adopción

| Qué verificar | Cómo |
| --- | --- |
| INSTALL (submodule / copia / solo docs) | Recorrido documental + dry-run mental de pasos |
| Etapas 1–3 adopción | `adoption-guide.md` + ADOPTION kit (etapa 2) |
| Fricción proyecto nuevo vs existente | Prompts `adopt-existing`, `formalize-domain-rules` |
| Upgrade de kit en consumidor | skill `sdd-upgrade-kit`, UPGRADE-LOG |

**Gaps / mejoras (hipótesis preliminar):**

- Sin validación en producción con repo ajeno (Discovery docs).
- `agent.targets: [cursor]` en config del kit: ¿paridad real al instalar otros targets?
- Oportunidad: checklist “primer día” medible (tiempo / archivos tocados / errores tipicos).

---

### 3.5 Integración con agentes

| Qué verificar | Cómo |
| --- | --- |
| Manifiestos prompts + skills | JSON válido (CI); contenido vs `prompt-catalog` |
| 6 skills Cursor vs bloques Claude/Codex/Copilot | `agent-setup.md`, `install-agents.py` |
| Drift rules ↔ skills ↔ core docs | Diff semántico muestreado |
| Tokens always-on | TOKEN-OPTIMIZATION; tamaño reglas |

**Gaps / mejoras (hipótesis preliminar):**

- Skills solo en Cursor; otros agentes dependen de bloques — auditar si el mapa trigger→prompt es suficiente en la práctica.
- Oportunidad: test de contrato “skill X menciona lectura previa BACKLOG/config/domain-rules”.
- Riesgo de duplicación usuario-skills (`~/.cursor/skills`) vs bootstrap del repo.

---

### 3.6 Perfiles por stack

| Qué verificar | Cómo |
| --- | --- |
| Archivos obligatorios por perfil | Paridad vs plantilla `profile-template` / CI perfiles |
| Profundidad checklist / deploy / ejemplos | Comparar Filament vs Django vs React vs reports |
| Contaminación dominio de negocio | Muestreo voyager / ejemplos |

**Gaps / mejoras (hipótesis preliminar):**

- Paridad de **archivos** parece OK (7 perfiles con set estándar); auditar **calidad** del contenido (deploy realista, ejemplos actualizados).
- `reports-latex-md` tiene `workflow-extensions.md` extra — documentar si es patrón o excepción.
- Perfiles adicionales (node/go/vue) en Discovery baja prioridad — no abrir sin demanda.
- Oportunidad: matriz “perfil × madurez (A/B/C)” publicada para consumidores.

---

### 3.7 CLI y calidad técnica

| Qué verificar | Cómo |
| --- | --- |
| Comandos `validate`, `backlog`, `spec`, etc. | README cli + smoke manual |
| CI | `.github/workflows/ci.yml` (compileall, manifests, install skills, perfiles) |
| Tests automatizados | Ausencia de pytest CLI (Discovery) |
| Observabilidad residual tokens | Post SDD-016 / SDD-013 |

**Gaps / mejoras (hipótesis preliminar):**

- **P1:** CI solo `compileall` + manifests; **sin suite pytest** de CLI (BACKLOG Discovery).
- CI dispara en `main` / PR a `main` — confirmar si `dev` queda sin gate equivalente.
- Oportunidad: job `validate-sdd` sobre `.github/docs/sdd` en CI del kit.

---

### 3.8 Gobernanza y evolución

| Qué verificar | Cómo |
| --- | --- |
| BACKLOG vs `ids.next_sdd` | Coherencia SDD-017 |
| ADRs | README adr; ADR-001/002 vigentes |
| SemVer + dual-release últimas versiones | v1.3.0–v1.3.2 |
| Domain-rules del kit | Completitud DR; sin reglas “asumidas” |

**Gaps / mejoras (hipótesis preliminar):**

- ROADMAP / ANALYSIS en planning son snapshots; falta ritual de “revisión trimestral” o marcar obsoletos.
- Oportunidad: política explícita de cuándo un hallazgo de auditoría entra a Discovery vs queda solo en `audits/`.
- Confirmar que deprecaciones (cost-governance, metrics) no dejan comandos/docs huérfanos en CLI o upgrade-guide.

---

### 3.9 Madurez y riesgos

| Qué verificar | Cómo |
| --- | --- |
| Complejidad cognitiva del kit | Conteo de entrypoints docs; onboarding time |
| Dogfooding | Etapa ADOPTION; specs recientes |
| Deuda documentada vs no documentada | BACKLOG Discovery + hallazgos nuevos |
| Riesgo “kit que se autogestiona demasiado” | ADR agentes/subagentes; safe-git |

**Gaps / mejoras (hipótesis preliminar):**

- Madurez metodológica alta (muchas iniciativas Released); madurez de **confianza automatizada** (tests CLI, dogfooding externo) media-baja.
- Riesgo: proliferación de carpetas (`research`, `metrics`, `audits`, planning) sin índice único.
- Oportunidad: índice `paths.sdd/README` o sección en ADOPTION listando artefactos permitidos.

---

## 4. Orden de ejecución sugerido

1. **Higiene SDD + arquitectura** (3.2, 3.3, 3.8) — barato, alto impacto en integridad.
2. **CLI / CI** (3.7) — gaps ya conocidos.
3. **Agentes + adopción** (3.5, 3.4).
4. **Perfiles** (3.6) — muestreo profundo 2–3 perfiles, no los 7 al detalle el mismo día.
5. **Producto / madurez** (3.1, 3.9) — síntesis y priorización final.

Tiempo estimado orientativo: **4–8 h** de trabajo enfocado (plan → informe), sin implementar fixes.

---

## 5. Plantilla de registro de hallazgos (para el informe)

| ID | Ámbito | Hallazgo | Severidad | Evidencia | Acción sugerida | Dominio |
| --- | --- | --- | --- | --- | --- | --- |
| H-001 | … | … | P0–P3 | path / comando | Discovery / Draft / trivial / nada | cli\|core\|… |

---

## 6. Criterios de cierre del plan

- [x] Los 9 ámbitos tienen al menos una pasada con evidencia.
- [x] Existe informe con tabla de hallazgos — [informe Ejecutado A–F](20260905-1202-auditoria-general-kit-informe.md).
- [x] Pasada documental: ámbitos 3.1–3.5 y 3.8 (Paso A).
- [x] Pasada estructural: ámbitos 3.2, 3.6, 3.7 (Paso B).
- [x] Pasada dogfooding: `validate-sdd` verde en instancia kit (Paso C).
- [x] Pasada agentes/skills: Cursor + paridad multi-agente (Paso D).
- [x] Pasada madurez/gobernanza histórica: contraste ANALYSIS + ámbitos 3.8–3.9 (Paso E).
- [x] Síntesis + Discovery actualizado (Paso F).
- [x] Gaps P0/P1 reflejados en BACKLOG Discovery — H-B01 (cli) + H-D01 (bootstrap); sin P0.
- [x] ANALYSIS histórico enlazado desde el informe como baseline 2026-06 — [informe §7](20260905-1202-auditoria-general-kit-informe.md); banner en el propio ANALYSIS queda en Discovery docs (H-E02).

---

## 7. Notas

- Este archivo es **planificación** bajo `paths.sdd/audits/` (petición explícita). No sustituye un spec; los fixes no triviales deben pasar por ciclo SDD.
- No ejecutar cambios de producto ni commits desde este plan sin aprobación humana.
)
