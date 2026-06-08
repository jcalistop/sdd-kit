# Política de ramas

> Ramas por defecto: desarrollo `dev`, producción `main`. Ajustar en `sdd.config.yaml` si el proyecto usa otros nombres.

## Reglas base

1. **No push directo** a rama de producción ni de desarrollo. Todo por PR.
2. **Desarrollo diario** → PR hacia rama de desarrollo.
3. **Producción** se alimenta desde desarrollo vía PR de campaña (release).
4. **CI en verde** antes de merge (workflow definido en perfil stack).

Extensiones opcionales (p. ej. rama de dependencias): ver `profiles/<stack>/branching-extensions.md`.

---

## Flujo normal

1. Rama `feature/…`, `bugfix/…` o `maintenance/…`
2. PR → rama de desarrollo
3. CI verde + revisión → merge

---

## Releases

Referencia: [`releases/RUNBOOK.md`](releases/RUNBOOK.md).

### Cierre en desarrollo (antes del PR de campaña)

- Specs en `archive/<YYYY>/<dominio>/` con `Estado: Released`
- BACKLOG actualizado
- `releases/vX.Y.Z/` completo
- CI verde en rama de desarrollo

> **Prohibido:** archivar specs o cerrar BACKLOG en un commit **posterior** al merge en producción.

### Promoción desarrollo → producción

1. Acordar versión SemVer `vX.Y.Z`
2. PR desarrollo → producción con cierre completo ya mergeado
3. Merge con **«Create a merge commit»** (no squash)
4. Tag anotado `vX.Y.Z` — **sin commits adicionales** en producción tras el merge

### Sync producción → desarrollo

Tras el tag, alinear desarrollo con producción (fast-forward):

```bash
git fetch origin
git checkout dev
git pull origin dev
git merge --ff-only origin/main
git push origin dev
```

Verificar: `git rev-parse origin/main` == `git rev-parse origin/dev`.

---

## Hotfix

1. Rama `hotfix/…` desde producción
2. PR → producción
3. Propagar a desarrollo (`main` → `dev` o cherry-pick)

Trazabilidad: spec `bugfix` preferido; alternativa ID `—` en release.

---

## Protección de ramas (sugerida)

- Rama de **producción**: require PR, status checks, restrict pushes
- Rama de **desarrollo**: require PR, status checks
