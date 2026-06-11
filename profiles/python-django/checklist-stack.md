# Checklist de PR — Python + Django (stack)

> Complementa [`../../core/checklist-pr.md`](../../core/checklist-pr.md). Marcar en cada PR junto con el checklist core.

---

## Calidad técnica

- [ ] `pytest --cov` sin errores _(local y CI)_
- [ ] `ruff check .` sin errores
- [ ] `mypy .` sin errores _(o No aplica si el proyecto aún no usa mypy)_
- [ ] `python manage.py check` sin errores
- [ ] Sin `print()`, `breakpoint()`, `pdb` ni logs de depuración en código entregado
- [ ] CI GitHub en verde (`.github/workflows/ci.yml`)

---

## Modelos y migraciones _(si aplica)_

- [ ] Migración en `apps/<app>/migrations/` _(sin DDL manual fuera de migraciones)_
- [ ] `python manage.py makemigrations` generó archivos en la app correcta
- [ ] `python manage.py migrate` probado en entorno de desarrollo
- [ ] Rollback documentado (`migrate <app> <migration_anterior>`) o descartado con justificación
- [ ] Seeders o fixtures referenciados en spec/release si aplica

---

## Vistas y templates _(si aplica)_

- [ ] URLs registradas en `urls.py` del proyecto o de la app
- [ ] Templates renderizan sin error en flujos tocados
- [ ] Formularios POST con token CSRF _(o excepción documentada)_
- [ ] Permisos de vista (`LoginRequiredMixin`, `@permission_required`) verificados

---

## Admin Django _(si aplica)_

- [ ] `ModelAdmin` (o recurso equivalente) registrado en `admin.py`
- [ ] `list_display`, filtros y búsqueda coherentes con el spec _(o No aplica)_
- [ ] Permisos de admin verificados (solo roles autorizados)
- [ ] Acciones personalizadas documentadas en spec si aplica

---

## DRF — API REST _(si aplica)_

- [ ] Serializers y viewsets/routers actualizados
- [ ] Permisos y autenticación en endpoints protegidos
- [ ] Paginación y códigos HTTP coherentes (4xx/5xx)
- [ ] Tests con `APIClient` para endpoints tocados

---

## Celery / tasks _(si aplica)_

- [ ] Tareas idempotentes o con manejo de reintentos documentado
- [ ] Signals o management commands referenciados en spec si aplica
- [ ] Variables de entorno nuevas en `.env.example` _(o No aplica)_

---

## Reglas de negocio del proyecto _(si aplica)_

> Definidas en `.github/docs/business/domain-rules.md`.

- [ ] Reglas transversales del dominio cumplidas _(o No aplica)_

---

## Post-deploy _(si cierra release)_

- [ ] Smoke según [`deploy.md`](deploy.md)
- [ ] Login admin y rutas críticas probadas
- [ ] `collectstatic` ejecutado si hubo cambios en static
