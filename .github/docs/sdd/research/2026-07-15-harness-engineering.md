# Harness Engineering -- Informe de investigacion para sdd-kit

> **Fecha:** 2026-07-15 | **Autor:** agente SDD | **Contexto:** evaluacion de adopcion del paradigma harness engineering en sdd-kit.

---

## Resumen ejecutivo

**Harness Engineering** es la disciplina de disenar el entorno completo de ejecucion alrededor de un agente de IA. La ecuacion es `Agente = Modelo + Harness`. El modelo es la inteligencia cruda; el harness es la infraestructura, restricciones, ciclos de feedback y sistemas de verificacion que transforman esa inteligencia en algo confiable, seguro y productivo.

Emerge formalmente en Q1 2026 a partir del articulo de Mitchell Hashimoto "My AI Adoption Journey" y es adoptado rapidamente por Thoughtworks, Martin Fowler, Anthropic, AWS y Stripe. La investigacion academica (Meta-Harness de Stanford, AHE de NexAU, Harness-Bench de Peking University) demuestra que un harness optimizado produce brechas de rendimiento de hasta 6x sobre el mismo modelo base.

**sdd-kit ya es un harness**, aunque no use el termino. Este informe documenta el estado del arte, mapea los componentes del kit al marco harness y propone atributos adoptables.

---

## 1. Origen y definicion

### 1.1 El momento fundacional

El 5 de febrero de 2026, Mitchell Hashimoto (co-fundador de HashiCorp, creador de Terraform y Vagrant) publico "My AI Adoption Journey" con una frase que catalizo la disciplina:

> "Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again."

La solucion no es "intenta de nuevo". La solucion es hacer el fallo imposible por diseno.

En 90 dias, la industria construyo un vocabulario sobre esta idea. Thoughtworks incluyo el termino en su Technology Radar. Martin Fowler publico un articulo canonico. Anthropic empezo a llamar al Claude Agent SDK un "agent harness". La frase de Aakash Gupta se volvio viral: "2025 was agents; 2026 is agent harnesses."

### 1.2 Definicion formal

Birgitta Bockeler (Distinguished Engineer en Thoughtworks):

> "A well-built harness serves two goals: it increases the probability that the agent gets it right in the first place, and it provides a feedback loop that self-corrects as many issues as possible before they even reach human eyes."

Vitor Hansen (DevOps.dev, julio 2026):

> "Harness engineering is the discipline of designing the complete execution environment around an AI agent. It is not about the model. It is not about the prompt. It is about the infrastructure, constraints, feedback loops, and verification systems that channel the agent's capability, define its boundaries, and validate its work."

### 1.3 La jerarquia: Prompt -> Contexto -> Harness

Cada nivel contiene al anterior:

| Nivel | Pregunta | Alcance |
|-------|----------|---------|
| Prompt Engineering | "Como le digo al modelo que hacer?" | La instruccion textual |
| Context Engineering | "Que necesita saber el modelo?" | Toda la informacion provista (RAG, tools, historial) |
| Harness Engineering | "Donde y como trabaja el agente?" | Entorno completo de ejecucion, restricciones, verificacion |

Dato clave: un estudio de Stanford HAI (2025) mostro que refinar prompts mas alla de una base razonable mejora la calidad < 3%. Cambios a nivel harness (agregar retrieval, tool access, validacion estructurada) mejoran la calidad 28-47%.

---

## 2. Componentes de un harness

El modelo canonico identifica siete componentes:

| Componente | Descripcion | Ejemplo |
|------------|-------------|---------|
| **Tools** | Lo que el agente puede llamar para actuar sobre el mundo | APIs, sistema de archivos, shell, navegador |
| **Memory** | Estado de corto y largo plazo entre interacciones | Scratchpad, decision log, known failures |
| **Guardrails** | Restricciones de seguridad y comportamiento | Content filters, budget limits, stop conditions |
| **Verification** | Checks deterministicos e inferenciales que validan outputs | Tests, linters, LLM-as-judge |
| **Orchestration** | El loop agentico, control de flujo, retries, timeouts | Agent loop, state machines, max steps |
| **Observability** | Logs, trazas, metricas para entender que ocurrio | Tracing, cost tracking, session replay |
| **Human gates** | Aprobacion humana para acciones de alto impacto | Ready approval, merge approval, deploy gates |

### 2.1 Guias y sensores (Martin Fowler, 2026)

Martin Fowler formaliza dos categorias de controles:

