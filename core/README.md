# SDD Core

Documentación **agnóstica al stack**. No editar con referencias a frameworks concretos; eso va en profiles/<stack>/.

## Entrada y contratos (raíz)

| Documento | Uso |
| --------- | --- |
| [workflow.md](workflow.md) | Ciclo, tipos de spec, ADR, DoR/DoD proceso |
| [concepts.md](concepts.md) | Glosario y modelo mental |
| [prompt-catalog.md](prompt-catalog.md) | Catálogo de prompts copy-paste (adopción, ciclo, excepciones) |
| [safe-git-contract.md](safe-git-contract.md) | Contrato Git destructivo (harness) |
| [sdd-dependency-graph.md](sdd-dependency-graph.md) | Grafo de dependencias de contexto |
| [templates/](templates/) | Plantillas spec, ADR, PR, release, BACKLOG, dominio |
| [templates/profile-template.md](templates/profile-template.md) | Guía para crear perfiles de nuevos stacks |
| [releases/RUNBOOK.md](releases/RUNBOOK.md) | Fases 0 → tag → sync; deploy según perfil |

## Guías (guides/)

Metodologías operativas y opcionales. Índice: [guides/README.md](guides/README.md).

| Documento | Uso |
| --------- | --- |
| [guides/adoption-guide.md](guides/adoption-guide.md) | Adopción incremental |
| [guides/upgrade-guide.md](guides/upgrade-guide.md) | Actualizar kit en instancia consumidora |
| [guides/agent-setup.md](guides/agent-setup.md) | Adaptadores multi-agente / IDE |
| [guides/operations.md](guides/operations.md) | Rituales y responsabilidades |
| [guides/branching.md](guides/branching.md) | Ramas dev / main, releases, hotfix |
| [guides/checklist-pr.md](guides/checklist-pr.md) | DoD de trazabilidad y release (común a todos los stacks) |
| [guides/healthy-development.md](guides/healthy-development.md) | Arquitectura, patrones, antipatrones, código limpio |
| [guides/audits.md](guides/audits.md) / [guides/research.md](guides/research.md) | Metodologías opcionales (artefactos bajo paths.sdd) |

Cada proyecto declara ramas, dominios y perfil en sdd.config.yaml (ver sdd.config.example.yaml en la raíz del kit).
