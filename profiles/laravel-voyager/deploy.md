# Despliegue — Laravel intranet (orquestador interno)

Perfil de deploy para proyectos Laravel en servidor **intranet** con CI en GitHub Actions (modelo híbrido).

## Principio

GitHub **no** despliega automáticamente. El merge a `main` habilita el tag/release; operaciones ejecuta deploy en el host.

| Capa   | Dónde             | Qué valida                                          |
| ------ | ----------------- | --------------------------------------------------- |
| CI     | GitHub Actions    | Tests PHP, Pint, audit, build npm condicional       |
| Deploy | Servidor intranet | Backup BD → `git pull` → composer/npm → migraciones |

## Pasos (Fase 4 del runbook)

1. Revisar `releases/vX.Y.Z/release_vX.Y.Z.md` (BD, env vars, comandos one-off).
2. Confirmar CI en verde en GitHub para la rama de deploy.
3. **Migraciones:** `php artisan migrate --force` tras backup (`php artisan db:backup` o procedimiento del orquestador).
4. **Variables:** solo en `.env` del servidor, no en repo.
5. **Backup** obligatorio antes de releases con `db-change`.

## Comandos frecuentes (Artisan)

```bash
php artisan migrate --force
php artisan optimize:clear
php artisan config:cache
php artisan route:cache
```

Adaptar nombres de comandos de deploy al proyecto consumidor si usa orquestador propio (ej. `app:deploy`, `deploy:run`).

## Smoke post-deploy

- [ ] Login
- [ ] Panel Voyager `/admin` y flujos tocados por la versión
- [ ] Componentes Livewire afectados
- [ ] Logs del entorno sin errores nuevos
- [ ] Reglas de `business/domain-rules.md` verificadas en flujos críticos si aplica

## Script `deploy-vX.Y.Z.sh`

Solo si DDL manual, orden no trivial o rollback semi-automático. Caso contrario: orquestador + `migrate --force`.
