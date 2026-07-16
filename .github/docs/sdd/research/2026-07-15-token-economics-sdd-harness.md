# Riesgo de quema excesiva de tokens en SDD y Harness Engineering — Estado del arte

> **Fecha:** 2026-07-15 | **Autor:** agente SDD | **Contexto:** investigación solicitada por el mantenedor sobre el riesgo de consumo excesivo de tokens al implementar metodologías SDD y/o Harness Engineering.

---

## Resumen ejecutivo

**La pregunta tiene un giro irónico: el spec es solo el 2.4% de los tokens; la revisión iterativa de código consume el 59.4%. El harness bien diseñado reduce costos en 38-41%, no los incrementa. El riesgo real no está en la metodología, sino en la ausencia de governance sobre el loop agentico.**

**Hallazgo clave:** Quemar tokens no es consecuencia de SDD ni de harness engineering. Es consecuencia de token maxing — comprar calidad con más tokens en un loop sin control. El harness es la cura, no la enfermedad.

---

## 1. ¿Dónde se van realmente los tokens?

### 1.1 Tokenomics del ciclo de vida agentico (ChatDev + GPT-5, 30 tareas)

El paper _Tokenomics: Quantifying Where Tokens Are Used in Agentic Software Engineering_ (Concordia University, arXiv:2601.14470, 2026) analizó 30 trazas de ejecución completas con GPT-5 reasoning model y encontró:

| Fase del SDLC | % de tokens |
|---------------|-------------|
| Design / Spec | **2.4%** |
| Coding inicial | 8.6% |
| Code Completion | 26.8% (n=6 tareas) |
| **Code Review** | **59.4%** |
| Testing | 10.3% (n=12 tareas) |
| Documentation | 20.1% |

**El spec es una fracción minúscula del costo total.** La revisión iterativa de código —el loop de "genera → verifica → corrige → re-verifica"— es el verdadero driver de costo.

### 1.2 Composición por tipo de token

| Tipo | % promedio |
|------|-----------|
| Input tokens | **53.9%** |
| Output tokens | 24.4% |
| Reasoning tokens | 21.6% |

El "communication tax" (impuesto de comunicación) domina: los agentes reenvían contexto completo en cada turno, y ese contexto crece cuadráticamente con el número de turnos (`O(k²)` sin compaction).

### 1.3 Context window creep

Una sesión que empieza modesta alcanza ~80K tokens de contexto tras unas pocas docenas de pasos. La misma llamada al final de una sesión larga cuesta un orden de magnitud más que al inicio, por exactamente el mismo trabajo.

### 1.4 SDD Costs: el spec es 2.4%, el review es 59.4%

Jaroslaw Wasowski (Level Up Coding, julio 2026) confirma los mismos números y agrega:

- **Razonamiento tax:** tokens de "thinking" se facturan como output text y pueden multiplicar el costo de una query 3-10x.
- **Prompt caching:** descuento de hasta 90% en reads, pero con break-even en ~1.4 reads/write. Por debajo de ese umbral, el cache **sube** el costo en vez de bajarlo.
- **U-curve:** ni zero-spec ni spec pesada es óptimo. El costo total más bajo está en criterios de aceptación bien estructurados (punto medio).

**Decisión threshold para SDD:**

| Condición | SDD paga | Vibe coding gana |
|-----------|----------|------------------|
| Feature toca 3+ componentes | Sí | — |
| Lifespan > 3 meses | Sí | — |
| Feature simple, 1 componente, efímera | — | Sí |
| Dominio de alto riesgo (auth, pagos, multi-tenant) | Sí (costo de error >> tokens) | — |

---

## 2. El harness como palanca de costo, no como costo

### 2.1 The Harness Effect (Writer + 38 autores, arXiv:2607.06906, julio 2026)

El paper más reciente y completo. Experimento controlado: **mismas 22 tareas, mismos 6 modelos, solo cambia el harness.** Modelos: Claude Sonnet 4.6, Gemini 3.1, Gemini Flash 3.5, Qwen 3.6, GLM 5.1, Palmyra X6.

**Resultados con harness optimizado:**

| Métrica | Baseline | Con harness | Delta |
|---------|----------|-------------|-------|
| Tokens por tarea | 14.2k | 8.8k | **-38%** |
| Costo por tarea | $0.21 | $0.12 | **-41%** |
| Wall-clock mediano | 48s | 27s | **-44%** |
| Quality per dollar | baseline | baseline × 1.82 | **+82%** |
| Task-completions / M tokens | 54.9 | 92.0 | **+68%** |

**El harness movió el costo por tarea más que cambiar entre el modelo más barato y el más caro.** Cambiar de modelo bajo el mismo harness ahorraba 36%; mantener cualquier modelo y adoptar el harness ahorraba 33-61%.

### 2.2 Harness leverage (r=0.99)

