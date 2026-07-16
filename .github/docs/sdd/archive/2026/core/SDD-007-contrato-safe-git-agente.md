# SDD-007 — Contrato safe-git para agente (Git destructivo)

---

## Cabecera

| Campo                 | Valor                                                                  |
| --------------------- | ---------------------------------------------------------------------- |
| **ID**                | `SDD-007`                                                              |
| **Dominio**           | `core`                                                                 |
| **Tipo**              | `feature` + `documentation`                                            |
| **Fecha**             | 2026-06-17                                                             |
| **Estado**            | `Released`                                                             |
| **Versión objetivo**  | `v1.3.0`                                                               |
| **Owner**             | mantenedor                                                             |
| **Prioridad**         | `P1`                                                                   |
| **ADRs relacionados** | `ADR-001`, `ADR-002`                                                   |
| **Dependencias**      | SDD-004 (skills/bootstrap); dogfooding incidente instancia consumidora |

---

## Problema y objetivo

**Problema:**

Los agentes de coding ejecutan comandos Git destructivos (`git reset --hard`, `merge --abort` encadenado, etc.) para “arreglar” conflictos o sincronizar ramas **sin petición explícita del humano** y **sin inspeccionar commits locales** no presentes en el remoto. En instancias consumidoras con `development_branch` activo (p. ej. `dev`), esto puede **descartar trabajo legítimo** aún no pusheado.

El kit SDD ya formaliza gates de metodología (Ready, verify-implementation) pero **no** un contrato transversal de seguridad Git para el agente. Las reglas de Git en `user_rules` del IDE no siempre se respetan bajo presión de “desbloquear CI” o ampliación de alcance.

**Objetivo:**

Publicar un **contrato safe-git** agnóstico de perfil de stack, instalable en todas las instancias vía `install-agents.py`, que obligue al agente a: (1) acotarse al alcance literal del pedido, (2) inspeccionar divergencia local/remoto antes de `pull`/`merge`/`reset`, (3) **parar y consultar** ante conflictos, y (4) prohibir comandos irreversibles salvo instrucción escrita explícita.

En lenguaje harness (ADR-002): safe-git es una **guía** (feedforward / guardrail) always-on; no define taxonomía de agentes ni subagentes (ADR-001).

---

## Alcance

**Incluye:**

- Documento canónico en `core/safe-git-contract.md` (texto agnóstico; sin comandos de stack; sin taxonomía agente/subagente).
- Prompt de agente `bootstrap/agent-prompts/sdd-safe-git.md` derivado del contrato (regla always-on, texto conciso — presupuesto de tokens SDD-006).
- Entrada en `bootstrap/agent-prompts/manifest.json` con `alwaysApply: true`.
- Extensión de `install-agents.py` / `sync-cursor-rules.py` para instalar `.cursor/rules/sdd-safe-git.mdc` en consumidores.
- Inyección del contrato en preámbulos multi-agente (Claude/Codex/Copilot) en bloque resumido o enlace al core.
- Fila de antipatrón en `sdd-workflow-reference` (kit y copia sincronizada en consumidores): _ampliar alcance Git más allá del pedido_.
- Tabla de comandos prohibidos / condicionados y flujos seguros (borrar rama local, sincronizar rama compartida).
- Nota producto `docs/releases/v1.3.0.md` + CHANGELOG + acta campaña con enlace (dual-release SDD-011) al cerrar release; nota en `upgrade-guide.md`.
- Test mínimo: manifest incluye `safe-git`; `install-agents.py` emite el archivo `.mdc` esperado (pytest o script existente de skills).

**Excluye:**

- Git hooks, Husky, pre-commit ni wrappers en shell del consumidor.
- Sustituir reglas Git del humano en Cursor (`user_rules`); el contrato es **capa kit**, complementaria.
- Comandos específicos de despliegue o backup por stack (perfiles pueden **extender** con `profiles/<stack>/safe-git-extensions.md` opcional).
- Reglas de migraciones destructivas de BD (patrón análogo vive en instancias; p. ej. Centinela `safe-migrations.mdc` + SDD-053).
- Automatizar `git push`, `gh pr create` o merge — siguen gobernados por skills SDD y aprobación humana.
- Definir agentes, subagentes o runtime de orquestación (ADR-001).
- Renombrar el ciclo SDD a “harness”; solo usa el marco conceptual (ADR-002 / SDD-008).

