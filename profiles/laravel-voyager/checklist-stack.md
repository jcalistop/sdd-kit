# Checklist de PR — Laravel + Voyager + Livewire (stack)

> Complementa [`../../core/checklist-pr.md`](../../core/checklist-pr.md) o el checklist unificado de la instancia. Marcar en cada PR.

---

## Calidad técnica

- [ ] `php artisan test --compact` sin errores _(local y CI)_
- [ ] `vendor/bin/pint --dirty` sin diferencias
- [ ] Sin `dd()`, `dump()`, `var_dump()`, `ray()`, `console.log()` en código entregado
- [ ] CI GitHub en verde (`.github/workflows/ci.yml`)

---

## Dominio de aplicación _(si aplica — proyectos con instrumentos/año activo)_

- [ ] Bifurcación `ano < 2025` / `ano >= 2025` verificada _(o No aplica)_
- [ ] Filtros por `cen_hie_dependency_id` verificados _(o No aplica)_
- [ ] Autorización por roles (`admin` / `parametrizador` / `user` / `visualizador`) verificada _(o No aplica)_
- [ ] Gates `current-add-edit` / `current-download` verificados _(o No aplica)_

---

## Voyager y Livewire _(si aplica)_

- [ ] BREAD / formfields Voyager probados en `/admin` _(o No aplica)_
- [ ] Componentes Livewire: validación y autorización en acciones; `wire:key` en listas _(o No aplica)_
- [ ] Validación inline en controllers Voyager o `#[Validate]` en Livewire _(convención del proyecto)_

---

## IndicatorType / rutas dinámicas _(si aplica)_

- [ ] Plan de invalidación de caché `indicator_type_routes` documentado si cambió `IndicatorType`
- [ ] Rutas dinámicas con `view` o `controller` probadas en navegador

---

## Cambio de base de datos _(si aplica)_

- [ ] Migración en `database/migrations/` _(sin DDL manual fuera de migraciones salvo excepción documentada)_
- [ ] No ejecutar `migrate:fresh` / `db:wipe` contra MySQL de desarrollo sin autorización explícita
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
