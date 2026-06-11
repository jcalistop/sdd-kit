# SDD-001 — API CRUD de productos

> **Spec de ejemplo** para el perfil `python-fastapi`. Referencia de nivel de detalle esperado.

---

## Cabecera

| Campo                 | Valor      |
| --------------------- | ---------- |
| **ID**                | `SDD-001`  |
| **Dominio**           | `api`      |
| **Tipo**              | `feature`  |
| **Fecha**             | 2026-06-11 |
| **Estado**            | `Draft`    |
| **Versión objetivo**  | v0.1.0     |
| **Owner**             | equipo     |
| **Prioridad**         | `P1`       |
| **ADRs relacionados** | —          |
| **Dependencias**      | —          |

---

## Problema y objetivo

**Problema:**

No existe forma programática de gestionar el catálogo de productos. Los consumidores internos dependen de acceso directo a la base de datos.

**Objetivo:**

Exponer endpoints REST para listar, crear, actualizar y eliminar productos con validación, paginación y documentación OpenAPI.

---

## Alcance

**Incluye:**

- `GET /api/v1/products` — listado paginado con filtro por `name` (query opcional)
- `GET /api/v1/products/{id}` — detalle
- `POST /api/v1/products` — creación
- `PUT /api/v1/products/{id}` — actualización completa
- `DELETE /api/v1/products/{id}` — eliminación lógica (`deleted_at`)
- Modelo SQLAlchemy `Product`, schemas Pydantic, router en `app/routers/products.py`
- Tests de integración con `TestClient`

**Excluye explícitamente:**

- Autenticación en esta versión (endpoints públicos en dev; auth en spec futuro)
- Importación masiva CSV
- Caché Redis

---

## Impacto técnico

| Pregunta                      | Respuesta                                          |
| ----------------------------- | -------------------------------------------------- |
| ¿Afecta endpoints REST?       | Sí — `/api/v1/products` (CRUD completo)            |
| ¿Modifica modelos SQLAlchemy? | Sí — nuevo modelo `Product`                        |
| ¿Requiere auth?               | No aplica — v0.1.0 sin auth; documentar en release |
| ¿Incluye `db-change`?         | Sí — migración Alembic `products` table            |
| ¿Background tasks?            | No aplica                                          |
| ¿Breaking change OpenAPI?     | No — API nueva                                     |
| ¿Variables de entorno nuevas? | No aplica                                          |
| ¿Reglas `domain-rules.md`?    | No aplica                                          |
| ¿ADR?                         | No                                                 |

---

## Reglas de negocio

- `name` obligatorio, 1–200 caracteres, único case-insensitive.
- `price` >= 0, máximo 2 decimales.
- Eliminación es lógica; registros con `deleted_at` no aparecen en listados por defecto.

---

## Criterios de aceptación

**Happy path:**

- [ ] `POST` con payload válido → 201 y cuerpo con `id`
- [ ] `GET` listado → 200, paginación `page`/`size`, filtro por `name`
- [ ] `PUT` actualiza campos → 200
- [ ] `DELETE` → 204; registro no visible en listado

**Error path:**

- [ ] `POST` sin `name` → 422 con detalle Pydantic
- [ ] `GET /products/{id}` inexistente → 404
- [ ] `POST` nombre duplicado → 409

---

## Cambio de BD

| Objeto     | Tipo         | Detalle                                             |
| ---------- | ------------ | --------------------------------------------------- |
| `products` | CREATE TABLE | id, name, price, deleted_at, created_at, updated_at |

**Rollback:** `alembic downgrade -1`

---

## Diseño técnico

| Archivo                                   | Cambio            |
| ----------------------------------------- | ----------------- |
| `app/models/product.py`                   | Modelo SQLAlchemy |
| `app/schemas/product.py`                  | Schemas Pydantic  |
| `app/routers/products.py`                 | Router CRUD       |
| `app/main.py`                             | Registrar router  |
| `alembic/versions/xxx_create_products.py` | Migración         |
| `tests/api/test_products.py`              | Tests integración |

---

## Verificación técnica

```bash
pytest --cov tests/api/test_products.py
ruff check .
mypy app/
```

---

## Riesgos y rollback

| Riesgo                    | Probabilidad | Impacto | Mitigación                                           |
| ------------------------- | ------------ | ------- | ---------------------------------------------------- |
| Sin auth en v0.1          | Alta         | Medio   | Documentar; no exponer en prod pública hasta SDD-002 |
| Migración falla en deploy | Baja         | Alto    | Backup + downgrade documentado                       |

**Rollback:** Revertir PR; `alembic downgrade -1` si migración ya aplicada.

---

## Notas post-implementación

- _(Completar al cerrar.)_
