# SDD Core

Documentación **agnóstica al stack**. No editar con referencias a frameworks concretos; eso va en `profiles/<stack>/`.

| Documento                                                      | Uso                                                                     |
| -------------------------------------------------------------- | ----------------------------------------------------------------------- |
| [workflow.md](workflow.md)                                     | Ciclo, tipos de spec, ADR, DoR/DoD proceso                              |
| [adoption-guide.md](adoption-guide.md)                         | Adopción incremental en proyectos nuevos y existentes                   |
| [operations.md](operations.md)                                 | Rituales y responsabilidades                                            |
| [branching.md](branching.md)                                   | Ramas `dev` / `main`, releases, hotfix                                  |
| [checklist-pr.md](checklist-pr.md)                             | DoD de trazabilidad y release (común a todos los stacks)                |
| [healthy-development.md](healthy-development.md)               | Arquitectura, patrones, antipatrones, codigo limpio (humanos y agentes) |
| [templates/](templates/)                                       | Plantillas spec, ADR, PR, release, BACKLOG, dominio                     |
| [templates/profile-template.md](templates/profile-template.md) | Guía para crear perfiles de nuevos stacks                               |
| [releases/RUNBOOK.md](releases/RUNBOOK.md)                     | Fases 0 → tag → sync; deploy según perfil                               |

Cada proyecto declara ramas, dominios y perfil en `sdd.config.yaml` (ver `sdd.config.example.yaml` en la raíz del kit).
