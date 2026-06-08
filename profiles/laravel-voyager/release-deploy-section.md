### Despliegue (intranet — orquestador interno)

Producción se actualiza **manualmente** en servidor intranet tras tag en `main`. GitHub no despliega solo.

- [ ] CI GitHub en verde para el commit de `main` de esta versión
- [ ] Variables de entorno nuevas cargadas en servidor
- [ ] Backup de BD si hubo `db-change`
- [ ] Migraciones en `database/migrations/`; `php artisan migrate --force` tras backup
- [ ] Comandos one-off / seeders documentados
- [ ] `php artisan optimize:clear` o limpieza de caché si aplica

### Validación post-despliegue

- [ ] Smoke: login, Voyager `/admin`, Livewire, flujos de la versión
- [ ] Logs del entorno sin errores nuevos
- [ ] Versión desplegada visible en app si aplica
