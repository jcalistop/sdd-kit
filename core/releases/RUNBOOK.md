# Release runbook

> Traza operativa desde cierre SDD en repo hasta verificación en producción.
> **Despliegue concreto:** `profiles/<stack>/deploy.md` según `sdd.config.yaml`.

---

## Roles (orientativo)

| Rol            | Responsabilidad                         |
| -------------- | --------------------------------------- |
| Implementación | Código, tests, spec en Validating, PR   |
| Revisión       | DoD, riesgos                            |
| Release owner  | Merge, tag, notas de versión            |
| Operaciones    | Deploy, smoke, migraciones según perfil |

---

## Fase 0 — Cierre en rama de desarrollo

1. Acordar versión SemVer `vX.Y.Z`.
2. Crear `releases/vX.Y.Z/` (notas, checklist registro, PR de campaña de referencia).
3. Cada iniciativa cumple DoD: spec archivado, BACKLOG _Released_, entrada en release.
4. Cambios sin spec: ID `—` en nota de release.

**Checklist obligatorio antes del PR de campaña:**

- [ ] Specs en `archive/<YYYY>/<dominio>/` con `Estado: Released`
- [ ] BACKLOG → _Released_
- [ ] `releases/vX.Y.Z/` cerrado
- [ ] CI verde en desarrollo

---

## Fase 1 — Integración en desarrollo

PRs habituales con plantilla PR + checklist core + perfil stack. CI verde.

---

## Fase 2 — Promoción a producción

1. PR desarrollo → producción (cierre Fase 0 ya mergeado).
2. Referenciar `releases/vX.Y.Z/release_vX.Y.Z.md`.
3. Merge **merge commit** (no squash).
4. Sin commits posteriores en producción.

---

## Fase 3 — Tag

```bash
git fetch origin
git checkout main
git pull origin main
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

---

## Fase 3b — Sync producción → desarrollo

```bash
git fetch origin
git checkout dev
git pull origin dev
git merge --ff-only origin/main
git push origin dev
```

Verificar paridad de tips entre ramas.

---

## Fase 4 — Despliegue

Ejecutar según **`profiles/<stack>/deploy.md`**. Típicamente: pipeline automático al merge en producción, variables de entorno, migraciones documentadas en la nota de release.

---

## Fase 5 — Verificación

1. Pipeline de deploy en verde.
2. Smoke según nota de release y perfil stack.
3. Logs sin errores nuevos.
4. Comunicación: enlace a release, tag y deployment.

---

## Checklist rápido

| #   | Paso                                         |
| --- | -------------------------------------------- |
| 1   | Cierre en dev: archive, BACKLOG, release, CI |
| 2   | PR dev → prod + CI                           |
| 3   | Merge (merge commit)                         |
| 4   | Tag `vX.Y.Z`                                 |
| 5   | Sync prod → dev (ff-only)                    |
| 6   | Deploy (perfil stack)                        |
| 7   | Smoke + comunicación                         |