Los modelos más fuertes extraen más calidad del harness. La mejora de calidad que un modelo obtiene del harness correlaciona casi perfectamente con su capacidad base (r=0.99, n=6). Esto significa: **el harness amplifica la capacidad del modelo, no la reemplaza.**

### 2.3 Token maxing: la enfermedad que el harness cura

**Definición formal** (del paper): Una trayectoria de desarrollo exhibe _token maxing_ si la intensidad de tokens crece (τₜ₊₁ > τₜ) mientras la calidad marginal por token declina. Es decir, cada release compra calidad a peor tasa de intercambio que el promedio histórico del sistema.

Es el Jevons paradox aplicado a tokens: los precios por token bajan → el consumo total sube → el gasto total no baja. El harness es la única capa donde se puede implementar disciplina de consumo.

### 2.4 Seis familias de mecanismos que reducen el consumo

| # | Mecanismo | Qué ataca | Magnitud |
|---|-----------|-----------|----------|
| 1 | **Cache-shape discipline** (two-zone prompt) | Precio efectivo de input tokens | ~10× descuento (99.9% cache hit → paga ~10% de lista) |
| 2 | **Structured compaction** (checkpoint al 80% del budget) | Crecimiento cuadrático de historia | Convierte O(k²) → O(k) |
| 3 | **Context offload** (sub-agents como firewalls, filesystem como memoria) | Tool outputs y retrieval payloads | Hasta 40% de input tokens en tool calls |
| 4 | **Zero-token waiting** (suspensión durable, no polling) | Espera activa | Elimina tokens de polling completamente |
| 5 | **Failure-spend governance** (clases tipadas, circuit breakers, max 50 iteraciones) | Retries y dead-ends | Multiplicador de Eq.(1) acotado |
| 6 | **Model-agnostic floor** (schema hygiene, portabilidad) | Costos de migración entre modelos | Ahorro compuesto en todo el fleet |

---

## 3. KV-Cache: el multiplicador silencioso

### 3.1 La diferencia de 10x

Manus (uno de los sistemas agenticos más documentados públicamente) publicó:

- Cached tokens: **$0.30/MTok**
- Uncached tokens: **$3.00/MTok**

Diferencia: **10x**. Y si el token cae en cache o no depende enteramente de decisiones del harness, no del modelo.

### 3.2 Las 4 reglas de higiene KV-cache

1. **No timestamps con precisión de segundos** en system prompts — date-level solamente
2. **Contexto append-only** — nunca insertar, borrar ni reordenar
3. **Serialización determinista** — `json.dumps(sort_keys=True)`, mismos bytes siempre
4. **Sticky session routing** — una sesión que rebota entre inference servers pierde el cache en cada salto

### 3.3 El patrón Claude Code

En abril 2026, Anthropic accidentalmente expuso ~512K líneas de TypeScript del source de Claude Code. Lo que reveló:

- System prompt se ensambla dinámicamente desde ~40 secciones condicionales
- ~50 tool definitions, cada una con condiciones
- Cache boundary marker para separar contenido cacheable de session-specific
- "Alrededor de una docena de métodos distintos para compaction, offloading y summarizing"
- Solo preserva los 5 resultados de función más recientes en contexto

**El harness de producción de Anthropic es prueba de existencia de que la disciplina funciona.**

---

## 4. Qué tiene sdd-kit y qué falta

### 4.1 Lo que ya existe (SDD-006, v1.2.2)

SDD-006 ya atacó ~1,470 líneas por carga de contexto:

- Fusión de reglas `alwaysApply` redundantes
- Lectura previa movida de always-apply a skills específicas
- Eliminación de cadena de lectura circular en verify-implementation
- Notas anti-boilerplate en spec-template
- Deduplicación de skills proyecto vs global

### 4.2 Mapeo de mecanismos del estado del arte al kit

| Mecanismo (Harness Effect) | Estado en sdd-kit | Gap |
|----------------------------|-------------------|-----|
| Cache-shape discipline | Parcial — reglas siempre en mismo orden, pero sin two-zone explícito | No hay separación formal prefix estable / volatile tail |
| Structured compaction | No aplica — sesiones Cursor son stateless entre mensajes | N/A para el modelo actual |
| Context offload | Skills on-demand (lectura bajo demanda), pero sin firewalls | Skills cargan todo el contexto del padre |
| Zero-token waiting | N/A — gates humanos son el mecanismo de pausa | N/A para el modelo actual |
| Failure-spend governance | SDD-007 (safe-git) en Draft | No hay circuit breaker, max iteraciones ni clases de fallo tipadas |
| Model-agnostic floor | Core agnóstico al stack (regla 1), pero acoplado a Cursor via Task tool | Skills son portables; reglas `.mdc` no |
| Observabilidad de tokens | **No existe.** No hay per-task token accounting. | **Gap principal** |

### 4.3 Lo que SDD-010 (observabilidad por componente) puede aportar