| Tipo | Proposito | Naturaleza |
|------|-----------|------------|
| **Guia (guide / feedforward)** | Anticipa comportamientos no deseados e intenta prevenirlos **antes** de que el agente actue | Aumenta probabilidad de acierto al primer intento |
| **Sensor (sensor / feedback)** | Observa al agente **despues** de actuar y permite autocorreccion | Detecta y corrige errores sin intervencion humana |

Ambos tipos se subdividen:

| | Computacional | Inferencial |
|---|---|---|
| **Guia** | Templates, bootstrap scripts, reglas de linter | AGENTS.md, skills, instrucciones de convencion |
| **Sensor** | Unit tests, type checkers, schema validation, analisis estructural | LLM-as-judge, AI code review, analisis semantico |

La potencia real esta en sensores computacionales con mensajes disenados para LLM: no solo "error en linea 42" sino "Violaste la frontera del modulo X. Mueve este import al adapter en /adapters/payment.ts. Razon: cada modulo es un bounded context."

---

## 3. Investigacion academica

### 3.1 Meta-Harness (Stanford, marzo 2026)

**Autores:** Yoonho Lee, Roshen Nair, Qizheng Zhang (Stanford), Kangwook Lee (KRAFTON), Omar Khattab (MIT), Chelsea Finn (Stanford)

**Arxiv:** `2603.28052`

**Idea central:** Un outer-loop que busca sobre codigo de harness usando un agente proposer. El proposer accede al codigo fuente, scores y trazas de ejecucion de todos los candidatos previos via filesystem (no resumenes comprimidos).

**Resultados clave:**
- En clasificacion de texto online: +7.7 puntos sobre ACE usando 4x menos tokens de contexto
- En razonamiento matematico: +4.7 puntos promedio en 200 problemas IMO-level sobre 5 modelos held-out
- En TerminalBench-2: rank #1 entre todos los harnesses Haiku 4.5
- El proposer lee una mediana de 82 archivos por iteracion, referenciando mas de 20 candidatos previos por paso
- Una sola ejecucion puede producir hasta 10M tokens de informacion diagnostica

**Loop de busqueda:**

```
1. Agente proposer inspecciona filesystem D (codigo, scores, trazas)
2. Propone nuevo harness H'
3. Evalua H' en tareas del search set
4. Almacena H', scores y trazas en D
5. Repite
```

**Implicacion para sdd-kit:** Validacion de arquitectura con trazas completas, no solo resumenes. El `validate-sdd` actual opera sobre estado final, no sobre trayectoria. La observabilidad por componente que se planea en SDD-010 es un primer paso en esta direccion.

### 3.2 AHE -- Agentic Harness Engineering (NexAU, 2026)

**Repo:** `github.com/china-qijizhifeng/agentic-harness-engineering`

**Idea central:** Sistema de observabilidad que descompone el harness en 7 componentes ortogonales file-level, cada uno git-tracked. El loop `evaluate -> analyze -> improve` usa tres capas de observabilidad:

| Capa | Herramienta | Funcion |
|------|-------------|---------|
| Component observability | NexAU | Descompone harness en componentes auditables y revertibles |
| Experience observability | Agent Debugger | Destila trazas de ~10M tokens en reportes por capas |
| Decision observability | Evolve Agent | Propone ediciones con evidencia, predice impacto y es falseado automaticamente |

**Resultados:** NexAU-AHE alcanza 84.7% +- 2.1 pass@1 en Terminal-Bench 2 (GPT-5.5). Eleva GPT-5.4 de 69.7% a 77.0% en 10 iteraciones. El harness congelado se transfiere sin re-evolucion a SWE-bench-Verified y a 4 modelos alternativos.

**Implicacion para sdd-kit:** El tracking por componente y la falsabilidad automatica de decisiones del agente son atributos que el kit podria adoptar progresivamente. Hoy no existe mecanismo para medir si un cambio en una regla o skill mejoro o empeoro el rendimiento del agente.

### 3.3 Harness-Bench (Peking University + Qiyuan Tech, 2026)

**Autores:** Yilun Yao, Xinyu Tan, Chao-Hsuan Liu et al.

**Arxiv:** `2605.27922`

**Idea central:** Benchmark diagnostico que varia configuraciones de harness a traves de modelos en entornos de tarea compartidos. 106 tareas sandboxed offline en 8 categorias de workflow. 5,194 trayectorias de ejecucion analizadas.

**Hallazgos principales:**
- Variacion sustancial en completion, process quality, efficiency y failure behavior segun el par model-harness
- La capacidad del agente debe reportarse a nivel de configuracion model-harness, no atribuirse solo al modelo base
- Fallas recurrentes de execution-alignment: razonamiento plausible desacoplado de tool feedback, workspace state, evidencia o contratos de output verificables

