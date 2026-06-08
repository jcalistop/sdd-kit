# Checklist de PR — Laravel + Filament (stack)

> Complementa [`../../core/checklist-pr.md`](../../core/checklist-pr.md). Marcar en cada PR junto con el checklist core.

---

## Calidad técnica

- [ ] `php artisan test --compact` sin errores _(local y CI)_
- [ ] `vendor/bin/pint --dirty` sin diferencias
- [ ] Sin `dd()`, `dump()`, `var_dump()`, `ray()` en código entregado
- [ ] CI GitHub en verde (`.github/workflows/ci.yml`)

---

## Filament y autorización _(si aplica)_

- [ ] Resources / Pages / widgets probados en panel Filament _(o No aplica)_
- [ ] Policies, roles o permisos verificados _(o No aplica)_
- [ ] Acciones deshabilitadas para usuarios sin permiso _(o No aplica)_

---

## Cambio de base de datos _(si aplica)_

- [ ] Migración en `database/migrations/` _(sin DDL manual fuera de migraciones)_
- [ ] Validación post-migración: estructura, smoke, datos coherentes
- [ ] Rollback documentado o descartado con justificación

---

## API / jobs _(si aplica)_

- [ ] Endpoints: auth, validación, errores acordes al contrato _(o No aplica)_
- [ ] Jobs / comandos Artisan: idempotencia y fallos documentados _(o No aplica)_

---

## Post-deploy _(si cierra release)_

- [ ] `php artisan optimize:clear` documentado si aplica
- [ ] Smoke Filament según [`deploy.md`](deploy.md)
