# SDD-001 — Capacitacion de usuarios en nuevo sistema de inventario

> Ejemplo de spec con plantilla simple ([`spec-simple-template.md`](../templates/spec-simple-template.md)).
> Pensado para contexto no tecnico: capacitacion, procesos, flujos operativos.

---

## Cabecera

| Campo            | Valor               |
| ---------------- | ------------------- |
| **ID**           | `SDD-001`           |
| **Dominio**      | `capacitacion`      |
| **Tipo**         | `feature`           |
| **Fecha**        | 2026-03-10          |
| **Estado**       | `Released`          |
| **Owner**        | Maria (operaciones) |
| **Prioridad**    | `P1`                |
| **Dependencias** | —                   |

---

## Que quiero lograr

**Problema o necesidad:**

El nuevo sistema de inventario reemplaza las planillas Excel que usaban las 3 sucursales. Nadie fuera del equipo de sistemas sabe usarlo. Si no capacitamos antes del lanzamiento, el primer dia habra caos: pedidos mal ingresados, stock fantasma, llamadas a soporte.

**Resultado esperado:**

Los 12 operadores de sucursal y los 2 auditores saben usar el sistema para sus tareas diarias (registrar entradas/salidas, consultar stock, exportar reportes). El cambio de planilla a sistema ocurre sin interrupcion operativa.

---

## Que incluye y que NO incluye

**Incluye:**

- Crear guia rapida impresa (1 hoja, laminada) con los 4 flujos principales.
- Dictar 3 sesiones presenciales (1 por sucursal, 2 horas cada una).
- Sesion extra para auditores (1 hora, enfocada en reportes y exportacion).
- Grabar video de referencia (max 10 min) para consultas futuras.
- Definir persona de contacto por sucursal para dudas post-lanzamiento.

**NO incluye (explicito):**

- Capacitar al equipo de sistemas (ellos ya conocen el sistema — son quienes lo construyeron).
- Crear manual completo (la guia rapida cubre el 80% de los casos; el resto se resuelve con la persona de contacto).
- Traducir la interfaz (esta en español y el equipo lo confirmo).
- Evaluacion formal con nota (es capacitacion operativa, no academica).

---

## Impacto

| Area afectada   | Como se afecta                                                      |
| --------------- | ------------------------------------------------------------------- |
| Sucursal Norte  | 4 operadores dejan planilla Excel, usan sistema desde el dia D+1    |
| Sucursal Centro | 5 operadores (igual)                                                |
| Sucursal Sur    | 3 operadores (igual)                                                |
| Auditoria       | 2 auditores migran de pedir Excel por correo a exportar del sistema |
| Soporte interno | Recibe consultas post-lanzamiento; derivan a persona de contacto    |

---

## Como se que esta listo (criterios de aceptacion)

- [x] Guia rapida impresa entregada a cada sucursal (verificacion: foto de la guia en cada sucursal)
- [x] 3 sesiones presenciales dictadas (verificacion: lista de asistencia firmada, +80% de operadores)
- [x] Sesion de auditores dictada (verificacion: ambos auditores confirman por correo que saben exportar reportes)
- [x] Video de referencia grabado y compartido (verificacion: enlace en canal interno, visto al menos 1 vez por sucursal)
- [x] Persona de contacto designada por sucursal (verificacion: nombre publicado en canal interno)

---

## Riesgos

| Que puede salir mal                                 | Como lo mitigo                                                       |
| --------------------------------------------------- | -------------------------------------------------------------------- |
| Un operador falta a la sesion                       | Video de referencia + guia impresa + persona de contacto lo cubren   |
| El sistema falla durante la sesion (demo en vivo)   | Tener capturas de pantalla de respaldo por si el sistema no responde |
| Los auditores necesitan mas que 1 hora              | Agendar sesion extra si ellos lo piden; no forzar el tiempo          |
| El video queda desactualizado si cambia la interfaz | La guia impresa es la fuente principal; el video es complemento      |

---

## Notas post-implementacion

- Las 3 sesiones se dictaron entre el 17 y el 21 de marzo. Asistencia: 11/12 operadores. El que falto vio el video y recibio acompañamiento de la persona de contacto el dia 22.
- Los auditores pidieron sesion extra de 30 min — se agendo para el 24 de marzo.
- La guia rapida quedo en la pared de cada sucursal junto al terminal.
- Video subido al canal `#inventario-nuevo-sistema`.
- Contactos designados: Pedro (Norte), Carla (Centro), Luis (Sur).