---

## Impacto técnico

| Pregunta                        | Respuesta                                                                             |
| ------------------------------- | ------------------------------------------------------------------------------------- |
| ¿Afecta código de aplicación?   | No — solo kit (`core/`, `bootstrap/`, docs)                                           |
| ¿db-change?                     | No                                                                                    |
| ¿Decisión arquitectónica nueva? | Parcial — entrega guardrail en **core** vía **bootstrap**; ADRs 001/002 ya aceptados  |
| ¿Perfiles de stack?             | No obligatorio; extensiones opcionales por perfil                                     |
| ¿Reglas de negocio kit?         | Refuerza invariante **#4** (agente ejecuta; humano aprueba) y **#1** (core agnóstico) |

### Entregables técnicos (In Build)

| Artefacto             | Ubicación                                                         |
| --------------------- | ----------------------------------------------------------------- |
| Contrato              | `core/safe-git-contract.md`                                       |
| Regla agente          | `bootstrap/agent-prompts/sdd-safe-git.md`                         |
| Cursor rule           | `.cursor/rules/sdd-safe-git.mdc` (kit dogfooding, vía sync)       |
| Manifest              | `bootstrap/agent-prompts/manifest.json` → clave `safe_git`        |
| Referencia antipatrón | `bootstrap/agent-prompts/sdd-workflow-reference.md` (sección Git) |

### Contrato (borrador normativo)

#### 1. Alcance literal

- Ejecutar **solo** lo que el humano pidió. Ejemplo: _“elimina rama local”_ → `checkout` + `branch -d`; **no** `pull`, `reset`, `merge --abort` ni sincronización de otras ramas salvo pedido explícito.

#### 2. Inspección antes de mutar ramas compartidas

Antes de `git pull`, `git merge`, `git rebase` o `git reset` sobre la rama de desarrollo (`sdd.config.yaml` → `project.development_branch`):

```bash
git status -sb
git fetch origin
git log --oneline HEAD..origin/<rama>   # commits remotos que faltan local
git log --oneline origin/<rama>..HEAD   # commits locales NO en remoto
```

Si `origin/<rama>..HEAD` no está vacío → **informar al humano** con el listado y **no** continuar hasta decisión (push, rama backup, descartar con confirmación escrita).

#### 3. Conflictos → parar

Si `pull`/`merge` produce conflictos:

- **No** encadenar `merge --abort` + `reset --hard` automáticamente.
- Reportar archivos en conflicto y opciones (resolver manual, abortar merge, crear rama backup).
- Esperar instrucción.

#### 4. Comandos prohibidos sin instrucción explícita escrita

| Comando / patrón                                               | Motivo                              |
| -------------------------------------------------------------- | ----------------------------------- |
| `git reset --hard`                                             | Descarta commits y working tree     |
| `git clean -fd` / `-fdx`                                       | Borra archivos no rastreados        |
| `git push --force` / `--force-with-lease` en ramas compartidas | Reescribe historia remota           |
| `git branch -D`                                                | Borrado forzado sin verificar merge |
| `git checkout -- .` / `restore .` masivo                       | Descarta cambios locales            |
| `git rebase --onto` / `rebase -i`                              | Reescritura de historia             |

#### 5. Borrado seguro de rama local (flujo recomendado)

1. `git fetch origin`
2. Cambiar a rama distinta (`development_branch` u otra indicada).
3. `git branch -d <rama>` si está mergeada; si falla, **preguntar** antes de `-D`.
4. No tocar otras ramas.

#### 6. Bypass humano (opcional por instancia)

Las instancias **pueden** documentar en su `business/` o `.env.example` una variable/frase de bypass para casos excepcionales (análogo a `CENTINELA_ALLOW_DESTRUCTIVE_DATABASE_COMMANDS`). El kit **no** impone nombre de variable; solo documenta el patrón en `core/safe-git-contract.md`.

---

## Reglas de negocio (kit)

| ID    | Regla aplicable                                                   |
| ----- | ----------------------------------------------------------------- |
| DR-#1 | Core agnóstico — contrato sin referencias a Laravel, npm, etc.    |
| DR-#4 | Humano aprueba acciones irreversibles; el agente reporta y espera |
| DR-#6 | Spec y BACKLOG solo en `paths.sdd` del kit                        |
| DR-#7 | Dual-release al cerrar `v1.3.0`: nota producto + acta campaña     |

