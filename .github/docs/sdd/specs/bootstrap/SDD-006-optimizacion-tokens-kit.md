# SDD-006 — Optimización de tokens en reglas, skills y pipeline de generación

---

## Cabecera

| Campo                 | Valor               |
| --------------------- | ------------------- |
| **ID**                | `SDD-006`           |
| **Dominio**           | `bootstrap`         |
| **Tipo**              | `feature`           |
| **Fecha**             | 2026-07-14          |
| **Estado**            | `In Build`          |
| **Versión objetivo**  | v1.3.0              |
| **Owner**             | SDD Kit maintainers |
| **Prioridad**         | `P1`                |
| **ADRs relacionados** | —                   |
| **Dependencias**      | —                   |

---

## Problema y objetivo

**Problema:**

La instancia consumidora del kit (`2026-analisis-retrospectivo-metas-2022-2025`) identificó y corrigió 6 fuentes de consumo innecesario de tokens (~1,470 líneas por carga de contexto). Estas mejoras deben trasladarse al repositorio fuente (`bootstrap/agent-prompts/`, `bootstrap/agent-skills/`, `install-agents.py`) para que todos los proyectos que usan el kit hereden las optimizaciones automáticamente.

Las fuentes de desperdicio detectadas fueron:

1. **Reglas `alwaysApply` redundantes:** `sdd-core.mdc` y `sdd-agent-workflow.mdc` existen como dos reglas separadas, cuando pueden fusionarse.
2. **Lectura previa forzada en cada mensaje:** La instrucción de leer `BACKLOG.md`, `sdd.config.yaml`, `domain-rules.md` vive en una regla `alwaysApply`, activándose incluso en tareas no-SDD.
3. **Cadena de lectura circular en verify-implementation:** La skill delega a `sdd-build-spec § B` → `sdd-workflow-reference.mdc`, forzando 3 lecturas.
4. **Sin guía anti-boilerplate en spec-template:** No hay advertencia contra copiar reglas de negocio transversales en specs repetitivas.
5. **Sin sección de optimización en workflow.md:** No hay guía para specs que siguen un patrón repetitivo.
6. **Skills duplicadas proyecto vs global:** `install-agents.py` instala skills en `~/.cursor/skills/` aunque ya existan en el proyecto.

**Objetivo:**

Aplicar las 6 correcciones al pipeline de generación del kit, ahorrando ~1,470 líneas por carga de contexto en cada proyecto consumidor que use Cursor.

---

## Alcance

**Incluye:**

- Fusionar `sdd-core.md` y `sdd-agent-workflow.md` en `bootstrap/agent-prompts/`; eliminar generación de `sdd-core.mdc` separado.
- Mover instrucción "Lectura previa" de la regla `alwaysApply` a las skills `sdd-draft-spec` y `sdd-build-spec` únicamente.
- Simplificar `sdd-verify-implementation/SKILL.md` con checklist inline (sin delegar a `sdd-build-spec § B`).
- Agregar nota anti-boilerplate en `core/templates/spec-template.md` para las secciones "Reglas de negocio" y "Criterios de aceptación".
- Agregar sección "Optimización de specs repetitivas" en `core/workflow.md`.
- Agregar lógica en `install-agents.py` para no instalar skills en `~/.cursor/skills/` si ya existen en `.cursor/skills/` del proyecto.
- Actualizar `bootstrap/agent-prompts/manifest.json` para reflejar el merge de reglas.
- Actualizar referencias a `sdd-core.mdc` en `core/agent-setup.md` y `bootstrap/agent-skills/*/reference.md`.
- Regenerar `bootstrap/cursor-rules/` vía `install-agents.py` / `sync-cursor-rules.py`.
- Agregar test en `bootstrap/test_install_skills.py` para el caso de deduplicación.

**Excluye explícitamente:**

- Cambios en perfiles de stack distintos de `sdd-kit`.
- Cambios en `cli/sdd.py`.
- Migración de specs existentes en repositorios consumidores (responsabilidad de cada proyecto).
- Cambios en la plantilla `spec-simple-template.md`.
- Modificar reglas `.cursor/rules/` del kit directamente (se regeneran desde `agent-prompts/`).

---

## Impacto técnico

