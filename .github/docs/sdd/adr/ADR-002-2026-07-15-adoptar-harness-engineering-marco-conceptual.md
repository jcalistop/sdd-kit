# ADR-002 — Adoptar Harness Engineering como marco conceptual del kit

---

## Cabecera

| Campo                  | Valor                                                                                                    |
| ---------------------- | -------------------------------------------------------------------------------------------------------- |
| **ID**                 | `ADR-002`                                                                                                |
| **Fecha**              | 2026-07-15                                                                                               |
| **Estado**             | `Aceptado`                                                                                               |
| **Specs relacionados** | `SDD-008` (lenguaje guias/sensores), `SDD-009` (posicionamiento docs), `SDD-010` (observabilidad)       |
| **Reemplaza**          | —                                                                                                        |

---

## Contexto / problema

sdd-kit **ya es un agent harness** en los hechos: define reglas, skills, verificaciones, orquestacion del ciclo SDD y gates humanos alrededor del agente de coding. Sin embargo, no usa ese lenguaje en su documentacion ni en su posicionamiento publico.

La disciplina de Harness Engineering emerge formalmente en Q1 2026 a partir del articulo de Mitchell Hashimoto "My AI Adoption Journey" y es adoptada por Thoughtworks, Martin Fowler, Anthropic, AWS y Stripe. La investigacion academica (Meta-Harness de Stanford, AHE de NexAU, Harness-Bench de Peking University) demuestra que el harness —no el modelo— es el factor determinante en la calidad del output del agente, con brechas de hasta 6x sobre el mismo modelo base.

El mapeo realizado en `.github/docs/sdd/research/2026-07-15-harness-engineering.md` muestra que sdd-kit cubre los 7 componentes canonicos de un harness (tools, memory, guardrails, verification, orchestration, observability, human gates), aunque con areas de mejora en sensores computacionales avanzados y observabilidad a nivel trayectoria.

No adoptar el termino "harness engineering" es perder una oportunidad de alineacion con el vocabulario de la industria y de comunicacion con desarrolladores que ya conocen el concepto. Sin embargo, la adopcion debe ser progresiva y complementaria: no reemplaza la metodologia SDD, la enmarca.

---

## Decision

**sdd-kit adopta el paradigma Harness Engineering como marco conceptual complementario. El kit se posiciona como un agent harness para coding agents, preservando su identidad como producto de metodologia y tooling.**

**Detalle:**

1. El termino "harness engineering" se incorpora como capa conceptual en documentacion, reglas y skills del agente, **sin reemplazar** el vocabulario operativo actual (spec, verificar, checklist, DoR/DoD).

2. Los conceptos de **guia** (guide/feedforward) y **sensor** (sensor/feedback) de Martin Fowler se adoptan como taxonomia interna para clasificar los mecanismos de control del kit:
   - **Guia**: instrucciones que previenen errores antes de actuar (domain-rules, checklists DoR, perfiles stack, skills, plantillas)
   - **Sensor**: verificaciones que detectan errores despues de actuar (verify-implementation, validate-sdd, CI gates, DoD, revision humana)

3. La implementacion se escalona en tres specs incrementales ya en Draft:
   - **SDD-008**: inyectar lenguaje guia/sensor en reglas y skills del agente (bajo riesgo, solo vocabulario)
   - **SDD-009**: posicionar el kit como agent harness en documentacion publica (README, concepts, agent-setup)
   - **SDD-010**: refactorizar `validate-sdd` con mensajes por componente harness (herramientas, guias, sensores, memoria, orquestacion)

4. La identidad del producto no cambia: sdd-kit sigue siendo "metodologia + tooling para desarrollo spec-first con agente IA". Harness Engineering es el **marco conceptual** que explica por que funciona, no un nuevo nombre del producto.

5. El principio de adopcion incremental se mantiene: no se exige reescribir documentacion existente ni forzar el termino en specs ya cerrados. Los nuevos specs y la documentacion publica incorporan el lenguaje de forma natural.

**Alternativas descartadas:**

