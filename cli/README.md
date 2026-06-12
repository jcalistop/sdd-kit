# CLI SDD

Herramienta de línea de comandos para operaciones SDD. Requiere **Python 3.10+** (stdlib).

## Invocación

Desde la raíz del proyecto consumidor (CMD, PowerShell o bash — requiere Python 3.10+):

```bash
python sdd-kit/cli/sdd.py validate
python sdd-kit/cli/sdd.py backlog
python sdd-kit/cli/sdd.py spec new --domain ux --type feature --title "Exportar Excel" --version v0.2.0
```

Atajos opcionales: `./sdd-kit/bootstrap/sdd.sh` (bash) · `.\sdd-kit\bootstrap\sdd.ps1` (solo PowerShell; en CMD no ejecuta el `.ps1`).

Variable de entorno opcional: `SDD_PATH` (default: `.github/docs/sdd`).

## Comandos

| Comando                                                                                          | Descripción                                |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------ |
| `init --profile NAME --project "App" [--agent auto\|cursor,claude,...] [--no-prompt] [--cursor]` | Ejecuta `init-sdd` + adaptadores de agente |
| `validate`                                                                                       | Coherencia BACKLOG / specs / archive       |
| `backlog [--state Draft] [--domain ux]`                                                          | Lista BACKLOG                              |
| `backlog sync [--direction push\|pull\|both] [--dry-run]`                                        | Sync con GitHub Issues (`gh`)              |
| `spec new --domain D --title "..." [--type feature] [--version v0.1.0]`                          | Crea spec Draft + BACKLOG                  |
| `spec status SDD-005`                                                                            | Estado y transiciones posibles             |
| `release changelog [-o path]`                                                                    | Genera `CHANGELOG.md` (Keep a Changelog)   |
| `release close v1.2.0 [--changelog] [--force]`                                                   | Checklist pre-campaña                      |
| `metrics [--markdown] [-o report.md]`                                                            | Salud del proceso SDD                      |
| `prompt list [--category adoption\|workflow\|exceptions] [--phase Draft]`                        | Catálogo de prompts copy-paste             |
| `prompt show <id> [--full]`                                                                      | Imprime prompt listo para pegar al agente  |

## GitHub sync

Requiere [GitHub CLI](https://cli.github.com/) autenticado (`gh auth login`).

Etiquetas usadas: `sdd`, `sdd:draft`, `sdd:ready`, `sdd:in-build`, etc.

Crear etiquetas en el repo si `gh issue create` falla por labels inexistentes.

## Ejemplos

```bash
# Nuevo spec
python sdd-kit/cli/sdd.py spec new --domain api --type feature --title "CRUD productos"

# Métricas
python sdd-kit/cli/sdd.py metrics --markdown -o .github/docs/sdd/metrics.md

# CHANGELOG tras releases
python sdd-kit/cli/sdd.py release changelog

# Catálogo de prompts
python sdd-kit/cli/sdd.py prompt list
python sdd-kit/cli/sdd.py prompt show adopt-existing
python sdd-kit/cli/sdd.py prompt show discovery-to-draft --full
```

Ver también: [core/prompt-catalog.md](../core/prompt-catalog.md).