SDD-010 en Draft apunta justamente a esto: reportar qué componente falló. Pero el estado del arte (Harness Effect §4.4, Tabla 1) muestra que **ningún framework público tiene per-task token accounting**. El que lo tenga gana una ventaja de governance que ningún otro ofrece hoy.

---

## 5. Riesgos reales vs percibidos

### 5.1 Riesgo percibido: "SDD quema tokens porque genera specs largas"

**Falso.** El spec es 2.4% de los tokens. El problema real es el loop de revisión sin control.

### 5.2 Riesgo real #1: Token maxing invisible

Sin observabilidad de tokens por tarea, el token maxing es inobservable — y lo inobservable es ingobernable. Esto aplica a cualquier metodología, no solo SDD.

### 5.3 Riesgo real #2: Governance ausente

Los desastres de costo documentados comparten un denominador común:
- Una empresa quemó su presupuesto anual de AI en meses
- Un ingeniero solo consumió decenas de miles de dólares al mes
- Una sesión quemó miles de dólares en una noche

**Ninguno fue fallo de SDD. Todos fueron fallos de governance:** sin dollar cap, sin límite de loop depth, sin per-task cost log.

### 5.4 Riesgo real #3: Cache hit rate bajo

Un equipo de engineering de una major media company lanzó queries en paralelo sin "calentar" el cache → 4.2% hit rate → factura 60% más alta. Una sola llamada síncrona extra al inicio revirtió el efecto → 60% en ahorros.

### 5.5 Riesgo real #4: Multi-agente sin firewalls

Anthropic reporta que sistemas multi-agente consumen ~15× los tokens de chat y ~4× los de single-agent. El token volume explica ~80% de la varianza de rendimiento. Sin firewalls de contexto (sub-agentes con summary cap), esto escala mal.

---

## 6. Modelo de costos proyectado para sdd-kit

### 6.1 Anatomía de una sesión SDD típica

Usando los datos del estado del arte, podemos proyectar el consumo de una sesión SDD completa en Cursor con sdd-kit:

| Fase SDD | Acciones típicas | Tokens estimados (bajo) | Tokens estimados (alto) | % del total |
|----------|-----------------|------------------------|------------------------|-------------|
| Discovery | Leer BACKLOG, domain-rules, sdd.config | 2-4k | 6-8k | 3-5% |
| Draft | Crear spec desde template, completar secciones | 4-8k | 12-20k | 8-12% |
| Ready | Aprobación humana (1-2 mensajes) | 1-2k | 3-5k | 2-3% |
| In Build | Implementar feature, ejecutar tests | 8-15k | 25-40k | 20-25% |
| Verify | verify-implementation completo | 5-10k | 15-25k | 12-15% |
| Validating | PR, checklist, correcciones post-review | 6-12k | 20-35k | 15-20% |
| Released | git mv, entrada release, validate-sdd | 2-4k | 5-8k | 3-5% |
| **Total sesión** | | **28-55k** | **86-141k** | **100%** |

### 6.2 Dónde está el desperdicio proyectado

Aplicando la taxonomía del estado del arte a sdd-kit:

| Fuente de desperdicio | % de tokens malgastados | Causa raíz | Mecanismo del harness que lo ataca |
|-----------------------|------------------------|------------|-----------------------------------|
| Relectura de contexto completo en cada turno | 20-30% | Cursor reenvía todo el historial por mensaje | Cache-shape discipline + structured compaction |
| Reglas alwaysApply en tareas no-SDD | 10-15% | `sdd-agent-workflow.mdc` siempre cargado | Ya atacado por SDD-006; margen de mejora: 5-8% |
| Skills que cargan referencia circular | 5-10% | verify → build-spec → reference → verify | Ya atacado por SDD-006; eliminado |
| Spec boilerplate en features repetitivas | 5-8% | Template completo para specs de patrón conocido | Anti-boilerplate notes (SDD-006) + compact mode |
| Contexto de specs previos innecesario | 8-12% | Agente lee specs de otras features | Context scoping (SpecLoom-style) |
| **Total proyectado recuperable** | **48-75%** del total de sesión | — | Combinación de mecanismos del harness |

### 6.3 Proyección de ahorro por mecanismo

| Mecanismo | Ahorro tokens/sesión | Ahorro costo/sesión (est. $2/MTok input) | Implementación en sdd-kit |
|-----------|---------------------|----------------------------------------|--------------------------|
| Cache-shape discipline (two-zone prompt) | 15-25k | $0.03-0.05 | Cambios en `install-agents.py` + `sync-cursor-rules.py` |
| Context scoping (solo dependencia directa) | 8-15k | $0.016-0.03 | Nueva sección en skills + `sdd.config.yaml` |
| Spec compact mode (para patrones repetitivos) | 5-10k | $0.01-0.02 | Nueva plantilla `spec-compact-template.md` |
| Governance (dollar cap, max turns) | 10-20k (evitado) | $0.02-0.04 (evitado) | Nueva skill `sdd-cost-governance` |
| **Total ahorro proyectado** | **38-70k** | **$0.076-0.14** | — |
| **% sobre sesión típica** | **44-50%** | — | Alineado con el 38-41% del Harness Effect paper |

