# SDD-001 — Login con recuperación de contraseña

> **Spec de ejemplo** para el perfil `laravel-filament`. Referencia de nivel de detalle esperado.
> No copiar literalmente a producción; usar como modelo al crear el primer spec real.

---

## Cabecera

| Campo                 | Valor      |
| --------------------- | ---------- |
| **ID**                | `SDD-001`  |
| **Dominio**           | `auth`     |
| **Tipo**              | `feature`  |
| **Fecha**             | 2026-06-11 |
| **Estado**            | `Draft`    |
| **Versión objetivo**  | v0.2.0     |
| **Owner**             | equipo     |
| **Prioridad**         | `P1`       |
| **ADRs relacionados** | —          |
| **Dependencias**      | —          |

---

## Problema y objetivo

**Problema:**

Los usuarios que olvidan su contraseña deben contactar al administrador manualmente. Esto genera demoras y carga operativa innecesaria.

**Objetivo:**

Permitir que un usuario registrado solicite un enlace de restablecimiento de contraseña por correo electrónico y complete el cambio sin intervención del administrador.

---

## Alcance

**Incluye:**

- Pantalla pública "Olvidé mi contraseña" con campo email
- Envío de enlace firmado con expiración (24 h) vía correo
- Pantalla de restablecimiento con validación de contraseña (mín. 8 caracteres, confirmación)
- Mensajes de error genéricos (no revelar si el email existe)
- Flujo Filament para login existente enlazado a recuperación

**Excluye explícitamente:**

- Autenticación de dos factores (2FA)
- Registro público de nuevos usuarios
- Cambio de contraseña desde perfil de usuario autenticado (spec futuro)

---

## Impacto técnico

| Pregunta                                                   | Respuesta                                                                               |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| ¿Afecta panel Filament (resources, pages, widgets)?        | Sí — página custom `ForgotPassword` y `ResetPassword` fuera del panel o en guest layout |
| ¿Requiere policies, roles o permisos nuevos o modificados? | No aplica — flujo guest, sin cambio de permisos autenticados                            |
| ¿Incluye `db-change`?                                      | No aplica — usa tabla `password_reset_tokens` estándar de Laravel                       |
| ¿Afecta rutas HTTP o API pública?                          | Sí — `GET/POST /forgot-password`, `GET/POST /reset-password/{token}`                    |
| ¿Requiere `php artisan optimize:clear` al deploy?          | No aplica — solo rutas nuevas, sin cambio de config cacheada                            |
| ¿Introduce dependencia externa nueva?                      | No aplica — mail driver ya configurado en el proyecto                                   |
| ¿Introduce decisión arquitectónica transversal?            | No                                                                                      |

---

## Reglas de negocio

- Solo usuarios con `email_verified_at` no nulo pueden solicitar reset (o permitir todos — acordar con humano; aquí: todos los emails registrados).
- Máximo 3 solicitudes de reset por email por hora (rate limit).
- El enlace expira a las 24 horas; token de un solo uso.
- Respuesta HTTP idéntica si el email existe o no ("Si el correo está registrado, recibirás instrucciones").

---

## Criterios de aceptación

**Happy path:**

- [ ] Usuario ingresa email válido registrado → recibe correo con enlace en menos de 2 minutos (entorno dev: log/mailhog)
- [ ] Usuario abre enlace válido → puede ingresar nueva contraseña y confirmación → redirige a login con mensaje de éxito
- [ ] Usuario inicia sesión con la nueva contraseña

**Error path:**

- [ ] Email no registrado → mismo mensaje genérico que email válido (sin filtración)
- [ ] Enlace expirado o ya usado → mensaje claro y opción de solicitar nuevo enlace
- [ ] Contraseña débil o sin confirmación → errores de validación en formulario, sin envío

---

## Diseño técnico

**Archivos principales:**

| Archivo                                                  | Cambio                   |
| -------------------------------------------------------- | ------------------------ |
| `routes/web.php`                                         | Rutas guest forgot/reset |
| `app/Http/Controllers/Auth/ForgotPasswordController.php` | Solicitud de enlace      |
| `app/Http/Controllers/Auth/ResetPasswordController.php`  | Restablecimiento         |
| `resources/views/auth/forgot-password.blade.php`         | Vista solicitud          |
| `resources/views/auth/reset-password.blade.php`          | Vista reset              |
| `tests/Feature/Auth/PasswordResetTest.php`               | Tests happy + error path |

---

## Verificación técnica

```bash
php artisan test --compact --filter=PasswordReset
vendor/bin/pint --dirty
```

---

## Riesgos y rollback

| Riesgo                            | Probabilidad | Impacto | Mitigación                                       |
| --------------------------------- | ------------ | ------- | ------------------------------------------------ |
| Mail no configurado en producción | Media        | Alto    | Verificar `MAIL_*` en release; smoke post-deploy |
| Rate limit insuficiente           | Baja         | Medio   | Throttle en rutas + test de límite               |
| Filtración de emails existentes   | Baja         | Alto    | Mensaje genérico; test explícito                 |

**Rollback:** Revertir PR; rutas dejan de estar registradas. Tokens en BD pueden limpiarse con `php artisan auth:clear-resets` si aplica.

---

## Notas post-implementación

- _(Completar al cerrar el spec.)_