| Área                                                        | Cambio                                                                     |
| ----------------------------------------------------------- | -------------------------------------------------------------------------- |
| `bootstrap/agent-prompts/sdd-core.md`                       | Fusionado dentro de `sdd-agent-workflow.md`; eliminado                     |
| `bootstrap/agent-prompts/sdd-agent-workflow.md`             | Reglas nucleares + sin "Lectura previa"                                    |
| `bootstrap/agent-prompts/manifest.json`                     | Sin entrada `core`; `workflow.alwaysApply` sigue `true`                    |
| `bootstrap/agent-skills/sdd-verify-implementation/SKILL.md` | Checklist inline; sin delegación circular                                  |
| `bootstrap/agent-skills/sdd-draft-spec/SKILL.md`            | Agrega "Lectura previa" al inicio                                          |
| `bootstrap/agent-skills/sdd-build-spec/SKILL.md`            | Agrega "Lectura previa" al inicio; quita ref a verify                      |
| `core/templates/spec-template.md`                           | Nota anti-boilerplate en Reglas y Criterios                                |
| `core/workflow.md`                                          | Sección "Optimización de specs repetitivas"                                |
| `core/agent-setup.md`                                       | Actualiza referencias (sin `sdd-core.mdc`)                                 |
| `bootstrap/install-agents.py`                               | Lógica de deduplicación skills proyecto vs global                          |
| `bootstrap/test_install_skills.py`                          | Test para caso de skills ya existentes en proyecto                         |
| `bootstrap/cursor-rules/`                                   | Regenerado: `sdd-core.mdc` eliminado; `sdd-agent-workflow.mdc` actualizado |

---

## Reglas de negocio

Aplica [`domain-rules.md`](../../business/domain-rules.md) del kit:

- **DR-1:** Core agnóstico al stack (ningún cambio en `core/` menciona stacks concretos).
- **DR-4:** El agente ejecuta; el humano aprueba. Verify local antes de push/PR.
- **DR-5:** Adopción incremental — el cambio es backward-compatible; no rompe instalaciones existentes.
- **DR-6:** Documentación SDD solo en `paths.sdd` (este spec y futura entrada en release).
- **DR-7:** Separación producto / proceso / versiones.

Particularidad de este spec: al reducir reglas `alwaysApply`, los proyectos consumidores notarán menos contexto SDD en tareas no relacionadas. El `upgrade-guide.md` debe mencionar este cambio como breaking-change menor (una regla menos en Cursor).

---

## Criterios de aceptación

**Happy path:**

- [ ] `bootstrap/agent-prompts/sdd-core.md` eliminado; su contenido integrado en `sdd-agent-workflow.md`.
- [ ] `sdd-agent-workflow.md` sin línea "Lectura previa:" en el encabezado.
- [ ] `manifest.json` sin entrada `core`; `workflow` sigue `alwaysApply: true`.
- [ ] `sdd-draft-spec/SKILL.md` y `sdd-build-spec/SKILL.md` incluyen "Lectura previa: BACKLOG.md, sdd.config.yaml, business/domain-rules.md" al inicio.
- [ ] `sdd-verify-implementation/SKILL.md` contiene checklist inline (quality gates, criterios, domain-rules, arquitectura, validate) sin referencia a `sdd-build-spec § B`.
- [ ] `sdd-build-spec/SKILL.md` sin la referencia "verify § B desde verify-implementation".
- [ ] `core/templates/spec-template.md` incluye nota anti-boilerplate en secciones "Reglas de negocio" y "Criterios de aceptación".
- [ ] `core/workflow.md` contiene sección "Optimización de specs repetitivas".
- [ ] `core/agent-setup.md` actualizado para no mencionar `sdd-core.mdc`.
- [ ] `install-agents.py`: `install_cursor()` genera solo 2 reglas `alwaysApply` (no 3).
- [ ] `install-agents.py`: `install_cursor_skills()` verifica existencia en `.cursor/skills/` del proyecto antes de escribir.
- [ ] `test_install_skills.py` incluye test que verifica que skills no se duplican si ya existen en proyecto.
- [ ] `bootstrap/cursor-rules/` regenerado: sin `sdd-core.mdc`; `sdd-agent-workflow.mdc` fusionado.
- [ ] `python -m compileall -q cli/` en verde.
- [ ] `python bootstrap/install-agents.py --agent cursor --target <fixture> --no-prompt --profile sdd-kit` ejecuta sin error.
- [ ] `sdd validate` sin errores.

**Error path:**