---

## 7. Propuestas concretas de implementación

### 7.1 Propuesta A: Two-zone prompt en bootstrap (P1 — Alto impacto, bajo esfuerzo)

**Qué hace:** Separar el contexto que se envía a Cursor en dos zonas: un prefix estable (cacheable) y un tail volátil (por turno). Maximiza cache hit rate.

**Archivos a modificar:**

1. `bootstrap/install-agents.py` — función `install_cursor()`:
   - Agrupar reglas `alwaysApply` al inicio del bloque de reglas (prefix estable)
   - Mover reglas `agentRequestable` después (tail volátil)
   - Agregar comentario `# === CACHE BOUNDARY ===` entre ambas zonas
   - Garantizar orden determinista (mismo hash de archivo siempre)

2. `bootstrap/sync-cursor-rules.py` — nueva validación:
   - Verificar que el orden de reglas no cambie entre instalaciones
   - Alertar si una regla `alwaysApply` se inserta después de una `agentRequestable`

3. `bootstrap/agent-prompts/manifest.json` — nuevo campo:
   ```json
   {
     "rules": {
       "workflow": {
         "alwaysApply": true,
         "cacheZone": "stable"
       }
     }
   }
   ```

**Patrón de código:**

```python
# install-agents.py — nueva función build_cursor_rules()
def build_cursor_rules(manifest: dict, profile: str) -> list[dict]:
    """Construye reglas .mdc con two-zone prompt para maximizar cache hit rate."""
    stable_rules = []   # alwaysApply + schemas — NUNCA muta entre sesiones
    volatile_rules = [] # agentRequestable — puede cambiar por perfil/sesión

    for rule_id, rule_def in manifest["rules"].items():
        content = load_rule_content(rule_id)
        rule = {
            "id": rule_id,
            "alwaysApply": rule_def.get("alwaysApply", False),
            "content": content,
        }
        if rule_def.get("cacheZone") == "stable" or rule["alwaysApply"]:
            stable_rules.append(rule)
        else:
            volatile_rules.append(rule)

    # Orden determinista — mismo hash siempre = mismo cache key
    stable_rules.sort(key=lambda r: r["id"])
    volatile_rules.sort(key=lambda r: r["id"])

    return stable_rules + volatile_rules
```

**Métrica de éxito:** Dos instalaciones consecutivas de `install-agents.py` producen archivos `.mdc` byte-idénticos (hash SHA256 coincide).

**Costo de implementación:** ~2-4 horas. Sin breaking changes. Backward-compatible.

---

### 7.2 Propuesta B: Context scoping — skills solo cargan lo necesario (P1 — Alto impacto, medio esfuerzo)

**Qué hace:** Cada skill `sdd-*` declara su "dependency closure" — qué archivos necesita leer antes de ejecutar. El agente solo carga esos archivos, no todo el contexto SDD.

**Archivos a crear/modificar:**

1. `core/sdd-dependency-graph.md` (nuevo) — declara el grafo de dependencias:

```markdown
# Grafo de dependencias SDD — contexto mínimo por fase

| Skill | Archivos requeridos | Archivos opcionales | ~Tokens |
|-------|--------------------|--------------------|---------|
| sdd-draft-spec | BACKLOG.md, sdd.config.yaml, domain-rules.md, spec-template.md | ADR relacionados | 3-5k |
| sdd-build-spec | spec.md, domain-rules.md, profile checklist | ADR, research | 4-8k |
| sdd-verify-implementation | spec.md (criterios), domain-rules.md | — | 2-4k |
| sdd-open-pr | spec.md (cabecera), BACKLOG.md | — | 1-2k |
| sdd-close-release | BACKLOG.md, spec.md, sdd.config.yaml | — | 2-3k |
```

2. `bootstrap/agent-skills/sdd-draft-spec/SKILL.md` — reemplazar "Lectura previa" genérica:

```markdown
## Contexto mínimo requerido

Antes de ejecutar, lee SOLO estos archivos en orden:
1. `.github/docs/sdd/BACKLOG.md` — para asignar SDD-NNN
2. `.github/docs/sdd/sdd.config.yaml` — para dominios, next_sdd, paths
3. `.github/docs/business/domain-rules.md` — para reglas aplicables

NO leas specs de otras features, ADRs ni releases a menos que el spec los referencie explícitamente.
```

3. `sdd.config.yaml` — nuevo campo opcional:

```yaml
# sdd.config.yaml — nuevo campo
agent:
  targets: [cursor]
  install_mode: explicit
  token_budget:        # NUEVO — opcional
    max_context_per_skill: 8000    # tokens máximos de contexto inicial por skill
    compact_mode: false            # usar spec-compact-template para specs repetitivas
    cache_warm_on_install: true    # pre-cargar reglas en orden determinista
```

