# Flujo Operativo SDD

Metodología spec-driven para un equipo pequeño en producción.
**Principio**: spec antes de código, evidencia antes de despliegue, archivo después de release.

**Release (operación):** [`releases/RUNBOOK.md`](releases/RUNBOOK.md) — cierre en repo, tag SemVer, despliegue según perfil de stack.

**Configuración del proyecto:** `sdd.config.yaml` (ramas, dominios, perfil).

---

## Estructura documental

Todo vive bajo la ruta `paths.sdd` del config (por defecto `.github/docs/sdd/`):

```
.github/docs/sdd/
├── sdd.config.yaml                 # instancia del proyecto
├── PROJECT.md                      # resumen de adopción SDD
├── README.md                       # índice
├── operations.md                   # rituales (puede enlazar al core o copia local)
├── workflow.md                     # este archivo (copia o enlace al kit)
├── BACKLOG.md                      # tablero único de iniciativas
├── checklist-pr.md                 # DoD trazabilidad (+ perfil stack)
├── healthy-development.md          # arquitectura, patrones, codigo limpio
├── templates/
├── specs/<dominio>/SDD-NNN-*.md
├── archive/<YYYY>/<dominio>/SDD-NNN-*.md
├── adr/ADR-*.md
├── releases/RUNBOOK.md
├── releases/README.md
└── releases/vX.Y.Z/
```

**Dominios** se definen en `sdd.config.yaml` → `domains`. Son etiquetas de **iniciativas**, no módulos de negocio (esos viven en `paths.business`).

---

## Ciclo por iniciativa

```
Discovery → Draft → Ready → In Build → Validating → Released
```

| Etapa          | Artefacto                                                | Criterio de salida                                                      |
| -------------- | -------------------------------------------------------- | ----------------------------------------------------------------------- |
| **Discovery**  | notas en BACKLOG                                         | Problema entendido, dominio y tipo declarados                           |
| **Draft**      | `specs/<dominio>/SDD-NNN-slug.md`                        | Definition of Ready (DoR) cumplida                                      |
| **Ready**      | spec con `Estado: Ready`                                 | Aprobación humana; alcance congelado; dependencias resueltas            |
| **In Build**   | código local + evidencia de verificación                 | Quality gates en verde; `verify-implementation` OK; **sin push/PR aún** |
| **Validating** | PR + [`checklist-pr.md`](checklist-pr.md) + perfil stack | DoD cumplida; revisión humana antes de merge                            |
| **Released**   | `archive/<YYYY>/<dominio>/` + entrada en release         | Mergeado, desplegado, archivado                                         |

### Momentos semánticos vs prompts

Los **estados** del spec son la fuente de verdad del progreso. Los **prompts** del [catálogo](prompt-catalog.md) son disparadores copy-paste opcionales; no son fases obligatorias 1:1.

| Concepto              | Qué es                                                               |
| --------------------- | -------------------------------------------------------------------- |
| **Momento semántico** | Cambio de estado, gate o frase humana con criterio en este documento |
| **Prompt**            | Plantilla del catálogo para disparar trabajo del agente              |
| **Regla always-on**   | Comportamiento del agente sin prompt (p. ej. reglas del IDE)         |

Contratos always-on del kit: workflow SDD y [safe-git](safe-git-contract.md) (Git destructivo). Detalle de instalación: [`agent-setup.md`](agent-setup.md).

| Situación                        | ¿Prompt?    | Notas                                             |
| -------------------------------- | ----------- | ------------------------------------------------- |
| Idea nueva (adopción madura)     | No          | El agente sigue el ciclo; describes la necesidad  |
| Adopción, excepciones, upgrade   | Sí          | Tareas puntuales del catálogo                     |
| Aprobar spec → Ready             | Semántico   | Frase basta: _"Apruebo SDD-NNN para implementar"_ |
| Revisar DoR en Draft             | Opcional    | `draft-review`                                    |
| Implementar spec aprobado        | Opcional    | `build-spec` si retomas sesión                    |
| Verificar vs spec (antes de Git) | Obligatorio | `verify-implementation` — gate local              |
| Publicar (commit, push, PR)      | Tras verify | `open-pr` si hace falta ritual explícito          |
| Revisar antes de merge           | Semántico   | Frase o `validate-pr`                             |

