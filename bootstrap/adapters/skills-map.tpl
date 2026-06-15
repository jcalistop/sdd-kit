
### Skills SDD (Cursor)

Preferir **skill** sobre copy-paste de prompt cuando el trigger coincide. Fuente: `{{KIT_PATH}}/bootstrap/agent-skills/manifest.json`.

{{SKILLS_MAP_TABLE}}

CLI: `python {{KIT_PATH}}/cli/sdd.py prompt show <id> --full`

**Precedencia:** skills SDD on-demand > prompts CLI copy-paste > reglas on-demand (`sdd-workflow-reference`, stack).
