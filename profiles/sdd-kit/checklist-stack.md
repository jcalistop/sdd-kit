# Checklist de PR — SDD Kit (mantenedores)

> Complementa [`../../core/checklist-pr.md`](../../core/checklist-pr.md). Marcar en cada PR junto con el checklist core.

---

## Calidad técnica

- [ ] `python -m compileall -q cli/` sin errores
- [ ] `bootstrap/agent-prompts/manifest.json` y `stack-descriptions.json` válidos (JSON)
- [ ] Si se tocó `bootstrap/agent-prompts/`: ejecutado `python bootstrap/sync-cursor-rules.py`
- [ ] CI GitHub en verde (`.github/workflows/ci.yml`)
- [ ] `validate-sdd` en verde sobre `.github/docs/sdd/` si se modificó BACKLOG, specs o config

---

## Core y perfiles

- [ ] Cambios en `core/` sin referencias a stacks concretos _(o No aplica)_
- [ ] Nuevo o modificado perfil: archivos obligatorios según [profile-template.md](../../core/templates/profile-template.md) _(o No aplica)_
- [ ] Perfil sin reglas de negocio de proyectos consumidores _(o No aplica)_
- [ ] Spec de ejemplo actualizado o añadido si el perfil cambia contrato de calidad _(o No aplica)_

---

## Bootstrap y agentes

- [ ] Cambios en prompts: fuente en `bootstrap/agent-prompts/` (no editar solo `.mdc` sin sync)
- [ ] `install-agents.py` probado si cambia contrato de adaptadores _(o No aplica)_
- [ ] Entrada en `stack-descriptions.json` si es perfil nuevo _(o No aplica)_

---

## CLI

- [ ] Comandos nuevos documentados en [cli/README.md](../../cli/README.md) _(o No aplica)_
- [ ] Sin dependencias Python externas nuevas sin justificación _(o No aplica)_

---

## Reglas del producto kit

> [`../../.github/docs/business/domain-rules.md`](../../.github/docs/business/domain-rules.md)

- [ ] Invariantes de arquitectura respetadas (core agnóstico, perfiles autocontenidos)
- [ ] Spec en BACKLOG con estado coherente si el cambio no es trivial _(o No aplica — ID `—`)_

---

## Post-release _(si cierra versión del kit)_

- [ ] Smoke según [`deploy.md`](deploy.md)
- [ ] Nota en `docs/releases/vX.Y.Z.md` y CHANGELOG si aplica