### Secuencia del ciclo (humano ↔ agente)

> ZenUML equivalente en [`prompt-catalog.md`](prompt-catalog.md). Mermaid renderiza en GitHub sin extensiones.

```mermaid
sequenceDiagram
    autonumber
    actor H as Humano
    participant A as Agente
    participant S as Spec / BACKLOG
    participant G as Git

    H->>A: Iniciativa (texto o discovery-to-draft)
    A->>S: Draft + auto-DoR
    opt draft-review (opcional)
        H->>A: Revisar DoR
        A-->>H: Gaps
    end
    H->>S: Aprobar → Ready
    A->>S: In Build
    Note over A: Local — sin push
    A->>A: Implementar + quality gates
    H->>A: verify-implementation
    A-->>H: Evidencia vs spec
    Note over A,G: Solo tras verify OK
    A->>G: commit + push + PR (1..N SDD-NNN)
    A->>S: Validating
    H->>A: Revisar PR / DoD
    H->>G: Merge
    A->>S: Released
```

### Verificación local antes de Git compartido

| Fase local (In Build)          | Git compartido (→ Validating) |
| ------------------------------ | ----------------------------- |
| Rama local opcional            | Commit de entrega             |
| Código según spec              | `push` al remoto              |
| Quality gates en verde         | Apertura de PR                |
| **`verify-implementation` OK** | Estado spec → `Validating`    |

**Permitido antes de verify:** working tree, rama local, commits WIP locales sin push.

**Prohibido antes de verify:** `push`, PR, solicitud de merge.

### Varios specs en un PR

Un PR puede referenciar **varios** `SDD-NNN` cuando:

1. Entrega coherente o misma campaña de release.
2. Cada spec cumple DoD en ese entregable.
3. La descripción del PR lista todos los IDs y criterios por spec.
4. Al cerrar release, cada spec se archiva individualmente.

Detalle en [`checklist-pr.md`](checklist-pr.md).

**Prompts por fase** (catálogo: [`prompt-catalog.md`](prompt-catalog.md)):

| Fase       | Prompt ID                                        |
| ---------- | ------------------------------------------------ |
| Discovery  | `discovery-to-draft`                             |
| Draft      | `draft-review` _(opcional)_                      |
| Ready      | `build-spec`                                     |
| In Build   | `build-spec`, `verify-implementation`, `open-pr` |
| Validating | `validate-pr`                                    |
| Released   | `close-release`                                  |

Alias deprecados (v1.2.x): `approve-ready`, `implement-spec` → usar `build-spec`.

Reglas de transición:

1. Cada cambio de estado en **cabecera del spec** y en **BACKLOG.md**.
2. En `specs/`, estados permitidos: `Draft`, `Ready`, `In Build`, `Validating`. **`Released` solo** tras `git mv` a `archive/`.
3. Al cerrar: `git mv` del spec y actualizar enlaces en BACKLOG.
4. Cambios triviales **no requieren spec** — registrar en release con ID `—`.
5. **`SDD-NNN` es global** en el repositorio (contador en BACKLOG).
6. **No `push` ni PR** hasta `verify-implementation` en verde.

### Descartado / en pausa

Solo en BACKLOG (no en cabecera del spec). Documentar razón y fecha.

### Hotfix

Rama `hotfix/…` → PR a rama de producción (ver [`branching.md`](branching.md)). Preferir spec `bugfix`; en urgencia extrema, ID `—` en release. Prompt: `hotfix-minor` en [`prompt-catalog.md`](prompt-catalog.md).

---

## Tipos de spec