**Métrica de éxito:** Una sesión `sdd-draft-spec` carga ≤5k tokens de contexto inicial (medido con herramienta de profiling por implementar en Propuesta E).

**Costo de implementación:** ~4-6 horas. Cambio en 6-8 skills. Backward-compatible (campos nuevos son opcionales).

---

### 7.3 Propuesta C: Spec compact mode para patrones repetitivos (P2 — Medio impacto, bajo esfuerzo)

**Qué hace:** Cuando un spec sigue un patrón ya documentado (ej. "nuevo perfil de stack", "nuevo comando CLI"), usar una plantilla reducida que elimina secciones redundantes.

**Archivos a crear:**

1. `core/templates/spec-compact-template.md` (nuevo):

```markdown
# SDD-NNN — [Título]

> **Modo compacto** — Este spec sigue el patrón documentado en `[referencia]`.
> Secciones omitidas: [lista de secciones estándar omitidas].
> Para detalles de proceso, ver `core/workflow.md`.

## Cabecera

| Campo | Valor |
|-------|-------|
| **ID** | `SDD-NNN` |
| **Dominio** | `[dominio]` |
| **Tipo** | `[feature|bugfix|refactor]` |
| **Fecha** | [YYYY-MM-DD] |
| **Estado** | `Draft` |
| **Versión objetivo** | vX.Y.Z |

## Problema y objetivo

[1-2 párrafos; solo lo específico de este spec]

## Alcance

- **Incluye:** [3-5 bullets]
- **Excluye:** [1-3 bullets]

## Criterios de aceptación

- [ ] [Criterio 1]
- [ ] [Criterio 2]
- [ ] [Criterio 3]
- [ ] Verify local OK (quality gates, domain-rules, validate-sdd)

> **Nota:** Reglas de negocio aplicables en `business/domain-rules.md`.
> Impacto técnico y checklist stack según perfil `[nombre]`.
```

2. `core/workflow.md` — nueva sección "Cuándo usar modo compacto":

```markdown
### Modo compacto de spec

Usar `spec-compact-template.md` cuando:
- El spec sigue un patrón documentado (nuevo perfil, nuevo comando CLI, nueva skill)
- El dominio y las reglas de negocio ya están establecidos
- No hay decisiones arquitectónicas nuevas (sin ADR)

No usar modo compacto cuando:
- El spec introduce un nuevo dominio
- Hay decisiones de diseño no triviales
- El spec requiere ADR
```

**Ahorro estimado:** 40-60% de tokens vs plantilla completa (~2-3k tokens ahorrados por spec compacto).

**Costo de implementación:** ~1-2 horas. Sin breaking changes.

---

### 7.4 Propuesta D: Governance de costo como skill (P1 — Alto impacto, medio esfuerzo)

**Qué hace:** Una skill `sdd-cost-governance` que el agente consulta antes de iniciar cualquier sesión SDD. Define límites de gasto, patrones de "stop" y logging de costo por spec.

**Archivos a crear:**

1. `bootstrap/agent-skills/sdd-cost-governance/SKILL.md` (nuevo):

```markdown
# SDD Cost Governance

> El agente DEBE leer esta skill al inicio de cada sesión SDD.
> No es opcional. Es el circuit breaker del harness.

## Límites de sesión

| Límite | Valor por defecto | Acción al alcanzar |
|--------|------------------|-------------------|
| Turnos máximos por fase | 15 | Pausar y pedir aprobación humana |
| Turnos máximos totales | 50 | Terminar sesión; reportar estado |
| Iteraciones de verify fallidas | 3 | STOP. No seguir. Reportar criterios fallidos. |
| Tool calls idénticas consecutivas | 3 | Circuit breaker: cambiar approach o pedir ayuda |
| Tiempo máximo de sesión | 45 min | Pausar y resumir progreso |

## Registro de costo por spec

Al finalizar cada fase, registrar en `.github/docs/sdd/metrics/token-usage.json`:

{
  "spec_id": "SDD-NNN",
  "date": "YYYY-MM-DD",
  "phases": {
    "draft": { "turns": N, "tool_calls": N, "estimated_tokens": N },
    "build": { "turns": N, "tool_calls": N, "estimated_tokens": N },
    "verify": { "turns": N, "tool_calls": N, "estimated_tokens": N }
  },
  "total_estimated_tokens": N,
  "verify_passed_first_attempt": true/false,
  "domain_rules_violations": N
}

## Anti-patrones de gasto — STOP inmediato

- Loop de "generar → test falla → mismo error → regenerar" sin cambiar approach
- Leer el mismo archivo 5+ veces sin modificarlo
- Re-escribir specs ya aprobadas en Ready
- Ejecutar tests sin cambiar código entre ejecuciones
- Cargar specs de otras features no relacionadas
```

2. `bootstrap/agent-prompts/manifest.json` — entrada nueva:

