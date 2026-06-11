# Checklist de PR — React + Vite (stack)

> Complementa [`../../core/checklist-pr.md`](../../core/checklist-pr.md). Marcar en cada PR junto con el checklist core.

---

## Calidad técnica

- [ ] `vitest run` (o `npm run test`) sin errores _(local y CI)_
- [ ] `eslint .` sin errores
- [ ] `prettier --check .` sin diferencias
- [ ] `tsc --noEmit` sin errores
- [ ] Sin `console.log` de depuración en código entregado
- [ ] CI GitHub en verde (`.github/workflows/ci.yml`)

---

## Componentes y rutas _(si aplica)_

- [ ] Componentes nuevos o modificados con tests unitarios _(o justificación si no aplica)_
- [ ] Rutas React Router registradas y probadas en navegador
- [ ] Estados de carga, error y vacío manejados en UI
- [ ] `key` estable en listas renderizadas

---

## Formularios y datos _(si aplica)_

- [ ] Validación de formularios (cliente) y mensajes de error visibles
- [ ] Llamadas API: manejo de errores HTTP y timeouts
- [ ] Tipos TypeScript alineados con contrato API _(o No aplica)_

---

## Accesibilidad y responsive _(si aplica)_

- [ ] Labels asociados a inputs; botones con texto o `aria-label`
- [ ] Navegación por teclado básica en flujos tocados _(o No aplica)_
- [ ] Layout probado en viewport móvil si la UI es pública

---

## Reglas de negocio del proyecto _(si aplica)_

> Definidas en `.github/docs/business/domain-rules.md`.

- [ ] Reglas transversales del dominio cumplidas _(o No aplica)_

---

## Build y assets _(si aplica)_

- [ ] `npm run build` exitoso sin warnings críticos
- [ ] Variables `VITE_*` nuevas documentadas en `.env.example`

---

## Post-deploy _(si cierra release)_

- [ ] Smoke según [`deploy.md`](deploy.md)
- [ ] Rutas SPA / fallback configurado en hosting si aplica