**Implicacion para sdd-kit:** Refuerza la tesis de que la metodologia (el harness SDD) es tan importante como el modelo. El kit deberia poder capturar metricas de exito/falla por spec para alimentar mejora continua.

---

## 4. Adopcion industrial

### 4.1 Stripe -- "Minions" (1,300+ PRs/semana)

El caso publico mas detallado de harness engineering a escala:

- **Volumen:** 1,300+ pull requests mergeados por semana con **cero codigo escrito por humanos**
- **Flujo:** Ingeniero reacciona con emoji en Slack -> minion planifica -> escribe codigo -> ejecuta tests -> envia PR para revision humana
- **Componentes del harness:**
  - Blueprints deterministicos que definen la estructura del cambio
  - Pre-push heuristic hooks que ejecutan linters segun tipo de cambio
  - Shift-left feedback: sensores corren durante la generacion, no despues
  - Nodos deterministicos + agenticos en el workflow

**Leccion:** El modelo es commodity. La ventaja competitiva esta en el harness.

### 4.2 AWS Bedrock AgentCore (GA junio 2026)

AWS incorporo el concepto harness como nucleo de AgentCore. Componentes declarativos:

- Modelo (Bedrock, OpenAI, Gemini, LiteLLM)
- Instrucciones del agente
- Tools (AgentCore Gateway, MCP servers, browser, code interpreter)
- Skills (catalogo AWS, Git, S3)
- Memory (corto y largo plazo)
- Identity y permisos

Cada sesion corre en microVM aislada con su propio filesystem y shell. Versionado inmutable con rollback instantaneo.

### 4.3 Anthropic -- Claude Agent SDK

Anthropic renombro su SDK de agente como "agent harness". Define 5 patrones canonicos: prompt chaining, routing, parallelization, orchestrator-workers, y evaluator-optimizer loops.

### 4.4 Coding Agent Index (Artificial Analysis, mayo 2026)

Primer benchmark publico que evalua stacks completos (modelo + harness), no modelos en aislamiento. Cubre SWE-Bench-Pro-Hard-AA, Terminal-Bench v2 y SWE-Atlas-QnA. Metrica: pass@1 promedio.

---

## 5. Mapeo: que ya tiene sdd-kit

sdd-kit **ya es un harness de agente de coding**, aunque no use el termino. Mapeo componente a componente:

| Componente Harness | Implementacion en sdd-kit | Tipo |
|--------------------|--------------------------|------|
| **Tools** | CLI (`validate`, `backlog`, `spec new`), Git, filesystem | Computacional |
| **Guia computacional** | `validate-sdd`, CI quality gates, `sync-cursor-rules.py`, plantillas spec | Computacional |
| **Guia inferencial** | `domain-rules.md`, `workflow.md`, `sdd-agent-workflow.mdc`, perfiles stack, checklists DoR/DoD, skills `sdd-*` | Inferencial |
| **Sensor computacional** | `verify-implementation` (criterios de aceptacion), CI (compileall, manifest, perfiles) | Computacional |
| **Sensor inferencial** | Revision humana en Ready y merge | Inferencial (humano) |
| **Memory** | `BACKLOG.md`, `sdd.config.yaml`, `archive/`, `releases/` | Estado persistente |
| **Orchestration** | Ciclo Discovery->Draft->Ready->In Build->Validating->Released | Flujo de estados |
| **Human gates** | Ready (aprobacion spec), merge (aprobacion PR) | Gate humano |
| **Budget** | SDD-006 (optimizacion de tokens en reglas) | Control de costo |
| **Observability** | `releases/`, `archive/`, `CHANGELOG.md`, `validate-sdd` | Trazabilidad documental |

**En conclusion:** sdd-kit es un harness maduro en su capa metodologica (guias, gates humanos, verificacion). Las areas de menor cobertura son sensores computacionales avanzados y observabilidad a nivel trayectoria.

---

## 6. Atributos adoptables (evaluados)

Se evaluaron 9 atributos potenciales. Los recomendados para adopcion inmediata:

| # | Atributo | Dominio | Riesgo | Estado |
|---|----------|---------|--------|--------|
| 1 | Lenguaje guias/sensores en reglas y skills | core | Bajo | SDD-008 en Draft |
| 2 | Posicionamiento explicito como harness en docs | docs | Bajo | SDD-009 en Draft |
| 3 | Observabilidad por componente en validate-sdd | cli | Medio | SDD-010 en Draft |