```json
{
  "skills": {
    "sdd-cost-governance": {
      "file": "sdd-cost-governance/SKILL.md",
      "alwaysApply": false,
      "trigger": "session_start"
    }
  }
}
```

3. `bootstrap/agent-skills/sdd-build-spec/SKILL.md` — agregar al inicio:

```markdown
## Antes de empezar

1. Leer `sdd-cost-governance` — verificar límites de sesión.
2. Si verify ya falló 3 veces en esta sesión → STOP y reportar.
```

**Costo de implementación:** ~3-4 horas. Nueva skill + entradas en 3-4 skills existentes.

---

### 7.5 Propuesta E: Observabilidad de tokens por spec (P2 — Alto impacto, alto esfuerzo)

**Qué hace:** Extender SDD-010 (observabilidad por componente) para incluir métricas de consumo de tokens por spec. El objetivo es tener per-task token accounting — el gap que nadie en la industria tiene hoy.

**Nota:** Esta propuesta es ambiciosa porque Cursor no expone token counts por API. La implementación sería una estimación basada en heurísticas:

**Archivos a crear/modificar:**

1. `cli/lib/metrics.py` — nueva función `estimate_tokens()`:

```python
def estimate_tokens(spec_id: str, session_log: Path) -> dict:
    """Estima consumo de tokens por spec basado en heurísticas del session log.

    Heurísticas (orden de magnitud, no precisión):
    - 1 mensaje del usuario ~ 200 tokens
    - 1 mensaje del asistente ~ 800 tokens (promedio)
    - 1 tool call (Read) ~ tamaño del archivo leído / 4
    - 1 tool call (Write) ~ tamaño del contenido escrito / 4
    - Contexto acumulado ~ O(k²) sin compaction, O(k) con

    Returns:
        dict con estimated_input_tokens, estimated_output_tokens,
        estimated_total_tokens, confidence (low/medium/high)
    """
    # Implementación: parsear session log, contar mensajes y tool calls,
    # estimar con factores del paper Tokenomics (53.9% input, 24.4% output, 21.6% reasoning)
```

2. `cli/sdd.py` — nuevo subcomando:

```bash
sdd metrics tokens SDD-NNN     # estimado de tokens para un spec
sdd metrics tokens --all        # todos los specs con estimados
sdd metrics tokens --summary    # resumen: total, promedio, top consumers
```

3. `.github/docs/sdd/metrics/` — nuevo directorio para logs de consumo.

4. `validate-sdd.ps1` / `validate-sdd.sh` — nuevo check:

```powershell
# Validar que existe token-usage.json para specs Released
# Alertar si un spec consumió >2x el promedio
```

**Métrica de éxito:** `sdd metrics tokens --summary` produce una tabla como:

```
SDD-NNN  | Dominio   | Fase más cara | Tokens est. | Verify 1er intento
SDD-006  | bootstrap | Draft         | 45k         | Sí
SDD-007  | core      | Build         | 78k         | No (2 intentos)
SDD-008  | core      | Draft         | 32k         | Sí
---
Promedio: 51.7k | Mediana: 45k | Top consumer: SDD-007 (78k)
```

**Costo de implementación:** ~8-12 horas. Requiere spec formal (extensión de SDD-010 o nuevo SDD-012).

---

### 7.6 Propuesta F: Threshold de decisión SDD vs no-SDD documentado (P2 — Bajo impacto, bajo esfuerzo)

**Qué hace:** Formalizar en `core/workflow.md` y `BACKLOG.md` el threshold de decisión que determina si una iniciativa requiere spec o va con ID `—`.

**Archivos a modificar:**

1. `core/workflow.md` — nueva sección:

```markdown
## ¿Esta iniciativa necesita spec?

Usar esta checklist ANTES de crear un spec. Si la respuesta es NO a todas, usar ID `—` en release.

### La iniciativa requiere spec si...

- [ ] Toca 3 o más componentes/dominios del proyecto
- [ ] Modifica el schema de base de datos
- [ ] Introduce una dependencia externa nueva
- [ ] Cambia el contrato de una API pública
- [ ] Afecta autenticación, autorización o datos multi-tenant
- [ ] Tiene lifespan esperado > 3 meses (se modificará en el futuro)
- [ ] Es un refactor que toca > 5 archivos
- [ ] Requiere ADR (decisión arquitectónica transversal)

### La iniciativa NO requiere spec si...

- [ ] Es un fix de typo, copy, traducción
- [ ] Es un bump de dependencias (sin cambios de API)
- [ ] Es una feature de 1 archivo, 1 componente, efímera (< 1 semana de vida)
- [ ] Es un hotfix crítico (spec post-mortem aceptable)

### Zona gris (criterio del mantenedor)

Si la iniciativa toca 2 componentes pero es simple → spec simplificado (compact mode).
Si la iniciativa es 1 componente pero de alto riesgo → spec completo.
```

