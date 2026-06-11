# SDD-001 — CRUD de productos en admin Django

> **Spec de ejemplo** para el perfil `python-django`. Referencia de nivel de detalle esperado.

---

## Cabecera

| Campo                 | Valor                   |
| --------------------- | ----------------------- |
| **ID**                | `SDD-001`               |
| **Dominio**           | `admin`                 |
| **Tipo**              | `feature` + `db-change` |
| **Fecha**             | 2026-06-11              |
| **Estado**            | `Draft`                 |
| **Versión objetivo**  | v0.1.0                  |
| **Owner**             | equipo                  |
| **Prioridad**         | `P1`                    |
| **ADRs relacionados** | —                       |
| **Dependencias**      | —                       |

---

## Problema y objetivo

**Problema:**

No hay forma de gestionar el catálogo de productos desde el panel administrativo. Los datos se mantienen en planillas externas.

**Objetivo:**

Registrar el modelo `Product` y exponer CRUD completo en Django Admin con listado, filtros y búsqueda. Sin API pública ni vistas de usuario final en esta versión.

---

## Alcance

**Incluye:**

- App `apps/catalog/` con modelo `Product`
- `ProductAdmin` con `list_display`, `search_fields`, `list_filter`
- Migración inicial `0001_initial.py`
- Tests de modelo y admin (crear, listar, permisos staff)
- Permiso: solo usuarios `is_staff` acceden al admin de productos

**Excluye explícitamente:**

- API REST (DRF) — spec futuro
- Vistas públicas o templates de catálogo
- Importación masiva CSV
- Celery o tareas en background

---

## Impacto técnico

| Pregunta                | Respuesta                                                 |
| ----------------------- | --------------------------------------------------------- |
| Apps Django             | `apps/catalog/` (nueva)                                   |
| Modelos                 | `Product`: name, price, is_active, created_at, updated_at |
| Vistas/templates        | No aplica — solo admin                                    |
| Admin                   | `ProductAdmin` registrado                                 |
| `db-change`             | Sí — `apps/catalog/migrations/0001_initial.py`            |
| DRF                     | No aplica                                                 |
| Auth                    | Staff requerido para `/admin/catalog/product/`            |
| Celery/signals/commands | No aplica                                                 |
| Variables de entorno    | No aplica                                                 |
| `domain-rules.md`       | No aplica                                                 |
| ADR                     | No                                                        |

---

## Reglas de negocio

- `name` obligatorio, único (case-insensitive).
- `price` >= 0, máximo 2 decimales.
- Solo productos con `is_active=True` visibles en listado por defecto del admin (filtro aplicado).

---

## Criterios de aceptación

**Happy path:**

- [ ] Staff crea producto desde admin → guardado y visible en changelist
- [ ] Búsqueda por `name` encuentra el producto
- [ ] Filtro por `is_active` funciona
- [ ] Staff edita y elimina producto sin error

**Error path:**

- [ ] Usuario no staff no accede al admin de productos (403 o redirect login)
- [ ] `price` negativo rechazado en validación de modelo o formulario admin
- [ ] `name` duplicado rechazado con mensaje claro

---

## Cambio de BD

| Objeto            | Tipo         | Detalle                                            |
| ----------------- | ------------ | -------------------------------------------------- |
| `catalog_product` | CREATE TABLE | id, name, price, is_active, created_at, updated_at |

**Rollback:** `python manage.py migrate catalog zero`

---

## Diseño técnico

| Archivo                                   | Cambio                                       |
| ----------------------------------------- | -------------------------------------------- |
| `apps/catalog/models.py`                  | Modelo `Product`                             |
| `apps/catalog/admin.py`                   | `ProductAdmin`                               |
| `apps/catalog/apps.py`                    | Config de app                                |
| `config/settings.py`                      | Registrar `apps.catalog` en `INSTALLED_APPS` |
| `apps/catalog/migrations/0001_initial.py` | Migración inicial                            |
| `tests/catalog/test_models.py`            | Tests de modelo                              |
| `tests/catalog/test_admin.py`             | Tests de admin con `Client`                  |

---

## Verificación técnica

```bash
pytest --cov tests/catalog/
ruff check .
python manage.py check
```

---

## Riesgos y rollback

| Riesgo                        | Probabilidad | Impacto | Mitigación                                  |
| ----------------------------- | ------------ | ------- | ------------------------------------------- |
| App no registrada en settings | Media        | Alto    | Checklist PR + `manage.py check`            |
| Migración falla en deploy     | Baja         | Alto    | Backup + `migrate catalog zero` documentado |

**Rollback:** Revertir PR; `python manage.py migrate catalog zero` si migración ya aplicada.

---

## Notas post-implementación

- _(Completar al cerrar.)_
