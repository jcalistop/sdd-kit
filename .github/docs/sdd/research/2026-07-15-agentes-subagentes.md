# Por que sdd-kit no debe definir agentes ni subagentes

> **Fecha:** 2026-07-15 | **Autor:** agente SDD | **Contexto:** analisis de inclusion del concepto "agente/subagente" en el core del kit, a partir de la discusion en sesion de contexto.

---

## Resumen ejecutivo

Agregar una definicion de "agente" y "subagente" al core de sdd-kit seria una violacion directa del principio de diseno **core agnostico al stack** (regla 1, `domain-rules.md`). El concepto carece de estandarizacion entre IDEs, frameworks y modelos, y su inclusion forzaria actualizaciones constantes del producto por cambios ajenos a la metodologia. sdd-kit ya cubre la necesidad real —orquestacion del ciclo SDD— mediante estados, gates humanos y skills on-demand, sin acoplarse a un runtime especifico. Este informe documenta la evidencia de fragmentacion, mapea el riesgo arquitectonico y fundamenta la decision de mantener el concepto fuera del core.

---

## 1. El problema: "agente" no tiene definicion unica

### 1.1 Definiciones en competencia

El termino "agente" es polisemico en el ecosistema actual de IA. Segun el contexto, refiere a:

| Contexto | Definicion de "agente" | "Subagente" | Fuente |
|----------|------------------------|-------------|--------|
| **Cursor IDE** | Modelo que ejecuta tools en un loop autonomo | Task tool con tipo fijo (`explore`, `shell`, `bugbot`) lanzado por el agente padre | Cursor docs, `@cursor/sdk` |
| **Claude Code** | Sesion interactiva con tools de filesystem, shell, Git | No existe como concepto; usa "sub-tasks" via `Task` tool con prompt delegado | Anthropic, Claude Code docs |
| **GitHub Copilot** | Chat + inline completions + agent mode (workspace-aware) | No existe como concepto; "agent mode" es una capa sobre el chat | GitHub Copilot docs, 2026 |
| **Codex (OpenAI)** | Sandbox remoto + tools + agent loop declarativo | No documentado publicamente como concepto separado | OpenAI Codex CLI docs |
| **LangChain / LangGraph** | Nodo en un grafo dirigido con tools y estado | Nodo delegado con su propio state-machine; la distincion es fluida | LangGraph docs, 2026 |
| **CrewAI** | Rol con objetivo, backstory, tools y delegacion | "Crew" de agentes colaborativos; no hay jerarquia padre-hijo rigida | CrewAI docs, 2026 |
| **AWS Bedrock AgentCore** | Sesion en microVM con tools, skills, memory, identity | Orquestador-worker: uno delega, otros ejecutan | AWS docs, GA junio 2026 |
| **Anthropic (patrones)** | Entidad que ejecuta tools en loop; 5 patrones canonicos | "Orchestrator-workers": uno planifica, varios ejecutan | Anthropic, "Building effective agents", 2025 |
| **Academia (agentes)** | Sistema autonomo con percepcion, razonamiento, actuacion y aprendizaje | Jerarquia de agentes con delegacion de sub-tareas | Russell & Norvig, AIMA 4th ed. |

**Conclusion:** No hay un contrato comun. Cada producto define "agente" y "subagente" segun su arquitectura interna. Lo unico transversal es la nocion de "modelo + tools + loop", que sdd-kit ya aborda como **orquestacion del ciclo SDD**, sin etiquetar quien ejecuta.

### 1.2 La distincion prompt-vs-agent es inestable

En 2025, la industria trazaba una linea clara: prompt engineering (texto) vs agent engineering (tools + loop). En 2026, esa linea se difumino:

- Cursor: el "agent" es el modo por defecto del chat; el prompt es un caso particular
- Claude: la sesion es inherentemente agentica si tiene acceso a tools
- Copilot: "agent mode" es una configuracion de alcance de workspace, no una categoria arquitectonica

Lo que hoy se llama "agente" podria llamarse "modo extendido" en 6 meses. Fijar esa taxonomia en el core del kit es garantia de obsolescencia.

---

## 2. Evidencia de fragmentacion

### 2.1 Cursor: Task tool y subagentes tipados

