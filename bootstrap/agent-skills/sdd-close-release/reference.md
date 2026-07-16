# SDD Close Release — Referencia

Fuente canónica: `{{SDD_PATH}}/releases/RUNBOOK.md`.

## Orden documental

1. Specs mergeados en `{{DEV_BRANCH}}`
2. `git mv` a `archive/` + BACKLOG Released
3. Entrada `{{SDD_PATH}}/releases/vX.Y.Z/` (acta campaña)
4. Si dual-release (perfil `sdd-kit` o existe `docs/releases/`): nota producto + CHANGELOG + enlace en acta
5. `validate-sdd` + `sdd validate`
6. PR campaña → producción (merge commit)
7. Tag + sync ramas + deploy

## Dual-release (producto kit)

| Artefacto | Fuente de verdad |
| --------- | ---------------- |
| `docs/releases/vX.Y.Z.md` | Qué cambió el producto para consumidores |
| `{{SDD_PATH}}/releases/vX.Y.Z/release_*.md` | Specs/gates de la campaña SDD |
| Enlace | Acta → nota producto (obligatorio) |

Instancias consumidoras (sin capa `docs/releases/` de producto kit): solo pasos 1–3 y 5–7.

## Prohibido

- `Estado: Released` en `specs/` sin `git mv`
- Archivar antes de merge en `{{DEV_BRANCH}}`
- Cerrar tag del kit con acta y sin nota en `docs/releases/`
- Duplicar el cuerpo largo de la nota producto dentro del acta
