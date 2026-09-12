# Checklist de PR — Laravel + Voyager + Livewire (stack)

> Complementa [`../../core/checklist-pr.md`](../../core/checklist-pr.md) o el checklist unificado de la instancia. Marcar en cada PR.

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
- [ ] Sin `dd()`, `dump()`, `var_dump()`, `ray()`, `console.log()` en código entregado
- [ ] CI GitHub en verde (`.github/workflows/ci.yml`)

---

## Reglas de negocio del proyecto _(si aplica)_

> Definidas en `.github/docs/business/domain-rules.md`. Marcar ítems relevantes o **No aplica**.

- [ ] Autorización por roles verificada según `domain-rules.md` _(o No aplica)_
- [ ] Filtros de datos (tenant, organización, periodo) verificados _(o No aplica)_
- [ ] Reglas transversales del dominio cumplidas _(o No aplica)_

---

## Voyager y Livewire _(si aplica)_

- [ ] BREAD / formfields Voyager probados en `/admin` _(o No aplica)_
- [ ] Componentes Livewire: validación y autorización en acciones; `wire:key` en listas _(o No aplica)_
- [ ] Validación inline en controllers Voyager o `#[Validate]` en Livewire _(convención del proyecto)_

---

## Rutas y caché _(si aplica)_

- [ ] Rutas dinámicas o configuración en `routes/web.php` probadas en navegador _(o No aplica)_
- [ ] Plan de invalidación de caché documentado si el cambio lo requiere _(o No aplica)_

---

## Cambio de base de datos _(si aplica)_

- [ ] Migración en `database/migrations/` _(sin DDL manual fuera de migraciones salvo excepción documentada)_
- [ ] No ejecutar `migrate:fresh` / `db:wipe` contra BD de desarrollo sin autorización explícita
- [ ] Validación post-migración: estructura, smoke, datos coherentes
- [ ] Rollback documentado o descartado con justificación

---

## API / jobs _(si aplica)_

- [ ] Endpoints: auth, validación, errores acordes al contrato _(o No aplica)_
- [ ] Jobs / comandos Artisan: idempotencia y fallos documentados _(o No aplica)_

---

## Post-deploy _(si cierra release)_

- [ ] `php artisan optimize:clear` o limpieza de caché documentada si aplica
- [ ] Smoke según [`deploy.md`](deploy.md)