**Costo de implementación:** ~30 minutos. Solo documentación.

---

### 7.7 Matriz de priorización

| Propuesta | Impacto en tokens | Esfuerzo | Riesgo | Dependencias | Recomendación |
|-----------|------------------|----------|--------|-------------|---------------|
| A: Two-zone prompt | Alto (-15-25k/sesión) | Bajo (2-4h) | Bajo | Ninguna | **Hacer ya** (sin spec) |
| B: Context scoping | Alto (-8-15k/sesión) | Medio (4-6h) | Bajo | SDD-006 completado | **Hacer ya** (sin spec) |
| C: Compact mode | Medio (-2-3k/spec) | Bajo (1-2h) | Bajo | Ninguna | **Hacer ya** (sin spec) |
| D: Cost governance | Alto (previene loops) | Medio (3-4h) | Bajo | Ninguna | **Hacer ya** (sin spec) |
| F: Threshold doc | Bajo (decisional) | Bajo (0.5h) | Nulo | Ninguna | **Hacer ya** (sin spec) |
| E: Token observability | Alto (visibilidad) | Alto (8-12h) | Medio | SDD-010 | Spec formal (SDD-012) |

---

### 7.8 Lo que NO hacer (anti-patrones confirmados por el estado del arte)

| Acción | Por qué es un error | Evidencia |
|--------|--------------------|-----------|
| Acortar specs por miedo a tokens | El spec es 2.4% del total. Optimizarlo es marginal. | Tokenomics paper §3.1, Wasowski §1 |
| Eliminar verify-implementation | Es lo que evita el loop de revisión infinita (59.4% del gasto). | Tokenomics paper Finding 1 |
| Adoptar multi-agente sin firewalls | Multiplicador 15× documentado por Anthropic. | Anthropic building effective agents, 2026 |
| Usar timestamps de segundos en system prompts | Rompe KV-cache en cada llamada → 10× más caro. | Sah, Manus data §3.1 |
| LLM-generated instruction files | ETH Zurich: +20% tokens, peor rendimiento. | Sah §1.5 |
| Cargar todos los MCP tools al inicio | Cada tool definition = 200-500 tokens. Two-tier loading reduce 60-70%. | GenAI Playbook §2 |
| Sesiones monolíticas (>50 turns) | Context window creep: mismo trabajo cuesta 10× más al final. | Wasowski §3 |
| Usar modelo caro para tareas mecánicas | Misma tarea en Flash/Haiku cuesta 5× menos. | EPAM Tokenomics §4 |

---

## 8. Plan de acción recomendado

### Fase 1 — Esta semana (sin specs nuevos, ~8-12 horas total)

1. Implementar **Propuesta A** (two-zone prompt en `install-agents.py`)
2. Implementar **Propuesta F** (threshold doc en `workflow.md`)
3. Implementar **Propuesta C** (spec-compact-template.md)

### Fase 2 — Próxima semana (sin specs nuevos, ~7-10 horas)

4. Implementar **Propuesta B** (context scoping en skills)
5. Implementar **Propuesta D** (cost governance skill)

### Fase 3 — v1.4.0 (spec formal SDD-012)

6. Crear spec SDD-012 para **Propuesta E** (token observability)
7. Implementar `sdd metrics tokens` en CLI
8. Integrar con validate-sdd

### Fase 4 — v1.5.0+ (evaluar según datos)

9. Analizar datos de token-usage.json tras 10+ specs Released
10. Ajustar thresholds de governance según datos reales
11. Evaluar sub-agentes con firewall si el patrón multi-agente se adopta

---

## 9. Conclusión

**El riesgo de quema excesiva de tokens no proviene de SDD ni de harness engineering. Proviene de la ausencia de governance sobre el loop agentico.** La evidencia del estado del arte (julio 2026) es contundente:

1. **El spec es ~2.4% de los tokens.** Optimizarlo es marginal. La revisión iterativa es ~59.4%.
2. **Un harness bien diseñado reduce tokens 38%, costo 41%, tiempo 44%** — manteniendo calidad (Harness Effect, arXiv:2607.06906).
3. **KV-cache hygiene es el multiplicador más grande** (10× diferencia cached vs uncached; Manus data).
4. **Nadie tiene per-task token accounting.** sdd-kit puede ser el primero.
5. **El threshold de decisión es claro:** 3+ componentes o >3 meses de lifespan → SDD paga.
6. **5 de las 6 propuestas son implementables sin spec nuevo** (solo la observabilidad requiere SDD-012).

sdd-kit ya avanzó con SDD-006 (optimización de ~1,470 líneas/contexto). Las propuestas A-F de este informe representan el siguiente nivel de madurez del harness: pasar de "metodología que funciona" a "metodología con governance de costo incorporada". El costo total de implementación de las 5 propuestas sin spec es ~11-17 horas. El retorno esperado es 38-50% de reducción de tokens por sesión SDD.

---

## 10. Fuentes

### Académicas

