# SDD Agent Workflow

Ejecutar el ciclo SDD de forma autónoma. El **humano aprueba** en Ready (spec) y en merge (PR). Adaptado a **desarrollador solo**.

**Lectura previa:** `BACKLOG.md`, `sdd.config.yaml`, `business/domain-rules.md`.

**Referencia on-demand:** checklists DoR/DoD, detección de antipatrones, arquitectura sana y manejo de errores → `sdd-workflow-reference.mdc` (léelo en Draft, In Build y Validating).

---

## Contexto de negocio

Leer `business/domain-rules.md` (ruta `paths.business` del config).

**Estado plantilla** si contiene `_ej.`, `_..._`, `{{PROJECT_NAME}}` o glosario vacío:

| Estado                       | Acción                                         |
| ---------------------------- | ---------------------------------------------- |
| Plantilla + código existente | Preguntar: formalizar ahora o posponer         |
| Plantilla + proyecto nuevo   | Sesión guiada antes del primer spec no trivial |
| Completado                   | Citar reglas aplicables en "Impacto técnico"   |

**Prohibido:** asumir reglas no documentadas. Si pospone, nota "domain-rules pendiente" en BACKLOG.

---

## Elegir plantilla de spec

| Condición                                  | Plantilla                                     |
| ------------------------------------------ | --------------------------------------------- |
| `domain-rules.md` completado               | `spec-template.md` (completa)                 |
| Plantilla + vocabulario técnico del humano | `spec-template.md`                            |
| Plantilla + sin vocabulario técnico        | Ofrecer `spec-simple-template.md` (no forzar) |

---

## ¿Hace falta spec?

| Situación                             | Acción                       |
| ------------------------------------- | ---------------------------- |
| Feature, refactor riesgoso, db-change | Spec obligatorio             |
| Bugfix no trivial                     | Spec simplificado (`bugfix`) |
| Typo, copy, bump deps                 | Sin spec — ID `—` en release |

---

## Fases (acciones clave)

**Discovery** — Verificar domain-rules; leer BACKLOG; identificar dominio y tipo; fila en Discovery; 1–3 preguntas solo si faltan datos críticos. Antipatrones tempranos → ver reference.

**Draft** — Asignar `SDD-NNN`; crear spec; completar alcance, impacto técnico y criterios; BACKLOG → Draft; **auto-verificar DoR** (reference).

**Ready** — Humano aprueba (frase o `build-spec`) → cabecera y BACKLOG a Ready; confirmar dependencias; congelar alcance.

**In Build** — Estado In Build; rama local; implementar según spec y perfil stack; quality gates en verde. **`draft-review` es opcional** (solo ritual DoR formal). **No push ni PR** hasta verificación local.

**Verify (In Build)** — `verify-implementation` obligatorio: criterios de aceptación, `domain-rules.md`, arquitectura sana (reference). Presentar evidencia. Solo tras OK → commit, push, PR.

**Validating** — PR con checklist core + stack; evidencia de verify + tests; **auto-verificar DoD** (reference); pedir merge al humano.

**Released** — `git mv` a `archive/<YYYY>/<dominio>/`; BACKLOG → Released; entrada en `releases/vX.Y.Z/`; `validate-sdd`. **Antes** del PR de campaña a producción.

---

## Anti-patrones (prohibido)

- Inventar `SDD-NNN` sin actualizar BACKLOG
- Código antes de spec para ítems no triviales en backlog
- Specs en `archive/` con estado distinto de `Released`
- Documentación SDD fuera de `paths.sdd` sin petición explícita
- Asumir roles de equipo — el humano único decide y aprueba
- Asumir reglas de negocio no escritas en `domain-rules.md`
- `push` o PR antes de `verify-implementation` en verde
