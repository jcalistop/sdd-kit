# ADR-001 — No definir "agente" ni "subagente" en el core del kit

---

## Cabecera

| Campo                  | Valor                                                                                                    |
| ---------------------- | -------------------------------------------------------------------------------------------------------- |
| **ID**                 | `ADR-001`                                                                                                |
| **Fecha**              | 2026-07-15                                                                                               |
| **Estado**             | `Aceptado`                                                                                               |
| **Specs relacionados** | `SDD-007` (safe-git, Released), `SDD-008` (lenguaje harness, Released)                                  |
| **Reemplaza**          | —                                                                                                        |

---

## Contexto / problema

El termino "agente" y "subagente" es polisemico en el ecosistema actual de IA. Cada IDE, framework y proveedor de modelo define estos conceptos segun su arquitectura interna, sin un estandar comun:

- **Cursor IDE** define "subagente" como invocacion de la `Task` tool con tipos fijos (`explore`, `shell`, `bugbot`, etc.).
- **Claude Code** no tiene el concepto de subagente; usa "sub-tasks" via `Task` tool.
- **GitHub Copilot** carece del concepto; "agent mode" es una configuracion de alcance, no una categoria arquitectonica.
- **LangGraph** y **CrewAI** modelan agentes como nodos en grafos o roles en crews, sin jerarquia padre-hijo rigida.
- **AWS Bedrock AgentCore** define orquestador-worker.
- La **academia** (Russell & Norvig) define agente como sistema autonomo con percepcion, razonamiento y actuacion, sin mencion "subagente".

En paralelo, el usuario del kit pregunto si la falta de definicion de agentes y subagentes constituye una debilidad del proyecto. La respuesta fue negativa, pero se requiere una decision arquitectonica formal que registre el fundamento y evite que futuras contribuciones introduzcan este acoplamiento.

---

## Decision

**sdd-kit no definira "agente" ni "subagente" en `core/`. La capa de proceso SDD permanece independiente del runtime de ejecucion del IDE.**

**Detalle:**

1. `core/` no contendra taxonomia, definicion ni contrato sobre agentes, subagentes o jerarquias de delegacion.
2. Las skills `sdd-*` (draft, build, verify, pr, release) son la unidad de delegacion: definen **que tarea** ejecutar, no **como** el IDE la despacha.
3. Si un perfil o adaptador requiere instrucciones sobre subagentes (ej. `profiles/sdd-kit/` documentando uso de `bugbot` para review), esa informacion vive en `profiles/<nombre>/` o `bootstrap/adapters/`, nunca en `core/`.
4. El contrato del kit con el agente sigue siendo: estados semanticos del ciclo (Discovery → Draft → Ready → In Build → Validating → Released), gates humanos (Ready, merge) y verificacion determinista (`verify-implementation`, `validate-sdd`).

**Alternativas descartadas:**

| Alternativa | Razon |
| ----------- | ----- |
| Definir un modelo canonico de agente/subagente en `core/` | Viola la regla 1 de `domain-rules.md` (core agnostico al stack). El concepto no tiene estandarizacion; cualquier definicion quedaria obsoleta en meses o acoplada a un producto especifico. |
| Adoptar el modelo de subagentes de Cursor como contrato del kit | Acopla el core a un solo IDE. Cursor puede cambiar su API de Task tool o sus tipos de subagente en cualquier release. Los otros IDEs (Claude, Copilot, Codex) no tienen el mismo modelo. |
| Delegar la decision a cada perfil sin pronunciarse en core | No es suficiente: el ADR debe registrar la decision negativa para que contribuciones futuras no introduzcan el acoplamiento por error. La ausencia de ADR es ambiguedad. |
| Crear una capa de abstraccion multi-runtime en `core/` | sdd-kit es un producto de metodologia y tooling, no un runtime de agentes. Competiria con LangGraph, CrewAI o el propio Cursor SDK en un terreno donde no tiene ventaja y donde la innovacion es demasiado rapida para estabilizar un contrato. |

---

## Consecuencias

**Positivas:**

- **Core agnostico preservado**: la regla 1 de `domain-rules.md` se mantiene intacta. Ningun cambio en IDEs o frameworks obliga a modificar `core/`.
- **Estabilidad del producto**: el ciclo SDD y sus artefactos (specs, BACKLOG, releases) no dependen de como el IDE orquesta internamente la ejecucion.
- **Adopcion universal**: el kit funciona igual en Cursor, Claude Code, Codex, Copilot o cualquier IDE futuro, sin configuracion adicional.
- **Deuda tecnica evitada**: no habra que mantener sincronizacion con APIs de subagentes que cambian entre versiones de cada IDE.

**Negativas / deuda:**

- **Sin guia explicita sobre delegacion**: el kit no prescribe si una skill debe ejecutarse en agente unico o con subagentes. Esto queda a criterio del usuario o del adaptador del IDE. En la practica, la mayoria de los usuarios delegan esto al IDE sin friccion.
- **Revision via subagente no estandarizada**: patrones como "bugbot para review pre-PR" no tienen un contrato en `core/`. Si se vuelven una necesidad comun, deberan documentarse en `profiles/sdd-kit/` o en `bootstrap/adapters/`, no en el core.

**Modulos afectados:**

- `core/` — confirmado: sin cambios. La decision es negativa (no hacer).
- `profiles/sdd-kit/` — puede documentar patrones de ejecucion con subagentes como guia, no como contrato.
- `bootstrap/adapters/` — puede inyectar instrucciones especificas de subagentes por IDE si el usuario lo requiere.
- `.github/docs/sdd/research/2026-07-15-agentes-subagentes.md` — informe de investigacion que fundamenta esta decision.

---

## Plan de validacion

- [ ] Verificar que ninguna regla, skill o template en `core/` mencione "subagente", "Task tool", "explore agent" o terminos equivalentes de un IDE especifico.
- [ ] Confirmar que `install-agents.py` no inyecta definiciones de agentes/subagentes en los adaptadores sin intervencion explicita del usuario.
- [ ] Si un spec futuro propone definir agentes/subagentes en `core/`, este ADR debe ser reemplazado (no ignorado) con justificacion de cambio de contexto.

---

## Notas

- Este ADR se origina en una sesion de contexto del proyecto (2026-07-15) donde el usuario pregunto si la omision de agentes/subagentes era una debilidad. La respuesta negativa se fundamento con evidencia de fragmentacion del ecosistema.
- El informe de investigacion completo esta en `.github/docs/sdd/research/2026-07-15-agentes-subagentes.md`, con 17 fuentes (productos, academia, taxonomias).
- Relacion con `SDD-007`: el contrato safe-git aplica al agente que ejecuta, independientemente de si es unico o delega en subagentes. No requiere definicion de subagente para ser efectivo.
