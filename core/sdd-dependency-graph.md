# Grafo de dependencias SDD — contexto mínimo por skill

> Cada skill `sdd-*` declara su "dependency closure": los archivos que necesita leer antes de ejecutar.
> El agente debe cargar solo estos archivos, no todo el contexto SDD.

---

## Regla general

- **Solo leer** los archivos listados en la columna "Requeridos" para la skill activa.
- **No leer** specs de otras features, ADRs no relacionados ni releases anteriores a menos que la skill los referencie explícitamente.
- **Archivos opcionales:** leer solo si el spec o la tarea los menciona por ID.

---

## Por skill

| Skill | Archivos requeridos | Archivos opcionales | ~Tokens estimados |
|-------|--------------------|--------------------|--------------------|
| `sdd-draft-spec` | `BACKLOG.md`, `sdd.config.yaml`, `domain-rules.md`, `spec-template.md` (o `spec-compact-template.md`) | ADR relacionados, `research/` pertinente | 3-5k |
| `sdd-build-spec` | Spec del SDD-NNN, `domain-rules.md`, `.cursor/rules/sdd-stack-<profile>.mdc` | ADR referenciados en el spec, `research/` pertinente | 4-8k |
| `sdd-verify-implementation` | Spec del SDD-NNN (solo criterios de aceptación), `domain-rules.md` | `.cursor/rules/sdd-stack-<profile>.mdc` | 2-4k |
| `sdd-open-pr` | Spec del SDD-NNN (solo cabecera), `BACKLOG.md`, `checklist-pr.md` | — | 1-2k |
| `sdd-close-release` | `BACKLOG.md`, specs a archivar (solo cabeceras), `sdd.config.yaml`, `releases/RUNBOOK.md` | — | 2-3k |
| `sdd-upgrade-kit` | `sdd.config.yaml`, `UPGRADE-LOG.md` | — | 1-2k |

---

## Anti-patrones de contexto (NO hacer)

1. **Leer `BACKLOG.md` completo** cuando solo necesitas el próximo ID → leer solo `ids.next_sdd` del config y la línea `Próximo ID disponible`.
2. **Leer specs de otras features** durante verify → solo leer el spec del SDD-NNN activo.
3. **Cargar todos los ADR** → solo los referenciados en `ADRs relacionados` de la cabecera del spec.
4. **Re-leer `domain-rules.md`** en cada fase → leer una vez al inicio de la sesión; confiar en cache para relecturas.
5. **Leer `releases/` anteriores** durante draft → innecesario; el BACKLOG contiene el histórico de Released.

---

## Fundamento (token economics)

Cada archivo leído innecesariamente suma 1-5k tokens al contexto que se reenvía en cada turno posterior (input tokens = 53.9% del total). Scoping preciso de dependencias ahorra 8-15k tokens por sesión SDD típica. Fuente: [research/2026-07-15-token-economics-sdd-harness.md](../research/2026-07-15-token-economics-sdd-harness.md).