- [ ] Si `install-agents.py` falla al detectar skills existentes, debe continuar con instalación normal (no bloquear).
- [ ] Si `manifest.json` está corrupto, `install-agents.py` debe reportar error claro.
- [ ] Si el proyecto consumidor no tiene `.cursor/skills/.sdd-kit-manifest.json`, instalar skills normalmente.

---

## Diseño técnico

**Archivos principales:**

| Archivo                                                     | Cambio                              |
| ----------------------------------------------------------- | ----------------------------------- |
| `bootstrap/agent-prompts/sdd-core.md`                       | Eliminado                           |
| `bootstrap/agent-prompts/sdd-agent-workflow.md`             | Fusionado + sin lectura previa      |
| `bootstrap/agent-prompts/manifest.json`                     | Eliminada entrada `core`            |
| `bootstrap/agent-skills/sdd-draft-spec/SKILL.md`            | + Lectura previa                    |
| `bootstrap/agent-skills/sdd-build-spec/SKILL.md`            | + Lectura previa; - ref verify      |
| `bootstrap/agent-skills/sdd-verify-implementation/SKILL.md` | Checklist inline                    |
| `core/templates/spec-template.md`                           | Nota anti-boilerplate               |
| `core/workflow.md`                                          | Nueva sección optimización          |
| `core/agent-setup.md`                                       | Actualizar referencias              |
| `bootstrap/install-agents.py`                               | Dedup skills + 2 reglas alwaysApply |
| `bootstrap/test_install_skills.py`                          | Test deduplicación                  |
| `bootstrap/cursor-rules/`                                   | Regenerado                          |

**`install_cursor()` — antes vs después:**

```python
# Antes: 3 items con 2 alwaysApply (core + workflow)
items: list[tuple[...]] = [
    ("sdd-core.mdc", ..., manifest["core"]["file"], True),         # ELIMINADO
    ("sdd-agent-workflow.mdc", ..., manifest["workflow"]["file"], True),
    ("sdd-workflow-reference.mdc", ..., manifest["reference"]["file"], False),
]

# Después: 2 items con 1 alwaysApply (solo workflow)
items: list[tuple[...]] = [
    ("sdd-agent-workflow.mdc", ..., manifest["workflow"]["file"], True),
    ("sdd-workflow-reference.mdc", ..., manifest["reference"]["file"], False),
]
```

**`install_cursor_skills()` — lógica de deduplicación (pseudocódigo):**

```python
def install_cursor_skills(target, profile, sdd_path, kit_path):
    project_skills_dir = target / ".cursor" / "skills"
    # Si el proyecto ya tiene skills instaladas, no instalar de nuevo
    marker = project_skills_dir / ".sdd-kit-manifest.json"
    if marker.is_file():
        existing = json.loads(marker.read_text())
        if existing.get("kit_path") == kit_path:
            print("SDD Kit: skills ya instaladas en proyecto, omitiendo.")
            return
    # ... instalación normal ...
```

---

## Verificación técnica

```bash
# En sdd-kit/
python -m compileall -q cli/
python bootstrap/install-agents.py install --target . --agent cursor --no-prompt --profile sdd-kit --kit-path sdd-kit
python -c "import json; json.load(open('bootstrap/agent-prompts/manifest.json'))"
python -m pytest bootstrap/test_install_skills.py -q
python cli/sdd.py validate
```

---

## Riesgos y rollback

| Riesgo                                      | Probabilidad | Impacto | Mitigación                                                                                                     |
| ------------------------------------------- | ------------ | ------- | -------------------------------------------------------------------------------------------------------------- |
| Proyectos existentes esperan `sdd-core.mdc` | Baja         | Bajo    | Las reglas nucleares siguen disponibles dentro de `sdd-agent-workflow.mdc`; mismo contenido, diferente archivo |
| Skill sin "Lectura previa" pierde contexto  | Media        | Medio   | Solo `draft-spec` y `build-spec` necesitan esa lectura; otras skills no la usaban                              |
| Upgrade de proyectos existentes rompe algo  | Baja         | Medio   | Documentar en `upgrade-guide.md` y `CHANGELOG.md` como cambio backward-compatible                              |

**Rollback:** revertir commits en `bootstrap/agent-prompts/`, `bootstrap/agent-skills/`, `core/`, `bootstrap/install-agents.py`; regenerar `bootstrap/cursor-rules/`.

---

## Notas post-implementación

_(Completar al cerrar In Build.)_
