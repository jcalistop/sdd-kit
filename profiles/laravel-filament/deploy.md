# Despliegue — Laravel Cloud

Perfil de deploy para proyectos Laravel en [Laravel Cloud](https://cloud.laravel.com/).

## Principio

Producción se actualiza **automáticamente** al merge en rama de producción (`main` por defecto).

## Pasos (Fase 4 del runbook)

1. Revisar `releases/vX.Y.Z/release_vX.Y.Z.md` (BD, env vars, comandos one-off).
2. Confirmar pipeline en verde en Laravel Cloud.
3. **Migraciones:** en `database/migrations/`; documentar si Cloud las ejecuta en deploy o paso manual.
4. **Variables:** solo en Cloud (Settings → Environment), no en `.env` versionado.
5. **Backup** antes de releases con `db-change`.

## Smoke post-deploy

- [ ] Login
- [ ] Panel Filament y flujos tocados por la versión
- [ ] Logs del entorno sin errores nuevos
- [ ] Tareas programadas si la versión las modifica

## CLI (opcional)

```bash
cloud deploy:monitor -n
```
