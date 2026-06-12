# Catálogo de prompts — notas para mantenedores

> Documentación interna del catálogo de plantillas copy-paste para usuarios del kit.
> Implementado: 2026-06-12. Audiencia consumidora: [`core/prompt-catalog.md`](../../core/prompt-catalog.md).

---

## Problema que resuelve

Las **reglas del agente** (`sdd-core`, `sdd-agent-workflow`) cubren el flujo autónomo, pero faltaban **disparadores explícitos** para momentos donde el humano inicia o aprueba (adopción, Ready, merge, release, excepciones). Esos textos estaban dispersos en `README.md`, `INSTALL.md` y `adoption-guide.md`.

El catálogo centraliza ~15 prompts en fichas con frontmatter YAML, índice Markdown y descubrimiento vía CLI.

---

## Arquitectura: dos capas de prompts

| Capa | Ubicación | Quién lo usa | Siempre activo |
| ---- | --------- | ------------ | -------------- |
| **Reglas del agente** | `bootstrap/agent-prompts/` → Cursor/CLAUDE.md/… | Agente | Sí (`alwaysApply` en Cursor) |
| **Prompts del usuario** | `core/prompts/` + `core/prompt-catalog.md` | Humano (copy-paste al chat) | No |

No duplicar el contenido de `sdd-agent-workflow.md` en las fichas: los prompts del catálogo son cortos (5–15 líneas) y asumen que las reglas ya están instaladas.

---

## Estructura de archivos

```
core/
├── prompt-catalog.md          # Índice (3 ejes: momento, fase SDD, etapa adopción)
└── prompts/
    ├── adoption/              # 4 fichas (onboarding)
    ├── workflow/              # 7 fichas (ciclo por transición)
    └── exceptions/            # 4 fichas (hotfix, spec atascado, migración docs, submodule)
cli/lib/prompts.py             # Parser frontmatter + list/show
```

`init-sdd` copia `prompt-catalog.md` y `prompts/` a `.github/docs/sdd/` en proyectos consumidores.

---

## Formato de una ficha

Cada `core/prompts/<categoria>/<id>.md` incluye:

1. **Frontmatter YAML** — fuente de verdad para `sdd prompt list` (`id`, `title`, `category`, `workflow_phase`, `human_approval`, etc.)
2. **Cuándo usarlo** / **Qué hará el agente** / **Después de pegarlo** / **Ver también**
3. **Bloque `## Prompt`** con fenced code block — lo que imprime `sdd prompt show <id>`

Convenciones:

- Placeholders en `<MAYÚSCULAS>` (`<PERFIL>`, `<SDD-NNN>`, …)
- `human_approval: true` cuando requiere OK explícito del humano
- Español latino; tono directo

---

## CLI

```bash
sdd prompt list
sdd prompt list --category adoption
sdd prompt list --phase Draft
sdd prompt show adopt-existing
sdd prompt show adopt-existing --full
```

Resolución de rutas (`cli/lib/prompts.py`):

1. Si existe `.github/docs/sdd/prompts/` con fichas → usa instancia local
2. Si no → `kit_root()/core/prompts/`

Parser de frontmatter sin dependencias externas (regex + líneas YAML simples).

---

## Inventario actual (15 prompts)

| ID | Categoría |
| -- | --------- |
| `adopt-new`, `adopt-existing`, `validate-setup`, `formalize-domain-rules` | adoption |
| `discovery-to-draft`, `draft-review`, `approve-ready`, `implement-spec`, `open-pr`, `validate-pr`, `close-release` | workflow |
| `hotfix-minor`, `spec-stuck`, `migrate-legacy-docs`, `update-submodule` | exceptions |

---

## Cómo añadir o editar un prompt

1. Crear `core/prompts/<categoria>/<id>.md` con frontmatter `id` único.
2. Añadir fila en [`core/prompt-catalog.md`](../../core/prompt-catalog.md) (tablas por momento / fase / etapa).
3. Enlazar desde docs de usuario si aplica (`workflow.md`, `adoption-guide.md`).
4. Probar: `python cli/sdd.py prompt list` y `prompt show <id>`.
5. No editar solo la copia en un proyecto consumidor — el submodule es la fuente; `init-sdd` re-copia en instalaciones nuevas.

---

## Integración en documentación de usuario

| Archivo | Cambio |
| ------- | ------ |
| `README.md` | Fila en navegación rápida; Paso 3/6 apuntan al catálogo |
| `INSTALL.md` | Prompt de adopción vía `sdd prompt show adopt-existing` |
| `core/adoption-guide.md` | Enlaces por etapa; escenario docs dispersos (sin asumir wiki/Notion) |
| `core/workflow.md` | Tabla fase → prompt ID |
| `cli/README.md` | Comandos `prompt list/show` |

### Migración de documentación legacy (redacción inclusiva)

La regla en `INSTALL.md` y el prompt `migrate-legacy-docs` hablan de **cualquier documentación previa** (READMEs, `docs/`, herramientas externas), no solo wiki/Notion. La consolidación a `business/` es **Etapa 3**, no parte del bootstrap.

---

## Fuera de alcance v1 (evolución futura)

- **Cursor Skills** (`/sdd-adopt`, etc.) — el catálogo Markdown es la fuente única a envolver después
- **Dashboard Canvas** — pendiente en ROADMAP 3.4
- Validación CI del catálogo (IDs duplicados, frontmatter obligatorio) — candidato a añadir en `validate-sdd` o test CLI

---

## Referencias

- [core/prompt-catalog.md](../../core/prompt-catalog.md) — índice para usuarios
- [ROADMAP.md](ROADMAP.md) — Fase 3, entregable 3.6
- [ANALYSIS.md](ANALYSIS.md) — brecha de prompts dispersos (oportunidad cerrada)
