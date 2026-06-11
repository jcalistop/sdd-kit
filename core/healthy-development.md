# Guia de desarrollo sano

> Referencia curada de arquitectura, patrones, antipatrones, codigo limpio y calidad.
> Para **humanos** (diseno, implementacion, revision) y **agentes de IA** (specs, codigo, PRs).
>
> **Relacionado:** [`workflow.md`](workflow.md) · [`checklist-pr.md`](checklist-pr.md) · [`adr/README.md`](adr/README.md)

---

## Proposito

Este documento no reemplaza libros ni cursos. Es un **mapa de lectura y checklist practico** para construir software de forma sostenible.

Complementa el ciclo SDD: los specs definen _que_ construir; esta guia orienta _como_ construirlo bien.

| Audiencia  | Uso principal                                                                        |
| ---------- | ------------------------------------------------------------------------------------ |
| **Humano** | Consultar al entrar al proyecto, disenar features, revisar PRs                       |
| **Agente** | Aplicar al redactar diseno tecnico en specs, implementar y auto-revisar antes del PR |

---

## Marco mental

Prioriza en este orden:

1. **Entender el dominio y el problema** — no la tecnologia primero.
2. **Limites claros** — modulos, servicios, capas, contratos.
3. **Simplicidad evolutiva** — poder cambiar sin romper todo.
4. **Calidad verificable** — tests, observabilidad, CI.
5. **Seguridad y operacion** — desde el diseno, no al final.

**Regla de oro:** la solucion mas simple que resuelva el problema actual. La complejidad se justifica con dolor medible, no con hipotesis.

---

## Arquitectura de sistemas

| Guia / marco                                                 | Para que sirve                                                                   |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| **C4 Model** (Simon Brown)                                   | Comunicar arquitectura en 4 niveles: contexto, contenedores, componentes, codigo |
| **12-Factor App**                                            | Apps cloud-native: config, logs, procesos, despliegue                            |
| **Fundamentals of Software Architecture** (Richards & Ford)  | Trade-offs entre monolito, microservicios, event-driven, etc.                    |
| **Software Architecture: The Hard Parts** (Ford et al.)      | Cuando dividir servicios y como manejar datos distribuidos                       |
| **Building Evolutionary Architectures** (Ford, Parsons, Kua) | Arquitectura que evoluciona con fitness functions y CI                           |
| **ADR** (Architecture Decision Records)                      | Documentar _por que_ se eligio X y no Y — ver [`adr/`](adr/README.md)            |

**Regla practica:** empieza simple (monolito modular); divide solo cuando el dolor lo justifique.

---

## Diseno orientado al dominio

| Guia                                                  | Para que sirve                                   |
| ----------------------------------------------------- | ------------------------------------------------ |
| **Domain-Driven Design** (Eric Evans)                 | Ubiquitous language, bounded contexts, agregados |
| **Implementing Domain-Driven Design** (Vaughn Vernon) | Como llevar DDD al codigo                        |
| **DDD Distilled** (Vernon)                            | Version corta y accionable                       |

Util cuando el negocio es complejo. Si el dominio es CRUD simple, no fuerces DDD completo.

---

## Patrones de diseno

| Fuente                                                       | Enfoque                                                |
| ------------------------------------------------------------ | ------------------------------------------------------ |
| **Design Patterns** (Gang of Four)                           | Clasicos: Strategy, Factory, Observer, Decorator, etc. |
| **Patterns of Enterprise Application Architecture** (Fowler) | Repository, Unit of Work, Active Record, etc.          |
| **Enterprise Integration Patterns** (Hohpe & Woolf)          | Mensajeria, colas, routing, sagas                      |
| **Refactoring** (Fowler)                                     | Catalogo de refactorings con nombres estandar          |

**En la practica:** conoce unos 15 patrones bien; el resto consultalos cuando aparezca el problema, no los apliques por moda.

---

## Antipatrones (evitar activamente)

| Antipatron                   | Senal tipica                                   | Accion recomendada                        |
| ---------------------------- | ---------------------------------------------- | ----------------------------------------- |
| **Big Ball of Mud**          | Todo depende de todo, sin limites              | Definir modulos; extraer interfaces       |
| **God Object / God Class**   | Una clase que hace todo                        | Dividir por responsabilidad (SRP)         |
| **Spaghetti code**           | Flujo imposible de seguir                      | Refactor; funciones cortas; tests         |
| **Golden Hammer**            | Usar la misma herramienta para todo            | Evaluar trade-offs; ADR si es transversal |
| **Premature Optimization**   | Optimizar antes de medir                       | Medir primero; optimizar cuellos reales   |
| **Lava Flow**                | Codigo muerto que nadie se atreve a borrar     | Eliminar con tests de regresion           |
| **Copy-Paste Programming**   | Duplicacion de logica de negocio               | Extraer funcion/modulo compartido         |
| **Microservices prematuros** | Muchos servicios para un equipo pequeno        | Monolito modular hasta que duela          |
| **Distributed Monolith**     | Microservicios acoplados como un solo sistema  | Contratos claros; desacoplar datos        |
| **Anemic Domain Model**      | Entidades vacias; toda la logica en "services" | Mover reglas de negocio al dominio        |
| **Over-engineering**         | Abstracciones para un solo caso de uso         | YAGNI; simplificar                        |

