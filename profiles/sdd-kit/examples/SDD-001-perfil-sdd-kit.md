# SDD-001 — Perfil sdd-kit para mantenedores

> **Spec de ejemplo** para el perfil `sdd-kit`. Referencia de nivel de detalle esperado al mantener el repositorio del kit.
> Spec de instancia (Released): `.github/docs/sdd/archive/2026/profiles/SDD-001-perfil-sdd-kit.md`.

---

## Cabecera

| Campo                | Valor      |
| -------------------- | ---------- |
| **ID**               | `SDD-001`  |
| **Dominio**          | `profiles` |
| **Tipo**             | `feature`  |
| **Estado**           | `Draft`    |
| **Versión objetivo** | v1.1.0     |

---

## Problema y objetivo

**Problema:** La instancia SDD del kit usaba `python-fastapi` como placeholder; no refleja la CI real del repositorio.

**Objetivo:** Perfil `sdd-kit` con checklist y deploy para mantenedores del kit.

---

## Alcance

**Incluye:** `profiles/sdd-kit/`, agent-prompts, `stack.profile: sdd-kit` en instancia.

**Excluye:** Cambios al ciclo SDD core; perfiles de apps consumidoras.

---

## Impacto técnico (resumen)

| Pregunta              | Respuesta                                       |
| --------------------- | ----------------------------------------------- |
| ¿Afecta `bootstrap/`? | Sí — stacks/sdd-kit.md, stack-descriptions.json |
| ¿Afecta `core/`?      | No                                              |
| ¿db-change?           | No aplica                                       |

---

## Criterios de aceptación

- [ ] Perfil completo en `profiles/sdd-kit/`
- [ ] `validate-sdd` y CI en verde
- [ ] README e INSTALL actualizados

---

## Diseño técnico

| Archivo                            | Cambio                   |
| ---------------------------------- | ------------------------ |
| `profiles/sdd-kit/*`               | Nuevo perfil             |
| `.github/docs/sdd/sdd.config.yaml` | `stack.profile: sdd-kit` |

**Verificación:**

```powershell
python -m compileall -q cli/
.\bootstrap\validate-sdd.ps1 -SddPath ".github/docs/sdd"
```