Atributos a evaluar en specs futuros (SDD-007 los cubre parcialmente):

| # | Atributo | Nota |
|---|----------|------|
| 4 | Sensores inferenciales (review agent pre-humano) | Costo en tokens; no debe saltar el gate Ready |
| 5 | Guardrails como codigo (Git destructivo, etc.) | SDD-007 ya en Draft cubre safe-git |
| 6 | Trazas de ejecucion como artefacto estructurado | Inspirado en Meta-Harness filesystem; alto volumen |

Atributo a evitar por ahora:

| # | Atributo | Razon |
|---|----------|-------|
| 7 | Ciclo evaluate->analyze->improve formal | Choca con "humano aprueba en puntos clave"; complejidad innecesaria para el kit actual |

---

## 7. Recomendaciones

1. **Adoptar el lenguaje harness en el posicionamiento del kit.** No cambia el producto, mejora la comunicacion con la industria. El termino ya esta en el radar de Thoughtworks, Martin Fowler, Anthropic y AWS.

2. **Avanzar SDD-008, SDD-009 y SDD-010 en orden.** Son incrementales, de bajo riesgo y construyen capa sobre capa.

3. **No forzar automatizacion total del ciclo.** El diseno actual (agente ejecuta, humano aprueba en Ready y merge) es correcto y se alinea con el principio de harness engineering de "human gates for high-impact actions".

4. **Evaluar metricas de exito por spec.** Si el kit capturara cuantas iteraciones de verify fallaron antes de pasar, o cuantas reglas de dominio se violaron, podria alimentar mejora continua del propio harness. Esto es material para un spec futuro (no urgente).

5. **El harness es la ventaja competitiva, no el modelo.** La investigacion es contundente: mismo modelo, distinto harness = hasta 6x diferencia. sdd-kit debe comunicar esto explicitamente.

---

## 8. Fuentes

### Articulos fundacionales

1. Hashimoto, M. (2026-02-05). "My AI Adoption Journey." https://mitchellh.com/
2. Fowler, M. (2026). "Harness Engineering for Coding Agent Users." https://martinfowler.com/articles/harness-engineering.html
3. Hansen, V. (2026-07-07). "Harness Engineering: The Complete Guide to the Discipline Redefining AI in 2026." DevOps.dev. https://blog.devops.dev/harness-engineering-the-complete-guide-to-the-discipline-redefining-ai-in-2026-faac2edacda5
4. Bockeler, B. (2026). Thoughtworks Technology Radar -- Harness Engineering.

### Investigacion academica

5. Lee, Y., Nair, R., Zhang, Q., Lee, K., Khattab, O., Finn, C. (2026). "Meta-Harness: End-to-End Optimization of Model Harnesses." arXiv:2603.28052. https://arxiv.org/abs/2603.28052
6. NexAU. (2026). "Agentic Harness Engineering (AHE)." https://github.com/china-qijizhifeng/agentic-harness-engineering
7. Yao, Y., Tan, X., Liu, C.H., et al. (2026). "Harness-Bench: Measuring Harness Effects across Models in Realistic Agent Workflows." arXiv:2605.27922. https://arxiv.org/abs/2605.27922

### Adopcion industrial

8. Stripe. (2026). "Minions: 1,300+ PRs per week with zero human-written code." Caso documentado en multiple fuentes.
9. AWS. (2026-06). "Amazon Bedrock AgentCore GA." https://aws.amazon.com/bedrock/agentcore/
10. Anthropic. (2026). "Claude Agent SDK (Agent Harness)."
11. Artificial Analysis. (2026-05). "Coding Agent Index." https://artificialanalysis.ai/

### Analisis y sintesis

12. Mysore, V. (2026-05). "Harness Engineering for AI Agents in 2026." Medium. https://medium.com/@visrow/harness-engineering-for-ai-agents-in-2026-114fcb8edf9e
13. Schmid, P. (2026). "The Importance of Agent Harness in 2026." https://www.philschmid.de/agent-harness-2026
14. Wasowski, J. (2026). "Coding Agent Index 2026: Benchmarking Full Agent Stacks." Medium. https://medium.com/@wasowski.jarek/coding-agent-index-2026-benchmarking-full-agent-stacks-model-harness-4183305e4b90
15. NxCode. (2026). "Harness Engineering Guide: Build Systems That Make AI Agents Reliable." https://www.nxcode.io/resources/news/harness-engineering-complete-guide-ai-agent-codex-2026
