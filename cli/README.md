# CLI SDD

Herramienta de línea de comandos para operaciones SDD. Requiere **Python 3.10+** (stdlib).

## Invocación

Desde la raíz del proyecto consumidor:

```powershell
.\sdd-kit\bootstrap\sdd.ps1 validate
.\sdd-kit\bootstrap\sdd.ps1 backlog
.\sdd-kit\bootstrap\sdd.ps1 spec new --domain ux --type feature --title "Exportar Excel" --version v0.2.0
```

```bash
./sdd-kit/bootstrap/sdd.sh validate
```

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

## GitHub sync

Requiere [GitHub CLI](https://cli.github.com/) autenticado (`gh auth login`).

Etiquetas usadas: `sdd`, `sdd:draft`, `sdd:ready`, `sdd:in-build`, etc.

Crear etiquetas en el repo si `gh issue create` falla por labels inexistentes.

## Ejemplos

```powershell
# Nuevo spec
.\sdd-kit\bootstrap\sdd.ps1 spec new --domain api --type feature --title "CRUD productos"

# Métricas
.\sdd-kit\bootstrap\sdd.ps1 metrics --markdown -o .github/docs/sdd/metrics.md

# CHANGELOG tras releases
.\sdd-kit\bootstrap\sdd.ps1 release changelog
```
