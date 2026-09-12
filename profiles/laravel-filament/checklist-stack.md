# Checklist de PR — Laravel + Filament (stack)

> Complementa [`../../core/checklist-pr.md`](../../core/checklist-pr.md). Marcar en cada PR junto con el checklist core.

---

## Verify — comandos obligatorios

> Gate local antes de open-pr / evidencia de `verify-implementation`. Ejecutar literales; no sustituir por atajos de autofix.

| Gate | Cuándo | Comando |
| ---- | ------ | ------- |
| test | Siempre | `php artisan test --compact` |
| format | Siempre | `vendor/bin/pint --test` _(mismo que CI; `pint --dirty` ≠ evidencia de verify)_ |
| Tests (alcance) | Preferir filtro al alcance del spec si el tooling lo permite; si no, suite del gate | p. ej. `php artisan test --compact --filter=…` o paths del spec |
| Condicional JS | Si el diff tocó `package.json`, lockfile o assets JS del front | `npm audit` |

---

## Calidad técnica

- [ ] `php artisan test --compact` sin errores _(local y CI)_
- [ ] `vendor/bin/pint --test` sin diferencias _(mismo comando que CI; flag `--dirty` solo ≠ evidencia de verify)_
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

## Reglas de negocio _(si aplica)_

> Definidas en `.github/docs/business/domain-rules.md`.

- [ ] Reglas `DR-*` citadas en spec verificadas en flujos tocados _(o No aplica)_
- [ ] Terminología alineada con glosario de `business/glossary.md` _(o No aplica)_

---

## Post-deploy _(si cierra release)_

- [ ] `php artisan optimize:clear` documentado si aplica
- [ ] Smoke Filament según [`deploy.md`](deploy.md)
