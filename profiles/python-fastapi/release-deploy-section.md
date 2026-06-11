### Despliegue (Python + FastAPI)

Producción según plataforma del proyecto (Docker, PaaS o servidor).

- [ ] CI GitHub en verde para el commit de `main` de esta versión
- [ ] Variables de entorno nuevas cargadas en el entorno de producción
- [ ] Backup de BD si hubo `db-change`
- [ ] Migraciones Alembic aplicadas (`alembic upgrade head`)
- [ ] Comandos one-off / seeders documentados
- [ ] Imagen Docker reconstruida y desplegada si aplica

### Validación post-despliegue

- [ ] Health check en verde
- [ ] Endpoints críticos y auth probados
- [ ] Logs del entorno sin errores nuevos
