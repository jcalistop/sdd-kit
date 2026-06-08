### Despliegue (Laravel Cloud)

Producción se actualiza automáticamente al mergear en `main`.

- [ ] Variables de entorno nuevas cargadas en Laravel Cloud
- [ ] Backup de BD si hubo `db-change`
- [ ] Migraciones en `database/migrations/`; `php artisan migrate --force` según política del entorno
- [ ] Comandos one-off / seeders documentados
- [ ] Pipeline en verde para el commit de `main` de esta versión

### Validación post-despliegue

- [ ] Smoke: login, panel Filament, flujos de la versión
- [ ] Logs del entorno sin errores nuevos