| Tipo            | Cuándo                                                            | Profundidad                                  |
| --------------- | ----------------------------------------------------------------- | -------------------------------------------- |
| `feature`       | Funcionalidad nueva visible                                       | Completa                                     |
| `bugfix`        | Comportamiento incorrecto                                         | Simplificada                                 |
| `performance`   | Optimización sin cambio funcional                                 | Simplificada                                 |
| `refactor`      | Reestructuración interna                                          | Completa + equivalencia funcional            |
| `db-change`     | Cambio de esquema o datos                                         | Completa + sección "Cambio de BD"            |
| `documentation` | Doc, manual, release                                              | Simplificada                                 |
| `transcription` | Convertir fuentes a Markdown legible por agente (PDF, DOCX, etc.) | Simplificada — ver perfil `reports-latex-md` |

Combinaciones permitidas: `feature + db-change`, `bugfix + db-change`, `feature + transcription`, etc.

### Fase opcional: Transcription

Antes de **Draft**, cuando el perfil o el spec lo requiera (p. ej. `reports-latex-md`):

| Etapa             | Artefacto                                        | Criterio de salida                                                  |
| ----------------- | ------------------------------------------------ | ------------------------------------------------------------------- |
| **Transcription** | `.md` en `data/transcripts/` (ruta del proyecto) | Fuentes no legibles convertidas; método y limitaciones documentados |

No es un estado en cabecera del spec: se registra en BACKLOG o como spec tipo `transcription` hasta completar. Detalle: [`profiles/reports-latex-md/workflow-extensions.md`](../profiles/reports-latex-md/workflow-extensions.md).

---

## ¿Esta iniciativa necesita spec?

Usar esta checklist **antes** de crear un spec. Si la respuesta es NO a todas las preguntas de la columna izquierda, registrar en release con ID `—` (cambio trivial).

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
- [ ] Es una feature de 1 archivo, 1 componente, efímera (< 1 semana de vida esperada)
- [ ] Es un hotfix crítico (spec post-mortem aceptable si la urgencia lo impide)

### Zona gris (criterio del mantenedor)

