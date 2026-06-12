# Guia de Adopcion Incremental — SDD

> Como introducir SDD en proyectos **nuevos** o **existentes** sin detener el desarrollo.
> Pensado para equipos de 1 persona con desarrollo asistido por agente de IA.
>
> **Primera vez con SDD?** Empieza por [`concepts.md`](concepts.md) (5 min) y vuelve aqui.

**Relacionado:** [`concepts.md`](concepts.md) · [`workflow.md`](workflow.md) · [`operations.md`](operations.md) · [`../docs/maintainers/ROADMAP.md`](../docs/maintainers/ROADMAP.md)

---

## Principios

1. **No reescribir el pasado.** El codigo ya en produccion no requiere specs retrospectivos obligatorios.
2. **SDD desde ahora.** Todo cambio no trivial nuevo entra al ciclo.
3. **El agente ejecuta, el humano aprueba.** El agente crea specs, codigo y documentacion; el humano valida en puntos de control.
4. **Incremental siempre.** Cada etapa aporta valor por si sola; no hay que completar las tres para beneficiarse.

---

## Antes de empezar

| Situacion del proyecto          | Que hacer                                                |
| ------------------------------- | -------------------------------------------------------- |
| **Proyecto nuevo**              | Submodule + `init-sdd` (humano o agente); `-Agent auto`  |
| **Proyecto existente sin docs** | Submodule + **modo agente** (recomendado) + Etapa 1      |
| **Proyecto existente con docs** | Submodule + modo agente; migrar a `business/` en Etapa 3 |

### Instalacion recomendada

**Humano (siempre):** añadir submodule:

```powershell
git submodule add https://github.com/jcalistop/sdd-kit.git sdd-kit
```

**Proyecto nuevo:** ejecutar bootstrap:

```powershell
.\sdd-kit\bootstrap\init-sdd.ps1 -Profile laravel-filament -Project "Mi App"
```

**Proyecto existente:** delegar al agente con el prompt `adopt-existing` del [catalogo de prompts](prompt-catalog.md) (`sdd prompt show adopt-existing`). El agente ejecuta `init-sdd` solo si no hay instancia SDD, lee documentacion previa y **no sobrescribe** archivos sin aprobacion.

Por defecto se detecta el agente/IDE e instalan instrucciones (Cursor, Claude Code, Codex o Copilot). Ver [`agent-setup.md`](agent-setup.md).

---

## Etapa 1 — Minima viable (dia 1)

**Objetivo:** Tener hoja de ruta visible sin burocracia.

### Pasos

1. **Ejecutar bootstrap** (ver arriba).
2. **Completar `sdd.config.yaml`:** nombre, ramas, dominios de iniciativas.
3. **Completar `business/README.md`:** que hace el sistema, roles, modulos principales.
4. **Opcional:** copiar y completar `business/domain-rules.md` desde `templates/business-domain-template.md` si el proyecto tiene reglas de negocio transversales (autorizacion, filtros por tenant, periodos activos, etc.).
5. **Inventariar el BACKLOG** — no crear specs retrospectivos:
   - Listar 3–10 capacidades ya existentes en _Released_ con ID `—` y nota "pre-SDD".
   - Agregar 3–5 iniciativas reales como `Discovery` (lo que viene ahora).
6. **Validar:** `.\sdd-kit\bootstrap\validate-sdd.ps1` (o `.sh`) debe pasar sin errores criticos. Prompt: `validate-setup` en [prompt-catalog.md](prompt-catalog.md).

### Que NO hacer en Etapa 1

- No escribir specs para features ya implementadas.
- No crear ADRs retrospectivos.
- No bloquear bugs urgentes por falta de spec (usar ID `—` en release).

### Checklist Etapa 1

- [ ] Estructura `.github/docs/sdd/` creada
- [ ] `sdd.config.yaml` con dominios del proyecto
- [ ] `business/README.md` con contexto minimo
- [ ] `BACKLOG.md` con inventario pre-SDD y al menos 3 items en Discovery
- [ ] Adaptadores de agente instalados (ver `sdd.config.yaml` → `agent.targets` o [`agent-setup.md`](agent-setup.md))
- [ ] `validate-sdd` sin errores

---

## Formalizar el contexto de negocio

