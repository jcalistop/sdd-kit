# Configuración de agentes IA — SDD Kit

> Qué herramienta lee qué archivo, cómo reinstalar adaptadores y cómo trabajar sin agente.

**Relacionado:** [`adoption-guide.md`](adoption-guide.md) · [`INSTALL.md`](../INSTALL.md)

---

## Resumen

El **core SDD** (BACKLOG, specs, CLI, `validate-sdd`) no depende de ningún IDE. La capa **agentica** instala instrucciones en el formato que cada herramienta reconoce.

| Herramienta        | Archivo instalado                      | Cuándo se aplica                      |
| ------------------ | -------------------------------------- | ------------------------------------- |
| **Cursor**         | `.cursor/rules/sdd-*.mdc` (3 archivos) | Cada chat (`alwaysApply: true`)       |
| **Claude Code**    | `CLAUDE.md` (bloque delimitado)        | Cada sesión en el proyecto            |
| **Codex**          | `AGENTS.md` (bloque delimitado)        | Cada sesión Codex en el repo          |
| **GitHub Copilot** | `.github/copilot-instructions.md`      | Instrucciones persistentes en VS Code |

La fuente única de contenido está en `sdd-kit/bootstrap/agent-prompts/`; los adaptadores solo cambian el envoltorio.

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

```powershell
python .\sdd-kit\bootstrap\install-agents.py install `
  --profile laravel-filament `
  --agent cursor,claude `
  --sdd-path .github/docs/sdd
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

Útil para saber qué archivos deberían existir en el proyecto.

---

## Trabajar sin adaptador instalado

1. Lee [`workflow.md`](workflow.md) y [`adoption-guide.md`](adoption-guide.md).
2. Pide al agente explícitamente: _"Sigue el flujo de `sdd-agent-workflow` en sdd-kit; crea spec Draft para [idea]."_
3. Usa la CLI: `.\sdd-kit\bootstrap\sdd.ps1 spec new ...` y `validate`.

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
- Validación automática de archivos según `agent.targets` en `validate-sdd`.
- Skills Cursor opcionales (`/sdd-release`).
