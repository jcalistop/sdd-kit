# Configuración de agentes IA — SDD Kit

> Qué herramienta lee qué archivo, cómo reinstalar adaptadores y cómo trabajar sin agente.

**Relacionado:** [`adoption-guide.md`](adoption-guide.md) · [`INSTALL.md`](../INSTALL.md)

---

## Resumen

El **core SDD** (BACKLOG, specs, CLI, `validate-sdd`) no depende de ningún IDE. La capa **agentica** instala el **harness SDD** en el formato que cada herramienta reconoce: no es un plugin, es la configuración del entorno de ejecución del agente (guías, sensores, skills y reglas).

| Herramienta        | Archivo instalado                                                          | Cuándo se aplica                                                                               |
| ------------------ | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Cursor**         | `.cursor/rules/sdd-*.mdc` (workflow + safe-git always-on; reference/stack on-demand) + `.cursor/skills/sdd-*` (6 skills) | Workflow y safe-git en cada chat; reference y stack bajo demanda; skills on-demand |
| **Claude Code**    | `CLAUDE.md` (bloque delimitado)                                            | Cada sesión en el proyecto                                                                     |
| **Codex**          | `AGENTS.md` (bloque delimitado)                                            | Cada sesión Codex en el repo                                                                   |
| **GitHub Copilot** | `.github/copilot-instructions.md`                                          | Instrucciones persistentes en VS Code                                                          |

La fuente única de contenido está en `sdd-kit/bootstrap/agent-prompts/` (reglas) y `sdd-kit/bootstrap/agent-skills/` (skills Cursor); los adaptadores solo cambian el envoltorio.

**Skills Cursor (v1.2.0+):** `install-agents.py` instala las 6 skills `sdd-*` desde `bootstrap/agent-skills/manifest.json`. Solo sobrescribe carpetas del manifest; no toca skills Boost del proyecto. **Precedencia:** skills SDD on-demand > `sdd prompt show` copy-paste > reglas on-demand.

**Claude / Codex / Copilot:** el preambulo del bloque marcado incluye mapa trigger → prompt kit (paridad con skills Cursor) y **mención** de safe-git (párrafo corto). **No** reciben la regla completa `sdd-safe-git.mdc`: el contrato íntegro vive en Cursor (`alwaysApply`) y en [`safe-git-contract.md`](safe-git-contract.md). Esa asimetría es intencional (tokens / formato del adaptador); no implica que el contrato no aplique al humano — el agente no-Cursor solo ve el resumen del preamble.

**Dogfood del repositorio sdd-kit:** este repo productor usa `agent.targets: [cursor]` a propósito. No se versionan `CLAUDE.md` / `AGENTS.md` / `copilot-instructions` en el kit salvo decisión explícita de mantenedores. Los consumidores sí pueden declarar varios targets e instalarlos con `install-agents`.

**Cursor — política de tokens:** `sdd-agent-workflow.mdc` y `sdd-safe-git.mdc` usan `alwaysApply: true` (safe-git es texto corto). `sdd-workflow-reference.mdc` (checklists DoR/DoD, antipatrones) y `sdd-stack-<perfil>.mdc` usan `alwaysApply: false` y se leen en fases Draft, In Build o Validating. Las skills `sdd-draft-spec` y `sdd-build-spec` incluyen la instrucción de lectura previa (`BACKLOG.md`, `sdd.config.yaml`, `domain-rules.md`), evitando cargarla en tareas no-SDD. Detalle: [`.github/docs/business/planning/TOKEN-OPTIMIZATION.md`](../.github/docs/business/planning/TOKEN-OPTIMIZATION.md). Contrato canónico: [`safe-git-contract.md`](safe-git-contract.md).

### Ciclo SDD con agente (resumen)

| Qué                      | Detalle                                                                                |
| ------------------------ | -------------------------------------------------------------------------------------- |
| **Estados**              | Discovery → Draft → Ready → In Build → Validating → Released (`workflow.md`)           |
| **Prompts**              | Disparadores opcionales del [catálogo](prompt-catalog.md); no son fases obligatorias   |
| **Aprobaciones humanas** | Ready (spec) y merge del PR — frase corta basta                                        |
| **Verify local**         | Obligatorio antes de `push`/PR (`verify-implementation`); ver `sdd-workflow-reference` |
| **Deprecados**           | `approve-ready` / `implement-spec` → `build-spec` (`sdd prompt show` redirige)         |