El agente necesita reglas explicitas en `business/domain-rules.md` para no inventar restricciones ni omitir las que el humano conoce.

### Por que importa

| Sin domain-rules completado                        | Con domain-rules completado                                       |
| -------------------------------------------------- | ----------------------------------------------------------------- |
| El agente no asume reglas (seguro pero incompleto) | El agente verifica roles, filtros e invariantes en cada spec y PR |
| Cada spec repite preguntas de negocio              | Las reglas transversales se citan una vez y se reutilizan         |
| Riesgo de regresiones en autorizacion o filtrado   | Checklist de PR incluye reglas verificables del dominio           |

### Cuando completarlo

| Situacion                                  | Recomendacion                                                                                         |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| Proyecto nuevo                             | Antes del primer spec no trivial (sesion guiada con el agente)                                        |
| Proyecto existente sin docs                | Etapa 1: minimo en `README.md`; formalizar `domain-rules.md` cuando el agente lo detecte en plantilla |
| Proyecto con docs fuera de `business/`     | Extraer roles y reglas a `domain-rules.md` en Etapa 3 (cuando toque migrar)                           |
| Cambio sin reglas de negocio (infra, copy) | No es obligatorio; el agente marca "No aplica" en el spec                                             |

### Como detectar estado plantilla

`domain-rules.md` esta en **plantilla** si contiene `_ej._`, `_..._`, `{{PROJECT_NAME}}` o glosario vacio. El agente (regla `sdd-agent-workflow.mdc`) lo detecta y pregunta si formalizar ahora o posponer.

### Sesion guiada (humano + agente)

1. El humano describe el sistema en lenguaje natural.
2. El agente hace las preguntas de [`templates/business-domain-template.md`](templates/business-domain-template.md) (seccion "Sesion guiada").
3. El agente redacta `domain-rules.md` y actualiza `business/README.md`.
4. El humano revisa y aprueba.
5. A partir de ahi, cada spec cita que reglas aplican en "Impacto tecnico".

**Prompt al agente:** `formalize-domain-rules` — ver [prompt-catalog.md](prompt-catalog.md) o `sdd prompt show formalize-domain-rules`.

### Valor para desarrollo agentico

- El agente **no adivina** restricciones; las lee de una fuente unica.
- Los specs incluyen reglas de negocio **trazables** a `domain-rules.md`.
- Los PRs verifican reglas con checklist del perfil stack + dominio.

---

## Etapa 2 — Nuevas features con SDD (semana 1+)

**Objetivo:** Todo cambio no trivial nuevo sigue el ciclo completo.

### Que entra al ciclo SDD

| Tipo                               | Spec requerido                         |
| ---------------------------------- | -------------------------------------- |
| Feature nueva visible              | Si — completo                          |
| Bugfix no trivial                  | Si — simplificado                      |
| Refactor con riesgo                | Si — completo + equivalencia funcional |
| Cambio de esquema                  | Si — incluye `db-change`               |
| Typo, bump de deps, ajuste de copy | No — ID `—` en release                 |

### Flujo tipico (humano + agente)

```
Humano: "Necesitamos exportar reportes a Excel"
    ↓
Agente: agrega fila Discovery en BACKLOG → crea spec Draft (SDD-NNN)
    ↓
Agente: auto-verifica DoR → presenta spec al humano
    ↓
Humano: aprueba → agente pasa a Ready → In Build
    ↓
Agente: implementa, tests, PR con checklist
    ↓
Humano: revisa PR → merge
    ↓
Agente: al cerrar release → archiva spec, actualiza BACKLOG
```

Prompts por transicion: [prompt-catalog.md](prompt-catalog.md) (`discovery-to-draft` → `close-release`).

### Referencia de calidad

Usar el spec de ejemplo del perfil como modelo de detalle esperado:

- `profiles/<stack>/examples/SDD-001-*.md` (en el kit)
- Copia opcional a `specs/<dominio>/` al iniciar el primer spec real

### Checklist Etapa 2

- [ ] Al menos 1 spec completado Discovery → Released
- [ ] PR con checklist core + perfil stack
- [ ] Release con tabla de specs (o ID `—` documentado)
- [ ] `validate-sdd` pasa tras cada cierre de release

