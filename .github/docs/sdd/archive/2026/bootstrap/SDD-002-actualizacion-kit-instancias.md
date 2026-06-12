# SDD-002 — Actualización del kit en instancias consumidoras

---

## Cabecera

| Campo                | Valor                                                  |
| -------------------- | ------------------------------------------------------ |
| **ID**               | `SDD-002`                                              |
| **Dominio**          | `bootstrap`                                            |
| **Tipo**             | `feature`                                              |
| **Fecha**            | 2026-06-12                                             |
| **Estado**           | `Released`                                             |
| **Versión objetivo** | `v1.1.0`                                               |
| **Owner**            | mantenedor                                             |
| **Prioridad**        | `P1`                                                   |
| **Dependencias**     | — (complementa `update-submodule`; no bloquea SDD-001) |

---

## Que quiero lograr

**Problema o necesidad:**

Cuando el kit publica una nueva versión (SemVer en `docs/releases/`), las instancias SDD en proyectos consumidores deben incorporar cambios en reglas de agente, workflow, plantillas y prompts. Hoy no hay un proceso formal documentado ni un prompt de catálogo que guíe al agente de punta a punta. El consumidor no tiene forma estándar de saber qué versión del kit tiene instalada ni un registro de qué actualizaciones aplicó y qué archivos de la instancia tocó.

**Resultado esperado:**

Un flujo reproducible (runbook + prompt) que permita: (1) identificar la versión actual del kit en la instancia, (2) actualizar el submodule o equivalente de forma segura sin pisar customizaciones, (3) portar cambios relevantes de `core/` a `.github/docs/sdd/`, (4) reinstalar adaptadores si cambió el manifest, (5) validar con `validate-sdd`, y (6) dejar trazabilidad escrita del upgrade.

---

## Que incluye y que NO incluye

**Incluye:**

- Runbook de actualización en `core/` (p. ej. `upgrade-guide.md` o sección dedicada enlazada desde `adoption-guide.md` e `INSTALL.md`)
- Evolución del prompt `update-submodule` o prompt nuevo `upgrade-kit` en `core/prompts/` (categoría `exceptions` o `adoption`) con pasos explícitos para el agente
- Campo de versión del kit en instancia: `kit.installed_version` (y opcional `kit.installed_at`) en `sdd.config.yaml` + plantilla `sdd.config.example.yaml`
- Archivo de trazabilidad en instancia (p. ej. `UPGRADE-LOG.md` en `.github/docs/sdd/` o sección en `PROJECT.md`) con formato mínimo: fecha, versión origen → destino, archivos mergeados, validación
- Actualización de `init-sdd` para escribir versión inicial del kit al bootstrap
- Entrada en [`core/prompt-catalog.md`](../../../../../core/prompt-catalog.md) y mapa mermaid
- Advertencia en `validate-sdd` / `sdd validate` si la versión registrada difiere del tag/commit del submodule (warning, no error bloqueante en v1)
- Dogfooding: aplicar el esquema en la instancia de este repo (`.github/docs/sdd/`)
- Actualización de [`README.md`](../../../../../README.md) en la raíz: sección breve «Actualizar el kit» (o equivalente) con enlace al runbook y al prompt del catálogo; entrada en tabla «Siguiente lectura» si aplica

**NO incluye (explicito):**

- Comando CLI `sdd upgrade` con merge automático de archivos (evaluar en spec futuro)
- Soporte para proyectos sin submodule (copia puntual) más allá de notas en el runbook — sin script nuevo
- Migración retrospectiva masiva de todas las instancias existentes en la wild
- Cambios en perfiles de stack consumidor (`profiles/<stack>/`) salvo enlaces desde el runbook
- Versionado SemVer del proceso SDD de cada proyecto (`.github/docs/sdd/releases/` sigue siendo independiente)

---

## Impacto

| Area afectada                    | Como se afecta                                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------------- |
| `core/`                          | Nuevo runbook; ampliación prompt-catalog; posible `upgrade-guide.md`                        |
| `bootstrap/`                     | `init-sdd` escribe versión inicial; `validate-sdd` compara versión vs submodule             |
| `cli/`                           | Opcional: mostrar versión en `sdd validate` (solo lectura; sin merge)                       |
| `profiles/`                      | No aplica — el runbook es agnóstico al stack (regla 1 domain-rules)                         |
| `.github/docs/sdd/` (dogfooding) | `sdd.config.yaml` con `kit.*`; `UPGRADE-LOG.md` o equivalente                               |
| `README.md` (raíz)               | Nueva sección o párrafo de actualización; enlace al runbook y prompt; coherente con SDD-001 |
| `INSTALL.md` / `agent-setup.md`  | Enlaces al runbook; reemplazar sección mínima de actualización                              |
| `docs/releases/`                 | Notas de release v1.1.0 documentan el nuevo flujo                                           |

**Reglas de [`domain-rules.md`](../../../business/domain-rules.md) aplicables:**

- **Regla 1** — Runbook y prompt en `core/` sin referencias a stacks concretos.
- **Regla 5** — El upgrade es incremental; no exige re-ejecutar `init-sdd` ni specs retrospectivos.
- **Regla 7** — Versiones del producto en `docs/releases/`; la instancia registra qué versión tiene instalada en `paths.sdd`.
- **Glosario** — _Instancia SDD_, _Consumidor_, _Kit_: el flujo opera entre submodule (`sdd-kit/`) e instancia (`.github/docs/sdd/`).

---

## Como se que esta listo (criterios de aceptacion)

- [x] Existe runbook enlazado desde `README.md`, `INSTALL.md` y `adoption-guide.md` con pasos ordenados: detectar versión → leer changelog → actualizar submodule → diff core vs instancia → merge con confirmación humana → reinstalar adaptadores → `validate-sdd` → registrar en log.
- [x] `README.md` (raíz) menciona el flujo de actualización y enlaza al runbook; un consumidor que solo lee el README sabe que existe el proceso y dónde profundizar.
- [x] Prompt en catálogo (`sdd prompt show <id> --full`) cubre el flujo completo y pide confirmación antes de sobrescribir archivos de instancia.
- [x] `sdd.config.example.yaml` incluye `kit.installed_version` documentado; `init-sdd` lo rellena en instalaciones nuevas.
- [x] Instancia dogfooding de sdd-kit tiene versión registrada y al menos una entrada de ejemplo en log de upgrade.
- [x] `sdd validate` emite **warning** (no error) cuando `kit.installed_version` ≠ tag/commit del submodule.
- [x] `validate-sdd` en verde tras los cambios; CI sin regresiones.
- [x] **Error path:** si el humano rechaza un merge, el agente documenta en el log qué quedó pendiente y no marca el upgrade como completado.

---

## Riesgos

| Que puede salir mal                                     | Como lo mitigo                                                                                           |
| ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Sobrescribir customizaciones en `.github/docs/sdd/`     | Prompt y runbook exigen diff + confirmación humana; nunca `--force` en archivos de instancia             |
| Confusión versión kit vs release SDD del proyecto       | Documentar en runbook y glosario; nombres distintos (`kit.installed_version` vs releases de iniciativas) |
| Proyectos sin submodule no pueden auto-detectar versión | Runbook describe verificación manual; warning de validate solo aplica con submodule                      |
| Scope creep hacia CLI merge automático                  | Excluido explícitamente; backlog futuro si hace falta                                                    |

---

## Notas post-implementacion

- Runbook: `core/upgrade-guide.md`; prompt: `upgrade-kit`; helper: `bootstrap/kit-version.py`
- Dogfooding: `kit.installed_version` v1.1.0 + `UPGRADE-LOG.md` con entrada SDD-002
