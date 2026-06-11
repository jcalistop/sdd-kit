# Despliegue — Python + Django

Perfil de deploy para aplicaciones Django en **Docker**, **PaaS** (Railway, Render, Fly.io) o servidor propio.

## Principio

El merge a rama de producción (`main` por defecto) dispara deploy automático **si** el proyecto tiene CI/CD configurado. En deploy manual, seguir los pasos de este documento.

| Capa   | Dónde           | Qué valida                                          |
| ------ | --------------- | --------------------------------------------------- |
| CI     | GitHub Actions  | pytest, ruff, mypy, `manage.py check`, build imagen |
| Deploy | PaaS / servidor | Migraciones, collectstatic, variables, smoke        |

## Pasos (Fase 4 del runbook)

1. Revisar `releases/vX.Y.Z/release_vX.Y.Z.md` (BD, env vars, comandos one-off).
2. Confirmar CI en verde en GitHub para el commit de deploy.
3. **Migraciones:** `python manage.py migrate` tras backup si hubo `db-change`.
4. **Static:** `python manage.py collectstatic --noinput` si hubo cambios en assets.
5. **Variables:** solo en panel PaaS o `.env` del servidor, no en repo.
6. **Backup** obligatorio antes de releases con `db-change`.

## Comandos frecuentes

```bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 0.0.0.0:8000
# ASGI (Channels, etc.):
# uvicorn config.asgi:application --host 0.0.0.0 --port 8000
```

Con Docker:

```bash
docker compose pull
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
```

## Smoke post-deploy

- [ ] Sitio responde 200 en ruta principal
- [ ] Login admin (`/admin/`) funciona con usuario de prueba
- [ ] Rutas críticas de la versión probadas (auth + flujos tocados)
- [ ] `DEBUG=False` en producción
- [ ] Logs sin errores nuevos
- [ ] Reglas de `business/domain-rules.md` verificadas si aplica

## Rollback

- Revertir imagen/commit anterior en PaaS o `docker compose` a tag previo
- Si hubo migración: evaluar `python manage.py migrate <app> <migration_anterior>` según plan del release
