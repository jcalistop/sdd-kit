# SDD-008 — Lenguaje guías/sensores (harness) en prompts del agente SDD

---

## Cabecera

| Campo                 | Valor                           |
| --------------------- | ------------------------------- |
| **ID**                | `SDD-008`                       |
| **Dominio**           | `core`                          |
| **Tipo**              | `feature` + `documentation`     |
| **Fecha**             | 2026-07-15                      |
| **Estado**            | `Draft`                         |
| **Version objetivo**  | `v1.3.0`                        |
| **Owner**             | mantenedor                      |
| **Prioridad**         | `P2`                            |
| **ADRs relacionados** | —                               |
| **Dependencias**      | —                               |

---

## Problema y objetivo

**Problema:**

El agente SDD recibe instrucciones como "verifica domain-rules", "auto-verificar DoR", "quality gates", "criterios de aceptacion", "arquitectura sana". Estos son terminos operativos que describen acciones, pero no transmiten la intencion estructural: cuales son **guias** (feedforward — previenen errores antes de actuar) y cuales son **sensores** (feedback — detectan errores despues de actuar).

La disciplina emergente de harness engineering (Mitchell Hashimoto, Martin Fowler, Thoughtworks 2026) formaliza esta distincion. Adoptarla en sdd-kit daria al agente un modelo mental mas claro de su propio harness, mejorando precision sin cambiar comportamiento.

**Objetivo:**

Incorporar los conceptos de **guia** (guide/feedforward) y **sensor** (sensor/feedback) en las reglas, skills y prompts del agente SDD, preservando el vocabulario operativo actual como complemento. Incluir nota de posicionamiento en `domain-rules.md` sobre la adopcion del marco harness engineering.

---

## Alcance

**Incluye:**

- `sdd-agent-workflow.mdc`: glosario minimo "guia vs sensor" en cabecera; referencias a sensores en verify y validacion
- `sdd-workflow-reference.mdc`: etiquetar cada checklist DoR/DoD como guia o sensor segun su naturaleza
- Skills `sdd-build-spec` y `sdd-verify-implementation`: introducir terminos en descripciones y procedimientos
- `domain-rules.md`: nota explicita de adopcion del paradigma harness engineering como marco conceptual del kit
- `core/prompt-catalog.md`: nota breve en la seccion "Momentos semanticos vs prompts"

**Excluye explicitamente:**

- Cambios de comportamiento del agente o del ciclo SDD
- Nuevos sensores computacionales adicionales (eso va en SDD futuro)
- Trazas de ejecucion (trajectory) — SDD futuro
- Guardrails como codigo — ya cubierto por SDD-007
- Modificar `validate-sdd` — SDD-010
- Perfiles de stack individuales

---

## Impacto tecnico

> Perfil: `sdd-kit`. Tabla segun `profiles/sdd-kit/spec-impact.md`.

| Item                        | Impacto                                                                                   |
| --------------------------- | ----------------------------------------------------------------------------------------- |
| **core/**                   | Bajo — cambios de vocabulario en reglas, skills y documentacion; sin cambios de logica     |
| **profiles/**               | No aplica — el cambio es transversal al core, no especifico de stack                       |
| **bootstrap/**              | Bajo — skills `sdd-build-spec` y `sdd-verify-implementation` reciben terminologia harness |
| **cli/**                    | No aplica — `validate-sdd` no se modifica en este spec                                    |
| **docs/**                   | Medio — `domain-rules.md` recibe nota de posicionamiento; `prompt-catalog.md` nota breve  |
| **BD o schema**             | No aplica                                                                                 |
| **CI**                      | No aplica — sin cambios en quality gates                                                  |
| **Seguridad**               | No aplica                                                                                 |
| **Compatibilidad**          | Alta — solo se renombran conceptos; todos los terminos actuales se preservan              |
| **Instancias consumidoras** | Transparente — los terminos guia/sensor son complementarios, no reemplazan vocabulario     |

---

## Reglas de negocio

> Aplica `domain-rules.md` principios #1 (core agnostico), #4 (agente ejecuta, humano aprueba), #6 (documentacion solo en paths.sdd).

Particularidad de este spec: la terminologia harness no se impone como reemplazo sino como **capa conceptual complementaria**. El vocabulario operativo ("verifica", "criterios", "checklist") se preserva.

---

## Criterios de aceptacion

**Happy path:**

- [ ] `sdd-agent-workflow.mdc` incluye glosario guia/sensor con ejemplos concretos del ciclo SDD
- [ ] `sdd-workflow-reference.mdc` etiqueta cada item DoR/DoD como [guia] o [sensor] sin alterar contenido
- [ ] Skills `sdd-build-spec` y `sdd-verify-implementation` mencionan guias y sensores en su descripcion
- [ ] `domain-rules.md` incluye nota explicita "sdd-kit adopta el paradigma harness engineering" con enlace a fuente
- [ ] `core/prompt-catalog.md` incluye nota breve sobre la distincion guia/sensor
- [ ] `python cli/sdd.py validate` sin errores tras cambios
- [ ] Ningun cambio rompe el comportamiento del agente ni modifica el ciclo SDD

**Error path:**

- [ ] Si un termino nuevo genera confusion en el agente (ej. aplica sensor donde deberia aplicar guia), se revierte en el archivo especifico
- [ ] Si `validate-sdd` detecta inconsistencia, se corrige antes de merge

---

## Diseno tecnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `.cursor/rules/sdd-agent-workflow.mdc` | Agregar glosario guia/sensor tras "Referencia on-demand" |
| `.cursor/rules/sdd-workflow-reference.mdc` | Etiquetas [guia]/[sensor] en listas DoR/DoD |
| `bootstrap/agent-skills/sdd-build-spec/SKILL.md` | Mencion "guias (feedforward)" en descripcion; nota en procedimiento |
| `bootstrap/agent-skills/sdd-verify-implementation/SKILL.md` | Mencion "sensores (feedback)" en descripcion; nota en checklist |
| `.github/docs/business/domain-rules.md` | Agregar seccion "Adopcion del paradigma harness engineering" |
| `core/prompt-catalog.md` | Agregar nota sobre distincion guia/sensor |

**Glosario propuesto (a incluir en sdd-agent-workflow.mdc):**

| Termino | Definicion | Ejemplo en SDD |
| ------- | ---------- | -------------- |
| **Guia (guide)** | Instruccion feedforward: previene errores antes de actuar | `domain-rules.md`, `sdd.config.yaml`, perfil stack, DoR checklist |
| **Sensor (sensor)** | Verificacion feedback: detecta errores despues de actuar | `verify-implementation`, `validate-sdd`, CI quality gates, DoD checklist |

---

## Verificacion tecnica

```bash
python cli/sdd.py validate
python -m compileall -q cli/
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigacion |
| ------ | ------------ | ------- | ---------- |
| Terminologia confunde al agente en vez de ayudar | Baja | Medio | Preservar vocabulario operativo; guia/sensor como capa complementaria |
| Cambio en domain-rules.md crea inconsistencia con otros specs | Baja | Bajo | Validar con `validate-sdd`; solo se agrega nota, no se modifica reglas |
| Romper formato de rules/skills | Baja | Alto | Revisar diff antes de commit; CI con compileall |

Rollback: revertir cada archivo individualmente; sin dependencias entre cambios.

---

## Notas post-implementacion

- Este spec es el primero de una serie harness engineering: seguiran SDD-009 (posicionamiento docs) y SDD-010 (observabilidad validate-sdd).
- Si el agente muestra mejora medible en precision tras adoptar terminos, documentar en `business/planning/`.
