# Reglas de dominio — {{PROJECT_NAME}}

> Reglas de negocio transversales que el agente debe verificar en specs y PRs.
> Ubicacion en el proyecto: `.github/docs/business/domain-rules.md`
> **No** incluir estas reglas en perfiles del kit — son propias de cada proyecto.

**Instrucciones:** Completar las secciones que apliquen. Borrar las que no. Si una seccion queda con placeholders (`_ej._`, `_..._`), el agente la trata como **no documentada**.

---

## Contexto

_Breve descripcion del dominio de negocio (sector, usuarios, restricciones legales u operativas)._

---

## Roles y autorizacion

| Rol            | Permisos principales |
| -------------- | -------------------- |
| _ej. admin_    | _..._                |
| _ej. operador_ | _..._                |

**Reglas:**

- _ej. Toda consulta de datos debe filtrar por organizacion del usuario autenticado._
- _ej. Acciones destructivas requieren rol admin._

---

## Entidades y periodos activos

| Concepto             | Regla                                                                                          |
| -------------------- | ---------------------------------------------------------------------------------------------- |
| _ej. Periodo fiscal_ | _La logica pivota en `session('active_year')`; validar ramas para anos anteriores y actuales._ |
| _ej. Tenant_         | _Filtrar por `organization_id` del usuario — sin consultas globales sin filtro._               |

---

## Reglas transversales para specs y PRs

Completar solo las que apliquen. Borrar secciones vacias.

### Autorizacion

- [ ] _Regla verificable en cada cambio visible_

### Filtrado de datos

- [ ] _Regla verificable_

### UI administrativa

- [ ] _ej. Cambios visibles en panel admin probados en ruta `/admin`_

### Cache e invalidacion

- [ ] _ej. Si cambia configuracion de rutas dinamicas, documentar invalidacion de cache_

---

## Glosario minimo

| Termino | Definicion |
| ------- | ---------- |
|         |            |

---

## Sesion guiada (para el agente)

Preguntas que el agente puede hacer al humano para completar este documento:

1. **Proposito:** Que problema resuelve el sistema y quienes lo usan?
2. **Roles:** Cuantos tipos de usuario hay? Que puede hacer cada uno?
3. **Datos:** Hay datos que deben filtrarse por organizacion, sucursal o tenant?
4. **Periodos:** Existe un periodo activo (ano, temporada) que cambie la logica?
5. **Invariantes:** Que reglas nunca pueden violarse (ej. saldos negativos, fechas futuras)?
6. **Aprobaciones:** Que acciones requieren rol especial o confirmacion?
7. **Terminos:** Hay palabras del dominio que deban definirse en el glosario?

Tras las respuestas, el agente redacta las secciones anteriores y pide aprobacion humana.

---

## Ejemplo completado (referencia — no copiar literal)

Sistema de inventario para bodega central con 3 sucursales.

### Contexto

Gestion de stock de productos no perecederos. Usuarios internos de bodega y sucursales.

### Roles y autorizacion

| Rol          | Permisos principales                            |
| ------------ | ----------------------------------------------- |
| admin_bodega | CRUD productos, ajustes de stock, ver auditoria |
| operador     | Registrar entradas/salidas, consultar stock     |
| auditor      | Solo lectura, exportar reportes                 |

**Reglas:**

- Toda consulta de stock filtra por `warehouse_id` del usuario (salvo admin_bodega que ve todas).
- Ajustes manuales de stock requieren rol `admin_bodega` y motivo obligatorio.

### Entidades y periodos activos

| Concepto       | Regla                                                  |
| -------------- | ------------------------------------------------------ |
| Stock          | Nunca negativo; validar en modelo y endpoint           |
| Periodo fiscal | Al cierre (31-dic) se congela el periodo; solo lectura |

### Reglas transversales

### Autorizacion

- [ ] Endpoints de escritura verifican rol segun tabla de roles

### Filtrado de datos

- [ ] Listados de stock filtran por `warehouse_id` del usuario autenticado

### Glosario minimo

| Termino    | Definicion                               |
| ---------- | ---------------------------------------- |
| Movimiento | Entrada o salida de unidades de producto |
| Ajuste     | Correccion manual de stock con motivo    |

---

## Referencias

- Contexto general: [`README.md`](README.md)
- Metodologia: `.github/docs/sdd/workflow.md`
- Formalizacion: `.github/docs/sdd/adoption-guide.md` (seccion "Formalizar el contexto de negocio")