Cursor define subagentes como invocaciones de la `Task` tool con un `subagent_type` fijo. Los tipos disponibles hoy (`explore`, `shell`, `generalPurpose`, `bugbot`, `security-review`, `ci-investigator`, `best-of-n-runner`) son especificos de Cursor y no tienen equivalente en Claude Code ni en Copilot.

```json
// Ejemplo de invocacion de subagente en Cursor (no portable)
{
  "tool": "Task",
  "subagent_type": "explore",
  "description": "Explorar estructura del proyecto",
  "prompt": "Mapea la arquitectura de carpetas..."
}
```

Este contrato no existe en ningun otro IDE. Si sdd-kit lo adoptara como concepto propio, se acoplaria a Cursor y quedaria roto en Claude, Codex o Copilot.

### 2.2 La inestabilidad de los tipos de subagente

Los tipos de subagente en Cursor ya cambiaron entre versiones y no hay garantia de estabilidad. El tipo `explore` podria dividirse en `deep-explore` y `quick-explore` en una version futura. El tipo `bugbot` es un alias de un patron de revision que podria desaparecer o renombrarse.

Para el kit, el costo de mantenimiento de sincronizar estos tipos con cada release de cada IDE es inviable.

### 2.3 El agente como runtime, no como concepto metodologico

La confusion de fondo es que algunos frameworks tratan "agente" como un runtime (LangGraph, CrewAI) y otros como un rol en el proceso (Cursor, Claude Code). sdd-kit opera en la capa de proceso: define **que hacer** (estados, verificacion, gates) pero no **quien lo hace** (un solo agente, varios, subagentes).

---

## 3. Alineacion con las invariantes del kit

### 3.1 Regla 1: Core agnostico al stack

`domain-rules.md`, regla 1:

> **Core agnostico al stack** — `core/` no menciona Laravel, React, Python, etc.

Por extension, `core/` tampoco debe mencionar Cursor, Claude, LangChain o cualquier runtime de ejecucion. Una definicion de "subagente" en `core/` seria equivalente a mencionar "Cursor Task tool" en el workflow: viola la invariante.

### 3.2 Regla 2: Perfiles autocontenidos

Si un perfil requiere comportamiento multi-agente (ej. `sdd-kit` usando `bugbot` para review), esa informacion vive en `profiles/sdd-kit/`, no en `core/`. El core no necesita saber si el agente delega en subagentes o ejecuta todo en secuencia.

### 3.3 Lo que el kit SI define (y es suficiente)

| Necesidad real | Como la cubre sdd-kit hoy | Sin acoplarse a runtime |
|----------------|---------------------------|-------------------------|
| Orquestacion del ciclo | Estados: Discovery → Draft → Ready → In Build → Validating → Released | Transiciones semanticas, no invocaciones de API |
| Delegacion de tareas | Skills `sdd-*` (draft, build, verify, pr, release) | El IDE decide como ejecutar la skill (agente unico, subagente, etc.) |
| Verificacion | `verify-implementation`, `validate-sdd`, CI gates | Checks deterministas, no dependientes del runtime |
| Gates humanos | Ready (aprobar spec), merge (aprobar PR) | Independientes de como se genero el codigo |
| Trazabilidad | `BACKLOG.md`, `archive/`, `releases/` | Estado persistente en archivos, no en memoria del agente |

---

## 4. Riesgos de incorporar agentes/subagentes

### 4.1 Acoplamiento a producto

Si sdd-kit definiera "subagente" hoy, se acoplaria al modelo de Cursor (Task tool con tipos). Si manana Cursor cambia el API o aparece un nuevo IDE dominante, el core quedaria obsoleto o requeriria refactors de breaking change.

### 4.2 Complejidad innecesaria

El ciclo SDD actual tiene 6 estados. Agregar una capa de "quien ejecuta que con que tipo de subagente" multiplicaria la complejidad sin beneficio metodologico: el spec no es mejor si lo escribio un agente solo o un orquestador con workers.

### 4.3 Perdida del foco metodologico

sdd-kit es un producto de metodologia y tooling, no un runtime de agentes. Competiria con LangGraph, CrewAI o el propio Cursor SDK en un terreno donde no tiene ventaja y donde la innovacion es demasiado rapida para estabilizar un contrato.

### 4.4 Violacion de la regla 6

`domain-rules.md`, regla 6:

> Documentacion SDD solo en `paths.sdd`