---

## Criterios de aceptación

**Happy path:**

- [x] `core/safe-git-contract.md` publicado y enlazado desde `core/workflow.md` (sección reglas always-on).
- [x] Contrato redactado sin taxonomía agente/subagente (ADR-001); puede etiquetarse como guía/guardrail (ADR-002).
- [x] `sdd-safe-git.md` instalado en consumidor tras `install-agents.py install --agent cursor`.
- [x] Regla aparece con `alwaysApply: true` en `.cursor/rules/sdd-safe-git.mdc`.
- [x] Preambles Claude/Codex/Copilot mencionan safe-git o enlace al contrato.
- [x] `python cli/sdd.py validate` en verde en repo kit.
- [ ] Upgrade documentado en `docs/releases/v1.3.0.md` + CHANGELOG + acta con enlace (SDD-011) y paso “reinstalar agent”. _(Nota producto/acta: diferido a cierre de campaña v1.3.0; paso reinstalar agent ya en `upgrade-guide.md`.)_

**Error path / comportamiento agente (verificación manual o escenario documentado):**

- [x] Pedido “borra rama local” con `dev` ahead of `origin/dev` → agente **no** ejecuta `reset --hard`. _(Cubierto por regla normativa + escenarios documentados en contrato; smoke manual humano.)_
- [x] `pull` con conflictos → agente reporta y **no** auto-repara con reset. _(Idem.)_
- [x] Pedido explícito “resetea dev a origin/dev aceptando perder commits locales” → permitido tras mostrar `git log origin/dev..dev`. _(Idem.)_

**Consumidor de referencia:**

- [ ] Instancia Centinela (u otra) reinstala kit ≥ v1.3.0 y confirma presencia de regla sin duplicar `safe-migrations`. _(Pendiente smoke humano post-release.)_
---

## Riesgos

| Riesgo                                              | Prob. | Impacto | Mitigación                                            |
| --------------------------------------------------- | ----- | ------- | ----------------------------------------------------- |
| Regla always-on aumenta tokens                      | Media | Bajo    | Texto conciso (SDD-006); detalle en core on-demand    |
| Duplicación con `user_rules` del humano             | Media | Bajo    | Complementariedad documentada; no contradecir         |
| Agente ignora regla bajo urgencia                   | Media | Alto    | Antipatrón en reference + incidente en notas del spec |
| Perfiles necesitan Git específico (LFS, submodules) | Baja  | Medio   | Extensiones opcionales en `profiles/`                 |

---

## Vigencia (revisión 2026-07-15)

| Frente | Evaluación |
| ------ | ---------- |
| **Problema / alcance normativo** | Vigente — incidente reales; borador de contrato intacto |
| **ADR-001** | Compatible — no define agentes/subagentes; aplica al ejecutor sea cual sea |
| **ADR-002 / SDD-008** | Compatible — se cataloga como guía/guardrail; no bloquea por SDD-008 |
| **SDD-006** | Restricción — keep always-on corto |
| **SDD-011** | Complemento — notes de `v1.3.0` siguen dual-release |
| **SDD-009 / SDD-010** | Ortogonales — sin conflicto |

**Conclusión:** Ready para implementar; no requiere rewrite de alcance.

---

## Notas

**Origen (2026-06-17):** incidente en instancia consumidora — tras merge remoto exitoso, pedido de borrar rama feature; el agente ejecutó `git reset --hard origin/dev` al resolver conflictos de `pull`, descartando commits locales en `dev`. Recuperación manual desde otras sesiones.

**Relación con patrones existentes:**

- Centinela: `.cursor/rules/safe-migrations.mdc` (instancia, dominio BD).
- Kit: este SDD generaliza **Git** para **todas** las instancias sin acoplar al perfil Voyager/Laravel.
- Research harness: atributo “Guardrails como código” mapeado a este SDD.

---

## Primer paso de implementación (Ready → In Build)

1. Redactar `core/safe-git-contract.md` (versión final del borrador normativo; etiqueta guía/guardrail opcional).
2. Añadir `sdd-safe-git.md` + manifest + `install-agents.py`.
3. `sync-cursor-rules.py` y validar dogfooding en repo kit.
4. Dual-release `v1.3.0` (nota producto + acta) + upgrade-guide (puede esperar al cierre de campaña con otros SDD v1.3.0).