| Situación | Recomendación |
|-----------|---------------|
| Iniciativa toca 2 componentes pero es simple | Spec simplificado ([modo compacto](#modo-compacto-de-spec)) |
| Iniciativa es 1 componente pero de alto riesgo | Spec completo |
| Patrón repetitivo ya documentado | Spec compacto con referencia al patrón |

### Fundamento (token economics)

El spec en sí consume ~2.4% de los tokens de una sesión SDD. La revisión iterativa de código consume ~59.4%. El spec **no es el driver de costo**. El driver es el loop de "genera → verifica → corrige → re-verifica" sin control. Un harness con governance adecuada reduce el costo total 38-41%. Fuente: [research/2026-07-15-token-economics-sdd-harness.md](research/2026-07-15-token-economics-sdd-harness.md).

### Modo compacto de spec

Usar [`spec-compact-template.md`](templates/spec-compact-template.md) cuando:

- El spec sigue un patrón documentado (nuevo perfil, nuevo comando CLI, nueva skill)
- El dominio y las reglas de negocio ya están establecidos
- No hay decisiones arquitectónicas nuevas (sin ADR)
- La iniciativa toca ≤2 componentes

**No usar** modo compacto cuando:

- El spec introduce un nuevo dominio
- Hay decisiones de diseño no triviales
- El spec requiere ADR
- La iniciativa toca 3+ componentes

El modo compacto omite secciones estándar (checklist stack, impacto técnico detallado, diagramas) y referencia `domain-rules.md` y el perfil correspondiente en lugar de repetirlos. Ahorro estimado: 40-60% de tokens vs plantilla completa.

---

## ADR — cuándo crear uno

Crear ADR cuando la decisión es **arquitectónica y transversal**:

1. Cambia una **convención global** del proyecto.
2. Afecta a **más de un módulo** o capa.
3. Introduce **dependencia o integración externa** nueva.
4. **Reemplaza** un ADR previo.

No crear ADR para cambios de esquema locales de un módulo (van en el spec).

Plantilla: [`templates/adr-template.md`](templates/adr-template.md).

---

## Definition of Ready (DoR)

- [ ] Tipo y dominio declarados
- [ ] Objetivo, alcance y exclusiones definidos
- [ ] Tabla **Impacto técnico** del spec completada (plantilla del perfil stack)
- [ ] Autorización evaluada si el cambio es visible para usuarios
- [ ] Si `db-change`: sección "Cambio de BD" completa
- [ ] Si decisión transversal: ADR creado y referenciado
- [ ] Criterios de aceptación (happy + error path)
- [ ] Riesgos y rollback documentados
- [ ] Owner y versión objetivo en cabecera

---

## Definition of Done (DoD) — proceso

- [ ] Quality gates del **perfil stack** en verde (tests, lint, build)
- [ ] Validación funcional manual (happy + error path)
- [ ] Entrada en `releases/vX.Y.Z/release_vX.Y.Z.md`
- [ ] Spec en `archive/<YYYY>/<dominio>/` (mismo commit que release si aplica)
- [ ] BACKLOG → fila en _Released_

Detalle técnico por stack: `profiles/<stack>/checklist-stack.md`.

---

## Rituales

### Cierre por entrega

Seguir [`releases/RUNBOOK.md`](releases/RUNBOOK.md). Archivado y BACKLOG **mergeados en rama de desarrollo antes** del PR de campaña a producción.

### Revisión semanal (~30 min)

- Actualizar BACKLOG según estado real.
- Specs estancados (>2 semanas) → replanificar o descartar. Prompt: `spec-stuck`.
- Decisiones transversales → ADR.

---

### Optimización de specs repetitivas

Cuando un dominio tiene múltiples specs que siguen el mismo patrón (ej. extracción por región, migración por tabla):

- Usar una **plantilla específica del dominio** referenciada desde cada spec
- No copiar reglas de negocio transversales ya definidas en `domain-rules.md`
- No copiar criterios de aceptación idénticos; referenciar el playbook o ADR que los define
- Cada spec solo debe contener lo **específico**: parámetros, tabla de datos particulares, riesgos únicos

---

## Nombrado

- **Spec activo:** `specs/<dominio>/SDD-NNN-slug.md`
- **Spec archivado:** `archive/<YYYY>/<dominio>/SDD-NNN-slug.md`
- **ADR:** `adr/ADR-NNN-YYYY-MM-DD-slug.md`
- **Release:** `releases/vX.Y.Z/release_vX.Y.Z.md`

### Partición por complejidad (`00/01/02…`)

Para iniciativas grandes: spec `00` (visión) + specs `01+` (entregables). IDs correlativos globales.

### Cambio de esquema

Seguir la convención del **perfil stack** (p. ej. migraciones, no DDL manual fuera del repo). Documentar en spec y release.

---

## Governance de costo (circuit breaker del harness)

> Ver skill completa: `sdd-cost-governance/SKILL.md`. Esta sección es el resumen always-on.

### Límites de sesión

| Límite | Valor | Acción |
|--------|-------|--------|
| Turnos máximos por fase | 15 | Pausar, pedir aprobación |
| Turnos máximos totales | 50 | Terminar, reportar estado |
| Verify fallidos consecutivos | 3 | **STOP.** No seguir iterando. |
| Tool calls idénticas consecutivas | 3 | Circuit breaker: cambiar approach |

### Anti-patrones de gasto — STOP inmediato

1. Loop "generar → test falla → mismo error → regenerar" sin cambiar approach
2. Leer mismo archivo 5+ veces sin modificarlo
3. Re-escribir specs en Ready sin aprobación humana
4. Ejecutar tests sin cambiar código
5. Cargar specs de otras features no relacionadas (usar [grafo de dependencias](#grafo-de-dependencias-sdd))
6. Debug por fuerza bruta (cambios aleatorios sin entender causa raíz)

### Fundamento (token economics)

- Spec = ~2.4% de tokens. Review iterativo = ~59.4%. Fuente: [Tokenomics paper](https://arxiv.org/abs/2601.14470).
- Harness con governance: -38% tokens, -41% costo, -44% tiempo. Fuente: [Harness Effect paper](https://arxiv.org/abs/2607.06906).
- KV-cache hit < 90% → hasta 10× más caro. Fuente: [research/2026-07-15-token-economics-sdd-harness.md](research/2026-07-15-token-economics-sdd-harness.md).