1. Salim, M., Latendresse, J., Khatoonabadi, S.H., Shihab, E. (2026). "Tokenomics: Quantifying Where Tokens Are Used in Agentic Software Engineering." arXiv:2601.14470. Concordia University DAS Lab. https://arxiv.org/abs/2601.14470
2. Sayed Ali, M., Novik, A., Boddupally, A., et al. (2026). "The Harness Effect: How Orchestration Design Sets the Token Economics of Enterprise Agentic AI." arXiv:2607.06906. Writer, Inc. https://arxiv.org/abs/2607.06906
3. Lee, Y., Nair, R., Zhang, Q., Lee, K., Khattab, O., Finn, C. (2026). "Meta-Harness: End-to-End Optimization of Model Harnesses." arXiv:2603.28052. Stanford. https://arxiv.org/abs/2603.28052
4. Yao, Y., Tan, X., Liu, C.H., et al. (2026). "Harness-Bench: Measuring Harness Effects across Models in Realistic Agent Workflows." arXiv:2605.27922. Peking University. https://arxiv.org/abs/2605.27922
5. NexAU. (2026). "Agentic Harness Engineering (AHE)." https://github.com/china-qijizhifeng/agentic-harness-engineering

### Industria y análisis

6. Wasowski, J. (2026-07-03). "SDD Costs: Where the Tokens Actually Go and When Spec-Driven Development Pays Off." Level Up Coding. https://levelup.gitconnected.com/when-sdd-pays-off-and-when-it-doesnt-the-full-cost-accounting-from-dozens-of-sources-3e87acf17169
7. Sah, V. (2026-04-13). "The Definitive Guide to Agent Harness Engineering." Medium. https://engineeratheart.medium.com/the-definitive-guide-to-agent-harness-engineering-5f5edf25fd73
8. CIO.com (2026-07). "The hidden AI cost driver: Harness design can make or break enterprise agent economics." https://www.cio.com/article/4197193/the-hidden-ai-cost-driver-harness-design-can-make-or-break-enterprise-agent-economics.html
9. GenAI Playbook. (2026). "Building an Agent Harness from Scratch — The Design-Side Companion." https://www.genai-playbook.com/articles/build-agent-harness-en.html
10. EPAM. (2026). "AI Tokenomics for Enterprises: Understanding and Optimizing AI Costs at Scale." https://www.epam.com/insights/ai/blogs/ai-tokenomics-reduce-cost-and-ai-spend
11. Hansen, V. (2026-07-07). "Harness Engineering: The Complete Guide to the Discipline Redefining AI in 2026." DevOps.dev. https://blog.devops.dev/harness-engineering-the-complete-guide-to-the-discipline-redefining-ai-in-2026-faac2edacda5
12. Fowler, M. (2026). "Harness Engineering for Coding Agent Users." https://martinfowler.com/articles/harness-engineering.html

### Herramientas y patrones

13. tinesoft/spec-kit-token-budget. (2026). GitHub. https://github.com/tinesoft/spec-kit-token-budget
14. Suthar, R. (2026). "SpecLoom: Deterministic Context for Coding Agents." https://ruchitsuthar.com/blog/developer-productivity/specloom-deterministic-context-for-coding-agents/
15. Anthropic. (2026). Claude Code source leak analysis. Debug source map en npm package v2.1.88 (~512K líneas TypeScript).
16. Anthropic. (2026). "Building effective agents." https://www.anthropic.com/engineering/building-effective-agents
17. Manus. (2026). Token cost data: cached $0.30/MTok vs uncached $3.00/MTok. Documentado en Sah (fuente 7).
18. Stripe. (2026). "Minions: 1,300+ PRs per week with zero human-written code." Caso documentado en múltiples fuentes.
19. Hashimoto, M. (2026-02-05). "My AI Adoption Journey." https://mitchellh.com/

### Internas sdd-kit

20. sdd-kit. (2026). SDD-006 — Optimización de tokens en reglas, skills y pipeline de generación. `archive/2026/bootstrap/SDD-006-optimizacion-tokens-kit.md`
21. sdd-kit. (2026). SDD-010 — Observabilidad por componente en validate-sdd. `specs/cli/SDD-010-observabilidad-componente-validate.md` (Draft)
22. sdd-kit. (2026). `domain-rules.md` — Principios de diseño del kit.
23. sdd-kit. (2026). Research: Harness Engineering. `research/2026-07-15-harness-engineering.md`
24. sdd-kit. (2026). Research: Agentes y subagentes. `research/2026-07-15-agentes-subagentes.md`
25. sdd-kit. (2026). ADR-001: No definir agentes/subagentes en core. `adr/ADR-001-2026-07-15-no-definir-agentes-subagentes-core.md`
26. sdd-kit. (2026). ADR-002: Adoptar harness engineering como marco conceptual. `adr/ADR-002-2026-07-15-adoptar-harness-engineering-marco-conceptual.md`