**Antidoto habitual:** YAGNI, limites claros, tests, refactor continuo.

---

## Codigo limpio y diseno orientado a objetos

| Guia                                                | Idea central                                               |
| --------------------------------------------------- | ---------------------------------------------------------- |
| **Clean Code** (Robert C. Martin)                   | Nombres, funciones pequeñas, pocos argumentos, legibilidad |
| **The Pragmatic Programmer** (Hunt & Thomas)        | Mentalidad profesional: DRY, tracer bullets, orthogonality |
| **Refactoring** (Fowler)                            | Mejorar diseno sin cambiar comportamiento                  |
| **Working Effectively with Legacy Code** (Feathers) | Cambiar codigo con poca o ninguna red de seguridad         |
| **A Philosophy of Software Design** (Ousterhout)    | Complejidad accidental vs esencial; deep modules           |

### Principios a internalizar

| Principio                        | Resumen                                                          |
| -------------------------------- | ---------------------------------------------------------------- |
| **SOLID**                        | Especialmente SRP, DIP y OCP en codigo que cambia seguido        |
| **DRY**                          | No duplicar _conocimiento_; no obsesionarse con lineas identicas |
| **KISS**                         | La solucion mas simple que funcione                              |
| **YAGNI**                        | No construir para hipotesis futuras                              |
| **Law of Demeter**               | Hablar con vecinos directos, no con toda la cadena               |
| **Composition over inheritance** | Preferir composicion en la mayoria de los casos                  |
| **Fail fast**                    | Errores explicitos y tempranos                                   |
| **Separation of Concerns**       | Una razon de cambio por modulo                                   |

---

## APIs, integracion y datos

| Guia                                                  | Tema                                      |
| ----------------------------------------------------- | ----------------------------------------- |
| **REST** (Fielding) + **OpenAPI**                     | Contratos HTTP claros                     |
| **API Design Patterns** (Lauret)                      | Recursos, errores, versionado, paginacion |
| **Designing Data-Intensive Applications** (Kleppmann) | BD, replicacion, consistencia, streams    |
| **Database Refactoring** (Sadalage & Fowler)          | Evolucionar esquema sin downtime          |

---

## Calidad, testing y entrega

| Guia                                                  | Tema                                           |
| ----------------------------------------------------- | ---------------------------------------------- |
| **Test Pyramid** (Cohn)                               | Muchos unitarios, menos integracion, pocos E2E |
| **Growing Object-Oriented Software, Guided by Tests** | TDD en la practica                             |
| **Continuous Delivery** (Humble & Farley)             | Pipeline, despliegue confiable                 |
| **Accelerate** (Forsgren et al.)                      | Lead time, frecuencia de deploy, MTTR          |

Los perfiles de stack del kit definen quality gates concretos — ver `profiles/<stack>/checklist-stack.md`.

---

## Seguridad y operacion

| Guia                                      | Tema                                     |
| ----------------------------------------- | ---------------------------------------- |
| **OWASP Top 10**                          | Vulnerabilidades web mas comunes         |
| **OWASP ASVS**                            | Checklist de seguridad por nivel         |
| **Site Reliability Engineering** (Google) | SLIs/SLOs, error budgets, observabilidad |
| **The Twelve-Factor App**                 | Config y secretos fuera del codigo       |

Nunca hardcodear secretos. Validar entrada en el borde del sistema. Principio de minimo privilegio en auth.

---

## Checklist por momento del proyecto

### Al entrar a un proyecto

- [ ] Leer ADRs, README y diagrama de contexto (C4 nivel 1–2) si existen
- [ ] Identificar bounded contexts y puntos de integracion
- [ ] Revisar CI, tests y proceso de despliegue
- [ ] Leer [`adoption-guide.md`](adoption-guide.md) y `business/domain-rules.md` si el proyecto usa SDD

### Al disenar una feature (spec Draft / Ready)

- [ ] ¿Que problema de negocio resuelve?
- [ ] ¿Donde vive la logica? (dominio vs infraestructura)
- [ ] ¿Que pasa si falla? (rollback, idempotencia, errores)
- [ ] ¿Como se prueba y observa?
- [ ] ¿Requiere ADR? (decision arquitectonica transversal)
- [ ] ¿La solucion es la mas simple posible? (KISS, YAGNI)

### Al escribir codigo (In Build)

