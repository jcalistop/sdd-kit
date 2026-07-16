# Reglas de dominio — SDD Kit

> Reglas transversales del **producto kit** que el agente debe verificar al crear specs y PRs en este repositorio.
> No confundir con reglas de negocio de proyectos consumidores — esas viven en el `business/` de cada proyecto.

---

## Contexto

El SDD Kit es un producto de **metodología y tooling**, no una aplicación de negocio. Su dominio es: cómo estructurar specs, backlogs, releases y adaptadores de agente para cualquier stack, sin acoplar el core a un framework concreto.

---

## Principios de diseño (invariantes)

Estas reglas **nunca** deben violarse en contribuciones al kit:

| #   | Regla                                                                                                                                                          | Verificación en PR                                                  |
| --- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| 1   | **Core agnóstico al stack** — `core/` no menciona Laravel, React, Python, etc.                                                                                 | Revisar diff en `core/`                                             |
| 2   | **Perfiles autocontenidos** — todo lo específico de un stack vive en `profiles/<nombre>/`                                                                      | Nuevo código de stack solo en perfiles                              |
| 3   | **Sin lógica de negocio de consumidores en perfiles** — roles, tenants o reglas de dominio de un proyecto van en `business/` del consumidor, no en el kit      | Revisar checklist y spec-impact del perfil                          |
| 4   | **El agente ejecuta; el humano aprueba** en Ready (spec) y merge (PR). Estados = progreso; prompts = opcionales. Verify local antes de push/PR                 | Ready antes de codificar; verify antes de PR                        |
| 5   | **Adopción incremental** — no exigir specs retrospectivos al adoptar SDD                                                                                       | adoption-guide y ADOPTION.md                                        |
| 6   | **Documentación SDD solo en `paths.sdd`** — specs, BACKLOG y releases de iniciativas en `.github/docs/sdd/`; planificación histórica en `business/planning/`   | No crear specs en `core/` ni duplicar planning fuera de `business/` |
| 7   | **Separación producto / proceso / versiones** — producto en raíz; proceso en `.github/docs/sdd/`; planning en `business/planning/`; SemVer en `docs/releases/`. Cierre de versión del kit = **dual-release** (nota producto + acta campaña enlazada) | Ver glosario en `docs/README.md` y ADOPTION.md                      |

---

## Arquitectura de capas

```
Kit (producto)     → core/, profiles/, bootstrap/, cli/
Proceso SDD        → .github/docs/sdd/
Contexto producto  → .github/docs/business/ (este directorio)
Planificación      → .github/docs/business/planning/ (análisis, roadmap histórico)
Release producto   → docs/releases/ (SemVer para consumidores; ver docs/README.md)
Release campaña    → .github/docs/sdd/releases/ (acta SDD; debe enlazar nota producto)
```

### Dual-release al cerrar versión del kit

| Artefacto | Ruta | Fuente de verdad |
| --------- | ---- | ---------------- |
| Nota producto | `docs/releases/vX.Y.Z.md` + `CHANGELOG.md` | Qué cambió el kit para consumidores |
| Acta campaña | `.github/docs/sdd/releases/vX.Y.Z/release_*.md` | Specs/gates del cierre SDD |

La acta **debe** enlazar la nota producto. No unificar carpetas. No exigir `docs/releases/` en proyectos consumidores.

---

## Reglas para specs y PRs del kit

### Cambios en core

- [ ] Sin referencias a stacks concretos salvo enlaces genéricos a `profiles/`
- [ ] Plantillas y workflow siguen siendo válidas para todos los perfiles

### Nuevo o cambio de perfil

- [ ] Sigue [core/templates/profile-template.md](../../../core/templates/profile-template.md)
- [ ] Incluye `sdd.config.yaml`, checklist, spec-impact, deploy, ejemplo SDD-001
- [ ] Entrada en `bootstrap/agent-prompts/stack-descriptions.json`
- [ ] Sin reglas de negocio de un proyecto específico

### Bootstrap y CLI

- [ ] Python 3.10+; sin dependencias externas obligatorias nuevas sin justificación
- [ ] Cambios en agent-prompts sincronizados con `bootstrap/cursor-rules/` vía `sync-cursor-rules.py`

### Documentación

- [ ] Español latino (Chile)
- [ ] Enlaces relativos; sin duplicar contenido entre core y perfiles

---

## Glosario

| Término              | Definición                                                            |
| -------------------- | --------------------------------------------------------------------- |
| **Kit**              | Este repositorio: metodología + perfiles + herramientas               |
| **Instancia SDD**    | `.github/docs/sdd/` en un proyecto (BACKLOG, specs, config)           |
| **Consumidor**       | Proyecto que instala el kit como submodule                            |
| **Mantenedor**       | Quien evoluciona el repositorio sdd-kit                               |
| **Perfil**           | Adaptación SDD a un stack (`profiles/<nombre>/`)                      |
| **Pre-SDD**          | Trabajo hecho antes de adoptar el ciclo formal (ID `—` en BACKLOG)    |
| **Release producto** | `docs/releases/vX.Y.Z.md` — notas SemVer para consumidores del kit    |
| **Release campaña**  | `.github/docs/sdd/releases/vX.Y.Z/` — acta SDD de una versión del kit |
| **Dual-release**     | Cierre kit exige nota producto + acta con enlace (SDD-011)            |

---

## Qué no aplica

Reglas típicas de apps de negocio (roles de usuario final, filtrado por tenant, periodos fiscales) **no aplican** al kit. Si un spec del kit las menciona por error, marcar "No aplica".
