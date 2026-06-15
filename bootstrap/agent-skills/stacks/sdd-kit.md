| Gate           | Comando                                                                        | Cuándo                                |
| -------------- | ------------------------------------------------------------------------------ | ------------------------------------- |
| Compilar CLI   | `python -m compileall -q cli/`                                                 | Tras editar Python del kit            |
| Manifest JSON  | validar `bootstrap/agent-prompts/manifest.json` y `agent-skills/manifest.json` | Tras cambios bootstrap                |
| Validación SDD | `python {{KIT_PATH}}/cli/sdd.py validate`                                      | Tras cambios en specs/BACKLOG del kit |
