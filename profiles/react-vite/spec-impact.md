# Impacto técnico — React + Vite

> Sección obligatoria en todo spec. Copiar al crear `SDD-NNN` o referenciar desde la plantilla de la instancia.
> Reglas de negocio específicas: `.github/docs/business/domain-rules.md`.

## Impacto técnico _(obligatorio)_

Responder cada ítem. Si no aplica: "No aplica — [razón]".

| Pregunta                                                            | Respuesta |
| ------------------------------------------------------------------- | --------- |
| ¿Afecta rutas (`src/routes/`, React Router)? ¿Cuáles?               |           |
| ¿Afecta componentes en `src/components/` o páginas en `src/pages/`? |           |
| ¿Modifica estado global (Context, Zustand, Redux, TanStack Query)?  |           |
| ¿Integra con API backend? Endpoints y contratos                     |           |
| ¿Requiere variables `VITE_*` nuevas? Listar claves (sin valores).   |           |
| ¿Afecta autenticación (token, sesión, rutas protegidas)?            |           |
| ¿Impacta accesibilidad (a11y) o i18n?                               |           |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles. |           |
| ¿Introduce decisión arquitectónica transversal? Si sí → ADR.        |           |

## Regla de build

- Build de producción: `npm run build` → `dist/`
- No commitear `dist/` salvo política explícita del proyecto
- Preview local: `npm run preview` antes de release si hay cambios de routing o assets