- [ ] Nombres que expliquen intencion
- [ ] Funciones o metodos cortos, una responsabilidad
- [ ] Dependencias explicitas (inyeccion, interfaces en los bordes)
- [ ] Tests en el comportamiento critico (happy path + error path)
- [ ] Quality gates del perfil en verde antes del PR
- [ ] Sin codigo muerto ni comentarios obsoletos

### Al revisar un PR (Validating)

- [ ] ¿Aumenta complejidad innecesaria?
- [ ] ¿Hay acoplamiento nuevo entre capas?
- [ ] ¿Se puede cambiar sin tocar muchos archivos?
- [ ] ¿Hay tests y manejo de errores?
- [ ] ¿El spec y el codigo estan alineados? (DoD SDD)
- [ ] ¿Se detecta algun antipatron de la tabla anterior?

---

## Instrucciones para agentes de IA

Aplicar esta guia al **disenar**, **implementar** y **auto-revisar**. No usarla como excusa para sobre-ingenieria.

### Al redactar o completar un spec

1. **Problema antes que tecnologia.** La seccion "Problema / objetivo" describe el negocio, no la stack.
2. **Alcance explicito.** Incluir exclusiones evita scope creep y abstracciones prematuras.
3. **Diseno tecnico proporcional.** Un bugfix no necesita microservicios; un CRUD no necesita event sourcing.
4. **Criterios de aceptacion verificables.** Deben poder convertirse en tests o checks automaticos.
5. **ADR si aplica.** Decisiones transversales (BD, auth, mensajeria, patron arquitectonico) → proponer ADR, no decidir en silencio.
6. **Reglas de negocio** solo desde `business/domain-rules.md` — no inventar restricciones.

### Al implementar codigo

1. **Seguir el spec.** No agregar features no especificadas sin acordarlo con el humano.
2. **Minimo diff correcto.** Cambiar solo lo necesario; reutilizar patrones existentes del proyecto.
3. **Capas claras.** Logica de negocio en dominio/servicios de aplicacion; infraestructura en adaptadores.
4. **Errores explicitos.** No tragar excepciones; mensajes utiles para operacion y debugging.
5. **Tests en comportamiento critico.** Priorizar paths del spec (aceptacion + error).
6. **Quality gates del perfil** (`checklist-stack.md`) en verde antes de pedir revision.

### Al auto-revisar antes del PR

Ejecutar mentalmente (o en comentario al humano) esta verificacion:

| Pregunta                          | Si la respuesta es "si", actuar          |
| --------------------------------- | ---------------------------------------- |
| ¿Agregue abstraccion sin 2+ usos? | Simplificar (YAGNI)                      |
| ¿Duplique logica de negocio?      | Extraer modulo compartido (DRY)          |
| ¿La clase hace mas de una cosa?   | Dividir (SRP)                            |
| ¿Optimice sin medicion?           | Revertir o documentar medicion           |
| ¿El spec y el codigo divergen?    | Alinear spec o codigo antes del PR       |
| ¿Detecto antipatron de esta guia? | Refactorizar o documentar deuda con plan |

### Prohibido para el agente

- Introducir microservicios, colas o patrones complejos sin requisito en el spec o ADR.
- Asumir reglas de negocio no documentadas en `business/`.
- Dejar codigo muerto, TODOs sin ticket/spec, o `console.log` de debug.
- Ignorar quality gates del perfil stack.
- Proponer reescrituras masivas cuando un cambio local resuelve el problema.

---

## Relacion con SDD Kit

| Practica de esta guia      | Artefacto SDD                           |
| -------------------------- | --------------------------------------- |
| Problema y alcance claros  | Spec (Discovery → Ready)                |
| Decisiones arquitectonicas | ADR en `adr/`                           |
| Criterios verificables     | Criterios de aceptacion + DoD           |
| Calidad automatica         | `checklist-stack.md` del perfil         |
| Contexto de negocio        | `business/README.md`, `domain-rules.md` |
| Trazabilidad de cambios    | BACKLOG, releases, archive              |

---

## Lectura recomendada (poco tiempo)

Orden sugerido si solo puedes leer cinco:

1. **The Pragmatic Programmer** — mentalidad
2. **Clean Code** — dia a dia
3. **Refactoring** — catalogo de mejoras
4. **Designing Data-Intensive Applications** — cuando toques BD, colas o escala
5. **Fundamentals of Software Architecture** — decisiones grandes

---

## Referencias

| Documento                                | Uso                         |
| ---------------------------------------- | --------------------------- |
| [`workflow.md`](workflow.md)             | Ciclo SDD, DoR/DoD          |
| [`checklist-pr.md`](checklist-pr.md)     | DoD de trazabilidad en PRs  |
| [`adr/README.md`](adr/README.md)         | Cuando y como escribir ADRs |
| [`adoption-guide.md`](adoption-guide.md) | Adopcion incremental de SDD |
| `profiles/<stack>/checklist-stack.md`    | Quality gates del stack     |
