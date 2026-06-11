# Plantilla — Crear perfil de stack

> Guía para añadir `profiles/<nombre>/` sin modificar `core/`.
> Copiar esta estructura y reemplazar placeholders.

---

## Archivos obligatorios

```
profiles/<nombre-perfil>/
├── README.md                    # Índice + quality gates
├── sdd.config.yaml              # Valores por defecto del perfil
├── checklist-stack.md           # DoD técnico específico del stack
├── spec-impact.md               # Tabla de impacto técnico para specs
├── deploy.md                    # Procedimiento de despliegue
├── release-deploy-section.md    # Bloque copiable a notas de release
├── branching-extensions.md      # Opcional pero recomendado (Dependabot)
└── examples/
    └── SDD-001-<slug>.md        # Spec de ejemplo como referencia de calidad
```

Además en el kit (no en el perfil):

```
bootstrap/agent-prompts/stacks/<nombre-perfil>.md   # fuente unica del prompt de stack
bootstrap/agent-prompts/stack-descriptions.json   # descripcion para reglas Cursor
```

Opcional (legacy / referencia): `bootstrap/cursor-rules/sdd-stack-<nombre-perfil>.mdc` — en install se genera desde `agent-prompts/`.

---

## README.md

Secciones mínimas:

1. Título: `# Perfil: <Stack>`
2. Tabla de archivos con enlaces
3. Lista de **quality gates** por defecto (comandos exactos)
4. Enlace al spec de ejemplo

---

## sdd.config.yaml

```yaml
stack:
  profile: <nombre-perfil>
  ci_workflow: .github/workflows/ci.yml
  quality_gates:
    test: "<comando test>"
    lint: "<comando lint>"
    # format, types según stack
  schema_changes: <ruta migraciones o null>
  deploy_platform: <laravel-cloud | docker-or-paas | static-hosting | intranet-orchestrator>

domains_suggested:
  - auth
  - ux
  - infra
  - docs
```

---

## checklist-stack.md

Secciones recomendadas:

1. **Calidad técnica** — comandos del perfil + CI verde
2. **Área específica del stack** — UI, API, componentes, etc.
3. **Reglas de negocio** — referencia a `business/domain-rules.md`
4. **Cambio de BD** — si aplica
5. **Post-deploy** — enlace a `deploy.md`

Cada ítem debe permitir **No aplica**.

---

## spec-impact.md

- Tabla con 6–10 preguntas técnicas del stack
- Última fila: ¿ADR transversal?
- Sección **Regla de esquema** si hay base de datos
- Referencia a `business/domain-rules.md` — **no** incluir reglas de negocio del proyecto

---

## deploy.md

- Principio (auto vs manual)
- Tabla CI vs Deploy
- Pasos alineados con Fase 4 del `releases/RUNBOOK.md`
- Comandos concretos
- Checklist smoke post-deploy
- Rollback breve

---

## release-deploy-section.md

Bloque markdown copiable a `releases/vX.Y.Z/release_vX.Y.Z.md`:

- Checklist de deploy (5–8 ítems)
- Validación post-despliegue (3–5 ítems)

---

## branching-extensions.md

Si el stack usa Dependabot:

- Rama `deps-integration`
- Sin spec para bumps rutinarios
- Workflows sugeridos en repo consumidor

---

## examples/SDD-001-\*.md

Spec completo que demuestre:

- Cabecera llena
- Problema/objetivo/alcance
- Impacto técnico respondido
- Criterios happy + error path
- Diseño técnico con tabla de archivos
- Comandos de verificación del perfil

---

## Regla Cursor: `sdd-stack-<perfil>.mdc`

```markdown
---
description: SDD — perfil <Stack> (...)
alwaysApply: true
---

# SDD Stack — <Stack>

Perfil activo cuando `sdd.config.yaml` → `stack.profile: <perfil>`.

## Quality gates

(comandos)

## Convenciones del stack

(estructura de carpetas, patrones)

## Deploy

(enlace a deploy.md)

## Dependabot (si aplica)
```

---

## Checklist de perfil completo

- [ ] Los 7+ archivos creados en `profiles/<perfil>/`
- [ ] Prompt `bootstrap/agent-prompts/stacks/<perfil>.md` + entrada en `stack-descriptions.json`
- [ ] `init-sdd` reconoce el perfil (carpeta existe → OK automático)
- [ ] Spec de ejemplo realista para el stack
- [ ] Sin reglas de negocio de un proyecto concreto en el perfil
- [ ] Entrada en `README.md` e `INSTALL.md` del kit
- [ ] `validate-sdd` pasa en instancia de prueba con el perfil

---

## Perfiles de referencia

| Perfil             | Stack                        |
| ------------------ | ---------------------------- |
| `laravel-filament` | Laravel + Filament           |
| `laravel-voyager`  | Laravel + Voyager + Livewire |
| `python-fastapi`   | Python + FastAPI             |
| `python-django`    | Python + Django              |
| `react-vite`       | React + Vite + TypeScript    |
| `reports-latex-md` | Informes MD/LaTeX → PDF/DOCX |
