# Contrato safe-git — SDD Kit

> **Guía (feedforward / guardrail):** restricciones Git para el agente de coding.
> Agnóstico al stack y al runtime del IDE (no define agentes ni subagentes).
> Instalación: `install-agents.py` → regla always-on `sdd-safe-git` (+ preámbulos Claude/Codex/Copilot).

**Regla short:** ejecutar **solo** el alcance literal pedido; inspeccionar divergencia antes de mutar ramas compartidas; ante conflictos **parar y preguntar**; no usar comandos irreversibles sin instrucción escrita explícita.

Detalle normativo abajo. Resumen always-on: `bootstrap/agent-prompts/sdd-safe-git.md`.

---

## 1. Alcance literal

Ejecutar **solo** lo que el humano pidió.

Ejemplo: _“elimina rama local”_ → `checkout` a otra rama + `branch -d`. **No** encadenar `pull`, `reset`, `merge --abort` ni sincronizar otras ramas salvo pedido explícito.

---

## 2. Inspección antes de mutar ramas compartidas

Antes de `git pull`, `git merge`, `git rebase` o `git reset` sobre la rama de desarrollo (`sdd.config.yaml` → `project.development_branch`):

```bash
git status -sb
git fetch origin
git log --oneline HEAD..origin/<rama>   # commits remotos que faltan local
git log --oneline origin/<rama>..HEAD   # commits locales NO en remoto
```

Si `origin/<rama>..HEAD` no está vacío → listar commits al humano y **no** continuar hasta decisión escrita (push, rama backup, o descartar con confirmación explícita).

---

## 3. Conflictos → parar

Si `pull`/`merge` produce conflictos:

- **No** encadenar `merge --abort` + `reset --hard` automáticamente.
- Reportar archivos en conflicto y opciones (resolver manual, abortar merge, crear rama backup).
- Esperar instrucción.

---

## 4. Comandos prohibidos sin instrucción explícita escrita

| Comando / patrón                                               | Motivo                              |
| -------------------------------------------------------------- | ----------------------------------- |
| `git reset --hard`                                             | Descarta commits y working tree     |
| `git clean -fd` / `-fdx`                                       | Borra archivos no rastreados        |
| `git push --force` / `--force-with-lease` en ramas compartidas | Reescribe historia remota           |
| `git branch -D`                                                | Borrado forzado sin verificar merge |
| `git checkout -- .` / `restore .` masivo                       | Descarta cambios locales            |
| `git rebase --onto` / `rebase -i`                              | Reescritura de historia             |

Pedido explícito válido (ejemplo): _“resetea `dev` a `origin/dev` aceptando perder commits locales”_ — tras mostrar `git log origin/dev..dev`.

---

## 5. Borrado seguro de rama local

1. `git fetch origin`
2. Cambiar a rama distinta (`development_branch` u otra indicada).
3. `git branch -d <rama>` si está mergeada; si falla, **preguntar** antes de `-D`.
4. No tocar otras ramas.

---

## 6. Bypass humano (opcional por instancia)

Las instancias pueden documentar en `business/` o `.env.example` una frase/variable de bypass para casos excepcionales. El kit **no** impone el nombre; solo describe el patrón aquí.

---

## Extensiones por perfil

Opcional: `profiles/<stack>/safe-git-extensions.md` (LFS, submodules, etc.). No sustituye este contrato.

---

## Relación con otras capas

- Complementa `user_rules` del humano en el IDE; no las contradice.
- No sustituye skills `sdd-open-pr` / aprobación humana para push y PR.
- Migraciones destructivas de BD son contrato **de instancia**, no de este documento.