Si el kit definiera agentes/subagentes en `core/`, estaria creando un contrato de runtime que no pertenece al proceso SDD ni al contexto de negocio del kit.

---

## 5. Que SI puede hacer el kit (sin romper invariantes)

### 5.1 Skills como unidad de delegacion

Las skills `sdd-*` ya son la interfaz correcta: definen **que tarea** ejecutar, no **como** el IDE la despacha. El IDE decide si usa un agente unico, un subagente o un worker pool. El kit solo provee la skill y espera el resultado.

### 5.2 Perfiles que documenten patrones de ejecucion

Un perfil (`profiles/sdd-kit/`) puede documentar patrones recomendados de ejecucion (ej. "usa bugbot para review pre-PR en Cursor"), pero como guia, no como contrato.

### 5.3 Adaptadores por IDE (capa bootstrap)

La capa `bootstrap/adapters/` ya inyecta reglas especificas por IDE. Si en el futuro un IDE requiere instrucciones sobre uso de subagentes, estas iran en el adaptador correspondiente, no en `core/`.

### 5.4 Observabilidad agnostica

Lo que si es pertinente al core es definir **que evidencias** debe producir una ejecucion (verify results, criterios cumplidos, reglas de dominio respetadas), no **quien** las produce. Esto ya esta en `verify-implementation`.

---

## 6. Recomendacion final

**No definir "agente" ni "subagente" en el core de sdd-kit.** La decision se fundamenta en:

1. **Fragmentacion del concepto**: no hay estandar entre IDEs, frameworks ni academia
2. **Invariante rota**: `core/` no debe mencionar runtimes especificos
3. **Suficiencia del diseno actual**: estados, skills, verify y gates humanos cubren la orquestacion sin acoplarse
4. **Riesgo de obsolescencia**: el concepto evoluciona mas rapido que el ciclo de release del kit

Si el humano mantenedor decide que un perfil o adaptador necesita instrucciones sobre subagentes, el lugar correcto es `profiles/<nombre>/` o `bootstrap/adapters/`, nunca `core/`.

---

## 7. Fuentes

### Definiciones de agente por producto

1. Cursor. (2026). "Agent Tools and Task Tool." Cursor Docs. https://docs.cursor.com/
2. Anthropic. (2025). "Building effective agents." https://www.anthropic.com/engineering/building-effective-agents
3. Anthropic. (2026). "Claude Code overview." https://docs.anthropic.com/en/docs/claude-code
4. GitHub. (2026). "GitHub Copilot agent mode." https://docs.github.com/en/copilot
5. OpenAI. (2026). "Codex CLI." https://github.com/openai/codex
6. LangChain. (2026). "LangGraph: Agent orchestration." https://langchain-ai.github.io/langgraph/
7. CrewAI. (2026). "CrewAI Documentation." https://docs.crewai.com/
8. AWS. (2026-06). "Amazon Bedrock AgentCore." https://aws.amazon.com/bedrock/agentcore/

### Inestabilidad de taxonomias

9. Bornstein, M. (2025). "Agents vs. Agentic: What's the Difference?" IEEE Spectrum. https://spectrum.ieee.org/ai-agents
10. Ng, A. (2025). "Agentic Design Patterns." DeepLearning.AI. https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-1/
11. Russell, S., Norvig, P. (2020). "Artificial Intelligence: A Modern Approach." 4th Edition. Pearson. (Definicion clasica de agente inteligente)

### Fragmentacion de subagentes

12. Cursor. (2026). "Subagent types and Task tool." Cursor SDK docs. https://docs.cursor.com/sdk
13. Aakash Gupta. (2026). "The Subagent Problem." Product Growth. https://www.aakashgupta.com/

### Harness engineering (marco de referencia del kit)

14. Hansen, V. (2026-07-07). "Harness Engineering: The Complete Guide." DevOps.dev. https://blog.devops.dev/harness-engineering-the-complete-guide-to-the-discipline-redefining-ai-in-2026-faac2edacda5
15. Fowler, M. (2026). "Harness Engineering for Coding Agent Users." https://martinfowler.com/articles/harness-engineering.html

### Reglas del kit (fuente primaria)

16. sdd-kit. (2026). `domain-rules.md` — Principios de diseno, reglas 1, 2, 6, 7.
17. sdd-kit. (2026). `sdd-agent-workflow.mdc` — Ciclo y restricciones del agente.
