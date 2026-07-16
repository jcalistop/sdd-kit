---
name: sdd-draft-spec
description: Crea un spec SDD en estado Draft para una nueva iniciativa siguiendo sdd-agent-workflow. Itera con el humano para capturar idea, dominio y tipo; asigna SDD-NNN; elige plantilla; completa DoR; actualiza BACKLOG. Usar cuando el usuario pida crear un spec, iniciar una iniciativa SDD, pasar de Discovery a Draft, o mencione /create-spec, draft spec, SDD-NNN nuevo.
---

# SDD Draft Spec

Crear un spec **Draft** listo para revisión humana (transición a **Ready**). No implementar código ni pasar a In Build.

**Contexto mínimo requerido** (ver `{{SDD_PATH}}/workflow.md` → grafo de dependencias):

1. `{{SDD_PATH}}/BACKLOG.md` — para asignar SDD-NNN y verificar duplicados
2. `{{SDD_PATH}}/sdd.config.yaml` — para dominios, `ids.next_sdd`, paths
3. `{{SDD_PATH}}/../business/domain-rules.md` — para reglas aplicables al spec

**NO leer** specs de otras features, ADRs no referenciados ni releases anteriores.
Si el spec referencia un ADR explícitamente, leer solo ese ADR.

## Rutas (instancia consumidora)

| Artefacto          | Ruta                                             |
| ------------------ | ------------------------------------------------ |
| Instancia SDD      | `{{SDD_PATH}}/`                                  |
| Specs              | `{{SDD_PATH}}/specs/<dominio>/SDD-NNN-slug.md`   |
| Plantilla completa | `{{SDD_PATH}}/templates/spec-template.md`        |
| Plantilla simple   | `{{SDD_PATH}}/templates/spec-simple-template.md` |
| BACKLOG            | `{{SDD_PATH}}/BACKLOG.md`                        |
| Config / IDs       | `{{SDD_PATH}}/sdd.config.yaml`                   |
| Reglas de negocio  | `{{SDD_PATH}}/../business/domain-rules.md`       |
| DoR / antipatrones | `.cursor/rules/sdd-workflow-reference.mdc`       |

---

## Fase 1 — Iteración agente ↔ humano

**No crear archivos** hasta tener contexto suficiente. Iterar con preguntas cortas (1–3 por turno).

### 1. Idea

Solicitar descripción inicial. Profundizar hasta cubrir:

- Problema o necesidad concreta
- Resultado esperado (qué cambia para el usuario/sistema)
- Qué **NO** incluye (exclusiones explícitas)
- Dependencias con otros SDD o ADR conocidos
- Versión objetivo tentativa (revisar campaña abierta en BACKLOG)

Detectar antipatrones tempranos (YAGNI, big rewrite, tecnología nueva sin problema) → alertar, no bloquear. Ver [reference.md](reference.md).

### 2. Dominio

Proponer dominio de `sdd.config.yaml` → `domains`. Si ninguno encaja: proponer nuevo dominio al humano → actualizar config **antes** de crear el spec.

### 3. Tipo

Proponer tipo según alcance: `feature`, `bugfix`, `refactor`, `performance`, `db-change`, `documentation`.

**¿Hace falta spec?** Feature, refactor riesgoso, db-change → sí. Bugfix no trivial → spec simplificado. Typo, copy, bump deps → **sin spec** (ID `—` en release).

Confirmar dominio, tipo e idea con el humano antes de continuar.

---

## Fase 2 — Asignar ID y crear spec

1. Leer `ids.next_sdd` en `sdd.config.yaml` y _Próximo ID disponible_ en BACKLOG.
2. Asignar `SDD-NNN`; crear `{{SDD_PATH}}/specs/<dominio>/SDD-NNN-slug.md`.

---

## Fase 3 — Elegir plantilla

| Condición                           | Plantilla                         |
| ----------------------------------- | --------------------------------- |
| `domain-rules.md` completado        | `spec-template.md`                |
| Plantilla + sin vocabulario técnico | Ofrecer `spec-simple-template.md` |

---

## Fase 4 — Completar contenido y DoR

Completar cabecera, problema/objetivo, alcance, impacto técnico, reglas `DR-*`, criterios happy/error, riesgos. Auto-verificar DoR en [reference.md](reference.md).

---

## Fase 5 — Actualizar BACKLOG

1. Agregar fila en **Draft**; incrementar `ids.next_sdd` y _Próximo ID disponible_.
2. `python {{KIT_PATH}}/cli/sdd.py validate` → 0 errores.

---

## Fase 6 — Presentar al humano

Resumen + checklist DoR + pregunta: "¿Apruebas pasar a **Ready**?"

## Recursos

- [reference.md](reference.md)
- Prompt kit: `python {{KIT_PATH}}/cli/sdd.py prompt show discovery-to-draft --full`
