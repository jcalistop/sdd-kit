# Despliegue — Python + FastAPI

Perfil de deploy para APIs FastAPI en **Docker**, **PaaS** (Railway, Render, Fly.io) o servidor propio.

## Principio

El merge a rama de producción (`main` por defecto) dispara deploy automático **si** el proyecto tiene CI/CD configurado. En deploy manual, seguir los pasos de este documento.

| Capa   | Dónde           | Qué valida                           |
| ------ | --------------- | ------------------------------------ |
| CI     | GitHub Actions  | pytest, ruff, mypy, build imagen     |
| Deploy | PaaS / servidor | Migraciones, variables, health check |

## Pasos (Fase 4 del runbook)

1. Revisar `releases/vX.Y.Z/release_vX.Y.Z.md` (BD, env vars, comandos one-off).
2. Confirmar CI en verde en GitHub para el commit de deploy.
3. **Migraciones:** `alembic upgrade head` tras backup si hubo `db-change`.
4. **Variables:** solo en panel PaaS o `.env` del servidor, no en repo.
5. **Backup** obligatorio antes de releases con `db-change`.

## Comandos frecuentes

```bash
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000   # o gunicorn + uvicorn workers
```

Con Docker:

```bash
docker compose pull
docker compose up -d --build
docker compose exec api alembic upgrade head
```

## Smoke post-deploy

- [ ] `GET /health` (o endpoint equivalente) responde 200
- [ ] OpenAPI `/docs` accesible si aplica en producción
- [ ] Endpoints críticos de la versión probados (auth + flujos tocados)
- [ ] Logs sin errores nuevos
- [ ] Reglas de `business/domain-rules.md` verificadas si aplica

## Rollback

- Revertir imagen/commit anterior en PaaS o `docker compose` a tag previo
- Si hubo migración: evaluar `alembic downgrade -1` según plan del release