Tras instalar adaptadores, describe la iniciativa en lenguaje natural; el agente sigue `sdd-agent-workflow` sin copiar prompts en cada paso.

---

## Instalación

### Automática (recomendada)

`init-sdd` detecta el entorno y, si hay ambigüedad, muestra un menú:

```powershell
.\sdd-kit\bootstrap\init-sdd.ps1 -Profile laravel-filament -Project "Mi App"
```

```bash
./sdd-kit/bootstrap/init-sdd.sh --profile python-fastapi --project "API"
```

### Explícita

```powershell
.\sdd-kit\bootstrap\init-sdd.ps1 -Profile react-vite -Project "App" -Agent cursor,claude
```

```bash
./sdd-kit/bootstrap/init-sdd.sh --profile react-vite --project "App" --agent codex,copilot
```

### Sin adaptadores (solo documentación SDD)

```powershell
.\sdd-kit\bootstrap\init-sdd.ps1 -Profile laravel-filament -Project "Mi App" -Agent none
```

### CI / sin menú interactivo

```powershell
.\sdd-kit\bootstrap\init-sdd.ps1 -Profile laravel-filament -Project "CI" -Agent cursor -NoPrompt
```

Con `--no-prompt` y `--agent auto`: solo instala si hay **un** candidato claro; si no, omite y muestra aviso.

### Reinstalar o actualizar tras actualizar el kit

Flujo completo (submodule, merge de instancia, log de version): [`upgrade-guide.md`](upgrade-guide.md). Prompt: `upgrade-kit` en [prompt-catalog.md](prompt-catalog.md).

Reinstalar solo adaptadores (paso del runbook):

```powershell
python .\sdd-kit\bootstrap\install-agents.py install `
  --profile laravel-filament `
  --agent cursor,claude `
  --sdd-path .github/docs/sdd `
  --kit-path .github/docs/sdd-kit
```

Los archivos `CLAUDE.md`, `AGENTS.md` y `copilot-instructions.md` usan marcadores `<!-- sdd-kit:agent-instructions:start/end -->` para no pisar contenido ajeno.

### Ver detección sin instalar

```powershell
python .\sdd-kit\bootstrap\install-agents.py detect
```

---

## Retrocompatibilidad

`-Cursor` / `--cursor` equivale a `-Agent cursor` / `--agent cursor`.

---

## Registro en configuración

Tras instalar, `sdd.config.yaml` incluye:

```yaml
agent:
  targets: [cursor]
  install_mode: auto # auto | explicit | none
```

Útil para saber qué archivos deberían existir en el proyecto. Tras un **upgrade-kit**, reinstalar adaptadores con `--agent` igual a la lista `agent.targets` (coma-separada), no asumir solo `cursor`.

---

## Trabajar sin adaptador instalado

1. Lee [`workflow.md`](workflow.md) y [`adoption-guide.md`](adoption-guide.md).
2. Pide al agente explícitamente: _"Sigue el flujo de `sdd-agent-workflow` en sdd-kit; crea spec Draft para [idea]."_
3. Usa la CLI: `python sdd-kit/cli/sdd.py spec new ...` y `validate`.

---

## Señales de detección (heurísticas)

| Agente      | Señales                                              |
| ----------- | ---------------------------------------------------- |
| Cursor      | Variables `CURSOR_*`, carpeta `.cursor/`             |
| Claude Code | `CLAUDE_CODE`, carpeta `.claude/`, `CLAUDE.md`       |
| Codex       | `AGENTS.md`, variables `CODEX_HOME` / `OPENAI_CODEX` |
| Copilot     | `.vscode/`, extensión Copilot en `extensions.json`   |

La detección no es infalible. Usa `--agent` explícito si el menú no coincide con tu entorno.

---

## Nuevo perfil de stack

Además de la regla Cursor, añade el prompt en:

```
sdd-kit/bootstrap/agent-prompts/stacks/<perfil>.md
```

Y actualiza `stack-descriptions.json`. Ver [`templates/profile-template.md`](templates/profile-template.md).

---

## Fuera de alcance actual

- Antigravity (sin adaptador empaquetado).
- Validación automática exhaustiva de skills según `agent.targets` (solo advertencia en `validate-sdd` si falta manifest).