---

## Etapa 3 — Cobertura completa (mes 2+)

**Objetivo:** SDD como unico canal de planificacion y trazabilidad.

### Pasos

1. **Refactors y mejoras** usan spec (tipo `refactor` o `performance`).
2. **ADRs** para decisiones arquitectonicas pendientes o nuevas.
3. **Migrar documentacion legacy** a `business/` (cualquier fuente previa: READMEs, docs en repo, herramientas externas, comentarios de arquitectura). Prompt: `migrate-legacy-docs` en [prompt-catalog.md](prompt-catalog.md).
4. **Completar `business/domain-rules.md`** si aplica — reglas que el agente debe verificar en cada PR (roles, filtros, periodos).
5. **Revisar dominios** en `sdd.config.yaml` — alinear con la taxonomia real del proyecto.

### Deuda tecnica pre-existente

Registrar en BACKLOG como `Discovery` con nota "deuda tecnica". Priorizar con el humano; no crear specs masivos de golpe.

### Checklist Etapa 3

- [ ] Cambios no triviales tienen spec o justificacion `—` en release
- [ ] ADRs para decisiones transversales activas
- [ ] Documentacion de producto centralizada en `business/`
- [ ] Dominios SDD reflejan como el equipo planifica trabajo

---

## Proyectos existentes — escenarios comunes

### "Tenemos documentacion repartida en varios lados"

Da igual si vive en READMEs del repo, carpetas `docs/`, Confluence, Google Docs, Notion, o solo en la cabeza del equipo documentada a medias.

1. Etapa 1: no consolidar todo de golpe ni borrar fuentes originales.
2. Extraer lo minimo a `business/README.md`: vision, roles, glosario, modulos.
3. Etapa 3: migrar con plan las reglas de negocio a `business/domain-rules.md`.

### "No tenemos rama dev, solo main"

Ajustar `sdd.config.yaml`:

```yaml
project:
  development_branch: main # o crear rama dev antes de Etapa 2
  production_branch: main
```

Recomendacion: crear rama `dev` antes de Etapa 2 para separar integracion de produccion.

### "El agente no sigue SDD"

1. Revisar `sdd.config.yaml` → `agent.targets` y que existan los archivos del adaptador (ver [`agent-setup.md`](agent-setup.md)):
   - Cursor: `.cursor/rules/sdd-core.mdc` y `sdd-agent-workflow.mdc`
   - Claude Code: bloque SDD en `CLAUDE.md`
   - Codex: bloque SDD en `AGENTS.md`
   - Copilot: `.github/copilot-instructions.md`
2. Reinstalar: `python sdd-kit/bootstrap/install-agents.py install --agent auto --profile <perfil>`
3. Pedir al agente: "Sigue sdd-agent-workflow: crea spec Draft para [idea]".
4. Ejecutar `validate-sdd` tras cada cambio documental.

---

## Validacion continua

```powershell
.\sdd-kit\bootstrap\validate-sdd.ps1
.\sdd-kit\bootstrap\validate-sdd.ps1 -SddPath ".github/docs/sdd"
```

El script verifica:

- IDs `SDD-NNN` unicos en BACKLOG
- Specs en `specs/` con entrada en BACKLOG
- Specs en `archive/` en seccion Released
- Coherencia basica de "Proximo ID disponible"

---

## Referencias

| Documento                                                                                              | Uso                                   |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------- |
| [`workflow.md`](workflow.md)                                                                           | Ciclo y tipos de spec                 |
| [`healthy-development.md`](healthy-development.md)                                                     | Arquitectura, patrones, codigo limpio |
| [`templates/spec-template.md`](templates/spec-template.md)                                             | Plantilla de spec                     |
| [`templates/spec-simple-template.md`](templates/spec-simple-template.md)                               | Plantilla reducida (no tecnica)       |
| [`agent-setup.md`](agent-setup.md)                                                                     | Adaptadores multi-herramienta         |
| [`../bootstrap/agent-prompts/sdd-agent-workflow.md`](../bootstrap/agent-prompts/sdd-agent-workflow.md) | Flujo agentico (fuente unica)         |
| [`templates/business-domain-template.md`](templates/business-domain-template.md)                       | Reglas de negocio del proyecto        |
