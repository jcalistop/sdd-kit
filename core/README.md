# SDD Core

Documentación **agnóstica al stack**. No editar con referencias a frameworks concretos; eso va en `profiles/<stack>/`.

| Documento                                  | Uso                                                      |
| ------------------------------------------ | -------------------------------------------------------- |
| [workflow.md](workflow.md)                 | Ciclo, tipos de spec, ADR, DoR/DoD proceso               |
| [operations.md](operations.md)             | Rituales y responsabilidades                             |
| [branching.md](branching.md)               | Ramas `dev` / `main`, releases, hotfix                   |
| [checklist-pr.md](checklist-pr.md)         | DoD de trazabilidad y release (común a todos los stacks) |
| [templates/](templates/)                   | Plantillas spec, ADR, PR, release, BACKLOG               |
| [releases/RUNBOOK.md](releases/RUNBOOK.md) | Fases 0 → tag → sync; deploy según perfil                |

Cada proyecto declara ramas, dominios y perfil en `sdd.config.yaml` (ver `sdd.config.example.yaml` en la raíz del kit).
