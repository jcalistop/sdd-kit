| Gate           | Comando                                   | Cuándo                                        |
| -------------- | ----------------------------------------- | --------------------------------------------- |
| Formato        | `vendor/bin/pint --dirty --format agent`  | Tras editar PHP                               |
| Tests          | `php artisan test --compact`              | Filtrar por archivo/`--filter` cuando aplique |
| Validación SDD | `python {{KIT_PATH}}/cli/sdd.py validate` | Tras cambios en specs/BACKLOG; en verify      |
| CI equivalente | `.github/workflows/ci.yml`                | Debe coincidir con lo ejecutado local         |
