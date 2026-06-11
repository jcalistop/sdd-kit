# Checklist de PR — Python + FastAPI (stack)

> Complementa [`../../core/checklist-pr.md`](../../core/checklist-pr.md). Marcar en cada PR junto con el checklist core.

---

## Calidad técnica

- [ ] `pytest --cov` sin errores _(local y CI)_
- [ ] `ruff check .` sin errores
- [ ] `mypy .` sin errores _(o No aplica si el proyecto aún no usa mypy)_
- [ ] Sin `print()`, `breakpoint()`, `pdb` ni logs de depuración en código entregado
- [ ] CI GitHub en verde (`.github/workflows/ci.yml`)

---

## API REST _(si aplica)_

- [ ] Endpoints documentados en OpenAPI (`/docs` o schema exportado)
- [ ] Validación con Pydantic en request/response
- [ ] Códigos HTTP y mensajes de error coherentes (4xx/5xx)
- [ ] Auth/autorización verificada en rutas protegidas _(o No aplica)_
- [ ] Tests de integración para endpoints tocados _(o No aplica)_

---

## Reglas de negocio del proyecto _(si aplica)_

> Definidas en `.github/docs/business/domain-rules.md`.

- [ ] Reglas transversales del dominio cumplidas _(o No aplica)_

---

## Cambio de base de datos _(si aplica)_

- [ ] Migración Alembic en `alembic/versions/` _(sin DDL manual fuera de migraciones)_
- [ ] `alembic upgrade head` probado en entorno de desarrollo
- [ ] Rollback documentado (`alembic downgrade`) o descartado con justificación
- [ ] Seeders o scripts de datos referenciados en spec/release si aplica

---

## Background tasks / workers _(si aplica)_

- [ ] Celery/RQ/BackgroundTasks: idempotencia y manejo de fallos documentados _(o No aplica)_
- [ ] Variables de entorno nuevas en `.env.example` _(o No aplica)_

---

## Post-deploy _(si cierra release)_

- [ ] Smoke según [`deploy.md`](deploy.md)
- [ ] Health check (`/health` o equivalente) en verde
