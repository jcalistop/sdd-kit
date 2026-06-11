# Despliegue — React + Vite (hosting estático)

Perfil de deploy para SPAs en **Vercel**, **Netlify**, **Cloudflare Pages**, **S3+CloudFront** o servidor nginx.

## Principio

El merge a `main` dispara build y deploy automático si el proyecto tiene CI/CD con el PaaS. El artefacto es la carpeta `dist/`.

| Capa   | Dónde          | Qué valida                                      |
| ------ | -------------- | ----------------------------------------------- |
| CI     | GitHub Actions | vitest, eslint, tsc, build                      |
| Deploy | PaaS / CDN     | Build `dist/`, variables `VITE_*`, SPA fallback |

## Pasos (Fase 4 del runbook)

1. Revisar `releases/vX.Y.Z/release_vX.Y.Z.md` (variables, feature flags, breaking UI).
2. Confirmar CI en verde para el commit de deploy.
3. **Variables:** `VITE_*` en panel del hosting, no en repo con secretos.
4. **Build:** verificar que `npm run build` pasó en CI.
5. **SPA routing:** rewrite a `index.html` para rutas cliente si aplica.

## Configuración SPA (ejemplo)

**Vercel / Netlify:** redirect `/*` → `/index.html` (200) para React Router.

## Smoke post-deploy

- [ ] Página de inicio carga sin error en consola
- [ ] Rutas principales de la versión navegables (refresh directo incluido)
- [ ] Login / flujos autenticados si aplica
- [ ] Formularios y llamadas API de la versión
- [ ] Reglas de `business/domain-rules.md` verificadas si aplica

## Rollback

- Revertir deploy al release anterior en el panel del PaaS o redeploy de tag previo
