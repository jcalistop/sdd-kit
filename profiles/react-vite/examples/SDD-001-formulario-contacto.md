# SDD-001 — Formulario de contacto

> **Spec de ejemplo** para el perfil `react-vite`. Referencia de nivel de detalle esperado.

---

## Cabecera

| Campo                 | Valor      |
| --------------------- | ---------- |
| **ID**                | `SDD-001`  |
| **Dominio**           | `ux`       |
| **Tipo**              | `feature`  |
| **Fecha**             | 2026-06-11 |
| **Estado**            | `Draft`    |
| **Versión objetivo**  | v0.1.0     |
| **Owner**             | equipo     |
| **Prioridad**         | `P2`       |
| **ADRs relacionados** | —          |
| **Dependencias**      | —          |

---

## Problema y objetivo

**Problema:**

La landing no tiene forma de contacto. Los visitantes deben buscar un correo en el footer.

**Objetivo:**

Agregar página `/contacto` con formulario (nombre, email, mensaje) que envíe datos a la API existente y muestre confirmación o error al usuario.

---

## Alcance

**Incluye:**

- Ruta `/contacto` con layout consistente con el sitio
- Componente `ContactForm` con validación cliente
- Integración `POST /api/v1/contact` (API externa al frontend)
- Estados: idle, loading, success, error
- Tests con Vitest + Testing Library
- Enlace en navegación principal

**Excluye explícitamente:**

- CAPTCHA / anti-spam
- Adjuntos de archivos
- Panel admin para leer mensajes

---

## Impacto técnico

| Pregunta             | Respuesta                                                         |
| -------------------- | ----------------------------------------------------------------- |
| ¿Afecta rutas?       | Sí — nueva ruta `/contacto` en React Router                       |
| ¿Componentes?        | Sí — `ContactForm`, página `ContactPage`                          |
| ¿Estado global?      | No aplica — estado local del formulario                           |
| ¿API backend?        | Sí — `POST /api/v1/contact`                                       |
| ¿Variables `VITE_*`? | Sí — `VITE_API_BASE_URL` (ya existe; verificar)                   |
| ¿Auth?               | No aplica — formulario público                                    |
| ¿a11y?               | Sí — labels, errores asociados a campos, foco en mensaje de éxito |
| ¿domain-rules.md?    | No aplica                                                         |
| ¿ADR?                | No                                                                |

---

## Reglas de negocio

- `nombre`: 2–100 caracteres.
- `email`: formato válido.
- `mensaje`: 10–2000 caracteres.
- Tras éxito, limpiar formulario y mostrar mensaje de confirmación.

---

## Criterios de aceptación

**Happy path:**

- [ ] Usuario completa campos válidos → submit → spinner → mensaje de éxito
- [ ] Enlace "Contacto" visible en nav y lleva a `/contacto`
- [ ] Refresh en `/contacto` carga la página (SPA fallback)

**Error path:**

- [ ] Campo vacío → mensaje de validación junto al campo
- [ ] API responde 500 → mensaje de error genérico, formulario conserva datos
- [ ] Email inválido → error antes de submit

---

## Diseño técnico

| Archivo                               | Cambio           |
| ------------------------------------- | ---------------- |
| `src/pages/ContactPage.tsx`           | Página           |
| `src/components/ContactForm.tsx`      | Formulario       |
| `src/routes/index.tsx`                | Ruta `/contacto` |
| `src/api/contact.ts`                  | Cliente POST     |
| `src/components/ContactForm.test.tsx` | Tests            |
| `src/components/layout/Nav.tsx`       | Enlace nav       |

---

## Verificación técnica

```bash
vitest run src/components/ContactForm.test.tsx
eslint .
prettier --check .
tsc --noEmit
npm run build
```

---

## Riesgos y rollback

| Riesgo             | Probabilidad | Impacto | Mitigación                           |
| ------------------ | ------------ | ------- | ------------------------------------ |
| CORS en API        | Media        | Alto    | Verificar con backend antes de merge |
| SPA 404 en refresh | Media        | Medio   | Verificar rewrite en hosting         |

**Rollback:** Revertir PR; quitar ruta y enlace nav.

---

## Notas post-implementación

- _(Completar al cerrar.)_
