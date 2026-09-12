# Guía — Research (`research/`)

> Metodología canónica del kit (producto). **No** es un plan de auditoría ni el [`releases/RUNBOOK.md`](../releases/RUNBOOK.md) de release de producto.
> Carpeta de notas: opcional bajo `paths.sdd/research/` de cada instancia. Plantilla: [`templates/research-nota-template.md`](../templates/research-nota-template.md).

---

## Glosario

| Término | Qué es |
| ------- | ------ |
| **Metodología** | Esta guía (reutilizable) |
| **Nota** | Artefacto de *esta* investigación (pregunta + hallazgos + implicaciones). **Default.** |
| **Ensayo largo** | Extensión opcional de una nota; la plantilla **no** lo exige |

---

## Research vs audits

| | **research/** | **audits/** |
| --- | --- | --- |
| Pregunta | ¿Qué aprendimos o qué marco adoptamos? | ¿Está sano y qué hay que arreglar? |
| Forma | Nota / ensayo (ensayo largo opcional) | Corrida con alcance, evidencias, cierre |
| Tablero | **No** es cola operativa (puede orientar un ADR o Discovery) | Alimenta Discovery / specs |

Metodología de audits: [audits.md](audits.md).

---

## Cuándo research vs audit vs ADR vs spec

| Usar | Cuando |
| ---- | ------ |
| **Research** | Explorar una idea, marco o literatura; documentar aprendizaje **sin** comprometer cambio de producto aún |
| **Audit** | Evaluar el estado actual del kit/proceso; producir gaps accionables → BACKLOG |
| **ADR** | Decisión arquitectónica transversal **ya tomada** (o a formalizar) |
| **Spec SDD** | Cambio de producto/proceso con ciclo Draft→Released (`SDD-NNN` en BACKLOG) |

**Prohibido:** inventar un `SDD-NNN` desde una nota de research sin fila en BACKLOG. Si la nota sugiere trabajo: añadir Discovery o draft de spec **después**, con el humano.

---

## Default: una nota

1. Copiar [`templates/research-nota-template.md`](../templates/research-nota-template.md) a `paths.sdd/research/YYYY-MM-DD-slug.md`.
2. Completar pregunta y hallazgos; implicaciones al cerrar.
3. Estados: `Borrador` → `Listo`.
4. **Sin** par plan/informe. Un archivo basta.
5. Ensayo largo: solo si el tema lo requiere; no es el default.

---

## Implicaciones (cierre de la nota)

Al pasar a `Listo`, declarar una de:

| Resultado | Acción |
| --------- | ------ |
| Nada | Aprendizaje archivado; sin follow-up |
| Discovery | Fila en BACKLOG Discovery (idea, no ID aún) |
| ADR | Borrador o enlace a `adr/` (humano aprueba ADR) |
| Spec | Solo si ya hay (o habrá) `SDD-NNN` reflejado en BACKLOG |

Research **no** sustituye tablero, ADR ni spec.

---

## Checklist de cierre

- [ ] Nota en estado **Listo** (pregunta + hallazgos + implicaciones).
- [ ] Índice de `paths.sdd` actualizado (tabla Research, si existe).
- [ ] Merge a la rama de desarrollo del proyecto.
- [ ] Si hubo follow-up: Discovery / ADR / spec enlazado desde Implicaciones.

No aplica stub≠SoT de audits: una nota no es corrida de evaluación con tag.

---

## Plantilla

| Plantilla | Uso |
| --------- | --- |
| [`research-nota-template.md`](../templates/research-nota-template.md) | Default — toda investigación |

---

## Consumidores

No se exige carpeta `research/` en proyectos consumidores. Guía y plantilla viven en el kit para adopción voluntaria.
