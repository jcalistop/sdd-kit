# Perfil: React + Vite

Extensión del SDD core para SPAs con React 18+, Vite, TypeScript y despliegue estático (Vercel, Netlify, S3+CDN).

| Archivo                                                                            | Uso                                               |
| ---------------------------------------------------------------------------------- | ------------------------------------------------- |
| [checklist-stack.md](checklist-stack.md)                                           | DoD técnico (vitest, eslint, prettier, tsc, a11y) |
| [spec-impact.md](spec-impact.md)                                                   | Tabla "Impacto técnico" para specs                |
| [deploy.md](deploy.md)                                                             | Build estático y PaaS                             |
| [branching-extensions.md](branching-extensions.md)                                 | Rama `deps-integration` + Dependabot (npm)        |
| [release-deploy-section.md](release-deploy-section.md)                             | Bloque para notas de release                      |
| [examples/SDD-001-formulario-contacto.md](examples/SDD-001-formulario-contacto.md) | Spec de ejemplo (referencia de calidad)           |

**Quality gates por defecto:**

- `npm run test` o `vitest run`
- `eslint .`
- `prettier --check .`
- `tsc --noEmit`
- CI: `.github/workflows/ci.yml` en verde
