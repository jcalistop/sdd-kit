# Checklist de PR — DoD (trazabilidad y release)

> **DoD común a todos los stacks.** Completar junto con el checklist del perfil: `profiles/<stack>/checklist-stack.md`.
>
> **Flujo:** [`workflow.md`](workflow.md). **Release:** [`releases/RUNBOOK.md`](releases/RUNBOOK.md).

---

## Cómo usar

1. PR contra **rama de desarrollo** (salvo hotfix acordado a producción).
2. Marcar `[x]` solo cuando verificado; si no aplica: **No aplica**.
3. **CI en verde** antes de merge (workflow del perfil stack).
4. Cambio trivial sin spec: registrar en release con ID `—`.

---

## 1. Trazabilidad — Spec / ADR

| Campo                 | Valor                                                                             |
| --------------------- | --------------------------------------------------------------------------------- |
| **Spec(s)**           | `SDD-NNN-slug` — uno o varios; enlaces a `specs/` o `archive/`                    |
| **Dominio**           | según `sdd.config.yaml` → `domains`                                               |
| **Tipo**              | `feature` / `bugfix` / `refactor` / `performance` / `db-change` / `documentation` |
| **Versión objetivo**  | `vX.Y.Z`                                                                          |
| **ADRs relacionados** | enlaces bajo `adr/` _(0..N)_                                                      |

- [ ] Cabecera Spec/ADR completada por cada `SDD-NNN` (o justificación sin spec + registro `—`)
- [ ] Si el PR agrupa varios specs: criterios de aceptación verificados **por cada** ID (ver [`workflow.md`](workflow.md))

---

## 2. Resumen del cambio

- [ ] **2–4 líneas**: qué hace y por qué

---

## 3. Calidad técnica (perfil stack)

- [ ] Completar [`profiles/<stack>/checklist-stack.md`](../profiles/) — sección Calidad técnica

---

## 4. Validación funcional

- [ ] `verify-implementation` completado **antes** de push/PR (evidencia en PR o enlace)
- [ ] Happy path verificado en dev/staging
- [ ] Error path / casos límite verificados
- [ ] Sin regresiones en flujos adyacentes

---

## 5. Release y archivado _(si este PR cierra el ítem)_

- [ ] Entrada en `releases/vX.Y.Z/release_vX.Y.Z.md`
- [ ] Entrada enlaza spec y ADR si aplica
- [ ] Spec movido a `archive/<YYYY>/<dominio>/` con `git mv`
- [ ] BACKLOG: fila en _Released_ con fecha y versión

---

## 6. Evidencia, rollback y deuda

- [ ] Capturas / comandos / salidas relevantes en el PR
- [ ] Plan de rollback descrito
- [ ] Deuda explícita documentada

---

## Referencias

| Tema              | Documento                                           |
| ----------------- | --------------------------------------------------- |
| Estados y BACKLOG | `workflow.md`, `BACKLOG.md`                         |
| Calidad por stack | `profiles/<stack>/checklist-stack.md`               |
| Despliegue        | `profiles/<stack>/deploy.md`, `releases/RUNBOOK.md` |
