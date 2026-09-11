| Gate           | Comando                                   | Cuándo                                        |
| -------------- | ----------------------------------------- | --------------------------------------------- |
| Formato (autofix) | `vendor/bin/pint --dirty --format agent` | Tras editar PHP (tip In Build; ≠ verify)     |
| Formato verify/open-pr | `vendor/bin/pint --test`            | Antes de open-pr / evidencia de verify (mismo que CI) |
| Tests          | `php artisan test --compact`              | Filtrar por archivo/`--filter` cuando aplique |
| Validación SDD | `python {{KIT_PATH}}/cli/sdd.py validate` | Tras cambios en specs/BACKLOG; en verify      |
| CI equivalente | `.github/workflows/ci.yml`                | Debe coincidir con lo ejecutado local         |