| Alternativa | Razon |
| ----------- | ----- |
| No adoptar el termino y mantener solo "metodologia SDD" | Perdida de oportunidad de alineacion con la industria. El kit ya es un harness; no usar el termino es invisibilidad, no neutralidad. |
| Reemplazar "SDD" por "Harness Engineering" como identidad del producto | Confunde a usuarios existentes. SDD es el metodo; harness engineering es el marco conceptual que lo explica. Son complementarios, no sustitutivos. |
| Adoptar los 7 componentes como taxonomia obligatoria en todos los specs | Complejidad innecesaria. La taxonomia guia/sensor es suficiente para el agente; los 7 componentes son utiles para analisis y comunicacion, no para ejecucion diaria. |
| Implementar todo en un solo spec | Riesgo alto: cambios en reglas, docs y CLI simultaneamente sin validacion incremental. Los tres specs (SDD-008, 009, 010) son independientes y construyen capa sobre capa. |
| Adoptar el ciclo evaluate-analyze-improve (Meta-Harness, AHE) | Choca con la invariante #4 (agente ejecuta, humano aprueba). El kit no es un optimizador automatico de harness; es un harness estable que el humano mejora via specs. |

---

## Consecuencias

**Positivas:**

- **Alineacion con la industria**: el kit habla el mismo lenguaje que Thoughtworks, Martin Fowler, Anthropic, AWS y Stripe. Desarrolladores que conocen harness engineering entienden inmediatamente el valor del kit.
- **Claridad conceptual para el agente**: la distincion guia/sensor da al agente un modelo mental mas preciso de su propio entorno de ejecucion, mejorando la calidad del output sin cambiar comportamiento.
- **Hoja de ruta clara**: los 7 componentes del harness son un mapa de madurez que permite priorizar mejoras futuras (ej. sensores computacionales, observabilidad de trayectoria).
- **Preservacion de identidad**: SDD sigue siendo el metodo; harness engineering es el "por que funciona". No se aliena a usuarios existentes.
- **Adopcion incremental**: los tres specs (SDD-008, 009, 010) son de bajo riesgo, independientes y construyen capa sobre capa. Cada uno puede implementarse y validarse por separado.

**Negativas / deuda:**

- **Termino en ingles**: "harness engineering", "guide", "sensor" son terminos en ingles en un proyecto documentado en español. Se mantienen en ingles por ser el vocabulario canonico de la disciplina.
- **Curva de aprendizaje**: usuarios nuevos deben entender dos capas conceptuales (SDD + harness engineering). Mitigacion: la documentacion trata harness engineering como "el marco que explica SDD", no como un segundo sistema que aprender.
- **Riesgo de sobre-ingenieria**: si el equipo fuerza la taxonomia de 7 componentes en cada decision, se burocratiza el proceso. Los 7 componentes son herramienta de analisis, no checklist obligatorio.

**Modulos afectados:**

- `core/` — cambios de vocabulario en reglas y documentacion (SDD-008, SDD-009); sin cambios de logica
- `bootstrap/agent-skills/sdd-*` — skills reciben terminologia guia/sensor (SDD-008)
- `cli/sdd.py` — `validate-sdd` recibe mensajes por componente (SDD-010)
- `.github/docs/business/domain-rules.md` — nota de adopcion del paradigma (SDD-008)
- `.github/docs/sdd/research/2026-07-15-harness-engineering.md` — informe que fundamenta esta decision

---

## Plan de validacion

- [ ] SDD-008 implementado: reglas y skills usan consistentemente guia/sensor sin romper validate-sdd
- [ ] SDD-009 implementado: README, concepts y agent-setup posicionan el kit como agent harness
- [ ] SDD-010 implementado: validate-sdd emite reporte por componente harness sin falsos positivos
- [ ] `python cli/sdd.py validate` en verde tras los tres specs
- [ ] Ningun spec cerrado antes de v1.3.0 fue modificado para forzar terminologia harness
- [ ] La documentacion publica no reemplaza "SDD" por "harness engineering"; los presenta como complementarios

---

## Notas

- Este ADR se origina en el informe de investigacion `.github/docs/sdd/research/2026-07-15-harness-engineering.md` (17 fuentes: Hashimoto, Fowler, Thoughtworks, Stanford, AWS, Stripe, Anthropic).
- La decision de **no** adoptar el ciclo evaluate-analyze-improve se registro por separado en el informe de investigacion (seccion 6, atributo #7) y se confirma aqui: choca con la invariante #4 de `domain-rules.md`.
- Relacion con ADR-001: ambas decisiones refuerzan el principio de core agnostico. ADR-001 prohibe acoplar el core a un runtime de subagentes; ADR-002 adopta un marco conceptual que es independiente del runtime.
- El termino "agent harness" es el estandar de la industria en 2026. Anthropic renombro su SDK como "agent harness"; AWS Bedrock AgentCore lo usa como nucleo de su producto. No adoptarlo seria una omision estrategica, no una decision de diseno.
