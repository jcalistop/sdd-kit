### Despliegue (Python + Django)

Producción según plataforma del proyecto (Docker, PaaS o servidor).

- [ ] CI GitHub en verde para el commit de `main` de esta versión
- [ ] Variables de entorno nuevas cargadas en el entorno de producción
- [ ] Backup de BD si hubo `db-change`
- [ ] Migraciones aplicadas (`python manage.py migrate`)
- [ ] `collectstatic` ejecutado si hubo cambios en static
- [ ] Comandos one-off / management commands documentados
- [ ] Imagen Docker reconstruida y desplegada si aplica

### Validación post-despliegue

- [ ] Sitio y login admin en verde
- [ ] Rutas críticas y permisos probados
- [ ] Logs del entorno sin errores nuevos
