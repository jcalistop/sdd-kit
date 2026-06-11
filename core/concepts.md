# SDD en 5 minutos

> Si es tu primera vez con Spec-Driven Development, empieza aqui.
> Si ya conoces la metodologia, puedes saltar directo a [`workflow.md`](workflow.md).

---

## La idea en una frase

**Primero escribes QUE quieres hacer; despues lo construyes.** El documento (spec) es el plano, el codigo es la construccion.

---

## La metafora de la casa

Construir software sin spec es como construir una casa sin plano:

| Sin plano (sin SDD)                                        | Con plano (con SDD)                                |
| ---------------------------------------------------------- | -------------------------------------------------- |
| Empiezas a poner ladrillos directo                         | Dibujas las habitaciones primero                   |
| A medio camino descubres que el baño debia ir al otro lado | El baño ya estaba en el plano                      |
| El electricista no sabe donde van los enchufes             | El plano lo dice                                   |
| El dueño ve la casa terminada y no era lo que pidio        | El dueño aprobo el plano antes del primer ladrillo |

SDD es **escribir el plano** antes de construir. No es burocracia: es evitar tirar paredes abajo despues.

---

## Como funciona (resumen)

1. **BACKLOG.md** — una lista unica con todo lo que hay que hacer (como una pizarra de post-its).
2. **Spec** — un documento breve que describe UNA iniciativa: que problema resuelve, que incluye, que NO incluye, y como sabras que esta lista.
3. **El spec se mueve por 6 estados:** Discovery → Draft → Ready → In Build → Validating → Released. Cada estado dice "en que momento va esto".
4. **El agente (IA) escribe specs y codigo; el humano aprueba** en dos puntos: cuando el spec esta listo (Ready) y cuando el codigo esta para mezclar (merge del PR).

---

## Glosario

| Termino                       | Que significa (en simple)                                                                                                                                                                              |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Spec**                      | Documento que describe una tarea antes de hacerla. Responde: que, por que, como sabre que esta lista.                                                                                                  |
| **BACKLOG**                   | Lista unica de todas las tareas del proyecto, ordenadas por estado.                                                                                                                                    |
| **Dominio**                   | Categoria para agrupar specs (ej. `ux`, `api`, `reportes`). Se definen en `sdd.config.yaml`.                                                                                                           |
| **DoR** (Definition of Ready) | Checklist que verifica que un spec tiene todo lo necesario para empezar a construir.                                                                                                                   |
| **DoD** (Definition of Done)  | Checklist que verifica que lo construido cumple lo prometido y esta listo para produccion.                                                                                                             |
| **ADR**                       | Documento que explica una decision importante de arquitectura (ej. "elegimos PostgreSQL en vez de MySQL porque...").                                                                                   |
| **Release**                   | Una version que se despliega a produccion. Agrupa uno o varios specs terminados.                                                                                                                       |
| **Estado**                    | Etiqueta que indica en que fase esta un spec: `Draft` (borrador), `Ready` (aprobado para construir), `In Build` (en construccion), `Validating` (en revision), `Released` (terminado y en produccion). |
| **Discovery**                 | Fase inicial: una idea anotada en el BACKLOG, sin spec todavia.                                                                                                                                        |
| **Archive**                   | Carpeta donde van los specs ya terminados (`Released`).                                                                                                                                                |
| **ID `—`**                    | Se usa para cambios tan pequeños que no necesitan spec propio (ej. corregir un typo).                                                                                                                  |
| **Perfil stack**              | Configuracion especifica para un tipo de tecnologia (Laravel, FastAPI, React...). Define tests, deploy y checklist tecnico.                                                                            |
| **Dominio de negocio**        | Reglas propias del proyecto (roles, permisos, periodos fiscales) que el agente debe conocer para no inventar. Se documentan en `business/domain-rules.md`.                                             |
| **Submodulo**                 | Forma de incluir el kit SDD dentro de tu proyecto sin copiarlo manualmente. Se actualiza con `git submodule update`.                                                                                   |
| **init-sdd**                  | Script que crea la estructura inicial de SDD en un proyecto nuevo o existente.                                                                                                                         |

---

## Dos caminos para crear specs

SDD ofrece dos plantillas. Elige la que se ajuste a lo que necesitas:

| Plantilla                                                                             | Para que sirve                                            | Ejemplo de uso                                                         |
| ------------------------------------------------------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Completa** ([`templates/spec-template.md`](templates/spec-template.md))             | Features tecnicas, cambios de BD, refactors               | "Agregar endpoint de exportacion Excel con filtros"                    |
| **Simple** ([`templates/spec-simple-template.md`](templates/spec-simple-template.md)) | Tareas no tecnicas, flujos de negocio, mejoras de proceso | "Planificar capacitacion de usuarios", "Rediseñar flujo de aprobacion" |

La plantilla simple es un subconjunto de la completa: **si empiezas con la simple y necesitas mas detalle despues, migrar a la completa es natural** (solo agregas secciones).

Ambas usan los mismos estados (Discovery → Released) y el mismo BACKLOG. No son metodologias distintas; son dos niveles de profundidad de la misma.

---

## Empieza por aqui segun tu perfil

| Si eres...                                  | Lee primero                                                                                      | Despues                                                                                    |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| Desarrollador nuevo en SDD                  | Este documento → [`adoption-guide.md`](adoption-guide.md) Etapa 1                                | [`workflow.md`](workflow.md)                                                               |
| Desarrollador con experiencia en SDD        | [`workflow.md`](workflow.md) directo                                                             | [`adoption-guide.md`](adoption-guide.md) para el setup                                     |
| No tecnico (marketing, operaciones, diseño) | Este documento → ejemplo [`SDD-001-evento-no-tecnico.md`](examples/SDD-001-evento-no-tecnico.md) | [`templates/spec-simple-template.md`](templates/spec-simple-template.md)                   |
| Quieres formalizar reglas de negocio        | [`adoption-guide.md`](adoption-guide.md) seccion "Formalizar el contexto de negocio"             | [`templates/business-domain-template.md`](templates/business-domain-template.md)           |
| Produccion de informes (MD, LaTeX, PDF)     | Este documento → [`reports-latex-md`](../profiles/reports-latex-md/README.md)                    | [`workflow-extensions.md`](../profiles/reports-latex-md/workflow-extensions.md) del perfil |

---

## Referencias

| Documento                                                                        | Uso                                                        |
| -------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| [`workflow.md`](workflow.md)                                                     | Ciclo completo SDD, tipos de spec, DoR/DoD detallados      |
| [`adoption-guide.md`](adoption-guide.md)                                         | Como instalar SDD en proyectos nuevos y existentes         |
| [`healthy-development.md`](healthy-development.md)                               | Arquitectura, patrones, codigo limpio (humanos y agentes)  |
| [`templates/spec-template.md`](templates/spec-template.md)                       | Plantilla completa de spec (tecnica)                       |
| [`templates/spec-simple-template.md`](templates/spec-simple-template.md)         | Plantilla reducida (no tecnica / iniciacion)               |
| [`examples/SDD-001-evento-no-tecnico.md`](examples/SDD-001-evento-no-tecnico.md) | Ejemplo de spec con plantilla simple                       |
| [`../profiles/reports-latex-md/`](../profiles/reports-latex-md/README.md)        | Perfil informes LaTeX/Markdown, transcripcion, publicacion |
